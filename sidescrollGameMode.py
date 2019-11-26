from cmu_112_graphics import *
from pacman import *
from ghost import *
from points import *
from sidescrollBoard import *
from tkinter import *
import random

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# SidescrollGameMode will establish a randomly generated board every single time
# a new game starts, will allow the user to travel off screen
class SideScrollGameMode(Mode):
    def appStarted(mode):
        mode.radius=10
        mode.pointRadius=5
        mode.margin=50
        mode.scrollX=0
        mode.scrollY=0
        mode.pacmanXPos,mode.pacmanYPos=mode.width/2,4*mode.height/5
        mode.pinkyGhostXPos,mode.pinkyGhostYPos=13*mode.width/30,7*mode.height/20
        mode.blinkyGhostXPos,mode.blinkyGhostYPos=13*mode.width/30,9*mode.height/20
        mode.inkyGhostXPos,mode.inkyGhostYPos=13*mode.width/30+30,9*mode.height/20
        mode.clydeGhostXPos,mode.clydeGhostYPos=13*mode.width/30-30,9*mode.height/20
        mode.wallX,mode.wallY=mode.width/150,mode.height/100
        mode.wallWidth,mode.wallHeight=mode.width/150,mode.height/100
        mode.speed=5
        mode.dxPacPos,mode.dyPacPos=-1*mode.speed,0
        mode.dxPinkyPos,mode.dyPinkyPos=1*mode.speed,0
        mode.pacCurrDirection="left"
        mode.pinkyCurrDirection="up"
        mode.pacDirection=mode.pacCurrDirection
        mode.pinkDirection=mode.pinkyCurrDirection
        mode.legalPacDirections=["up","right","down","left"]
        mode.legalPinkyDirections=["up","right","down","left"]
        mode.gameBoard=SideScrollBoard(mode,mode.wallX,mode.wallY,\
            mode.wallWidth,mode.wallHeight)
        mode.points=[]
        mode.drawCoins()
        mode.score=0
        mode.gameOver=False

    # from 
    # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
    def makePlayerVisible(mode):
        if (mode.pacmanXPos < mode.scrollX + mode.margin):
            mode.scrollX = mode.pacmanXPos - mode.margin
        if (mode.pacmanXPos > mode.scrollX + mode.width - mode.margin):
            mode.scrollX = mode.pacmanXPos - mode.width + mode.margin
        if (mode.pacmanYPos < mode.scrollY + mode.margin):
            mode.scrollY = mode.pacmanYPos - mode.margin
        if (mode.pacmanXPos > mode.scrollY + mode.height - mode.margin):
            mode.scrollY = mode.pacmanYPos - mode.height + mode.margin

    def keyPressed(mode,event):
        if mode.gameOver==False:
            if event.key=="Right":
                mode.pacDirection="right"
            elif event.key=="Left":
                mode.pacDirection="left"
            elif event.key=="Up":
                mode.pacDirection="up"
            elif event.key=="Down":
                mode.pacDirection="down"
            mode.setPinkyDir()
            if mode.pacDirection in mode.legalPacDirections:
                mode.pacCurrDirection=mode.pacDirection
                mode.movePlayer(mode.pacCurrDirection,"pac")
            else:
                mode.movePlayer(mode.pacCurrDirection,"pac")
        else:
            if event.key=="r":
                mode.appStarted()
                mode.gameOver=False
    
    # will move to moveGhost method in Pinky class after bugs are removed 
    # and tested
    def setPinkyDir(mode):
        if mode.pacCurrDirection=="right":
            mode.pinkyCurrDirection="left"
        elif mode.pacCurrDirection=="left":
            mode.pinkyCurrDirection=="right"
        elif mode.pacCurrDirection=="up":
            mode.pinkyCurrDirection=="down"
        elif mode.pacCurrDirection=="down":
            mode.pinkyCurrDirection=="up"

    def movePlayer(mode,direction,name):
        if direction=="right":
            mode.dirSetter(name,mode.speed,0)
        elif direction=="left":
            mode.dirSetter(name,-1*mode.speed,0)
        elif direction=="up":
            mode.dirSetter(name,0,-1*mode.speed)
        elif direction=="down":
            mode.dirSetter(name,0,mode.speed)

    def timerFired(mode):
        if mode.gameOver==False:
            mode.legalPacDirections=mode.legalPlaces(mode.pacmanXPos,mode.pacmanYPos)
            if mode.pacCurrDirection in mode.legalPacDirections:
                mode.pacmanXPos+=mode.dxPacPos
                mode.pacmanYPos+=mode.dyPacPos
            mode.makePlayerVisible()
            mode.setPinkyDir()
            mode.legalPinkyDirections=mode.legalPlaces(mode.pinkyGhostXPos,mode.pinkyGhostYPos)
            if mode.pinkyCurrDirection in mode.legalPinkyDirections:
                mode.movePlayer(mode.pinkyCurrDirection,"pinky")
            else:
                mode.pinkyCurrDirection=random.choice(mode.legalPinkyDirections)
                mode.movePlayer(mode.pinkyCurrDirection,"pinky")
            mode.pinkyGhostXPos+=mode.dxPinkyPos
            mode.pinkyGhostYPos+=mode.dyPinkyPos
            if mode.pinkyGhostXPos==mode.pacmanXPos and mode.pinkyGhostYPos==mode.pacmanYPos:
                mode.gameOver=True
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
            mode.dirSetter(mode,0,0)

    def dirSetter(mode,name,dx,dy):
        if name=="pac":
            mode.dxPacPos=dx
            mode.dyPacPos=dy
        elif name=="pinky":
            mode.dxPinkyPos=dx
            mode.dyPinkyPos=dy

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
        for x in range(int(mode.wallX*10),int(2*(mode.width-3*mode.wallWidth)),int(mode.wallX*10)):
            for y in range(int(mode.wallY*10),int(1.5*(mode.height-3*mode.wallHeight)),int(mode.wallY*10)):
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
            for wall in mode.gameBoard.board:
                wall.x-=mode.scrollX
                wall.y-=mode.scrollY
            mode.gameBoard.drawBoard(canvas)
            for coin in mode.points:
                coin.x-=mode.scrollX
                coin.y-=mode.scrollY
                coin.drawPoints(canvas)
            mode.pacmanXPos-=mode.scrollX
            mode.pacmanYPos-=mode.scrollY
            PacMan(mode.pacmanXPos,mode.pacmanYPos).drawPacMan(canvas)
            mode.blinkyGhostXPos-=mode.scrollX
            mode.blinkyGhostYPos-=mode.scrollY
            Blinky(mode,mode.blinkyGhostXPos,mode.blinkyGhostYPos).drawGhost(canvas)
            mode.pinkyGhostXPos-=mode.scrollX
            mode.pinkyGhostYPos-=mode.scrollY
            Pinky(mode,mode.pinkyGhostXPos,mode.pinkyGhostYPos).drawGhost(canvas)
            mode.inkyGhostXPos-=mode.scrollX
            mode.inkyGhostYPos-=mode.scrollY
            Inky(mode,mode.inkyGhostXPos,mode.inkyGhostYPos).drawGhost(canvas)
            mode.clydeGhostXPos-=mode.scrollX
            mode.clydeGhostYPos-=mode.scrollY
            Clyde(mode,mode.clydeGhostXPos,mode.clydeGhostYPos).drawGhost(canvas)
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