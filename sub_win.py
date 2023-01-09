from collections import deque
from math import fabs

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.Qt import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QImage


class PaintBoard(QWidget):


    def __init__(self):
        QWidget.__init__(self)

        # self.label = QLabel(self)
        # self.gridLayout = QGridLayout(self)
        # self.gridLayout.addWidget(self.label)

        self.pixmap = QPixmap(1,1)
        self.pixmap.fill(Qt.white)
        self.img = QImage(self.pixmap.toImage())

        # self.label.setFrameShape(1)
        # # self.label.setPixmap(self.pixmap)
        # self.label.setScaledContents(True)
        # self.label.setVisible(False)

        self.pen = QPainter()

    def paintEvent(self, paintEvent):
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.pen.begin(self)
        # self.pen.drawPixmap(0, 0, self.pixmap)
        self.img = QImage(self.pixmap.toImage())
        self.pen.drawImage(0, 0, self.img)
        self.pen.end()

    def drawPoints(self, x, y):
        # print(self.width(),self.height())
        m = int(self.width()/2) + x
        n = int(self.height()/2) - y
        self.pen.begin(self.pixmap)
        self.pen.setPen(QPen(Qt.black,1))
        self.pen.drawPoint(m, n)
        self.pen.end()
        self.update()
        # self.repaint()

    def load_img(self, img):
        self.pixmap.load(img)
        self.update()

    #DDA
    def drawLine(self, x0, y0, x1, y1):
        self.Clear()
        dx = x1 - x0
        dy = y1 - y0
        if fabs(dx) > fabs(dy):
            steps = fabs(dx)
        else:
            steps = fabs(dy)
        self.drawPoints(int(x0+0.5), int(y0+0.5))
        xInc = dx/steps
        yInc = dy/steps
        for i in range(int(steps+0.5)):
            x0 += xInc
            y0 += yInc
            self.drawPoints(int(x0+0.5), int(y0+0.5))

    #中点法画圆
    def CirclePlot(self, xc, yc, x, y):
        self.drawPoints(x+xc, y+yc)
        self.drawPoints(-x+xc, y+yc)
        self.drawPoints(x+xc, -y+yc)
        self.drawPoints(-x+xc, -y+yc)
        self.drawPoints(y+xc, x+yc)
        self.drawPoints(y+xc, -x+yc)
        self.drawPoints(-y+xc, x+yc)
        self.drawPoints(-y+xc, -x+yc)
    def drawRound(self, xc, yc, r):
        self.Clear()
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
            
    '''
    # 边界填充
    def fill(self, x, y):
        w = int(self.width()/2)
        h = int(self.height()/2)
        block = deque([(x, y)])
        while 1:
            if len(block) == 0:
                break
            else:
                # print(block)
                point = block.popleft()
                m = point[0]
                n = point[1]
                # c = self.img.pixel(w+m, h+n)
                # colors = QColor(c).getRgb()
                # if colors != (0, 0, 0, 255):
                self.drawPoints(m, n)
                # result.append((m,n))
    
                c = self.img.pixel(w+m, h+n-1)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m,n-1) not in block:
                        block.append((m,n-1))
    
                c = self.img.pixel(w+m, h+n+1)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m,n+1) not in block:
                        block.append((m,n+1))
    
                c = self.img.pixel(w+m-1, h+n)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m-1,n) not in block:
                        block.append((m-1,n))
    
                c = self.img.pixel(w+m+1, h+n)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m+1,n) not in block:
                        block.append((m+1,n))
        print(results)
    '''

    #边界填充
    #种子边界填充
    def fill(self, x, y):
        w = int(self.width()/2)
        h = int(self.height()/2)
        block = deque([(x, y)])
        results = []
        while 1:
            if len(block) == 0:
                break
            else:
                point = block.popleft()
                m = point[0]
                n = point[1]
                results.append((m,n))

                c = self.img.pixel(w+m, h+n-1)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m,n-1) not in block:
                        if (m,n-1) not in results:
                            block.append((m,n-1))

                c = self.img.pixel(w+m, h+n+1)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m,n+1) not in block:
                        if (m,n+1) not in results:
                            block.append((m,n+1))

                c = self.img.pixel(w+m-1, h+n)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m-1,n) not in block:
                        if (m-1,n) not in results:
                            block.append((m-1,n))

                c = self.img.pixel(w+m+1, h+n)
                colors = QColor(c).getRgb()
                if colors != (0, 0, 0, 255):
                    if (m+1,n) not in block:
                        if (m+1,n) not in results:
                            block.append((m+1,n))
        for point in results:
            self.drawPoints(point[0], point[1])

    def Clear(self):
        self.pixmap.fill(Qt.white)
        self.update()

