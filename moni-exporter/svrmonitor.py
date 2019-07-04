#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import division
import sys
import re
import os
import math
import glob
import platform
import traceback
from time import time, sleep


g_attr = {
    # /proc/net/dev statistics
    'eth0_in_pkg':            {'type': 'gauge', 'id': 10001, 'desc': 'pkg/s'},
    'eth0_out_pkg':           {'type': 'gauge', 'id': 10002, 'desc': 'pkg/s'},
    'eth0_in_traff':          {'type': 'gauge', 'id': 10003, 'desc': 'bits/s'},
    'eth0_out_traff':         {'type': 'gauge', 'id': 10004, 'desc': 'bits/s'},
    'eth1_in_pkg':            {'type': 'gauge', 'id': 10011, 'desc': 'pkg/s'},
    'eth1_out_pkg':           {'type': 'gauge', 'id': 10012, 'desc': 'pkg/s'},
    'eth1_in_traff':          {'type': 'gauge', 'id': 10013, 'desc': 'bits/s'},
    'eth1_out_traff':         {'type': 'gauge', 'id': 10014, 'desc': 'bits/s'},
    'bond0_in_pkg':           {'type': 'gauge', 'id': 10021, 'desc': 'pkg/s'},
    'bond0_out_pkg':          {'type': 'gauge', 'id': 10022, 'desc': 'pkg/s'},
    'bond0_in_traff':         {'type': 'gauge', 'id': 10023, 'desc': 'bits/s'},
    'bond0_out_traff':        {'type': 'gauge', 'id': 10024, 'desc': 'bits/s'},
    'bond1_in_pkg':           {'type': 'gauge', 'id': 10031, 'desc': 'pkg/s'},
    'bond1_out_pkg':          {'type': 'gauge', 'id': 10032, 'desc': 'pkg/s'},
    'bond1_in_traff':         {'type': 'gauge', 'id': 10033, 'desc': 'bits/s'},
    'bond1_out_traff':        {'type': 'gauge', 'id': 10034, 'desc': 'bits/s'},
    # CPU usage
    'cpu':                    {'type': 'gauge', 'id': 20000, 'desc': '%'},
    'cpu0':                   {'type': 'gauge', 'id': 20001, 'desc': '%'},
    'cpu1':                   {'type': 'gauge', 'id': 20002, 'desc': '%'},
    'cpu2':                   {'type': 'gauge', 'id': 20003, 'desc': '%'},
    'cpu3':                   {'type': 'gauge', 'id': 20004, 'desc': '%'},
    'cpu4':                   {'type': 'gauge', 'id': 20005, 'desc': '%'},
    'cpu5':                   {'type': 'gauge', 'id': 20006, 'desc': '%'},
    'cpu6':                   {'type': 'gauge', 'id': 20007, 'desc': '%'},
    'cpu7':                   {'type': 'gauge', 'id': 20008, 'desc': '%'},
    'cpu8':                   {'type': 'gauge', 'id': 20009, 'desc': '%'},
    'cpu9':                   {'type': 'gauge', 'id': 20010, 'desc': '%'},
    'cpu10':                  {'type': 'gauge', 'id': 20011, 'desc': '%'},
    'cpu11':                  {'type': 'gauge', 'id': 20012, 'desc': '%'},
    'cpu12':                  {'type': 'gauge', 'id': 20013, 'desc': '%'},
    'cpu13':                  {'type': 'gauge', 'id': 20014, 'desc': '%'},
    'cpu14':                  {'type': 'gauge', 'id': 20015, 'desc': '%'},
    'cpu15':                  {'type': 'gauge', 'id': 20016, 'desc': '%'},
    'cpu16':                  {'type': 'gauge', 'id': 20017, 'desc': '%'},
    'cpu17':                  {'type': 'gauge', 'id': 20018, 'desc': '%'},
    'cpu18':                  {'type': 'gauge', 'id': 20019, 'desc': '%'},
    'cpu19':                  {'type': 'gauge', 'id': 20020, 'desc': '%'},
    'cpu20':                  {'type': 'gauge', 'id': 20021, 'desc': '%'},
    'cpu21':                  {'type': 'gauge', 'id': 20022, 'desc': '%'},
    'cpu22':                  {'type': 'gauge', 'id': 20023, 'desc': '%'},
    'cpu23':                  {'type': 'gauge', 'id': 20024, 'desc': '%'},
    'cpu24':                  {'type': 'gauge', 'id': 20025, 'desc': '%'},
    'cpu25':                  {'type': 'gauge', 'id': 20026, 'desc': '%'},
    'cpu26':                  {'type': 'gauge', 'id': 20027, 'desc': '%'},
    'cpu27':                  {'type': 'gauge', 'id': 20028, 'desc': '%'},
    'cpu28':                  {'type': 'gauge', 'id': 20029, 'desc': '%'},
    'cpu29':                  {'type': 'gauge', 'id': 20030, 'desc': '%'},
    'cpu30':                  {'type': 'gauge', 'id': 20031, 'desc': '%'},
    'cpu31':                  {'type': 'gauge', 'id': 20032, 'desc': '%'},
    'cpu32':                  {'type': 'gauge', 'id': 20033, 'desc': '%'},
    'cpu33':                  {'type': 'gauge', 'id': 20034, 'desc': '%'},
    'cpu34':                  {'type': 'gauge', 'id': 20035, 'desc': '%'},
    'cpu35':                  {'type': 'gauge', 'id': 20036, 'desc': '%'},
    'cpu36':                  {'type': 'gauge', 'id': 20037, 'desc': '%'},
    'cpu37':                  {'type': 'gauge', 'id': 20038, 'desc': '%'},
    'cpu38':                  {'type': 'gauge', 'id': 20039, 'desc': '%'},
    'cpu39':                  {'type': 'gauge', 'id': 20040, 'desc': '%'},
    'cpu40':                  {'type': 'gauge', 'id': 20041, 'desc': '%'},
    'cpu41':                  {'type': 'gauge', 'id': 20042, 'desc': '%'},
    'cpu42':                  {'type': 'gauge', 'id': 20043, 'desc': '%'},
    'cpu43':                  {'type': 'gauge', 'id': 20044, 'desc': '%'},
    'cpu44':                  {'type': 'gauge', 'id': 20045, 'desc': '%'},
    'cpu45':                  {'type': 'gauge', 'id': 20046, 'desc': '%'},
    'cpu46':                  {'type': 'gauge', 'id': 20047, 'desc': '%'},
    'cpu47':                  {'type': 'gauge', 'id': 20048, 'desc': '%'},
    # memory usage
    'mem_total':              {'type': 'gauge', 'id': 30000, 'desc': 'Bytes'},
    'mem_used':               {'type': 'gauge', 'id': 30001, 'desc': 'Bytes'},
    'mem_free':               {'type': 'gauge', 'id': 30002, 'desc': 'Bytes'},
    'shm_num':                {'type': 'gauge', 'id': 30003, 'desc': '-'},
    'shm_use':                {'type': 'gauge', 'id': 30004, 'desc': '-'},
    'dev_shm_size':           {'type': 'gauge', 'id': 30005, 'desc': 'Bytes'},
    'dev_shm_use':            {'type': 'gauge', 'id': 30006, 'desc': 'Bytes'},
    # swap
    'swap_total':             {'type': 'gauge', 'id': 31001, 'desc': 'Bytes'},
    'swap_free':              {'type': 'gauge', 'id': 31002, 'desc': 'Bytes'},
    'swap_in':                {'type': 'gauge', 'id': 31003, 'desc': 'Bytes/s'},
    'swap_out':               {'type': 'gauge', 'id': 31004, 'desc': 'Bytes/s'},
    # hard disk usage
    '/':                      {'type': 'gauge', 'id': 40001, 'desc': '%'},
    '/usr/local':             {'type': 'gauge', 'id': 40002, 'desc': '%'},
    '/data':                  {'type': 'gauge', 'id': 40003, 'desc': '%'},
    '/data1':                 {'type': 'gauge', 'id': 40004, 'desc': '%'},
    '/data2':                 {'type': 'gauge', 'id': 40005, 'desc': '%'},
    '/data3':                 {'type': 'gauge', 'id': 40006, 'desc': '%'},
    '/data4':                 {'type': 'gauge', 'id': 40007, 'desc': '%'},
    '/data5':                 {'type': 'gauge', 'id': 40008, 'desc': '%'},
    '/data6':                 {'type': 'gauge', 'id': 40009, 'desc': '%'},
    '/data7':                 {'type': 'gauge', 'id': 40010, 'desc': '%'},
    '/data8':                 {'type': 'gauge', 'id': 40011, 'desc': '%'},
    '/ssd/data':              {'type': 'gauge', 'id': 40012, 'desc': '%'},
    '/ssd/data1':             {'type': 'gauge', 'id': 40013, 'desc': '%'},
    '/ssd/data2':             {'type': 'gauge', 'id': 40014, 'desc': '%'},
    '/ssd/data3':             {'type': 'gauge', 'id': 40015, 'desc': '%'},
    '/ssd/data4':             {'type': 'gauge', 'id': 40016, 'desc': '%'},
    '/ssd/data5':             {'type': 'gauge', 'id': 40017, 'desc': '%'},
    '/ssd/data6':             {'type': 'gauge', 'id': 40018, 'desc': '%'},
    '/ssd/data7':             {'type': 'gauge', 'id': 40019, 'desc': '%'},
    '/ssd/data8':             {'type': 'gauge', 'id': 40020, 'desc': '%'},
    # hard disk io usage
    'sda_rio':                {'type': 'gauge', 'id': 41001, 'desc': 'sda每秒读请求(次/秒)'},
    'sda_wio':                {'type': 'gauge', 'id': 41002, 'desc': 'sda每秒写请求(次/秒)'},
    'sda_rsect':              {'type': 'gauge', 'id': 41003, 'desc': 'sda磁盘io读(KB/s)'},
    'sda_wsect':              {'type': 'gauge', 'id': 41004, 'desc': 'sda磁盘io写(KB/s)'},
    'sda_await':              {'type': 'gauge', 'id': 41005, 'desc': 'sda平均每次I/O操作的等待时间(微秒)'},
    'sda_svctm':              {'type': 'gauge', 'id': 41006, 'desc': 'sda平均每次I/O操作的服务时间(微秒)'},
    'sdb_rio':                {'type': 'gauge', 'id': 41011, 'desc': 'sdb每秒读请求(次/秒)'},
    'sdb_wio':                {'type': 'gauge', 'id': 41012, 'desc': 'sdb每秒写请求(次/秒)'},
    'sdb_rsect':              {'type': 'gauge', 'id': 41013, 'desc': 'sdb磁盘io读(KB/s)'},
    'sdb_wsect':              {'type': 'gauge', 'id': 41014, 'desc': 'sdb磁盘io写(KB/s)'},
    'sdb_await':              {'type': 'gauge', 'id': 41015, 'desc': 'sdb平均每次I/O操作的等待时间(微秒)'},
    'sdb_svctm':              {'type': 'gauge', 'id': 41016, 'desc': 'sdb平均每次I/O操作的服务时间(微秒)'},
    'sdc_rio':                {'type': 'gauge', 'id': 41021, 'desc': 'sdc每秒读请求(次/秒)'},
    'sdc_wio':                {'type': 'gauge', 'id': 41022, 'desc': 'sdc每秒写请求(次/秒)'},
    'sdc_rsect':              {'type': 'gauge', 'id': 41023, 'desc': 'sdc磁盘io读(KB/s)'},
    'sdc_wsect':              {'type': 'gauge', 'id': 41024, 'desc': 'sdc磁盘io写(KB/s)'},
    'sdc_await':              {'type': 'gauge', 'id': 41025, 'desc': 'sdc平均每次I/O操作的等待时间(微秒)'},
    'sdc_svctm':              {'type': 'gauge', 'id': 41026, 'desc': 'sdc平均每次I/O操作的服务时间(微秒)'},
    'sdd_rio':                {'type': 'gauge', 'id': 41031, 'desc': 'sdd每秒读请求(次/秒)'},
    'sdd_wio':                {'type': 'gauge', 'id': 41032, 'desc': 'sdd每秒写请求(次/秒)'},
    'sdd_rsect':              {'type': 'gauge', 'id': 41033, 'desc': 'sdd磁盘io读(KB/s)'},
    'sdd_wsect':              {'type': 'gauge', 'id': 41034, 'desc': 'sdd磁盘io写(KB/s)'},
    'sdd_await':              {'type': 'gauge', 'id': 41035, 'desc': 'sdd平均每次I/O操作的等待时间(微秒)'},
    'sdd_svctm':              {'type': 'gauge', 'id': 41036, 'desc': 'sdd平均每次I/O操作的服务时间(微秒)'},
    'sde_rio':                {'type': 'gauge', 'id': 41041, 'desc': 'sda每秒读请求(次/秒)'},
    'sde_wio':                {'type': 'gauge', 'id': 41042, 'desc': 'sda每秒写请求(次/秒)'},
    'sde_rsect':              {'type': 'gauge', 'id': 41043, 'desc': 'sda磁盘io读(KB/s)'},
    'sde_wsect':              {'type': 'gauge', 'id': 41044, 'desc': 'sda磁盘io写(KB/s)'},
    'sde_await':              {'type': 'gauge', 'id': 41045, 'desc': 'sda平均每次I/O操作的等待时间(微秒)'},
    'sde_svctm':              {'type': 'gauge', 'id': 41046, 'desc': 'sda平均每次I/O操作的服务时间(微秒)'},
    'sdf_rio':                {'type': 'gauge', 'id': 41051, 'desc': 'sda每秒读请求(次/秒)'},
    'sdf_wio':                {'type': 'gauge', 'id': 41052, 'desc': 'sda每秒写请求(次/秒)'},
    'sdf_rsect':              {'type': 'gauge', 'id': 41053, 'desc': 'sda磁盘io读(KB/s)'},
    'sdf_wsect':              {'type': 'gauge', 'id': 41054, 'desc': 'sda磁盘io写(KB/s)'},
    'sdf_await':              {'type': 'gauge', 'id': 41055, 'desc': 'sda平均每次I/O操作的等待时间(微秒)'},
    'sdf_svctm':              {'type': 'gauge', 'id': 41056, 'desc': 'sda平均每次I/O操作的服务时间(微秒)'},
    'sdg_rio':                {'type': 'gauge', 'id': 41061, 'desc': 'sda每秒读请求(次/秒)'},
    'sdg_wio':                {'type': 'gauge', 'id': 41062, 'desc': 'sda每秒写请求(次/秒)'},
    'sdg_rsect':              {'type': 'gauge', 'id': 41063, 'desc': 'sda磁盘io读(KB/s)'},
    'sdg_wsect':              {'type': 'gauge', 'id': 41064, 'desc': 'sda磁盘io写(KB/s)'},
    'sdg_await':              {'type': 'gauge', 'id': 41065, 'desc': 'sda平均每次I/O操作的等待时间(微秒)'},
    'sdg_svctm':              {'type': 'gauge', 'id': 41066, 'desc': 'sda平均每次I/O操作的服务时间(微秒)'},
    'sdh_rio':                {'type': 'gauge', 'id': 41071, 'desc': 'sda每秒读请求(次/秒)'},
    'sdh_wio':                {'type': 'gauge', 'id': 41072, 'desc': 'sda每秒写请求(次/秒)'},
    'sdh_rsect':              {'type': 'gauge', 'id': 41073, 'desc': 'sda磁盘io读(KB/s)'},
    'sdh_wsect':              {'type': 'gauge', 'id': 41074, 'desc': 'sda磁盘io写(KB/s)'},
    'sdh_await':              {'type': 'gauge', 'id': 41075, 'desc': 'sda平均每次I/O操作的等待时间(微秒)'},
    'sdh_svctm':              {'type': 'gauge', 'id': 41076, 'desc': 'sda平均每次I/O操作的服务时间(微秒)'},
    # Ip statistics
    'Ip_InReceives':          {'type': 'gauge', 'id': 50001, 'desc': 'IP统计-入包总数(pkg/m)'},
    'Ip_InHdrErrors':         {'type': 'gauge', 'id': 50002, 'desc': 'IP统计-入包头错误(pkg/m)'},
    'Ip_InDiscards':          {'type': 'gauge', 'id': 50003, 'desc': 'IP统计-入包丢包(pkg/m)'},
    'Ip_InDelivers':          {'type': 'gauge', 'id': 50004, 'desc': 'IP统计-入包送达上层协议(pkg/m)'},
    'Ip_OutRequests':         {'type': 'gauge', 'id': 50005, 'desc': 'IP统计-出包总数(pkg/m)'},
    'Ip_OutDiscards':         {'type': 'gauge', 'id': 50006, 'desc': 'IP统计-出包丢包(pkg/m)'},
    'Ip_ReasmTimeout':        {'type': 'gauge', 'id': 50007, 'desc': 'IP统计-分片重组超时(每分钟)'},
    'Ip_ReasmReqds':          {'type': 'gauge', 'id': 50008, 'desc': 'IP统计-入包需重组(每分钟)'},
    'Ip_ReasmOKs':            {'type': 'gauge', 'id': 50009, 'desc': 'IP统计-分片重组成功(每分钟)'},
    'Ip_ReasmFails':          {'type': 'gauge', 'id': 50010, 'desc': 'IP统计-分片重组失败(每分钟)'},
    'Ip_FragOKs':             {'type': 'gauge', 'id': 50011, 'desc': 'IP统计-分片成功(每分钟)'},
    'Ip_FragFails':           {'type': 'gauge', 'id': 50012, 'desc': 'IP统计-分片失败(每分钟)'},
    'Ip_FragCreates':         {'type': 'gauge', 'id': 50013, 'desc': 'IP统计-创建分片数(每分钟)'},
    # Tcp statistics
    'Tcp_InSegs':             {'type': 'gauge', 'id': 51001, 'desc': 'TCP统计-TCP Received(pkg/s)'},
    'Tcp_OutSegs':            {'type': 'gauge', 'id': 51002, 'desc': 'TCP统计-TCP Sent(pkg/s)'},
    'Tcp_CurrEstab':          {'type': 'gauge', 'id': 51003, 'desc': 'TCP统计-TCP当前连接数'},
    'Tcp_NewEstab':           {'type': 'gauge', 'id': 51004, 'desc': 'TCP统计-TCP连接变化数(新增or减少)'},
    'Tcp_ActiveOpens':        {'type': 'gauge', 'id': 51005, 'desc': 'TCP统计-服务器主动连接的TCP数(每分钟)'},
    'Tcp_PassiveOpens':       {'type': 'gauge', 'id': 51006, 'desc': 'TCP统计-服务器接收TCP连接数(每分钟)'},
    'Tcp_AttemptFails':       {'type': 'gauge', 'id': 51007, 'desc': 'TCP统计-TCP连接建立时被对方重置(每分钟)'},
    'Tcp_RetransSegs':        {'type': 'gauge', 'id': 51008, 'desc': 'TCP统计-TCP报文重传数(pkg/m)'},
    'Tcp_RetransRatio':       {'type': 'gauge', 'id': 51009, 'desc': 'TCP统计-TCP重传率(%,当前分钟)'},
    'Tcp_InErrs':             {'type': 'gauge', 'id': 51010, 'desc': 'TCP统计-TCP入包错误(pkg/m,通常是校验错误)'},
    'Tcp_TcpInCsumErrors':    {'type': 'gauge', 'id': 51011, 'desc': 'TCP统计-TCP入包校验错误(pkg/m)'},
    "Tcp_OutRsts":            {'type': 'gauge', 'id': 51012, 'desc': 'TCP统计-TCP发送重置包(pkg/m)'},
    "Tcp_EstabResets":        {'type': 'gauge', 'id': 51013, 'desc': 'TCP统计-TCP已建立的连接被重置(每分钟)'},
    'TcpExt_ListenOverflows': {'type': 'gauge', 'id': 51014, 'desc': 'TCP统计-TCP监听队列溢出(每分钟)'},
    'TcpExt_TCPTimeouts':     {'type': 'gauge', 'id': 51015, 'desc': 'TCP统计-TCP超时(每分钟)'},
    # Udp statistics
    'Udp_InDatagrams':        {'type': 'gauge', 'id': 52001, 'desc': 'UDP统计-UDP Received(pkg/s)'},
    'Udp_OutDatagrams':       {'type': 'gauge', 'id': 52002, 'desc': 'UDP统计-UDP Sent(pkg/s)'},
    'Udp_InErrors':           {'type': 'gauge', 'id': 52003, 'desc': 'UDP统计-UDP InErrors(pkg/m)'},
    'Udp_NoPorts':            {'type': 'gauge', 'id': 52004, 'desc': 'UDP统计-UDP NoPorts(pkg/m)'},
    'Udp_InCsumErrors':       {'type': 'gauge', 'id': 52005, 'desc': 'UDP统计-UDP InCsumErrors(pkg/m)'},
    'Udp_RcvbufErrors':       {'type': 'gauge', 'id': 52006, 'desc': 'UDP统计-UDP RcvbufErrors(pkg/m)'},
    'Udp_SndbufErrors':       {'type': 'gauge', 'id': 52007, 'desc': 'UDP统计-UDP SndbufErrors(pkg/m)'},
    # Icmp statistic
    'Icmp_InDestUnreachs':    {'type': 'gauge', 'id': 53001, 'desc': 'ICMP统计-收到目标不可达消息(pkg/m)'},
    'Icmp_OutDestUnreachs':   {'type': 'gauge', 'id': 53002, 'desc': 'ICMP统计-发送目标不可达消息(pkg/m)'},
    # File descriptor statistics
    'fd_used':                {'type': 'gauge', 'id': 60001, 'desc': '文件句柄-已分配使用数'},
    'fd_unuse':               {'type': 'gauge', 'id': 60002, 'desc': '文件句柄-已分配未使用数'},
    'fd_max':                 {'type': 'gauge', 'id': 60003, 'desc': '文件句柄-系统最大数'},
    # Process information
    'total_process':          {'type': 'gauge', 'id': 70001, 'desc': '进程统计-总进程数'},
    'procs_running':          {'type': 'gauge', 'id': 70002, 'desc': '进程统计-可运行进程数'},
    'procs_blocked':          {'type': 'gauge', 'id': 70003, 'desc': '进程统计-阻塞中进程数'},
    'new_process':            {'type': 'gauge', 'id': 70004, 'desc': '进程统计-新创建进程数(每分钟)'},
}


