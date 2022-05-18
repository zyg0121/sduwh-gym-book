#!/usr/bin/python
# encoding:utf-8
import datetime
import time
from argparse import ArgumentParser
from numpy import empty

import requests
from logzero import logger
from requests import RequestException

from getId import getuser
from threading import Thread
import socket
import socks
from PIL import Image
import os
import base64
import re
import ddddocr

def get_image(cookies):
    logger.info("获取图片信息")
    trys = 5  # 尝试获取5次

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    get_imgs_url = 'http://freshmansno.wh.sdu.edu.cn:9007/common/code'

    get_img_key = ""
    get_img_base64 = ""

    while trys:
        try:
            res = requests.post(get_imgs_url, headers=headers, cookies=cookies)
            logger.info(res.status_code)
            if res.status_code == 200:
                if res.json()['code'] == 0:
                    logger.info("获取图片成功")
                    get_img_key = res.json()['data']['key']
                    get_img_base64 = res.json()['data']['base64']
                    return get_img_key,get_img_base64
                else:
                    logger.info(res.json()['msg'])
                    logger.info("将再次请求图片")
                    trys = trys - 1
                    time.sleep(1)
            else:
                logger.info(res.status_code)
        except RequestException as e:
            logger.error({e})
            break
    return None


def get_image_file(img_key, img_base64):
    # 1、信息提取
    result = re.search(
        "data:image/(?P<ext>.*?);base64,(?P<data>.*)", img_base64, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")

    else:
        raise Exception("Do not parse!")

    # 2、base64解码
    img = base64.urlsafe_b64decode(data)

    # 3、二进制文件保存
    filename = "img/{}.gif".format(img_key)
    with open(filename, "wb") as f:
        f.write(img)

    # 4、提取gif
    gif = Image.open(filename)
    try:
        gif.save(f"img/{img_key}-{gif.tell()}.png")
        while True:
            gif.seek(gif.tell() + 1)
            gif.save(f'img/{img_key}-{gif.tell()}.png')
    except Exception as e:
        print("处理结束")

    return f"img/{img_key}"

def ocr_image(src):
    ocr = ddddocr.DdddOcr()

    with open(src+"-0.png", 'rb') as f:
        image1 = f.read()
    res0 = ocr.classification(image1)

    with open(src+"-1.png", 'rb') as f:
        image2 = f.read()
    res1 = ocr.classification(image2)
    with open(src+"-2.png", 'rb') as f:
        image1 = f.read()
    res2 = ocr.classification(image1)

    with open(src+"-3.png", 'rb') as f:
        image2 = f.read()
    res3 = ocr.classification(image2)
    with open(src+"-4.png", 'rb') as f:
        image1 = f.read()
    res4 = ocr.classification(image1)

    # res = (res4[0] + res3[1] + res2[2] + res1[3] + res0[3]).lower()
    res = ""
    try:
        res = (res4[0] + res3[1] + res2[2] + res1[3] + res0[3]).lower()
    except Exception as e:
        print("识别验证码信息异常")

    return res
