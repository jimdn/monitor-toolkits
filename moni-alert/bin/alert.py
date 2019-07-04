#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
path = os.path.abspath(os.curdir)
path = path + '/third'
sys.path.append(path)

import comm.log
logger = comm.log.Logger('/data/log/moni-alert/alert.log', comm.log.WARNING)

class GlobalConfig:
    host = "127.0.0.1"
    port = 9198
    sms_send = True
    sms_appid = 0
    sms_appkey = ""
    sms_phone_nums = {}

def ParseConfig(cfgfile):
    try:
        file = open(cfgfile, "rb")
        v = json.load(file)
    except Exception as err:
        print(err)
    else:
        if "Host" in v:
            GlobalConfig.host = v["Host"]
        if "Port" in v:
            GlobalConfig.port = v["Port"]
        if "SmsSend" in v:
            GlobalConfig.sms_send = v["SmsSend"]
        if "SmsAppId" in v:
            GlobalConfig.sms_appid = v["SmsAppId"]
        if "SmsAppKey" in v:
            GlobalConfig.sms_appkey = v["SmsAppKey"]
        if "SmsPhoneNums" in v:
            GlobalConfig.sms_phone_nums = v["SmsPhoneNums"]


from qcloudsms_py import SmsMultiSender
from qcloudsms_py.httpclient import HTTPError
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/alerts', methods=['POST'])
def AlertHandler():
    body = request.get_data()
    logger.debug(body)
    try:
        v = json.loads(body)
    except Exception as err:
        logger.warn("json decode error, err=%s, body=%s" % (err, body))
        return '{"code":1,"msg":"json decode error"}'
    else:
        if "state" in v and v["state"] == "alerting":
            if "evalMatches" in v:
                value_str = ""
                for i in range(len(v["evalMatches"])):
                    if "value" not in v["evalMatches"][i]:
                        continue
                    value = v["evalMatches"][i]["value"]
                    if value < 0:
                        # value如果小于0表明数据回退了，这里忽略告警
                        return '{"code":0,"msg":"ok"}'
                    if "tags" not in v["evalMatches"][i]:
                        if value_str == "":
                            value_str += "当前值%d已超出" % value
                        else:
                            value_str += "，当前值%d已超出" % value
                    else:
                        tags = v["evalMatches"][i]["tags"]
                        if "host" in tags:
                            host = tags["host"]
                            if value_str == "":
                                value_str += "%s当前值%d已超出" % (host, value)
                            else:
                                value_str += "，%s当前值%d已超出" % (host, value)
                        else:
                            if value_str == "":
                                value_str += "当前值%d已超出" % value
                            else:
                                value_str += "，当前值%d已超出" % value

                rule_name = ""
                if "ruleName" in v:
                    rule_name = v["ruleName"]
                else:
                    return '{"code":2,"msg":"missing ruleName"}'

                alert_str = "%s，%s" % (rule_name, value_str)
                time_str = " [" + time.strftime('%m-%d %H:%M', time.localtime(time.time())) + "]"
                msg = alert_str + time_str
                logger.warn(msg)

                # message目前保存的是负责人,多个负责人用;分隔
                message = ""
                if "message" in v:
                    message = v["message"]
                managers = message.split(";")
                phone_nums = []
                for i in range(len(managers)):
                    person = managers[i]
                    if person in GlobalConfig.sms_phone_nums:
                        phone_num = GlobalConfig.sms_phone_nums[person]
                        phone_nums.append(phone_num)
                if GlobalConfig.sms_send == True and len(phone_nums) > 0:
                    msender = SmsMultiSender(GlobalConfig.sms_appid, GlobalConfig.sms_appkey)
                    try:
                        result = msender.send(0, "86", phone_nums, msg)
                    except HTTPError as e:
                        logger.warn("msender err=%s" % e)
                    except Exception as e:
                        logger.warn("msender err=" % e)
        return '{"code":0,"msg":"ok"}'

if __name__ == "__main__":
    # encoding
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # config
    cfgfile = "../conf/alert.conf"
    if len(sys.argv) >= 2:
        conf_file = sys.argv[1]
    ParseConfig(cfgfile)
    # business
    app.run(host=GlobalConfig.host, port=GlobalConfig.port)
