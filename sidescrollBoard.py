from cmu_112_graphics import *
from wall import *
import random

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

#creates a randomly generated board

class SideScrollBoard(Wall):
    def __init__(self,mode,x,y,width,height):
        super().__init__(x,y,width,height)
        self.ratio1=50/mode.width
        #right wall
        rightWall=Wall(2*self.x,2*self.y,self.width,\
            1.5*(mode.height-4*self.height))
        #left wall
        leftWall=Wall(2*(mode.width-3*self.x),2*self.y,self.width,\
            1.5*(mode.height-4*self.height))
        #top wall
        topWall=Wall(2*self.x,2*self.y,2*(mode.width-4*self.width),\
            self.height)
        #bottom wall
        bottomWall=Wall(2*self.x,1.5*(mode.height-3*self.y),2*(mode.width-4*self.width),\
            self.height)
        self.board=[rightWall,leftWall,topWall,bottomWall]
        i=0
        while i < 10:
            x=random.randint(10,2*(mode.width-30))
            y=random.randint(10,2*(mode.width-20))
            wall=random.choice(["horizontal","vertical"])
            if wall=="horizontal":
                newWall=Wall(x,y,50,100)
            elif wall=="vertical":
                newWall=Wall(x,y,100,50)
            self.board.append(newWall)
            i+=1
        self.dimensions=set()
        for wall in self.board:
            self.dimensions.add((wall.x,wall.y,wall.width,wall.height))
    def drawBoard(self,canvas):
        for wall in self.board:
            wall.drawWall(canvas)
    def drawCells(self,mode):
        self.rows=mode.height//5
        self.cols=mode.width//5
        self.table=[[0]*self.cols for row in range(self.rows)]
        for wall in mode.gameBoard.dimensions:
            for row in range(int(wall[1])//5,int(wall[1])//5+int(wall[3])//5):
                for col in range(int(wall[0])//5,int(wall[0])//5+int(wall[2])//5):
                    pass #change when algorithm is complete