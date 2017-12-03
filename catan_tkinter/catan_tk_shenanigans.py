import time
import math
import pprint
import random
import string
import Tkinter
import numbers    
 
#how to gui?!?!?!?!

cdr = lambda a: a[1:]
car = lambda a: a[0]
INTERSECTIONS = []

ct = {'clay': 'brown', 'wood': 'darkgreen', 'sheep': 'lightgreen', 'stone': 'grey', 'grain': 'yellow', 'desert': 'blue'}
AVAILBLETERRAINS = [ct['sheep']]*4+[ct['clay']]*3+[ct['grain']]*4+[ct['stone']]*3+[ct['wood']]*4+[ct['desert']]
random.shuffle(AVAILBLETERRAINS)
painter = iter(AVAILBLETERRAINS)
def flatten(a):
    try:
        if not len(a):
            return []
    except:
        return [a]
    else:
        return flatten(car(a))+flatten(cdr(a))
        

class Base:
    mandatory_arguements = set()
    class BaseClassException(Exception):
        pass
        
    def __init__(self, **kwargs):
        mandatory_arguements = self.__class__.mandatory_arguements
        
        if not mandatory_arguements.issubset(kwargs):
            raise Base.BaseClassException(
                self.__class__.__name__ + ' requires args: ' + str(mandatory_arguements))
        self.kwargs = kwargs
        for arg in kwargs:

            setattr(self, arg, kwargs[arg])

    def __repr__(self):
        return self.__class__.__name__ + '(**'+pprint.pformat(self.kwargs)+')'


class Ngon(Base):
    #a=Ngon(n=3, center=(0,0), radius=1, rotation=0)
    mandatory_arguements = set('n center radius rotation'.split())
    def __init__(self, **args):
        self.coordinates = False
        
        Base.__init__(self,**args)
        

    def __call__(self):
        if not self.coordinates:
            xi = self.rotation
            step = 2*math.pi/self.n
            self.coordinates = []
            (x0,y0) = self.center
            r = self.radius
            for i in range(self.n):
                self.coordinates.append((r*math.cos(xi)+x0, r*math.sin(xi)+y0))
                xi+=step
        return self.coordinates

    @property
    def flat(self):
        return flatten(self())

    @property
    def inner_radius(self):
        return self.radius*math.sqrt(1**2-(1/2)**2)
    

class Terrain(Ngon):
    #a=Terrain(center=(0,0), radius=1, rotation=0)
    mandatory_arguements = set('center radius rotation color'.split())
    
    def __init__(self, **args):
        
        args['n'] = 6
        
        Ngon.__init__(self, **args)

class Vector(Base):
    mandatory_arguements = set('P')
    def __len__(self):
        return len(self.P)
    def __getitem__(self, index):
        return self.P[index]
    def __add__(a,b):
        if a.__class__ != b.__class__:
            raise Exception('y u no add vectahrz?')
        if len(a) != len(b):
            raise Exception('incoherent dim')
        return Vector(P=tuple(a[i] + b[i] for i in range(len(a))))
    def __neg__(self):
        return self*(-1)
    def __sub__(a,b):
        return a+(-b)
    def __mul__(a,b):
        if not isinstance(b, numbers.Number):
            raise Exception('supports only multiply by scalar')
        return Vector(P=tuple(p*b for p in a))
    def dot(a,b=None):
        b = b or a
        try:
            if (len(a) == len(b)) and isinstance(b[0], numbers.Number):
                return sum(A*B for (A,B) in zip(a,b))
        except:
            pass
        raise Exception('Incoherent dim/type')

class SuperCanvas(Tkinter.Canvas):

    def create_loop(self, *args, **kwargs):
        global INTERSECTIONS
        loop = tuple(args) + (args[0],args[1])
        self.create_line(*loop, **kwargs)
        INTERSECTIONS += [args]



class pscales:

    def __init__(self, playert, master):
        self.scales = {}
        if playert:
            for i in ['sheep','stone','wood','grain','clay']:
                self.scales[i] = Tkinter.Scale(master, from_=playert[i], to=0, background=ct[i], troughcolor=ct[i], relief='ridge')
        else:
            for i in ['sheep','stone','wood','grain','clay']:
                self.scales[i] = Tkinter.Scale(master, from_=5, to=0, background=ct[i], troughcolor=ct[i], relief='ridge')


