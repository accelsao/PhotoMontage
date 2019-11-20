import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QMargins
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QApplication, QListWidgetItem, QListView


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # str = QListWidgetItem()

        # w = str.setSizeHint()
        # print(w)
        list = QListWidget()
        list.setViewMode(QListView.IconMode)
        img_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(QPixmap('images/002.jpg'), QIcon.Normal, QIcon.Off)
        img_item.setIcon(icon)
        list.addItem(img_item)


        vbox = QVBoxLayout(self)
        vbox.addWidget(list)
        # list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # list.setContentsMargins(QMargins(2, 0, 2, 0))

        # list.setFixedSize(list.sizeHintForColumn(0) + 2 * list.frameWidth(),
        #                   list.sizeHintForRow(0) * list.count())


        # print(list.sizeHintForRow(0), list.count(), list.frameWidth())
        # print(list.sizeHintForRow(0) * list.count())
        # list.setMaximumWidth()
        # list.setMinimumWidth(list.sizeHintForColumn(0))


app = QApplication(sys.argv)
myapp = MainWindow()
myapp.show()
sys.exit(app.exec_())
