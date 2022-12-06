from PyQt5 import QtWidgets, QtCore
import sys
from app.main import MainPanel
from utils.general import SetDisplay
import os
SoftwareName = 'RoboarmSim v1'
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    DisplayScreen = app.primaryScreen()
    
    os.system('cls' if os.name == 'nt' else 'clear')

    MainWindow = MainPanel()
    SetDisplay(DisplayScreen, MainWindow)
    MainWindow.show()
    MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", SoftwareName))
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())

    

