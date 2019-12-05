from cmu_112_graphics import *

# animation framework attained from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

# CITATION: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

class InstructionsMode(Mode):
    def redrawAll(mode,canvas):
        font='Courier 18 bold'
        canvas.create_rectangle(0,0,mode.width,mode.height,fill="black")
        canvas.create_text(mode.width/2, mode.height/8, \
            text='Instructions', font='Courier 26 bold', fill="white")
        canvas.create_text(mode.width/2, mode.height/8+20, \
            text='Welcome to Pac-Man, Version 1.12! There are three different modes:', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/8+40, \
            text='Demo: play this mode if you have never played Pac-Man before', font=font, fill="purple")
        canvas.create_text(mode.width/2, mode.height/8+60, \
            text='Single Player: creates a randomly generated board every game', font=font, fill="green")
        canvas.create_text(mode.width/2, mode.height/8+80, \
            text='Sidescroll: can move off-screen to collect points', font=font, fill="blue")
        canvas.create_text(mode.width/2, mode.height/8+100, \
            text='Each game starts after 3 seconds. You have three lives.', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/8+120, \
            text='Each ghost has a different characteristic:', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/8+140, \
            text='Blinky: follows the shortest path to Pac-Man', font=font, fill="red")
        canvas.create_text(mode.width/2, mode.height/8+160, \
            text='Pinky: changes direction based on relative pos of Pac-Man', font=font, fill="pink")
        canvas.create_text(mode.width/2, mode.height/8+180, \
            text='Inky: goes to the area with the most points', font=font, fill="aqua")
        canvas.create_text(mode.width/2, mode.height/8+200, \
            text='Clyde: follows the ghost closest to Pac-Man', font=font, fill="orange")
        canvas.create_text(mode.width/2, mode.height/8+220, \
            text='Press arrows to move the respective direction', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/8+240, \
            text='You can move through portals at the end of the board', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/8+260, \
            text='Collect all the points before the ghosts kill you', font=font, fill="white")
        canvas.create_text(mode.width/2, mode.height/8+280, \
            text='Good luck!', font='Courier 26 bold', fill="white")
        canvas.create_rectangle(550,450,700,475,fill="blue")
        canvas.create_text(625,463,text='Home',font=font,\
            fill="white")
    
    def mousePressed(mode,event):
        if event.x>550 and event.x<700 and event.y>450 and event.y<475:
            mode.app.setActiveMode(mode.app.splashScreenMode)