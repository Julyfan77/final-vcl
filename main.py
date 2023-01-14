from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
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
        model = QStandardItemModel()
        #self.main_ui.dwgDrawings
        self.board = PaintBoard()
        self.cb=colorBoard(self.board)
        self.main_ui.gridLayout.addWidget(self.board)
        self.main_ui.colorboard.addWidget(self.cb)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def closeEvent(self, *args, **kwargs):
        sys.exit(app.exec_())

    # def add(self,type):
    #     item = QStandardItem()
    #     item.setEditable(False)
    #     index = self.indexFromItem(item).row()
    #     typeItem = QStandardItem(type)
    #     typeItem.setEditable(False)
    #     self.setItem(index, self.TYPE, typeItem)
    #     self.appendRow(item)
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
        self.window.main_ui.choose_action.triggered.connect(self.window.board.choose)   
        self.window.main_ui.line_action.triggered.connect(
            self.window.board.draw_line_action)
        self.window.main_ui.curve_action.triggered.connect(
            self.window.board.draw_curve_action)  
        self.window.main_ui.circle_action.triggered.connect(
            self.window.board.draw_circle_action)
        self.window.main_ui.rec_action.triggered.connect(
            self.window.board.draw_rec_action)
        self.window.main_ui.fill_rect_action.triggered.connect(
            self.window.board.draw_fill_rec_action)
        self.window.main_ui.fill_circle_action.triggered.connect(
            self.window.board.draw_fill_circle_action)
        self.window.main_ui.action1.triggered.connect(self.window.board.action1)
        self.window.main_ui.action2.triggered.connect(self.window.board.action2)
        self.window.main_ui.action3.triggered.connect(self.window.board.action3)
        self.window.main_ui.action4.triggered.connect(self.window.board.action4)
        self.window.main_ui.action5.triggered.connect(self.window.board.action5)
        self.window.main_ui.style1.triggered.connect(self.window.board.style1)
        self.window.main_ui.style2.triggered.connect(self.window.board.style2)
        self.window.main_ui.style3.triggered.connect(self.window.board.style3)
        self.window.main_ui.style_outline.triggered.connect(
            self.window.board.style_outline)
        self.window.main_ui.brushstyle0.triggered.connect(self.window.board.brushstyle0)
        self.window.main_ui.brushstyle1.triggered.connect(self.window.board.brushstyle1)
        self.window.main_ui.brushstyle2.triggered.connect(self.window.board.brushstyle2)
        self.window.main_ui.brushstyle3.triggered.connect(self.window.board.brushstyle3)
        self.window.main_ui.undo_action.triggered.connect(self.window.board.undo)
        #self.window.main_ui.brushstyle4.triggered.connect(self.window.board.brushstyle4)
       # self.window.main_ui.action5.triggered.connect(self.window.board.action5)
       
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = connect_win()
    sys.exit(app.exec_())