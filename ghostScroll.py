from cmu_112_graphics import *
from pacman import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Ghost class defines characteristics of ghosts, draws ghosts, 
# and defines movement

# specifically for sidescroll to avoid bugs with Pac-Man and ghosts not being
# on the same screen
class Ghost(object):
    def __init__(self):
        self.speed=5
        self.x,self.y=0,0
        self.radius=10
        self.color=None
        self.dx,self.dy=0,-1*self.speed
        self.currDirection="down"
        self.direction=self.currDirection
        self.legalDirections=["up","right","down","left"]
        self.distances=set()
    def dirSetter(self):
        if self.currDirection=="right":
            self.speedSetter(self.speed,0)
        elif self.currDirection=="left":
            self.speedSetter(-1*self.speed,0)
        elif self.currDirection=="up":
            self.speedSetter(0,-1*self.speed)
        elif self.currDirection=="down":
            self.speedSetter(0,self.speed)
    def speedSetter(self,dx,dy):
        self.dx=dx
        self.dy=dy
    def shortestGhost(self,ghosts):
        for ghost in ghosts:
            distance=((self.x-ghost.x)**2+(self.y-ghost.y)**2)**0.5
            self.distances.add(distance)
        minDist=min(self.distances)
        for ghost in ghosts:
            if ((self.x-ghost.x)**2+(self.y-ghost.y)**2)**0.5==minDist:
                return (ghost.x,ghost.y)
    def moveGhost(self,ghosts,a,b): #x,y are Ghost's positions
        x,y=self.shortestGhost(ghosts)
        if x==self.x and y==self.y:
            x,y=a,b
        if self.currDirection in self.legalDirections:
            if y<self.y:
                if x<self.x:
                    if self.x-x<self.y-y:
                        self.currDirection="up"
                    else:
                        self.currDirection="left"
                else:
                    if x-self.x<self.y-y:
                        self.currDirection="up"
                    else:
                        self.currDirection="right"
            else:
                if x<self.x:
                    if self.x-x<y-self.y:
                        self.currDirection="down"
                    else:
                        self.currDirection="left"
                else:
                    if x-self.x<y-self.y:
                        self.currDirection="down"
                    else:
                        self.currDirection="right"
        else:
            if self.currDirection=="left" or self.currDirection=="right":
                if y<self.y:
                    self.currDirection="up"
                else:
                    self.currDirection="down"
            elif self.currDirection=="up" or self.currDirection=="down":
                if x<self.x:
                    self.currDirection="left"
                else:
                    self.currDirection="right"
        self.dirSetter()
        if self.currDirection in self.legalDirections:
            self.x+=self.dx
            self.y+=self.dy
    def drawGhost(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)

class Inky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="aqua"

class Pinky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="pink"

class Blinky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="red"

class Clyde(Ghost):
    def __init__(self):
        super().__init__()
        self.color="orange"