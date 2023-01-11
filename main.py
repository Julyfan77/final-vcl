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
        self.cb=colorBoard()
        self.main_ui.gridLayout.addWidget(self.board)
        self.main_ui.colorboard.addWidget(self.cb)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def closeEvent(self, *args, **kwargs):
        sys.exit(app.exec_())


class connect_win:
    def __init__(self):
        self.window = main_win()
        self.bll = img(self.window)
        self.mypen=0 #0-pen
        self.mywidth=1
        #self.linetool=myLineTool()
        self.colordialog=ColorDialog(self.window.x()+700,self.window.y()+700,self.window.cb)
        
        self.connect()
        self.window.show()
        
    def connect(self):
        self.window.main_ui.color_action.triggered.connect(self.colordialog.showDialog)  
        self.window.main_ui.open_action.triggered.connect(self.bll.img_show)
        self.window.main_ui.save_action.triggered.connect(self.bll.img_save)   
        self.window.main_ui.line_action.triggered.connect(self.window.board.draw_line_action) 
    
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = connect_win()
    sys.exit(app.exec_())