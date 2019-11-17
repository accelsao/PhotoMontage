import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter
from PyQt5.QtCore import pyqtSlot, QPointF, QSize


class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.img = None
        self.update_pos = False
        self.start_pos = None
        self.current_pos = None
        self.img_pos_x = None
        self.img_pos_y = None
        self.new_img_pos_x = None
        self.new_img_pos_y = None

    def setPixmap(self, QPixmap):
        self.img = QPixmap
        self.img_pos_x = self.img.width() / 2
        self.img_pos_y = self.img.height() / 2
        self.new_img_pos_x = self.img_pos_x
        self.new_img_pos_y = self.img_pos_y

    def paintEvent(self, QPaintEvent):

        if self.img is not None:

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(
            #     # self.width() - self.img.width(),
            #     # self.height() - self.img.height(),
            #     # self.width() / 2 - self.img.width() / 2,
            #     # self.height() / 2 - self.img.height() / 2,
                QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
                # self.width() / 2,
                # self.height() / 2,
            #     # self.pos.x() - self.img.width() / 2,
            #     # self.pos.y() - self.img.height() / 2,
            #     # self.img.width() / 2,
            #     # self.img.height() / 2,
                self.img
            )

    def mousePressEvent(self, QMouseEvent):
        self.update_pos = True
        self.start_pos = QMouseEvent.pos()

    def mouseMoveEvent(self, QMouseEvent):
        self.current_pos = QMouseEvent.pos()
        self.new_img_pos_x = self.img_pos_x + self.current_pos.x() - self.start_pos.x()
        self.new_img_pos_y = self.img_pos_y + self.current_pos.y() - self.start_pos.y()
        # if self.update_pos:
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        self.update_pos = False
        self.img_pos_y, self.img_pos_x = self.new_img_pos_y, self.new_img_pos_x


class ImgLabel2(QWidget):
    def __init__(self):
        super(ImgLabel2, self).__init__()


        print(self.img.size())
        self.resize(self.img.size())
        print(self.size())

        self.update_pos = False
        self.start_pos = None
        self.current_pos = None
        self.img_pos_x = self.img.width() / 2
        self.img_pos_y = self.img.height() / 2
        self.new_img_pos_x = self.img_pos_x
        self.new_img_pos_y = self.img_pos_y
        self.time_count = 0

    def paintEvent(self, QPaintEvent):

        self.time_count += 1
        print(self.time_count)
        # print(self.size())
        # print(self.pixmap().size())
        # print(self.img.size())
        # print('PaintEvent')
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)
        # print(self.width(), self.height())
        # # print(self.img.width(), self.img.height())
        painter.drawPixmap(
        #     # self.width() - self.img.width(),
        #     # self.height() - self.img.height(),
        #     # self.width() / 2 - self.img.width() / 2,
        #     # self.height() / 2 - self.img.height() / 2,
            QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
            # self.width() / 2,
            # self.height() / 2,
        #     # self.pos.x() - self.img.width() / 2,
        #     # self.pos.y() - self.img.height() / 2,
        #     # self.img.width() / 2,
        #     # self.img.height() / 2,
            self.img
        )

    def mousePressEvent(self, QMouseEvent):
        self.update_pos = True
        self.start_pos = QMouseEvent.pos()

    def mouseMoveEvent(self, QMouseEvent):
        self.current_pos = QMouseEvent.pos()
        self.new_img_pos_x = self.img_pos_x + self.current_pos.x() - self.start_pos.x()
        self.new_img_pos_y = self.img_pos_y + self.current_pos.y() - self.start_pos.y()
        # if self.update_pos:
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        self.update_pos = False
        self.img_pos_y, self.img_pos_x = self.new_img_pos_y, self.new_img_pos_x

class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        # super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        # self.width = 320
        # self.height = 200
        self.button = None
        # self.initUI()
        self.img = QPixmap('./images/123.jpg')
        assert type(self.img) == QPixmap
        self.img = 123
        assert type(self.img) == int
        self.img = QLabel()
        self.img = QPixmap('./images/123.jpg')
        assert type(self.img) == QPixmap
        exit(0)
        # self.resize(self.img.size())
        self.resize(QSize(1200, 800))
        # self.label = ImgLabel()
        self.label = ImgLabel()
        self.label.setPixmap(self.img)
        # print(self.img.size())
        # self.resize(self.img.size())
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        # layout.addWidget(self.button)
        # print(self.label.size())
        # self.label.setPixmap(QPixmap('./images/123.jpg'))
        # print('Trigger')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_click)
        self.button = button

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        # self.label.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())