class BaseProcessor(object):
    """
    Base Processor for collecting and reporting data.
    All specific instance should inherit from this class.
    """
    def __init__(self, interval):
        # time to sleep (seconds)
        # result1 is the result before sleep
        # result2 is the result after sleep
        self.interval = interval
        self.result1 = {}
        self.result2 = {}

    def collect(self):
        """
        Implemented by subclasses
        There are 2 kinds of return value: 
        result = {'key1': v1, 'key2': v2, ...}
        result = {'key1': [v1, v2, ...], 'key2': [v1, v2, ...], ...}
        """
        return {}

    def process(self):
        """
        If interval is zero, return instantaneous value
        If interval is not zero, return increasing value
        There are 2 kinds of return value: 
        result = {'key1': v1, 'key2': v2, ...}
        result = {'key1': [v1, v2, ...], 'key2': [v1, v2, ...], ...}
        """
        result = self.collect()
        self.result1 = result.copy()
        if self.interval > 0:
            sleep(self.interval)
            self.result2 = self.collect()
            if type(self.result1) == dict and type(self.result2) == dict and len(self.result1) > 0 and len(self.result2) > 0:
                for key in self.result2.keys():
                    if type(self.result2[key]) == list:
                        for i in range(len(self.result2[key])):
                            try:
                                tmp = int(self.result2[key][i]) - int(self.result1[key][i])
                            except Exception:
                                print(traceback.format_exc())
                                tmp = 0
                            if tmp < 0:
                                result[key][i] = tmp + 4294967296
                            else:
                                result[key][i] = tmp
                    else:
                        try:
                            tmp = int(self.result2[key]) - int(self.result1[key])
                        except Exception:
                            print(traceback.format_exc())
                            tmp = 0
                        if tmp < 0:
                            result[key] = tmp + 4294967296
                        else:
                            result[key] = tmp
        return result

    def report(self):
        """
        Report to shm
        """
        global g_attr
        result = self.process()
        if len(result) > 0:
            for key in result.keys():
                if key not in g_attr:
                    continue
                typ = g_attr[key]["type"]
                attrid = g_attr[key]["id"]
                value = result[key]
                if typ == "counter":
                    tool = "%s/%s" % (os.path.split(os.path.realpath(__file__))[0], 'rpt-counter')
                    cmd = "%s %s %d" % (tool, str(attrid).strip(), value)
                    os.system(cmd)
                    # print("(%s) %s" % (key, cmd))
                elif typ == "gauge":
                    tool = "%s/%s" % (os.path.split(os.path.realpath(__file__))[0], 'rpt-gauge')
                    cmd = "%s %s %d" % (tool, str(attrid).strip(), value)
                    os.system(cmd)
                    # print("(%s) %s" % (key, cmd))


