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

        self.label_list = [Button(self.cells_frame, image = tec_tac_toe.empty, ) for i in range(9)]
        self.label_list[0]["command"] = lambda: self.pressed(0)
        self.label_list[1]["command"] = lambda: self.pressed(1)
        self.label_list[2]["command"] = lambda: self.pressed(2)
        self.label_list[3]["command"] = lambda: self.pressed(3)
        self.label_list[4]["command"] = lambda: self.pressed(4)
        self.label_list[5]["command"] = lambda: self.pressed(5)
        self.label_list[6]["command"] = lambda: self.pressed(6)
        self.label_list[7]["command"] = lambda: self.pressed(7)
        self.label_list[8]["command"] = lambda: self.pressed(8)

        for i, l in enumerate(self.label_list):
            l.grid(row=i//3, column=i%3, sticky = 'n' )

        self.label_1 = Label(self.window, text='O 차례')
        self.label_1.grid(row = 1, column = 0)

    def disable_all(self):
        for i in range(9):
            self.label_list[i]["state"] = DISABLED

    def finish(self):
        self.label_1["text"] = self.end_text_front + self.end_text_behind
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
        if self.turn == 8:
            self.finish()
        for i in range(3):
            if self.cells[i*3] == self.cells[i*3+1] == self.cells[i*3+2]:
                if self.cells[i*3] == 'o':
                    self.O_win()
                elif self.cells[i*3] == 'x':
                    self.X_win()
                break
            if self.cells[i] == self.cells[i+3] == self.cells[i+6]:
                if self.cells[i] == 'o':
                    self.O_win()
                elif self.cells[i] == 'x':
                    self.X_win()
                break
        if self.cells[0] == self.cells[4] == self.cells[8] or self.cells[2] == self.cells[4] == self.cells[6]:
            if self.cells[4] == 'o':
                self.O_win()
            elif self.cells[4] == 'x':
                self.X_win()

    def pressed(self, i):
        if self.turn % 2 == 1:
            self.label_list[i]["image"] = tec_tac_toe.i_X
            self.label_list[i]["state"] = DISABLED
            self.cells[i] = 'x'
            self.label_1["text"] = "O 차례"
        elif self.turn % 2 == 0:
            self.label_list[i]["image"] = tec_tac_toe.i_O
            self.label_list[i]["state"] = DISABLED
            self.cells[i] = 'o'
            self.label_1["text"] = "X 차례"

        self.judge()
        self.turn = self.turn + 1


game1 = tec_tac_toe()

game1.window.mainloop()