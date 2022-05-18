#!/usr/bin/python
# encoding:utf-8
import datetime
import time
from argparse import ArgumentParser

import requests
from logzero import logger
from requests import RequestException

from getId import getuser
from getImg import get_image,get_image_file,ocr_image
from threading import Thread
import socket
import socks


def bookseat(trys, buildingCode, kssj, jssj, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }

    logger.info("开始预约")
    book_url = 'http://freshmansno.wh.sdu.edu.cn:9007/common/submitApply'
    while trys:
        try:
            img_key,img_base64 = get_image(cookies)
            print(img_key)
            img_src = get_image_file(img_key,img_base64)
            print(img_src)
            value = ocr_image(img_src)
            print(value)
            data = {'key':img_key, 'value':value, 'buildingCode': buildingCode, 'kssj': kssj, 'jssj': jssj}
            res = requests.post(book_url, headers=headers, data=data, cookies=cookies)
            logger.info(res.status_code)
            if res.status_code == 200:
                if res.json()['code'] == 0:
                    logger.info("预约成功")
                    break
                else:
                    logger.info(res.json()['msg'])
                    logger.info("将再次请求该场馆")
                    trys = trys - 1
                    time.sleep(1)
            else:
                logger.info(res.status_code)
        except RequestException as e:
            logger.error({e})
            break
    logger.info("预约失败")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--userid', type=str, help='山东大学学号')
    parser.add_argument('--passwd', type=str, help='山东大学统一身份认证密码')
    parser.add_argument('--area', type=str, default='1001', help='区域编号')
    parser.add_argument('--retry', type=int, default=30, help='重试次数,默认为30次')
    parser.add_argument('--starttime', type=str, default='19:30', help='开始时间')
    parser.add_argument('--endtime', type=str, default='21:30', help='结束时间')
    paras = parser.parse_args()

    cookies = getuser(paras.userid, paras.passwd)

    thread1 = Thread(target=bookseat, args=(paras.retry,paras.area, paras.starttime, paras.endtime, cookies))

    thread1.start()
