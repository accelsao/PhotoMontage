import sys
from PyQt5.QtCore import Qt, QLineF, QPointF
from PyQt5.QtGui import QPixmap, QTransform, QPolygonF
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtCore import Qt, QPointF, QRectF, QSize, QLine, QLineF
from PyQt5.QtGui import QPainter, QPen, QPixmap, QTransform, QImage
from PyQt5.QtWidgets import QLabel
from copy import deepcopy


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        rect1 = QRectF(QPointF(50, 80), QPointF(150, 200))
        rect4 = QRectF(QPointF(50 + 10, 80 + 10), QPointF(150 + 0, 200 + 0))
        # print(rect1.getCoords())
        ang = 0
        tras = QTransform()
        ct = rect1.center()
        # ct = QPointF(150, 200)
        # print(ct)
        tras.translate(ct.x(), ct.y())
        tras.rotate(-ang)
        tras.translate(-ct.x(), -ct.y())
        rect2 = tras.map(QPolygonF(rect1))

        tras.reset()
        tras.translate(ct.x(), ct.y())
        tras.rotate(-ang)
        tras.translate(-ct.x(), -ct.y())
        rect5 = tras.map(QPolygonF(rect4))


        # rect7
        tras.reset()
        ct2 = rect4.center()
        dx = ct2.x() - ct.x()
        dy = ct2.y() - ct.y()
        print(dx, dy)
        # dx = -dx
        # dy = -dy
        # rect8 = QRectF(QPointF(rect4.topLeft().x() + dx, rect4.topLeft().y() + dy), QPointF(rect4.bottomRight().x() + dx, rect4.bottomRight().y() + dy))

        # tras.translate(ct.x(), ct.y())
        # tras.rotate(+ang)
        # tras.translate(-ct.x(), -ct.y())
        tras.translate(ct2.x(), ct2.y())
        tras.rotate(+ang)
        tras.translate(-ct2.x(), -ct2.y())
        rect7 = tras.map(rect5)
        print(rect7.boundingRect().getCoords())

        # tras.translate(ct2.x(), ct2.y())
        # tras.rotate(-ang)
        # tras.translate(-ct2.x(), -ct2.y())
        # rect7 = tras.map(QPolygonF(rect8))
        #
        #
        # dx = ct2.x() - ct.x()
        # dy = ct2.y() - ct.y()
        # rect4.setTopLeft(QPointF(rect4.topLeft().x() + dx, rect4.topLeft().y() + dy))
        # rect4.setBottomRight(QPointF(rect4.bottomRight().x() + 0, rect4.bottomRight().y() + 0))
        #
        # tras.reset()
        # tras.translate(ct2.x(), ct2.y())
        # tras.rotate(-ang)
        # tras.translate(-ct2.x(), -ct2.y())
        #
        # # tras.translate(ct2.x() - ct.x(), ct2.y() - ct.y())
        # print(rect7.boundingRect().getCoords())
        #
        # # rect7 = tras.map(QPolygonF(rect4))
        # print('pass')
        # print(rect2.boundingRect().getCoords())
        # print(rect2.)

        self.rect1 = rect1
        self.rect2 = rect2
        self.rect4 = rect4
        self.rect5 = rect5
        self.rect7 = rect7
        # self.p = QPointF(100, 80)
        # print(rect2.boundingRect().topLeft())
        # print(rect2.boundingRect().bottomRight())
        # print(QLineF(rect2.boundingRect().topLeft(), QPointF(26, 80)).length())

        # self.rect3 = QRectF(rect2.boundingRect())
        # self.rect6 = QRectF(rect5.boundingRect())


    def paintEvent(self, e):
        pt = QPainter(self)
        # ct = self.rect1.center()
        # pt.translate(ct)
        pt.setPen(QPen(Qt.red))
        pt.drawRect(self.rect1)
        pt.setPen(QPen(Qt.blue))
        pt.drawPolygon(self.rect2)
        # pt.setPen(QPen(Qt.black))
        # pt.drawRect(self.rect3)
        # pt.resetTransform()

        # ct2 = self.rect4.center()
        # pt.translate(QPointF(ct.x() + ct2.x() - ct.x(), ct.y() + ct2.y() - ct.y()))
        # pt.translate(QPointF(ct2.x() - ct.x(), ct2.y() - ct.y()))
        pt.setPen(QPen(Qt.darkMagenta))
        pt.drawRect(self.rect4)
        pt.setPen(QPen(Qt.darkGreen))
        pt.drawPolygon(self.rect5)
        pt.setPen(QPen(Qt.black))
        # pt.drawRect(self.rect7)
        pt.drawPolygon(self.rect7)


    # def resizeEvent(self, event):
    #     self.lb.resize(self.width(), self.lb.height())
    #     self.lb.setPixmap(self.lb.pixmap().scaled(self.lb.size(), Qt.IgnoreAspectRatio))
    #     QWidget.resizeEvent(self, event)
    #
    #
    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # app.exec_()
    # p = QLineF(QPointF(0, 2), QPointF(4, 5))
    # print(p.angle())
    # p.setAngle(307)
    # print(p.angle())
    # print(p)
    # print(p.dx())
    # print(p.dy())
    # print(p.dx(), p.dy())
    # trans = QTransform()
    # trans.translate(0, 2)
    # trans.rotate(-30)
    # trans.translate(-0, -2)
    # q = trans.map(p)
    # print(q)

    # p = []
    # p.append(QPixmap('images/003.png'))
    # p.append(QPixmap('images/001.jpg'))
    # p.append(QPixmap('images/002.png'))
    # p.append(QPixmap('images/123.jpg'))
    q = QImage('images/001.jpg')
    p = []
    p.append(q)
    p.append(QImage('images/002.jpg'))
    # p.append(QPointF(3, 5))
    # p.append(QPointF(3, 9))
    print(p)
    # f = 3
    del p[0]
    print(p)
    # t = 1
    # print(p)
    # item = p[f]
    # del p[f]
    # # p.remove(item)
    # # p.insert(t, item)
    # print(p)
    # self.imgLayer.n。sert(indexTo, item)




