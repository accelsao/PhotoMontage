import sys
import cv2 as cv

from PyQt5.QtCore import QMimeData, QPointF, Qt, QObject, pyqtSlot, QSize, QAbstractListModel, QRectF
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter, QStandardItemModel, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout,
                             QListView, QListWidgetItem, QMainWindow, QStackedWidget, QStackedLayout, QMenu, QMenuBar,
                             QAction, QSpacerItem, QSizePolicy)

from crop import MainCropWindow
from image import ImgLabel


class MainQWidget(QWidget):
    def __init__(self, parent=None):
        super(MainQWidget, self).__init__(parent)

        self.layout = QStackedLayout(self)
        self.main_board = QWidget()
        self.crop_main_window = QMainWindow()

        self.main_board_layout = QHBoxLayout()
        self.main_board.setLayout(self.main_board_layout)

        # self.main_board.setFixedSize(1920, 1280)

        self.image_board = ImgLabel()
        self.image_lists = QListWidget()

        # self.image_board.setFixedSize(1920, 1080 - 256)
        # self.image_lists.setFixedSize(1920)


        self.main_board_layout.addWidget(self.image_lists, 1)
        self.main_board_layout.addWidget(self.image_board, 2)


        # self.crop_board = CropLabel()
        # self.crop_board.setAlignment(Qt.AlignCenter)
        self.crop_board = MainCropWindow()

        self.crop_main_window.setCentralWidget(self.crop_board)

        image_crop_lists = QMenuBar()
        image_crop_lists.addAction('Free')
        image_crop_lists.addAction('4:3')
        image_crop_lists.addAction('3:4')
        image_crop_lists.addAction('1:1')
        image_crop_lists.addAction('Done', lambda: self.set_crop_mode(False))

        self.crop_main_window.setMenuBar(image_crop_lists)

        self.layout.addWidget(self.main_board)
        self.layout.addWidget(self.crop_main_window)
        self.layout.setCurrentIndex(0)
        self.img = None

        # self.croppedPixmap = None

    def set_crop_mode(self, mode, qPixmap=None):
        print('start cropping: {}'.format(mode))

        if mode:
            # Set crop Rect

            self.crop_board.setPixmap(qPixmap)
            # print(self.crop_board.sizeHint())
            # self.crop_main_window.setFixedSize(self.crop_board.sizeHint())
            # print(self.crop_main_window.size())
            window.setFixedSize(self.crop_main_window.sizeHint())
            # self.setFixedSize(self.crop_main_window.size())
            self.layout.setCurrentIndex(1)
            # print(123)

        else:
            print('setcroppedimg')
            print(self.crop_board.scene.cropped_img == None)
            window.setCroppedImg(self.crop_board.scene.cropped_img)
            # Crop Img
            self.layout.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.image_list_width = 256
        self.image_board_height = 1080
        self.image_board_width = 1920

        # MainWindow Size
        self.resize(QSize(self.image_board_width + self.image_list_width, self.image_board_height))


        button_list = QMenuBar()
        button_list.addAction('SetBackGround', self.setBackGround)
        button_list.addAction('AddImage', self.addImage)

        self.setMenuBar(button_list)

        self.mainWindow = MainQWidget()
        self.setCentralWidget(self.mainWindow)

        self.setBG = False

    @pyqtSlot()
    def setBackGround(self):
        self.mainWindow.image_lists.clear()
        self.mainWindow.image_lists.setViewMode(QListView.ListMode)
        self.mainWindow.image_lists.setDragDropMode(QAbstractItemView.InternalMove)
        self.mainWindow.image_lists.itemClicked.connect(self.selectImage)
        self.mainWindow.image_board.img = None
        self.mainWindow.image_board.img_layers = []
        self.setBG = True

        self.addImage()


    def addImage(self):
        filename, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './images', '*.png *.jpg *.bmp')

        if filename is '':
            return

        src = cv.imread(filename)
        # dst = cv.resize(src, dsize=(348, 720), interpolation=cv.INTER_CUBIC)

        # TODO Bug Here
        self.mainWindow.img = src

        height, width, channel = self.mainWindow.img.shape

        bytesPerLine = 3 * width
        qImg = QImage(self.mainWindow.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        qPixmap = QPixmap.fromImage(qImg)

        # RESIZE
        qPixmap = qPixmap.scaledToHeight(720)

        # TODO not set but blend images to one Pixmap


        self.mainWindow.set_crop_mode(True, qPixmap)

        # TODO main Window size 保持不變 crop window 可變動
        # TODO
        # TODO addimage 不要更動window size 同時保證大小不超過background
        # TODO
        # self.mainWindow.image_board.setPixmap(qPixmap)
        # print(456)
        # image_list_item = QListWidgetItem()
        # icon = QIcon()
        # icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        # image_list_item.setIcon(icon)
        # self.mainWindow.image_lists.addItem(image_list_item)

    def setCroppedImg(self, qPixmap):
        self.mainWindow.image_board.setPixmap(qPixmap)
        image_list_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        image_list_item.setIcon(icon)
        self.mainWindow.image_lists.addItem(image_list_item)

        if self.setBG:
            w, h = self.mainWindow.image_board.img.width(), self.mainWindow.image_board.img.height()
            self.mainWindow.image_board.setFixedSize(w, h)
            self.mainWindow.image_lists.setFixedSize(self.image_list_width, h)
            self.setFixedSize(w + self.mainWindow.image_lists.width(), h)
            self.setBG = False

    def selectImage(self, item):
        self.mainWindow.image_board.selectImage(self.mainWindow.image_lists.indexFromItem(item).row())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
