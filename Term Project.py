from cmu_112_graphics import *
from tkinter import *
import random

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
    def mousePressed(mode):
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

class Pinky(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="pink"

class Inky(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="aqua"

class Clyde(Ghost):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color="orange"

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
        self.ratio1=2/15
        self.ratio2=3/10
        self.ratio3=7/15
        self.ratio4=11/15
        self.ratio5=4/5
        #1
        wall11=Wall(self.x,self.y,self.width,self.height)
        #5
        wall51=Wall(self.x+self.ratio1*mode.width,self.y,self.width*2,\
            self.height/5)
        wall52=Wall(self.x+self.ratio1*mode.width,self.y+mode.height/10,\
            self.width,2*self.height/5)
        wall53=Wall(self.x+mode.width/5,self.y+mode.height/5,self.width,\
            2*self.height/5)
        wall54=Wall(self.x+self.ratio1*mode.width,self.y+2*mode.height/5,\
            self.width*2,self.height/5)
        #dash
        wallDash=Wall(self.x+self.ratio2*mode.width,self.y+mode.height/5,\
            self.width*2,self.height//5)
        #1
        wall12=Wall(self.x+self.ratio3*mode.width,self.y,self.width,self.height)
        #1
        wall13=Wall(self.x+2*self.ratio2*mode.width,self.y,self.width,\
            self.height)
        #2
        wall21=Wall(self.x+self.ratio4*mode.width,self.y,self.width*2,\
            self.height//5)
        wall22=Wall(self.x+self.ratio5*mode.width,self.y+mode.height/10,\
            self.width,2*self.height//5)
        wall23=Wall(self.x+self.ratio4*mode.width,self.y+mode.height/5,\
            self.width,2*self.height//5)
        wall24=Wall(self.x+self.ratio4*mode.width,self.y+2*mode.height/5,\
            self.width*2,self.height//5)
        #right wall
        rightWall=Wall(10,10,5,475)
        #left wall
        leftWall=Wall(735,10,5,475)
        #top wall
        topWall=Wall(10,10,730,5)
        #bottom wall
        bottomWall=Wall(10,485,730,5)
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
        mode.pacmanXPos,mode.pacmanYPos=mode.width//2,4*mode.height//5
        mode.ghostXPos,mode.ghostYPos=325,225
        mode.wallX,mode.wallY=50,100
        mode.wallWidth,mode.wallHeight=50,250
        mode.dxPos,mode.dyPos=-5,0
        mode.direction="left"
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
                mode.dxPos=+5
                mode.movePacMan(mode.dxPos,0)
            elif event.key=="Left":
                mode.direction="left"
                mode.dxPos=-5
                mode.movePacMan(mode.dxPos,0)
            elif event.key=="Up":
                mode.direction="up"
                mode.dyPos=-5
                mode.movePacMan(0,mode.dyPos)
            elif event.key=="Down":
                mode.direction="down"
                mode.dyPos=+5
                mode.movePacMan(0,mode.dyPos)
        else:
            if event.key=="r":
                mode.appStarted()
                mode.gameOver=False

    def timerFired(mode):
        if mode.gameOver==False:
            if mode.illegalPlaces("y"):
                mode.movePacMan(mode.dxPos,0)
            if mode.illegalPlaces("x"):
                mode.movePacMan(0,mode.dyPos)
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
            mode.movePacMan(0,0)

    def movePacMan(mode,dx,dy):
        mode.dxPos=dx
        mode.dyPos=dy

    def illegalPlaces(mode,direction):
        for wall in mode.gameBoard.dimensions:
            if direction=="y":
                if mode.pacmanXPos+mode.radius>wall[0] and \
                    mode.pacmanXPos-mode.radius<wall[0]+wall[2]:
                    if (mode.pacmanYPos-mode.radius==wall[1]+wall[3] and \
                        mode.direction=="up") or \
                            (mode.pacmanYPos+mode.radius==wall[1] and \
                                mode.direction=="down"):
                                return True
            elif direction=="x":
                if mode.pacmanYPos+mode.radius>wall[1] and \
                    mode.pacmanYPos-mode.radius<wall[1]+wall[3]:
                    if (mode.pacmanXPos-mode.radius==wall[0]+wall[2] and \
                        mode.direction=="left") or \
                            (mode.pacmanXPos+mode.radius==wall[0] and \
                                mode.direction=="right"):
                                return True

    def drawCoins(mode):
        for x in range(50,750,50):
            for y in range(50,500,50):
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
            Blinky(mode.ghostXPos-30,mode.ghostYPos).drawGhost(canvas)
            Pinky(mode.ghostXPos-10,mode.ghostYPos).drawGhost(canvas)
            Inky(mode.ghostXPos+10,mode.ghostYPos).drawGhost(canvas)
            Clyde(mode.ghostXPos+30,mode.ghostYPos).drawGhost(canvas)
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
