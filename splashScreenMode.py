from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# CITATION: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

class SplashScreenMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, mode.height/5, \
            text='Pac-Man', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/3, \
            text='Press o for original mode, s for sidescroll mode!',font=font,fill="white")

    def keyPressed(mode,event):
        if event.key=="o":
            mode.app.setActiveMode(mode.app.gameMode)
        elif event.key=="s":
            mode.app.setActiveMode(mode.app.scrollMode)

    #will add buttons to determine mode
    def mousePressed(mode,event):
        pass