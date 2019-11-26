import sys
from PyQt5.QtCore import QPointF, QSize, QRectF, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen
from PyQt5.QtWidgets import *

class CropLabel(QLabel):
    def __init__(self, parent=None):
        super(CropLabel, self).__init__(parent)
        self.img = None
        self.left_top = QPointF(0, 0)
        self.bot_right = QPointF(0, 0)
        self.left_top_icon = QPixmap('images/lefttop-botright.png').scaled(QSize(25, 25))

    def setPixmap(self, QPixmap):
        self.img = QPixmap
        h, w = QPixmap.height(), QPixmap.width()
        self.bot_right = QPointF(self.left_top.x() + w, self.left_top.y() + h)
        self.resize(QSize(w+100, h+100))


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

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.label = CropLabel(self)
        self.board_width = 100
        qPixmap = QPixmap('images/cat.jpg').scaled(QSize(256, 256))
        self.resize(QSize(qPixmap.width() + self.board_width * 2, qPixmap.height() + self.board_width * 2))
        self.label.left_top = QPointF   (self.board_width, self.board_width)
        self.label.setPixmap(qPixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()