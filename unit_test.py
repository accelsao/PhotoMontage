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
        print(rect1.getCoords())
        ang = 30
        tras = QTransform()
        ct = rect1.center()

        tras.translate(ct.x(), ct.y())
        tras.rotate(-ang)
        tras.translate(-ct.x(), -ct.y())
        rect2 = tras.map(QPolygonF(rect1))

        print(rect2.boundingRect().getCoords())
        # rect2 = rect2.boundingRect()
        # print(rect2)


        self.rect1 = rect1
        self.rect2 = rect2
        self.setGeometry(300, 300, 280, 170)

        self.p = QPointF(100, 80)
        print(rect2.boundingRect().topLeft())
        print(rect2.boundingRect().bottomRight())
        print(QLineF(rect2.boundingRect().topLeft(), QPointF(26, 80)).length())

        self.rect3 = QRectF(rect2.boundingRect())

    def paintEvent(self, e):
        pt = QPainter(self)
        pt.setPen(QPen(Qt.red))
        pt.drawRect(self.rect1)
        pt.setPen(QPen(Qt.blue))
        pt.drawPolygon(self.rect2)
        pt.setPen(QPen(Qt.black))
        pt.drawRect(self.rect3)


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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

