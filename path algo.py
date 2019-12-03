from cmu_112_graphics import *
# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# this file is a test file for the algorithm, currently not running in the game

# node class for a* path-finding for Blinky
# program attained from 
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

class Node(object):
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return (self.position == other.position)

# Returns a list of tuples as a path from the given start to the given end in the given maze
def astar(maze, start, end):
    start=(int(start[0])//50,int(start[1])//50)
    end=(int(end[0])//50,int(end[1])//50)
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)
        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)

# Wall class defines characteristics of walls and draws walls
class Wall(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color="blue"
    def drawWall(self,canvas):
        canvas.create_rectangle(self.x,self.y,\
            self.x+self.width,self.y+self.height,fill=self.color,width=0)

class OriginalBoard(Wall):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.ratio1=50/750
        #right wall
        rightWall=Wall(2*self.x,2*self.y,self.width,\
            500-4*self.height)
        #left wall
        leftWall=Wall(750-3*self.x,2*self.y,self.width,\
            500-4*self.height)
        #top wall
        topWall=Wall(2*self.x,2*self.y,750-4*self.width,\
            self.height)
        #bottom wall
        bottomWall=Wall(2*self.x,500-3*self.y,750-4*self.width,\
            self.height)
        #1
        wall11=Wall(10*self.x,20*self.y,10*self.width,50*self.height)
        #5
        wall51=Wall(10*self.x+2*self.ratio1*750,20*self.y,20*self.width,\
            10*self.height)
        wall52=Wall(10*self.x+2*self.ratio1*750,20*self.y+10*self.height,\
            10*self.width,20*self.height)
        wall53=Wall(20*self.x+2*self.ratio1*750,20*self.y+20*self.height,10*self.width,\
            20*self.height)
        wall54=Wall(10*self.x+2*self.ratio1*750,20*self.y+40*self.height,20*self.width,\
            10*self.height)
        #dash
        wallDash=Wall(10*self.x+50*self.width,20*self.y+20*self.width,\
            10*self.width,10*self.height)
        #1
        wall12=Wall(80*self.x,20*self.y,10*self.width,50*self.height)
        #1
        wall13=Wall(100*self.x,20*self.y,10*self.width,50*self.height)
        #2
        wall21=Wall(100*self.x+2*self.ratio1*750,20*self.y,20*self.width,\
            10*self.height)
        wall22=Wall(110*self.x+2*self.ratio1*750,20*self.y+10*self.height,\
            10*self.width,20*self.height)
        wall23=Wall(100*self.x+2*self.ratio1*750,20*self.y+20*self.height,10*self.width,\
            20*self.height)
        wall24=Wall(100*self.x+2*self.ratio1*750,20*self.y+40*self.height,20*self.width,\
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

from tkinter import *
from ghost import *
from points import *
import random

class OriginalGameMode(Mode):
    def appStarted(mode):
        mode.count=0
        mode.pointRadius=5

        mode.blinky=Blinky()
        mode.inky=Inky()

        mode.blinky.x,mode.blinky.y=50,50
        mode.inky.x,mode.inky.y=350,400

        mode.wallX,mode.wallY=mode.width/150,mode.height/100
        mode.wallWidth,mode.wallHeight=mode.width/150,mode.height/100
        mode.gameBoard=OriginalBoard(mode.wallX,mode.wallY,\
            mode.wallWidth,mode.wallHeight)
        mode.board=mode.gameBoard.drawCells()

        mode.points=[]
        mode.drawCoins()

        mode.start=(mode.blinky.y,mode.blinky.x)
        mode.end=(mode.inky.y,mode.inky.x)
        mode.path=astar(mode.board,mode.start,mode.end)
    
    def keyPressed(mode,event):
        if event.key=="Right":
            mode.inky.x+=5
        elif event.key=="Left":
            mode.inky.x-=5
        elif event.key=="Up":
            mode.inky.y-=5
        elif event.key=="Down":
            mode.inky.y+=5

    def timerFired(mode):
        mode.count+=1
        mode.startPath=mode.path[0]
        mode.target=mode.path[1]
        if mode.target[0]-mode.startPath[0]==0:
            if mode.startPath[1]<=mode.target[1]:
                mode.blinky.x+=10
            else:
                mode.blinky.x-=10
        else:
            if mode.startPath[0]<=mode.target[0]:
                mode.blinky.y+=10
            else:
                mode.blinky.y-=10
        if mode.count==10:
            mode.start=(mode.blinky.y,mode.blinky.x)
            mode.end=(mode.inky.y,mode.inky.x)
            mode.path=astar(mode.board,mode.start,mode.end)
            mode.count=0

    def drawCoins(mode):
        for x in range(int(mode.wallX*10),int(mode.width-3*mode.wallWidth),int(mode.wallX*10)):
            for y in range(int(mode.wallY*10),int(mode.height-3*mode.wallHeight),int(mode.wallY*10)):
                mode.points.append(Points(x,y))
                for wall in mode.gameBoard.dimensions:
                    for point in mode.points:
                        if (point.x+mode.pointRadius>=wall[0] and \
                            point.x-mode.pointRadius<=wall[0]+wall[2] and \
                                point.y-mode.pointRadius<=wall[1]+wall[3] and \
                                    point.y+mode.pointRadius>=wall[1]):
                                    mode.points.remove(point)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        mode.gameBoard.drawBoard(canvas)
        for coin in mode.points:
                coin.drawPoints(canvas)
        mode.blinky.drawGhost(canvas)
        mode.inky.drawGhost(canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode=OriginalGameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay=1000

app = MyModalApp(width=750, height=500)