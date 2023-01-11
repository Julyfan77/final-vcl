from PyQt5.QtWidgets import QMessageBox, QFileDialog

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
        file_Name, file_type = QFileDialog.getOpenFileName(self.window,"选取文件","C:","All Files (*)")
        
        return file_Name

    def img_show(self):
        self.ImgPath = self.f_msg()
        self.window.board.load_img(self.ImgPath)
    def img_save(self):
        tmppath= QFileDialog.getSaveFileName(self.window,"save file","C:" ,"All Files (*)")   

        self.window.board.save_img(tmppath[0])

        
