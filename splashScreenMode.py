from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# CITATION: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

class SplashScreenMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        for row in range(0,mode.height+50,50):
            for col in range(0,mode.width+50,50):
                canvas.create_oval(col-5,row-5,col+5,row+5,fill="orange")
        canvas.create_text(mode.width/2, mode.height/8, \
            text='Pac-Man, Version 1.12', font='Courier 26 bold', fill="white")
        canvas.create_rectangle(200,250,350,275,fill="blue")
        canvas.create_text(275,263, \
            text='Instructions', font='Courier 14 bold', fill="white")
        canvas.create_text(500,263, \
            text='Rules and player information', font='Courier 14 bold', fill="white")
        canvas.create_rectangle(200,300,350,325,fill="blue")
        canvas.create_text(275,313, \
            text='Demo', font='Courier 14 bold', fill="white")
        canvas.create_text(500,313, \
            text='Learn the basics', font='Courier 14 bold', fill="white")
        canvas.create_rectangle(200,350,350,375,fill="blue")
        canvas.create_text(275,363, \
            text='Single Player Mode', font='Courier 14 bold', fill="white")
        canvas.create_text(500,363, \
            text='New game, new maze', font='Courier 14 bold', fill="white")
        canvas.create_rectangle(200,400,350,425,fill="blue")
        canvas.create_text(275,413, \
            text='Sidescroll Mode', font='Courier 14 bold', fill="white")
        canvas.create_text(500,413, \
            text='Travel off-screen with unknown paths', font='Courier 14 bold', fill="white")
        def drawCoins(mode):
            pass

    def mousePressed(mode,event):
        if event.x>200 and event.x<350:
            if event.y>250 and event.y<275:
                mode.app.setActiveMode(mode.app.instructions)
            elif event.y>300 and event.y<325:
                mode.app.setActiveMode(mode.app.demoMode)
            elif event.y>350 and event.y<375:
                mode.app.setActiveMode(mode.app.singleMode)
            elif event.y>400 and event.y<425:
                mode.app.setActiveMode(mode.app.scrollMode)