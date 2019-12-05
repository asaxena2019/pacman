from cmu_112_graphics import *
from pacman import *
from ghostScroll import *
from points import *
from randomBoard import *
from tkinter import *
import random

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# SidescrollGameMode will establish a randomly generated board every single time
# a new game starts, will allow the user to travel off screen
class SideScrollGameMode(Mode):
    def appStarted(mode):
        mode.count=0
        mode.timer=3

        mode.wallX,mode.wallY=mode.width/150,mode.height/100
        mode.wallWidth,mode.wallHeight=mode.width/150,mode.height/100
        mode.limitWidth=(2*mode.width-4*mode.wallX)
        mode.limitHeight=(mode.height-4*mode.wallY)
        mode.gameBoard=RandomBoard(mode,mode.wallX,mode.wallY,\
            mode.wallWidth,mode.wallHeight,mode.limitWidth,mode.limitHeight)
        mode.maze=mode.gameBoard.drawCells(mode)

        mode.radius=10
        mode.pointRadius=5
        mode.speed=5
        mode.scrollX=0
        mode.margin=100

        mode.points=[]
        mode.areaCoords=dict()
        mode.drawCoins()
        mode.freqX,mode.freqY=0,0

        mode.pacman=PacMan()
        mode.inky=Inky()
        mode.pinky=Pinky()
        mode.blinky=Blinky()
        mode.clyde=Clyde()
        mode.ghosts=[mode.inky,mode.pinky,mode.blinky,mode.clyde]
        mode.establishPlayerCoords()

        mode.lives=[]
        for i in range(3):
            life=PacMan()
            life.x,life.y=(i+1)*25,15
            mode.lives.append(life)
       
        mode.score=0
        mode.gameOver=False
        mode.mute=False

    def keyPressed(mode,event):
        if mode.gameOver==False:
            if event.key=="Right":
                mode.pacman.direction="right"
            elif event.key=="Left":
                mode.pacman.direction="left"
            elif event.key=="Up":
                mode.pacman.direction="up"
            elif event.key=="Down":
                mode.pacman.direction="down"
            elif event.key=="r":
                mode.appStarted()
                mode.gameOver=False
            elif event.key=="m":
                mode.mute=True
            elif event.key=="u":
                mode.mute=False
            elif event.key=="h":
                mode.appStarted()
                mode.app.setActiveMode(mode.app.splashScreenMode)
        else:
            if event.key=="r":
                mode.appStarted()
                mode.gameOver=False
    
    def mousePressed(mode,event):
        if mode.gameOver==True:
            if event.x>550 and event.x<700 and event.y>450 and event.y<475:
                mode.app.setActiveMode(mode.app.splashScreenMode)
                mode.appStarted()
    
    # from 
    # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    def makePlayerVisible(mode):
        if (mode.pacman.x < mode.scrollX + mode.margin) and mode.pacman.currDirection=="left":
            mode.scrollX = mode.pacman.x - mode.margin
        elif (mode.pacman.x > mode.scrollX + mode.width - mode.margin) and mode.pacman.currDirection=="right":
            mode.scrollX = mode.pacman.x - mode.width + mode.margin
        else:
            mode.scrollX=0

    def establishPlayerCoords(mode):
        mode.pacman.x,mode.pacman.y=mode.width/2,4*mode.height/5
        mode.inky.x,mode.inky.y=mode.width/2,75
        mode.pinky.x,mode.pinky.y=mode.width/2,50
        mode.blinky.x,mode.blinky.y=mode.width/2-50,50
        mode.clyde.x,mode.clyde.y=mode.width/2+50,50

    def distance(mode,w,x,y,z):
        return ((w-x)**2+(y-z)**2)**0.5

    def portal(mode):
        if mode.pacman.x+mode.radius==mode.width:
                mode.pacman.x=mode.radius
        elif mode.pacman.x-mode.radius==0:
            mode.pacman.x=mode.width-mode.radius

    def timerSetter(mode):
        if mode.count==0:
            mode.timer=3
        elif mode.count==20:
            mode.timer=2
        elif mode.count==40:
            mode.timer=1
    
    def movePac(mode):
        mode.pacman.legalDirections=\
            mode.legalPlaces(mode.pacman.x,mode.pacman.y)
        mode.pacman.movePacMan()

    def moveInky(mode):
        mode.inky.legalDirections=mode.legalPlaces(mode.inky.x,mode.inky.y)
        mode.inky.moveGhost(mode.ghosts,mode.pacman.x,mode.pacman.y)
    
    def moveBlinky(mode):
        mode.blinky.legalDirections=\
            mode.legalPlaces(mode.blinky.x,mode.blinky.y)
        mode.blinky.moveGhost(mode.ghosts,mode.pacman.x,mode.pacman.y)

    def movePinky(mode):
        mode.pinky.legalDirections=mode.legalPlaces(mode.pinky.x,mode.pinky.y)
        mode.pinky.moveGhost(mode.ghosts,mode.pacman.x,mode.pacman.y)

    def moveClyde(mode):
        mode.clyde.legalDirections=mode.legalPlaces(mode.clyde.x,mode.clyde.y)
        mode.clyde.moveGhost(mode.ghosts,mode.pacman.x,mode.pacman.y)

    def timerFired(mode):
        if mode.gameOver==False:
            mode.timerSetter()
            mode.count+=1
            if mode.count>60:
                mode.movePac()
                mode.makePlayerVisible()
                mode.moveInky()
                if mode.count>300:
                    mode.moveBlinky()
                if mode.count>600:
                    mode.moveClyde()
                if mode.count>900:
                    mode.movePinky()
                mode.portal()
                mode.gameOverCheck()
        else: mode.pacman.speedSetter(0,0)

    def legalPlaces(mode,x,y):
        legalDirections=["up","right","down","left"]
        for wall in mode.gameBoard.dimensions:
            if x+mode.radius>wall[0] and \
                x-mode.radius<wall[0]+wall[2]:
                if (y>wall[1]+wall[3] and y-mode.radius<=wall[1]+wall[3]):
                    if "up" in legalDirections:
                        legalDirections.remove("up")
                elif (y<wall[1] and y+mode.radius>=wall[1]):
                    if "down" in legalDirections:
                        legalDirections.remove("down")
            if y+mode.radius>wall[1] and \
                y-mode.radius<wall[1]+wall[3]:
                if (x>wall[0]+wall[2] and x-mode.radius<=wall[0]+wall[2]):
                    if "left" in legalDirections:
                        legalDirections.remove("left")
                elif (x<wall[0] and x+mode.radius>=wall[0]):
                    if "right" in legalDirections:
                        legalDirections.remove("right")
        return legalDirections

    def gameOverCheck(mode):
        for ghost in mode.ghosts:
            if mode.mute==False:
                if mode.distance(ghost.x,mode.pacman.x,ghost.y,mode.pacman.y)\
                    <=mode.radius:
                    mode.lives.pop()
                    mode.establishPlayerCoords()
                    mode.count=0
                    mode.blinkyCount=0
                    mode.inkyCount=0
        if len(mode.lives)==0:
            mode.gameOver=True
        i=0
        while i<len(mode.points):
            if mode.distance(mode.points[i].x,mode.pacman.x,mode.points[i].y,\
                mode.pacman.y)<mode.points[i].radius+mode.radius:
                mode.points.pop(i)
                mode.score+=1
                if len(mode.points)==0:
                    mode.gameOver=True
            i+=1

    def drawCoins(mode):
        for x in range(int(mode.wallX*10),\
            int(mode.limitWidth+mode.wallWidth),int(mode.wallX*10)):
            for y in range(int(mode.wallY*10),\
                int(mode.limitHeight+mode.wallHeight),int(mode.wallY*10)):
                mode.points.append(Points(x,y))
                for wall in mode.gameBoard.dimensions:
                    for point in mode.points:
                        if (point.x+mode.pointRadius>=wall[0] and \
                            point.x-mode.pointRadius<=wall[0]+wall[2] and \
                                point.y-mode.pointRadius<=wall[1]+wall[3] and \
                                    point.y+mode.pointRadius>=wall[1]):
                                    mode.points.remove(point)
    
    def findMostPoints(mode):
        for row in range(0,int(mode.width),int(mode.width)//5):
            for col in range(0,mode.height,int(mode.width)//5):
                coords=(row,col,row+int(mode.width)//5,col+int(mode.width)//5)
                mode.areaCoords[coords]=0
        for coord in mode.areaCoords:
            for coin in mode.points:
                if (coin.x>=coord[0] and coin.x<=coord[2]) and\
                    (coin.y>=coord[1] and coin.y<=coord[3]):
                    mode.areaCoords[coord]+=1
        maxPoints=0
        maxCoord=(0,0,0,0)
        for coord in mode.areaCoords:
            if mode.areaCoords[coord]>=maxPoints:
                maxPoints=mode.areaCoords[coord]
                maxCoord=coord
        mode.freqX=(maxCoord[0]+maxCoord[2])//2
        mode.freqY=(maxCoord[1]+maxCoord[3])//2

    def drawGame(mode,canvas):
        for wall in mode.gameBoard.board:
            wall.x-=mode.scrollX
        for wall in mode.gameBoard.dimensions:
            wall[0]-=mode.scrollX
        mode.gameBoard.drawBoard(canvas)
        for coin in mode.points:
            coin.x-=mode.scrollX
            coin.drawPoints(canvas)
        for life in mode.lives:
            life.drawPacMan(canvas)
        mode.pacman.x-=mode.scrollX
        mode.pacman.drawPacMan(canvas)
        mode.blinky.x-=mode.scrollX
        mode.blinky.drawGhost(canvas)
        mode.pinky.x-=mode.scrollX
        mode.pinky.drawGhost(canvas)
        mode.inky.x-=mode.scrollX
        mode.inky.drawGhost(canvas)
        mode.clyde.x-=mode.scrollX
        mode.clyde.drawGhost(canvas)

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        if mode.gameOver==False:
            mode.drawGame(canvas)
            canvas.create_text(mode.width//2,15,text=f'Score:{mode.score}',\
                font='Courier 18 bold',fill="white")
            if mode.count<60:
                canvas.create_text\
                    (13*mode.width/30,9*mode.height/20,text=f'{mode.timer}',\
                font='Courier 50 bold',fill="white")
            if mode.mute==True:
                canvas.create_text(mode.width-50,15,text='Mute',\
                font='Courier 18 bold',fill="white")
        else:
            font = 'Courier 26 bold'
            if len(mode.points)==0:
                canvas.create_text(mode.width//2,mode.height//2, 
                text='Game Over! You won!', font=font, fill="white")
            else:
                canvas.create_text(mode.width//2,mode.height//2, 
                text='Game Over! You lost!', font=font, fill="white")
            canvas.create_text(mode.width//2,3*mode.height//4,\
                 text=f'Your score: {mode.score}',font=font,fill="white")
            canvas.create_text(mode.width//2,5*mode.height//6,\
                text='Press r to restart',font=font,fill="white")
            canvas.create_rectangle(550,450,700,475,fill="blue")
            canvas.create_text(625,463,text='Home',font='Courier 14 bold',\
                fill="white")