import sys
import cv2 as cv

from PyQt5.QtCore import QMimeData, QPointF, Qt, QObject, pyqtSlot, QSize, QAbstractListModel, QRectF
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter, QStandardItemModel, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout,
                             QListView, QListWidgetItem, QMainWindow, QStackedWidget, QStackedLayout, QMenu, QMenuBar,
                             QAction, QSpacerItem, QSizePolicy, QSlider)

if __name__ == '__main__':

    q = QPixmap().load('images/cat.jpg')
    p = [q]
    # fromImage(QImage('images/cat.jpg'))
    print(p)

    # q.fill(Qt.red)
    # p = [q, q, q]
    # p.append(q)
    # print(p)
    # p = p[:-1]
    # print(p)
    # p = [QPixmap(QSize(3, 5)), QPixmap(QSize(3, 7))]
    # print(len(p))
    # print(p)
    # print(p[: -2])