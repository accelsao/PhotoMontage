import sys

from PyQt5.QtCore import QRectF, Qt, QPoint, QPointF, QRect
from PyQt5.QtGui import QPen, QBrush, QPixmap, QPainter, QImage, QPainterPath, QColor, QBitmap
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsRectItem


class CutImg(QGraphicsItem):
    def __init__(self, qPixmap):
        super(CutImg, self).__init__()
        # self.qPixmap = qPixmap
        self.img = qPixmap.toImage()
        self.imgdraw = QImage(self.img.size(), QImage.Format_ARGB32)
        self.imgdraw.fill(Qt.transparent)
        print(self.img)
        print(self.imgdraw)

    def boundingRect(self):
        return QRectF(self.img.rect())

    def paint(self, qPainter, qStyleOptionGraphicsItem, widget=None):
        # qPainter.drawPixmap(QPointF(), self.qPixmap)
        # qPainter.setCompositionMode(QPainter.CompositionMode_Clear)
        # qPainter.fillRect(QRectF(QPointF(30, 50), QPointF(100, 150)), QBrush(Qt.red))
        # print(123)
        qPainter.drawImage(QPointF(), self.img)
        qPainter.setCompositionMode(QPainter.CompositionMode_Clear)
        qPainter.eraseRect(QRectF(50, 50, 80, 80))
        # qPainter.restore()


class CutScene(QGraphicsScene):
    def __init__(self):
        super(CutScene, self).__init__()
        self.cuttedImg = None

    def setPixmap(self, qPixmap):
        self.mainImg = CutImg(qPixmap)
        print(self.mainImg)
        self.addItem(self.mainImg)
        self.cuttedImg = qPixmap


class MainCutWindow(QGraphicsView):
    def __init__(self):
        super(MainCutWindow, self).__init__()
        self.scene = CutScene()
        self.setScene(self.scene)
        self.boardmargin = 100

    def setPixmap(self, qPixmap):
        self.scene = CutScene()
        self.setScene(self.scene)
        self.setFixedSize(qPixmap.width() + self.boardmargin * 2, qPixmap.height() + self.boardmargin * 2)
        self.scene.setPixmap(qPixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainCutWindow()
    window.setPixmap(QPixmap('images/cat.jpg'))
    window.show()
    app.exec_()