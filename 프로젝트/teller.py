#!/usr/bin/python
# coding=utf-8

import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
import re
from datetime import date, datetime

import noti

# 기존 앱 코드에서 함수만 가져와본다.
import common_functions

# 튜플을 받음. 순서대로 nx, ny, latitude, longitude
def replyAptData( num, user ):
    global return_lsit

    adr_tuple = return_lsit[int(num) - 1]
    name, (nx, ny, latitude, longitude) = adr_tuple
    print(adr_tuple)

    weather_list = noti.getData( nx, ny )
    print(weather_list)

    base_date, base_time = common_functions.Set_Time()

    noti.sendMessage( user, common_functions.make_data(name, base_date, base_time, weather_list))

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS \
        users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )

def handle(msg):
    global return_lsit
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    text = msg['text']
    args = text.split(' ')
    if text.startswith('날씨') and len(args)>1:
        print('try to 날씨', args[1])
        if return_lsit == None:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
        num_of_data = len(return_lsit)
        if num_of_data:
            if args[1] == '전부':
                for i in range(num_of_data):
                    replyAptData(i+1, chat_id)
            elif num_of_data >= int(args[1]) > 0:
                replyAptData(str(int(args[1])), chat_id)
            else:
                noti.sendMessage( chat_id, '검색된 지역의 수 보다 높은 번호를 불렀습니다.' )
                noti.sendMessage( chat_id, '현재 검색된 지역의 수는 '+str(num_of_data)+'개 입니다' )
        else:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
    elif text.startswith('날씨전부'):
        print('try to 날씨전부')
        if return_lsit == None:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
        num_of_data = len(return_lsit)
        if num_of_data:
            for i in range(num_of_data):
                replyAptData(i, chat_id)
        else:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
    elif text.startswith('저장') and len(args)>1:
        print('try to 저장', args[1])
        save( chat_id, args[1] )
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    elif text.startswith('검색') and len(args)>1:
        print('try to 검색', args[1])
        if args[1] == '확인':
                text = ''
                count = 1
                for i, data in enumerate(return_lsit):   # 포멧을 사용해보자.
                    name, val = data
                    text += '['+str(i+1 )+']'
                    text += str(name)
                    text += '\n'
                noti.sendMessage( chat_id, text )
                return
        return_lsit = common_functions.Get_Name_Val_From_Dict(args[1], adress_dict)
        if return_lsit == None:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
        num_of_data = len(return_lsit)
        if num_of_data:
            noti.sendMessage( chat_id, str(num_of_data)+'개 지역 검색' )
            noti.sendMessage( chat_id, '검색 결과를 확인하려면 "검색확인" 을 입력해주세요' )
            noti.sendMessage( chat_id, '날씨를 확인하려면 "날씨"와 "검색된 결과의 순서"or "전부"를 입력해주세요\n예) "날씨 '+str(num_of_data//2)+'", "날씨 전부"')
        else:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
    elif text.startswith('검색확인'):
        print('try to 검색확인')
        if return_lsit == None:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.\n다른 값을 검색해 보세요' )
        num_of_data = len(return_lsit)
        if num_of_data:
            text = ''
            count = 1
            for i, data in enumerate(return_lsit):   # 포멧을 사용해보자.
                name, val = data
                text += '['+str(i+1 )+']'
                text += str(name)
                text += '\n'
            noti.sendMessage( chat_id, text )
        else:
            noti.sendMessage( chat_id, '검색된 지역이 없습니다.' )
    elif text.startswith('?'):
        print('try to ?')
        noti.sendMessage(chat_id,
'''명령어 모음입니다.
날씨 [검색된 지역의 수 이하의 숫자 or 전부]
 - 해당하는 지역의 날씨를 출력합니다
 - 전부 를 입력하면 전부 다 나옵니다.
 예) 날씨 4, 날씨전부, 날씨 전부

저장 [저장할 단어]
 - 입력 단어를 저장합니다

확인
 - 저장 단어를 전부 다 불러옵니다

검색 [검색할 지역에 포함된 단어]
 - 입력한 단어가 포함된 지역을 전부 검색합니다
예) 검색 광, 검색 4, 검색 서, 검색 ,

검색확인 or 검색 확인
 - 검색한 지역들을 출력합니다.


중 하나의 명령을 입력하세요.]
''')
    else:
        noti.sendMessage(chat_id,
'''모르는 명령어 이거나 잘못된 입력입니다.
명령어들의 사용법이 궁금하시면 ? 를 입력해 주세요
''')

return_lsit = None  #검색한 단어가 들어간 지역들의 리스트

adress_dict = common_functions.Read_Adress_From_File()

today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

from noti import bot
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')
while 1:
    time.sleep(10)