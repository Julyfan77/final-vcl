from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import sys

from Ui_mainwin import *
from help import *
from Ui_color import *
from load_save import *
class main_win(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.board = PaintBoard()
        self.main_ui.gridLayout.addWidget(self.board)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def closeEvent(self, *args, **kwargs):
        sys.exit(app.exec_())


class connect_win:
    def __init__(self):
        self.window = main_win()
        self.bll = img(self.window)
        self.color=ColorDialog(self.window.x()+700,self.window.y()+700)
        #self.color.show()
        self.connect()
        self.window.show()
        
    def connect(self):
        self.window.main_ui.color_action.triggered.connect(self.color.show)  
        self.window.main_ui.open_action.triggered.connect(self.bll.img_show)       
        #pass
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = connect_win()
    sys.exit(app.exec_())