class NetTraffic(BaseProcessor):
    """
    Get network traffic information
    Calculate by: /proc/net/dev
    """
    def collect(self):
        fd = open("/proc/net/dev")
        sep = re.compile(r'[:\s]+')
        traffic_dict = {}
        for line in fd:
            # skip header line
            if ":" not in line: continue
            fields = sep.split(line.strip())
            intf = fields.pop(0)
            traffic_dict[intf + "_in_traff"] = int(fields[0])
            traffic_dict[intf + "_in_pkg"] = int(fields[1])
            traffic_dict[intf + "_out_traff"] = int(fields[8+0])
            traffic_dict[intf + "_out_pkg"] = int(fields[8+1])
        fd.close()
        return traffic_dict

    def process(self):
        result = {}
        base_result = super(NetTraffic, self).process()
        for key in base_result.keys():
            try:
                if "traff" in key:
                    # traffic ( bits/s ) = bytes * 8 / 60
                    result[key] = int(math.ceil(int(base_result[key]) * 8 / self.interval))
                elif "pkg" in key:
                    # traffic ( pkg/s ) = pkg / 60
                    result[key] = int(math.ceil(int(base_result[key]) / self.interval))
            except Exception:
                print(traceback.format_exc())
                result[key] = 0
        return result


class CpuUsage(BaseProcessor):
    """
    Get each CPU usage information
    Calculate by: /proc/stat
    """
    def collect(self):
        fd = open('/proc/stat')
        cpus_info_list = [ l for l in fd.readlines() if l.startswith('cpu') ]
        fd.close()
        cpus_use_dict = {}
        for line in cpus_info_list:
            cpu_list = line.split()
            cpus_use_dict[cpu_list[0]] = cpu_list[1:]
        return cpus_use_dict

    def process(self):
        result = {}
        base_result = super(CpuUsage, self).process()
        for key in base_result.keys():
            try:
                total = 0.0
                for item in base_result[key]:
                    total += float(item)
                # CPU Usage =  100 * (total - idle)/toal
                result[key] = int(math.ceil(100 * (total - base_result[key][3] - base_result[key][4]) / total))
            except Exception:
                print(traceback.format_exc())
                result[key] = 0
        return result


