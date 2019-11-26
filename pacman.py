from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Pac-Man class defines characteristics of Pac-Man and draws Pac-Man
class PacMan(Mode):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.radius=10
        self.color="yellow"
        self.url="http://labs.phaser.io/assets/games/pacman/sprites32.png"
    def drawPacMan(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)