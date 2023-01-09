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
        self.lb=QLabel()
        self.pixmap = QPixmap()
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

    def load_img(self, img):
        self.pixmap.load(img)
        self.update()
        print(img)
