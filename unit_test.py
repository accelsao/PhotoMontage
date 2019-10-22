import sys
import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget)


class win(QWidget):
    def __init__(self):
        super(win, self).__init__()
        self.img = None
        self.initUI()

    def initUI(self):
        self.label = QLabel()
        self.btnQuit = QPushButton('Quit', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnSave = QPushButton('Save', self)
        self.btnOpen = QPushButton('Open', self)
        self.setGeometry(500, 300, 300, 300)

        # 佈局設定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0, 1, 0)
        layout.addWidget(self.btnOpen, 1, 0)
        layout.addWidget(self.btnSave, 1, 1)
        layout.addWidget(self.btnProcess, 1, 2)
        layout.addWidget(self.btnQuit, 1, 3)

        # 信號與槽連接, PyQt5與Qt5相同, 信號可綁定普通成員函數
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)

    def openSlot(self):
        # 調用打開文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './images', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        self.img = cv.imread(fileName)
        self.refreshShow()

    def saveSlot(self):
        # 調用存儲文件dialog
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './images', '*.png *.jpg *.bmp', '*.png')

        if fileName is '':
            return
        if self.img.size == 1:
            return

        # 調用opencv寫入圖像
        cv.imwrite(fileName, self.img)

    def processSlot(self):
        if self.img.size == 1:
            return

        # 對圖像做模糊處理, 窗口設定爲5x5
        self.img = cv.blur(self.img, (5, 5))

        self.refreshShow()

    def refreshShow(self):
        # 提取圖像的尺寸和通道, 用於將opencv下的image轉換成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 將Qimage顯示出來
        self.label.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(a.exec_())