class Ui_line_Form(object):
    def setupUi(self, line_Form):
        line_Form.setObjectName("line_Form")
        line_Form.resize(180, 160)
        self.gridLayout = QtWidgets.QGridLayout(line_Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(line_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.x0 = QtWidgets.QLineEdit(line_Form)
        self.x0.setObjectName("x0")
        self.horizontalLayout.addWidget(self.x0)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(line_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.y0 = QtWidgets.QLineEdit(line_Form)
        self.y0.setObjectName("y0")
        self.horizontalLayout_2.addWidget(self.y0)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(line_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.x1 = QtWidgets.QLineEdit(line_Form)
        self.x1.setObjectName("x1")
        self.horizontalLayout_3.addWidget(self.x1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(line_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.y1 = QtWidgets.QLineEdit(line_Form)
        self.y1.setObjectName("y1")
        self.horizontalLayout_4.addWidget(self.y1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ok_btn = QtWidgets.QPushButton(line_Form)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_5.addWidget(self.ok_btn)
        self.re_btn = QtWidgets.QPushButton(line_Form)
        self.re_btn.setObjectName("re_btn")
        self.horizontalLayout_5.addWidget(self.re_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(line_Form)
        self.re_btn.clicked.connect(self.x0.clear)
        self.re_btn.clicked.connect(self.y0.clear)
        self.re_btn.clicked.connect(self.x1.clear)
        self.re_btn.clicked.connect(self.y1.clear)
        QtCore.QMetaObject.connectSlotsByName(line_Form)

    def retranslateUi(self, line_Form):
        _translate = QtCore.QCoreApplication.translate
        line_Form.setWindowTitle(_translate("line_Form", "参数输入"))
        self.label.setText(_translate("line_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">X</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">起点</span><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_2.setText(_translate("line_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Y</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">起点</span><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_3.setText(_translate("line_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">X</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">终点</span><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_4.setText(_translate("line_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Y</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">终点</span><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.ok_btn.setText(_translate("line_Form", "确定"))
        self.re_btn.setText(_translate("line_Form", "重置"))

class Ui_round_Form(object):
    def setupUi(self, round_Form):
        round_Form.setObjectName("round_Form")
        round_Form.resize(180, 127)
        self.gridLayout = QtWidgets.QGridLayout(round_Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(round_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(round_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(round_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(round_Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(round_Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(round_Form)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.x0 = QtWidgets.QLineEdit(round_Form)
        self.x0.setObjectName("x0")
        self.verticalLayout_2.addWidget(self.x0)
        self.y0 = QtWidgets.QLineEdit(round_Form)
        self.y0.setObjectName("y0")
        self.verticalLayout_2.addWidget(self.y0)
        self.R = QtWidgets.QLineEdit(round_Form)
        self.R.setObjectName("R")
        self.verticalLayout_2.addWidget(self.R)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ok_btn = QtWidgets.QPushButton(round_Form)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.re_btn = QtWidgets.QPushButton(round_Form)
        self.re_btn.setObjectName("re_btn")
        self.horizontalLayout_2.addWidget(self.re_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(round_Form)
        self.re_btn.clicked.connect(self.x0.clear)
        self.re_btn.clicked.connect(self.y0.clear)
        self.re_btn.clicked.connect(self.R.clear)
        QtCore.QMetaObject.connectSlotsByName(round_Form)

    def retranslateUi(self, round_Form):
        _translate = QtCore.QCoreApplication.translate
        round_Form.setWindowTitle(_translate("round_Form", "参数输入"))
        self.label.setText(_translate("round_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">X</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">圆心</span></p></body></html>"))
        self.label_2.setText(_translate("round_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Y</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">圆心</span></p></body></html>"))
        self.label_3.setText(_translate("round_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">R</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">半径</span></p></body></html>"))
        self.label_4.setText(_translate("round_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_5.setText(_translate("round_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_6.setText(_translate("round_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.ok_btn.setText(_translate("round_Form", "确定"))
        self.re_btn.setText(_translate("round_Form", "重置"))

class Ui_point_Form(object):
    def setupUi(self, point_Form):
        point_Form.setObjectName("point_Form")
        point_Form.resize(180, 101)
        self.gridLayout = QtWidgets.QGridLayout(point_Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(point_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(point_Form)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(point_Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(point_Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.x = QtWidgets.QLineEdit(point_Form)
        self.x.setObjectName("x")
        self.verticalLayout_2.addWidget(self.x)
        self.y = QtWidgets.QLineEdit(point_Form)
        self.y.setObjectName("y")
        self.verticalLayout_2.addWidget(self.y)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ok_btn = QtWidgets.QPushButton(point_Form)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.re_btn = QtWidgets.QPushButton(point_Form)
        self.re_btn.setObjectName("re_btn")
        self.horizontalLayout_2.addWidget(self.re_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(point_Form)
        self.re_btn.clicked.connect(self.x.clear)
        self.re_btn.clicked.connect(self.y.clear)
        QtCore.QMetaObject.connectSlotsByName(point_Form)

    def retranslateUi(self, point_Form):
        _translate = QtCore.QCoreApplication.translate
        point_Form.setWindowTitle(_translate("point_Form", "参数输入"))
        self.label.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">X</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">图形内某点</span></p></body></html>"))
        self.label_2.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Y</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">图形内某点</span></p></body></html>"))
        self.label_4.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.label_5.setText(_translate("point_Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">：</span></p></body></html>"))
        self.ok_btn.setText(_translate("point_Form", "确定"))
        self.re_btn.setText(_translate("point_Form", "重置"))