class MemUsage(BaseProcessor):
    '''
    Get memory usage information
    Calculate by: /proc/meminfo
    '''
    def collect(self):
        fd = open("/proc/meminfo")
        mem_info_list = fd.readlines()
        fd.close()
        mem_use_dict = {}
        for line in mem_info_list:
            tmp = line.split(":")
            try:
                mem_use_dict[tmp[0]] = int(tmp[1].split()[0])
            except Exception:
                print(traceback.format_exc())
                mem_use_dict[tmp[0]] = 0
        return mem_use_dict

    def process(self):
        result = {}
        base_result = super(MemUsage, self).process()
        if 'Mapped' in base_result:
            result['mem_free'] = int((base_result['MemFree'] + base_result['Cached'] - base_result['Dirty'] - base_result['Mapped'])) * 1024
        else:
            result['mem_free'] = int(base_result['MemFree']) * 1024
        result['mem_total'] = int(base_result['MemTotal']) * 1024
        result['mem_used'] = int(base_result['MemTotal']) * 1024 - result['mem_free']
        result['swap_total'] = int(base_result['SwapTotal']) * 1024
        result['swap_free'] = int(base_result['SwapFree']) * 1024
        return result


class ShmUsage(BaseProcessor):
    """
    Get shm usage information
    """
    def collect(self):
        cmd = "ipcs -mb | grep -E '^0x'"
        fd = os.popen(cmd)
        shm_list = fd.readlines()
        fd.close()
        shm_use_dict = {}
        shm_use_dict["shm_num"] = int(len(shm_list))
        use_bytes = 0
        for line in shm_list:
            tmp = line.split()
            use_bytes += int(tmp[4])
        shm_use_dict["shm_use"] = use_bytes
        return shm_use_dict


