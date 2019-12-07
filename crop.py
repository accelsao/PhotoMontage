import sys

from PyQt5.QtCore import QRectF, Qt, QPoint, QPointF, QRect
from PyQt5.QtGui import QPen, QBrush, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsRectItem

class ArrowIcon(QGraphicsPixmapItem):

    def __init__(self, icon_path='images/righttop-leftbot.png'):
        super(ArrowIcon, self).__init__()
        arrow_pixmap = QPixmap(icon_path).scaledToWidth(50)
        self.setPixmap(arrow_pixmap)
        self.startPos = self.pos()
        self.updatePos = False

    def mousePressEvent(self, e):
        self.updatePos = True
        # self.startPos = e.pos()

    def mouseMoveEvent(self, e):
        # if self.updatePos
        pass
        # self.currentPos = e.pos()
        # self.newImagePos = QPointF(self.currentPos.x() + self.imgPosX)

    def mouseReleaseEvent(self, e):
        self.updatePos = False


class MyScene(QGraphicsScene):
    def __init__(self):
        super(MyScene, self).__init__()
        self.img = None
        self.updateMode = 0
        self.startPos = QPointF()
        self.minSizeofRect = 64

        # TODO Assert image is not none while updating scene

    def mousePressEvent(self, e):
        if self.arrow_icon_top_left.x() <= e.scenePos().x() <= self.arrow_icon_top_left.x() + self.arrow_icon_top_left.pixmap().width() and \
                self.arrow_icon_top_left.y() <= e.scenePos().y() <= self.arrow_icon_top_left.y() + self.arrow_icon_top_left.pixmap().height():
            self.updateMode = 1
            self.startPos = e.scenePos()
        elif self.arrow_icon_bottom_right.x() <= e.scenePos().x() <= self.arrow_icon_bottom_right.x() + self.arrow_icon_bottom_right.pixmap().width() and \
                self.arrow_icon_bottom_right.y() <= e.scenePos().y() <= self.arrow_icon_bottom_right.y() + self.arrow_icon_bottom_right.pixmap().height():
            self.updateMode = 2
            self.startPos = e.scenePos()
        else:

            self.updateMode = 0

    def mouseMoveEvent(self, e):
        if self.updateMode == 1:
            self.currentPos = e.scenePos()
            self.rectTopLeft.setX(min(max(self.prevRectTopLeft.x() + self.currentPos.x() - self.startPos.x(), 0.0),
                                         self.prevRectBottomRight.x() - self.minSizeofRect))

            self.rectTopLeft.setY(min(max(self.prevRectTopLeft.y() + self.currentPos.y() - self.startPos.y(), 0.0),
                                         self.prevRectBottomRight.y() - self.minSizeofRect))
            self.update()
        elif self.updateMode == 2:
            self.currentPos = e.scenePos()
            self.rectBottomRight.setX(max(min(self.prevRectBottomRight.x() + self.currentPos.x() - self.startPos.x(), self.imgW),
                                      self.prevRectTopLeft.x() + self.minSizeofRect))

            self.rectBottomRight.setY(max(min(self.prevRectBottomRight.y() + self.currentPos.y() - self.startPos.y(), self.imgH),
                                      self.prevRectTopLeft.y() + self.minSizeofRect))
            self.update()


    def mouseReleaseEvent(self, e):

        self.updateMode = False
        self.prevRectTopLeft = QPointF(self.rectTopLeft)
        self.prevRectBottomRight = QPointF(self.rectBottomRight)


    def update(self):

        self.rectCropArea.setRect(QRectF(self.rectTopLeft, self.rectBottomRight))
        self.arrow_icon_top_left.setPos(self.rectTopLeft.x() - 25, self.rectTopLeft.y() - 25)
        self.arrow_icon_bottom_right.setPos(self.rectBottomRight.x() - 25, self.rectBottomRight.y() - 25)

    def setPixmap(self, qPixmap):
        self.imgW, self.imgH = qPixmap.width(), qPixmap.height()
        self.img = QGraphicsPixmapItem(qPixmap)
        self.arrow_icon_top_left = ArrowIcon()
        self.arrow_icon_bottom_right = ArrowIcon()
        self.rectPen = QPen(Qt.red)
        self.rectPen.setWidth(5)
        self.rectTopLeft = QPointF(0, 0)
        self.rectBottomRight = QPointF(self.imgW, self.imgH)
        self.rectCropArea = QGraphicsRectItem(QRectF(self.rectTopLeft, self.rectBottomRight))
        self.prevRectTopLeft = QPointF(self.rectTopLeft)
        self.prevRectBottomRight = QPointF(self.rectBottomRight)
        self.rectCropArea.setPen(self.rectPen)
        self.arrow_icon_top_left.setPos(-25, -25)
        self.arrow_icon_bottom_right.setPos(self.imgW - 25, self.imgH - 25)
        self.addItem(self.img)
        self.addItem(self.rectCropArea)
        self.addItem(self.arrow_icon_top_left)
        self.addItem(self.arrow_icon_bottom_right)


class MainCropWindow(QGraphicsView):
    def __init__(self):
        super(MainCropWindow, self).__init__()
        self.scene = MyScene()
        self.setScene(self.scene)

    def setPixmap(self, qPixmap):
        # TODO Reszie Image another way
        self.scene.setPixmap(qPixmap.scaledToHeight(720))

        self.resize(qPixmap.width() + 200, qPixmap.height() + 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainCropWindow()
    window.setPixmap(QPixmap('images/cat.jpg'))
    window.show()
    app.exec_()
