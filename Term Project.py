from cmu_112_graphics import *
from tkinter import *
import random

#CITE cmu graphics and tkinter

# CITATION: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# #subclassingModalApp
class SplashScreenMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, mode.height/5, \
            text='Pac Man', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/3, \
            text='Press space to start!',font=font,fill="white")

    def keyPressed(mode,event):
        if event.key=="Space":
            mode.app.setActiveMode(mode.app.gameMode)

    #will add buttons to determine mode
    def mousePressed(mode,event):
        pass

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
        wallDash=Wall(10*self.x+45*self.width,20*self.y+20*self.width,\
            20*self.width,10*self.height)
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

# Points class defines characteristics of points and draws points
class Points(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.radius=5
    def drawPoints(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill="orange")

# OriginalGameMode establishes original game mode with static board
# if time permits, may add randomly generated board without side scroll
class OriginalGameMode(Mode):
    def appStarted(mode):
        mode.radius=10
        mode.pointRadius=5
        mode.pacmanXPos,mode.pacmanYPos=mode.width/2,4*mode.height/5
        mode.ghostXPos,mode.ghostYPos=325,225
        mode.wallX,mode.wallY=mode.width/150,mode.height/100
        mode.wallWidth,mode.wallHeight=mode.width/150,mode.height/100
        mode.speed=5
        mode.dxPos,mode.dyPos=-1*mode.speed,0
        mode.currDirection="left"
        mode.direction=mode.currDirection
        mode.legalDirections=["up","right","down","left"]
        mode.gameBoard=OriginalBoard(mode,mode.wallX,mode.wallY,\
            mode.wallWidth,mode.wallHeight)
        mode.points=[]
        mode.drawCoins()
        mode.score=0
        mode.gameOver=False

    def keyPressed(mode,event):
        if mode.gameOver==False:
            if event.key=="Right":
                mode.direction="right"
            elif event.key=="Left":
                mode.direction="left"
            elif event.key=="Up":
                mode.direction="up"
            elif event.key=="Down":
                mode.direction="down"
            if mode.direction in mode.legalDirections:
                mode.currDirection=mode.direction
                mode.movePacMan(mode.currDirection)
            else:
                mode.movePacMan(mode.currDirection)
        else:
            if event.key=="r":
                mode.appStarted()
                mode.gameOver=False

    def movePacMan(mode,direction):
        if direction=="right":
            mode.dirPacMan(mode.speed,0)
        elif direction=="left":
            mode.dirPacMan(-1*mode.speed,0)
        elif direction=="up":
            mode.dirPacMan(0,-1*mode.speed)
        elif direction=="down":
            mode.dirPacMan(0,mode.speed)

    def timerFired(mode):
        if mode.gameOver==False:
            mode.legalDirections=mode.legalPlaces()
            if mode.currDirection in mode.legalDirections:
                mode.pacmanXPos+=mode.dxPos
                mode.pacmanYPos+=mode.dyPos
            i=0
            while i<len(mode.points):
                if ((mode.points[i].x-mode.pacmanXPos)**2+\
                    (mode.points[i].y-mode.pacmanYPos)**2)**0.5\
                    <mode.points[i].radius+mode.radius:
                    mode.points.pop(i)
                    mode.score+=1
                    if len(mode.points)==0:
                        mode.gameOver=True
                i+=1
        else:
            mode.dirPacMan(0,0)

    def dirPacMan(mode,dx,dy):
        mode.dxPos=dx
        mode.dyPos=dy

    def legalPlaces(mode):
        mode.legalDirections=["up","right","down","left"]
        for wall in mode.gameBoard.dimensions:
            if mode.pacmanXPos+mode.radius>wall[0] and \
                mode.pacmanXPos-mode.radius<wall[0]+wall[2]:
                if (mode.pacmanYPos>wall[1]+wall[3] and mode.pacmanYPos-mode.radius<=wall[1]+wall[3]):
                    if "up" in mode.legalDirections:
                        mode.legalDirections.remove("up")
                elif (mode.pacmanYPos<wall[1] and mode.pacmanYPos+mode.radius>=wall[1]):
                    if "down" in mode.legalDirections:
                        mode.legalDirections.remove("down")
            if mode.pacmanYPos+mode.radius>wall[1] and \
                mode.pacmanYPos-mode.radius<wall[1]+wall[3]:
                if (mode.pacmanXPos>wall[0]+wall[2] and mode.pacmanXPos-mode.radius<=wall[0]+wall[2]):
                    if "left" in mode.legalDirections:
                        mode.legalDirections.remove("left")
                elif (mode.pacmanXPos<wall[0] and mode.pacmanXPos+mode.radius>=wall[0]):
                    if "right" in mode.legalDirections:
                        mode.legalDirections.remove("right")
        return mode.legalDirections

    def drawCoins(mode):
        for x in range(int(mode.wallX*10),int(mode.width-3*mode.wallWidth),int(mode.wallX*10)):
            for y in range(int(mode.wallY*10),int(mode.height-3*mode.wallHeight),int(mode.wallY*10)):
                mode.points.append(Points(x,y))
        i=0
        while i < len(mode.points):
            for wall in mode.gameBoard.dimensions:
                if (mode.points[i].x>wall[0] and \
                    mode.points[i].x<wall[0]+wall[2] and \
                        mode.points[i].y<wall[1]+wall[3] and \
                            mode.points[i].y>wall[1]):
                                    mode.points.pop(i)
            i+=1

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        if mode.gameOver==False:
            mode.gameBoard.drawBoard(canvas)
            for coin in mode.points:
                coin.drawPoints(canvas)
            Blinky(mode.ghostXPos-mode.width/25,mode.ghostYPos).drawGhost(canvas)
            Pinky(mode.ghostXPos-mode.width/75,mode.ghostYPos).drawGhost(canvas)
            Inky(mode.ghostXPos+mode.width/75,mode.ghostYPos).drawGhost(canvas)
            Clyde(mode.ghostXPos+mode.width/25,mode.ghostYPos).drawGhost(canvas)
            PacMan(mode.pacmanXPos,mode.pacmanYPos).drawPacMan(canvas)
            canvas.create_text(mode.width//2,15,text=f'Score:{mode.score}',\
                fill="white")
        else:
            font = 'Arial 26 bold'
            canvas.create_text(mode.width//2,mode.height//2, 
            text='Game Over!', font=font, fill="white")
            canvas.create_text(mode.width//2,3*mode.height//4, 
            text=f'Your score: {mode.score}',font=font,fill="white")
            canvas.create_text(mode.width//2,5*mode.height//6, 
            text='Press r to restart',font=font,fill="white")

# SidescrollGameMode will establish a randomly generated board every single time
# a new game starts, will allow the user to travel off screen
class SidescrollGameMode(Mode):
    pass

# CreativeMode will allow the user to create their own map, will play like
# original mode
class CreativeMode(Mode):
    pass

# MultiplayerMode will allow two users to player, one as ghost
# can play in original mode
class MultiplayerMode(Mode):
    pass

# from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# #subclassingModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode=SplashScreenMode()
        app.gameMode=OriginalGameMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay=50

app = MyModalApp(width=750, height=500)
