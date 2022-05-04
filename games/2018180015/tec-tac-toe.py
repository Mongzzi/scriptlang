from tkinter import *


class tec_tac_toe:
    empty = None
    i_X = None
    i_O = None

    def __init__(self):
        self.turn = 0
        self.cells=[' ',' ',' ',' ',' ',' ',' ',' ',' ',]
        self.window = Tk()
        self.window.title("Tic-Tac-Toe")
        if tec_tac_toe.empty == None:
            tec_tac_toe.empty = PhotoImage(file = "C:\\Users\\yyyyw\\Desktop\\script\\Tic-Tac-Toe\\empty.gif")
        if tec_tac_toe.i_X == None:
            tec_tac_toe.i_X = PhotoImage(file = "C:\\Users\\yyyyw\\Desktop\\script\\Tic-Tac-Toe\\x.gif")
        if tec_tac_toe.i_O == None:
            tec_tac_toe.i_O = PhotoImage(file = "C:\\Users\\yyyyw\\Desktop\\script\\Tic-Tac-Toe\\o.gif")

        self.end_text_front = "비김!"
        self.end_text_behind = "게임이 끝났습니다"
        self.is_over = False

        self.cells_frame = Frame(self.window)
        self.cells_frame.grid(row = 0, column = 0)

        self.button_list = [Button(self.cells_frame, image = tec_tac_toe.empty, ) for i in range(9)]
        self.button_list[0]["command"] = lambda: self.pressed_callback(0)
        self.button_list[1]["command"] = lambda: self.pressed_callback(1)
        self.button_list[2]["command"] = lambda: self.pressed_callback(2)
        self.button_list[3]["command"] = lambda: self.pressed_callback(3)
        self.button_list[4]["command"] = lambda: self.pressed_callback(4)
        self.button_list[5]["command"] = lambda: self.pressed_callback(5)
        self.button_list[6]["command"] = lambda: self.pressed_callback(6)
        self.button_list[7]["command"] = lambda: self.pressed_callback(7)
        self.button_list[8]["command"] = lambda: self.pressed_callback(8)

        for i, l in enumerate(self.button_list):
            l.grid(row=i//3, column=i%3, sticky = 'n' )

        self.text_label = Label(self.window, text='O 차례')
        self.text_label.grid(row = 1, column = 0)

    def disable_all(self):
        for i in range(9):
            self.button_list[i]["state"] = DISABLED

    def finish(self):
        self.text_label["text"] = self.end_text_front + self.end_text_behind
        self.disable_all()

    def O_win(self):
        self.end_text_front = "O 승리!"
        self.is_over = True
        self.finish()

    def X_win(self):
        self.end_text_front = "X 승리!"
        self.is_over = True
        self.finish()

    def judge(self):
        if self.turn == 9:
            self.finish()
        for i in range(3):
            if self.cells[i*3] == self.cells[i*3+1] == self.cells[i*3+2]:
                self.who_is_winner(i*3)
                break
            if self.cells[i] == self.cells[i+3] == self.cells[i+6]:
                self.who_is_winner(i)
                break
        if self.cells[0] == self.cells[4] == self.cells[8] or self.cells[2] == self.cells[4] == self.cells[6]:
            self.who_is_winner( 4 )

    def who_is_winner( self, i ):
        if self.cells[i] == 'o':
            self.O_win()
        elif self.cells[i] == 'x':
            self.X_win()

    def pressed_callback(self, i):
        if self.cells[i] == ' ':
            if self.turn % 2 == 1:
                self.button_list[i]["image"] = tec_tac_toe.i_X
                self.cells[i] = 'x'
                self.text_label["text"] = "O 차례"
            if self.turn % 2 == 0:
                self.button_list[i]["image"] = tec_tac_toe.i_O
                self.cells[i] = 'o'
                self.text_label["text"] = "X 차례"
            self.turn = self.turn + 1
        else:
            self.text_label["text"] = "다른 곳을 선택해 주세요"
        self.judge()
        self.for_debug()

    def for_debug(self):
        print( "trun : ", self.turn )
        for i in range(3):
            print(self.cells[i*3],self.cells[i*3+1],self.cells[i*3+2])

    def start_game(self):
        self.window.mainloop()

    def end_game(self):
        self.window.destroy()       # 사용할 곳이 있을까?


game1 = tec_tac_toe()

game1.start_game()