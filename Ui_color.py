# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import sys


class ColorDialog(QWidget):
    def __init__(self, x, y, cb):
        super().__init__()
        # 颜色值
        color = QColor(0, 0, 0)
        # 位置
        self.setGeometry(x, y, 650, 280)
        # 标题
        self.setWindowTitle('颜色选择')
        # 按钮名称
        self.button = QPushButton('颜色选择', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        # 按钮位置
        self.button.move(40, 20)
        # 按钮绑定方法
        self.button.clicked.connect(self.showDialog)
        self.setFocus()
        self.widget = QWidget(self)
        self.widget.setStyleSheet('QWidget{background-color:%s} ' % color.name())
        # 取色框大小
        self.widget.setGeometry(210, 20, 400, 100)
        self.cb = cb

    def showDialog(self):
        col = QColorDialog.getColor()
        # print(type(col))
        # print(col.name(),"\n")
        if col.isValid():
            self.widget.setStyleSheet('QWidget {background-color:%s}' % col.name())
            self.cb.color = col
            self.cb.load_color(col)

# if __name__ == "__main__": 
#     app = QApplication(sys.argv) 
#     qb = ColorDialog() 
#     qb.show()
#     sys.exit(app.exec_())
