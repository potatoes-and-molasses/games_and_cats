import random
import sys
import threading
CA,CO,AS,AM,DU,IN,FA,COUP=0,1,2,3,4,5,6,7
deck = [CA,CO,AS,AM,DU]*3

def chooseindex(player):
    pass

def chooseplayer(player):
    pass

class Cool:
    
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.tokens = 2
        self.dieded = 0
        self.diededindex = -1
        self.draw()
        self.draw()

    def __repr__(self):
        return self.name

    def replace(self,index):
        global deck
        deck+=[self.cards.pop(index)]
        self.draw()
        if(self.diededindex > -1):
            random.shuffle(self.cards)
        
    def draw(self):
        random.shuffle(deck)
        self.cards+=[deck.pop()]
        
    def become_dieded(self,index):
        if self.diededindex > -1:
            self.dieded = 1
        else:
            self.diededindex = index

    def action(self,cmd):
        global deck
        cmds = {'coup':COUP,'income':IN,'in':IN,'foreignaid':FA,'fa':FA,'captain':CA,'ca':CA,'contessa':CO,'co':CO,'duke':DU,'du':DU,'ambassador':AM,'am':AM,'assasin':AS,'as':AS}

        if cmd not in cmds:
            print cmd
            return
        else:
            cmd=cmds[cmd]

        if cmd==IN:
            self.tokens+=1
            print '+1 tokens'
        elif cmd==FA:
            result = self.allowcounter(cmd)
            if result == 1:
                self.tokens+=2
                print '+2 tokens'
            else:
                print 'stopped by duke'
        elif cmd==COUP:
            if(self.tokens < 7):
                print 'not enough tokens for coup'
            else:
                self.tokens-=7
                target=chooseplayer(self)
                index=chooseindex(target)
                target.become_dieded(index)
                print 'coup! tar=%s' % self.name
        elif cmd==DU:
            result = self.allowcounter(cmd)
            if result == 1:
                self.tokens += 3
                print '+3 tokens'
            else:
                index = chooseindex(self)
                self.become_dieded(index)
                print 'lie!'
        elif cmd==CO:
            print 'no actions lol why does that exist?'
        elif cmd==CA:
            target=chooseplayer()
            result = self.allowcounter(cmd)
            if result==1:
                s=min(target.tokens,2)
                target.tokens-=s
                self.tokens+=s
                print 'stole %d from %s' % s,target.name
            elif result==-1: #counter by ambassador
                print 'counter by ambassador'
            elif result==-2: #counter by captain
                print 'counter by captain'
            else:
                index = chooseindex(self)
                self.become_dieded(index)
                print 'lie!'

        elif cmd==AS:
            if self.tokens<3:
                print 'not enough tokens for assasination'
            else:
                target=chooseplayer()
                result = self.allowcounter(cmd)
                if result == 1:
                    index=chooseindex(target)
                    target.become_dieded(index)
                    print 'coup! tar=%s' % self.name
                elif result == -1:
                    print 'counter by contessa'
                else:
                    index = chooseindex(self)
                    self.become_dieded(index)
                    print 'lie!'
        elif cmd==AM:
            result = self.allowcounter(cmd)
            if result==1:
                self.draw()
                self.draw()
                index1,index2=0,0
                while index1==index2 and 0<=index1<=3:
                    
                    index1=chooseindex(self)
                    index2=chooseindex(self)

                index1,index2=min(index1,index2),max(index1,index2)
                deck+=[self.cards.pop(index1)]
                deck+=[self.cards.pop(index2-1)]
                random.shuffle(deck)
                print 'changed cards'
            else:
                index = chooseindex(self)
                self.become_dieded(index)
                print 'lie!'

    def allowcounter(self,cmd):
        pass

            
                
            
                            
            
if(1-len(sys.argv)):
    players = sys.argv[1]
else:
    players = 2

plist = [Cool('player%d' % i) for i in range(players)]

