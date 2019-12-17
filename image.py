from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel


class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.img = None
        self.img_layers = []
        self.update_pos = False
        self.start_pos = None
        self.current_pos = None
        self.img_pos_x = None
        self.img_pos_y = None
        self.new_img_pos_x = None
        self.new_img_pos_y = None
        # self.resize(QSize(1920, 1280))

    def blending(self, img_layers):

        out = QPixmap(img_layers[0].size())
        out.fill(Qt.transparent)
        pt = QPainter(out)
        pt.setCompositionMode(0)
        for i, img in enumerate(img_layers):
            pt.drawImage(0, 0, img.toImage())
        return out

    def setPixmap(self, qPixmap):

        if len(self.img_layers) == 0:
            self.resize(qPixmap.size())
        else:
            qPixmap.scaledToHeight(self.img_layers[0].height())
            qPixmap.scaledToWidth(self.img_layers[0].width())


        self.img_layers.append(qPixmap)
        self.img = self.blending(self.img_layers)
        # self.img = self.img_layers[-1]
        # self.img = QPixmap

        self.img_pos_x = self.img.width() / 2
        self.img_pos_y = self.img.height() / 2
        self.new_img_pos_x = self.img_pos_x
        self.new_img_pos_y = self.img_pos_y
        self.drawRect = False

        # TODO delete
        # self.img = None

    def selectImage(self, index):
        self.drawRect = True
        self.update()
        print('select {}'.format(index))

    def paintEvent(self, QPaintEvent):


        if self.img is not None:
            self.resize(self.img.size())

        if self.img is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(
                QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
                self.img
            )
            if self.drawRect is True:
                paintRect = QPen(Qt.red)
                paintRect.setWidth(5)
                painter.setPen(paintRect)
                painter.drawRect(QRectF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2,
                                        self.img.width(), self.img.height()))



    def mousePressEvent(self, QMouseEvent):

        self.update_pos = True
        self.start_pos = QMouseEvent.pos()


    def mouseMoveEvent(self, QMouseEvent):

        if self.img is not None:
            self.current_pos = QMouseEvent.pos()
            self.new_img_pos_x = self.img_pos_x + self.current_pos.x() - self.start_pos.x()
            self.new_img_pos_y = self.img_pos_y + self.current_pos.y() - self.start_pos.y()
            if self.update_pos:
                self.update()



    def mouseReleaseEvent(self, QMouseEvent):

        self.update_pos = False
        self.img_pos_y, self.img_pos_x = self.new_img_pos_y, self.new_img_pos_x

