import random
from player import Player, KaijiClass

#foo and classes
def help(): print('Rules \n\n\
number of players: 3-12 (one of them is dealer) \n\
everyone starts with random cash (between 60k and 100k), you starts with 60k \n\
every player except of dealer make his bet (bet can be from 100 to 20k) \n\
then everybody rolls 3 dice, dealer rolls first \n\
then player\'s and dealer\'s combinations are compared according to the list below \n\
(every player is competing with dealer only) \n\
combinations (from the strongest to the weakest): \n\
  1+1+1 => player wins 5 times \n\
  for triple (2+2+2 to 6+6+6) => player wins 3 times (higher triple beat lower triple) \n\
  4+5+6 => player wins 2 times \n\
  for double [2+5+5 (means 2) or 4+1+1 (means 4)] => player wins 1 time \n\
   (higher double beat lower double) \n\
  1+2+3 => player pays twise \n\
if you throw nothing of above (nothing valuable) you still have 2 attempt \n\
after 3 unsuccessful rolls you loose your bet to dealer \n\
if dice jumps out you loose your bet immediately and can\'t reroll \n\
when everyone rolls, there will be another round \n\
player plays as dealer twise (with the exception of case he rolls 1 or nothing for first round) \n\
then the next player will be dealer and everything starts from the beginning \n\
dealer can\'t win immediately with 6 or 4+5+6 or triple, others will roll too \n\
likewise if dealer gets 1+2+3 it will be draw if another player rolls the same or his dice jumps out \n\
you can skip dealer turn (so could others do)\n')

r = lambda r1, r2: random.randint(r1,r2) #shorthanded randomize

