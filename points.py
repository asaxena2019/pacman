from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Points class defines characteristics of points and draws points
class Points(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.radius=5
    def drawPoints(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill="orange")