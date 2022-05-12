from calendar import c
from distutils.util import change_root
from faulthandler import disable
from textwrap import fill
from tkinter import *
from tkinter.tix import COLUMN
from tkinter import font

turn = 0
root = Tk()
root.title('Tic-Tac-Toe')

img_x = PhotoImage(file = "C:\\Users\\NA HYEON\\Desktop\\게임공학\\3학년\\스크립트언어\\실습\\05-03\\x.gif")
img_o = PhotoImage(file="C:\\Users\\NA HYEON\\Desktop\\게임공학\\3학년\\스크립트언어\\실습\\05-03\\o.gif")
img_e = PhotoImage(file="C:\\Users\\NA HYEON\\Desktop\\게임공학\\3학년\\스크립트언어\\실습\\05-03\\empty.gif")
fontNormal=font.Font(root,size=15,weight='bold')

class cell():
    def __init__(self):
        global root
        # self.row=row
        # self.col=col
        self.color = "white"
        
        self.Bt=Canvas(root,width=100,height=100,bg='blue')
        self.Bt.create_oval(0,0,100,100,fill='white',tags="oval")
        self.Bt.bind("<Button-1>",self.clicked)

    def clicked(self,event):
        global turn
                
        if self.color == "white":  
            if turn %2 == 0:
                self.setColor("red")
                turn+=1
                
            elif turn %2 == 1:
                nextcolor="red" if self.color !="red" else "yellow"
                self.setColor("yellow")
                turn+=1
        else:
            print("둘수 없는 자리입니다.")
        
        self.show_turn()
        print("status = ",self.color,"turn = ",turn)
        
    def setColor(self,color):
        self.Bt.delete("oval")
        self.color=color
        self.Bt.create_oval(0,0,100,100,fill=self.color,tags="oval")
    
    # check_valid , clicked 함수 손봐야함 --------------- 여기서부터 시작
    
    def check_valid(self):
        global cells
        for i in range(42):
            if (i//7) == 5 and cells[i].color== "white":
                return True

            else:
                if cells[i+7].color==self.color  or cells[i-7].color==self.color:
                    return True
                elif cells[i+1].color== self.color or cells[i-1].color==self.color:
                    return True
                elif cells[i-8].color==self.color or cells[i+8].color==self.color:
                    return True
                else: return False
    
    def show_turn(self): 
        global turn
        global result_lable
        if turn %2==0:
                result_lable.config(text="빨강 차례")
        elif turn %2 ==1:
                result_lable.config(text="노랑 차례")   
    
    
    def grid(self,r,c):
        self.Bt.grid(row=r,column=c)

    # def grid(self):
    #     self.Bt.grid(row=self.row,column=self.col)
    
    def game_end(self):
        global cells
        for i in range(9):
            cells[i].Bt.config(state=DISABLED)





result_lable = Button(root,font=fontNormal,text="새로시작",justify='center')
cells = [ cell() for _ in range(6*7)]

# cells = [[]*7]
# temp=[]
# for i in range(6):
#     for j in range(7):
#         temp.append(cell(i,j))  
#     cells.append(temp)


for i in range(42):
    cells[i].grid(i//7,i%7)
    
# for i in range(6):
#     for j in range(7):
#         cells[i][j].grid()

    
result_lable.grid(row=7,column=3)


root.mainloop()
