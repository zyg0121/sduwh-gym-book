# encoding:utf-8
import execjs
import requests
from bs4 import BeautifulSoup
from requests.exceptions import *
from datetime import datetime as t
import time
from logzero import *

logfile('log/' + t.now().strftime('%Y-%m-%d') + '.txt', encoding='utf-8')

requests.adapters.DEFAULT_RETRIES = 3


def getuser(id, pwd):
    username = id  # input("请输入用户名:")
    password = pwd  # input("请输入密码:")
    retry = 15  # 重试次数

    # 获取登录信息
    loginurl = "https://pass.sdu.edu.cn/cas/login?service=http%3A%2F%2Ffreshmansno.wh.sdu.edu.cn%3A9007%2Fapply.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }

    session = requests.session()
    session.keep_alive = False
    session.headers.update(headers)
    loginpageHtml = session.get(loginurl, headers=headers)

    page = BeautifulSoup(loginpageHtml.text, "html.parser")  # bs4进行解析,
    ul = len(username)
    pl = len(password)
    lt = page.select_one("#lt").get("value")
    execution = page.select_one("[name=execution]").get("value")
    _eventId = page.select_one("[name=_eventId]").get("value")

    with open("des.js", 'r') as file:  # 打开js文件
        desJsCode = file.read()
    js = execjs.compile(desJsCode)
    rsa = js.call("strEnc", username + password + lt, "1", "2", "3")  # 调用js函数,获取加密后的字符串

    data = {
        "rsa": rsa,
        "ul": ul,
        "pl": pl,
        "lt": lt,
        "execution": execution,
        "_eventId": _eventId
    }

    for i in range(retry):
        logger.info("尝试第" + str(i + 1) + "次获取登录信息")
        try:
            login_info = session.post(loginurl, headers=headers, data=data)  # 报错
            if (login_info.status_code == 200):
                logger.info("获取登录信息成功")
                break
        except RequestException as e:
            logger.error({e})
        time.sleep(5)

    # logger.info(session.cookies)
    cookies = {
        "JSESSIONID": session.cookies.get("JSESSIONID", domain="freshmansno.wh.sdu.edu.cn"),
    }

    return cookies
