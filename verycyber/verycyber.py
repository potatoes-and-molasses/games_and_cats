import sys
import os
import time

class being:
    #stuff
    pass
class cyberclass(being):

    bla=0



class link:

    connected = []
    choices = []
    name=''
    message=''
    isover=False
    
    def __init__(self, name, message='You enter a room... \n\n No message set! Dem lousy developerz!'):
        self.name=name
        self.connected=[]
        self.message=message
        self.choices=[]
        self.isover=False

    def connect(self, other):
        self.connected+=[other]

    def connect2(self, other):
        self.connected+=[other]
        other.connected+=[self]

    def connectall(self, lst):
        for i in lst:
            self.connect(i)
    def connectall2(self, lst):
        for i in lst:
            self.connect(i)
            i.connect(self)
            

    def __repr__(self):
        c=0
        st='You are in {}\n{}\nWhat would you like to do?\n'.format(self.name, self.message)
        for i in filter(lambda x: not x.isover, self.connected):
            c+=1
            st += '{}: Move to {}\n'.format(c, i.name)
        for i in filter(lambda x: not x.isover, self.choices):
            c+=1
            st += '{}: {}\n'.format(c, i.name)

        return st

    def add_choice(self, choice):
        self.choices += [choice]


class event:

    isover=False
    name=''
    def __init__(self, name):
        self.isover=False
        self.name=name

    def start(self):
        if self.isover:
            self.ended()
        else:
            pass #happens
    def ended(self):
        #relevant resolution stuff
        pass
    def __repr__(self):
        return self.name

class combatevent(event):
    enemies=[]
    name=''
    isover=False

    def __init__(self, name):
        self.enemies=[]
        self.name=name
        self.isover=False
    def adden(self, en):
        self.enemies+=[en]

    def start(self):
        if self.isover:
            self.ended()
        for i in self.enemies:
            i.fight(YOU)
        self.ended()

    def __repr__(self):
        return 'NOT IMPLEMENTED! HURR!'
        
class riddlecat(event):


    def start(self):
        wrong=False
        if self.isover:
            print 'Go find your dentist! or was it your destiny? can\'t recall... maybe they are the same... curious!'
        else:
            print 'Before forth you venture (weee!), you must answer questions three!'
            NAME=raw_input('What is your name?')
            QUEST=raw_input('What is your quest?')
            tmp=raw_input('What is your favorite colour?')
            if tmp.lower() != 'blue':
                wrong=True
            self.ended(wrong)
            
    def ended(self, wrong):

        if wrong:
            print 'Wow, Very wrong. Much incorrectness. So gameover.'
            lose()
        else:
            print 'Indeed! You completed the tutorial, wasn\'t it informational?\n'+'-_'*10+'-'
            firstroom.isover=False
            self.isover=True
class riddlecat2(event):
    def ended(self, wrong):
        if wrong:
            print 'Alas, mistakes were made! I\'ll spare your soul this time.'
        else:
            print 'Ten points to Gryffindor!'
            self.isover=True
            postcat2.isover=False

    def start(self):

        wrong=False
        ans=[]
        q1='I HAS A KITTEH ITZ 0\nIM IN YR BASKATT UPPIN YR KITTEH TIL BOTHSAEM KITTEH AN 6\n\tVISIBLE SMOOSH KITTEH AN KITTEH\nIM OUTTA YR BASKATT\nVISIBLE "HOW MENI DIGETS?"?'
        q2='abcdefghijklmnopqrstuwxyz'
        q3='how r u doin 2dayh?'
        q4='X-PLANE STRING THEEORY IN 2 WORDSES!'
        final=['14','v','','string theory']
        for i in [q1,q2,q3,q4]:
            tmp=raw_input(i)
            ans+=[tmp]
        ans[2]=''
        if [j.lower() for j in ans] != final:
            wrong=True
        else:
            wrong=False


        self.ended(wrong)
class puzzledoor(event):
    def start(self):
        pw = raw_input('Please enter password: ')
        if pw == '135240':
            self.isover=True
            print 'The door is now open.'
            b1.isover=False
        else:
            print 'The lock won\'t budge!'
        
class useless(event):
    patience=0
    isover=False
    name=''
    msg=0
    tre=None
    patmsg=''
    def __init__(self, name, msg, tre=None, patmsg=None):
        self.isover=False
        self.name=name
        self.msg=msg
        self.patience=0
        self.tre=tre
        self.patmsg=patmsg
    def start(self):
        self.patience+=1
        if self.tre:
            if self.patience > self.tre:
                print self.patmsg
                self.patience=0
            else:
                print self.msg
        else:        
            print self.msg
        
        
#add specific events


class enemy(being):
    pass

def lose():
    print 'That\'s it!'
    time.sleep(10)
    exit()
        
YOU=0
CURRENTPLACE=0
#test

