from collections import deque
from math import fabs

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel,QDialog
from PyQt5.Qt import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QImage
from Ui_color import *

global nowcol,nowwid
nowcol=Qt.black
nowwid=1
class PaintBoard(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.lbl=QLabel("图片",self)
        self.pixmap = QPixmap(1,1)
        self.pixmap.fill(Qt.white)
        self.img = QImage(self.pixmap.toImage())
        self.lbl.setPixmap(self.pixmap)
        self.mode=0  #0-choose,1-straight,2-circle,3-curve
        self.pen = QPainter()
        self.setMouseTracking(True)
        self.linexy=[]
    def paintEvent(self, paintEvent):
        print("paint event !!!")
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.pen.begin(self)
        # self.pen.drawPixmap(0, 0, self.pixmap)
        self.img = QImage(self.pixmap.toImage())
        self.pen.drawImage(0, 0, self.img)
        self.pen.end()

    def load_img(self, img):
        self.pixmap=QPixmap(img)
        #self.lbl.setPixmap(self.pixmap)
        #self.show()
        self.update()
        
        print(img)
    def save_img(self,img):
        print(img)
        self.img.save(img)
    # def myRemovePic(self):
    #     self.lbl.setPixmap(QPixmap(""))
    # def myAddPic(self):
    #     self.lbl.setPixmap(self.pixmap)
    def drawPoint(self, x, y,col=Qt.black,wid=1):
        # print(self.width(),self.height())
        m = int(self.width()/2) + x
        n = int(self.height()/2) - y
        self.pen.begin(self.pixmap)
        self.pen.setPen(QPen(col,wid))
        self.pen.drawPoint(x, y)
        self.pen.end()
        self.update()
    def mousePressEvent(self, event):
        x=event.x()
        y=event.y()
        text="x: {0}, y: {1}".format(x,y)
        if self.mode==1:
            if event.button()==Qt.LeftButton:
                if len(self.linexy)==0:
                    self.linexy.append([x,y])
                elif len(self.linexy)==1:
                    self.draw_line(self.linexy[0][0],self.linexy[0][1],x,y)
                    self.linexy.clear()
        self.update()
            
    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        text = "x: {0}, y: {1}".format(x, y)
    def mouseMoveEvent(self,event):
        x = event.x()
        y = event.y()
        text = "x:{0},y:{1}".format(x,y)
        #self.ui.label_2.setText(text)  
    def draw_line_action(self):
        self.mode=1

    def draw_line(self,x0,y0,x1,y1,col=0,wid=0):
        self.mode=1        
        dx = x1 - x0
        dy = y1 - y0
        if fabs(dx) > fabs(dy):
            steps = fabs(dx)
        else:
            steps = fabs(dy)
        self.drawPoint(int(x0+0.5), int(y0+0.5),nowcol,nowwid)
        if steps==0:
            return
        xInc = dx/steps
        yInc = dy/steps
        for i in range(int(steps+0.5)):
            x0 += xInc
            y0 += yInc
            self.drawPoint(int(x0+0.5), int(y0+0.5),nowcol,nowwid)  
            self.update()
class colorBoard(PaintBoard):
    def __init__(self):
        QWidget.__init__(self)
        self.pixmap = QPixmap(1,1)
        self.pixmap.fill(Qt.black)
        self.img = QImage(self.pixmap.toImage())
        #self.lbl.setPixmap(self.pixmap)
        self.pen = QPainter()
        self.color=QColor(255,255,255,127)
    def paintEvent(self, paintEvent):
        return super().paintEvent(paintEvent)
    def load_color(self, col):
        #self.widget.setStyleSheet('QWidget {background-color:%s}'%col.name())
        global nowcol
        nowcol=col
        self.pixmap.fill(col)
    
