RELEASE_DIR=moni-exporter

all: prepare
	go build -o $(RELEASE_DIR)/bin/moni-exporter ./exporter.go
	go build -o $(RELEASE_DIR)/tools/rpt-counter ./report_counter.go
	go build -o $(RELEASE_DIR)/tools/rpt-gauge ./report_gauge.go
	@ cp -p moni-exporter.toml $(RELEASE_DIR)/conf
	@ cp -p svrmonitor.py $(RELEASE_DIR)/tools

prepare:
	@ [ -d $(RELEASE_DIR) ] || mkdir -p $(RELEASE_DIR)
	@ [ -d $(RELEASE_DIR)/bin ] || mkdir -p $(RELEASE_DIR)/bin
	@ [ -d $(RELEASE_DIR)/conf ] || mkdir -p $(RELEASE_DIR)/conf
	@ [ -d $(RELEASE_DIR)/tools ] || mkdir -p $(RELEASE_DIR)/tools

clean:
	rm -rf $(RELEASE_DIR)

.PHONY: all clean prepare
