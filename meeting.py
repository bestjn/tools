#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import datetime

url = 'https://ecm.inspur.com/inspur_esg/meeting/booking'
body1 = {"topic": "jcjc", "alert": 0, "notice": "", "from": 1523665800000, "to": 1523698200000, "organizer": "22418", "room": {
    "id": "60", "name": "S06栋南(6层) 软件集团通信602 会议室"}, "participant": {"user": ["22418"], "channel": []}, "attendant": ""}
body2 = {"topic": "jcjc", "alert": 0, "notice": "", "from": 1523665800000, "to": 1523698200000, "organizer": "22418", "room": {
    "id": "61", "name": "S06栋南(6层) 软件集团通信603 会议室"}, "participant": {"user": ["22418"], "channel": []}, "attendant": ""}
headers = {'Cookie': "connect.sid=s%3AV5PmJdJ4Nu1rZeG1Fd76bAFHcX5VpYog.toPc0qYH%2BbD%2FGeZwDmLgMomsgoVYC3kYPUGcrx8R3%2Fs",
           'User-Agent': 'Android/6.0.1(Lenovo Lenovo-P2) CloudPlus_Phone/1.6.0',
           'X-Device-ID': 'ffffffff-aac8-806b-ffff-ffff9db95b36',
           'Accept': 'application/json',
           'Authorization': 'Bearer AT-3-24307963-TgmAscdrICByvkgWgIgKHqnNOgPxOROARqg',
           'X-ECC-Current-Enterprise': '10000',
           'Accept-Language': 'zh-Hans',
           'Content-Type': 'application/json;charset=UTF-8',
           'Host': 'ecm.inspur.com',
           'Connection': 'Keep-Alive'}

while (True):
    t = time.time()
    sec = int(t)

    xz = "2018-04-12 23:59:50"
    timeArray = time.strptime(xz, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))

    stop_time = "2018-04-13 00:01:59"
    timeArray2 = time.strptime(stop_time, "%Y-%m-%d %H:%M:%S")
    timeStamp2 = int(time.mktime(timeArray2))

    if sec < timeStamp:
        print('time has not arrived yet')
        time.sleep(5)
        continue

    if sec > timeStamp2:
        print('game over')
        break

    # print type(body)
    # print type(json.dumps(body))
    # 这里有个细节，如果body需要json形式的话，需要做处理
    # 可以是data = json.dumps(body)
    response = requests.post(url, data=json.dumps(body2), headers=headers)
    # 也可以直接将data字段换成json字段，2.4.3版本之后支持
    # response  = requests.post(url, json = body, headers = headers)

    # 返回信息
    print(response.text)

    time.sleep(0.5)
    # 返回响应头
    # print response.status_code
'''
    response = requests.post(url, data=json.dumps(body2), headers=headers)

    # 返回信息
    print(response.text)
    # 返回响应头
    #print response.status_code
    time.sleep(0.5)'''
