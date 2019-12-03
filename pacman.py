from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Pac-Man class defines characteristics of Pac-Man and draws Pac-Man
class PacMan(object):
    def __init__(self):
        self.speed=5
        self.x,self.y=0,0
        self.dx,self.dy=-1*self.speed,0
        self.radius=10
        self.color="yellow"
        self.currDirection="left"
        self.direction=self.currDirection
        self.legalDirections=["up","right","down","left"]
        self.url="http://labs.phaser.io/assets/games/pacman/sprites32.png"
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
    def movePacMan(self):
        if self.direction in self.legalDirections:
            self.currDirection=self.direction
        self.dirSetter()
        if self.currDirection in self.legalDirections:
            self.x+=self.dx
            self.y+=self.dy
    def drawPacMan(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)