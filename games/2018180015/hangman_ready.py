import math
from tkinter import * # Import tkinter
from random import *
    
class Hangman:
    nCorrectChar = 0 # 맞춘 알파벳 
    nMissChar = 0 # 틀린 알파벳
    nCorrectedLetters = [] #맞춘 알파벳 리스트
    nMissedLetters =[] #틀린 알파벳 리스트
    gool_ward = ''
    show_ward=''
    is_over = False

    def __init__(self):
        self.draw()
        self.setWard()

    def reset(self):
        self.is_over = False
        self.nCorrectChar = 0
        self.nMissChar = 0
        self.nCorrectedLetters = []
        self.nMissedLetters = []
        self.gool_ward = ''
        self.show_ward=''

    def setWard(self):
        # 새로운 단어를 선택하고 게임 (재)시작.
        self.reset()
        # 새로운 단어를 선택
        f = open( r'C:\Users\yyyyw\Desktop\script\11주\hangman.txt', 'r' )

        # ward_list = f.read()
        ward_list = (list(map(str, f.read().split())))

        self.gool_ward = ward_list[randrange(len(ward_list))]
        
        f.close()

    def draw_rope(self,radius=20):
        canvas.create_line(160, 20, 160, 40, tags = "hangman") # Draw the hanger

    def draw_head(self,radius=20):
        canvas.create_oval(140, 40, 180, 80, tags = "hangman") # Draw the hanger

    def draw_LA(self, radius=20):
        self.draw_head()
        x1 = 160 - radius * math.cos(math.radians(45))
        y1 = 60 + radius * math.sin(math.radians(45))
        x2 = 160 - (radius+60) * math.cos(math.radians(45))
        y2 = 60 + (radius+60) * math.sin(math.radians(45))

        canvas.create_line(x1, y1, x2, y2, tags = "hangman") # 왼팔

    def draw_RA(self, radius=20):
        self.draw_LA()
        x1 = 160 - radius * math.cos(math.radians(135))
        y1 = 60 + radius * math.sin(math.radians(135))
        x2 = 160 - (radius+60) * math.cos(math.radians(135))
        y2 = 60 + (radius+60) * math.sin(math.radians(135))

        canvas.create_line(x1, y1, x2, y2, tags = "hangman") # 오른팔

    def draw_body(self,radius=20):
        self.draw_RA()
        x1 = 160 
        y1 = 80
        x2 = 160
        y2 = 140

        canvas.create_line(x1, y1, x2, y2, tags = "hangman") # 몸

    def draw_LL(self, radius=20):
        self.draw_body()
        x1 = 160 
        y1 = 140
        x2 = 160 - (radius+60) * math.cos(math.radians(45))
        y2 = 140 + (radius+60) * math.sin(math.radians(45))

        canvas.create_line(x1, y1, x2, y2, tags = "hangman") # 왼다리

    def draw_RL(self, radius=20):
        self.draw_LL()
        x1 = 160 
        y1 = 140
        x2 = 160 - (radius+60) * math.cos(math.radians(135))
        y2 = 140 + (radius+60) * math.sin(math.radians(135))

        canvas.create_line(x1, y1, x2, y2, tags = "hangman") # 오른다리

    def draw(self):
        # 한꺼번에 지울 요소들을 "hangman" tag로 묶어뒀다가 일괄 삭제.
        canvas.delete("hangman")

        # 인자 : (x1,y1)=topleft, (x2,y2)=bottomright, start=오른쪽이 0도(반시계방향), extent=start부터 몇도까지인지
        #    style='pieslice'|'chord'|'arc'
        canvas.create_arc(20, 200, 100, 240, start = 0, extent = 180, style='chord', tags = "hangman") # Draw the base
        canvas.create_line(60, 200, 60, 20, tags = "hangman")  # Draw the pole
        canvas.create_line(60, 20, 160, 20, tags = "hangman") # Draw the hanger
        
        radius = 20 # 반지름

        key = self.nMissChar
        print(key)
        self.draw_rope()

        if key == 1:
            self.draw_head()
        elif key == 2:
            self.draw_LA()
        elif key == 3:
            self.draw_RA()
        elif key == 4:
            self.draw_body()
        elif key == 5:
            self.draw_LL()
        elif key >= 6:
            self.draw_RL()

        self.set_show_ward()

        text1 = canvas.create_text(200,220, text = str("단어추측:")+self.show_ward, font = ("나눔고딕코딩", 10),tags="hangman")
        text2 = canvas.create_text(200,240, text = list("틀린글자:")+self.nMissedLetters, font = ("나눔고딕코딩", 10),tags="hangman")

        if key >=6 :
            self.is_over=True
            # canvas.create_line(x1, y1, x2, y2, tags = "hangman")
            canvas.itemconfig(text1,text=list("정답:{0}".format(self.gool_ward)))
            canvas.itemconfig(text2,text="패배! 게임을 계속하려면 ENTER를 누르세요")

        if self.gool_ward == self.show_ward:
            self.is_over=True
            canvas.itemconfig(text1,text=list("정답:{0}".format(self.gool_ward)))
            canvas.itemconfig(text2,text="승리! 게임을 계속하려면 ENTER를 누르세요")

        

    def set_show_ward(self):
        len_of_ward = len(self.gool_ward)
        self.show_ward = ''
        print('확인중')

        check_list = [False for i in range(len_of_ward)]
        
        for i, char in enumerate(self.gool_ward):
            if char in self.nCorrectedLetters:
                check_list[i] = True


        for i, flag in enumerate(check_list):
            if flag:
                self.show_ward += self.gool_ward[i]
            else:
                self.show_ward += '*'
        print(self.show_ward)

                
    def guess(self, letter):

        pass




        

        
# Initialize words, get the words from a file
infile = open(r"C:\Users\yyyyw\Desktop\script\11주\hangman.txt", "r")   # C:\Users\yyyyw\Desktop\script\11주\hangman.txt
words = infile.read().split()
    
window = Tk() # Create a window
window.title("행맨") # Set a title

def processKeyEvent(event):  #입력받은 키 처리 함수
    global hangman
    if event.char >= 'a' and event.char <= 'z':
        # 이미 선택했던 단어인지 확인

        if event.char in hangman.gool_ward and event.char not in hangman.nCorrectedLetters:
            hangman.nCorrectChar += 1
            hangman.nCorrectedLetters.append(event.char)
        else:
            if event.char not in hangman.nMissedLetters:
                hangman.nMissChar += 1
                hangman.nMissedLetters.append(event.char)

    elif event.keycode == 13:# 엔터키
        if hangman.is_over:
            hangman.setWard()

    hangman.draw()
    
width = 400
height = 280    
# 선, 다각형, 원등을 그리기 위한 캔버스를 생성
canvas = Canvas(window, bg = "white", width = width, height = height)
canvas.pack()

hangman = Hangman()

# Bind with <Key> event
canvas.bind("<Key>", processKeyEvent)
# key 입력 받기 위해 canvas가 focus 가지도록 함.
canvas.focus_set()

window.mainloop() # Create an event loop
