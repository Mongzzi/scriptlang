from tkinter import *
from tkinter import font
from player import *
from dice import *
from configuration import *
from tkinter import messagebox

Roll_Dice_Flag = True

class YahtzeeBoard:
    # index들.
    UPPERTOTAL = 6  # "Upper Scores" 위치의 index.
    UPPERBONUS = 7  # "Upper Bonus(35)" 위치의 index.
    LOWERTOTAL = 15  # "Lower Scores" 위치의 index.
    TOTAL = 16  # "Total" 위치의 index.

    # 객체 리스트
    dice = []       # Dice() 객체의 리스트.
    diceButtons = [] # 각 주사위를 표현하는 Button 객체의 리스트.
    fields = []     # 각 플레이어별 점수판(카테고리). Button 객체의 2차원 리스트.
                    # 열: 플레이어 (0열=플레이어1, 1열=플레이어2,…)
                    # 17행: upper카테고리6행, upperScore, upperBonus, lower카테고리7행, LowerScore, Total
    players = []    # 플레이어 수 만큼의 Player 인스턴스를 가짐.
    numPlayers = 0  # # 플레이어 수
    player = 0      # players 리스트에서 현재 플레이어의 index.
    round = 0       # 13 라운드 중 몇번째인지 (0~12 사이의 값을 가짐)
    roll = 0        # 각 라운드에서 3번 중 몇번째 굴리기인지 (0~2 사이의 값을 가짐)
    # 색깔
    color_btn_bg = 'SystemButtonFace'

    def __init__(self):
        self.InitGame()

    def InitGame(self):     #player window 생성하고 최대 10명까지 플레이어 설정
        self.pwindow = Tk()
        self.TempFont = font.Font(size=12, weight='bold', family='Consolas')
        self.label = []
        self.entry = []
        self.label.append( Label(self.pwindow, text='플레이어 수', font=self.TempFont ) )
        self.label[0].grid(row=0, column=0)

        for i in range(1,11):
            self.label.append( Label(self.pwindow, text='플레이어'+str(i)+' 이름', font=self.TempFont))
            self.label[i].grid(row=i, column=0)
        for i in range(11):
            self.entry.append(Entry(self.pwindow, font=self.TempFont))
            self.entry[i].grid(row=i, column=1)
        Button(self.pwindow, text='Yahtzee 플레이어 설정 완료', font=self.TempFont, command=self.InitAllPlayers).grid(row=11, column=0)

        self.pwindow.mainloop()

    def InitAllPlayers(self):
        '''
        [플레이어 설정 완료 버튼 누르면 실행되는 함수]
        numPlayers를 결정하고 이 숫자에 따라 각 player에게 필요한 정보들을 초기화.
        기존 toplebel 윈도우를 닫고 Yahtzee 보드 윈도우 생성.
        '''
        self.numPlayers = int(self.entry[0].get())
        for i in range(1, self.numPlayers+1):
            self.players.append(Player(str(self.entry[i].get())))
        self.pwindow.destroy()

        ##################################################       
        # Yahtzee 보드판: 플레이어 수 만큼 생성
        
        self.window = Tk('Yahtzee Game')
        self.TempFont = font.Font(size=12, weight='bold', family='Consolas')

        for i in range(5): #Dice 객체 5개 생성
            self.dice.append(Dice())

        self.rollDice = Button(self.window, text='Roll Dice', font=self.TempFont, command=self.rollDiceListener, bg=self.color_btn_bg)  # Roll Dice 버튼
        self.rollDice.grid(row=0, column=0)
        for i in range(5):  #dice 버튼 5개 생성
	        #각각의 dice 버튼에 대한 이벤트 처리 diceListener 연결
            #람다 함수를 이용하여 diceListener 매개변수 설정하면 하나의 Listener로 해결
            self.diceButtons.append(Button(self.window, text='?', font=self.TempFont, width=8, bg=self.color_btn_bg, command=lambda row=i: self.diceListener(row))) 
            self.diceButtons[i].grid(row=i + 1, column=0)
        
        for i in range(self.TOTAL + 2):  # i행 : 점수
            Label(self.window, text=Configuration.configs[i], font=self.TempFont).grid(row=i, column=1)
            for j in range(self.numPlayers):  # j열 : 플레이어
                if (i == 0):  # 플레이어 이름 표시
                    Label(self.window, text=self.players[j].toString(), font=self.TempFont).grid(row=i, column=2 + j)
                else:
                    if (j==0): #각 행마다 한번씩 리스트 추가, 다중 플레이어 지원
                        self.fields.append(list())
                    #i-1행에 플레이어 개수 만큼 버튼 추가하고 이벤트 Listener 설정, 매개변수 설정
                    self.fields[i-1].append(Button(self.window, text="", font=self.TempFont, width=8,
                        command=lambda row=i-1: self.categoryListener(row)))
                    self.fields[i-1][j].grid(row=i,column=2 + j)
                    # 누를 필요없는 버튼은 disable 시킴
                    if (j != self.player or (i-1) == self.UPPERTOTAL or (i-1) == self.UPPERBONUS 
                        or (i-1) == self.LOWERTOTAL or (i-1) == self.TOTAL):
                        self.fields[i-1][j]['state'] = 'disabled'
                        self.fields[i-1][j]['bg'] = 'light gray'
        
        #상태 메시지 출력
        self.bottomLabel=Label(self.window, text='R '+str(self.round+1)+' '+self.players[self.player].toString()+
            "차례: Roll Dice 버튼을 누르세요", width=35, font=self.TempFont)
        self.bottomLabel.grid(row=self.TOTAL + 2, column=0, columnspan=2)
        self.window.mainloop()

    def updateCurplayerScoreboard(self, flag = False):
        cur_player = self.players[self.player]

        if flag:
            for i in range(0, 5+1):
                if not cur_player.getAtUsed(i):
                    self.fields[i][self.player]['text'] = ''
            for i in range(8, 14+1):
                if not cur_player.getAtUsed(i-2):
                    self.fields[i][self.player]['text'] = ''
            return

        for i in range(0, 5+1):
            score = Configuration.score(i, self.dice)
            if not cur_player.getAtUsed(i):
                if score == 0:
                    self.fields[i][self.player]['text'] = ''
                else:
                    self.fields[i][self.player]['text'] = score

        for i in range(8, 14+1):
            score = Configuration.score(i, self.dice)
            if not cur_player.getAtUsed(i-2):
                if score == 0:
                    self.fields[i][self.player]['text'] = ''
                else:
                    self.fields[i][self.player]['text'] = score

    def replay(self):
        # 라운드 초기화
            self.round = 0
            self.roll = 0
            self.player = 0
            
            # 플레이어 초기화
            for player in self.players:
                player.reset()
            
            # 보드 초기화
            for j in range(self.numPlayers):
                for i in range(0,self.TOTAL+1):
                    self.fields[i][j]['text'] = ''
                    self.fields[i][j]['state'] = 'normal'
                    self.fields[i][j]['bg'] = self.color_btn_bg

            # 누를 필요없는 버튼은 disable 시킴
                    if (j != self.player or i == self.UPPERTOTAL or i == self.UPPERBONUS 
                        or i == self.LOWERTOTAL or i == self.TOTAL):
                        self.fields[i][j]['state'] = 'disabled'
                        self.fields[i][j]['bg'] = 'light gray'

            self.rollDice['text'] = 'Roll Dice'
            self.popup.destroy()

    def goTitle(self):
        self.popup.destroy()
        self.window.destroy()
        
        self.dice = [] 
        self.diceButtons = [] 
        self.fields = []     
                        
        self.players = [] 
        self.numPlayers = 0  
        self.player = 0     
        self.round = 0      
        self.roll = 0


        self.InitGame()


    # 게임 종료
    def is_over(self):
        # 일단 전부 다 회색으로 전환
        for j in range(self.numPlayers):
            for i in range(0,self.TOTAL+1):
                self.fields[i][j]['bg'] = 'light gray'
        # 토탈을 비교해서 더 큰 쪽을 파란색으로 만든다. 공동 우승도 가능
        totals = []
        for j in range(self.numPlayers):
            totals.append(self.players[j].getTotalScore())
        most = max(totals)
        winnerText = '승자는'
        for j in range(self.numPlayers):
            if most == self.players[j].getTotalScore():
                self.fields[self.TOTAL][j]['bg'] = 'blue'
                winnerText += ' "'+self.players[j].toString()+'" '
        winnerText += '입니다.'
        
        self.bottomLabel['text'] = "게임 끝"
        self.rollDice['text'] = '게임 끝'
        
        # 팝업 알림
        self.popup = Toplevel(self.window)
        self.popup.geometry("300x150")
        self.popup.title("알림")

        self.popupLable = Label(self.popup,font=self.TempFont,text=winnerText)
        self.popupLable.pack(expand=True)

        self.replayButton = Button(self.popup, text="다시하기", command=self.replay)
        self.replayButton.pack(anchor="s", padx=10, pady=10)

        self.titleButton = Button(self.popup, text="타이틀로", command=self.goTitle)
        self.titleButton.pack(anchor="s", padx=10, pady=10)

    # 주사위 굴리기 함수.
    def rollDiceListener(self):
        # 'state' 값이 'disabled'가 아닌 모든 주사위 값을 새로 할당하고 화면에 표시.
        if Roll_Dice_Flag:
            for i in range(5):
                if self.diceButtons[i]['bg'] != 'light gray':
                    self.dice[i].rollDie()
                if self.roll==2:
                    self.diceButtons[i]['state'] = 'disabled'
                    self.diceButtons[i]['bg'] = 'light gray'
        else:
            for i in range(5):
                if self.diceButtons[i]['state'] != 'disabled':
                    self.dice[i].rollDie()
                if self.roll==2:
                    self.diceListener(i)
        for i in range(5):
            self.diceButtons[i]['text'] = str(self.dice[i].getRoll())
            

        # 주사위를 굴리면 컴퓨터가 점수를 계산해줌.
        self.updateCurplayerScoreboard()

        # self.roll 이 0, 1 일 때 : 
        if (self.roll == 0 or self.roll ==1):
            self.roll += 1
            self.rollDice.configure(text="Roll Again("+str(3-self.roll)+')')
            self.bottomLabel.configure(text='R '+str(self.round+1)+' '+"보관할 주사위 선택 후 Roll Again")
        elif (self.roll==2):
            self.rollDice.configure(text="Can't Roll")
            self.bottomLabel.configure(text='R '+str(self.round+1)+' '+"카테고리를 선택하세요")
            self.rollDice['state'] = 'disabled'
            self.rollDice['bg'] = 'light gray'
            self.roll += 1
                
    # 각 주사위에 해당되는 버튼 클릭 : disable 시키고 배경색을 어둡게 바꿔 표현해 주기.
    def diceListener(self, row):
        # 주사위를 굴렸을때만 선택 가능
        # if self.roll == 0:
            # return
        if 1<=self.roll<=2:
            if Roll_Dice_Flag:
                if self.diceButtons[row]['bg'] == 'light gray':
                    self.diceButtons[row]['bg'] = self.color_btn_bg
                else:
                    self.diceButtons[row]['bg'] = 'light gray'
            else:
                self.diceButtons[row]['state'] = 'disabled'
                self.diceButtons[row]['bg'] = 'light gray'

    # 카레고리 버튼 눌렀을 때의 처리.
    #   row: 0~5, 8~14
    def categoryListener(self, row):
        # self.is_over() # 테스트용
        # 주사위를 굴렸을때만 선택 가능
        if self.roll == 0:
            return

        score = Configuration.score(row, self.dice)      #점수 계산
        # index : 0~12
        index = row
        if (row>7):
            index = row-2
        cur_player = self.players[self.player]

        # (1) cur_player에 setScore(), setAtUsed() 호출하여 점수와 사용상태 반영.
        cur_player.setScore(score, index)
        cur_player.setAtUsed(index)
        # (2) 선택한 카테고리의 점수를 버튼에 적고 -> 이 부분은 주사위 굴릴때 한다. 0은 예외
        if score == 0:
            self.fields[row][self.player]['text'] = score
        # (3) 버튼을 disable 시킴.
        self.fields[row][self.player]['state'] = 'disabled'
        self.fields[row][self.player]['bg'] = 'light gray'
        
        # UPPER category가 전부 사용되었으면(cur_player.allUpperUsed()로써 확인)
        # -> cur_player.getUpperScore() 점수에 따라
        #    UI의 UPPERTOTAL(6), UPPERBONUS(7) 에 내용 채우기.
        self.fields[self.UPPERTOTAL][self.player]['text'] = str(cur_player.getUpperScore())
        if cur_player.getUpperScore() >= 63:
            self.fields[self.UPPERBONUS][self.player]['text'] = '35'
        else:
            self.fields[self.UPPERBONUS][self.player]['text'] = '0'
        if cur_player.allUpperUsed():
            self.fields[self.UPPERTOTAL][self.player]['bg'] = 'blue'
            if cur_player.getUpperScore() >= 63:
                self.fields[self.UPPERBONUS][self.player]['bg'] = 'blue'
            else:
                self.fields[self.UPPERBONUS][self.player]['bg'] = 'red'

        # LOWER category 전부 사용되었으면(cur_player.allLowerUsed()로써 확인) 
        # -> cur_player.getLowerScore() 점수에 따라
        #   UI의 LOWERTOTAL(15) 에 내용 채우기.
        self.fields[self.LOWERTOTAL][self.player]['text'] = str(cur_player.getLowerScore())
        if cur_player.allLowerUsed():
            self.fields[self.LOWERTOTAL][self.player]['bg'] = 'blue'
            
        # UPPER category와 LOWER category가 전부 사용되었으면 
        # -> UI의 TOTAL(16) 에 내용 채우기.
        self.fields[self.TOTAL][self.player]['text'] = str(cur_player.getTotalScore())
        if cur_player.allLowerUsed() and self.players[self.player].allUpperUsed():
            self.fields[self.TOTAL][self.player]['bg'] = 'blue'

        # 보드판 정보 초기화
        self.updateCurplayerScoreboard(True)


        # 다음 플레이어로 가기.
        self.player = (self.player + 1) % self.numPlayers
        cur_player = self.players[self.player]

        # 선택할 수 없는 카테고리들과 현재 player 것이 아닌 버튼들은 disable 시키기.
        for j in range(self.numPlayers):
            # row: 0~5, 8~14
            
            if j != self.player:
                for i in range(0, 5+1):
                    self.fields[i][j]['state'] = 'disable'
                    self.fields[i][j]['bg'] = 'light gray'
                for i in range(8, 14+1):
                    self.fields[i][j]['state'] = 'disable'
                    self.fields[i][j]['bg'] = 'light gray'
        # 그 외는 enable 시키기. ? normal
            
        for i in range(0, 5+1):
            if not cur_player.getAtUsed(i):
                self.fields[i][self.player]['state'] = 'normal'
                self.fields[i][self.player]['bg'] = self.color_btn_bg
        for i in range(8, 14+1):
            if not cur_player.getAtUsed(i-2):
                self.fields[i][self.player]['state'] = 'normal'
                self.fields[i][self.player]['bg'] = self.color_btn_bg

        # 라운드 증가 시키기.
        if self.player == 0:
            self.round += 1

        # 다시 Roll Dice 버튼과 diceButtons 버튼들을 활성화. 주사위 값은 0 인걸로 계산
        self.rollDice.configure(text="Roll Dice")
        self.rollDice['state'] = 'normal'
        self.rollDice['bg'] = self.color_btn_bg
        self.roll = 0
        for i in range(5):  #dice 버튼 5개 생성
            self.diceButtons[i].configure(text='')
            self.diceButtons[i]['state'] = 'normal'
            self.diceButtons[i]['bg'] = self.color_btn_bg
            self.diceButtons[i]['text'] = '?'

        # bottomLabel 초기화.
        self.bottomLabel.configure(text='R '+str(self.round+1)+' '+cur_player.toString()+
            "차례: Roll Dice 버튼을 누르세요")
        
        # 게임이 종료되었는지 검사 (13 == self.round이면 종료된것임.) 
        # -> 이긴 사람을 알리고 새 게임 시작.
        if self.round == 13:
            self.is_over()
            return

if __name__ == '__main__':
    YahtzeeBoard()
