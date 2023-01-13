from collections import deque
from math import fabs

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel,QDialog
from PyQt5.Qt import QPixmap, QPainter, QPen,QBrush
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QImage
from Ui_color import *
import math
import cv2

global nowcol,nowwid
nowcol=Qt.black
nowwid=1
class PaintBoard(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #self.lbl=QLabel("图片",self)
        self.pixmap = QPixmap(200,200)
        self.pixmap.fill(Qt.white)
        self.img = QImage(self.pixmap.toImage())
        #self.lbl.setPixmap(self.pixmap)
        self.mode=0  #0-choose,1-straight,2-circle,3-rec,4-fillrec,5-fillcircle
        self.pen = QPainter()
        self.setMouseTracking(True)
        self.linexy=[]
        self.recpoint=[]
        self.fill_recpoint=[]
        self.style=0
        self.brushstyle=0
    def choose(self):
        self.mode=0
    def paintEvent(self, paintEvent):
        print("paint event !!!")
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.pen.begin(self)
        # self.pen.drawPixmap(0, 0, self.pixmap)
        self.img = QImage(self.pixmap.toImage())
        self.pen.drawImage(0, 0, self.img)
        self.pen.end()

    def load_img(self, img):
        image = cv2.imread(img)
        size = image.shape
        w=size[1]
        h=size[0]
        print(w)
        print(h)
        if w/h > 390/144:
            h=3900*h/w
            w=3900
        else:
            w=1440*w/h
            h=1440    
        print(w)
        print(h) 
        self.pixmap=QPixmap(img).scaled(w,h)
        w = self.pixmap.width()
        h = self.pixmap.height()
        print((w, h))
        #self.lbl.setPixmap(self.pixmap)
        #self.show()
        self.update()
    def save_img(self,img):
        self.img.save(img)
    # def myRemovePic(self):
    #     self.lbl.setPixmap(QPixmap(""))
    # def myAddPic(self):
    #     self.lbl.setPixmap(self.pixmap)

    #global nowwid,nowcol
    def drawPoint(self, x, y,col=Qt.black,wid=1,style=0):
        # print(self.width(),self.height())
        m = int(self.width()/2) + x
        n = int(self.height()/2) - y
        
        self.pen.begin(self.pixmap)
        mypen=QPen(col,wid)
        self.pen.setPen(mypen)
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
        if self.mode==3:
            #print("rec")
            if event.button()==Qt.LeftButton:
                self.recpoint.append([x,y])
            elif event.button()==Qt.RightButton:
                #print("???")
                for iter in range(len(self.recpoint)):
                    self.draw_line(self.recpoint[(iter)%len(self.recpoint)][0],
                    self.recpoint[(iter)%len(self.recpoint)][1],
                    self.recpoint[(iter+1)%len(self.recpoint)][0],
                    self.recpoint[(iter+1)%len(self.recpoint)][1])
                self.recpoint.clear()
        if self.mode==2:
            if event.button()==Qt.LeftButton:
                if len(self.linexy)==0:
                    self.linexy.append([x,y])
                elif len(self.linexy)==1:
                    self.linexy.append([x,y])
                    r=math.sqrt((self.linexy[0][0]-x)*(self.linexy[0][0]-x)+
                    (self.linexy[0][1]-y)*(self.linexy[0][1]-y))
                    self.drawRound(self.linexy[0][0],self.linexy[0][1],r)
                    self.linexy.clear()
        if self.mode==5:
            if event.button()==Qt.LeftButton:
                if len(self.linexy)==0:
                    self.linexy.append([x,y])
                elif len(self.linexy)==1:
                    self.linexy.append([x,y])
                    r=math.sqrt((self.linexy[0][0]-x)*(self.linexy[0][0]-x)+
                    (self.linexy[0][1]-y)*(self.linexy[0][1]-y))
                    self.drawfillRound(self.linexy[0][0],self.linexy[0][1],r)
                    self.linexy.clear()
        if self.mode==4:#fill_rec
            if event.button()==Qt.LeftButton:
                if len(self.fill_recpoint)==0:
                    self.fill_recpoint.append([x,y])
                elif len(self.fill_recpoint)==1:
                    self.fill_recpoint.append([x,y])
                    self.draw_fill_rec(self.fill_recpoint[0][0],
                    self.fill_recpoint[0][1],self.fill_recpoint[1][0],
                    self.fill_recpoint[1][1])
                    self.fill_recpoint.clear()
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
        self.linexy.clear()
    def draw_line(self,x0,y0,x1,y1):
        global nowcol,nowwid
        col=nowcol
        wid=nowwid
        self.pen.begin(self.pixmap)  
        #print(wid)
        mypen=QPen(col,wid,Qt.SolidLine)
        if self.style==0:
            mypen=(QPen(col,wid,Qt.SolidLine))
            self.pen.setPen(mypen)
        elif self.style==1:
            mypen=QPen(col,wid,Qt.DashLine)
            self.pen.setPen(mypen)
        elif self.style==2:
            mypen=QPen(col,wid,Qt.CustomDashLine)
            mypen.setDashPattern([1,4,5,4])
            self.pen.setPen(mypen)
        elif self.style==3:
            #print("style is dotline,wid is ?")
            mypen=QPen(col,wid,Qt.DotLine)
            self.pen.setPen(mypen)   
           
        self.pen.drawLine(x0,y0,x1,y1)
        self.pen.end()
    def draw_circle_action(self):
        self.mode=2
        self.linexy.clear()
    def CirclePlot(self, xc, yc, x, y):
        global nowwid,nowcol
        col=nowcol
        wid=nowwid
        self.drawPoint(x+xc, y+yc,col,wid)
        self.drawPoint(-x+xc, y+yc,col,wid)
        self.drawPoint(x+xc, -y+yc,col,wid)
        self.drawPoint(-x+xc, -y+yc,col,wid)
        self.drawPoint(y+xc, x+yc,col,wid)
        self.drawPoint(y+xc, -x+yc,col,wid)
        self.drawPoint(-y+xc, x+yc,col,wid)
        self.drawPoint(-y+xc, -x+yc,col,wid)
    def drawRound(self, xc, yc, r):
        x = 0
        y = r
        d = 3-2*r
        self.CirclePlot(xc, yc, x, y)
        while x<y:
            if d<0:
                d = d+4*x+6
            else:
                d = d+4*(x-y)+10
                y -= 1
            x +=1
            self.CirclePlot(xc, yc, x, y)
    def drawfillRound(self, xc, yc, r):
        global nowcol
        col=nowcol
        self.pen.begin(self.pixmap)  
        #print(wid)
        mypen=QBrush()
        mypen.setColor(nowcol)
        if self.brushstyle==0:
            mypen.setStyle(Qt.SolidPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle==1:
            mypen.setStyle(Qt.HorPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle==2:
            mypen.setStyle(Qt.BDiagPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle==3:
            #print("style is dotline,wid is ?")
            mypen.setStyle(Qt.Dense1Pattern)
            self.pen.setBrush(mypen)   
        elif self.brushstyle==4:
            #print("style is dotline,wid is ?")
            mypen.setStyle(Qt.RadialGradientPattern)
            self.pen.setBrush(mypen)     
        self.pen.drawEllipse(xc-r,yc-r,2*r,2*r)
        print(xc,r,yc,r)
        self.pen.end() 
    def draw_rec_action(self):
        self.mode=3
        #print("change mode")      
        self.recpoint.clear()
    def draw_fill_rec_action(self):
        self.mode=4
        self.fill_recpoint.clear()
    def draw_fill_circle_action(self):
        self.mode=5
        self.linexy.clear()
    def draw_fill_rec(self,x0,y0,x1,y1):
        global nowcol
        col=nowcol
        self.pen.begin(self.pixmap)  
        #print(wid)
        mypen=QBrush()
        mypen.setColor(nowcol)
        if self.brushstyle==0:
            mypen.setStyle(Qt.SolidPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle==1:
            mypen.setStyle(Qt.HorPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle==2:
            mypen.setStyle(Qt.BDiagPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle==3:
            #print("style is dotline,wid is ?")
            mypen.setStyle(Qt.Dense1Pattern)
            self.pen.setBrush(mypen)   
        elif self.brushstyle==4:
            #print("style is dotline,wid is ?")
            mypen.setStyle(Qt.RadialGradientPattern)
            self.pen.setBrush(mypen)       
        self.pen.drawRect(x0,y0,x1-x0,y1-y0)
        print(x0,y0,x1,y1)
        self.pen.end()
    def action1(self):
        global nowwid
        nowwid=1
    def action2(self):
        global nowwid
        nowwid=2
    def action3(self):
        global nowwid
        nowwid=3
    def action5(self):
        global nowwid
        nowwid=5
    def action4(self):
        global nowwid
        nowwid=4
    def style1(self):
        self.style=1
    def style2(self):
        self.style=2
    def style3(self):
        self.style=3
    def style_outline(self):
        self.style=0
    def brushstyle1(self):
        self.brushstyle=1
    def brushstyle2(self):
        self.brushstyle=2
    def brushstyle3(self):
        self.brushstyle=3
    def brushstyle0(self):
        self.brushstyle=0
    def brushstyle4(self):
        self.brushstyle=4
    
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
    
