from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# Ghost class defines characteristics of ghosts, draws ghosts, 
# and defines movement
class Ghost(Mode):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.color=None
        self.radius=10
        self.url="http://labs.phaser.io/assets/games/pacman/sprites32.png"
    def drawGhost(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)
    def moveGhost(self):
        # each ghost will have its own algorithm to determine its
        # path around the maze, can be implemented in this method in each 
        # ghost subclass
        pass

class Blinky(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="red"
    def moveGhost(self):
        pass
    # follows the shortest path to get to Pac-Man

class Pinky(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="pink"
    def moveGhost(self):
        pass
    # follows the path to get to four tiles to the right or left of Pac-Man

class Inky(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="aqua"
    def moveGhost(self):
        pass
    # follows the shortest path from Blinky to two tiles next to Pac-Man and 
    # doubles length in that direction

class Clyde(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="orange"
    def moveGhost(self):
        pass
    # if less than 8 tiles away from Pac-Man, random mode but if not, same algorithm as Blinky