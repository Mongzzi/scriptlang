import math
from secrets import choice
from tkinter import * # Import tkinter




class Hangman:
    def __init__(self):
        self.draw()
    
    def draw(self):
        global num_Miss,MissedLetters
        global word,pword
        global Game_Over_win, Game_Over_lose
        # 한꺼번에 지울 요소들을 "hangman" tag로 묶어뒀다가 일괄 삭제.
        canvas.delete("hangman")

        # 인자 : (x1,y1)=topleft, (x2,y2)=bottomright, start=오른쪽이 0도(반시계방향), extent=start부터 몇도까지인지
        #    style='pieslice'|'chord'|'arc'
        canvas.create_arc(20, 200, 100, 240, start = 0, extent = 180, style='chord', tags = "hangman") # Draw the base
        canvas.create_line(60, 200, 60, 20, tags = "hangman")  # Draw the pole
        canvas.create_line(60, 20, 160, 20, tags = "hangman") # Draw the hanger
        # -------------------------------------------------------------------------------------        
        
        text1 = canvas.create_text(200,220, text = list("단어추측:")+pword, font = ("나눔고딕코딩", 10),tags="hangman")
        text2 = canvas.create_text(200,240, text = list("틀린글자:")+MissedLetters, font = ("나눔고딕코딩", 10),tags="hangman")
        
        # --------------------아래부터 틀릴때마다 그리기----------------------------------------
        
        radius = 20 # 반지름
        if num_Miss >=1 :
            canvas.create_line(160, 20, 160, 40, tags = "hangman") # Draw the hanger

        # -------------------------------------------------------------------------------------
        
        # Draw the circle
        if num_Miss >=2 :
            canvas.create_oval(140, 40, 180, 80, tags = "hangman") # Draw the hanger

        # -------------------------------------------------------------------------------------
        # Draw the left arm (중심(160,60)에서 45도 움직인 지점의 x좌표는 cos로, y좌표는 sin으로 얻기)
        x1 = 160 - radius * math.cos(math.radians(45))
        y1 = 60 + radius * math.sin(math.radians(45))
        x2 = 160 - (radius+60) * math.cos(math.radians(45))
        y2 = 60 + (radius+60) * math.sin(math.radians(45))

        if num_Miss >=3 :
            canvas.create_line(x1, y1, x2, y2, tags = "hangman")
        # -------------------------------------------------------------------------------------
        x1 = 160 + radius * math.cos(math.radians(45))
        y1 = 60 + radius * math.sin(math.radians(45))
        x2 = 160 + (radius+60) * math.cos(math.radians(45))
        y2 = 60 + (radius+60) * math.sin(math.radians(45))

        if num_Miss >=4 :
            canvas.create_line(x1, y1, x2, y2, tags = "hangman")        
        # -------------------------------------------------------------------------------------
        if num_Miss >=5 :
            canvas.create_line(160, 80, 160, 140, tags = "hangman")        
        # -------------------------------------------------------------------------------------
        x1 = 160
        y1 = 140
        x2 = 160 - (radius+60) * math.cos(math.radians(45))
        y2 = 140 + (radius+60) * math.sin(math.radians(45))

        if num_Miss >=6 :
            canvas.create_line(x1, y1, x2, y2, tags = "hangman")        
        # --------------------게임 패 및 캔버스 조정---------------------------------------------
        x1 = 160 
        y1 = 140
        x2 = 160 + (radius+60) * math.cos(math.radians(45))
        y2 = 140 + (radius+60) * math.sin(math.radians(45))

        if num_Miss >=7 :
            Game_Over_lose=True
            canvas.create_line(x1, y1, x2, y2, tags = "hangman")
            canvas.itemconfig(text1,text=list("정답:{0}".format(word)))
            canvas.itemconfig(text2,text="패배! 게임을 계속하려면 ENTER를 누르세요")

        # ---------------------게임 승 및 캔버스 조정---------------------------------
        if Game_Over_win == True:
            canvas.itemconfig(text1,text=list("정답:{0}".format(word)))
            canvas.itemconfig(text2,text="승리! 게임을 계속하려면 ENTER를 누르세요")
        
        
# Initialize words, get the words from a file
infile = open(r"C:\Users\NA HYEON\Desktop\게임공학\3학년\스크립트언어\실습\05-17\hangman.txt", "r")
words = infile.read().split()
word= choice(words)
#word= "aabbccdd"
pword= ['*']*len(word)
CorrectedLetters= []
num_Corr=0

MissedLetters= []  # 틀린 알파벳 리스트
num_Miss=0 # 틀린 알파벳 갯수
Game_Over_win = False
Game_Over_lose = False

window = Tk() # Create a window
window.title("행맨") # Set a title

def processKeyEvent(event):  
    global hangman
    global word,pword
    global num_Miss,MissedLetters
    if event.char >= 'a' and event.char <= 'z':
        is_find= False
        for i in range(len(word)):
            if event.char == word[i]:
                pword[i]=event.char
                is_find=True   
        if is_find == False:
            
            if str(MissedLetters).find(event.char)==-1:
                num_Miss+=1
                MissedLetters.append(event.char)
        is_end()
        hangman.draw()
    
    elif event.keycode == 13:
        pass

        
def is_end():
    global pword,Game_Over_win
    for i in range(len(pword)):
        if pword[i]=='*':
            Game_Over_win=False
            return
    Game_Over_win=True        
          
def enter(event):
    global hangman
    global Game_Over_win , Game_Over_lose
    global word,pword
    global CorrectedLetters,num_Corr
    global MissedLetters,num_Miss
    
    if Game_Over_win or Game_Over_lose:
        word= choice(words)
        pword= ['*']*len(word)
        CorrectedLetters= []
        num_Corr=0
        MissedLetters= []  # 틀린 알파벳 리스트
        num_Miss=0 # 틀린 알파벳 갯수
        Game_Over_win = False
        Game_Over_lose = False
        canvas.delete("hangman")

        canvas.create_arc(20, 200, 100, 240, start = 0, extent = 180, style='chord', tags = "hangman") # Draw the base
        canvas.create_line(60, 200, 60, 20, tags = "hangman")  # Draw the pole
        canvas.create_line(60, 20, 160, 20, tags = "hangman") # Draw the hanger

        text1 = canvas.create_text(200,220, text = list("단어추측:")+pword, font = ("나눔고딕코딩", 10),tags="hangman")
        text2 = canvas.create_text(200,240, text = list("틀린글자:")+MissedLetters, font = ("나눔고딕코딩", 10),tags="hangman")
        hangman.draw()
        

#------------------------------------------------------------------------------------------------------------------------
width = 400
height = 280    
# 선, 다각형, 원등을 그리기 위한 캔버스를 생성
canvas = Canvas(window, bg = "white", width = width, height = height)
canvas.pack()

hangman = Hangman()

# Bind with <Key> event
canvas.bind("<Key>", processKeyEvent)
canvas.bind("<Return>",enter)
# key 입력 받기 위해 canvas가 focus 가지도록 함.

canvas.focus_set()
window.mainloop() # Create an event loop
