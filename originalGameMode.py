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
        mode.radius=10
        mode.pointRadius=5
        mode.speed=5

        mode.pacman=PacMan()
        mode.blinky=Blinky()
        mode.pinky=Pinky()
        mode.pacman.x,mode.pacman.y=mode.width/2,4*mode.height/5
        mode.pinky.x,mode.pinky.y=13*mode.width/30,7*mode.height/20

        mode.wallX,mode.wallY=mode.width/150,mode.height/100
        mode.wallWidth,mode.wallHeight=mode.width/150,mode.height/100
        mode.gameBoard=OriginalBoard(mode,mode.wallX,mode.wallY,\
            mode.wallWidth,mode.wallHeight)

        mode.points=[]
        mode.drawCoins()
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

    def timerFired(mode):
        if mode.gameOver==False:
            mode.pacman.legalDirections=mode.legalPlaces(mode.pacman.x,mode.pacman.y)
            mode.pacman.movePacMan()
            mode.pinky.legalDirections=mode.legalPlaces(mode.pinky.x,mode.pinky.y)
            mode.pinky.moveGhost(mode.pacman.x,mode.pacman.y)
            if mode.pinky.x==mode.pacman.x and mode.pinky.y==mode.pacman.y:
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

    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        if mode.gameOver==False:
            mode.gameBoard.drawBoard(canvas)
            for coin in mode.points:
                coin.drawPoints(canvas)
            mode.pacman.drawPacMan(canvas)
            mode.pinky.drawGhost(canvas)
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