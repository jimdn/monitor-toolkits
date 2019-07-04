package main

import (
	"fmt"
	"os"
	"path"
	"time"
	"sync"
	"io"
	"net"
	"strings"
	"errors"
	"syscall"
	"os/signal"
	"os/exec"
	"net/http"
	"sync/atomic"

	"moni-exporter/gomonitor"

	"github.com/BurntSushi/toml"
	"github.com/sirupsen/logrus"
	"github.com/gorilla/mux"
)


type appConfig struct {
	// Log param
	LogPath            string
	LogLevel           int
	// IP:Port or :Port
	ListenAddr         string
	LanIpPrefix        []string
	SvrMonitorFile     string
}

type appVariable struct {
	Log           *logrus.Logger
	HttpSvr       *http.Server
	LocalIp       string
	Exit          bool
	// Time(ms) for update cache
	AttrMtime     int64
	// AttrMapList : Cache for last 1 minute and 2 minute
	//   key   : attrId
	//   value : AttrValue
	AttrMapList   [2]sync.Map
	AttrMapIndex  int
	// Update lock
	AttrLock      *sync.RWMutex
}

// value contains a type(t) and value(v)
// type : 0-counter 1-gauge
type AttrValue struct {
	t int
	v int64
}

var (
	appCfg    appConfig
	appVar    appVariable
	appFiniCb []func()
)

func init() {
	appFiniCb = make([]func(), 0)
	appVar.Exit = false
	appVar.AttrMtime = 0
	appVar.AttrMapIndex = 0
	appVar.AttrLock = new(sync.RWMutex)
}

func appInit() error {
	// configuration set default & parse from file
	appCfg.LogPath = "/data/log/moni-exporter"
	appCfg.LogLevel = 3
	appCfg.ListenAddr = ":9108"
	appCfg.LanIpPrefix = []string{"9.", "10.", "100.", "172.", "192."}
	appCfg.SvrMonitorFile = "../tools/svrmonitor.py"
	cfgFile := "../conf/moni-exporter.toml"
	if len(os.Args) >= 2 {
		cfgFile = os.Args[1]
	}
	if _, err := toml.DecodeFile(cfgFile, &appCfg); err != nil {
		fmt.Printf("DecodeFile err: %v\n", err)
		return err
	}

	// get lan if ip
	ip, err := getLocalIp()
	if err != nil {
		fmt.Printf("Error getLocalIp: %v\n", err)
		return err
	}
	appVar.LocalIp = ip

	// log init
	name := path.Base(os.Args[0])
	logPath := path.Clean(appCfg.LogPath)
	logFile := fmt.Sprintf("%s/%s.log", logPath, name)
	if err := os.MkdirAll(logPath, 0755); err != nil {
		return err
	}
	file, err := os.OpenFile(logFile, os.O_WRONLY|os.O_APPEND|os.O_CREATE, 0666)
	if err != nil {
		fmt.Printf("OpenFile err: %v\n", err)
		return err
	}
	logger := logrus.New()
	logger.SetNoLock()
	logger.SetLevel(logrus.AllLevels[appCfg.LogLevel])
	logger.Out = file
	appVar.Log = logger

	// rounter
	router := mux.NewRouter()
	router.HandleFunc("/metrics", HandleMetrics)
	appVar.HttpSvr = &http.Server{
		Addr:         appCfg.ListenAddr,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
		Handler:      router,
	}
	return nil
}

func appFini() {
	for len(appFiniCb) > 0 {
		appFiniCb[len(appFiniCb)-1]()
		appFiniCb = appFiniCb[:len(appFiniCb)-1]
	}
}

func getLocalIp() (string, error) {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		return "", err
	}
	for _, addr := range addrs {
		if ipnet, ok := addr.(*net.IPNet); ok {
			if ipnet.IP.To4() != nil {
				ip := ipnet.IP.String()
				for _, prefix := range appCfg.LanIpPrefix {
					if strings.HasPrefix(ip, prefix) {
						return ip, nil
					}
				}
			}
		}
	}
	err = errors.New("no found")
	return "", err
}

func updateAttrCache() {
	appVar.AttrLock.Lock()
	defer appVar.AttrLock.Unlock()
	// update value (delete not exist key first)
	idxToUpdate := (appVar.AttrMapIndex + 1) % 2
	appVar.AttrMapList[idxToUpdate].Range(func(k, v interface{}) bool {
		key, _ := k.(int)
		if rc := gomonitor.Get(key); rc < 0 {
			appVar.AttrMapList[idxToUpdate].Delete(key)
		}
		return true
	})
	row := gomonitor.MaxRow()
	col := gomonitor.MaxCol()
	for rowIdx := 0; rowIdx < row; rowIdx++ {
		for colIdx := 0; colIdx < col; colIdx++ {
			id, t, v := gomonitor.AttrWalk(rowIdx, colIdx)
			if id > 0 && t >= 0 && v >= 0 {
				attrVal := AttrValue {
					t: t,
					v: v,
				}
				appVar.AttrMapList[idxToUpdate].Store(id, attrVal)
			}
		}
	}
	// update finished, change the index
	appVar.AttrMapIndex++
}

