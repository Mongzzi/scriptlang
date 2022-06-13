import pickle

import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta  # 현재 날짜 외의 날짜 구하기 위한 모듈


def Read_Adress_From_File():
    f = open('adress', 'rb') #pickle 사용을 위해 바이너리 읽기 파일 오픈
    return pickle.load(f) #파일에서 리스트 load

def Get_Name_Val_From_Dict(for_search, adress_dict):
    flag = False
    
    return_lsit = []

    for adress in adress_dict['level_3']:
        if flag: break
        if adress != None and for_search in adress:
            return_lsit.append((adress, adress_dict['level_3'][adress]))
            # flag = TRUE
    
    for adress in adress_dict['level_2']:
        if flag: break
        if adress != None and for_search in adress:
            return_lsit.append((adress, adress_dict['level_2'][adress]))
            # flag = TRUE

    for adress in adress_dict['level_1']:
        if flag: break
        if adress != None and for_search in adress:
            return_lsit.append((adress, adress_dict['level_1'][adress]))
            # flag = TRUE

    return return_lsit


def make_data(name, base_date, base_time, weather_list):
    return '오늘의 날자 ' + base_date + '\n'\
    + str(int(base_time)//100) + '시' + str(int(base_time)%100) + '분의 '\
    + name +'의 날씨입니다.\n'\
    + '강수확률 = ' + str(rain_condition(weather_list[0][0])\
    + '\n강수량 = '+ weather_list[1][0] \
    + '\n현재온도 = ' + weather_list[2][0]+'도'\
    + '\n현재습도 = '+weather_list[3][0]+'%'\
    + '\n현재 하늘상태 = '+str(sky_condition(weather_list[4][0])))\


def rain_condition(n):
    data = ''
    if n == '0':
        data = '비가 오지 않습니다.'
    elif n == '1':
        data= '비가 옵니다.'
    elif n== '2':
        data= '비/눈이 옵니다.'
    elif n== '3':
        data= '눈이 옵니다.'           
    elif n== '5':
        data= '빗방울이 떨어집니다.'
    elif n== '6':
        data= '빗방울눈날림이 있습니다.'
    elif n== '7':
        data= '눈날림이 있습니다.'
    return data                                

def sky_condition(n):
    data = ''
    if n == '1':
        data = '맑습니다.'
    elif n == '3':
        data= '구름이 꼈습니다.'
    elif n== '4':
        data= '흐립니다.'
    return data 

def Set_Time():
    if datetime.now().minute <45:
        if datetime.now().hour==0:
            base_date= (date.today() - timedelta(days=1)).strftime("%Y%m%d")
            base_time = "2330"
        else:
            pre_hour=datetime.now().hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
            base_date= datetime.today().strftime("%Y%m%d")

    else:
        if datetime.now().hour < 10:
            base_time = "0" + str(datetime.now().hour) + "30"
        else:
            base_time = str(datetime.now().hour) + "30"
        base_date = datetime.today().strftime("%Y%m%d")
    return base_date, base_time