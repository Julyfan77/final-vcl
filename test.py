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

from PyQt5.QtWidgets import QMessageBox, QFileDialog
import matplotlib.pyplot as plt
class img:
    def __init__(self, win):
        
        self.window = win
        self.ImgPath = None

    def i_msg(self, widget, context):
        echo = QMessageBox(QMessageBox.Information, "提示", context, QMessageBox.NoButton, widget)
        echo.addButton("好的", QMessageBox.AcceptRole)
        echo.exec_()

    def f_msg(self):
        file_Name, file_type = QFileDialog.getOpenFileName(self.window,
                                                           "选取文件",
                                                           "C:",
                                                           "All Files (*)")
        # name = file_Name.split('.')
        # h = hashlib.md5()
        # h.update(name[0].encode("utf8"))
        # name0 = h.hexdigest()
        # file_Name = name0 + '.' + name[-1]
        # print(file_Name,file_type)
        return file_Name

    def img_show(self):
        self.ImgPath = self.f_msg()
        self.window.board.load_img(self.ImgPath)


    def line(self):
        if self.li.sub_ui.x0.text() != '' and self.li.sub_ui.y0.text() != '' and self.li.sub_ui.x1.text() != '' and self.li.sub_ui.y1.text() != '':
            self.window.board.drawLine(
                float(self.li.sub_ui.x0.text()),
                float(self.li.sub_ui.y0.text()),
                float(self.li.sub_ui.x1.text()),
                float(self.li.sub_ui.y1.text()))
        else:
            self.i_msg(self.li, "输入不能为空！")

    def round(self):
        if self.ri.sub_ui.x0.text() != '' and self.ri.sub_ui.y0.text() != '' and self.ri.sub_ui.R.text() != '':
            self.window.board.drawRound(
                float(self.ri.sub_ui.x0.text()),
                float(self.ri.sub_ui.y0.text()),
                float(self.ri.sub_ui.R.text()))
        else:
            self.i_msg(self.ri, "输入不能为空！")

    def fill(self):
        if self.pi.sub_ui.x.text() != '' and self.pi.sub_ui.y.text() != '':
            self.window.board.fill(
                float(self.pi.sub_ui.x.text()),
                float(self.pi.sub_ui.y.text()))
        else:
            self.i_msg(self.pi, "输入不能为空！")

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = connect_win()
    sys.exit(app.exec_())