moni-exporter
=======================
moni-exporter is a exporter for Prometheus.
***
moni-exporter会每分钟读取上报到共享内存里面的监控值，并提供http接口由[prometheus](https://github.com/prometheus/prometheus)采集。
另外moni-exporter还会每分钟调取`svrmonitor.py`，监控服务器的基础属性如网卡流量、CPU、内存等，并把数据上报到共享内存。


### Dependencies

- linux 64bit platform
- gcc version 4.4.6+
- go version 1.12+


### How to use
Run `make all`, if succ will generate a dir named `moni-exporter`, copy moni-exporter dir to your server.

```
# mkdir -p /data/log/moni-exporter
# cd moni-exporter/bin
# nohup ./moni-exporter ../conf/moni-exporter.toml &
```