class PosixShmUsage(BaseProcessor):
    """
    Get posix shm usage information
    Calculate by: df -k
    """
    def collect(self):
        cmd = "df -k | grep /dev/shm"
        fd = os.popen(cmd)
        shm_list = fd.read().strip().split()
        fd.close()
        posix_shm_dict = {}
        posix_shm_dict['dev_shm_size'] = int(shm_list[1]) * 1024
        posix_shm_dict['dev_shm_use'] = int(shm_list[2]) * 1024
        return posix_shm_dict


class SwapUsage(BaseProcessor):
    """
    Get swap in and out amount
    Calculate by: /proc/vmstat
    """
    def collect(self):
        cmd = "grep -E '^(pswpin|pswpout)' /proc/vmstat"
        fd = os.popen(cmd)
        swap_list = fd.readlines()
        fd.close()
        swap_dict = {}
        for line in swap_list:
            tmp = line.split()
            try:
                swap_dict[tmp[0]] = int(tmp[1])
            except Exception:
                print(traceback.format_exc())
                swap_dict[tmp[0]] = 0
        return swap_dict

    def process(self):
        result = {}
        base_result = super(SwapUsage, self).process()
        result['swap_in'] = int(base_result['pswpin'] * 1024 / self.interval)
        result['swap_out'] = int(base_result['pswpout'] * 1024 / self.interval)
        return result