class Settlers:

    def __init__(self,s,intersections,players,radius=65,rotation=0.53, ):
        self.cards = 14*['knight'] + 5*['vp'] + 2*['monopole'] + 2*['roads'] + 2*['plenty']
        random.shuffle(self.cards)
        Game.HC=self
        self.freemode = True
        self.freecount = 0
        self.freeprogress = 2
        self.robberpos = 0
        self.BANDITCOORDS=None
        self.comb(radius,rotation)
        self.players=players
        self.currentplayer=0
        self.tempinter = None
        self.playNow = self.turn_iter()
        self.currentplayerobj = self.playNow.next()
        self.boardclickable = False
        tk=Tkinter.Tk()
        tk.geometry('1440x900')
        self.SELECTED = [False]*len(self.HEXAGONS)
        self.SELECTIONS = []
        canvas = SuperCanvas(tk)
        canvas.bind('<Button-1>', self.button)
        self.playersbycolor = {}
        for i in players:
            self.playersbycolor[i.color] = i
        canvas.pack(expand=True, fill=Tkinter.BOTH)
        canvas.focus_set()
        
        self.canvas = canvas
        self.texts = s[:len(self.HEXAGONS)]
        self.tk = tk

        self.paint()

        global INTERSECTIONS
        b=flatten(INTERSECTIONS)

        intc=[(int(b[i+1]),int(b[i])) for i in range(0,len(b),2)]
        intc = sorted(intc)
        intc = [(i[1],i[0]) for i in intc]
        ys = [i[1] for i in intc]
        finalc = map(lambda i: Vector(P=(i[0],i[1]+1)) if (i[1] in ys and i[1]+1 in ys) else Vector(P=(i[0],i[1])),intc)

        self.intersections = finalc
        self.INTERSECTIONMAP = {0:1,1:2,2:3,3:4,4:5,5:5,6:6,7:6,8:7,9:8,15:8,10:9,11:9,16:9,12:10,13:10,17:10,14:11,18:11,
                                22:12,19:13,23:13,26:13,20:14,24:14,27:14,21:15,25:15,28:15,29:16,30:17,38:17,31:18,34:18,39:18,
                                32:19,35:19,40:19,36:20,33:20,41:20,37:21,42:21,47:22,43:23,48:23,52:23,44:24,49:24,53:24,45:25,50:25,54:25,
                                46:26,55:26,51:26,56:27,57:28,67:29,62:29,58:29,59:30,63:30,68:30,60:31,64:31,69:31,61:32,65:32,70:32,66:33,
                                71:34,76:34,72:35,77:35,80:35,73:36,78:36,81:36,74:37,82:37,79:37,75:38,83:38,84:39,85:40,88:40,92:40,86:41,89:41,93:41,
                                87:42,90:42,94:42,91:43,95:44,99:44,96:45,100:45,101:45,97:46,102:46,103:46,98:47,104:47,105:48,106:49,107:49,108:50,109:50,110:51,
                                111:52, 112:53,113:54}
        self.actionpanel = Tkinter.Frame(tk)
        self.actionpanel.place(x=300,y=700)
        self.activefunction = None
        self.buildSettlement = Tkinter.Button(self.actionpanel, text='Settlement',background='grey')
        self.buildSettlement.bind('<Button-1>', self.buildSettlementf)
        self.buildSettlement.pack()
        self.buildCity = Tkinter.Button(self.actionpanel, text='City',background='grey')
        self.buildCity.bind('<Button-1>', self.buildCityf)
        self.buildCity.pack()
        self.buildRoad = Tkinter.Button(self.actionpanel, text='Road',background='grey')
        self.buildRoad.bind('<Button-1>', self.buildRoadf)
        self.buildRoad.pack()
        self.buyCard = Tkinter.Button(self.actionpanel, text='Buy Development Card',background='grey')
        self.buyCard.bind('<Button-1>', self.buyCardf)
        self.useCard = Tkinter.Button(self.actionpanel, text='Use Development Card',background='grey')
        self.useCard.bind('<Button-1>', self.useCardf)
        self.placeBandit = Tkinter.Button(self.actionpanel, text='Place Bandit',background='grey')
        self.placeBandit.bind('<Button-1>', self.placeBanditf)
        self.placeBandit.pack()
        nextplayer = Tkinter.Button(self.actionpanel, text='End Turn', command=self.nextplayer,background='grey')
        nextplayer.pack()
        self.useCard.pack()
        self.buyCard.pack()
        self.PICTUREPATH=r'C:\users\user\desktop\dice' 
        img1 = Tkinter.PhotoImage(file='{}\\start.gif'.format(self.PICTUREPATH))
        d1=Tkinter.Label(canvas, image=img1, anchor=Tkinter.SW)
        d1.photo=img1
        d1.pack()
        self.d1=d1
        img2 = Tkinter.PhotoImage(file='{}\\start.gif'.format(self.PICTUREPATH))
        d2=Tkinter.Label(canvas, image=img1, anchor=Tkinter.SW)
        d2.photo=img2
        d2.pack()
        self.d2=d2
        banditimg = Tkinter.PhotoImage(file='{}\\start.gif'.format(self.PICTUREPATH), width=32,height=32)
        self.banditpct = Tkinter.Label(canvas, image=banditimg)
        self.setbanditcoords(self.BANDITCOORDS)
        self.roads = dict()
        self.oldlocation=None
        self.midroad=None


        #resources
        self.resourcepanel = Tkinter.Frame(tk)
        self.resourcepanel.place(x=700,y=700)
        self.grainc = Tkinter.Button(self.resourcepanel, text='Grain: 0',background=ct['grain'])
        self.grainc.pack()
        self.woodc = Tkinter.Button(self.resourcepanel, text='Wood: 0',background=ct['wood'])
        self.woodc.pack()
        self.clayc = Tkinter.Button(self.resourcepanel, text='Clay: 0',background=ct['clay'])
        self.clayc.pack()
        self.stonec = Tkinter.Button(self.resourcepanel, text='Stone: 0',background=ct['stone'])
        self.stonec.pack()
        self.sheepc = Tkinter.Button(self.resourcepanel, text='Sheep: 0',background=ct['sheep'])
        self.sheepc.pack()

        self.monopanel = None
        self.plentypanel = None
        self.cmenu=None
        self.lbl=None
        self.roadscardon=False
        self.plentyc = 0
        self.roadscardprog = 0
        self.chosenplayer=None

        self.tradewindow = Tkinter.Button(self.actionpanel, text='Trade', background='grey')
        self.tradewindow.bind('<Button-1>', self.tradepanel1)
        self.tradewindow.pack()
        self.tradepanel=None
        self.armyholder=None
        tk.mainloop()


    def tradepanel1(self, EVENT):
        self.tradepanel = Tkinter.Toplevel()
        bank = Tkinter.Button(self.tradepanel, text='Trade with the bank', background='green', command=self.bankpanel)
        
        bank.pack()
        players = Tkinter.Button(self.tradepanel, text='Trade with players', background='white', command=self.playerpanel)
        players.pack()
        exitb = Tkinter.Button(self.tradepanel, text='Exit', command=self.tradepanel.destroy)
        exitb.pack()

    def bankpanel(self):
        self.tradepanel.destroy()
        tradesettings = Tkinter.Toplevel()
        mySettings=Tkinter.Frame(tradesettings)
        otherSettings=Tkinter.Frame(tradesettings)
        a = Tkinter.Button(tradesettings, text='Cancel', command=tradesettings.destroy)
        a.pack()

        myScales = pscales(self.currentplayerobj, mySettings)
        otherScales = pscales(None, otherSettings)

        lazy, verylazy = myScales.scales.values(), otherScales.scales.values()
        for i in myScales.scales:
            myScales.scales[i].pack(side='left')
            if i in self.currentplayerobj.ports:
                myScales.scales[i]['resolution'] = 2
            elif '3x1' in self.currentplayerobj.ports:
                myScales.scales[i]['resolution'] = 3
            else:
                myScales.scales[i]['resolution'] = 4
            myScales.scales[i]['from_'] = myScales.scales[i]['resolution']*int(self.currentplayerobj[i]/myScales.scales[i]['resolution'])

            
            
        for i in verylazy:
            i.pack(side='right')

            
            
            
            
        def confirm():
            
            if all(filter(None, map(lambda x: x.get(), i)) for i in [lazy, verylazy]):
                p1, p2 =range(5), range(5)                
                for i,t in enumerate(['sheep','stone','wood','grain','clay']):
                    
                    p1[i] = int(lazy[i].get()/lazy[i]['resolution'])
                    p2[i] = int(verylazy[i].get()/verylazy[i]['resolution'])

                print p1, p2
                if sum(p1) == sum(p2):
                    for i,t in enumerate(['sheep','stone','wood','grain','clay']):
                        self.currentplayerobj.grant(t, int(-p1[i]*lazy[i]['resolution']))
                        self.currentplayerobj.grant(t, int(p2[i]))
                    

                tradesettings.destroy()

                

        execute = Tkinter.Button(tradesettings, text='Confirm', command=confirm)
        execute.pack()
        mySettings.pack(side='left')
        otherSettings.pack(side='right')
        
        print '{} \n\n -- is trading with -- \n\nBANK\n\n(to be implemented)\n\n'.format(self.currentplayerobj.name)

    def playerpanel(self):
        self.tradepanel.destroy()
        self.chooseplayermenu('Choose a player to trade with...', self.tradewithplayer)

    def tradewithplayer(self, player):
     
        tradesettings = Tkinter.Toplevel()
        mySettings=Tkinter.Frame(tradesettings)
        otherSettings=Tkinter.Frame(tradesettings)
        a = Tkinter.Button(tradesettings, text='Cancel', command=tradesettings.destroy)
        a.pack()

        myScales = pscales(self.currentplayerobj, mySettings)
        otherScales = pscales(player, otherSettings)

        lazy, verylazy = myScales.scales.values(), otherScales.scales.values()
        for i in lazy:
            i.pack(side='left')
        for i in verylazy:
            i.pack(side='right')
            
        def confirm():
            
            if all(filter(None, map(lambda x: x.get(), i)) for i in [lazy, verylazy]):
                p1, p2 =[0]*5, [0]*5
                
                for i,t in enumerate(['sheep','stone','wood','grain','clay']):

                    p1[0] = lazy[0].get()
                    p2[0] = verylazy[0].get()
                    self.currentplayerobj.grant(t, -p1[i])
                    self.currentplayerobj.grant(t, p2[i])
                    player.grant(t, -p2[i])
                    player.grant(t, p1[i])
                tradesettings.destroy()
                self.tradewithplayer(player)
                

        execute = Tkinter.Button(tradesettings, text='Confirm', command=confirm)
        execute.pack()
        mySettings.pack(side='left')
        otherSettings.pack(side='right')

    
    def buyCardf(self, EVENT):
        if self.currentplayerobj.cardable() and self.activefunction == None:
            self.currentplayerobj.cardbuilt()
            self.currentplayerobj.cards += [self.cards.pop()]
            print self.currentplayerobj.cards
            

    def useCardf(self, EVENT):
        if self.activefunction == None:
            self.cardmenu()
        
    def cardmenu(self):
        self.cmenu = Tkinter.Toplevel()
        cardtitles = {'dknight': ' - Knight - \n(counts towards biggest army bonus)','knight': ' - Knight - \nmove the bandit to a new location.', 'plenty': ' - Year of Plenty - \nDraw two resource cards of any type you choose.', 'roads': ' - Road Construction - \nBuild two roads', 'monopole': ' - Monopoly! - \nSteal all resource cards of a specific type from all players.', 'vp': ' - Victory Point - \nThis is worth one victory point.'}
        
        cardfunctions = {'knight': self.banditcard, 'plenty': self.plentycard, 'vp': self.vpcard, 'dknight': None, 'roads': self.roadscard, 'monopole': self.monopolecard}
        availblecards = [Tkinter.Button(self.cmenu, text=cardtitles[i], command=cardfunctions[i]) for i in self.currentplayerobj.cards]
        for i in availblecards:
            if i['text'] in [cardtitles['vp'], cardtitles['dknight']]:
                i.configure(relief='groove', state='disabled')
            i.pack()
        
        a = Tkinter.Button(self.cmenu, text='Exit', command=self.cmenu.destroy)
        a.pack()
        
    def chooseplayermenu(self, text, event,robberhex=None):
        if robberhex != None:
            targets = map(lambda x: x[1], filter(lambda x: x!=None and x[1]!=self.currentplayerobj.color,[i.building for i in Game.hexes[robberhex+1].indexes]))
            if not targets:
                return None
        chooseplayerpanel = Tkinter.Toplevel()
        lbl = Tkinter.Label(chooseplayerpanel, text=text)
        lbl.pack()
    
        def funcbuild(i, event):
            
            def f():
                chooseplayerpanel.destroy()
                event(i)

            return f
        buttons = [Tkinter.Button(chooseplayerpanel, text = i.name, command=funcbuild(i, event), background=i.color) for i in filter(lambda x: x!=self.currentplayerobj, self.players)]
        if robberhex != None:
            
            buttons = filter(lambda x: x['background'] in targets, buttons)
            
            
        
        for i in buttons:
            i.pack()

    def banditcard(self):
        self.currentplayerobj.knightcount += 1
        self.grantbiggestarmy()
        self.placeBanditf(None)
        self.cmenu.destroy()
        index = self.currentplayerobj.cards.index('knight')
        self.currentplayerobj.cards = self.currentplayerobj.cards[:index]+['dknight']+self.currentplayerobj.cards[index+1:]

    def grantbiggestarmy(self):

        cds = filter(lambda x: x.knightcount >= 3, self.players)
        
        mx = sum([x.knightcount for x in cds])
        tied = filter(lambda x: x.knightcount == mx, cds)
        if len(tied) == 1 and tied[0].biggestarmy == False:
            self.givearmytoken(tied[0])

    def givearmytoken(self, player):
        print 'missing graphics(biggest army card)!!'
        if self.armyholder:
            self.armyholder.vp -= 2
            
        self.armyholder=player
        self.armyholder.vp += 2
        
        
      #need to implement once there is a biggest army card graphics - show the token and VP update on relevant turns!'
        
        

    def longestroad(self):

        def findlongestchain(lst, cur, l):
            if cur == None:
                
                return max([findlongestchain(lst - set([i]),i, l+1) for i in lst])

            elif lst == None:
                print 'full'
                return l
            else:
                t = filter(lambda x: x[0] == cur[1] or x[1] == cur[1], lst)
                if t:
                    return max([findlongestchain(lst - set([i]),i, l+1) for i in t])
                else:
                    
                    return l
                
    
            
        d = {}
        players = map(lambda x: x.color, self.players)
    
        for i in players:
            d[i] = []
        for i in self.roads:
            d[self.roads[i]] += [i]
        ls = []
        for i in d:
            if len(d[i])<5:
                print 'lt5'
                ls += [0]
            else:
                ls += [findlongestchain(set(d[i])),None, 0]

        if len(filter(lambda x: x==max(ls), ls)) > 1:
            pass
        x = index(max(ls), ls)
        print x, players[x], self.players[x]
        self.roadholder.longestroad = False
        self.roadholder.vp -= 2
        self.roadholder = self.players[x]
        self.roadholder.longestroad = True
        self.roadholder.vp += 2
        
                
        
    def plentycard(self):
        self.cmenu.destroy()

        self.plentypanel = Tkinter.Toplevel()
        self.lbl = Tkinter.Label(self.plentypanel, text='Select the first bonus resource:')
        self.lbl.pack()
        grainc = Tkinter.Button(self.plentypanel, text='Grain', command=self.grainf1,background=ct['grain'])
        grainc.pack()
        woodc = Tkinter.Button(self.plentypanel, text='Wood', command=self.woodf1,background=ct['wood'])
        woodc.pack()
        clayc = Tkinter.Button(self.plentypanel, text='Clay', command=self.clayf1,background=ct['clay'])
        clayc.pack()
        stonec = Tkinter.Button(self.plentypanel, text='Stone', command=self.stonef1,background=ct['stone'])
        stonec.pack()
        sheepc = Tkinter.Button(self.plentypanel, text='Sheep', command=self.sheepf1,background=ct['sheep'])
        sheepc.pack()
        index = self.currentplayerobj.cards.index('plenty')
        self.currentplayerobj.cards = self.currentplayerobj.cards[:index]+self.currentplayerobj.cards[index+1:]


    def grainf1(self):
        
        if self.plentyc == 0:

            self.lbl.configure(text='Select the second bonus resource:')
            self.plentyc = 1
            self.currentplayerobj.grant('grain', 1)
        else:
            self.plentypanel.destroy()

            self.currentplayerobj.grant('grain', 1)
            self.plentyc = 0
            
        

    def stonef1(self):
        if self.plentyc == 0:

            self.lbl.configure(text='Select the second bonus resource:')
            self.plentyc = 1
            self.currentplayerobj.grant('stone', 1)
        else:
            self.plentypanel.destroy()

            self.currentplayerobj.grant('stone', 1)
            self.plentyc = 0

    def clayf1(self):
        if self.plentyc == 0:

            self.lbl.configure(text='Select the second bonus resource:')
            self.plentyc = 1
            self.currentplayerobj.grant('clay', 1)
        else:
            self.plentypanel.destroy()

            self.currentplayerobj.grant('clay', 1)
            self.plentyc = 0

    def sheepf1(self):
        if self.plentyc == 0:

            self.lbl.configure(text='Select the second bonus resource:')
            self.plentyc = 1
            self.currentplayerobj.grant('sheep', 1)
        else:
            self.plentypanel.destroy()

            self.currentplayerobj.grant('sheep', 1)
            self.plentyc = 0

    def woodf1(self):
        if self.plentyc == 0:

            self.lbl.configure(text='Select the second bonus resource:')
            self.plentyc = 1
            self.currentplayerobj.grant('wood', 1)
        else:
            self.plentypanel.destroy()

            self.currentplayerobj.grant('wood', 1)
            self.plentyc = 0
    
    def vpcard(self):
        pass
        
    def roadscard(self):
        self.roadscardon = True
        self.buildRoad.configure(state='disabled')
        self.buildRoadf(None)

    def monopolecard(self):
        self.cmenu.destroy()
        index = self.currentplayerobj.cards.index('monopole')
        self.currentplayerobj.cards = self.currentplayerobj.cards[:index]+self.currentplayerobj.cards[index+1:]
        self.monopanel = Tkinter.Toplevel()
        lbl = Tkinter.Label(self.monopanel, text='Choose a resource type:')
        lbl.pack()
        grainc = Tkinter.Button(self.monopanel, text='Grain', command=self.grainf,background=ct['grain'])
        grainc.pack()
        woodc = Tkinter.Button(self.monopanel, text='Wood', command=self.woodf,background=ct['wood'])
        woodc.pack()
        clayc = Tkinter.Button(self.monopanel, text='Clay', command=self.clayf,background=ct['clay'])
        clayc.pack()
        stonec = Tkinter.Button(self.monopanel, text='Stone', command=self.stonef,background=ct['stone'])
        stonec.pack()
        sheepc = Tkinter.Button(self.monopanel, text='Sheep', command=self.sheepf,background=ct['sheep'])
        sheepc.pack()
        

    def turn_iter(self):
        
        for i in self.players:
            self.currentplayer += 1
            yield i
        for i in self.players[::-1]:
            yield i
            self.currentplayer += 1
        while 1:
            for i in self.players:
                yield i
                self.currentplayer += 1
        
    def grainf(self):
        count = 0
        for i in self.players:
            if i != self.currentplayerobj:
                count += i.grain
                i.grant('grain', -i.grain)
        self.currentplayerobj.grant('grain', count)
        self.monopanel.destroy()
        
    def woodf(self):
        count = 0
        for i in self.players:
            if i != self.currentplayerobj:
                count += i.wood
                i.grant('wood', -i.wood)
        self.currentplayerobj.grant('wood', count)
        self.monopanel.destroy()
        
    def clayf(self):
        count = 0
        for i in self.players:
            if i != self.currentplayerobj:
                count += i.clay
                i.grant('clay', -i.clay)
        self.currentplayerobj.grant('clay', count)
        self.monopanel.destroy()
        
    def stonef(self):
        count = 0
        for i in self.players:
            if i != self.currentplayerobj:
                count += i.stone
                i.grant('stone', -i.stone)
        self.currentplayerobj.grant('stone', count)
        self.monopanel.destroy()
        
    def sheepf(self):
        count = 0
        for i in self.players:
            if i != self.currentplayerobj:
                count += i.sheep
                i.grant('sheep', -i.sheep)
        self.currentplayerobj.grant('sheep', count)
        self.monopanel.destroy()
        
    def updateresources(self):
        p = self.currentplayerobj
        self.grainc.configure(text='Grain: {}'.format(p.grain))
        self.woodc.configure(text='Wood: {}'.format(p.wood))
        self.clayc.configure(text='Clay: {}'.format(p.clay))
        self.stonec.configure(text='Stone: {}'.format(p.stone))
        self.sheepc.configure(text='Sheep: {}'.format(p.sheep))
        
        

        
    def nextplayer(self):
        if self.activefunction != None and not self.freemode:
            return None
            
        if self.freecount == 4*len(self.players):
            self.freemode = False

        if self.freeprogress == self.freecount or self.freemode == False:
            self.freeprogress += 2

            print 'previous player: {}'.format(self.currentplayer)
            self.currentplayer = (self.currentplayer+1) % len(self.players)
            self.currentplayerobj = self.playNow.next()
            print 'starting turn of player: {}'.format(self.currentplayer)
            if not self.freemode:
                diceroll1,diceroll2 = random.randint(1,6),random.randint(1,6)
                img1,img2=Tkinter.PhotoImage(file='{}\\{}.gif'.format(self.PICTUREPATH, diceroll1)),Tkinter.PhotoImage(file='{}\\{}.gif'.format(self.PICTUREPATH, diceroll2))
                self.d1.configure(image=img1)
                self.d1.photo=img1
                self.d2.configure(image=img2)
                self.d2.photo=img2

                self.yieldresource(diceroll1+diceroll2)

    def buildSettlementf(self,EVENT):


            
        if self.activefunction == None or self.activefunction == self.buildSettlementf:
            self.activefunction = self.buildSettlementf
        
            if self.boardclickable == False:
            
                self.buildSettlement.configure(background=self.currentplayerobj.color, text='Cancel')
                self.boardclickable=True
        
            
            else:
            
                self.buildSettlement.configure(background='grey', text='Settlement')
                self.boardclickable = False
                self.activefunction = None
    #test
    def buildRoadf(self,EVENT):
        if self.buildRoad['state'] == 'disabled':
            pass

        
        if self.activefunction == None or self.activefunction == self.buildRoadf:
            self.activefunction = self.buildRoadf
        
            if self.boardclickable == False:
            
                self.buildRoad.configure(background=self.currentplayerobj.color, text='Cancel')
                self.boardclickable=True
        
            
            else:
            
                self.buildRoad.configure(background='grey', text='Road')
                self.boardclickable = False
                self.activefunction = None
                self.oldlocation=None
                self.midroad=None
        
        
    
    def buildCityf(self,EVENT):


        if self.activefunction == None or self.activefunction == self.buildCityf:
            self.activefunction = self.buildCityf
        
            if self.boardclickable == False:
            
                self.buildCity.configure(background=self.currentplayerobj.color, text='Cancel')
                self.boardclickable=True
        
            
            else:
            
                self.buildCity.configure(background='grey', text='City')
                self.boardclickable = False
                self.activefunction = None

    def placeBanditf(self,EVENT):


        if self.activefunction == None or self.activefunction == self.placeBanditf:
            self.activefunction = self.placeBanditf
        
            if self.boardclickable == False:
            
                self.placeBandit.configure(background=self.currentplayerobj.color, text='Cancel')
                self.boardclickable=True
        
            
            else:
            
                self.placeBandit.configure(background='grey', text='Place Bandit')
                self.boardclickable = False
                self.activefunction = None
                
    def paint(self):
        global ct
        canvas = self.canvas
        canvas.anchor = Tkinter.CENTER
        S = self.texts
        
        for (I,H) in enumerate(self.HEXAGONS):

            canvas.create_polygon(*H.flat, fill=(H.color, 'cyan')[self.SELECTED[I]])
            
            if H.color == ct['desert']:
                
                canvas.create_text(*H.center, text=' ',fill='black')
                
                self.robberpos = I
                self.BANDITCOORDS = H.center
                S=S[:I]+[' ']+S[I:]

            else:
                if int(S[I]) in [2,12]:
                    size=12
                else:
                    size=16
                if int(S[I]) in [6,8]:
                    col = 'red'
                else:
                    col = 'black'
                canvas.create_text(*H.center, text=S[I],fill=col, font=('Tahoma',size))
        self.texts=S

            
        for H in self.HEXAGONS:
             canvas.create_loop(*H.flat, width=3)
        
        self.tk.update_idletasks()

        print self.HEXAGONS


    def setbanditcoords(self, coords):
        
        self.banditpct.place(x=coords.P[0]-16, y=coords.P[1]-16)
        
    def __call__(self):
        return ' '.join(self.texts[J] for J in self.SELECTIONS)

    

    def button(self, EVENT):
       
        if self.boardclickable==True:
            
            BUTTONRADIUS=15
            A = Vector(P=(EVENT.x,EVENT.y))
            (BEST,SHORTEST) = (None, 9e44)
            if self.activefunction in [self.__init__, self.placeBanditf]:
            
                for (I,H) in enumerate(self.HEXAGONS):
                    L = (A-Vector(P=H.center)).dot()
                    
                    if L<SHORTEST and L<(0.85*H.radius)**2:
                        (BEST,SHORTEST) = (I,L)
                        
                if BEST == None:
                    print 'clicked nothing(debug1)'
                else:
                    self.clickedhex(BEST)

            if self.activefunction in [self.buildSettlementf,self.buildCityf,self.buildRoadf]:
                
                for (I,V) in enumerate(self.intersections):
                    L = (A-Vector(P=V)).dot()

                    if L<SHORTEST and L<(BUTTONRADIUS)**2:
                        (BEST,SHORTEST) = (I,L)
                        
                if BEST == None:
                    print 'clicked nothing(debug2)'
                else:
                    
                    self.clickedinter(self.INTERSECTIONMAP[BEST], EVENT)

    def distancecheck(self, inter):
        dst1 = Game.nodes[inter].linked
        if all([not i.building for i in dst1]):
            return 1
        return 0
    
        
    def settable(self, inter):
        if Game.nodes[inter].building == None and self.distancecheck(inter):
            
            if self.freemode:
                return 1
            elif self.currentplayerobj.settable() and inter in self.myroads():
                return 1
        return 0
    def cityable(self, inter):
        if Game.nodes[inter].building == ('settlement', self.currentplayerobj.color):
            
            return 1

    def clickedhex(self,terrain):
        if self.activefunction == self.placeBanditf:
            self.setbanditcoords(self.HEXAGONS[terrain].center)
            self.banditpos = terrain

            self.banditchoice(terrain)
            self.activefunction(None)

    def banditchoice(self,terrain):
        print 'bandit on {} event!'.format(terrain)
        self.chooseplayermenu('Choose a player to steal from:', self.banditevent, terrain)
        
        #when a user places the bandit - choose target to steal from according to given terrain, then use banditevent() on relevant target
    def legalRoad(self,inter1, inter2):

        
        if (Game.nodes[inter2] in Game.nodes[inter1].linked) and ((inter1,inter2) not in self.roads) and ((inter2,inter1) not in self.roads):
            
            myroads = self.myroads()
            print myroads, inter1, inter2, self.roads
            if (inter1 in myroads or inter2 in myroads) and (self.currentplayerobj.roadable() or self.roadscardon == True):

                return 1
             #currently very bad - not allowing a road near another player's settlement(fix!)
            if Game.nodes[inter1].building:
                if Game.nodes[inter1].building[1] == self.currentplayerobj.color:
                        if self.freemode or self.currentplayerobj.roadable():

                            return 1

                
            elif Game.nodes[inter2].building:
                if Game.nodes[inter2].building[1] == self.currentplayerobj.color:
                    if self.freemode or self.currentplayerobj.roadable() or self.roadscardon:

                        return 1

                
            
        return 0
    
    def myroads(self):
        return flatten(filter(lambda x: self.roads[x] == self.currentplayerobj.color, self.roads.keys()))
    
    def clickedinter(self, inter, EVENT):
        

        if self.activefunction == self.buildSettlementf and self.settable(inter):

            if self.freemode and (self.freecount) % 2:
                pass

            else:

                self.canvas.create_oval(EVENT.x-10,EVENT.y-10,EVENT.x+10,EVENT.y+10,fill=self.currentplayerobj.color)
                if inter in Game.portlocations:
                    self.currentplayerobj.ports += [Game.ports[Game.portlocations[inter]]]
                    print self.currentplayerobj
                if self.freemode and self.freecount >= len(self.players):
                    self.resourcebonus(inter)
                Game.nodes[inter].building = ('settlement', self.currentplayerobj.color)
                if self.freemode:
                    self.freecount += 1
                    self.tempinter = inter
                else:
                    self.currentplayerobj.settbuilt()
            self.activefunction(None)
            self.activefunction = None
        elif self.activefunction == self.buildCityf and self.cityable(inter):
            
            self.canvas.create_rectangle(EVENT.x-12,EVENT.y-12,EVENT.x+12,EVENT.y+12,fill=self.currentplayerobj.color)
            self.canvas.create_oval(EVENT.x-5,EVENT.y-5,EVENT.x+5,EVENT.y+5,fill='white')
            self.currentplayerobj.citybuilt()
            
            Game.nodes[inter].building = ('city', self.currentplayerobj.color)
            self.activefunction(None)
            self.activefunction = None
        elif self.activefunction == self.buildRoadf:
            if self.midroad:
                if self.legalRoad(inter,self.midroad):

                    if self.freemode and (self.freecount + 1) % 2:
                        pass

                    else:
                        if not (self.freemode and self.tempinter not in [self.midroad, inter]):
                            self.canvas.create_line(EVENT.x, EVENT.y, self.oldlocation.x, self.oldlocation.y, fill=self.currentplayerobj.color, width=6)
                            self.roads[(inter,self.midroad)] = self.currentplayerobj.color
                            self.tempinter = None
                            if self.freemode:
                                self.freecount += 1
                                
                                self.nextplayer()
                            elif self.roadscardon:
                                if self.roadscardprog == 1:
                                    self.roadscardon = False
                                    self.roadscardprog = 0
                                    self.buildRoad.configure(state='enabled')
                                else:
                                    self.roadscardprog = 1
                                
                            else:
                                self.currentplayerobj.roadbuilt()
                            

                self.midroad = None
                self.activefunction(None)
                self.activefunction = None
                if self.roadscardon:
                    self.buildRoadf(None)
                
                    
            else:
                self.midroad = inter
                self.oldlocation = EVENT
            print self.longestroad()
             

            
            
    def resourcebonus(self, inter):
        
        
        targets = filter(lambda t: inter in [i.number for i in t.indexes], Game.lst)
        q = [ord(t.name)-97 for t in targets]
        for i in q:
            self.currentplayerobj.grant(self.HEXAGONS[i].color, 1)
        
        
        
        
            
        
    def comb(self, radius=20, rotation=0):
        C=Vector(P=(radius*4, radius*2))
        H = Terrain(center = C, radius = radius, rotation = rotation, color=painter.next(),number='tba')
        IR = H.inner_radius
        OFFSET = Vector(P=(1.9*IR,0))
        HEXAGONS = [H]
        for i in range(2):
            C+= OFFSET
            HEXAGONS.append(Terrain(center=C,radius=radius,rotation=rotation, color=painter.next(),number='tba'))
        
        
        C=Vector(P=(radius*1.15,radius*3.65))
        for i in range(4):

            
            HEXAGONS.append(Terrain(center=C+OFFSET,radius=radius,rotation=rotation, color=painter.next(),number='tba'))
            C+=OFFSET
        C=Vector(P=(radius*0.2,radius*5.3))
        for i in range(5):

            
            HEXAGONS.append(Terrain(center=C+OFFSET,radius=radius,rotation=rotation, color=painter.next(),number='tba'))
            C+=OFFSET
        C=Vector(P=(radius*1.15,radius*6.95))
        for i in range(4):

            
            HEXAGONS.append(Terrain(center=C+OFFSET,radius=radius,rotation=rotation, color=painter.next(),number='tba'))
            C+=OFFSET
            
        C=Vector(P=(radius*2.1,radius*8.6))
        for i in range(3):

            
            HEXAGONS.append(Terrain(center=C+OFFSET,radius=radius,rotation=rotation, color=painter.next(),number='tba'))
            C+=OFFSET
            
        self.HEXAGONS=HEXAGONS
        


    def yieldresource(self,n):
        if n == 7:
            print 'temp bandit event from dice roll!!!'
            self.placeBanditf(None)
        targets=[]
        for i in range(len(self.texts)):
            if str(n) == self.texts[i] !=str(self.robberpos):
                targets+=[i]
        for i in targets:
            for j in Game.hexes[i+1].indexes:
                if j.building:
                    pl = self.playersbycolor[j.building[1]]
                    if j.building[0] == 'settlement':
                        
                        pl.grant(self.HEXAGONS[i].color,1)
                    else:
                        pl.grant(self.HEXAGONS[i].color,2)
                    #tbc
        self.updateresources()

    def banditevent(self, target):
        opts = ['wood']*target.wood + ['clay']*target.clay + ['stone']*target.stone + ['grain']*target.grain + ['sheep']*target.sheep
        print 'banditevent occured.'
        print 'target={}'.format(target)
        if opts:
            t = random.choice(opts)
            self.currentplayerobj.grant(t, 1)
            target.grant(t,-1)
            print '{} transferred from {} to {}'.format(t, self.currentplayer, target)
        else:
            print 'no resources to steal'
        
                    
