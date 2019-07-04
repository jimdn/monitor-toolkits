# libmonitor
libmonitor is a c/c++ package that you can easily report metrics to shm.
***
libmonitor是一个c/c++库，用于业务程序上报属性监控量，如请求量、失败量、超时量，使用率等。属性监控值上报到本地的共享内存，所以执行效率非常高。
[moni-exporter](https://github.com/jimdn/moni-exporter)会读取共享内存里面的值，并提供http接口供[prometheus](https://github.com/prometheus/prometheus)采集。


### Dependencies

- linux 64bit platform
- gcc version 4.4.6+


### 使用示例：
see examples

