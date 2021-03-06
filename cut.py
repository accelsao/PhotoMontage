import sys

from PyQt5.QtCore import QRectF, Qt, QPoint, QPointF, QRect, QSize
from PyQt5.QtGui import QPen, QBrush, QPixmap, QPainter, QImage, QPainterPath, QColor, QBitmap, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsRectItem


# class CutImg(QGraphicsItem):
#     def __init__(self, qPixmap):
#         super(CutImg, self).__init__()
#         self.qPixmap = qPixmap
#
#     def boundingRect(self):
#         return QRectF(self.qPixmap.rect())
#
#     def paint(self, qPainter, qStyleOptionGraphicsItem, widget=None):
#         # qPainter.fillRect(self.qPixmap.size(), Qt.transparent)
#
#         qPainter.drawPixmap(QPointF(), self.qPixmap)
#         qPainter.setCompositionMode(QPainter.CompositionMode_Clear)
#         qPainter.fillRect(QRectF(QPointF(50, 80), QPointF(100, 150)), QBrush(Qt.red))

class CutImg(QPixmap):
    def __init__(self, qPixmap):
        super(CutImg, self).__init__()
        self.img = qPixmap

class CutScene(QGraphicsScene):
    def __init__(self):
        super(CutScene, self).__init__()
        self.cuttedImg = None
        self.eraserRadius = 5
        self.originImg = None
        self.mainImg = None
        self.count = 0
        # self.eraseArea = QPainterPath()
        # self.eraseArea = None
        self.eraseArea = []
        self.eraseAreaCurrentIndex = -1


    def update(self):
        img = QPixmap(self.originImg.size())
        img.fill(Qt.transparent)
        pt = QPainter(img)
        pt.drawPixmap(QPointF(), self.originImg)
        pt.setCompositionMode(QPainter.CompositionMode_Xor)
        # pt.fillPath(self.eraseArea, Qt.transparent)
        # pt.fillRect(QRectF(QPointF(30, 150), QPointF(150, 500)), Qt.transparent)
        # pt.fillRect(QRectF(QPointF(30, 300), QPointF(350, 350)), Qt.red)
        # pt.drawPixmap(QPointF(), self.eraseArea)
        pt.drawPixmap(QPointF(), self.eraseArea[self.eraseAreaCurrentIndex])
        # pt.eraseRect(QRectF(QPointF(30, 150), QPointF(150, 500)), Qt.transparent)
        # print(self.count)
        # self.count += 1
        self.mainImg = QGraphicsPixmapItem(img)
        self.clear()
        self.addItem(self.mainImg)
        self.cuttedImg = img

    def setPixmap(self, qPixmap):
        self.originImg = qPixmap
        self.mainImg = QGraphicsPixmapItem(qPixmap)
        self.addItem(self.mainImg)
        self.cuttedImg = qPixmap

        # eraseArea = QPixmap(qPixmap.size())
        # eraseArea.fill(Qt.transparent)
        # pt = QPainter(eraseArea)
        # pt.drawLine(Q)
        # pt.fillRect(QRectF(QPointF(30, 150), QPointF(150, 500)), Qt.white)
        # pt.fillRect(QRectF(QPointF(30, 300), QPointF(350, 350)), Qt.red)
        # pt.setCompositionMode(QPainter.CompositionMode_Clear)
        # pt.fillRect(QRectF(QPointF(30, 150), QPointF(150, 500)), Qt.white)

        # self.eraseArea = eraseArea


