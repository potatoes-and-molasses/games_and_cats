import random
import sys
OPTS = ['rock', 'paper', 'scissors']

def wins(name):
    if name == 'rock':
        return 'paper'
    elif name == 'paper':
        return 'scissors'
    else:
        return 'rock'
def random_alg():
    return random.choice(OPTS)



class basic_rpsb:


    history = []
    
    def __init__(self):
        
        self.history = []

    def playround(self, other, isfirst=0):
        a,b = self.alg(isfirst),other.alg(isfirst)
        self.history += [(a,b) ]
        other.history += [(b,a)]
        return (a,b)

    def alg(self, isfirst):
        return 'paper'


class copy(basic_rpsb):
    
    def alg(self, isfirst):
        if isfirst:
            return random_alg()
            
        else:
            return self.history[-1][1]
            
        

class repeat(basic_rpsb):
    current = 0

    def __init__(self):
        self.current = random.randint(0,2)
        self.history = []
        
    def alg(self, isfirst):
        self.current = (self.current + 1) % 3
        return OPTS[self.current]

class rand(basic_rpsb):
    def alg(self, isfirst):
        return random_alg()

class wincopy(basic_rpsb):
    
    def alg(self, isfirst):
        if isfirst:
            return random_alg()
            
        elif self.history[-1][1] == 'rock':
            return 'paper'
        elif self.history[-1][1] == 'scissors':
            return 'rock'
        else:
            return 'scissors'
class human(basic_rpsb):
    def alg(self, isfirst):
        choice = 0
        while choice not in ['r', 'rock', 'p', 'paper', 's', 'scissors']:
            choice = raw_input('[r]ock, [p]aper, or [s]cissors?')
        if choice.lower() in ['r', 'rock']:
            return 'rock'
        elif choice.lower() in ['p', 'paper']:
            return 'paper'
        elif choice.lower() in ['s', 'scissors']:
            return 'scissors'

class foolish(basic_rpsb):

    pcount=0
    rcount=0
    scount=0
    total=0
    def __init__(self):
        self.history = []
        self.pcount=0
        self.rcount=0
        self.scount=0
        self.total=0
    
    def alg(self, isfirst):
        if isfirst:
            return random_alg()
        if self.history[-1][1] == 'rock':
            self.rcount += 1
            self.total += 1
        elif self.history[-1][1] == 'paper':
            self.pcount += 1
            self.total += 1
        else:
            self.scount += 1
            self.total += 1
            
        if random.randint(1,100) < 20 or self.total < 10:
            return random_alg()

        else:
            x = random.randint(0, self.total)
            if x<self.pcount:
                return (wins('paper'))
            elif x<self.pcount+self.rcount:
                return (wins('rock'))
            else:
                return (wins('scissors'))


class mfoolish(foolish):
    def alg(self, isfirst):
        return wins(foolish.alg(self, isfirst))
        
class tmfoolish(foolish):
    def alg(self, isfirst):
        if isfirst:
            return random_alg()
        if len(self.history)>10:
            if self.history[0][1] == 'rock':
                self.rcount -= 1
                self.total -= 1
            elif self.history[0][1] == 'paper':
                self.pcount -= 1
                self.total -= 1
            else:
                self.scount -= 1
                self.total -= 1
            self.history = self.history[1:]
            return foolish.alg(self, isfirst)
    
class selfpattern(basic_rpsb):

    def alg(self, isfirst):
        t = 6
        if len(self.history)<3*t:
            return random_alg()
        else:

            opts = filter(lambda x: x, [self.pat(i) for i in range(1,t+1)])
            if opts:
                if random.randint(1,100)<25:
                    return random_alg()
                c = random.choice(opts)

                return wins(c)

            else:
                return random_alg()
        
    def pat(self, length):

        for i in range(0, length):
            p1 = map(lambda x: x[1] , self.history[-length-i:-i])
            
            p2 = map(lambda x: x[1] , self.history[-2*length-i:-length-i])
            p3 = map(lambda x: x[1] , self.history[-3*length-i:-2*length-i])
            #print i, p1, p2, p3
            if p1 == p2 ==p3 and len(p1[i])>0:
                return p1[i]
        for i in range(0, length):
            p1 = self.history[-length-i:-i]
            p2 = self.history[-2*length-i:-length-i]

            if p1 == p2:
                return p1[i]
        return None
        

def winchain(selfpattern):

    winchain = 0
    def __init__(self):
        self.winchain = 0
        selfpattern.__init__()
    def alg(self, isfirst):
        pass #to be continued

    
def string_to_alg(name):

    if name == 'basic':
        return basic_rpsb()
    elif name == 'foolish':
        return foolish()
    elif name == 'copy':
        return copy()
    elif name == 'repeat':
        return repeat()
    elif name == 'rand':
        return rand()
    elif name == 'wincopy':
        return wincopy()
    elif name == 'human':
        return human()
    elif name == 'mfoolish':
        return mfoolish()
    elif name == 'tmfoolish':
        return mfoolish()
    elif name == 'selfpattern':
        return selfpattern()
    elif name == 'winchain':
        return selfpattern()
    else:
        print 'oh noes'

def round_score(round_tuple):
    a, b = round_tuple[0], round_tuple[1]
    if a == 'rock':
        if b == 'paper':
            return 0,1
        elif b == 'scissors':
            return 1,0
        else:
            return 0,0
    elif a == 'paper':
        if b == 'rock':
            return 1,0
        elif b == 'paper':
            return 0,0
        else:
            return 0,1
    else:
        if b == 'rock':
            return 0,1
        elif b == 'paper':
            return 1,0
        else:
            return 0,0
def main():
    silent = 0
    
    if len(sys.argv)>1:
        p1, p2 = sys.argv[1], sys.argv[2]
    else:
        print '''availble algorithms:
basic
copy
rand
wincopy
repeat
human
foolish
mfoolish
tmfoolish
selfpattern
winchain
(see source code!)
'''
        p1=raw_input('player1: choose alg')
        p2=raw_input('player2: choose alg')
    

    p1 = string_to_alg(p1)
    p2 = string_to_alg(p2)

    if len(sys.argv)>3:
        rounds = sys.argv[3]
    else:
        rounds = input('number of rounds: ')
    score1, score2 = 0, 0
    first = 1
    for i in range(rounds):
        if silent == False:
            print '''
##################\t\t\tROUND {}\t\t\t##################
'''.format(i+1)
        result = p1.playround(p2, first)
        score = round_score(result)
        score1 += score[0]
        score2 += score[1]
        if silent == False:
            print 'Player1: {}!\nPlayer2: {}!'.format(result[0], result[1])
            if score[0] == 1:
                print 'You win this round.'
            elif score[1] == 1:
                print 'You lose this round.'
            else:
                print 'Tie.'
        
        
            print score1, score2
        first = 0
    print score1, score2
if __name__=='__main__':
    main()
