from cmu_112_graphics import *
from tkinter import *
import random

class SplashScreenMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, \
            text='Pac Man', font=font, fill="white")
        canvas.create_text(mode.width/2, 200, \
            text='Press space to start!',font=font,fill="white")

    def keyPressed(mode,event):
        if event.key=="Space":
            mode.app.setActiveMode(mode.app.gameMode)

class PacMan(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.radius=10
        self.color="yellow"
        self.url="http://labs.phaser.io/assets/games/pacman/sprites32.png"
    def drawPacMan(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)

class Ghost(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.color=None
        self.radius=10
        self.url="http://labs.phaser.io/assets/games/pacman/sprites32.png"
    def drawGhost(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill=self.color)

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
        #1
        wall11=Wall(self.x,self.y,self.width,self.height)
        #5
        wall51=Wall(self.x+100,self.y,self.width*2,self.height//5)
        wall52=Wall(self.x+100,self.y+50,self.width,2*self.height//5)
        wall53=Wall(self.x+150,self.y+100,self.width,2*self.height//5)
        wall54=Wall(self.x+100,self.y+200,self.width*2,self.height//5)
        #dash
        wallDash=Wall(self.x+225,self.y+100,self.width*2,self.height//5)
        #1
        wall12=Wall(self.x+350,self.y,self.width,self.height)
        #1
        wall13=Wall(self.x+450,self.y,self.width,self.height)
        #2
        wall21=Wall(self.x+550,self.y,self.width*2,self.height//5)
        wall22=Wall(self.x+600,self.y+50,self.width,2*self.height//5)
        wall23=Wall(self.x+550,self.y+100,self.width,2*self.height//5)
        wall24=Wall(self.x+550,self.y+200,self.width*2,self.height//5)
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

class Points(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.radius=5
    def drawPoints(self,canvas):
        canvas.create_oval(self.x-self.radius,self.y-self.radius,\
            self.x+self.radius,self.y+self.radius,fill="orange")

class OriginalGameMode(Mode):
    def appStarted(mode):
        mode.radius=10
        mode.pacmanXPos,mode.pacmanYPos=mode.width//2,4*mode.height//5
        mode.ghostXPos,mode.ghostYPos=325,225
        mode.wallX,mode.wallY=50,100
        mode.wallWidth,mode.wallHeight=50,250
        mode.dxPos,mode.dyPos=-5,0
        mode.direction="left"
        mode.gameBoard=OriginalBoard(mode.wallX,mode.wallY,\
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

    def timerFired(mode):
        if mode.legalPlaces("y"):
            mode.movePacMan(mode.dxPos,0)
        if mode.legalPlaces("x"):
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

    def movePacMan(mode,dx,dy):
        mode.dxPos=dx
        mode.dyPos=dy

    def legalPlaces(mode,direction):
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
            text=f'Your score:{mode.score}',font=font,fill="white")
            canvas.create_text(mode.width//2,5*mode.height//6, 
            text='Press r to restart',font=font,fill="white")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode=SplashScreenMode()
        app.gameMode=OriginalGameMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay=50

app = MyModalApp(width=750, height=500)
