from asyncio.windows_events import NULL
from re import L
from tkinter import *
import tkinter
from email.mime.text import MIMEText
from tkinter import font
from collections import defaultdict
from numpy import true_divide
import tkintermapview   # 지도를 위한 참조
from PIL import ImageTk

import spam

import common_functions

root = Tk()
root.geometry("600x700+600+100")
root.title('Sun')

#------------------------이미지-----------------------------------

canvas_bg=PhotoImage(file=r"scriptlang\프로젝트\canvas_bg.png")
mail_img= PhotoImage(file=r"scriptlang\프로젝트\mail_640_416.png")
weather_top_img=PhotoImage(file=r"scriptlang\프로젝트\weather_top.PNG")
weather_bottom_img=PhotoImage(file=r"scriptlang\프로젝트\weather_bottom.PNG")

#------------------------global 변수------------------------------

nx = "62"               # 위도 변수
ny = "125"              # 경도 변수

latitude = NULL         # 지도용 위도 경도
longitude = NULL

base_date = ""
base_time = ""

weather_list = [[],[],[],[],[]] # [0] = 강수확률 [1] = 강수량 [2] = 온도 [3] =습도 [4] = 하늘상태

cloud=PhotoImage(file=r"scriptlang\프로젝트\cloud.PNG")
sun=PhotoImage(file=r"scriptlang\프로젝트\sun.PNG")
rain=PhotoImage(file=r"scriptlang\프로젝트\rain.PNG")


Cur_temp = "0"          # 현재 온도    
Cur_Air= "구름 많음"             # 현재 하늘 상태
Cur_Rain= "없음"             # 현재 강수량
Cur_Humidity ="0"        # 현재 습도

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
    global items,Cur_temp,Cur_Air,Cur_Humidity,Cur_Rain
    global base_date,base_time,weather_list
    base_date, base_time = common_functions.Set_Time()
    
    params ={'serviceKey' : serviceKey,  'numOfRows' : '1000','pageNo' : '1', 'dataType' : 'JSON', 'base_date' : base_date, 'base_time' : base_time, 'nx' : nx, 'ny' : ny }
    response = requests.get(url, params=params)
    #print(response.content)
    items = response.json().get('response').get('body').get('items')
    if weather_list:
        weather_list = [[],[],[],[],[]]

    for item in items['item']:
        if item['category'] =='PTY':    #강수확률- 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
            #print(item['fcstValue'])
            cnt=0
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='RN1':    #1시간 강수량
            #print(item['fcstValue'])
            cnt=1
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='T1H':    #온도
            cnt=2
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='REH':    #습도
            #print(item['fcstValue'])        
            cnt=3
            weather_list[cnt].append(item['fcstValue'])
            
        if item['category'] =='SKY':    #하늘상태- 맑음(1), 구름많음(3), 흐림(4)
            #print(item['fcstValue'])
            cnt=4
            weather_list[cnt].append(item['fcstValue'])
            
    print(weather_list)         #weather_list = # [0] = 강수확률 [1] = 강수량 [2] = 온도 [3] =습도 [4] = 하늘상태
   
    if(weather_list[1][0]=='강수없음'): Cur_Rain= False
    else: Cur_Rain = True
    
    Cur_temp=weather_list[2][0]
    Cur_Humidity=weather_list[3][0]
    if(weather_list[4][0]=='1'): Cur_Air = "맑음"
    elif(weather_list[4][0]=='3'): Cur_Air = "구름많음"
    elif(weather_list[4][0]=='4'):Cur_Air="흐림"
    
    
    
    Update_Label_Temp()
    Update_map()
    draw_canvas() # 업데이트할때도 다시 그려야함

#----------------------------etc-----------------------------------
adress_dict = None

# cities = ["서울","부산","경기","인천"]


def Update_Label_Temp():
    global Cur_Temp_Lable
    global Cur_temp
    
    Cur_Temp_Lable.config(text="현재 기온{0}".format(Cur_temp +"도"),bg='#FFFF99')


def sendMail(fromAddr,toAddr,msg):
    import smtplib
    s= smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()
    
    s.login('hjna0206@gmail.com','yebbawamctnrjdky')
    s.sendmail(fromAddr,[toAddr],msg.as_string())
    s.close()
    

def Popup_Popup_command():
    global Email_Popup_Popup
    Email_Popup_Popup.destroy()


def Popup_Popup_command_2():
    global Email_Popup_Popup, Email_Popup

    Email_Popup_Popup.destroy()
    Email_Popup.destroy() # popup 내리기



