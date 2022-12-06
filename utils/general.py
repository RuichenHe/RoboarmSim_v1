global AppWidth
global AppHeight
AppWidth= 1200
AppHeight= 600
def SetDisplay(DisplayScreen, MainWindow):
    '''
    Set the size of the UI window
    '''
    DisplayScreenSize = DisplayScreen.availableGeometry()
    ScreenHalfWidth = int(DisplayScreenSize.width()/2)
    ScreenHalfHeight = int(DisplayScreenSize.height()/2)
    MainWindow.setGeometry(ScreenHalfWidth - int(AppWidth/2), ScreenHalfHeight - int(AppHeight/2), AppWidth, AppHeight)
    MainWindow.setFixedSize(AppWidth, AppHeight+5)