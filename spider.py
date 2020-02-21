import requests
import re
import os
from lxml import etree
from bs4 import BeautifulSoup

def get_cookie():
    host = 'http://jwxt.ahut.edu.cn/'
    session = requests.session()
    session.get(host, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.130 Safari/537.36 '
    })
    return session


class Student:

    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.session = get_cookie()
        self.encoded = self.get_code(self.session)

    def get_code(self, session):
        str_url = 'http://jwxt.ahut.edu.cn/Logon.do?method=logon&flag=sess'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'jwxt.ahut.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36 '
        }
        r = session.get(str_url, headers=headers)
        dataStr = r.text
        scode = dataStr.split("#")[0]
        sxh = dataStr.split("#")[1]
        code = self.username + "%%%" + self.password
        encode = ""
        i = 0
        while i < len(code):
            if i < 20:
                encode += code[i:i + 1] + scode[0:int(sxh[i:i + 1])]
                scode = scode[int(sxh[i:i + 1]):len(scode)]
            else:
                encode += code[i:len(code)]
                i = len(code)
            i += 1
        return encode

    def login(self):
        login_url = 'http://jwxt.ahut.edu.cn/Logon.do?method=logon'
        data = {
            'userAccount': self.username,
            'userPassword': '',
            'encode': self.encoded,
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '79',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jwxt.ahut.edu.cn',
            'Origin': 'http://jwxt.ahut.edu.cn',
            'Referer': 'http://jwxt.ahut.edu.cn/jsxsd',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36'}
        r = self.session.post(login_url, headers=headers, data=data)
        try:
            html = etree.HTML(r.text)
            error = html.xpath('//font[@color="red"]/text()')[0]
            print(error)
        except:
            print(r.text)

    def getClassJson(self):
        url = 'http://jwxt.ahut.edu.cn/jsxsd/xskb/xskb_list.do'
        Header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'jwxt.ahut.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36 ',
            'Referer': 'http://jwxt.ahut.edu.cn/jsxsd/framework/xsMain.jsp'
        }
        '''数据项需要改'''
        date = {
            'xnxq01id': '2019-2020-2',
            'zc': '(全部)',
            'sjms': '默认节次模式',

        }
        list_class = self.session.get(url, headers=Header, params=date)
        print(list_class)


if __name__ == '__main__':
    student = Student('id', 'password')
    # 这里实例化一个学生类，可以有登陆方法
    student.login()
    student.getClassJson()
