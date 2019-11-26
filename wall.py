from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Wall class defines characteristics of walls and draws walls
class Wall(Mode):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color="blue"
    def drawWall(self,canvas):
        canvas.create_rectangle(self.x,self.y,\
            self.x+self.width,self.y+self.height,fill=self.color,width=0)