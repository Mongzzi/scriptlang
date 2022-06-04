from asyncio.windows_events import NULL
from re import L
from tkinter import *
import tkinter
import pickle
from tkinter import font
# 초기화를 해주지 않아도 되는 dict
from collections import defaultdict
from numpy import true_divide
import tkintermapview   # 지도를 위한 참조
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta  # 현재 날짜 외의 날짜 구하기 위한 모듈

root = Tk()
root.geometry("600x700+600+100")
root.title('Sun')

#------------------------global 변수------------------------------

nx = "62"               # 위도 변수
ny = "125"              # 경도 변수

latitude = NULL         # 지도용 위도 경도
longitude = NULL

base_date = ""
base_time = ""

weather_list = []


Cur_temp = "0"          # 현재 온도    
items= NULL

default_status = "기본보기"
opposite_status = "그래프보기"

# 지도 관련 변수
number_of_marker = 0
markerlist = []


corrent_canvas_status = default_status  # "기본" = 기본, "상세보기" = 상세보기
next_canvas_status = opposite_status  # 이 둘은 서로 바뀌어야한다.

# 그래프 관련 변수
canvas = NULL

#----------------------------시간 재정의 함수----------------------

def Set_Time():
    global base_date,base_time
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

#----------------------------파싱----------------------------------

import requests # HTTP 요청을 보내는 모듈
import json
#import datetime
                        # 서버 url 변수
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
                        # 서버 인증키 변수(디코딩)
serviceKey = 'nROKr9gqJ/zCVFiZhf/2PKCFTXCSUm3R4tzU4lLbQg9ehw7c1UnINQL413EYxPvHfVUaPVAkTMaSWabh11bt8Q=='

#----------------------------Update------------------------------------

# 카테고리 코드값 
# POP(강수확률) PTY(강수형태) REH(습도) SKY(하늘상태)
# TMX(일 최고기온) TMN(일 최저기온) T1H(기온) TMP(1시간 기온) 

def Update_map():
    global map_widget
    global City_Name_Lable
    global nx, ny
    global number_of_marker, markerlist
    
    if latitude and longitude:
        marker_1 = map_widget.set_position(float(latitude), float(longitude), marker=True)
        # print(marker_1.position, marker_1.text) # 확인용 출력
        marker_1.set_text(City_Name_Lable["text"]) # set new text
        map_widget.set_zoom(15) # 0~19 (19 is the highest zoom level)
        markerlist.append(marker_1)

def Update():
    global serviceKey,url
    global nx,ny
    global base_date, base_time
    global items,Cur_temp
    global base_date,base_time
    Set_Time()
    
    params ={'serviceKey' : serviceKey,  'numOfRows' : '1000','pageNo' : '1', 'dataType' : 'JSON', 'base_date' : base_date, 'base_time' : base_time, 'nx' : nx, 'ny' : ny }
    response = requests.get(url, params=params)
    print(response.content)
    items = response.json().get('response').get('body').get('items')
    
    for item in items['item']:
        if item['category'] =='PTY':    #강수확률- 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
            print(item['fcstValue'])
            
        if item['category'] =='RN1':    #1시간 강수량
            print(item['fcstValue'])
            
        if item['category'] =='T1H':    #온도
            Cur_temp= str(item['fcstValue'])
            
        if item['category'] =='REH':    #습도
            print(item['fcstValue'])        
            
        if item['category'] =='SKY':    #하늘상태- 맑음(1), 구름많음(3), 흐림(4)
            print(item['fcstValue'])              
            
            
            
    Change_Label_Temp()
    Update_map()

#----------------------------etc-----------------------------------

f = open('adress', 'rb') #pickle 사용을 위해 바이너리 읽기 파일 오픈
adress_dict = pickle.load(f) #파일에서 리스트 load

cities = ["서울","부산","경기","인천"]
mail_img= PhotoImage(file=r"scriptlang\프로젝트\mail_640_416.png")
weather_top_img=PhotoImage(file=r"scriptlang\프로젝트\weather_top.PNG")
weather_bottom_img=PhotoImage(file=r"scriptlang\프로젝트\weather_bottom.PNG")

def Change_Label_Temp():
    global Cur_Temp_Lable
    global Cur_temp
    
    Cur_Temp_Lable.config(text="현재 기온{0}".format(Cur_temp +"도"),bg='#FFFF99')

#------------------------검색 함수----------------------------------

def Search_city():
    global cities
    global Search_Entry
    global City_Name_Lable
    global adress_dict
    global nx, ny
    global items, Max_temp
    global latitude, longitude
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
        City_Name_Lable.config(text=str(for_search)+" 찾지 못함")
        print(for_search)
        print("찾지 못 함")
                            # 1. 찾지 못 했을 경우 다른 값을 반환하고, 만약 이 값이 반환되면 찾지 못했다고 판단해야함. 
                            # 2. 혹은 그냥 입력 받을때 기본값을 NULL로 해놓고 NULL이면 찾지 못했다고 코딩하면 될듯.
    else:
        print(name)
        print(val)
        nx, ny, latitude, longitude = val
        nx = str(nx)
        ny = str(ny)
        
        City_Name_Lable.config(text=str(name))
        Update()

