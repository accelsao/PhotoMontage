import sys
import cv2 as cv
import numpy as np

from PyQt5.QtCore import QMimeData, QPointF, Qt, QObject, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout)



class DraggableLabel(QLabel):
    def __init__(self,parent,image):
        super(QLabel,self).__init__(parent)
        self.setPixmap(QPixmap(image))
        self.show()
        self.drag_start_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text())
        mimedata.setImageData(self.pixmap().toImage())

        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class my_label(QLabel):
    def __init__(self,title,parent):
        super().__init__(title,parent)
        self.setAcceptDrops(True)
        print('Construct Label')

    def dragEnterEvent(self,event):
        print('DragEvent')
        if event.mimeData().hasImage():
            print("event accepted")
            event.accept()
        else:
            print("event rejected")
            event.ignore()

    def dropEvent(self,event):
        if event.mimeData().hasImage():
            self.setPixmap(QPixmap.fromImage(QImage(event.mimeData().imageData())))

class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.img = None
        self.update_pos = False
        self.start_pos = None
        self.current_pos = None
        self.img_pos_x = None
        self.img_pos_y = None
        self.new_img_pos_x = None
        self.new_img_pos_y = None

    def setPixmap(self, QPixmap):
        print('setPixmap')
        self.img = QPixmap
        self.img_pos_x = self.img.width() / 2
        self.img_pos_y = self.img.height() / 2
        self.new_img_pos_x = self.img_pos_x
        self.new_img_pos_y = self.img_pos_y
        self.resize(self.img.size())

    def paintEvent(self, QPaintEvent):
        print('Come in')

        if self.img is not None:
            print('Comeback')
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(
            #     # self.width() - self.img.width(),
            #     # self.height() - self.img.height(),
            #     # self.width() / 2 - self.img.width() / 2,
            #     # self.height() / 2 - self.img.height() / 2,
                QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
                # self.width() / 2,
                # self.height() / 2,
            #     # self.pos.x() - self.img.width() / 2,
            #     # self.pos.y() - self.img.height() / 2,
            #     # self.img.width() / 2,
            #     # self.img.height() / 2,
                self.img
            )

    def mousePressEvent(self, QMouseEvent):

        print('Mouse Press')
        self.update_pos = True
        self.start_pos = QMouseEvent.pos()

    def mouseMoveEvent(self, QMouseEvent):
        print('Mouse Move')
        if self.img is not None:
            self.current_pos = QMouseEvent.pos()
            self.new_img_pos_x = self.img_pos_x + self.current_pos.x() - self.start_pos.x()
            self.new_img_pos_y = self.img_pos_y + self.current_pos.y() - self.start_pos.y()
            if self.update_pos:
                self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        print('Mouse Release')
        self.update_pos = False
        self.img_pos_y, self.img_pos_x = self.new_img_pos_y, self.new_img_pos_x


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # MainWindow Size
        self.resize(QSize(1200, 800))

        self.img = None
        # self.img = QPixmap('images/123.jpg')
        self.image_board = ImgLabel()
        # self.image_board.setPixmap(self.img)

        # TODO Image resizes before loading in photo
        # TODO adjust Qloabel size with Window Size
        # Set Buttons
        self.btnOpen = QPushButton('Open', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_board)

        button_list = QHBoxLayout()
        button_list.addWidget(self.btnOpen)
        layout.addLayout(button_list)


        # add buttons action
        self.btnOpen.clicked.connect(self.openSlot)

    @pyqtSlot()
    def openSlot(self):
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './images', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        src = cv.imread(fileName)
        print('Successfully Open image, fileName: {}'.format(fileName))
        dst = cv.resize(src, dsize=(256, 256), interpolation=cv.INTER_CUBIC)
        self.img = dst
        self.refreshShow()


    def refreshShow(self):
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        qPixmap = QPixmap.fromImage(self.qImg)
        assert type(qPixmap) == QPixmap, 'type must be qPixmap'
        self.image_board.setPixmap(QPixmap('images/123.jpg'))
        # self.image_board.setPixmap(qPixmap)


    # def mousePressEvent(self, QMouseEvent):
    #     self.update_pos = True
    #     self.start_pos = QMouseEvent.pos()
    #
    # def mouseMoveEvent(self, QMouseEvent):
    #     self.cur_pos = QMouseEvent.pos()
    #     # print(self.cur_pos.x() - self.start_pos.x())
    #     self.cur_img_x = self.img_x + self.cur_pos.x() - self.start_pos.x()
    #     self.cur_img_y = self.img_y + self.cur_pos.y() - self.start_pos.y()
    #     if self.update_pos:
    #         self.update()
    #
    # def mouseReleaseEvent(self, QMouseEvent):
    #     self.update_pos = False
    #     self.img_y, self.img_x = self.cur_img_y, self.cur_img_x




        # listwidget = QListWidget(self)
        # listwidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # listwidget.setDragEnabled(True)
        # listwidget.viewport().setAcceptDrops(True)
        # listwidget.setDropIndicatorShown(True)
        # listwidget.setDragDropMode(QAbstractItemView.InternalMove)

    # def initUI(self):
    #     self.label = QLabel()
    #     self.btnQuit = QPushButton('Quit', self)
    #     self.btnProcess = QPushButton('Process', self)
    #     self.btnSave = QPushButton('Save', self)
    #     self.btnOpen = QPushButton('Open', self)
    #     self.setGeometry(500, 300, 300, 300)
    #
    #     # 佈局設定
    #     layout = QGridLayout(self)
    #     layout.addWidget(self.label, 0, 0, 1, 0)
    #     layout.addWidget(self.btnOpen, 1, 0)
    #     layout.addWidget(self.btnSave, 1, 1)
    #     layout.addWidget(self.btnProcess, 1, 2)
    #     layout.addWidget(self.btnQuit, 1, 3)
    #
    #     # 信號與槽連接, PyQt5與Qt5相同, 信號可綁定普通成員函數
    #     self.btnOpen.clicked.connect(self.openSlot)
    #     self.btnSave.clicked.connect(self.saveSlot)
    #     self.btnProcess.clicked.connect(self.processSlot)
    #     self.btnQuit.clicked.connect(self.close)
    #
    # def openSlot(self):
    #     # 調用打開文件diglog
    #     fileName, tmp = QFileDialog.getOpenFileName(
    #         self, 'Open Image', './images', '*.png *.jpg *.bmp')
    #
    #     if fileName is '':
    #         return
    #
    #     self.img = cv.imread(fileName)
    #     self.refreshShow()
    #
    # def saveSlot(self):
    #     # 調用存儲文件dialog
    #     fileName, tmp = QFileDialog.getSaveFileName(
    #         self, 'Save Image', './images', '*.png *.jpg *.bmp', '*.png')
    #
    #     if fileName is '':
    #         return
    #     if self.img.size == 1:
    #         return
    #
    #     # 調用opencv寫入圖像
    #     cv.imwrite(fileName, self.img)
    #
    # def processSlot(self):
    #     if self.img.size == 1:
    #         return
    #
    #     # 對圖像做模糊處理, 窗口設定爲5x5
    #     self.img = cv.blur(self.img, (5, 5))
    #
    #     self.refreshShow()
    #
    # def refreshShow(self):
    #     # 提取圖像的尺寸和通道, 用於將opencv下的image轉換成Qimage
    #     height, width, channel = self.img.shape
    #     bytesPerLine = 3 * width
    #     self.qImg = QImage(self.img.data, width, height, bytesPerLine,
    #                        QImage.Format_RGB888).rgbSwapped()
    #
    #     # 將Qimage顯示出來
    #     self.label.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