class HdUsage(BaseProcessor):
    """
    Get Hard disk use percentage
    """
    def collect(sef):
        cmd = 'df -k'
        fd = os.popen(cmd)
        re_obj = re.compile(r'^/dev/.+\s+(?P<used>\d+)%\s+(?P<mount>.+)')
        hd_use_dict = {}
        for line in fd:
            match = re_obj.search(line)
            if match is not None:
                hd_use_dict[match.groupdict()['mount']] = int(match.groupdict()['used'])
        fd.close()
        return hd_use_dict


class HdIoRatio(BaseProcessor):
    """
    Get hard disk IO usage
    """
    def collect(self):
        fd = open('/proc/diskstats')
        disk_io_list = fd.readlines()
        fd.close()
        disk_io_dict = {}
        if len(disk_io_list) > 0:
            for line in disk_io_list:
                io_list = line.split()
                disk_io_dict[io_list[2]] = io_list[3:]
        return disk_io_dict

    def process(self):
        hd_io_ratio_dict = {}
        base_result = super(HdIoRatio, self).process()
        for key in base_result.keys():
            hd_io_ratio_dict[key + '_rio'] = int(base_result[key][0] / self.interval)
            hd_io_ratio_dict[key + '_wio'] = int(base_result[key][4] / self.interval)
            # each sector is 512 bytes
            hd_io_ratio_dict[key + '_rsect'] = int(base_result[key][2] / self.interval / 2)
            hd_io_ratio_dict[key + '_wsect'] = int(base_result[key][6] / self.interval / 2)
            rw_num = base_result[key][0] + base_result[key][4]
            if rw_num == 0:
                hd_io_ratio_dict[key + '_await'] = 0
                hd_io_ratio_dict[key + '_svctm'] = 0
            else:
                hd_io_ratio_dict[key + '_await'] = int((base_result[key][3] + base_result[key][7]) * 1000 / rw_num)
                hd_io_ratio_dict[key + '_svctm'] = int(base_result[key][9] * 1000 / rw_num)
        return hd_io_ratio_dict