class MainCutWindow(QGraphicsView):
    def __init__(self):
        super(MainCutWindow, self).__init__()
        self.scene = CutScene()
        self.setScene(self.scene)
        self.setMouseTracking(True)
        self.board_margin = 100
        self.qPainterPath = QPainterPath()
        self.qPainterPath.setFillRule(1)
        # erase: 0, repair: 1, clean: 2
        self.mode = 0
        self.updateMode = False

        self.eraserRadius = 10

        # cursorImg = QPixmap(QSize(self.eraserRadius, self.eraserRadius))
        # cursorImg.fill(Qt.transparent)
        # painter = QPainter(cursorImg)
        # painter.setPen(QPen(Qt.black, 2))
        # painter.drawRect(cursorImg.rect())
        # painter.end()
        # cursor = QCursor(cursorImg)
        # self.setCursor(cursor)
        # self.cursor = cursor
        # app.setOverrideCursor(cursor)
        # self.update()

    def initialize(self, img, imgEraseArea):
        # print('IN here')
        self.mode = 0
        self.scene = CutScene()
        self.setScene(self.scene)
        self.setFixedSize(img.width() + self.board_margin * 2, img.height() + self.board_margin * 2)
        self.scene.setPixmap(img)
        self.scene.eraseArea.clear()
        self.scene.eraseArea.append(imgEraseArea)
        self.scene.eraseAreaCurrentIndex = 0
        self.update()
        self.scene.update()

    def update(self):
        cursorImg = QPixmap(QSize(self.eraserRadius, self.eraserRadius))
        cursorImg.fill(Qt.transparent)
        painter = QPainter(cursorImg)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(cursorImg.rect())
        painter.end()
        cursor = QCursor(cursorImg)
        self.setCursor(cursor)

    def mousePressEvent(self, e):
        self.updateMode = True
        print(self.scene.eraseAreaCurrentIndex)
        print('self.scene.eraseArea: {}'.format(self.scene.eraseArea))
        # print(self.scene.eraseArea[:self.scene.eraseAreaCurrentIndex])
        self.scene.eraseArea = self.scene.eraseArea[:self.scene.eraseAreaCurrentIndex + 1]
        self.scene.eraseArea.append(self.scene.eraseArea[-1].copy())
        # self.scene.eraseArea.append(self.scene.eraseArea[-1])
        print('self.scene.eraseArea: {}'.format(self.scene.eraseArea))
        self.scene.eraseAreaCurrentIndex += 1

    def mouseMoveEvent(self, e):
        if self.updateMode:
            if self.mode == 0:
                print('self.scene.eraseAreaCurrentIndex: {}'.format(self.scene.eraseAreaCurrentIndex))
                print('self.scene.eraseArea: {}'.format(self.scene.eraseArea))
                pt = QPainter(self.scene.eraseArea[self.scene.eraseAreaCurrentIndex])
                pt.fillRect(QRectF(e.pos().x() - self.eraserRadius / 2 - self.board_margin,
                                   e.pos().y() - self.eraserRadius / 2 - self.board_margin,
                                   self.eraserRadius, self.eraserRadius), Qt.white)

                self.scene.update()
            elif self.mode == 1:
                pt = QPainter(self.scene.eraseArea[self.scene.eraseAreaCurrentIndex])
                pt.setCompositionMode(QPainter.CompositionMode_Clear)
                pt.fillRect(QRectF(e.pos().x() - self.eraserRadius / 2 - self.board_margin,
                                   e.pos().y() - self.eraserRadius / 2 - self.board_margin,
                                   self.eraserRadius, self.eraserRadius), Qt.white)

                self.scene.update()

    def clean(self):
        self.scene.eraseArea.clear()
        self.scene.eraseArea.append(QPixmap(self.scene.originImg.size()))
        self.scene.eraseAreaCurrentIndex = 0
        # self.scene.eraseArea[self.scene.eraseAreaCurrentIndex] = QPixmap(self.scene.originImg.size())
        # self.scene.eraseArea = QPixmap(self.scene.originImg.size())
        self.scene.update()

    def mouseReleaseEvent(self, e):
        self.updateMode = False
        print('finish')

    # def setPixmap(self, img, imgEraseArea):
    #     self.setFixedSize(img.width() + self.board_margin * 2, img.height() + self.board_margin * 2)
    #     self.scene.setPixmap(img)
    #     self.scene.eraseArea = imgEraseArea

    def eraseUndo(self):
        print('undo')
        self.scene.eraseAreaCurrentIndex = max(0, self.scene.eraseAreaCurrentIndex - 1)
        print(self.scene.eraseAreaCurrentIndex)
        self.scene.update()
    def eraseRedo(self):
        print('redo')
        self.scene.eraseAreaCurrentIndex = min(len(self.scene.eraseArea) - 1, self.scene.eraseAreaCurrentIndex + 1)
        print(self.scene.eraseAreaCurrentIndex)
        self.scene.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainCutWindow()
    window.setPixmap(QPixmap('images/cat.jpg'))
    window.show()
    app.exec_()