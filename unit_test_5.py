import sys

from PyQt5.QtCore import QRectF, Qt, QPoint, QPointF
from PyQt5.QtGui import QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QFrame


class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(1920, 1280)

        scene = QGraphicsScene()

        qPixmap = QPixmap('images/123.jpg')
        h, w = qPixmap.height(), qPixmap.width()

        board = 100
        self.setFixedSize(w + board * 2, h + board * 2)

        scene.addPixmap(qPixmap)
        qPen = QPen(Qt.red)
        qPen.setWidth(5)

        scene.addRect(QRectF(0, 0, w, h), qPen)

        arrow = QPixmap('images/arrow.png').scaledToWidth(50)

        scene.addPixmap(arrow)

        # print(scene.items()[-1].offset())

        scene.items()[-1].setOffset(-25, -25)
        self.setScene(scene)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()