def makeboard():
    global INTERSECTIONS
    

    UC = [str(j) for j in (range(3,7)+range(8,12))*2+[2,12]]
    random.shuffle(UC)
    pnames = [('player1','red'),('player2','blue'), ('player3', 'green'), ('player4', 'purple')]
    TEMP =  ['roads']*10#CHANGE TO EMPTY LIST AFTER DEBUGGING IS OVER!!!!
    playerslist = [player(name=i[0], cards=TEMP, color=i[1], roadlength=0, vp=0, ishuman=1, knightcount=0, biggestarmy=False, longestroad=False, sheep=0,stone=0,clay=0,wood=0,grain=0,ports=[]) for i in pnames]
    HC = Settlers(s=UC,intersections=[],players=playerslist)


class Hex:

    def __init__(self, name, indexeslist):
        self.indexes = indexeslist
        self.blocked = False
        self.type = None
        self.name = name

    def block(self):
        self.block = True

    def unblock(self):
        self.block = False

    def __repr__(self):
        return "hex {}".format(self.name)
class index:

    def __init__(self, number, linkedset=None):
        self.number = number
        self.linked = linkedset
        self.building = None

    def setlinks(self, links):
        if self.linked == None:
            self.linked = links
        else:
            self.linked = self.linked | links

    def build(self, player, building):
        self.building = (player, building)

    def decon(self):
        self.building = None

    def __repr__(self):
        return "link number {}".format(self.number)


