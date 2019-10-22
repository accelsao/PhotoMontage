"""
Watershed segmentation
=========
This program demonstrates the watershed segmentation algorithm
in OpenCV: watershed().
Usage
-----
watershed.py [image filename]
Keys
----
  1-7   - switch marker color
  SPACE - update segmentation
  r     - reset
  a     - toggle autoupdate
  ESC   - exit
"""
import sys
import cv2 as cv
import numpy as np
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QFileDialog, QApplication


class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv.imshow(self.windowname, self.dests[0])

    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()


class App:
    def __init__(self, fn):
        self.img = cv.imread(fn)
        if self.img is None:
            raise Exception('Failed to load image file: {}'.format(fn))

        h, w = self.img.shape[:2]
        self.markers = np.zeros((h, w), np.int32)
        self.markers_vis = self.img.copy()
        self.cur_marker = 1
        self.colors = np.int32(list(np.ndindex(2, 2, 2))) * 255

        self.auto_update = True
        self.sketch = Sketcher('img', [self.markers_vis, self.markers], self.get_colors)

    def get_colors(self):
        return list(map(int, self.colors[self.cur_marker])), self.cur_marker

    def watershed(self):
        m = self.markers.copy()
        cv.watershed(self.img, m)
        overlay = self.colors[np.maximum(m, 0)]
        vis = cv.addWeighted(self.img, 0.5, overlay, 0.5, 0.0, dtype=cv.CV_8UC3)
        cv.imshow('watershed', vis)

    def run(self):
        while cv.getWindowProperty('img', 0) != -1 or cv.getWindowProperty('watershed', 0) != -1:
            ch = cv.waitKey(50)
            if ch == 27:
                break
            if ord('1') <= ch <= ord('7'):
                self.cur_marker = ch - ord('0')
                print('marker: ', self.cur_marker)
            if ch == ord(' ') or (self.sketch.dirty and self.auto_update):
                self.watershed()
                self.sketch.dirty = False
            if ch in [ord('a'), ord('A')]:
                self.auto_update = not self.auto_update
                print('auto_update if', ['off', 'on'][self.auto_update])
            if ch in [ord('r'), ord('R')]:
                self.markers[:] = 0
                self.markers_vis[:] = self.img
                self.sketch.show()
        cv.destroyAllWindows()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.img = None
        self.pic = None
        self.btnOpen = None
        self.btnSave = None
        self.btnProcess = None
        self.btnQuit = None
        self.initUI()


    def initUI(self):
        self.pic = QLabel()
        self.btnQuit = QPushButton('Quit', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnSave = QPushButton('Save', self)
        self.btnOpen = QPushButton('Open', self)
        self.setGeometry(500, 300, 300, 300)

        layout = QGridLayout(self)
        layout.addWidget(self.pic, 0, 0, 1, 0)
        layout.addWidget(self.btnOpen, 1, 0)
        layout.addWidget(self.btnSave, 1, 1)
        layout.addWidget(self.btnProcess, 1, 2)
        layout.addWidget(self.btnQuit, 1, 3)

        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)

    def openSlot(self):
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './images', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        self.img = cv.imread(fileName)
        self.refreshShow()

    def saveSlot(self):
        filename, tmp = QFileDialog.getOpenFileName(self, 'Save Image', './images',
                                                    '*.png *.jpg *.bmp', '*.png')
        if filename is '':
            return
        cv.imwrite(filename, self.img)

    def processSlot(self):
        self.img = cv.blur(self.img, (5, 5))
        self.refreshShow()

    def refreshShow(self):
        # 提取圖像的尺寸和通道, 用於將opencv下的image轉換成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 將Qimage顯示出來
        self.pic.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


    # print(__doc__)
    #
    # # try:
    # #     fn = sys.argv[1]
    # # except:
    # #     fn = 'fruits.jpg'
    # fn = 'images/001.jpg'
    # App(cv.samples.findFile(fn)).run()
#
# # cv2.imshow('img', img)
# _, img_otsu = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
# cv2.imshow('img_org', img)
# contours, hierarchy = cv2.findContours(img_otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (5, 0, 0), 1)
# # print(contours)
# # print(hierarchy)
# cv2.imshow('otsu', img_otsu)
# cv2.imshow('img', img)
# cv2.waitKey(0)
