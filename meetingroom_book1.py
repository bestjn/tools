#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-30 15:05:46
# @Author  : luzhuang

import requests
import json
import time
import datetime
from loguru import logger

AFTER_DAYS = 2
START_TIME = 9  # 预订开始时间
END_TIME = 20  # 预订结束时间
TITLE = '电子台账' # 会议主题
ROOM_BOOK = ['603'] #要预定的会议室列表
LOGIN_INFO = 'client_id=51c6a0a8-7a40-47e8-b8bd-cc305ece9c52' \
                '&client_secret=a4738cc3-f929-46d2-b4e5-277b6cac8e01' \
                '&grant_type=password' \
                '&password=' \
                '&scope=' \
                '&username=luzhuang@inspur.com' # 验证信息
RELOGIN_INTERVAL = 10 # 获取access_token失败时重新获取间隔时长(s)
ROOM_LIST = {
'602':{
    'id': '60',
    'building': 'S06栋南(6层)',
    'displayName': '软件集团通信602会议室'
},
'603':{
    'id': '61',
    'building': 'S06栋南(6层)',
    'displayName': '软件集团通信603会议室'
},
'501':{
    'id': '56',
    'building': 'S06栋南(5层)',
    'displayName': '软件集团通信501会议室'
}}

# BOOK_TIME_H = 14 #预订的时间点小时
# BOOK_TIME_M = 13 #预订的时间点分钟

def cloudplus_login():
    url = 'https://id.inspuronline.com/oauth2.0/token'
    headers = {
        'Host': 'id.inspuronline.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'imp cloud/3.1.0 (iPhone; iOS 12.3; Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1, en-US;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate'
    }
    data = LOGIN_INFO
    while True:
        try:
            response = requests.post(url, data=data, headers=headers)
            records = json.loads(response.text)
            access_token = records['access_token']
            logger.info('获取access_token成功：' + access_token)
            return access_token
        except Exception as e:
            logger.info('获取access_token失败，等待' + str(RELOGIN_INTERVAL) + 's重新获取...')
            time.sleep(RELOGIN_INTERVAL)


def is_room_busy():
    # TODO
    pass

def meeting_cancel():
    # TODO
    pass

def meetingroom_book(access_token, book_info):
    url = 'https://ecm.inspuronline.com/inspur_esg/schedule-ext/api/schedule/v6.0/meeting/add'
    headers = {
        'Host': 'ecm.inspuronline.com',
        'Cookie': 'X-ECC-Current-Enterprise=10000; x-ecp-token=bearer%20' + access_token,
        'X-Device-ID': '64d72692c8a8f7b3643ef84fe1680ddf706df2e2',
        'X-ECC-Current-Enterprise': '10000',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'iOS/12.3(Apple iPhone10,2) CloudPlus_Phone/3.1.0',
        'Accept-Language': 'zh-Hans-CN',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer ' + access_token
    }
    form_data = book_info
    while True:
        try:
            response = requests.post(url, json=form_data, headers=headers)
            # logger.info(response.text)
            if len(response.text) is 34:
                logger.info('预定成功！' + '地点：' + book_info['room']['name'] + '\n')
                break
            else:
                try:
                    records = json.loads(response.text)
                    logger.info('预定失败！' + 'msg：' + records['msg'] + '\n')
                    break
                except Exception as e:
                    logger.info('预定失败！\n')
                    break
        except:
            logger.info('请求失败！重新发起请求\n')
            continue


def get_room_info(access_token):
    url = 'https://ecm.inspuronline.com/inspur_esg/meeting/room/?isIdle=false'
    headers = {
        'Host': 'ecm.inspuronline.com',
        'Cookie': 'X-ECC-Current-Enterprise=10000; x-ecp-token=bearer%20' + access_token,
        'X-Device-ID': '64d72692c8a8f7b3643ef84fe1680ddf706df2e2',
        'X-ECC-Current-Enterprise': '10000',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'iOS/12.3(Apple iPhone10,2) CloudPlus_Phone/3.1.0',
        'Accept-Language': 'zh-Hans-CN',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)
    records = json.loads(response.text)
    print(records)


def get_room_schedule(access_token):
    url = 'https://ecm.inspuronline.com/inspur_esg/schedule-ext/api/schedule/v6.0/meeting/GetRoomUse?endTime=1560096000000&roomId=56&startTime=1559232000000'
    headers = {
        'Host': 'ecm.inspuronline.com',
        'Cookie': 'X-ECC-Current-Enterprise=10000; x-ecp-token=bearer%20' + access_token,
        'X-Device-ID': '64d72692c8a8f7b3643ef84fe1680ddf706df2e2',
        'X-ECC-Current-Enterprise': '10000',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'User-Agent': 'iOS/12.3(Apple iPhone10,2) CloudPlus_Phone/3.1.0',
        'Accept-Language': 'zh-Hans-CN',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)
    records = json.loads(response.text)
    print(records)


def get_start_end_timestamp(start_time, end_time):
    now = datetime.datetime.now()
    today_0 = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
    start_datetime = today_0 + datetime.timedelta(days=AFTER_DAYS, hours=start_time)
    end_datetime = today_0 + datetime.timedelta(days=AFTER_DAYS, hours=end_time)
    logger.info('会议开始时间：' + str(start_datetime) + ' 结束时间：' + str(end_datetime))
    s = time.mktime(start_datetime.timetuple())
    e = time.mktime(end_datetime.timetuple())
    return int(s), int(e)

def timestamp2str(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def str2timestamp(timestr):
    return int(time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S")))

def get_book_info(start_time, end_time, title, room_id, building, displayName):
    book_info = {
                "title": title,
                "startTime": start_time,
                "endTime": end_time,
                "remindEvent": {
                    "advanceTimeSpan": 600,
                    "remindType": "in_app"
                },
                "isCommunity": False,
                "lastTime": 0,
                "owner": "288135",
                "note": "",
                "type": "meeting",
                "room": {
                    "id": room_id,
                    "name": building + ' ' + displayName
                },
                "creationTime": 0,
                "syncToLocal": True,
                "location": {
                    "id": room_id,
                    "building": building,
                    "displayName": displayName
                },
                "isAllDay": False,
                "participants": [{
                    "id": "288135",
                    "name": "陆壮",
                    "role": "common"
                }]
            }
    return book_info

if __name__ == '__main__':
    # logger.add("D:/meeting/log/file_{time}.log")
    # book_info_list = []
    # start_timestamp, end_timestamp = get_start_end_timestamp(START_TIME, END_TIME)
    # logger.info('会议主题：' + TITLE)
    # logger.info('将要预定的会议室：' + str(ROOM_BOOK))
    # for room in ROOM_BOOK:
    #     if ROOM_LIST[room] is not None:
    #         book_info_list.append(get_book_info(str(start_timestamp)+'000', str(end_timestamp)+'000', TITLE, ROOM_LIST[room]['id'], ROOM_LIST[room]['building'], ROOM_LIST[room]['displayName']))
    
    # access_token = cloudplus_login()

    # i = 0
    # for book_info in book_info_list:
    #     logger.info('开始预订' + ROOM_BOOK[i])
    #     i +=1
    #     meetingroom_book(access_token, book_info)

    # access_token = cloudplus_login()
    # get_room_info(access_token)
    # access_token = cloudplus_login()
    # get_room_schedule(access_token)
    print(timestamp2str(1559527259))
    # print(str2timestamp('2019-06-01 09:00:00'))
    # print(len("a16f03ccfb92426584769c692e9ae441"))