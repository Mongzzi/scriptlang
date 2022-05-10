from tkinter import *

_MAXROW = 6
_MAXCOL = 7
# _TargetCount = 4

Turn = "red"
Turn_count = 0

cells=None

process_button = None

button_text ="red 차례"

def button_callback():
    global is_over
    if is_over == True:
        process_button["command"] = restart
        process_button["text"] = "새로시작"
        is_over = False

def restart():
    global cell_list, process_button, Turn, Turn_count, end_text_front
    for r in range(_MAXROW):
        for c in range(_MAXCOL):
            cell_list[r][c].able = False
            cell_list[r][c].setColor("white")
            cell_list[r][c]["bg"] = "blue"

            # 지우고 다시 그려야함

    for c in range(_MAXCOL):
        cell_list[_MAXROW-1][c].able = True
    
    process_button["command"] = button_callback
    process_button["text"] = "red 차례"
    Turn = "red"
    Turn_count = 0
    # end_text_front = "비김!" 

size_of_cell = 50
soc = size_of_cell

oval_size_list=[4,4,soc,soc]

end_text_front = "비김!"
end_text_behind = "게임이 끝났습니다"
is_over = False

def finish():
    global process_button, end_text_behind, end_text_front, is_over
    is_over = True
    process_button["text"] = end_text_front + end_text_behind
    disable_all()

def disable_all():
    global cell_list
    for r in range(_MAXROW):
        for c in range(_MAXCOL):
            cell_list[r][c].able = False

def red_win():
    global end_text_front
    end_text_front = "red 승리!"
    finish()
    return 'red'

def yellow_win():
    global end_text_front
    end_text_front = "yellow 승리!"
    finish()
    return 'yellow'

def is_draw():
    global Turn_count, end_text_front
    if Turn_count == _MAXROW*_MAXCOL:
        end_text_front = "비김!"
        finish()

def check_row():
    global cell_list
    for c in range(_MAXCOL):
        for r in range(_MAXROW-(4-1)):
            if cell_list[r][c].color == cell_list[r+1][c].color == cell_list[r+2][c].color==cell_list[r+3][c].color:
                cell_list[r][c]["bg"] = cell_list[r+1][c]["bg"] = cell_list[r+2][c]["bg"]=cell_list[r+3][c]["bg"] = who_is_winner(r,c)

def check_col():
    global cell_list
    for r in range(_MAXROW):
        for c in range(_MAXCOL-(4-1)):
            if cell_list[r][c].color == cell_list[r][c+1].color == cell_list[r][c+2].color==cell_list[r][c+3].color:
                cell_list[r][c]["bg"] = cell_list[r][c+1]["bg"] = cell_list[r][c+2]["bg"]=cell_list[r][c+3]["bg"] = who_is_winner(r,c)

def check_diagonal():
    for r in range(_MAXROW-(4-1)):
        for c in range(_MAXCOL-(4-1)):
            if cell_list[r][c].color == cell_list[r+1][c+1].color == cell_list[r+2][c+2].color==cell_list[r+3][c+3].color:
                cell_list[r][c]["bg"] = cell_list[r+1][c+1]["bg"] = cell_list[r+2][c+2]["bg"]=cell_list[r+3][c+3]["bg"] = who_is_winner(r,c)
            if cell_list[r+3][c].color == cell_list[r+2][c+1].color == cell_list[r+1][c+2].color==cell_list[r][c+3].color:
                cell_list[r+3][c]["bg"] = cell_list[r+2][c+1]["bg"] = cell_list[r+1][c+2]["bg"]=cell_list[r][c+3]["bg"] = who_is_winner(r+3,c)

def judge():
    # 무승부
    is_draw()
    # 수평승리
    check_col()
    # 수직승리
    check_row()
    # 대각승리
    check_diagonal()

def who_is_winner( r, c ):
    if cell_list[r][c].color == 'red':
        return red_win()
    elif cell_list[r][c].color == 'yellow':
        return yellow_win()

class Cell(Canvas):
    def __init__(self, parent, row, col, width = 20, height = 20):  # 20은 기본값으로 해두신듯?
        Canvas.__init__(self, parent, width = width, height = height, 
        bg = "blue", borderwidth = 0) # borderwidth는 뭐에 쓰는가?  원래 2였음
        self.color = "white"
        self.row = row
        self.col = col
        # https://tkdocs.com/shipman/canvas.html
        # https://tkdocs.com/shipman/create_oval.html
        self.create_oval(oval_size_list, fill = "white", tags="oval")
        self.bind("<Button-1>", self.clicked)

        self.able = False


    def clicked(self, event): # red 또는 yellow 돌 놓기.
        global Turn, Turn_count, cell_list, process_button
        if self.color == 'white' and self.able==True:    # 혹시 몰라서 2번 검사
            nextcolor = "red" if Turn == "red" else "yellow"
            if Turn == 'red':
                Turn = "yellow"
                process_button["text"] = "yellow 차례"
            else:
                Turn = 'red'
                process_button["text"] = "red 차례"

            Turn_count = Turn_count + 1
            self.setColor(nextcolor)
            # 아래서부터 클릭 가능 기능 추가하기. 초기화를 아래줄 빼고 불가능으로 해두고 클릭 시 위칸을 가능으로 바꾼다.
            self.able = False
            if self.row != 0:
                cell_list[self.row-1][self.col].able = True
            judge()


    def setColor(self, color):
        self.delete("oval") # https://pythonguides.com/python-tkinter-canvas/
        self.color = color
        self.create_oval(oval_size_list, fill = self.color, tags="oval")

window = Tk() # Create a window
window.title("Connect Four") # Set title
window.resizable(False, False)  # 크기 변경 불가능?
frame1 = Frame(window)
frame1.pack()

cell_list = [[Cell(frame1, r, c, width = soc, height = soc)for c in range(_MAXCOL)] for r in range(_MAXROW)]

for r in range(_MAXROW):
    for c in range(_MAXCOL):
        cell_list[r][c].grid(row=r,column=c)

for r in range(_MAXROW):
    for c in range(_MAXCOL):
        cell_list[_MAXROW-1][c].able = False

for c in range(_MAXCOL):
    cell_list[_MAXROW-1][c].able = True        

frame2 = Frame(window)
frame2.pack()

process_button = Button(frame2, text=button_text, command=button_callback)
process_button.grid(row=0, column=0)

window.mainloop() # Create an event loop