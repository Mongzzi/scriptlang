#!/usr/bin/python
# coding=utf-8

import sys
import telepot
from pprint import pprint # 데이터를 읽기 쉽게 출력
from urllib.request import urlopen
import traceback
from xml.etree import ElementTree
from xml.dom.minidom import parseString

import common_functions


#-------------------------------------------------------------------------------------------------
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta  # 현재 날짜 외의 날짜 구하기 위한 모듈
import requests # HTTP 요청을 보내는 모듈
import json
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
key = 'nROKr9gqJ/zCVFiZhf/2PKCFTXCSUm3R4tzU4lLbQg9ehw7c1UnINQL413EYxPvHfVUaPVAkTMaSWabh11bt8Q=='

#-------------------------------------------------------------------------------------------------

TOKEN = '5518030601:AAGxOIZJyz8Vc2hDBoSYPzrUSgoWOueBdMY'
MAX_MSG_LENGTH = 300

#-------------------------------------------------------------------------------------------------


bot = telepot.Bot(TOKEN)
base_date = ""
base_time = ""

#-------------------------------------------------------------------------------------------------

def getData(nx, ny):
    
    base_date,base_time = common_functions.Set_Time()
    params ={'serviceKey' : key,  'numOfRows' : '1000','pageNo' : '1', 'dataType' : 'JSON', 'base_date' : base_date, 'base_time' : base_time, 'nx' : nx, 'ny' : ny }
    response = requests.get(url, params=params)
    items = response.json().get('response').get('body').get('items')
    
    weather_list = [[],[],[],[],[]]

    for item in items['item']:
        if item['category'] =='PTY':    #강수확률- 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
            cnt=0
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='RN1':    #1시간 강수량
            cnt=1
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='T1H':    #온도
            cnt=2
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='REH':    #습도
            cnt=3
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='SKY':    #하늘상태- 맑음(1), 구름많음(3), 흐림(4)
            cnt=4
            weather_list[cnt].append(item['fcstValue'])
            
    return weather_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        # 예외 정보와 스택 트레이스 항목을 인쇄.
        traceback.print_exception(*sys.exc_info(), file=sys.stdout)