class listOfPlayersClass: # O_O_O_O
    lop = {}
    dealer = 0
    roundCounter = 0
    numberOfPlayers = 0
    def addPlayer(self, player):
        self.lop [player.number] = player
        self.numberOfPlayers += 1
    def replace(self, player):
        self.lop [player.number] = player
    def delPlayer(self, number):
        del self.lop[number]
    def showPlayers(self, case):
        if not(case == 'inf' and self.dealer == Kaiji.number):
            for player in self.lop:
                print(self.lop[player].display(case))
    def searchNextDealer(self, dealer):
        nextDealer = dealer+1
        while not nextDealer in self.lop:
            if nextDealer >= numberOfPlayers:
                nextDealer = 1
            else:
                nextDealer += 1
        return nextDealer
    def setDealer(self): #ready
        if self.roundCounter == 0:
            self.dealer = r(1,self.numberOfPlayers)
            self.roundCounter = 1
        elif self.roundCounter == 1 and self.dealer in self.lop:
            self.roundCounter = 2
        else: #set new dealer
            nextDealer = self.searchNextDealer(self.dealer)
            if self.lop[nextDealer].name == 'Kaiji':
                ans = 't'
                while ans != 'y' and ans != 'n':
                    ans = input('enter \'y\' if you want to be dealer or \'n\' otherwise\n')
                if ans == 'y':
                    self.dealer = nextDealer
                elif ans == 'n':
                    self.dealer = self.searchNextDealer(nextDealer)
            else:
                self.dealer = nextDealer
            self.roundCounter = 1
        for player in self.lop:
            self.lop[player].isDealer = 0
        self.lop[self.dealer].isDealer = 1
    def betMaking(self):
        for player in self.lop:
            if self.lop[player].isDealer == 0:
                if self.lop[player].name != 'Kaiji':
                    self.lop[player].betMaking()
                else:
                    self.lop[player].betMaking(self.lop, self.dealer)
    def isTimeFor456 (self, playerNumber):
        betMore15 = 0
        selfBetMore15 = 0
        order =(self.lop[playerNumber].name == 'Isava')*\
               (self.lop[self.searchNextDealer(self.dealer)].name == 'Otsuki')\
               +\
               (self.lop[playerNumber].name == 'Otsuki')*\
               (self.lop[self.searchNextDealer(self.dealer)].name == 'Numakava')
        for player in self.lop:
            if player != self.dealer:
                if self.lop[player].bet >= 15000:
                    betMore15 = 1
                    if (self.lop[player].name == 'Isava'  and self.lop[self.searchNextDealer(self.player)] == 'Otsuki') or\
                       (self.lop[player].name == 'Otsuki' and self.lop[self.searchNextDealer(self.player)] == 'Numakava'):
                        selfBetMore15 = 1
        return order * betMore15 + selfBetMore15
               
    def roll(self):
        for player in self.lop:
            if self.isTimeFor456(player):
                self.lop[player].roll456()                
            else:
                self.lop[player].roll()
    def isBankrupt(self):
        bankruptNumbers = []
        for player in self.lop:
            self.lop[player].lastProfit = 0
            if self.lop[player].cash <= 0:
                if (self.lop[player].cash == 0) & (self.lop[player].name != 'Kaiji'):
                    print('\n' + self.lop[player].name + ' ends with nothing')
                elif (self.lop[player].cash < 0) & (self.lop[player].name != 'Kaiji'):
                    print('\n' + self.lop[player].name + ' heavily in debt, good luck for him')
                elif (self.lop[player].cash == 0) & (self.lop[player].name == 'Kaiji'):
                    print('\nthat\'s over Kaiji, you have no money')
                elif (self.lop[player].cash < 0) & (self.lop[player].name == 'Kaiji'):
                    print('\nyou\'re in debt Kaiji')
                bankruptNumbers = bankruptNumbers + [player]
        for n in bankruptNumbers:
            self.delPlayer(n)            
    def endOfGame(self):
        if Kaiji.cash <= 0:
            return 'f'
        elif len(self.lop) == 1:
            return 'w'
        else:
            return 'd'
    def competition (self) :
        for player in self.lop:
            self.lop[player].whatCombination()
            #print(self.lop[player].name, " dice ", self.lop[player].dice, "  comb = ", self.lop[player].combination)
        dRes = self.lop[self.dealer].combination
        for player in self.lop:
            if player != self.dealer:
                pRes = self.lop[player].combination
                bet = self.lop[player].bet
                #comparing and payment
                if dRes[0] > pRes[0]:
                    if dRes[0] == 1 and pRes[0] == -2:
                        self.lop[self.dealer].pay(bet*2)
                        self.lop[player].pay(-bet*2)
                    elif dRes[0] == -1 and pRes[0] == -2:
                        self.lop[self.dealer].pay(0)
                        self.lop[player].pay(0)
                    elif dRes[0] == 0 and pRes[0] == -1:
                        self.lop[self.dealer].pay(0)
                        self.lop[player].pay(0)                        
                    else:
                        self.lop[self.dealer].pay(bet*dRes[0])
                        self.lop[player].pay(-bet*dRes[0])
                elif dRes[0] < pRes[0]:
                    if pRes[0] == 1 and dRes[0] == -2:
                        self.lop[self.dealer].pay(-bet*2)
                        self.lop[player].pay(bet*2)
                    elif pRes[0] == -1 and dRes[0] == -2:
                        self.lop[self.dealer].pay(0)
                        self.lop[player].pay(0)
                    elif pRes[0] == 0 and dRes[0] == -1:
                        self.lop[self.dealer].pay(0)
                        self.lop[player].pay(0) 
                    else:
                        self.lop[self.dealer].pay(-bet*pRes[0])
                        self.lop[player].pay(bet*pRes[0])
                else:
                    if dRes[1] > pRes[1]:
                        self.lop[self.dealer].pay(bet*dRes[0])
                        self.lop[player].pay(-bet*dRes[0])
                    elif dRes[1] < pRes[1]:
                        self.lop[self.dealer].pay(-bet*dRes[0])
                        self.lop[player].pay(bet*dRes[0])
                    else:
                        self.lop[self.dealer].pay(0)
                        self.lop[player].pay(0)
                        
#initialisations
help()
nameList = ['Otsuki', 'Maeda', 'Miesi', 'Isida', 'Hanaka', 'Arikava', 'Hattori', 'Kitagava',\
            'Takahasi', 'Numakava', 'Isava', 'Takuya', 'Kenta', 'Yuya', 'Koutarou', 'Masaki']
random.shuffle(nameList)
numberOfPlayers = r(3,12)        
listOfPlayers = listOfPlayersClass()
for i in range(1,numberOfPlayers+1):
    listOfPlayers.addPlayer (Player(nameList[i-1], i, r(60,100) * 1000))
KaijiNumber = r(1,numberOfPlayers)
Kaiji = KaijiClass ('Kaiji', KaijiNumber, 60000)
listOfPlayers.replace(Kaiji)

handler = str(input ('Welcome Kaiji, you have 60000 perica, enter \'g\' if you want to play or \'e\' to leave,\n\
but remember that you NEVER could stop until you win or loose ALL money \n'))
result = 'd'

#game start
while (handler == 'g') and (result == 'd'):
    print('\nNew round!\n')
    listOfPlayers.setDealer()
    listOfPlayers.showPlayers('inf')
    listOfPlayers.betMaking()
    listOfPlayers.showPlayers('bet')
    listOfPlayers.roll()
    listOfPlayers.competition()
    listOfPlayers.showPlayers('profit')
    listOfPlayers.isBankrupt()
    result = listOfPlayers.endOfGame()
if result == 'w':
    print('You WIN')
elif result == 'f':
    print('Game over')
