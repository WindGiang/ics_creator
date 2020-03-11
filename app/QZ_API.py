#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import datetime

"""强智教务管理系统
   使用方法
      Q = SW(account, password)
    # Q.getStudentIdInfo() #获取学号信息
    # Q.getCurrentTime() #获取学年信息
    # Q.getKbcxAzc()  # 当前周次课表
    # Q.getKbcxAzc(zc) #指定周次课表
    # Q.getKxJscx("0304") #空教室查询 "allday"：全天 "am"：上午 "pm"：下午 "night"：晚上 "0102":1.2节空教室 "0304":3.4节空教室
    # Q.getCjcx("2018-2019-2") #成绩查询 #无参数查询全部成绩
    # Q.getKscx() #获取考试信息
    具体API文档可参考https://qzapi.github.tlingc.com/api/
    感谢贡献API
"""


class SW(object):

    def __init__(self, account, password):
        super(SW, self).__init__()
        self.account = account
        self.password = password
        self.session = self.login()

    isLogin = False
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Mobile; Android 6.0.1;C107-9 Build/FRF91 )',
        'Referer': 'http://www.baidu.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
        'cache-control': 'max-age=0'
    }
    '''
    DO NOT REMOVE OR MODIFY HEADERS ABOVE.
    '''
    ###############################################
    url = "http://jwxt.ahut.edu.cn/app.do"

    ###############################################

    def login(self):
        params = {
            "method": "authUser",
            "xh": self.account,
            "pwd": self.password
        }
        session = requests.Session()
        req = session.get(self.url, params=params, timeout=5, headers=self.HEADERS)
        s = json.loads(req.text)
        # print(s['msg'])
        # print(s['success'])
        if not s['success']:
            return
        self.isLogin = True
        self.HEADERS['token'] = s['token']
        # print(self.HEADERS)
        return session

    def GetHandle(self, params):
        req = self.session.get(self.url, params=params, timeout=5, headers=self.HEADERS)
        return req

    def getStudentIdInfo(self):
        params = {
            "method": "getStudentIdInfo",
            "xh": self.account
        }
        req = self.GetHandle(params)
        print(req.text)
        pass

    def getCurrentTime(self):
        params = {
            "method": "getCurrentTime",
            "currDate": datetime.datetime.now().strftime('%Y-%m-%d')
        }
        req = self.GetHandle(params)
        # print(req.text)
        return req.text

    def getKbcxAzc(self, zc=-1):
        s = json.loads(self.getCurrentTime())
        params = {
            "method": "getKbcxAzc",
            "xnxqid": s['xnxqh'],
            "zc": s['zc'] if zc == -1 else zc,
            "xh": self.account
        }
        req = self.GetHandle(params)
        pass

    def getKbcx(self, week=20):
        list_class = []
        s = json.loads(self.getCurrentTime())
        for i in range(1, week + 1):
            params = {
                "method": "getKbcxAzc",
                "xnxqid": s['xnxqh'],
                "zc": i,
                "xh": self.account
            }
            req = self.GetHandle(params)
            c = eval(req.text)
            for class_l in c:
                if class_l not in list_class:
                    print(class_l)
                    list_class.append(class_l)
        return list_class

    def getKxJscx(self, idleTime="0304"):
        params = {
            "method": "getKxJscx",
            "time": datetime.datetime.now().strftime('%Y-%m-%d'),
            "idleTime": "0304",
            "jxlid": 1
        }
        req = self.GetHandle(params)

    def getCjcx(self, sy=""):
        params = {
            "method": "getCjcx",
            "xh": self.account,
            "xnxqid": sy
        }
        req = self.GetHandle(params)

    def getKscx(self):
        params = {
            "method": "getKscx",
            "xh": self.account,
        }
        req = self.GetHandle(params)
