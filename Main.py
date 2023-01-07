# coding=utf-8
import wx
import os
import pickle
import _thread as thread
import pygame
import cv2 as cv
import Model
import Tools


class SDLThread:
    def __init__(self, panel, size):
        self.panel = panel
        self.size = size
        self.main_screen = pygame.display.set_mode(size)
        self.main_screen.fill((255, 255, 255))
        self.shapes = []
        self.lines = []
        self.current_num = 0
        self.color = (0, 0, 0)
        self.state = 0  # 0-等待绘制 1-正在绘制 2-选择模式
        # 绑定按钮事件
        self.panel.identify_button.Bind(wx.EVT_BUTTON, self.get_shape)
        self.panel.choose_button.Bind(wx.EVT_BUTTON, self.choose_event)
        self.panel.draw_button.Bind(wx.EVT_BUTTON, self.draw_event)
        self.panel.color_button.Bind(wx.EVT_BUTTON, self.color_event)
        self.panel.save_button.Bind(wx.EVT_BUTTON, self.save_event)
        self.panel.open_button.Bind(wx.EVT_BUTTON, self.open_event)
        self.panel.listBox.Bind(wx.EVT_BUTTON, self.tuceng_event)

    def add_point(self, pos):
        if len(self.lines) > 0:
            self.lines[-1].append(pos)

    def choose_event(self, event):
        if len(self.lines) > 0:
            return
        self.state = 2
        self.panel.set_draw_button_label("绘图")

    def color_event(self, event):
        dlg = wx.ColourDialog(self.panel)
        dlg.GetColourData().SetChooseFull(True)  # 创建颜色对象数据
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour()  # 根据选择设置颜色
            self.color = color[0], color[1], color[2]
        dlg.Destroy()

    def draw_event(self, event):
        if self.state == 2:
            self.state = 0
            self.current_num = len(self.shapes)
            self.panel.set_draw_button_label("撤销")
            self.panel.set_text("请绘制图形", "")
        elif self.state == 0:
            if len(self.lines) > 0:
                self.lines.pop()

    def save_event(self, event):
        with wx.FileDialog(self.panel, "保存文件", wildcard="画板文件 (*)|*|PNG图像 (*.png)|*.png", style=wx.FD_SAVE) as fd:
            if fd.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fd.GetPath()
            file_type = fd.GetFilterIndex()
            try:
                if file_type == 0:
                    with open(pathname, 'wb') as f:
                        pickle.dump(self.shapes, f)
                        f.close()
                        self.panel.set_text("文件保存成功", None)
                elif file_type == 1:
                    pygame.image.save(self.main_screen, pathname)
            except IOError:
                self.panel.set_text("文件保存出错", None)

    def open_event(self, event):
        with wx.FileDialog(self.panel, "保存文件", wildcard=u"画板文件 (*)|*", style=wx.FD_OPEN) as fd:
            if fd.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fd.GetPath()
            try:
                with open(pathname, 'rb') as f:
                    self.shapes = pickle.load(f)
                    self.current_num = len(self.shapes)
                    self.panel.set_text("读取文件成功", None)
            except IOError:
                self.panel.set_text("读取文件出错", None)

    def draw_lines(self, screen):
        for line in self.lines:
            if len(line) > 1:
                pygame.draw.lines(screen, self.color, False, line, 1)

    def draw(self):
        self.main_screen.fill((255, 255, 255))
        for index, shape in enumerate(self.shapes):
            shape.draw(self.main_screen, index == self.current_num)
        self.draw_lines(self.main_screen)
        pygame.display.flip()

    def get_shape(self, event):
        if self.state != 0 or len(self.lines) == 0:
            return
        screen = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        screen.fill((255, 255, 255, 0))
        self.draw_lines(screen)
        pygame.image.save(screen, "s.png")
        img = cv.imread("s.png")
        # 二值化图像
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        out_binary, contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            # 轮廓逼近
            epsilon = 0.03 * cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)

            # 分析几何形状
            corners = len(approx)
            # print approx
            if corners == 3:
                points = [(p[0][0], p[0][1]) for p in approx]
                self.shapes.append(Model.Triangle(points, self.color, self.panel.get_input()))
            elif corners == 4:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                points = [(p[0], p[1]) for p in box]
                a = Tools.get_distance(points[0], points[1])
                b = Tools.get_distance(points[0], points[3])
                if abs(a - b) / max(a, b) < 0.15:
                    points[1] = (b / a * points[1][0] + (1 - b / a) * points[0][0],
                                 b / a * points[1][1] + (1 - b / a) * points[0][1])
                    points[2] = (b / a * points[2][0] + (1 - b / a) * points[3][0],
                                 b / a * points[2][1] + (1 - b / a) * points[3][1])
                self.shapes.append(Model.Rect(points, self.color, self.panel.get_input()))
            elif corners >= 7:
                mm = cv.moments(cnt)
                cx = int(mm['m10'] / mm['m00'])
                cy = int(mm['m01'] / mm['m00'])
                radius_list = map(lambda point: Tools.get_distance(point[0], (cx, cy)), approx)
                radius = int(sum(radius_list) / len(radius_list))
                self.shapes.append(Model.Circle((cx, cy), radius, self.color, self.panel.get_input()))
        self.lines = []
        if self.current_num != len(self.shapes):
            self.current_num = len(self.shapes)
            self.panel.set_text("识别结果：" + self.shapes[-1].get_shape(), "")

    def run(self):
        while True:
            if not pygame.display.get_init():
                break
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 鼠标单击左键
                if event.button == 1:
                    # 处于等待绘制状态
                    if self.state == 0:
                        self.state = 1
                        self.lines.append([])
                    # 处于正在绘制状态
                    elif self.state == 1:
                        self.state = 0
                    elif self.state == 2:
                        flag = True
                        for index, shape in enumerate(self.shapes):
                            if shape.judge_point(pos):
                                self.current_num = index
                                self.panel.set_text("选择的图形形状：" + shape.get_shape(), shape.info)
                                flag = False
                                break
                        if flag:
                            self.current_num = len(self.shapes)
                # 鼠标单击右键
                elif event.button == 3:
                    pass
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if self.state == 1 and pos[1] < self.size[1]:
                    self.add_point(pos)
            if self.current_num < len(self.shapes):
                self.shapes[self.current_num].info = self.panel.get_input()
                self.shapes[self.current_num].color = self.color
            self.draw()

    def start(self):
        thread.start_new_thread(self.run, ())


