from cmu_112_graphics import *
from pacman import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Ghost class defines characteristics of ghosts, draws ghosts, 
# and defines movement
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
    def moveGhost(self):
        # each ghost will have its own algorithm to determine its
        # path around the maze, can be implemented in this method in each 
        # ghost subclass
        pass
    def drawGhost(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)

# node class for a* path-finding for Blinky and Inky
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

# calculates shortest length from Inky to the 100X100 area with the most points
# astar attained from
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Inky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="aqua"
    def astar(self,maze,start,end):
        start=(int(start[0])//50,int(start[1])//50)
        end=(int(end[0])//50,int(end[1])//50)
        if(start[0] == end[0]) and (start[1] == end[1]):
            return (0,0)
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        open_list = []
        closed_list = []
        open_list.append(start_node)
        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            open_list.pop(current_index)
            closed_list.append(current_node)
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
                node_position = (current_node.position[0] + \
                    new_position[0], current_node.position[1] + new_position[1])
                if node_position[0] < 0 or node_position[1] < 0:
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)
            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                    ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue
                open_list.append(child)
    def makePath(self,maze,x,y):
        start=(self.x,self.y)
        end=(x,y)
        path=self.astar(maze,start,end)
        return path
    def moveGhost(self,path):
        startPath=path[0]
        target=path[1]
        if target[0]-startPath[0]==0:
            if startPath[1]<=target[1] or target[1]==0:
                self.currDirection="down"
            elif startPath[1]>target[1] or target[1]==10:
                self.currDirection="up"
        else:
            if startPath[0]<=target[0] or target[0]==0:
                self.currDirection="right"
            elif startPath[0]>target[0] or target[0]==15:
                self.currDirection="left"
        self.dirSetter()
        if self.currDirection in self.legalDirections:
            self.x+=self.dx
            self.y+=self.dy

# determines direction based on Pinky's relative position to Pac-Man
class Pinky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="pink"
    def moveGhost(self,x,y): #x,y are Pac-Man's position
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

# follows the shortest path to get to Pac-Man using a* for path-finding
# astar attained from
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Blinky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="red"
    def astar(self,maze,start,end):
        start=(int(start[0])//50,int(start[1])//50)
        end=(int(end[0])//50,int(end[1])//50)
        if(start[0] == end[0]) and (start[1] == end[1]):
            return (0,0)
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        open_list = []
        closed_list = []
        open_list.append(start_node)
        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            open_list.pop(current_index)
            closed_list.append(current_node)
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                node_position = (current_node.position[0] + \
                    new_position[0], current_node.position[1] + new_position[1])
                if node_position[0] < 0 or node_position[1] < 0:
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)
            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                    ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue
                open_list.append(child)
    def makePath(self,maze,x,y):
        start=(self.x,self.y)
        end=(x,y)
        path=self.astar(maze,start,end)
        return path
    def moveGhost(self,path):
        startPath=path[0]
        target=path[1]
        if target[0]-startPath[0]==0:
            if startPath[1]<=target[1] or target[1]==0:
                self.currDirection="down"
            elif startPath[1]>target[1] or target[1]==10:
                self.currDirection="up"
        else:
            if startPath[0]<=target[0] or target[0]==0:
                self.currDirection="right"
            elif startPath[0]>target[0] or target[0]==15:
                self.currDirection="left"
        self.dirSetter()
        if self.currDirection in self.legalDirections:
            self.x+=self.dx
            self.y+=self.dy

# follows ghost closest to Pac-Man
class Clyde(Ghost):
    def __init__(self):
        super().__init__()
        self.color="orange"
        self.distances=set()
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