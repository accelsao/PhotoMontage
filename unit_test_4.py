import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QHBoxLayout(self)
        self.label = QLabel()
        self.listwidget = QListWidget()
        self.initGUI()

    def initGUI(self):
        self.listwidget.setViewMode(QListView.IconMode)
        qPixmap = QPixmap('images/002.jpg')
        self.label.setPixmap(qPixmap)
        image_list_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        image_list_item.setIcon(icon)
        self.listwidget.addItem(image_list_item)

        w = self.listwidget.sizeHintForColumn(0) + 2 * self.listwidget.frameWidth()
        self.listwidget.setFixedSize(w, 512)

        qPixmap = QPixmap('images/003.jpg')
        image_list_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        image_list_item.setIcon(icon)
        self.listwidget.addItem(image_list_item)

        self.layout.addWidget(self.listwidget)
        self.layout.addWidget(self.label)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()