def draw_graph(data, canvasWidth, canvasHeight):
    global canvas
    canvas.delete(corrent_canvas_status) # 기존 그림 지우기

    if not len(data): # 데이터 없으면 return
        canvas.create_text(canvasWidth/2,(canvasHeight/2), text="No Data", tags=corrent_canvas_status)
        return
    nData = len(data) # 데이터 개수, 최대값, 최소값 얻어 놓기
    nMax = max(data)
    nMin = min(data)
    # background 그리기
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill='white', tag=corrent_canvas_status)

    if nMax == 0: # devide by zero 방지
        nMax=1

    rectWidth = (canvasWidth // nData) # 데이터 1개의 폭.
    percentage_of_rect = 1 / 2  # 폭의 기둥의 비율
    
    bottom = canvasHeight - 20 # bar의 bottom 위치
    maxheight = canvasHeight - 40 # bar의 최대 높이.(위/아래 각각 20씩 여유.)
    for i in range(nData): # 각 데이터에 대해..
        # max/min은 특별한 색으로.
        if nMax == data[i]: color="red"
        elif nMin == data[i]: color='blue'
        else: color="grey"
        
        curHeight = maxheight * data[i] / nMax # 최대값에 대한 비율 반영
        top = bottom - curHeight # bar의 top 위치
        left = i * rectWidth + rectWidth * (1 - percentage_of_rect) / 2 # bar의 left 위치
        right = (i + 1) * rectWidth - rectWidth * (1 - percentage_of_rect) / 2# bar의 right 위치
        canvas.create_rectangle(left, top, right, bottom, fill=color, tag=corrent_canvas_status, activefill='yellow')
        # 위에 값, 아래에 번호.
        canvas.create_text((left+right)//2, top-10, text=data[i], tags=corrent_canvas_status)
        canvas.create_text((left+right)//2, bottom+10, text=i+1, tags=corrent_canvas_status)


def draw_canvas():
    global canvas
    if corrent_canvas_status == default_status:
        text1 = canvas.create_text(200,220, text = corrent_canvas_status, font = ("나눔고딕코딩", 20),tags=corrent_canvas_status)
        # 여기서 날씨정보

    elif corrent_canvas_status == opposite_status:
        # 여기서 위에 나온 정보들의 그래프를 그린다.
        draw_graph([670, 900, 150], 580, 240)

def View_Detail():
    global corrent_canvas_status, next_canvas_status

    # 현재 그림을 지운다.
    canvas.delete(corrent_canvas_status)
    # staus 교환
    corrent_canvas_status, next_canvas_status = next_canvas_status, corrent_canvas_status
    View_Detail_Button["text"] = next_canvas_status
    # 새로운 그림을 그린다.
    draw_canvas()
    pass

def Refresh_markers():
    global markerlist

    for marker in markerlist:
        marker.delete()
        # marker_1.delete()

def Refresh():
    Refresh_markers()

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
Frame_information=Frame(root,padx=10, pady=10, bg='#CCFFFF')
Frame_information.pack(side="top",fill="both",expand=True)

    #임시 지도 출력부
Frame_map=Frame(root,padx=10, pady=10, bg='#999999')
Frame_map.pack(side="top",fill="both",expand=True)
#------------------------<위젯 부분>--------------------------------

    # 제목 레이블
Title_Lable= Label(Frame_title,font=fontTitle,text="★오늘의 날씨는 푸르당★",bg='#FFFF99')
Title_Lable.pack(anchor="center",fill="both")
    
    # 검색 엔트리 , 검색 버튼, 새로고침 버튼 
Search_Entry= Entry(Frame_search,font=fontNormal,width=30,borderwidth=10,relief='ridge')
Search_Entry.pack(side="left",padx=10)

Search_Button=Button(Frame_search,width=5,font=fontNormal,text="검색",command=Search_city)
Search_Button.pack(side="left",padx=10)

Renewal_Button=Button(Frame_search,width=10,font=fontNormal,text="새로고침",command=Refresh)
Renewal_Button.pack(side="left",padx=10)

    # 현재 최고 최저 기온 레이블 , 상세보기 버튼, 이메일 버튼
Cur_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="현재 기온 {0}".format(Cur_temp +"도"),bg='#FFFF99')
Cur_Temp_Lable.pack(side="left",padx=10,fill="both")
    
City_Name_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',width=13,text= "O O 시",bg='#FFFF99')
City_Name_Lable.pack(side="left",padx=10,fill="both")

# Low_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="최저 기온 {0}".format(Cur_temp+"도"),bg='#FFFF99')
# Low_Temp_Lable.pack(side="left",padx=10,fill="both")

Send_Email_Button = Button(Frame_etc,font=fontNormal,image=mail_img)
Send_Email_Button.pack(side="right",padx=10,fill="both")


View_Detail_Button= Button(Frame_etc,width=13,font=fontNormal,text=next_canvas_status,command=View_Detail)
View_Detail_Button.pack(side="right",padx=10,fill="both")


    # 날씨 정보 그래프 레이블

canvas = Canvas(Frame_information, bg = "white")
canvas.pack(fill="both")

draw_canvas() # 한번 먼저 그려놓는다

    # 지도 레이블
map_widget = tkintermapview.TkinterMapView(Frame_map, width=800, height=500, corner_radius=0)
map_widget.pack()

root.mainloop()

