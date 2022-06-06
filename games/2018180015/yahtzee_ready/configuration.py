from dice import *

Full_House_Flag = True

class Configuration:

    configs = [
        "Categoty", "Ones", "Twos", "threes", "Fours", "Fives", "Sixes",
        "Upper Scores", "Upper Bonus(35)",
        "3 of a kind", "4 of a kind", "Full House(25)",
        "Small Straight(30)", "Large Straight(40)", "Yahtzee(50)", "Chance",
        "Lower Scores", "Total"
    ]

    @staticmethod
    def getConfigs():       # 정적 메소드 (객체 없이 사용 가능)
        return Configuration.configs

    # row에 따라 주사위 점수를 계산하여 반환. 
    # 예를 들어, row가 0이면 "Ones"가, 2이면 "Threes"가 채점되어야 함을 의미. 
    # row가 득점위치가 아닌 곳(즉, UpperScore, UpperBonus, LowerScore, Total 등)을 나타내는 경우 -1을 반환.
    @staticmethod
    def score(row, dices):       # 정적 메소드 (객체 없이 사용 가능)
        # 반환할 점수
        return_score = 0

        # 연속된 주사위 개수
        combo = 0
        max_combo = 0

        # 각 주사위 개수 세기
        number_of_each_dice = [0,0,0,0,0,0]
        for dice in dices:
            number_of_each_dice[dice.getRoll() - 1] += 1

        # 연속 개수 세기
        for i in number_of_each_dice:
            if i != 0:
                combo += 1
                if max_combo < combo:
                    max_combo = combo
            elif i == 0:
                combo = 0

        # 0 ~ 5
        if 0 <= row <= 5 :
            return_score = number_of_each_dice[row]*(row+1)

        # 8 ~ 14
        if row == 8:
            for i in range(3, 6):
                if i in number_of_each_dice:
                    for dice in dices:
                        return_score += dice.getRoll()
        if row == 9:
            for i in range(4, 6):
                if i in number_of_each_dice:
                    for dice in dices:
                        return_score += dice.getRoll()
        if row == 10:
            if 3 in number_of_each_dice and 2 in number_of_each_dice:
                return_score = 25
            if Full_House_Flag and 5 in number_of_each_dice:
                return_score = 25
        # 스스
        if row == 11:
            if max_combo >= 4:
                return_score = 30
        # 라스
        if row == 12:
            if max_combo >= 5:
                return_score = 40
        # 얏지
        if row == 13:
            if 5 in number_of_each_dice:
                return_score = 50
        # 초이스
        if row == 14:
            for dice in dices:
                return_score += dice.getRoll()

        print('number_of_each_dice : ', number_of_each_dice)
        print('max_combo : ', max_combo)
        print('return_score : '+str(return_score))
        return return_score

