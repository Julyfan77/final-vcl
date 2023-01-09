from PyQt5.QtWidgets import QMessageBox, QFileDialog
import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
class img:
    def __init__(self, win):
        #self.pro = ImgProcess()
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
        self.window.board.pixmap.show()