class game:
    def __init__(self,players):
        #board construction
        self.HC = None
        temp = [index(i) for i in range(1,55)]
        nodes = {}
        for i in range(len(temp)):
            nodes[i+1] = temp[i]
        self.nodes = nodes
        lst = [Hex(chr(96+i),[nodes[i], nodes[i+3], nodes[i+4], nodes[i+7], nodes[i+8], nodes[i+12]]) for i in range(1,4)]
        lst += [Hex(chr(92+i),[nodes[i], nodes[i+4], nodes[i+5], nodes[i+9], nodes[i+10], nodes[i+15]]) for i in range(8,12)]
        lst += [Hex(chr(87+i),[nodes[i], nodes[i+5], nodes[i+6], nodes[i+11], nodes[i+12], nodes[i+17]]) for i in range(17,22)]
        lst += [Hex(chr(80+i),[nodes[i], nodes[i+5], nodes[i+6], nodes[i+10], nodes[i+11], nodes[i+15]]) for i in range(29,33)]
        lst += [Hex(chr(73+i),[nodes[i], nodes[i+4], nodes[i+5], nodes[i+8], nodes[i+9], nodes[i+12]]) for i in range(40,43)]
        self.lst = lst
        hexes = {}
        for i in range(len(lst)):
            hexes[i+1] = lst[i]

        for i in lst:
            for l,k in enumerate([(1,2), (0,3), (0,4), (1,5), (2,5), (3,4)]):
                i.indexes[l].setlinks(set([i.indexes[k[0]],i.indexes[k[1]]]))

        self.hexes = hexes
        self.players=players
        self.ports = ['sheep', 'stone', 'wood', 'grain', 'clay']+['3x1']*4
        random.shuffle(self.ports)
        self.portlocations = {2:0,5:0,3:1,7:1,8:2,12:2,16:3,21:3,22:4,28:4,38:5,43:5,39:6,44:6,49:7,53:7,51:8,54:8}
        