def onEmailInput():
    global name
    global Email_Entry
    global base_date,base_time,weather_list
    global Email_Popup, Email_Popup_Popup, Popup_Popup_Lable, Popup_Popup_Button
    
    #[0] = 강수확률 [1] = 강수량 [2] = 온도 [3] =습도 [4] = 하늘상태
    #강수확률- 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
    email = Email_Entry.get()
    
    # 이메일 검사
    Email_Flag = False

    # 팝업용 변수들
    main_text = lable_text = popup_command = None

    if '.' in email and '@' in email:
            Email_Flag = True

    if Email_Flag:
        if email:
            show_data = common_functions.make_data(name, base_date,base_time,weather_list)
            msg=MIMEText(show_data)
            msg['Subject']= '날씨 정보'
            try:
                sendMail('hjna0206@gmail.com',email,msg)
                main_text="발송 성공"

                lable_text="성공"
                
                popup_command=Popup_Popup_command_2
            except:
                main_text="오류 발생"

                lable_text="이메일을 다시 확인해 주세요"

                popup_command=Popup_Popup_command
    else:
        main_text = "오류 발생"

        lable_text = '이메일에 '

        if not '.' in email:
            lable_text += '\'.\' '
        if not '@' in email:
            lable_text += '\'@\' '

        lable_text += '(이)가 없습니다.'

        popup_command=Popup_Popup_command

    Email_Popup_Popup = Toplevel(Email_Popup) # popup 띄우기
    Email_Popup_Popup.geometry("400x150")
    Email_Popup_Popup.title(main_text)
    Popup_Popup_Lable= Label(Email_Popup_Popup,font=fontTitle,text=lable_text)
    Popup_Popup_Lable.pack(expand=True)
    Popup_Button = Button(Email_Popup_Popup, text="확인", command=popup_command)
    Popup_Button.pack(anchor="s", padx=10, pady=10)


def onEmailPopup():
    global root, Email_Popup
    Email_Popup = Toplevel(root) # popup 띄우기
    Email_Popup.geometry("300x150")
    Email_Popup.title("받을 이메일 주소 입력")

    global Email_Entry, Popup_Button
    Email_Entry = Entry(Email_Popup, width = 200,)
    Email_Entry.pack(fill='x', padx=10, expand=True)

    Popup_Button = Button(Email_Popup, text="보내기", command=onEmailInput)
    Popup_Button.pack(anchor="s", padx=10, pady=10)

name = None

def Search_city():
    global cities
    global Search_Entry
    global City_Name_Lable
    global adress_dict
    global nx, ny
    global items, Max_temp
    global latitude, longitude
    global name
    for_search = Search_Entry.get()

    val = NULL

    return_lsit = common_functions.Get_Name_Val_From_Dict(for_search, adress_dict)
    
    if not len(return_lsit):
        City_Name_Lable['text'] = str(name)
        Cur_Temp_Lable['text'] = str(for_search)+" 찾지 못함"
    else:
        name, val = return_lsit[0]
        nx, ny, latitude, longitude = val
        if type(nx) == int:
            nx = spam.itoa(nx)
        if type(ny) == int:
            ny = spam.itoa(ny)
        
        City_Name_Lable.config(text=str(name))
        Update()

def draw_default(canvasWidth,canvasHeight):
    global canvas
    global Cur_temp,Cur_Air,Cur_Humidity,Cur_Rain
    canvas.delete(corrent_canvas_status)
    global weather_list
    
    if(Cur_Rain==False):
        
        if Cur_Air=='맑음':canvas.create_image(300,80,image=sun,tags=corrent_canvas_status)
        elif Cur_Air=='구름많음' or Cur_Air=='흐림':canvas.create_image(300,80,image=cloud,tags=corrent_canvas_status)
    else:
        canvas.create_image(300,80,image=rain,tags=corrent_canvas_status)
    
    
    canvas.create_text(300,180, text ="하늘 상태 =  "+Cur_Air, font = ("나눔고딕코딩", 20),tags=corrent_canvas_status)
    canvas.create_text(300,220, text ="현재 습도 =  "+Cur_Humidity+"%", font = ("나눔고딕코딩", 20),tags=corrent_canvas_status)

