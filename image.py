from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel





class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.imgLayer = []
        self.imgLayerPos = []
        self.imgLayerNewPos = []
        self.update_pos = False
        self.start_pos = None
        self.current_pos = None

        # self.img_pos_x = None
        # self.img_pos_y = None
        # self.new_img_pos_x = None
        # self.new_img_pos_y = None
        self.drawRect = False

        self.selectedImgIndex = -1
        # self.selectedImg = None
        # self.selectedImgPos = None
        # self.selectedImgNewPos = None

    def initialize(self):
        self.imgLayer = []
        self.imgLayerPos = []
        self.imgLayerNewPos = []

    def blending(self):
        out = QPixmap(self.imgLayer[0].size())
        out.fill(Qt.transparent)
        pt = QPainter(out)
        # pt.setCompositionMode(0)


        for i, (img, pos) in enumerate(zip(self.imgLayer, self.imgLayerPos)):
            pt.drawPixmap(pos, img)
        return out

    def addPixmap(self, qPixmap):

        if len(self.imgLayer) == 0:
            self.resize(qPixmap.size())
        else:
            # qPixmap.scaledToHeight(self.img_layers[0].height())
            # qPixmap.scaledToWidth(self.img_layers[0].width())
            pass
        print('pass1')
        self.imgLayer.append(qPixmap)
        # self.img_layers.append(qPixmap)

        print('pass2')
        self.imgLayerPos.append(QPointF(0, 0))
        self.imgLayerNewPos.append(QPointF(0, 0))

        # self.img_layers_pos.append(QPointF(0, 0))

        # self.selectedImg = qPixmap
        # self.selectedImgPos = QPointF(0, 0)
        # self.selectedImgNewPos = QPointF(0, 0)
        print('pass3')
        self.selectedImgIndex = -1

        print('pass4')
        self.setPixmap(self.blending())

        print('pass5')
        self.drawRect = False

    def selectImage(self, index):
        if self.selectedImgIndex == index or index == 0:
            self.selectedImgIndex = -1
            self.drawRect = False
        elif index > 0:
            self.selectedImgIndex = index
            self.drawRect = True

        self.repaint()

    def paintEvent(self, event):
        super(ImgLabel, self).paintEvent(event)


        if len(self.imgLayer) > 0:

            print('Start Drawing')

            self.resize(self.imgLayer[0].size())
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            for i, (img, pos) in enumerate(zip(self.imgLayer, self.imgLayerNewPos)):
                painter.drawPixmap(pos, img)

            # print('DRaw OK')
            print(self.drawRect)

            if self.drawRect is True:
                paintRect = QPen(Qt.red)
                paintRect.setWidth(5)
                painter.setPen(paintRect)
                print(self.imgLayerNewPos[self.selectedImgIndex].x())
                print(self.imgLayer[self.selectedImgIndex].width())
                painter.drawRect(QRectF(self.imgLayerNewPos[self.selectedImgIndex].x(),
                                 self.imgLayerNewPos[self.selectedImgIndex].y(),
                                 self.imgLayer[self.selectedImgIndex].width(),
                                 self.imgLayer[self.selectedImgIndex].height()))

                # painter.drawRect(self.selectedImgNewPos.x() - self.selectedImg.width() / 2,
                #                  self.selectedImgNewPos.y() - self.selectedImg.height() / 2,
                #                  self.selectedImg.width(), self.selectedImg.height())


        # if self.img is not None:
        #     painter = QPainter(self)
        #     painter.setRenderHint(QPainter.Antialiasing)
        #     painter.drawPixmap(
        #         QPointF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2),
        #         self.img
        #     )
        #     if self.drawRect is True:
        #         paintRect = QPen(Qt.red)
        #         paintRect.setWidth(5)
        #         painter.setPen(paintRect)
        #         painter.drawRect(
        #             QRectF(self.new_img_pos_x - self.img.width() / 2, self.new_img_pos_y - self.img.height() / 2,
        #                    self.img.width(), self.img.height()))

    def mousePressEvent(self, QMouseEvent):

        self.update_pos = True
        self.start_pos = QMouseEvent.pos()
        self.imgLayerNewPos = self.imgLayerPos.copy()


    def mouseMoveEvent(self, QMouseEvent):

        # if self.img is not None:
        #     self.current_pos = QMouseEvent.pos()
        #     self.new_img_pos_x = self.img_pos_x + self.current_pos.x() - self.start_pos.x()
        #     self.new_img_pos_y = self.img_pos_y + self.current_pos.y() - self.start_pos.y()
        #     if self.update_pos:
        #         self.update()

        if len(self.imgLayer) > 0 and self.selectedImgIndex > 0:
            self.current_pos = QMouseEvent.pos()

            self.imgLayerNewPos[self.selectedImgIndex] = QPointF(self.imgLayerPos[self.selectedImgIndex].x() +
                                                                 self.current_pos.x() - self.start_pos.x(),
                                                                 self.imgLayerPos[self.selectedImgIndex].y() +
                                                                 self.current_pos.y() - self.start_pos.y())

            # self.selectedImgNewPos = QPointF(self.selectedImgPos.x() + self.current_pos.x() - self.start_pos.x(),
            #                                  self.selectedImgPos.y() + self.current_pos.y() - self.start_pos.y())

            if self.update_pos:
                self.update()

    def mouseReleaseEvent(self, QMouseEvent):

        self.update_pos = False
        self.imgLayerPos = self.imgLayerNewPos.copy()

        self.setPixmap(self.blending())
        # self.img_pos_y, self.img_pos_x = self.new_img_pos_y, self.new_img_pos_x
