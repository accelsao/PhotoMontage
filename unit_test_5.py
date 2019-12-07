import sys

from PyQt5.QtCore import QRectF, Qt, QPoint, QPointF, QRect
from PyQt5.QtGui import QPen, QBrush, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsRectItem


class CropImage(QGraphicsPixmapItem):
    def __init__(self):
        # super(MyPainter, self).__init__()
        super(CropImage, self).__init__()
        self.img = QPixmap('images/cat.jpg').scaledToHeight(720)
        h, w = self.img.height(), self.img.width()
        self.board = 100
        # bg_img = QImage(w + self.board * 2, h + self.board * 2, QImage.Format_RGB32)
        # bg_img.fill(Qt.white)
        # self.background = QPixmap.fromImage(bg_img)

        # self.new_img_pos_x, self.new_img_pos_y = self.img.width(), self.img.height()

        self.currentTopLeft = QPointF(self.board, self.board)

        self.mainImg = QPixmap()

        painter = QPainter(self.mainImg)
        styleoptiongrahpicsitem = QStyleOptionGraphicsItem()
        self.paint(painter, styleoptiongrahpicsitem)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        print('RePaint')
        painter.drawPixmap(
            # QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
            # QRectF(0, 0, self.img.width(), self.img.height()),
            # QPointF(-self.img.width() / 2, -self.img.height() / 2),
            QPointF(self.board, self.board),
            self.img
        )
        # print(self.mainImg.size())
        # painter.drawPixmap(
        #     QRect(0, 0, self.img.width() + self.board * 2, self.img.height() + self.board * 2), QPixmap()
        # )
        # painter.drawPixmap(
        #     # QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
        #     # QRectF(0, 0, self.img.width(), self.img.height()),
        #     # QPointF(-self.img.width() / 2, -self.img.height() / 2),
        #     QPointF(self.board, self.board),
        #     self.img2
        # )
        # self.setPixmap(self.mainImg)
        self.setPixmap(self.img)
        # print(123)

    def mouseMoveEvent(self, e):
        print(123)


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
    def __init__(self, imgPixmap):
        """

        :param img: (QGraphicsPixmapItem) main image
        """
        super(MyScene, self).__init__()

        self.imgW, self.imgH = imgPixmap.width(), imgPixmap.height()
        self.img = QGraphicsPixmapItem(imgPixmap)

        # board = 100

        # # arrow
        # arrow_pixmap = QPixmap('images/righttop-leftbot.png').scaledToWidth(50)
        # arrow = QGraphicsPixmapItem(arrow_pixmap)
        # arrow.setPos(-25, -25)
        self.arrow_icon_top_left = ArrowIcon()
        self.arrow_icon_bottom_right = ArrowIcon()



        # arrow.mousePressEvent.connect(self.arrow_mouse_pressed)

        # rectangle
        self.rectPen = QPen(Qt.red)
        self.rectPen.setWidth(5)

        self.addItem(self.img)
        # self.rectCropArea = QGraphicsRectItem(QRectF(0, 0, self.imgW, self.imgH))
        self.rectTopLeft = QPointF(0, 0)
        self.rectBottomRight = QPointF(self.imgW, self.imgH)
        self.rectCropArea = QGraphicsRectItem(QRectF(self.rectTopLeft, self.rectBottomRight))
        self.rectCropArea.setPen(self.rectPen)
        self.addItem(self.rectCropArea)

        self.arrow_icon_top_left.setPos(-25, -25)
        self.arrow_icon_bottom_right.setPos(self.imgW - 25, self.imgH - 25)

        self.addItem(self.arrow_icon_top_left)
        self.addItem(self.arrow_icon_bottom_right)

        self.updateMode = 0



        # mouseEvent
        # self.rectPos = QPointF()
        # self.newRectPos = self.rectPos
        self.startPos = QPointF()

        # self.prevRectTopLeft = self.rectTopLeft
        self.prevRectTopLeft = QPointF(self.rectTopLeft)
        self.prevRectBottomRight = QPointF(self.rectBottomRight)

        self.minSizeofRect = 64

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
        # print('Pass')
        # self.arrow_icon.setPos(self.newRectTopLeft.x() - 25, self.newRectTopLeft.y() - 25)
        self.arrow_icon_top_left.setPos(self.rectTopLeft.x() - 25, self.rectTopLeft.y() - 25)
        self.arrow_icon_bottom_right.setPos(self.rectBottomRight.x() - 25, self.rectBottomRight.y() - 25)


class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        # main image
        img_pixmap = QPixmap('images/cat.jpg').scaledToHeight(720)
        h, w = img_pixmap.height(), img_pixmap.width()
        # img = QGraphicsPixmapItem(img_pixmap)
        scene = MyScene(img_pixmap)
        self.setScene(scene)
        self.resize(w + 200, h + 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
