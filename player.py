import random
r = lambda r1, r2: random.randint(r1,r2) #shorthanded randomize
class Player:
    name = ''
    number = 0
    cash = 0
    dice = [2,4,6]
    bet = 0
    isDealer = 0
    lastProfit = 0
    combination = (0,0) #meaning for rolled dice
    def __init__ (self, name, number, startCash):
        self.name = name
        self.number = number
        self.cash = startCash
    def display (self, case):
        if self.number//10 == 0:
            isDecimal = 1
        elif self.number//10 == 1:
            isDecimal = 0
        if self.isDealer == 1:
            dd = 1; pp = 0
        else:
            dd = 0; pp = 1
        if case == 'inf':
            return ('no.' + ' '*isDecimal + str(self.number) + ' ' + self.name + \
                    '\t cash:' + str(self.cash) + ' perica' + '\tDealer'*dd)
        if case == 'bet':
            return ('no.' + ' '*isDecimal + str(self.number) + ' ' + self.name + \
                    '\t cash:' + str(self.cash) + ' perica\t' + 'Dealer'*dd + 'bet: '*pp + str(self.bet)*pp)
        if case == 'profit':
            s = ('no.' + ' '*isDecimal + str(self.number) + ' ' + self.name + \
                 '\t cash:' + str(self.cash - self.lastProfit) + ' perica,\t roll ' + str(self.dice) + \
                 ' profit '+ str(self.lastProfit) + '   Dealer'*dd)
            self.lastProfit = 0
            return s
    def betMaking (self):
        self.bet = self.cash + 1
        while self.bet > self.cash:
            if not self.isDealer:
                self.bet = 1000*(r(1,100)<40) * (1+r(0,4)*(r(1,100)<30)) + 10000*(r(1,100)<7) * (1+r(0,2)*(r(1,100)<7))
                if self.bet == 0:
                    self.bet = 100*r(1,9)
                elif self.bet > 20000:
                    self.bet = 20000
    def singleRoll(self):
        for i in range(0,3):
            self.dice[i] = r(1,6)
            if r(0,100) < 3:
                self.dice[0] = 0
    def nothing (self): #returns true if there is no combination on dice or false otherwise
        return not ((self.dice[0]==self.dice[1]) or\
                    (self.dice[1]==self.dice[2]) or\
                    (self.dice[0]==1 and self.dice[1]==2 and self.dice[2]==3) or\
                    (self.dice[0]==4 and self.dice[1]==5 and self.dice[2]==6))
    def roll (self):
        self.dice = [2,4,6]
        tryNo = 1
        while self.nothing() and tryNo <=3:
            self.singleRoll()
            tryNo+=1
            self.dice.sort()
    def singleRoll456(self):
        for i in range(0,3):
            self.dice[i] = r(4,6)
            if r(0,100) < 2:
                self.dice[0] = 0
    def roll456 (self):
        self.dice = [2,4,6]
        tryNo = 1
        while self.nothing() and tryNo <=3:
            self.singleRoll456()
            tryNo+=1
            self.dice.sort()
    def whatCombination(self): #returns (x,y) where x means x*bet to be taken, y means "playing" score for double/triple
        d = self.dice
        if d[0] == 0: self.combination = (-1,0)
        elif d[0] == 1 and d[1] == 2 and d[2] == 3: self.combination = (-2,0)
        elif d[0] == 4 and d[1] == 5 and d[2] == 6: self.combination = (2,0)
        elif d[0] == 1 and d[1] == 1 and d[2] == 1: self.combination = (5,0)
        elif d[0] == d[1] and d[1] != d[2]: self.combination = (1,d[2])
        elif d[0] != d[1] and d[1] == d[2]: self.combination = (1,d[0])
        elif d[0] == d[1] and d[1] == d[2]: self.combination = (3,d[1])
        else: self.combination = (0,0)
    def pay (self, gain):
        self.lastProfit += gain
        self.cash += gain

class KaijiClass (Player): #for Kaiji overrided roll and bet making functions
    def roll(self):
        self.dice = [2,4,6]
        tryNo = 1
        a = input ('\nyour roll Kaiji! press enter\n')
        while self.nothing() and tryNo <=3:
            if tryNo == 2:
                a = input('\nsecond try')
            elif tryNo == 3:
                a = input('\nlast try!')
            self.singleRoll()
            print(self.dice)
            tryNo+=1
            self.dice.sort()
            if self.dice[0] == 0:
                print('jump out')
                break
    def betMaking(self, listOfPlayers, dealer):
        print(' ')
        self.bet = 0
        betT = 'a'
        while (self.bet <100) or (self.bet%100 !=0) or ((self.bet > 20000) and (listOfPlayers[dealer].name != 'Otsuki')) or self.bet > self.cash:
            if (self.bet > 20000) & (listOfPlayers[dealer].name != 'Otsuki'):
                print('you can bet no more than 20k')
            betT = input('it\'s time to bet Kaiji\n')
            try: self.bet = int(betT)
            except: print('bet must be integer')