class player(Base):

    mandatory_arguements = set('name color ishuman wood stone sheep grain clay vp roadlength knightcount biggestarmy longestroad cards ports'.split())
    
    def __init__(self,**args):
        Base.__init__(self, **args)

    def __getitem__(self, index):
        if index == 'wood':
            return self.wood
        elif index == 'stone':
            return self.stone
        elif index == 'clay':
            return self.clay
        elif index == 'sheep':
            return self.sheep
        elif index == 'grain':
            return self.grain


        

    def roadable(self):
        
        if self.wood >= 1 and self.clay >= 1:
            return True
        return False
    def roadbuilt(self):
        self.wood -= 1
        self.clay -= 1
        Game.HC.updateresources()

    def cityable(self):
        
        if self.stone >= 3 and self.grain >= 2:
            return True
        return False
    
    def citybuilt(self):
        self.stone -= 3
        self.grain -= 2
        Game.HC.updateresources()
        
    def settable(self):
        
        if self.grain >= 1 and self.sheep >= 1 and self.wood >= 1 and self.clay >= 1:
            return True
        return False
        
    def settbuilt(self):
        self.sheep -= 1
        self.grain -= 1
        self.clay -= 1
        self.wood -= 1
        Game.HC.updateresources()

    def cardable(self):
        
        if self.grain >= 1 and self.sheep >= 1 and self.stone >= 1:
            return True
        return False
        
    def cardbuilt(self):
        self.sheep -= 1
        self.grain -= 1
        self.stone -= 1
        Game.HC.updateresources()

    



    
    def grant(self,name, q=1):
        global ct
        if name == ct['wood'] or name == 'wood':
            self.wood += q

        elif name == ct['clay'] or name == 'clay':
            self.clay += q

        elif name == ct['stone'] or name == 'stone':
            self.stone += q

        elif name == ct['grain'] or name == 'grain':
            self.grain += q

        elif name == ct['sheep'] or name == 'sheep':
            self.sheep += q

        Game.HC.updateresources()
        

    
            
            
    

            
#temp
if __name__ == '__main__':
    #players = raw_input('Number of players: ')
    Game=game(4)
    
    makeboard()

#pnames = [('player1','red'),('player2','blue')]
#players = [player(name=i[0], cardcount=0, color=i[1], roadlength=0, vp=0, ishuman=1, cardused=0, knightcount=0, sheep=0,stone=0,clay=0,wood=0,grain=0) for i in pnames]
    