// HandleMetrics:
// HTTP endpoints for Prometheus
func HandleMetrics(w http.ResponseWriter, r *http.Request) {
	appVar.Log.Infof("receive req from %s", r.RemoteAddr)

	// update cache every minute
	now := time.Now().Unix()
	ms := (now / 60) * 60 * 1000
	if ms > appVar.AttrMtime {
		if atomic.CompareAndSwapInt64(&appVar.AttrMtime, appVar.AttrMtime, ms) {
			appVar.Log.Infof("update cache, before update AttrMapIndex=%d", appVar.AttrMapIndex)
			updateAttrCache()
		}
	}

	reportData := ""
	// monitor_0_value used to report local ip
	tmp := fmt.Sprintf("# HELP monitor_0_value n/a\n# TYPE monitor_0_value gauge\nmonitor_0_value{host=\"%s\"} 1\n", appVar.LocalIp)
	reportData += tmp

	appVar.AttrLock.RLock()
	defer appVar.AttrLock.RUnlock()

	idxToRead := appVar.AttrMapIndex % 2
	idxToCmp := (appVar.AttrMapIndex + 1) % 2
	isRestart := true
	if appVar.AttrMapIndex > 1 {
		isRestart = false
	}
	appVar.AttrMapList[idxToRead].Range(func(k, v interface{}) bool {
		key, _ := k.(int)
		val, _ := v.(AttrValue)
		switch val.t {
		case 0:
			// counter
			metricName := fmt.Sprintf("monitor_%d_total", key)
			helpStr := fmt.Sprintf("# HELP %s n/a\n", metricName)
			typeStr := fmt.Sprintf("# TYPE %s counter\n", metricName)
			reportData += fmt.Sprintf("%s%s", helpStr, typeStr)
			if !isRestart {
				// If report a non-zero counter straightly, delta(metric{lable="xxx"}[$interval]) will get zero result
				// To resolve this problem, we report a zero value in last 6 minite (to support $interval=5m)
				_, ok := appVar.AttrMapList[idxToCmp].Load(key)
				if !ok {
					for minute := int64(6); minute > 0; minute-- {
						valStr := fmt.Sprintf("%s{host=\"%s\"} %d %d\n", metricName, appVar.LocalIp, 0, appVar.AttrMtime - minute * 60 * 1000)
						reportData += fmt.Sprintf("%s", valStr)
					}
				}
			}
			valStr := fmt.Sprintf("%s{host=\"%s\"} %d %d\n", metricName, appVar.LocalIp, val.v, appVar.AttrMtime)
			reportData += fmt.Sprintf("%s", valStr)
		case 1:
			// gauge
			metricName := fmt.Sprintf("monitor_%d_value", key)
			helpStr := fmt.Sprintf("# HELP %s n/a\n", metricName)
			typeStr := fmt.Sprintf("# TYPE %s gauge\n", metricName)
			valStr := fmt.Sprintf("%s{host=\"%s\"} %d %d\n", metricName, appVar.LocalIp, val.v, appVar.AttrMtime)
			reportData += fmt.Sprintf("%s%s%s", helpStr, typeStr, valStr)
		}
		return true
	})
	io.WriteString(w, reportData)
}

// MonitorServerLoop:
// run script to monitor server base
// like network, cpu, mem, ...
func MonitorServerLoop() {
	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()
	for {
		if appVar.Exit {
			return
		}
		select {
		case <-ticker.C:
			go func() {
				appVar.Log.Warnf("cmd exec begin")
				cmd := exec.Command("/usr/bin/env", "python", appCfg.SvrMonitorFile)
				err := cmd.Run()
				if err != nil {
					appVar.Log.Warnf("cmd exec failed, err=%v", err)
				}
			}()
		}
	}
}


func main() {
	defer appFini()
	if err := appInit(); err != nil {
		fmt.Printf("appInit fail: %v\n", err)
		return
	}

	go func() {
		sigs := make(chan os.Signal, 1)
		signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
		switch sig := <-sigs; sig {
		default:
			{
				appVar.Log.Warnf("receive exit signal!")
				appVar.Exit = true
				appVar.HttpSvr.Shutdown(nil)
			}
		}
	}()

	go MonitorServerLoop()

	appVar.Log.Warnf("moni-exporter | server restart!")

	if err := appVar.HttpSvr.ListenAndServe(); err != nil {
		appVar.Log.Warnf("ListenAndServe err=%v", err)
	}

	appVar.Log.Warnf("moni-exporter | server stop!")
	return
}
