from cmu_112_graphics import *
from pacman import *
from originalBoard import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Ghost class defines characteristics of ghosts, draws ghosts, 
# and defines movement
class Ghost(object):
    def __init__(self):
        self.speed=5
        self.x,self.y=0,0
        self.dx,self.dy=0,-1*self.speed,
        self.radius=10
        self.color=None
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

# follows the shortest path to get to Pac-Man
class Blinky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="red"
        self.start=(int(self.x)//5,int(self.y)//5)
        self.end=(int(mode.pacmanXPos)//5,int(mode.pacmanYPos)//5)
        self.screen=mode.gameBoard.drawCells(mode)
    # program attained from 
    # https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    def moveGhost(self,mode):
        # Returns a list of tuples as a path from the given start to the given end in the given maze
        # Create start and end node
        start_node = Node(None, self.start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.end)
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
                if node_position[0] > (len(self.screen) - 1) or node_position[0] < 0 or node_position[1] > (len(self.screen[len(self.screen)-1]) -1) or node_position[1] < 0:
                    continue
                # Make sure walkable terrain
                if self.screen[node_position[0]][node_position[1]] != 0:
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

class Inky(Ghost):
    def __init__(self):
        super().__init__()
        self.color="aqua"
    def moveGhost(self,mode):
        pass
    # follows the shortest path from Blinky to two tiles next to Pac-Man and 
    # doubles length in that direction

class Clyde(Ghost):
    def __init__(self):
        super().__init__()
        self.color="orange"
    def moveGhost(self,mode):
        pass
    # if less than 8 tiles away from Pac-Man, random mode but if not, same algorithm as Blinky