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
        mode.pacmanXPos,mode.pacmanYPos=mode.width/2,4*mode.height/5
        mode.ghostXPos,mode.ghostYPos=13*mode.width/30,9*mode.height/20
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
            for y in range(int(mode.wallY*10),int(mode.height-3*mode.wallHeight),int(mode.wallY *10)):
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