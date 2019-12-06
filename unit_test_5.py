import sys

from PyQt5.QtCore import QRectF, Qt, QPoint, QPointF, QRect
from PyQt5.QtGui import QPen, QBrush, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QFrame, QGraphicsPixmapItem, \
    QGraphicsItem, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent


class CropImage(QGraphicsPixmapItem):
    def __init__(self):
        # super(MyPainter, self).__init__()
        super(CropImage, self).__init__()
        self.img = QPixmap('images/cat.jpg').scaledToHeight(720)
        h, w = self.img.height(), self.img.width()
        self.board = 100
        bg_img = QImage(w + self.board * 2, h + self.board * 2, QImage.Format_RGB32)
        bg_img.fill(Qt.white)
        self.background = QPixmap.fromImage(bg_img)

        self.new_img_pos_x, self.new_img_pos_y = self.img.width(), self.img.height()

        self.mainImg = QPixmap()

        painter = QPainter(self.mainImg)
        styleoptiongrahpicsitem = QStyleOptionGraphicsItem()
        self.paint(painter, styleoptiongrahpicsitem)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # print(self.new_img_pos_x)
        # print(self.img.width())
        painter.drawPixmap(
            # QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
            # QRectF(0, 0, self.img.width(), self.img.height()),
            # QPointF(-self.img.width() / 2, -self.img.height() / 2),
            QPointF(0, 0),
            self.background
        )
        print(self.mainImg.size())
        painter.drawPixmap(
            # QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
            # QRectF(0, 0, self.img.width(), self.img.height()),
            # QPointF(-self.img.width() / 2, -self.img.height() / 2),
            QPointF(self.board, self.board),
            self.img
        )
        print(self.mainImg.size())
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

class ArrowIcon(QGraphicsPixmapItem):

    def __init__(self, icon_path='images/righttop-leftbot.png'):
        super(ArrowIcon, self).__init__()
        arrow_pixmap = QPixmap(icon_path).scaledToWidth(50)
        self.setPixmap(arrow_pixmap)
        # self.arrow = arrow
        # self.setSelected(True)
        # self.setAcceptHoverEvents(True)

    def mousePressEvent(self, e):
        print('selected')



class MyScene(QGraphicsScene):
    def __init__(self, img_pixmap):
        """

        :param img: (QGraphicsPixmapItem) main image
        """
        super(MyScene, self).__init__()

        h, w = img_pixmap.height(), img_pixmap.width()
        img = QGraphicsPixmapItem(img_pixmap)

        board = 100

        # # arrow
        # arrow_pixmap = QPixmap('images/righttop-leftbot.png').scaledToWidth(50)
        # arrow = QGraphicsPixmapItem(arrow_pixmap)
        # arrow.setPos(-25, -25)
        arrow_icon = ArrowIcon()
        # arrow.mousePressEvent.connect(self.arrow_mouse_pressed)

        # rectangle
        qPen = QPen(Qt.red)
        qPen.setWidth(5)

        self.addItem(img)
        self.addRect(QRectF(10, 10, w, h), qPen)
        self.addItem(arrow_icon)

    def mousePressEvent(self, e):
        super(MyScene, self).mousePressEvent(e)




class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        # main image
        img_pixmap = QPixmap('images/cat.jpg').scaledToHeight(720)
        h, w = img_pixmap.height(), img_pixmap.width()
        img = QGraphicsPixmapItem(img_pixmap)
        scene = MyScene(img_pixmap)
        self.setScene(scene)
        self.resize(w + 200, h + 200)
        
    def mousePressEvent(self, e):
        super(MainWindow, self).mousePressEvent(e)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()