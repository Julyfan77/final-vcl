import copy

from PyQt5.Qt import QPixmap, QPainter, QPen, QBrush
from PyQt5.QtGui import QImage

import mymath
from Ui_color import *
from drawitems import *

nowcol = Qt.black
nowwid = 1
CHOOSE = 0


class PaintBoard(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.bg_loaded = False
        self.interact = None
        # self.lbl=QLabel("图片",self)
        self.pixmap = QPixmap(200, 200)
        self.pixmap.fill(Qt.white)
        self.img = QImage(self.pixmap.toImage())
        self.bg = None
        # self.lbl.setPixmap(self.pixmap)
        self.mode = CHOOSE  # 0-choose,1-straight,2-circle,3-rec,4-fillrec,5-fillcircle,6-curve
        # 7-pingyi,8-rotate
        self.pen = QPainter()
        self.setMouseTracking(True)
        self.linexy = []
        self.recpoint = []
        self.fill_recpoint = []
        self.style = 0
        self.brushstyle = 0
        # self.actions=[]
        self.drawitems = []
        self.col = Qt.black
        self.wid = 1
        self.currentid = 0
        self.undolst = []
        self.rotatepot = []
        self.cb = None

    def choose(self):
        self.mode = CHOOSE

    def paintEvent(self, paintEvent):
        # print("paint event !!!")
        self.pixmap = self.pixmap.scaled(self.width(), self.height())
        self.pen.begin(self)
        # self.pen.drawPixmap(0, 0, self.pixmap)
        self.img = QImage(self.pixmap.toImage())
        self.pen.drawImage(0, 0, self.img)
        self.pen.end()

    def load_img(self, img):
        self.bg = img
        self.pixmap = QPixmap(img)
        w = self.pixmap.width()
        h = self.pixmap.height()
        self.bg_loaded = True
        self.update()

    def save_img(self, img):
        self.img.save(img)

    # def myRemovePic(self):
    #     self.lbl.setPixmap(QPixmap(""))
    # def myAddPic(self):
    #     self.lbl.setPixmap(self.pixmap)

    def drawPoint(self, x, y, col=Qt.black, wid=1, style=0):
        m = int(self.width() / 2) + x
        n = int(self.height() / 2) - y

        self.pen.begin(self.pixmap)
        mypen = QPen(col, wid)
        self.pen.setPen(mypen)
        self.pen.drawPoint(x, y)
        self.pen.end()
        self.update()

    def mouseDoubleClickEvent(self, event):
        self.mode = CHOOSE

        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        x = event.x()
        y = event.y()
        n = len(self.drawitems)
        if n == 0:
            return
        nearid = 0
        mindis = getdis_2(x, y, self.drawitems[0].Gx, self.drawitems[0].Gy)
        self.interact = 0
        for i in range(1, n):
            if getdis_2(x, y, self.drawitems[i].Gx, self.drawitems[i].Gy) < mindis:
                self.interact = i
                mindis = getdis_2(x, y, self.drawitems[i].Gx, self.drawitems[i].Gy)
        # print(f'object {self.drawitems[self.interact]} chosen!')
        # print(self.drawitems[nearid].Gx,self.drawitems[nearid].Gy,5)
        self.myupdate()
        # self.drawfillRound2(self.drawitems[nearid].Gx,self.drawitems[nearid].Gy,5)

    def mycopy(self):
        self.undolst.append([x.mycopy() for x in self.drawitems])

    def mousePressEvent(self, event):
        nowcol = self.col
        nowwid = self.wid
        x = event.x()
        y = event.y()
        text = "x: {0}, y: {1}".format(x, y)
        if self.mode == STRAIGHT:
            if event.button() == Qt.LeftButton:
                if len(self.linexy) == 0:
                    self.linexy.append([x, y])

                elif len(self.linexy) == 1:
                    self.drawitems.append(line_drawitem([[self.linexy[0][0],
                                                          self.linexy[0][1]], [x, y]],
                                                        nowcol, copy.deepcopy(nowwid), copy.deepcopy(self.style), self))
                    self.mycopy()
                    self.draw_line(self.linexy[0][0], self.linexy[0][1], x, y)

                    # self.actions.append(["line",self.linexy[0][0],
                    #         self.linexy[0][1],x,y,nowcol,nowwid,self.style])
                    self.linexy.clear()
        if self.mode == REC:
            # print("rec")
            if event.button() == Qt.LeftButton:
                self.recpoint.append([x, y])
            elif event.button() == Qt.RightButton:
                # print("???")
                if len(self.recpoint) == 0:
                    pass
                else:
                    thisrec = copy.deepcopy(self.recpoint)
                    self.drawitems.append(rec_drawitem(thisrec, nowcol, nowwid,
                                                       self.style, self))
                    self.mycopy()
                    # self.actions.append(["rec",thisrec,nowcol,nowwid,self.style])
                    # self.win.add("rec")
                    for iter in range(len(self.recpoint)):
                        self.draw_line(self.recpoint[(iter) % len(self.recpoint)][0],
                                       self.recpoint[(iter) % len(self.recpoint)][1],
                                       self.recpoint[(iter + 1) % len(self.recpoint)][0],
                                       self.recpoint[(iter + 1) % len(self.recpoint)][1])
                self.recpoint.clear()

        if self.mode == CIRCLE:
            if event.button() == Qt.LeftButton:
                if len(self.linexy) == 0:
                    self.linexy.append([x, y])
                elif len(self.linexy) == 1:
                    self.linexy.append([x, y])
                    r = math.sqrt((self.linexy[0][0] - x) * (self.linexy[0][0] - x) +
                                  (self.linexy[0][1] - y) * (self.linexy[0][1] - y))
                    self.drawRound(self.linexy[0][0], self.linexy[0][1], r)
                    # self.actions.append(["circle",self.linexy[0][0],
                    #     self.linexy[0][1],r,nowcol,nowwid])
                    self.drawitems.append(circle_drawitem(
                        self.linexy[0][0],
                        self.linexy[0][1], r, nowcol, nowwid, self
                    ))
                    self.mycopy()
                    self.linexy.clear()
        if self.mode == FILLCIRCLE:
            if event.button() == Qt.LeftButton:
                if len(self.linexy) == 0:
                    self.linexy.append([x, y])

                elif len(self.linexy) == 1:
                    self.linexy.append([x, y])

                    r = math.sqrt((self.linexy[0][0] - x) * (self.linexy[0][0] - x) +
                                  (self.linexy[0][1] - y) * (self.linexy[0][1] - y))

                    self.drawitems.append(fill_circle_drawitem(
                        self.linexy[0][0], self.linexy[0][1], r, self.col,
                        self.wid, self.brushstyle, self))
                    self.mycopy()
                    self.drawfillRound(self.linexy[0][0], self.linexy[0][1], r)
                    self.linexy.clear()

                    print(len(self.undolst))
        if self.mode == FILLREC:  # fill_rec
            if event.button() == Qt.LeftButton:
                if len(self.fill_recpoint) == 0:
                    self.fill_recpoint.append([x, y])
                elif len(self.fill_recpoint) == 1:
                    self.fill_recpoint.append([x, y])
                    self.draw_fill_rec(self.fill_recpoint[0][0],
                                       self.fill_recpoint[0][1], self.fill_recpoint[1][0],
                                       self.fill_recpoint[1][1])
                    self.drawitems.append(fill_rec_drawitem(self.fill_recpoint[0][0],
                                                            self.fill_recpoint[0][1], self.fill_recpoint[1][0],
                                                            self.fill_recpoint[1][1], nowcol, nowwid, self.brushstyle,
                                                            self
                                                            ))
                    self.mycopy()

                    # self.actions.append(["fill_rec",self.fill_recpoint[0][0],
                    #     self.fill_recpoint[0][1],self.fill_recpoint[1][0],
                    #     self.fill_recpoint[1][1],nowcol,nowwid,self.brushstyle])
                    self.fill_recpoint.clear()
        if self.mode == CURVE:  # draw curve for free

            col = self.col
            wid = self.wid
            self.drawPoint(x, y, col, wid)
            self.drawitems.append(mypoint(x, y, col, wid, self))
            self.mycopy()
            # self.actions.append(["point",x,y,nowcol,nowwid])
        self.update()
        if self.mode == 7:
            if event.button() == Qt.LeftButton:
                id = self.interact
                if id == None:
                    return
                dx = -self.drawitems[id].Gx + x
                dy = -self.drawitems[id].Gy + y
                self.drawitems[id].move(dx, dy)
                self.mycopy()
                self.myupdate()
        if self.mode == 8:
            if event.button() == Qt.LeftButton:
                id = self.interact
                if id is None:
                    return
                if len(self.rotatepot) == 0:
                    self.rotatepot.append([x, y])
                elif len(self.rotatepot) == 1:

                    rotation = mymath.getarc(self.rotatepot[0][0], self.rotatepot[0][1],
                                             self.drawitems[id].Gx, self.drawitems[id].Gy,
                                             x, y
                                             )
                    self.drawitems[id].rotate(rotation)
                    self.mycopy()
                    self.rotatepot.clear()
                    self.myupdate()

    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        text = "x: {0}, y: {1}".format(x, y)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        if event.button() == Qt.LeftButton and self.mode == 6:
            col = self.col
            wid = self.wid
            self.drawPoint(x, y, col, wid)
        text = "x:{0},y:{1}".format(x, y)
        # self.ui.label_2.setText(text)

    def draw_line_action(self):
        self.mode = 1
        self.linexy.clear()

    def draw_line(self, x0, y0, x1, y1):
        col = self.col
        wid = self.wid
        self.pen.begin(self.pixmap)
        # print(wid)
        mypen = QPen(col, wid, Qt.SolidLine)
        if self.style == 0:
            mypen = (QPen(col, wid, Qt.SolidLine))
            self.pen.setPen(mypen)
        elif self.style == 1:
            mypen = QPen(col, wid, Qt.DashLine)
            self.pen.setPen(mypen)
        elif self.style == 2:
            mypen = QPen(col, wid, Qt.CustomDashLine)
            mypen.setDashPattern([1, 4, 5, 4])
            self.pen.setPen(mypen)
        elif self.style == 3:
            # print("style is dotline,wid is ?")
            mypen = QPen(col, wid, Qt.DotLine)
            self.pen.setPen(mypen)

        self.pen.drawLine(x0, y0, x1, y1)
        self.pen.end()

    def draw_circle_action(self):
        self.mode = 2
        self.linexy.clear()

    def CirclePlot(self, xc, yc, x, y):
        col = self.col
        wid = self.wid
        self.drawPoint(x + xc, y + yc, col, wid)
        self.drawPoint(-x + xc, y + yc, col, wid)
        self.drawPoint(x + xc, -y + yc, col, wid)
        self.drawPoint(-x + xc, -y + yc, col, wid)
        self.drawPoint(y + xc, x + yc, col, wid)
        self.drawPoint(y + xc, -x + yc, col, wid)
        self.drawPoint(-y + xc, x + yc, col, wid)
        self.drawPoint(-y + xc, -x + yc, col, wid)

    def drawRound(self, xc, yc, r):
        x = 0
        y = r
        d = 3 - 2 * r
        self.CirclePlot(xc, yc, x, y)
        while x < y:
            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1
            x += 1
            self.CirclePlot(xc, yc, x, y)

    def drawfillRound(self, xc, yc, r):
        nowcol = self.col
        nowwid = self.wid
        self.pen.begin(self.pixmap)
        # print(wid)
        mypen = QBrush()
        mypen.setColor(nowcol)
        if self.brushstyle == 0:
            mypen.setStyle(Qt.SolidPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 1:
            mypen.setStyle(Qt.HorPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 2:
            mypen.setStyle(Qt.BDiagPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 3:

            mypen.setStyle(Qt.Dense1Pattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 4:

            mypen.setStyle(Qt.RadialGradientPattern)
            self.pen.setBrush(mypen)
        self.pen.drawEllipse(xc - r, yc - r, 2 * r, 2 * r)

        self.pen.end()
        self.update()

    def drawfillRound2(self, xc, yc, r):
        col = Qt.red
        self.pen.begin(self.pixmap)

        mypen = QBrush()
        mypen.setColor(col)

        mypen.setStyle(Qt.SolidPattern)
        self.pen.setBrush(mypen)

        self.pen.drawEllipse(xc - r, yc - r, 2 * r, 2 * r)
        self.pen.end()
        self.update()

    def draw_rec_action(self):
        self.mode = 3

        self.recpoint.clear()

    def draw_fill_rec_action(self):
        self.mode = 4
        self.fill_recpoint.clear()

    def draw_fill_circle_action(self):
        self.mode = 5
        self.linexy.clear()

    def draw_curve_action(self):
        self.mode = 6
        # self.linexy.clear()

    def draw_fill_rec(self, x0, y0, x1, y1):
        col = self.col
        wid = self.wid
        self.pen.begin(self.pixmap)
        # print(wid)
        mypen = QBrush()
        mypen.setColor(col)
        if self.brushstyle == 0:
            mypen.setStyle(Qt.SolidPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 1:
            mypen.setStyle(Qt.HorPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 2:
            mypen.setStyle(Qt.BDiagPattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 3:

            mypen.setStyle(Qt.Dense1Pattern)
            self.pen.setBrush(mypen)
        elif self.brushstyle == 4:

            mypen.setStyle(Qt.RadialGradientPattern)
            self.pen.setBrush(mypen)
        self.pen.drawRect(x0, y0, x1 - x0, y1 - y0)

        self.pen.end()

    def action1(self):
        self.wid = 1

    def action2(self):
        self.wid = 2

    def action3(self):
        self.wid = 3

    def action5(self):
        self.wid = 5

    def action4(self):
        self.wid = 4

    def style1(self):
        self.style = 1

    def style2(self):
        self.style = 2

    def style3(self):
        self.style = 3

    def style_outline(self):
        self.style = 0

    def brushstyle1(self):
        self.brushstyle = 1

    def brushstyle2(self):
        self.brushstyle = 2

    def brushstyle3(self):
        self.brushstyle = 3

    def brushstyle0(self):
        self.brushstyle = 0

    def brushstyle4(self):
        self.brushstyle = 4

    def pingyi(self):
        self.mode = 7

    def rotate(self):
        self.rotatepot.clear()
        self.mode = 8

    def myupdate(self):
        self.pixmap.fill(Qt.white)
        if self.bg:
            self.load_img(self.bg)
        n = len(self.drawitems)
        for i in range(n):
            self.drawitems[i].draw()
            if i == self.interact:
                self.drawfillRound2(self.drawitems[i].Gx, self.drawitems[i].Gy, 5)
        self.update()

    def undo(self):
        print(self.undolst)
        if len(self.undolst) == 0:
            print("\n \n none to undo")
            return
        if len(self.undolst) == 1:
            self.pixmap.fill(Qt.white)

            if self.bg:
                self.load_img(self.bg)
            self.update()
            del self.undolst[-1]
            self.drawitems.clear()
            return
        allitems = self.undolst[-2]
        self.drawitems = allitems
        # print(len(allitems))
        see = []
        for i in range(len(self.undolst)):
            see.append(len(self.undolst[i]))
        # print(see)
        n = len(allitems)
        self.pixmap.fill(Qt.white)
        if self.bg:
            self.load_img(self.bg)
        for i in range(n):
            self.cb.load_color(allitems[i].col)
            allitems[i].draw()
        self.update()
        del self.undolst[-1]


class colorBoard(PaintBoard):
    def __init__(self, pb):
        QWidget.__init__(self)
        super().__init__()
        self.pixmap = QPixmap(1, 1)
        self.pixmap.fill(Qt.black)
        self.img = QImage(self.pixmap.toImage())
        # self.lbl.setPixmap(self.pixmap)
        self.pen = QPainter()
        self.col = QColor(255, 255, 255, 127)
        self.pb = pb

    def paintEvent(self, paintEvent):
        return super().paintEvent(paintEvent)

    def load_color(self, col):
        print(col)
        # self.widget.setStyleSheet('QWidget {background-color:%s}'%col.name())
        self.pb.col = col
        self.pixmap.fill(col)
        self.update()
