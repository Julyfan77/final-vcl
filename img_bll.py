from PyQt5.QtWidgets import QMessageBox, QFileDialog
import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import hashlib

class img:
    def __init__(self, win, li, ri, pi):
        self.pro = ImgProcess()
        self.window = win
        self.li = li
        self.ri = ri
        self.pi = pi

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

    def img_ehm(self):
        if self.ImgPath:
            self.pro.ImgEhm(self.ImgPath)
        else:
            self.i_msg(self.window, "请先载入图像！")

    def img_canny(self):
        if self.ImgPath:
            self.pro.Canny(self.ImgPath)
        else:
            self.i_msg(self.window, "请先载入图像！")       

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

class ImgProcess:
    # def __init__(self, ImgPath, x, y):
    #     tmp = cv.imread(ImgPath, 0)
    #     self.img = cv.resize(tmp, None, fx=x, fy=y)
    def __init__(self):
        self.lowThreshold = 0
        self.max_lowThreshold = 100
        self.ratio = 3
        self.kernel_size = 3

        self.fx = 0.15
        self.fy = 0.15
        self.img = None
        self.gray = None

    # 绘制直方图
    def grayHist(self, img):
        h, w = img.shape[:2]
        pixelSequence = img.reshape([h * w, ])
        numberBins = 256
        histogram, bins, patch = plt.hist(pixelSequence, numberBins,
                                          facecolor='black', histtype='bar')
        plt.xlabel("gray label")
        plt.ylabel("number of pixels")
        plt.axis([0, 255, 0, np.max(histogram)])
        plt.show()

    # 计算灰度直方图
    def calcGrayHist(self, I):
        h, w = I.shape[:2]
        grayHist = np.zeros([256], np.uint64)
        for i in range(h):
            for j in range(w):
                grayHist[I[i][j]] += 1
        return grayHist

    #全局直方图均衡化
    def equalHist(self, img):
        # 灰度图像矩阵的高、宽
        h, w = img.shape
        # 第一步：计算灰度直方图
        grayHist = self.calcGrayHist(img)
        # 第二步：计算累加灰度直方图
        zeroCumuMoment = np.zeros([256], np.uint32)
        for p in range(256):
            if p == 0:
                zeroCumuMoment[p] = grayHist[0]
            else:
                zeroCumuMoment[p] = zeroCumuMoment[p - 1] + grayHist[p]
        # 第三步：根据累加灰度直方图得到输入灰度级和输出灰度级之间的映射关系
        outPut_q = np.zeros([256], np.uint8)
        cofficient = 256.0 / (h * w)
        for p in range(256):
            q = cofficient * float(zeroCumuMoment[p]) - 1
            if q >= 0:
                outPut_q[p] = np.math.floor(q)
            else:
                outPut_q[p] = 0
        # 第四步：得到直方图均衡化后的图像
        equalHistImage = np.zeros(img.shape, np.uint8)
        for i in range(h):
            for j in range(w):
                equalHistImage[i][j] = outPut_q[img[i][j]]
        return equalHistImage

    def ImgEhm(self, ImgPath):
        tmp = cv.imread(ImgPath, 0)
        self.img = cv.resize(tmp, None, fx=self.fx, fy=self.fy)
        # 全局直方图均衡化
        equa = self.equalHist(self.img)
        # 限制对比度的自适应直方图均衡化
        # 创建CLAHE对象
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # 限制对比度的自适应阈值均衡化
        dst = clahe.apply(self.img)
        # 绘制灰度直方图
        self.grayHist(self.img)
        self.grayHist(dst)
        self.grayHist(equa)
        # 使用OpenCV提供的全局直方图均衡化函数实现
        # equa = cv.equalizeHist(self.img)
        # 显示
        # cv.namedWindow("img",0)
        # cv.imshow("img", self.img)
        # cv.imshow("equa", equa)
        tmp = np.hstack((self.img, dst, equa))
        cv.imshow('img/dst/equa', tmp)
        cv.waitKey()

    def CannyThreshold(self, lowThreshold):
        detected_edges = cv2.GaussianBlur(self.gray, (3, 3), 0)
        detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * self.ratio, apertureSize=self.kernel_size)
        dst = cv2.bitwise_and(self.img, self.img, mask=detected_edges)  # just add some colours to edges from original image.
        cv2.imshow('canny demo', dst)

    def Canny(self, ImgPath):
        tmp = cv2.imread(ImgPath)
        self.img = cv2.resize(tmp, None, fx=self.fx, fy=self.fy)
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        cv2.namedWindow('canny demo')

        cv2.createTrackbar('Min threshold', 'canny demo', self.lowThreshold, self.max_lowThreshold, self.CannyThreshold)

        self.CannyThreshold(0)  # initialization
        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()



if __name__ == '__main__':
    run = img()