from cmu_112_graphics import *
from pacman import *
from ghost import *
from points import *
from originalBoard import *
from tkinter import *
import random

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# OriginalGameMode establishes original game mode with static board
# if time permits, may add randomly generated board without side scroll
class OriginalGameMode(Mode):
    def appStarted(mode):
        mode.count=0
        mode.inkyCount=0
        mode.blinkyCount=0

        mode.wallX,mode.wallY=mode.width/150,mode.height/100
        mode.wallWidth,mode.wallHeight=mode.width/150,mode.height/100
        mode.gameBoard=OriginalBoard(mode,mode.wallX,mode.wallY,\
            mode.wallWidth,mode.wallHeight)
        mode.maze=mode.gameBoard.drawCells()

        mode.radius=10
        mode.pointRadius=5
        mode.speed=5

        mode.points=[]
        mode.areaCoords=dict()
        mode.drawCoins()
        mode.freqX,mode.freqY=0,0

        mode.pacman=PacMan()
        mode.inky=Inky()
        mode.pinky=Pinky()
        mode.blinky=Blinky()
        mode.clyde=Clyde()

        mode.pacman.x,mode.pacman.y=mode.width/2,4*mode.height/5
        mode.inky.x,mode.inky.y=13*mode.width/30,7*mode.height/20
        mode.pinky.x,mode.pinky.y=2*mode.width/5,9*mode.height/20
        mode.blinky.x,mode.blinky.y=13*mode.width/30,9*mode.height/20
        mode.clyde.x,mode.clyde.y=7*mode.width/15,9*mode.height/20

        mode.pathInky=mode.inky.makePath(mode.maze,mode.freqX,mode.freqY)
        mode.pathBlinky=mode.blinky.makePath(mode.maze,mode.pacman.x,mode.pacman.y)

        mode.score=0
        mode.gameOver=False

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
        else:
            if event.key=="r":
                mode.appStarted()
                mode.gameOver=False

    def gameOverCheck(mode):
        if (mode.inky.x==mode.pacman.x and mode.inky.y==mode.pacman.y) or \
             (mode.pinky.x==mode.pacman.x and mode.pinky.y==mode.pacman.y) or \
                 (mode.blinky.x==mode.pacman.x and mode.blinky.y==mode.pacman.y)\
                      or (mode.clyde.x==mode.pacman.x and mode.clyde.y==mode.pacman.y):
                mode.gameOver=True
        i=0
        while i<len(mode.points):
            if ((mode.points[i].x-mode.pacman.x)**2+\
                (mode.points[i].y-mode.pacman.y)**2)**0.5\
                <mode.points[i].radius+mode.radius:
                mode.points.pop(i)
                mode.score+=1
                if len(mode.points)==0:
                    mode.gameOver=True
            i+=1

    def timerFired(mode):
        if mode.gameOver==False:
            mode.count+=1
            mode.inkyCount+=1

            mode.pacman.legalDirections=mode.legalPlaces(mode.pacman.x,mode.pacman.y)
            mode.pacman.movePacMan()
            
            if mode.inkyCount==10:
                mode.findMostPoints()
                mode.pathInky=mode.inky.makePath(mode.maze,mode.freqX,mode.freqY)
                if len(mode.pathInky)==2:
                    mode.pathInky=mode.inky.makePath(mode.maze,(int(mode.freqX)+2)%15,(int(mode.freqY)+2)%10)
                mode.inkyCount=0
            mode.inky.legalDirections=mode.legalPlaces(mode.inky.x,mode.inky.y)
            mode.inky.moveGhost(mode.pathInky)

            if mode.count>150:
                mode.pinky.legalDirections=mode.legalPlaces(mode.pinky.x,mode.pinky.y)
                mode.pinky.moveGhost(mode.pacman.x,mode.pacman.y)

            if mode.count>300:
                mode.blinkyCount+=1
                if mode.blinkyCount==10:
                    mode.pathBlinky=mode.blinky.makePath(mode.maze,mode.pacman.x,mode.pacman.y)
                    if len(mode.pathBlinky)==2:
                        mode.pathBlinky=mode.blinky.makePath(mode.maze,(int(mode.pacman.x)+2)%15,(int(mode.pacman.y)+2)%10)
                    mode.blinkyCount=0
                mode.blinky.legalDirections=mode.legalPlaces(mode.blinky.x,mode.blinky.y)
                mode.blinky.moveGhost(mode.pathBlinky)

            if mode.count>450:
                mode.clyde.legalDirections=mode.legalPlaces(mode.clyde.x,mode.clyde.y)
                mode.clyde.moveGhost((mode.pinky.x+50)%750,(mode.pinky.y+50)%500)
        
            mode.gameOverCheck()

        else:
            mode.pacman.speedSetter(0,0)

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
    
    def findMostPoints(mode):
        for row in range(0,int(mode.width),int(mode.width)//5):
            for col in range(0,mode.height,int(mode.width)//5):
                coords=(row,col,row+int(mode.width)//5,col+int(mode.width)//5)
                mode.areaCoords[coords]=0
        for coord in mode.areaCoords:
            for coin in mode.points:
                if (coin.x>=coord[0] and coin.x<=coord[2]) and (coin.y>=coord[1] \
                    and coin.y<=coord[3]):
                    mode.areaCoords[coord]+=1
        maxPoints=0
        maxCoord=(0,0,0,0)
        for coord in mode.areaCoords:
            if mode.areaCoords[coord]>=maxPoints:
                maxPoints=mode.areaCoords[coord]
                maxCoord=coord
        mode.freqX=(maxCoord[0]+maxCoord[2])//2
        mode.freqY=(maxCoord[1]+maxCoord[3])//2

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        if mode.gameOver==False:
            mode.gameBoard.drawBoard(canvas)
            for coin in mode.points:
                coin.drawPoints(canvas)
            mode.pacman.drawPacMan(canvas)
            mode.blinky.drawGhost(canvas)
            mode.pinky.drawGhost(canvas)
            mode.inky.drawGhost(canvas)
            mode.clyde.drawGhost(canvas)
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