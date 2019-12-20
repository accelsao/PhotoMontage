import sys

from PyQt5.QtCore import Qt, QLineF, QPointF
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QLabel


class PrettyWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.initUI()

    def initUI(self):
        # self.center()
        self.setWindowTitle('Browser')

        self.lb = QLabel(self)
        pixmap = QPixmap("images/coshunie.png")
        pixmap = pixmap.transformed(QTransform().scale(-1, 2))
        self.resize(pixmap.size())
        # height_of_label = 100
        # self.lb.resize(self.width(), height_of_label)
        self.lb.setPixmap(pixmap)
        # self.lb.setPixmap(pixmp。.scaled(self.lb.size(), Qt.IgnoreAspectRatio))
        self.show()

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

def main():
    app = QApplication(sys.argv)
    w = PrettyWidget()
    app.exec_()

if __name__ == '__main__':
    # main()

    p = QLineF(QPointF(0, 0), QPointF(10, -10))
    print(p)
    print(p.angle())
    p.setAngle(135)
    print(p)
    # print(q.p1(), q.p2())
