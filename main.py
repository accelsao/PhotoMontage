import sys
import cv2 as cv

from PyQt5.QtCore import QMimeData, QPointF, Qt, QObject, pyqtSlot, QSize, QAbstractListModel, QRectF
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter, QStandardItemModel, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout,
                             QListView, QListWidgetItem)


class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.img = None
        self.img_layers = []
        self.update_pos = False
        self.start_pos = None
        self.current_pos = None
        self.img_pos_x = None
        self.img_pos_y = None
        self.new_img_pos_x = None
        self.new_img_pos_y = None
        self.resize(QSize(1920, 1280))

    def blending(self, img_layers):
        pass

    def setPixmap(self, QPixmap):

        if len(self.img_layers) == 0:
            self.resize(QPixmap.size())

        self.img_layers.append(QPixmap)
        # self.img = self.blending(self.img_layers)
        self.img = QPixmap

        self.img_pos_x = self.img.width() / 2
        self.img_pos_y = self.img.height() / 2
        self.new_img_pos_x = self.img_pos_x
        self.new_img_pos_y = self.img_pos_y
        self.drawRect = False

    def seltecImage(self, index):
        # painter = QPainter(self)
        # paintRect = QPen(Qt.red)
        #
        # paintRect.setWidth(10)
        # painter.setPen(paintRect)
        # print('select {}'.format(index))
        # print(self.img_pos_y - self.img.height() / 2)
        # print(self.img_pos_x - self.img.width() / 2)
        # painter.drawRect(QRectF(self.img_pos_x - self.img.width() / 2, self.img_pos_y - self.img.height() / 2,
        #                         self.img.width(), self.img.height()))
        self.drawRect = True
        self.update()
        print('select {}'.format(index))

    def paintEvent(self, QPaintEvent):
        # self.resize(1920, 1280)
        if self.img is not None:
            self.resize(self.img.size())
        # print(self.size())
        if self.img is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(
                QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
                self.img
            )
            if self.drawRect is True:
                print('paintRect')
                paintRect = QPen(Qt.red)
                paintRect.setWidth(5)
                painter.setPen(paintRect)
                painter.drawRect(QRectF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2,
                                        self.img.width(), self.img.height()))

    def mousePressEvent(self, QMouseEvent):

        self.update_pos = True
        self.start_pos = QMouseEvent.pos()

    def mouseMoveEvent(self, QMouseEvent):

        if self.img is not None:
            self.current_pos = QMouseEvent.pos()
            self.new_img_pos_x = self.img_pos_x + self.current_pos.x() - self.start_pos.x()
            self.new_img_pos_y = self.img_pos_y + self.current_pos.y() - self.start_pos.y()
            if self.update_pos:
                self.update()

    def mouseReleaseEvent(self, QMouseEvent):

        self.update_pos = False
        self.img_pos_y, self.img_pos_x = self.new_img_pos_y, self.new_img_pos_x


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.window_addition_size = 0
        self.image_list_width = 256
        self.image_board_height = 1920
        self.image_board_width = 1280
        self.button_list_height = 200

        # MainWindow Size
        self.resize(QSize(self.image_board_height + self.window_addition_size + self.button_list_height,
                          self.image_board_width + self.image_list_width))

        self.img = None
        self.image_board = ImgLabel()

        # TODO Image resizes before loading in photo

        # Set Buttons
        self.btnSetBackGround = QPushButton('SetBackGround')
        # self.btnSetBackGround.resize(QSize(self.button_list_height, self.image_board_width + self.image_list_width))
        self.btnAddImage = QPushButton('AddImage')


        layout = QVBoxLayout(self)

        images_area = QHBoxLayout()

        # model = QStandardItemModel()
        # model.insertColumn(0)
        # model.insertRows(0, 2)
        # model.setData(model.index(0, 0), QPixmap('images/002.jpg'))
        # model.setData(model.index(1, 0), QPixmap('images/003.jpg'))

        self.image_lists = QListWidget()
        # self.image_list_item = QListWidgetItem()

        # image_list_item = QListWidgetItem()
        # icon = QIcon()
        # icon.addPixmap(QPixmap('images/002.jpg'), QIcon.Normal, QIcon.Off)
        # image_list_item.setIcon(icon)
        # image_lists.addItem(image_list_item)

        # image_lists.setMaximumWidth(image_lists.sizeHintForRow(0) + 2 * image_lists.frameWidth())
        # image_lists.setFixedSize(image_lists.sizeHintForColumn(0) + 2 * image_lists.frameWidth(),
        #                          image_lists.sizeHintForRow(0) * image_lists.count() + 2 * image_lists.frameWidth())
        # image_lists.resize(QSize(self.image_board_height, self.image_list_width))

        images_area.addWidget(self.image_lists)
        images_area.addWidget(self.image_board)
        # print(image_lists.size())
        # print(self.image_board.size())
        # print(images_area.size())

        button_list = QHBoxLayout()
        # button_list.addWidget(self.btnOpen)
        button_list.addWidget(self.btnSetBackGround)
        button_list.addWidget(self.btnAddImage)

        layout.addLayout(images_area)
        layout.addLayout(button_list)

        # add buttons action
        self.btnSetBackGround.clicked.connect(self.setBackGround)
        self.btnAddImage.clicked.connect(self.addImage)


    @pyqtSlot()
    def setBackGround(self):
        # fileName, _ = QFileDialog.getOpenFileName(
        #     self, 'Open Image', './images', '*.png *.jpg *.bmp')
        # if fileName is '':
        #     return
        # src = cv.imread(fileName)
        # # TODO customer _ resize
        # dst = cv.resize(src, dsize=(256, 256), interpolation=cv.INTER_CUBIC)
        # self.img = dst
        # h, w = self.img.shape[:2]
        #
        # height, width, channel = self.img.shape
        # bytesPerLine = 3 * width
        # self.qImg = QImage(self.img.data, width, height, bytesPerLine,
        #                    QImage.Format_RGB888).rgbSwapped()
        # qPixmap = QPixmap.fromImage(self.qImg)
        # assert type(qPixmap) == QPixmap, 'type must be qPixmap'
        # self.image_board.setPixmap(qPixmap)


        self.image_lists.clear()
        self.image_lists.setViewMode(QListView.IconMode)
        self.image_lists.itemClicked.connect(self.selectImage)



        # image_list_item = QListWidgetItem()
        # icon = QIcon()
        # icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        # image_list_item.setIcon(icon)

        self.addImage()

        # self.image_lists.addItem(image_list_item)
        print('pass here')

        print('pass here')

        h, w = self.img.shape[:2]
        print(h, w)

        image_lists_width = self.image_lists.sizeHintForRow(0) + 2 * self.image_lists.frameWidth()
        image_lists_height = h + 2 * self.image_lists.frameWidth()

        self.image_lists.setFixedSize(image_lists_width, image_lists_height)

        self.resize(QSize(h + self.button_list_height, w + self.image_list_width))

    # @pyqtSlot()
    def addImage(self):

        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './images', '*.png *.jpg *.bmp')

        if fileName is '':
            return


        src = cv.imread(fileName)
        # TODO customer _ resize
        dst = cv.resize(src, dsize=(256, 256), interpolation=cv.INTER_CUBIC)
        self.img = dst

        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        qPixmap = QPixmap.fromImage(self.qImg)
        assert type(qPixmap) == QPixmap, 'type must be qPixmap'
        # TODO not set but blend images to one Pixmap
        self.image_board.setPixmap(qPixmap)

        image_list_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        image_list_item.setIcon(icon)
        self.image_lists.addItem(image_list_item)

    # @pyqtSlot()
    def selectImage(self, item):
        # print(item.)
        # print(self.image_lists.indexFromItem(item).row())
        self.image_board.seltecImage(self.image_lists.indexFromItem(item).row())
        # self.hightlightImage(self.image_lists.indexFromItem(item).row())
        # print(123)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
