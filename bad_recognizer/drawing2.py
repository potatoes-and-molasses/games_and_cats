import time
import Tkinter
import math
import os

def dst(p1, p2):
    return (abs(p1[0]-p2[0])**2+abs(p1[1]-p2[1])**2)**0.5 

class Pattern():

    def __init__(self, strokes):

        if isinstance(strokes, list):
            self.strokes = strokes
        elif isinstance(strokes, str):
            
            a=open(strokes, 'r').read()

            strokes = a.split('+')
            tmp=[]
            for j in strokes:
                strk = []
                for k in j.split('%'):
                    z = k.split('-')
                    strk += [(float(z[0]), float(z[1]))]
                    
                
                tmp+=[strk]
            self.strokes = tmp
        self.functions = {'per-stroke-regular-distance':self.lstdst, 'per-stroke-directional-distance':self.lstdst2}


    def distance(self, other, f):

        

        #for now same number of strokes is essential
        if len(self.strokes) != len(other.strokes):
            return -1
        s = sum(self.lstdst2(self.strokes[i], other.strokes[i]) for i in range(len(self.strokes)))

            
        return s


    def lstdst(self, l1, l2):
        if len(l1) <= len(l2):
            relative = 1.0*len(l1)/len(l2)
            test=map(lambda x: x[0]+x[1], l1)
            m=min(test)
            topleft1=test.index(m)
            test=map(lambda x: x[0]+x[1], l2)
            m=min(test)
            topleft2=test.index(m)
            
            dx,dy=l1[topleft1][0]-l2[topleft2][0],l1[topleft1][1]-l2[topleft2][1]
            print dx,dy
            #dx, dy = l1[0][0]-l2[0][0], l1[0][1]-l2[0][1]
            l2 = map(lambda x: (x[0]+dx, x[1]+dy), l2)
            summ = 0
            for j in range(len(l1)):
                c1, c2 = l1[j], l2[int(relative*j)]
                
                summ += dst(c1,c2)

            return summ
        else:
            return self.lstdst(l2,l1)
        
            

    def lstdst2(self, l1,l2):
        if len(l1) <= len(l2):
            relative = 1.0*len(l1)/len(l2)
            
            print l1
            for i in range(len(l1)):
                pass
            
            summ = 0
            for j in range(len(l2)):
                c1, c2 = l1[int(relative*j)], l2[j]
                
                summ += dst(c1,c2)

            return summ
        else:
            return self.lstdst(l2,l1)

class Drawing():
    def __init__(self):

        self.POINTSDISTANCE=1
        self.root = Tkinter.Tk()
        self.pre=None
        self.DEFAULTDIR = r'C:\users\MY_USER_HEHE\desktop\patterns'
        self.patterns = {}
        self.loadpatterns(self.DEFAULTDIR)
        canvas = Tkinter.Canvas(self.root, width=678, height=678)
        canvas.pack(expand=True, fill=Tkinter.BOTH)
        canvas.focus_set()
        canvas.bind('<ButtonPress-1>', self.onPress)
        canvas.bind('<B1-Motion>', self.onMotion)
        canvas.bind('<ButtonRelease-1>', self.onRelease)
        self.canvas = canvas
        self.strokes = []
        a = Tkinter.Button(self.root, text='clear', command=self.clear)
        b = Tkinter.Button(self.root, text='find match', command=self.findmatch)
        c = Tkinter.Button(self.root, text='export', command=self.export)
        a.pack()
        b.pack()
        c.pack()
        self.coordsHistory = []
        self.root.mainloop()
        

    def loadpatterns(self, dirpath):
        for i in os.listdir(dirpath):
            self.patterns[i] = Pattern(dirpath+'\\{}'.format(i))

    def clear(self):
        self.canvas.delete('all')
        self.strokes = []
        self.coordsHistory = []
        self.pre = None

    def onPress(self, EVENT):


        self.coordsHistory += [(EVENT.x, EVENT.y)]
        
    def onRelease(self, EVENT):


        self.pre = None


        self.strokes += [self.coordsHistory]
        self.coordsHistory = []
        
    

    def addpoints(self, p1, p2):
        if dst(p1, p2)<self.POINTSDISTANCE:
            return 1
        new = (1.0*(p1[0]+p2[0])/2,1.0*(p1[1]+p2[1])/2)
        #self.canvas.create_oval(new[0]-5, new[1]-5, new[0]+5, new[1]+5, fill='red')
        self.coordsHistory += [(new[0], new[1])]
        self.addpoints(new, p1)
        self.addpoints(new, p2)

    def onMotion(self, EVENT):
        
        #self.canvas.create_oval(EVENT.x-5, EVENT.y-5, EVENT.x+5, EVENT.y+5, fill='black')
        if self.pre:
            self.addpoints((EVENT.x, EVENT.y), (self.pre.x, self.pre.y))
            self.canvas.create_line(EVENT.x, EVENT.y, self.pre.x, self.pre.y, smooth=True, width=4)

        self.pre=EVENT

        self.coordsHistory += [(EVENT.x, EVENT.y)]


    def findmatch(self):
        mypattern = Pattern(self.strokes)
        mindst = 100000000000
        t=None
        for f in mypattern.functions:
            for i in self.patterns:
                a = mypattern.distance(self.patterns[i], mypattern.functions[f])
                print 'distance from {} using {}: {}'.format(i, f, a)
                if a >= 0 and a < mindst:
                    t = i
                    mindst = a
        if t!=None:
            print 'closest match: {} (dst {})'.format(t, mindst)
                    
            

    def filestring(self):

        return '+'.join(['%'.join(['-'.join([str(k) for k in j]) for j in i]) for i in self.strokes])
        
    def export(self):

        st = self.filestring()
        path = raw_input(self.DEFAULTDIR+'\\')
        f = open(self.DEFAULTDIR+'\\'+path, 'w')
        f.write(st)
        
        f.close()
        self.patterns[path] = Pattern(self.strokes)

        
a=Drawing()



