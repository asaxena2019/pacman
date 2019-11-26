from cmu_112_graphics import *
from splashScreenMode import *
from originalGameMode import *

# from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# #subclassing ModalApp
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode=SplashScreenMode()
        app.gameMode=OriginalGameMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay=50

app = MyModalApp(width=750, height=500)