class SDLPanel(wx.Panel):
    def __init__(self, parent, panel_id, panel_size):
        wx.Panel.__init__(self, parent, panel_id, size=panel_size)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        self.thread = SDLThread(parent, panel_size)
        self.thread.start()


class MyFrame(wx.Frame):
    def __init__(self, parent, panel_id, title, panel_size, win_size):
        wx.Frame.__init__(self, parent, panel_id, title, size=win_size)
        self.SetMaxSize(win_size)
        SampleList=["background","1","2","3"]
        self.choose_button = wx.Button(self, label="选择", pos=(10, 610), size=(70, 30))
        self.draw_button = wx.Button(self, label="撤销", pos=(90, 610), size=(70, 30))
        self.identify_button = wx.Button(self, label="识别", pos=(170, 610), size=(70, 30))
        self.color_button = wx.Button(self, label="颜色", pos=(250, 610), size=(70, 30))
       # self.input_box = wx.TextCtrl(self, -1, '', pos=(330, 610), size=(210, 30))
        self.save_button = wx.Button(self, label="保存", pos=(410, 610), size=(70, 30))
        self.open_button = wx.Button(self, label="打开", pos=(490, 610), size=(70, 30))
        #self.info_box = wx.TextCtrl(self,  -1, '', pos=(0, 650), size=(win_size[0], 30))
       # self.info_box.SetEditable(False)
        self.pnlSDL = SDLPanel(self, -1, panel_size)
        self.listBox = wx.ListBox(self.pnlSDL, -1,(330,620),(80,120), SampleList,wx.LB_SINGLE)
        self.listBox.SetSelection(3)


    def get_input(self):
        return self.input_box.GetValue()

    def set_draw_button_label(self, label):
        self.draw_button.SetLabel(label)

    def set_text(self, info, text):
        if text is not None:
            self.input_box.SetValue(text)
        self.info_box.SetValue(info)


def main():
    app = wx.App()
    frame = MyFrame(None, wx.ID_ANY, "DrawingBoard", (600, 600), (815, 715))
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
