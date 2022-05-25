from asyncio.windows_events import NULL
from re import L
from tkinter import *
import tkinter
import pickle
from tkinter import font
# 초기화를 해주지 않아도 되는 dict
from collections import defaultdict


root = Tk()
root.geometry("600x700+600+100")
root.title('Sun')

#-----------------------etc----------------------------------------

f = open('adress', 'rb') #pickle 사용을 위해 바이너리 읽기 파일 오픈
adress_dict = pickle.load(f) #파일에서 리스트 load

cities = ["서울","부산","경기","인천"]
mail_img= PhotoImage(file=r"C:\Users\NA HYEON\Desktop\게임공학\3학년\스크립트언어\실습\05-17\mail_640_416.png")
weather_top_img=PhotoImage(file=r"C:\Users\NA HYEON\Desktop\게임공학\3학년\스크립트언어\실습\05-17\weather_top.PNG")
weather_bottom_img=PhotoImage(file=r"C:\Users\NA HYEON\Desktop\게임공학\3학년\스크립트언어\실습\05-17\weather_bottom.PNG")


#------------------------검색 함수----------------------------------

def Search_city():
    global cities
    global Search_Entry
    global adress_dict
    for_search = Search_Entry.get()

    value = NULL

    flag = False

    import pprint
    # adress_dict에서 for_search 찾는다.
    for level_2 in adress_dict.values():
        for level_3 in level_2.values():
            for adress in level_3:
                if for_search == adress:
                    print(for_search)
                    print(level_3[adress])
                    flag = True
                    break
                    # level_3[adress] 가 튜플임. 순서대로 X, Y, 위도, 경도
                if flag: break
            if flag: break
        if flag: break

    if not flag:
        print(for_search)
        print("찾지 못 함")  
                            # 1. 찾지 못 했을 경우 다른 값을 반환하고, 만약 이 값이 반환되면 찾지 못했다고 판단해야함. 
                            # 2. 혹은 그냥 입력 받을때 기본값을 NULL로 해놓고 NULL이면 찾지 못했다고 코딩하면 될듯.

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
High_Temp_Lable= Label(Frame_etc,font=fontNormal,borderwidth=3,relief='groove',text="최고 기온 {0}".format("xx도"),bg='#FFFF99')
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