class NetSnmpIpTcpUdp(BaseProcessor):
    """
    IP statistics
    Calculate by: /proc/net/snmp & /proc/net/netstat
    """
    def collect(self):
        fd1 = open("/proc/net/snmp")
        fd2 = open("/proc/net/netstat")
        lines = fd1.readlines()
        lines.extend(fd2.readlines())
        fd1.close()
        fd2.close()
        snmp_dict = {}
        sep = re.compile(r'[:\s]+')
        n = 0
        for line in lines:
            n += 1
            fields = sep.split(line.strip())
            proto = fields.pop(0)
            if n % 2 == 1:
                # header line
                keys = []
                for field in fields:
                    key = "%s_%s" % (proto, field)
                    keys.append(key)
            else:
                # value line
                try:
                    values = [int(f) for f in fields]
                except Exception as e:
                    print(e)
                kv = dict(zip(keys, values))
                snmp_dict.update(kv)
        return snmp_dict

    def process(self):
        result = super(NetSnmpIpTcpUdp, self).process()
        # RetransRatio during this interval time
        if result['Tcp_OutSegs'] == 0:
            result['Tcp_RetransRatio'] = 0
        else:
            result['Tcp_RetransRatio'] = int(result['Tcp_RetransSegs'] * 100 / result['Tcp_OutSegs'])
        result['Tcp_NewEstab'] = result.pop('Tcp_CurrEstab', 0)
        if result['Tcp_NewEstab'] > 2147483648:
            result['Tcp_NewEstab'] = abs(result['Tcp_NewEstab'] - 4294967296)
        # CurrEstab is a tmp value, not inc/dec value
        result['Tcp_CurrEstab'] = self.result1['Tcp_CurrEstab']
        result['Tcp_InSegs'] = int(result['Tcp_InSegs'] / self.interval)
        result['Tcp_OutSegs'] = int(result['Tcp_OutSegs'] / self.interval)
        result['Udp_InDatagrams'] = int(result['Udp_InDatagrams'] / self.interval)
        result['Udp_OutDatagrams'] = int(result['Udp_OutDatagrams'] / self.interval)
        return result


