from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from utils.general import AppWidth, AppHeight
from utils.geometry import AB, BC, CD, GridWidth, CalculatePointC
from utils.transform import im2grid, grid2im
import numpy as np
from numpy import sqrt
import math
import warnings
warnings.filterwarnings('ignore')
class MainPanel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.ratio = AppWidth/GridWidth
        self.AB = AB * self.ratio
        self.BC = BC * self.ratio
        self.CD = CD * self.ratio
        pointAx, pointAy = grid2im(0,0)
        self.pointA = QtCore.QPoint(pointAx, pointAy)
        pointBx, pointBy = grid2im(0,self.AB)
        self.pointB = QtCore.QPoint(pointBx, pointBy)
        pointCx, pointCy = grid2im(100* self.ratio,150* self.ratio)
        self.pointC = QtCore.QPoint(pointCx, pointCy)
        pointDx, pointDy = grid2im(100* self.ratio,100* self.ratio)
        self.pointD = QtCore.QPoint(pointDx, pointDy)
        self.an1 = 90
        self.an2 = 90
        self.an3 = 90
        self.an1Old = 90
        self.an2Old = 90
        self.an3Old = 90
        self.cxOld = 100* self.ratio
        self.cyOld = 150* self.ratio
        self.count = 0

    def paintEvent(self, event):
        '''
        Drawing event that will be updated when user press the left mouse key, or drag the mouse to different location
        '''
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #### Draw the boundary line
        painter.setPen(QPen(Qt.black,  8, Qt.SolidLine))
        painter.drawRect(0,0,AppWidth,AppHeight)
        #### Draw the arc
        painter.setPen(QPen(Qt.blue,  4, Qt.SolidLine))
        painter.drawArc(0, 0, AppWidth, AppWidth, 0 * 16, 180 * 16)
        #### Draw the grid line in gray
        painter.setPen(QPen(Qt.gray,  2, Qt.SolidLine))
        for i in range(15):
            painter.drawLine(0, int(AppHeight/15)*(i+1), AppWidth, int(AppHeight/15)*(i+1))
        for i in range(30):
            painter.drawLine(int(AppWidth/30)*(i+1), 0, int(AppWidth/30)*(i+1), AppHeight)

        #### Draw the current point A, B, C, D location
        painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        painter.drawPoint(self.pointA)
        painter.drawPoint(self.pointB)
        painter.drawPoint(self.pointC)
        painter.drawPoint(self.pointD)
        painter.setPen(QPen(Qt.red, 6, Qt.SolidLine))
        painter.drawLine(self.pointA, self.pointB)
        painter.drawLine(self.pointB, self.pointC)
        painter.drawLine(self.pointC, self.pointD)
    def CalculatePointD(self):
        '''
        function to calculate the location of the point D by reading the current mouse location
        '''
        dx = self.pointD.x()
        dy = self.pointD.y()
        dx, dy = im2grid(dx, dy)
        self.AD = sqrt(max(0, (dx**2+dy**2)))
        ####Check whether the D is in the range of the half circle, if not, replace it at the nearest point on the circle
        if dy < 0:
            dy = 0
            self.AD = np.abs(dx)
        if self.AD > self.AB+self.BC+self.CD:
            dx = dx * (self.AB+self.BC+self.CD)/self.AD
            dy = dy * (self.AB+self.BC+self.CD)/self.AD
            self.AD = self.AB+self.BC+self.CD
        return dx, dy
    def CalculateThreePoints(self, an1):
        '''
        function to calculate locations of point B, C, and D
        '''
        dx, dy = self.CalculatePointD()
        bx = self.AB * np.cos(np.radians(an1))
        by = self.AB * np.sin(np.radians(an1))
        self.BD = sqrt(max(0, (bx-dx)**2+(by-dy)**2))
        isValid, PointCInfoList = CalculatePointC(self.BC, self.CD, self.BD, bx, by, dx, dy)
        PointList = []
        if isValid == True:
            for PointCInfo in PointCInfoList:
                cx = PointCInfo[0]
                cy = PointCInfo[1]
                PointList.append([bx, by, cx, cy, dx, dy])
        return isValid, PointList
    def CalculateMaxDeltaAn1(self):
        '''
        function to calculate the maximum possible angle of BAx that is necessary to check
        '''
        dx, dy = self.CalculatePointD()
        if self.AD == 0:
            return
        ####Calculate the angle between AD and the horizontal axis, assume this angle is equal to the angle between AB and horizontal axis
        self.an1 = np.degrees(np.arccos(dx/self.AD))
        ####Use an1 to update the locaiton B
        bx = self.AB * np.cos(np.radians(self.an1))
        by = self.AB * np.sin(np.radians(self.an1))
        ####Calculate the distance between point B and point D
        self.BD = sqrt(max(0, (bx-dx)**2+(by-dy)**2))
        isValid = False
        organ1 = self.an1
        moveDirection = 1
        isValid, _ = CalculatePointC(self.BC, self.CD, self.BD, bx, by, dx, dy)
        while self.BD < np.abs(self.BC - self.CD) or isValid != True:
            self.an1 = self.an1 - moveDirection * 1
            if self.an1 < 0:
                self.an1 = organ1
                moveDirection = -1
            ####Use an1 to update the locaiton B
            bx = self.AB * np.cos(np.radians(self.an1))
            by = self.AB * np.sin(np.radians(self.an1))
            ####Calculate the distance between point B and point D
            self.BD = sqrt(max(0, (bx-dx)**2+(by-dy)**2))
            isValid, _ = CalculatePointC(self.BC, self.CD, self.BD, bx, by, dx, dy)
    def CalculateOptimalAngle(self):
        '''
        function to find the optimal angle that can leads to minimum sum of delta angle 
        '''
        MinDeltaSum = 1080
        MinDelta = 1080
        Optimalan1 = self.an1
        Optimalan2 = self.an2
        Optimalan3 = self.an3
        OptimalCount = 0
        resultList = []
        disList = []
        LowDistC= 10000
        for Currentan1 in range(int(min(self.an1, self.an1Old)), int(max(self.an1, self.an1Old))):
            ####Loop all the possible angle of BAx, and find the optimal one
            isValid, PointsList = self.CalculateThreePoints(Currentan1)
            if isValid:
                for count, CurrentPointList in enumerate(PointsList):
                    bx = CurrentPointList[0]
                    by = CurrentPointList[1]
                    cx = CurrentPointList[2]
                    cy = CurrentPointList[3]
                    dx = CurrentPointList[4]
                    dy = CurrentPointList[5]
                    CurrentDeltaan1 = abs(Currentan1 - self.an1Old)
                    self.AC = sqrt(max(0, cx**2+cy**2))
                    self.BD = sqrt(max(0, (bx-dx)**2+(by-dy)**2))
                    Currentan2 = np.degrees(np.arccos((self.AB**2 + self.BC**2 - self.AC**2)/(2*self.AB*self.BC)))
                    CurrentDeltaan2 = abs(Currentan2 - self.an2Old)
                    Currentan3 = np.degrees(np.arccos((self.BC**2 + self.CD**2 - self.BD**2)/(2*self.BC*self.CD)))
                    CurrentDeltaan3 = abs(Currentan3 - self.an3Old)
                    CurrentMinDelta = min(min(CurrentDeltaan1, CurrentDeltaan2), CurrentDeltaan3)
                    CurrentDeltSum = CurrentDeltaan1+CurrentDeltaan2+CurrentDeltaan3
                    CurrentDistC = (np.sqrt((self.cxOld - cx)**2 + (self.cyOld - cy)**2))
                    if math.isnan(CurrentDeltSum) == False and CurrentMinDelta < MinDelta:
                        ####If the current angle is smaller than the previous minimum value, update it
                        if MinDelta < 10 and CurrentDistC > LowDistC:
                            continue
                        MinDeltaSum = CurrentDeltSum
                        LowDistC = CurrentDistC
                        Optimalan1 = Currentan1
                        Optimalan2 = Currentan2
                        Optimalan3 = Currentan3
                        OptimalCount = count
        self.an1 = Optimalan1
        self.an2 = Optimalan2
        self.an3 = Optimalan3
        self.count = OptimalCount

    def UpdatePointsLocations(self):
        self.CalculateMaxDeltaAn1()
        self.CalculateOptimalAngle()
        isValid, PointsList = self.CalculateThreePoints(self.an1)
        if isValid:
            CurrentPointList = PointsList[self.count]
            bx = CurrentPointList[0]
            by = CurrentPointList[1]
            cx = CurrentPointList[2]
            cy = CurrentPointList[3]
            self.cxOld = cx
            self.cyOld = cy
            dx = CurrentPointList[4]
            dy = CurrentPointList[5]
            bx, by = grid2im(bx, by)
            cx, cy = grid2im(cx, cy)
            dx, dy = grid2im(dx, dy)
            self.pointB = QtCore.QPoint(int(bx), int(by))
            self.pointC = QtCore.QPoint(int(cx), int(cy))
            self.pointD = QtCore.QPoint(int(dx), int(dy))
            self.an1Old = self.an1
            self.an2Old = self.an2
            self.an3Old = self.an3
        
        
        ####Calculate the angle between CB and DB

    def mousePressEvent(self, event):
        '''
        the function that calls whenever the mouse is pressed
        '''
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.pointD = event.pos()
            self.UpdatePointsLocations()
            self.update() 
    def mouseMoveEvent(self, event):
        '''
        the function that calls whenever the mouse is moved
        '''
        if event.buttons() & Qt.LeftButton:
            self.drawing = True
            self.pointD = event.pos()
            self.UpdatePointsLocations()
            self.update()

    def keyPressEvent(self, event):
        print(self.frameGeometry().width())
        try:
            print(chr(event.key()))
        except:
            print(event.key())
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
    