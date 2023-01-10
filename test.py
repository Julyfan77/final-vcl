import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton
from PyQt5.QtGui import QPixmap

class MyClass(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.lbl=QLabel("图片",self)
        self.pm=QPixmap("C:/Users/Dionyus/Pictures/moments/4aaed03b0424f813c3d5b97d49dd04f.jpg")
        self.lbl.setPixmap(self.pm)
        self.lbl.resize(300,200)
        self.lbl.setScaledContents(True)

        self.show()
    def myRemovePic(self):
        self.lbl.setPixmap(QPixmap(""))
    def myAddPic(self):
        self.lbl.setPixmap(self.pm)
if __name__=="__main__":
    app=QApplication(sys.argv)
    mc=MyClass()
    app.exec_()