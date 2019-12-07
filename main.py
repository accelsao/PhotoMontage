import sys
import cv2 as cv

from PyQt5.QtCore import QMimeData, QPointF, Qt, QObject, pyqtSlot, QSize, QAbstractListModel, QRectF
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter, QStandardItemModel, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout,
                             QListView, QListWidgetItem, QMainWindow, QStackedWidget, QStackedLayout, QMenu, QMenuBar,
                             QAction)

from crop import MainCropWindow


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

    def selectImage(self, index):
        self.drawRect = True
        self.update()
        print('select {}'.format(index))

    def paintEvent(self, QPaintEvent):
        if self.img is not None:
            self.resize(self.img.size())

        if self.img is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(
                QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
                self.img
            )
            if self.drawRect is True:
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


class CropLabel(QLabel):
    def __init__(self):
        super(CropLabel, self).__init__()
        self.img = None
        self.left_top = QPointF(200, 200)
        self.bot_right = QPointF(0, 0)
        self.left_top_icon = QPixmap('images/down-arrow.png').scaled(QSize(25, 25))
        # self.left_top_icon.scaled(QSize(25, 25))

    def setPixmap(self, QPixmap):
        self.img = QPixmap
        h, w = QPixmap.height(), QPixmap.width()
        self.bot_right = QPointF(self.left_top.x() + w, self.left_top.y() + h)
        # self.setPixmap()

    def paintEvent(self, QPaintEvent):
        if self.img is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(self.left_top, self.img)
            painter.drawPixmap(self.left_top.x() - self.left_top_icon.width() / 2,
                               self.left_top.y() - self.left_top_icon.height() / 2,
                               self.left_top_icon)

            paintRect = QPen(Qt.red)
            paintRect.setWidth(3)
            painter.setPen(paintRect)
            painter.drawRect(QRectF(self.left_top, self.bot_right))



class MainQWidget(QWidget):
    def __init__(self, parent=None):
        super(MainQWidget, self).__init__(parent)

        self.layout = QStackedLayout(self)
        self.main_board = QWidget()
        self.crop_main_window = QMainWindow()

        self.main_board_layout = QHBoxLayout()
        self.main_board.setLayout(self.main_board_layout)

        self.image_board = ImgLabel()
        self.image_lists = QListWidget()

        self.main_board_layout.addWidget(self.image_lists)
        self.main_board_layout.addWidget(self.image_board)

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

    def set_crop_mode(self, mode):
        if mode:
            # Set crop Rect
            print('assss')
            self.layout.setCurrentIndex(1)
        else:
            # Crop Img
            self.layout.setCurrentIndex(0)


class MainWindow(QMainWindow):
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


        button_list = QMenuBar()
        button_list.addAction('SetBackGround', self.setBackGround)
        button_list.addAction('AddImage', self.addImage)

        self.setMenuBar(button_list)

        self.mainWindow = MainQWidget(self)
        self.setCentralWidget(self.mainWindow)


    @pyqtSlot()
    def setBackGround(self):
        self.mainWindow.image_lists.clear()
        self.mainWindow.image_lists.setViewMode(QListView.ListMode)
        self.mainWindow.image_lists.setDragDropMode(QAbstractItemView.InternalMove)
        self.mainWindow.image_lists.itemClicked.connect(self.selectImage)

        self.addImage()
        h, w = self.mainWindow.img.shape[:2]
        image_lists_width = self.mainWindow.image_lists.sizeHintForRow(0) + 2 * self.mainWindow.image_lists.frameWidth()
        image_lists_height = h + 2 * self.mainWindow.image_lists.frameWidth()
        self.mainWindow.image_lists.setFixedSize(image_lists_width, image_lists_height)
        self.mainWindow.main_board.resize(QSize(h, w + image_lists_width))
        # self.mainWindow.main_board.resize(QSize(h, w + image_lists_width))

    def addImage(self):
        filename, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './images', '*.png *.jpg *.bmp')

        if filename is '':
            return

        src = cv.imread(filename)
        # dst = cv.resize(src, dsize=(256, 256), interpolation=cv.INTER_CUBIC)
        self.mainWindow.img = src

        height, width, channel = self.mainWindow.img.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.mainWindow.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        qPixmap = QPixmap.fromImage(qImg)
        assert type(qPixmap) == QPixmap, 'type must be qPixmap'
        # TODO not set but blend images to one Pixmap

        self.mainWindow.crop_board.setPixmap(qPixmap)
        self.mainWindow.set_crop_mode(True)

        self.mainWindow.image_board.setPixmap(qPixmap)
        image_list_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        image_list_item.setIcon(icon)
        self.mainWindow.image_lists.addItem(image_list_item)

    def selectImage(self, item):
        self.mainWindow.image_board.selectImage(self.mainWindow.image_lists.indexFromItem(item).row())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
