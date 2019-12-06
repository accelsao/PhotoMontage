import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem


class CustomScene(QGraphicsScene):
    def __init__(self):
        super(CustomScene, self).__init__()
    # def mousePressEvent(self, event):
    #     print('Custom view clicked.')
    #     # super(CustomScene, self).mousePressEvent(event)

class CustomItem(QGraphicsPixmapItem):
    def __init__(self, icon_path='images/righttop-leftbot.png'):
        super(CustomItem, self).__init__()
        arrow_pixmap = QPixmap(icon_path).scaledToWidth(50)
        self.setPixmap(arrow_pixmap)

    def mousePressEvent(self, event):
        print('Custom item clicked.')


class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        item = CustomItem()
        # item.setRect(20, 20, 60, 60)
        scene = CustomScene()

        scene.addItem(item)
        self.setScene(scene)

if __name__ == '__main__':

    a = QApplication(sys.argv)
    view = MainWindow()
    view.show()
    a.exec_()
