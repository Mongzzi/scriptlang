from asyncio.windows_events import NULL
from re import L
from tkinter import *
import tkinter
import pickle
from tkinter import font
# 초기화를 해주지 않아도 되는 dict
from collections import defaultdict
from numpy import true_divide


root = Tk()
root.geometry("600x700+600+100")
root.title('Sun')



#----------------------------파싱----------------------------------

import requests # HTTP 요청을 보내는 모듈
import json
#import datetime


nx = "62"               # 위도 변수
ny = "125"              # 경도 변수

base_date = "20220530"  # 날짜 변수
base_time = "0600"      # 시각 변수

                        # 서버 url 변수
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
                        # 서버 인증키 변수(디코딩)
serviceKey = 'nROKr9gqJ/zCVFiZhf/2PKCFTXCSUm3R4tzU4lLbQg9ehw7c1UnINQL413EYxPvHfVUaPVAkTMaSWabh11bt8Q=='
                        # 위도, 경도, 날짜 , 저장
params ={'serviceKey' : serviceKey, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : base_date, 'base_time' : base_time, 'nx' : nx, 'ny' : ny }
                        # 정보 받아오는 부분
response = requests.get(url, params=params)
                        # JSON 파일 파싱 
items = response.json().get('response').get('body').get('items')


# 카테고리 코드값 
# POP(강수확률) PTY(강수형태) REH(습도) SKY(하늘상태)
# TMX(일 최고기온) TMN(일 최저기온) T1H(기온) TMP(1시간 기온) 
#
#
               
for item in items['item']:
    if item['category'] =='PTY':
        print(item['obsrValue'])
    if item['category'] =='T1H':
        Max_temp= item['obsrValue']


#----------------------------etc-----------------------------------

f = open('adress', 'rb') #pickle 사용을 위해 바이너리 읽기 파일 오픈
adress_dict = pickle.load(f) #파일에서 리스트 load

cities = ["서울","부산","경기","인천"]
mail_img= PhotoImage(file=r"scriptlang\프로젝트\mail_640_416.png")
weather_top_img=PhotoImage(file=r"scriptlang\프로젝트\weather_top.PNG")
weather_bottom_img=PhotoImage(file=r"scriptlang\프로젝트\weather_bottom.PNG")

#------------------------검색 함수----------------------------------

def Search_city():
    global cities
    global Search_Entry
    global adress_dict
    global nx, ny
    global items, Max_temp
    for_search = Search_Entry.get()

    val = NULL
    name = NULL
    flag = False

    import pprint
    
    for adress in adress_dict['level_3']:
        if flag: break
        if adress != None and for_search in adress:
            name = adress
            val = adress_dict['level_3'][adress]
            flag = TRUE
    
    for adress in adress_dict['level_2']:
        if flag: break
        if adress != None and for_search in adress:
            name = adress
            val = adress_dict['level_2'][adress]
            flag = TRUE

    for adress in adress_dict['level_1']:
        if flag: break
        if adress != None and for_search in adress:
            name = adress
            val = adress_dict['level_1'][adress]
            print(val)
            flag = TRUE
                    # val 가 튜플임. 순서대로 X, Y, 위도, 경도
                    # 사용 예시         nx, ny, latitude, longitude = val
                    # name 는 그 지역의 이름.

    if not flag:
        print(for_search)
        print("찾지 못 함")
                            # 1. 찾지 못 했을 경우 다른 값을 반환하고, 만약 이 값이 반환되면 찾지 못했다고 판단해야함. 
                            # 2. 혹은 그냥 입력 받을때 기본값을 NULL로 해놓고 NULL이면 찾지 못했다고 코딩하면 될듯.
    else:
        print(name)
        print(val)


def View_Detail():
    pass


#--------------------------<폰트>-------------------------------------


fontTitle = font.Font(root, size=18, weight='bold', family = '양재벨라체M')
fontNormal=font.Font(root,size=15,weight='bold',family='양재벨라체M')


#-----------------------<프레임 부분>--------------------------------

    # 타이틀창
Frame_title = Frame(root,pady=10,bg='#FFFF99')
Frame_title.pack(side='top',fill="both")

    # 검색창, 검색버튼, 갱신버튼
Frame_search = Frame(root,padx=10, pady=10, bg='#CCFF99')
Frame_search.pack(side='top',fill="x")

    #최고기온, 최저기온, 상세보기 버튼
Frame_etc =Frame(root,pady=10, bg='#99FFFF')
Frame_etc.pack(side="top",fill="x")

    #각종 그래프 및 정보 1
Frame_graph=Frame(root,padx=10, pady=10, bg='#CCFFFF')
Frame_graph.pack(side="top",fill="both",expand=True)

Frame_graph_top=Frame(Frame_graph,padx=10, pady=10, bg='#CCCCFF')
Frame_graph_top.pack(side="top",fill="both",expand=True)

Frame_graph_bottom=Frame(Frame_graph,padx=10, pady=10, bg='#FFFFFF')
Frame_graph_bottom.pack(side="top",fill="both",expand=True)

#------------------------<위젯 부분>--------------------------------

    # 제목 레이블
Title_Lable= Label(Frame_title,font=fontTitle,text="★오늘의 날씨는 푸르당★",bg='#FFFF99')
Title_Lable.pack(anchor="center",fill="both")
    
    # 검색 엔트리 , 검색 버튼, 새로고침 버튼 
Search_Entry= Entry(Frame_search,font=fontNormal,width=30,borderwidth=10,relief='ridge')
Search_Entry.pack(side="left",padx=10)

Search_Button=Button(Frame_search,width=5,font=fontNormal,text="검색",command=Search_city)
Search_Button.pack(side="left",padx=10)

Renewal_Button=Button(Frame_search,width=10,font=fontNormal,text="새로고침",command=Search_city)
Renewal_Button.pack(side="left",padx=10)

    # 최고 최저 기온 레이블 , 상세보기 버튼, 이메일 버튼    
High_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="최고 기온 {0}".format(Max_temp +"도"),bg='#FFFF99')
High_Temp_Lable.pack(side="left",padx=10,fill="both")

Low_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="최저 기온 {0}".format("xx도"),bg='#FFFF99')
Low_Temp_Lable.pack(side="left",padx=10,fill="both")

View_Detail_Button= Button(Frame_etc,width=13,font=fontNormal,text="상세보기 버튼",command=View_Detail)
View_Detail_Button.pack(side="left",padx=10,fill="both")

Send_Email_Button = Button(Frame_etc,font=fontNormal,image=mail_img)
Send_Email_Button.pack(side="left",padx=10,fill="both")

    # 날씨 정보 그래프 레이블
    
Weather_Top_Lable=Label(Frame_graph_top,image=weather_top_img)
Weather_Top_Lable.pack(fill="both")

Weather_Bottom_Lable=Label(Frame_graph_bottom,image=weather_bottom_img)
Weather_Bottom_Lable.pack(fill="both")






root.mainloop()

