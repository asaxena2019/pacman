from cmu_112_graphics import *
from wall import *
import random

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# creates a randomly generated board for sidescroll, single, and multiplayer mode

class RandomBoard(Wall):
    def __init__(self,mode,x,y,width,height,limitWidth,limitHeight):
        super().__init__(x,y,width,height)
        self.limitWidth=limitWidth
        self.limitHeight=limitHeight
        self.ratio1=50/mode.width
        #top wall
        topWall=Wall(2*self.x,2*self.y,self.limitWidth-self.width,\
            self.height)
        #bottom wall
        bottomWall=Wall(2*self.x,mode.height-3*self.y,self.limitWidth-self.width,\
            self.height)
        #bottom left
        bottomLeft=Wall(2*self.x,2*self.y+0.6*self.limitHeight,self.width,\
            0.4*self.limitHeight)
        #top left
        topLeft=Wall(2*self.x,2*self.y,self.width,\
            0.4*self.limitHeight)
        #bottom right
        bottomRight=Wall(self.limitWidth,2*self.y+0.6*self.limitHeight,self.width,\
            0.4*self.limitHeight)
        #top right
        topRight=Wall(self.limitWidth,2*self.y,self.width,\
            0.4*self.limitHeight)
        self.board=[bottomRight,topRight,bottomLeft,topLeft,topWall,bottomWall]
        i=0
        while i<15:
            self.randomWalls(mode)
            i+=1
        self.dimensions=list()
        for wall in self.board:
            self.dimensions.append([wall.x,wall.y,wall.width,wall.height])
    def randomWalls(self,mode):
        maxX=random.randint(20*self.width,mode.limitWidth-20*self.width)
        maxY=random.randint(20*self.height,mode.limitHeight-20*self.height)
        wall=random.choice(["horizontal","vertical"])
        if wall=="horizontal":
            newWall=Wall(maxX,maxY,100,50)
        elif wall=="vertical":
            newWall=Wall(maxX,maxY,50,100)
        self.board.append(newWall)
    def drawBoard(self,canvas):
        for wall in self.board:
            wall.drawWall(canvas)
    def drawCells(self,mode):
        self.rows=int(((mode.limitHeight)+4*self.width)//50)
        self.cols=int(((mode.limitWidth)+4*self.height)//50)
        self.table=[[0]*self.cols for row in range(self.rows)]
        for wall in self.dimensions:
            for col in range(int(wall[0]),int(wall[0])+int(wall[2]),50):
                for row in range(int(wall[1]),int(wall[1])+int(wall[3]),50):
                    self.table[row//50][col//50]=1
        return self.table