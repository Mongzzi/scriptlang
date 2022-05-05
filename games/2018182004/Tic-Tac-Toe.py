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

class cell:
    def __init__(self):
        global root
        self.status = 0 #  0=empty   1=o      2=x
        self.Bt= Button(root,image=img_e,padx=10,pady=10,command=self.call_back)
        self.Bt.config(width=100,height=100)
    
    def call_back(self):
        self.change_status()
        self.show_turn()
        self.game_result()
    
    def change_status(self):
        global turn
        if self.status ==0:  
            if turn %2 == 0:
                self.status= 1
                self.Bt.config(image=img_o)
                
            elif turn %2 == 1:
                self.status=2
                self.Bt.config(image=img_x)
            
            turn+=1 
        else:
            print("둘수 없는 자리입니다.")
        
        print("status = ",self.status,"turn = ",turn)
        
    
    def show_turn(self): 
        global turn
        global result_lable
        if turn %2==0:
                result_lable.config(text="O차례")
        elif turn %2 ==1:
                result_lable.config(text="X차례")   

    def game_result(self):
        global turn ,result_lable, cells
        #가로
        for i in range(3):
            if cells[3*i].status!=0 and cells[3*i].status== cells[(3*i)+1].status== cells[(3*i)+2].status:
                if cells[3*i].status==1:
                    result_lable.config(text="O승리")
                    self.game_end()
                    return
                elif cells[3*i].status==2:
                    result_lable.config(text="X승리")
                    self.game_end()
                    return
                
        #세로
        for i in range(3):
            if cells[i].status!=0 and cells[i].status== cells[3+i].status== cells[6+i].status:
                if cells[i].status==1:
                    result_lable.config(text="O승리")
                    self.game_end()
                    return
                elif cells[i].status==2:
                    result_lable.config(text="X승리")
                    self.game_end()
                    return        
                
        #대각선경우    
        if (cells[0].status!=0 and cells[0].status== cells[4].status== cells[8].status) or (cells[2].status!=0 and cells[2].status== cells[4].status== cells[6].status):
            if cells[4].status==1:
                result_lable.config(text="O승리")
                self.game_end()
                return
            elif cells[4].status==2:
                result_lable.config(text="X승리")
                self.game_end()
                return              
        #무승부
        if turn == 9:
            result_lable.config(text="무승부")
    
    
    def grid(self,r,c):
        self.Bt.grid(row=r,column=c)

    def game_end(self):
        global cells
        for i in range(9):
            cells[i].Bt.config(state=DISABLED)





result_lable = Label(root,font=fontNormal,text="게임시작",justify='center')
cells = [ cell() for _ in range(9)]

for i in range(9):
    cells[i].grid(i//3,i%3)
    
result_lable.grid(row=4,column=1)


root.mainloop()
