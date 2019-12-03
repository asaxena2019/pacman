from cmu_112_graphics import *
from wall import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# OriginalBoard class draws walls based on given dimensions
# original board is static, and the dimensions and coordinates are predetermined
class OriginalBoard(Wall):
    def __init__(self,mode,x,y,width,height):
        super().__init__(x,y,width,height)
        self.ratio1=50/mode.width
        #right wall
        rightWall=Wall(2*self.x,2*self.y,self.width,\
            mode.height-4*self.height)
        #left wall
        leftWall=Wall(mode.width-3*self.x,2*self.y,self.width,\
            mode.height-4*self.height)
        #top wall
        topWall=Wall(2*self.x,2*self.y,mode.width-4*self.width,\
            self.height)
        #bottom wall
        bottomWall=Wall(2*self.x,mode.height-3*self.y,mode.width-4*self.width,\
            self.height)
        #1
        wall11=Wall(10*self.x,20*self.y,10*self.width,50*self.height)
        #5
        wall51=Wall(10*self.x+2*self.ratio1*mode.width,20*self.y,20*self.width,\
            10*self.height)
        wall52=Wall(10*self.x+2*self.ratio1*mode.width,20*self.y+10*self.height,\
            10*self.width,20*self.height)
        wall53=Wall(20*self.x+2*self.ratio1*mode.width,20*self.y+20*self.height,10*self.width,\
            20*self.height)
        wall54=Wall(10*self.x+2*self.ratio1*mode.width,20*self.y+40*self.height,20*self.width,\
            10*self.height)
        #dash 
        wallDash=Wall(10*self.x+50*self.width,20*self.y+20*self.width,\
            10*self.width,10*self.height)
        #1
        wall12=Wall(80*self.x,20*self.y,10*self.width,50*self.height)
        #1
        wall13=Wall(100*self.x,20*self.y,10*self.width,50*self.height)
        #2
        wall21=Wall(100*self.x+2*self.ratio1*mode.width,20*self.y,20*self.width,\
            10*self.height)
        wall22=Wall(110*self.x+2*self.ratio1*mode.width,20*self.y+10*self.height,\
            10*self.width,20*self.height)
        wall23=Wall(100*self.x+2*self.ratio1*mode.width,20*self.y+20*self.height,10*self.width,\
            20*self.height)
        wall24=Wall(100*self.x+2*self.ratio1*mode.width,20*self.y+40*self.height,20*self.width,\
            10*self.height)
        self.board=[wall11,wall51,wall52,wall53,wall54,wallDash,wall12,wall13,\
            wall21,wall22,wall23,wall24,rightWall,leftWall,topWall,bottomWall]
        self.dimensions=set()
        for wall in self.board:
            self.dimensions.add((wall.x,wall.y,wall.width,wall.height))
    def drawBoard(self,canvas):
        for wall in self.board:
            wall.drawWall(canvas)
    def drawCells(self):
        self.rows=500//50
        self.cols=750//50
        self.table=[[0]*self.cols for row in range(self.rows)]
        for wall in self.dimensions:
            for col in range(int(wall[0]),int(wall[0])+int(wall[2]),50):
                for row in range(int(wall[1]),int(wall[1])+int(wall[3]),50):
                    self.table[row//50][col//50]=1
        return self.table