def draw_graph(canvasWidth, canvasHeight):
    global canvas
    canvas.delete(corrent_canvas_status) # 기존 그림 지우기

    data = list(map(int, weather_list[2]))

    if not len(data): # 데이터 없으면 return
        canvas.create_text(canvasWidth/2,(canvasHeight/2), text="No Data", tags=corrent_canvas_status)
        return
    nData = len(data) # 데이터 개수, 최대값, 최소값 얻어 놓기
    nMax = max(data)
    nMin = min(data)

    # 크기 조절
    size_of_infomation = 40
    canvasWidth = canvasWidth - size_of_infomation

    # background 그리기
    # canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill='white', tag=corrent_canvas_status)

    if nMax == 0: # devide by zero 방지
        nMax=1

    rectWidth = (canvasWidth // nData) # 데이터 1개의 폭.
    percentage_of_rect = 1 / 2  # 폭의 기둥의 비율
    
    # bottom = canvasHeight - 50 # bar의 bottom 위치 
    bottom = canvasHeight - 50 # bar의 bottom 위치 
    maxheight = canvasHeight - 70 # bar의 최대 높이.(위/아래 각각 50씩 여유.  표 아래에 정보를 추가 할 때마다 15씩 늘일것)

    coordinates = [] # 꺾은선 그래프를 위한 정보.

    for i in range(nData): # 각 데이터에 대해..
        # max/min은 특별한 색으로.
        if nMax == data[i]: color="red"
        elif nMin == data[i]: color='blue'
        else: color="grey"
        
        # curHeight = maxheight * data[i] / nMax # 최대값에 대한 비율 반영 막대그래프
        curHeight = maxheight * ((data[i] - nMin)/(nMax - nMin)) # 꺾은선 그래프를 위한 비율
        top = bottom - curHeight # bar의 top 위치
        left = size_of_infomation + i * rectWidth + rectWidth * (1 - percentage_of_rect) / 2 # bar의 left 위치
        right = size_of_infomation + (i + 1) * rectWidth - rectWidth * (1 - percentage_of_rect) / 2# bar의 right 위치
        # canvas.create_rectangle(left, top, right, bottom, fill=color, tag=corrent_canvas_status, activefill='yellow')
        middle = (right+left)/2

        coordinates.append((top, middle))
        # 온도
        canvas.create_text((left+right)//2, top-10, text=data[i], tags=corrent_canvas_status)
        # 시간
        hour = (int(base_time)//100 + i) % 24
        if not hour:    # 0시로 표시하고 싶으면 주석처리할것.
            hour = 24
        canvas.create_text((left+right)//2, bottom+10, text=spam.itoa(hour)+':'+"30", tags=corrent_canvas_status)
        # 강수 확률
        canvas.create_text((left+right)//2, bottom+25, text=weather_list[0][i], tags=corrent_canvas_status)
        # 강수량
        canvas.create_text((left+right)//2, bottom+40, text=weather_list[1][i], tags=corrent_canvas_status)

    for i in range(nData-1): # 막대
        color = 'black'

        top , middle = coordinates[i]
        next_top , next_middle = coordinates[i+1]
        canvas.create_line(middle, top, next_middle,next_top,fill=color, width = 3, tag=corrent_canvas_status)
    
    for i in range(nData): # 원
        if nMax == data[i]: color="red"
        elif nMin == data[i]: color='blue'
        else: color="grey"
        top, middle = coordinates[i]

        r = 4

        canvas.create_oval(middle-r,top-r,middle+r,top+r, fill=color, tag=corrent_canvas_status, activefill='yellow')



    canvas.create_text(30, bottom-10, text='온도', tags=corrent_canvas_status)
    canvas.create_text(30, bottom+10, text='시간', tags=corrent_canvas_status)
    canvas.create_text(30, bottom+25, text='강수 확률', tags=corrent_canvas_status)
    canvas.create_text(30, bottom+40, text='강수량', tags=corrent_canvas_status)


def draw_canvas():
    global canvas
    # 기본 배경을 그린다.
    # 검색된 결과가 없거나 검색한 적이 없으면 배경이 보일 것.
    # 만약 검색한적이 없다면 아래 작업을 하지 않도록 하면 된다.
    canvas.delete("bg")
    
    if len(weather_list[0]) != 0:
        if corrent_canvas_status == default_status:
            # 여기서 날씨정보
            draw_default(580,260)
        elif corrent_canvas_status == opposite_status:
            # 여기서 위에 나온 정보들의 그래프를 그린다.
            draw_graph(580, 260)
    else:
        imagesprite = canvas.create_image([290,130], image=canvas_bg, tags="bg")
        canvas.image_names=canvas_bg

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
Cur_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="      위에서      ",bg='#FFFF99')
Cur_Temp_Lable.pack(side="left",padx=10,fill="both")
    
City_Name_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',width=13,text= "검색을 해주세요",bg='#FFFF99')
City_Name_Lable.pack(side="left",padx=10,fill="both")

# Low_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="최저 기온 {0}".format(Cur_temp+"도"),bg='#FFFF99')
# Low_Temp_Lable.pack(side="left",padx=10,fill="both")

Send_Email_Button = Button(Frame_etc,font=fontNormal,image=mail_img,command=onEmailPopup)
Send_Email_Button.pack(side="right",padx=10,fill="both")

Email_Popup = Email_Entry = Popup_Button = None # 이메일 팝업에 사용
Email_Popup_Popup = Popup_Popup_Lable = Popup_Popup_Button = None    # 이메일 팝업의 팝업에 활용

View_Detail_Button= Button(Frame_etc,width=13,font=fontNormal,text=next_canvas_status,command=View_Detail)
View_Detail_Button.pack(side="right",padx=10,fill="both")


    # 날씨 정보 그래프 레이블

canvas = Canvas(Frame_information, bg = "white")
canvas.pack(fill="both")

draw_canvas() # 한번 먼저 그려놓는다

    # 지도 레이블
map_widget = tkintermapview.TkinterMapView(Frame_map, width=800, height=500, corner_radius=0)
map_widget.pack()

if __name__ == '__main__':
    adress_dict = common_functions.Read_Adress_From_File()

    root.mainloop()

