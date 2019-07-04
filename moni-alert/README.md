moni-alert
=======================
moni-alert is a component that receives the Grafana alert and sends SMS.
SMS is based on Qcloud SMS.
***
moni-alert是一个接收Grafana告警的组件，收到告警后会发送短信，短信服务基于腾讯云短信。


### Dependencies

- linux 64bit platform
- python 2.7


### How to use
Copy the whole dir `moni-alert` to your server:
```
# mkdir -p /data/log/moni-alert
# cd moni-alert/bin
# nohup python alert.py ../conf/alert.conf >> /data/log/moni-alert/nohup.log 2>&1 &
```
