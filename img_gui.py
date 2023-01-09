from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import sys

from main_win_rc import *
from sub_win import *
from img_bll import *

class main_win(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_main_win()
        self.main_ui.setupUi(self)
        self.board = PaintBoard()
        self.main_ui.gridLayout.addWidget(self.board)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def closeEvent(self, *args, **kwargs):
        sys.exit(app.exec_())

class line_in(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.sub_ui = Ui_line_Form()
        self.sub_ui.setupUi(self)
        self.sub_ui.x0.setValidator(QIntValidator(-2000, 2000, self))
        self.sub_ui.y0.setValidator(QIntValidator(-2000, 2000, self))
        self.sub_ui.x1.setValidator(QIntValidator(-2000, 2000, self))
        self.sub_ui.y1.setValidator(QIntValidator(-2000, 2000, self))
        # self.move(552 - self.width(), 188)

class round_in(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.sub_ui = Ui_round_Form()
        self.sub_ui.setupUi(self)
        self.sub_ui.x0.setValidator(QIntValidator(-2000, 2000, self))
        self.sub_ui.y0.setValidator(QIntValidator(-2000, 2000, self))
        self.sub_ui.R.setValidator(QIntValidator(-2000, 2000, self))
        self.move(552 - self.width(), 378)

class point_in(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.sub_ui = Ui_point_Form()
        self.sub_ui.setupUi(self)
        self.sub_ui.x.setValidator(QIntValidator(-2000, 2000, self))
        self.sub_ui.y.setValidator(QIntValidator(-2000, 2000, self))
        self.move(552 - self.width(), 535)

class connect_win:
    def __init__(self):
        self.window = main_win()
        self.li = line_in()
        self.ri = round_in()
        self.pi = point_in()
        self.bll = img(self.window, self.li, self.ri, self.pi)

        self.connect()
        self.window.show()
        self.li.move(self.window.x() - self.li.width(), self.window.y())
        self.ri.move(self.window.x() - self.ri.width(), self.window.y() + self.li.height())
        self.pi.move(self.window.x() - self.pi.width(), self.window.y() + self.li.height() + self.ri.height())

    def connect(self):
        self.window.main_ui.line_action.triggered.connect(self.li.show)
        self.window.main_ui.round_action.triggered.connect(self.ri.show)
        self.window.main_ui.fill_action.triggered.connect(self.pi.show)
        self.window.main_ui.clear_action.triggered.connect(self.window.board.Clear)
        self.window.main_ui.load_action.triggered.connect(self.bll.img_show)
        self.window.main_ui.ehm_action.triggered.connect(self.bll.img_ehm)
        self.window.main_ui.canny_action.triggered.connect(self.bll.img_canny)
        self.li.sub_ui.ok_btn.clicked.connect(self.bll.line)
        self.ri.sub_ui.ok_btn.clicked.connect(self.bll.round)
        self.pi.sub_ui.ok_btn.clicked.connect(self.bll.fill)

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = connect_win()
    sys.exit(app.exec_())