class FdUsage(BaseProcessor):
    """
    Get file descriptor amount
    """
    def collect(self):
        tmp = open("/proc/sys/fs/file-nr").read().strip().split()
        fd_dict = {}
        fd_dict['fd_used'] = int(tmp[0])
        fd_dict['fd_unuse'] = int(tmp[1])
        fd_dict['fd_max'] = int(tmp[2])
        return fd_dict


class ProcessInfo(BaseProcessor):
    """
    Get process information
    """
    def collect(self):
        stat_dict = {}
        proc_dict = {}
        fd = open('/proc/stat')
        for line in fd:
            key, value = line.strip().split(None, 1)
            stat_dict[key] = value
        fd.close()
        keys = ('processes', 'procs_running','procs_blocked')
        for k in keys:
            proc_dict[k] = int(stat_dict[k])
        return proc_dict

    def process(self):
        result = super(ProcessInfo, self).process()
        result['total_process'] = len(glob.glob('/proc/*/stat'))
        result['procs_running'] = self.result2['procs_running']
        result['procs_blocked'] = self.result2['procs_blocked']
        result['new_process'] = result.pop('processes', 0)
        return result


if __name__ == "__main__":
    print(platform.python_version())
    start_time = time()
    print("Start Time: %s" % start_time)
    # key:   function class
    # value: sleep time (seconds)
    jobs = {
        NetTraffic: 60,
        CpuUsage: 5,
        MemUsage: 0,
        ShmUsage: 0,
        PosixShmUsage: 0,
        SwapUsage: 60,
        HdUsage: 0,
        HdIoRatio: 60,
        NetSnmpIpTcpUdp: 60,
        FdUsage: 0,
        ProcessInfo: 60,
    }

    child_pid_list = []
    for key in jobs.keys():
        try:
            pid = os.fork()
        except OSError:
            sys.exit("Unable to create child process!")
        if pid == 0:
            instance = key(jobs[key])
            instance.report()
            sys.exit(0)
        else:
            child_pid_list.append(pid)

    for pid in child_pid_list:
        os.wait()

    # calculate run time
    end_time = time()
    run_time = (int(end_time * 10) - int(start_time * 10)) / 10
    print("End Time: %s" % end_time)
    print("Cost Time: %ss" % run_time)