a=link('a roomly room', 'This is a place. it lurks.')
aa=link('a great hallway', 'YOU SHALL NOT PASS!')
aa1=useless('Run, fools!', 'Indeed, it is a marvelous idea!')
aa.add_choice(aa1)
aa2=useless('#remember to give the player a false sense of choice','they say it enhances gameplay??')
a.add_choice(aa2)
b=link('THE ROOM', 'A notoriously gruesome room of yellow monkeys!')
aa.connect2(b)
c=link('a room', 'Ow what horrors await for those who delve unto this cybersome place!\nThere is a riddle cat in the room.')
d=link('some questionably ill-located place', 'This is the beginning, hi!')
firstroom=link('a sneaky room that was hidden until recently', 'A crossroad of yet to be implemented twisty paths! it\'s time for choices...')
firstroom.isover=True
lol=link('Reading the source code are we?', 'Shoulda compiled before letting you scum in!')
a1=link('a twisty path of narrowness', 'Are you 1ost?')
a2=link('a narrow twisting path', 'Follow th2 light!')
a3=link('eggplant fortress', 'Rook to c3.')
a4=link('a twisty narrow path', 'Hurry, 4 the end is near!.')
a5=link('a path of narrow twists', 'What are we mis5ing??')
a6=link('a narrow path of twists', 'Initiate emergency evacuation plan in order t0 retrieve some icecream.')
a7=link('a cool room', 'It has air conditioning.')
firstroom.connectall([a1,a2,a3,a4,a5, a6])
a1.connectall([a3,a5])
a2.connectall([a5,a4,a1])
a3.connectall([a6,a5])
a4.connectall([a1,a6, a4])
a5.connectall([a2, a3])
a6.connectall([a3, a7, a1, firstroom])
a71=useless('Chill', 'The air conditioner freezes your spine.', 3, 'the sneaky path from there to here, six days by numbers steer.')
a72=puzzledoor('Approach the locked door')
a7.add_choice(a71)
a7.add_choice(a72)
a7.connect(firstroom)
b1=link('AFTERWARDS','Open eyes, adjusting to the dark.\n The rattle of machinery, can\'t say if it\'s night or day.')
b2=link('where spaceships are kept', 'Sadly, the spaceships are nowhere to be found!')
b3=link('the way out', 'How easily can relativism fool those meek of heart!\n you\'re outside already, get us outta here would you?')
b4=link('the brink of the wild abyss', 'Guaranteed to be the best journey-pondering spot in a thousand miles radius.')
b21=useless('Look for spaceships around the corners of the room', 'You see no spaceships there.')
b22=useless('Scan the surroundings for spaceship remenants', 'The gigantic dinosaur is blocking your view', 8, 'BADUM!')
b23=useless('Check if the spaceship was inside you all along, waiting for the right moment to sprout and take you away', 'YE RIGHT LOL', 10, 'The force is strong with this one')
b24=useless('Fly the spaceship regardless of its lack of existence!', 'Your cyber-powers need some honing before you can operate this no-spaceship', 15, 'As the spaceship\'s engines ignite you hear a soft humm, then the ship rumbles comically sets for the horizon, you forgot to put a seatbelt on so you die. btw you win!!!(it\'s a matter of perspective, long live space race)')
b1.connectall([b2,b3,b4])
b2.add_choice(b21)
b2.add_choice(b22)
b2.add_choice(b23)
b2.add_choice(b24)
b33=riddlecat2('It\'s another riddle cat!')
b3.add_choice(b33)
b2.connect(b1)
b1.connect2(a7)
b4.connect(b1)
b3.connect(b1)
b41=useless('Ponder your journey', 'Paradise lost!')
b31=useless('Search for traps', 'Roll d20 and add your search skill modifier, were you born yesterday?', 10, 'The rabbit is preparing something bad.')
b1.isover=True
b3.add_choice(b31)
b4.add_choice(b41)

postcat2=link('some frozen god-forsaken place','This doesn\'t seem to be the way unless you wish to end your adventure as a block of ice.')
postcat2.isover=True
postcat2.connect2(b3)
postcat21=useless('Freeze to death', 'You recall the chill of air conditioners long lost and decide not to freeze after all.', 6, 'giefegg')
postcat22=link('a windswept valley', 'Stone pillars are spread across this valley. The cutting winds break the frozen  crust coating these pillars, revealing runes in a long forgotten language.')
postcat2.connect2(postcat22)
postcat2.add_choice(postcat21)

               
a.connect(b)
b.connect(c)
c.connect(d)
d.connect(a)
b.connect2(d)
c.connect2(firstroom)
b1.connect(d)

e=riddlecat('Converse with the riddle cat')
c.add_choice(e)
CURRENTPLACE=a

def gief(string):
    hax = {}
    hax['cool']=a7
    hax['after']=b1
    hax['cat']=c
    hax['sneaky']=firstroom
    hax['cyber']=lol
    hax['egg']=a3



    return hax[string]
while True:
    hax=False
    print CURRENTPLACE
    if isinstance(CURRENTPLACE, event):
        CURRENTPLACE.start()
        raw_input('Press any key to continue...')
        CURRENTPLACE = lastplace
    else:
        options = filter(lambda x: not x.isover, CURRENTPLACE.connected + CURRENTPLACE.choices)
        ch='a'
        while True:
            if ch[:4] == 'gief':
                CURRENTPLACE = gief(ch[4:])
                hax=True
                break
            if ch.isdigit():
                if int(ch) <=len(options):
                    break
                else:
                    os.system('cls')
                    print CURRENTPLACE
                    ch=raw_input('=====> . . . . ') 
            else:
                os.system('cls')
                print CURRENTPLACE
                ch=raw_input('=====> . . . . ')
        if hax:
            pass
        elif isinstance(CURRENTPLACE, link):
            lastplace, CURRENTPLACE = CURRENTPLACE,(options)[int(ch)-1]
        
    
        
    
