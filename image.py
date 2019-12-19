from PyQt5.QtCore import Qt, QPointF, QRectF, QSize
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QLabel
from copy import deepcopy


class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.imgLayer = []
        self.imgLayerTopLeft = []
        self.imgLayerNewTopLeft = []
        self.imgLayerBottomRight = []
        self.imgLayerNewBottomRight = []

        self.resize_and_turn_margin = 30

        self.update_pos = False
        self.update_corner = -1  # 0 for left top, 1 for right top, 2 for bottom right, 3 for bottom left

        self.start_pos = None
        self.current_pos = None

        self.minImgSize = 50

        # self.img_pos_x = None
        # self.img_pos_y = None
        # self.new_img_pos_x = None
        # self.new_img_pos_y = None
        self.drawRectmode = False

        self.selectedImgIndex = -1
        # self.selectedImg = None
        # self.selectedImgPos = None
        # self.selectedImgNewPos = None

        # 0 for move (default), 1 for resize, 2 for flip, 3 for turn
        # rectcolor red:0 cyan: 1 green:2 black:3
        self.mode = 0

        self.bgsize = QSize()

    def initialize(self):
        self.imgLayer = []
        self.imgLayerTopLeft = []
        self.imgLayerNewTopLeft = []
        self.imgLayerBottomRight = []
        self.imgLayerNewBottomRight = []
        self.mode = -1
        self.selectedImgIndex = -1
        self.drawRectmode = False
        self.bgsize = QSize()

    def blending(self):
        # out = QPixmap(self.imgLayer[0].size())
        out = QPixmap(self.bgsize)
        out.fill(Qt.transparent)
        pt = QPainter(out)
        # pt.setCompositionMode(0)

        for i, (img, tl, br) in enumerate(zip(self.imgLayer, self.imgLayerTopLeft, self.imgLayerBottomRight)):
            resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
            pt.drawPixmap(tl, resized_img)
        return out

    def addPixmap(self, qPixmap):

        if len(self.imgLayer) == 0:
            self.resize(qPixmap.size())
            self.bgsize = qPixmap.size()
        else:
            # qPixmap.scaledToHeight(self.img_layers[0].height())
            # qPixmap.scaledToWidth(self.img_layers[0].width())
            pass

        self.imgLayer.append(qPixmap)
        # self.img_layers.append(qPixmap)

        self.imgLayerTopLeft.append(QPointF(0, 0))
        self.imgLayerNewTopLeft.append(QPointF(0, 0))

        self.imgLayerTopLeft.append(QPointF(0, 0))
        self.imgLayerNewTopLeft.append(QPointF(0, 0))

        self.imgLayerBottomRight.append(QPointF(qPixmap.width(), qPixmap.height()))
        self.imgLayerNewBottomRight.append(QPointF(qPixmap.width(), qPixmap.height()))

        # self.img_layers_pos.append(QPointF(0, 0))

        # self.selectedImg = qPixmap
        # self.selectedImgPos = QPointF(0, 0)
        # self.selectedImgNewPos = QPointF(0, 0)
        print('pass3')
        self.selectedImgIndex = -1

        print('pass4')
        self.setPixmap(self.blending())

        print('pass5')
        self.mode = 0
        self.drawRectmode = False

    def selectImage(self, index):
        if self.selectedImgIndex == index or index == 0:
            self.selectedImgIndex = -1
            self.drawRectmode = False
        elif index > 0:
            self.selectedImgIndex = index
            self.drawRectmode = True

        self.repaint()

    def paintEvent(self, event):
        super(ImgLabel, self).paintEvent(event)

        if len(self.imgLayer) > 0:

            print('Start Drawing')

            self.resize(self.imgLayer[0].size())
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            if self.mode == 0:
                for i, (img, tl, br) in enumerate(
                        zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight)):
                    resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
                    painter.drawPixmap(tl, resized_img)

                # for i, (img, pos) in enumerate(zip(self.imgLayer, self.imgLayerNewTopLeft)):
                #     painter.drawPixmap(pos, img)
            elif self.mode == 1:  # RESIZE
                print('start to set resized img')

                for i, (img, tl, br) in enumerate(
                        zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight)):
                    resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
                    painter.drawPixmap(tl, resized_img)

                # for i, (img, pos, corn) in enumerate(zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight)):
                #     resized_img = img.copy().scaled(corn[1].x() - corn[0].x(), corn[1].y() - corn[0].y())
                #     painter.drawPixmap(pos, resized_img)
                #     print(img)
                #     print(corn)
                #     print(pos)

            if self.drawRectmode is True:
                paintRect = QPen(Qt.red)
                if self.mode == 1:

                    paintRect = QPen(Qt.cyan)
                elif self.mode == 2:

                    paintRect = QPen(Qt.green)
                elif self.mode == 3:

                    paintRect = QPen(Qt.blue)
                paintRect.setWidth(5)
                painter.setPen(paintRect)
                # print(self.imgLayerNewTopLeft[self.selectedImgIndex].x())
                # print(self.imgLayer[self.selectedImgIndex].width())
                painter.drawRect(QRectF(self.imgLayerNewTopLeft[self.selectedImgIndex].x(),
                                        self.imgLayerNewTopLeft[self.selectedImgIndex].y(),
                                        # self.imgLayerNewTopLeft[self.selectedImgIndex].y(),
                                        # self.imgLayerNewBottomRight[self.selectedImgIndex].x() - self.imgLayerNewTopLeft[self.selectedImgIndex].x(),
                                        self.imgLayerNewBottomRight[self.selectedImgIndex].x() -
                                        self.imgLayerNewTopLeft[self.selectedImgIndex].x(),
                                        self.imgLayerNewBottomRight[self.selectedImgIndex].y() -
                                        self.imgLayerNewTopLeft[self.selectedImgIndex].y()
                                        ))

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

    def mousePressEvent(self, e):

        if self.selectedImgIndex > 0:

            if self.mode == 0:  # Move
                if self.imgLayerTopLeft[self.selectedImgIndex].x() <= e.pos().x() <= self.imgLayerBottomRight[
                    self.selectedImgIndex].x() and \
                        self.imgLayerTopLeft[self.selectedImgIndex].y() <= e.pos().y() <= self.imgLayerBottomRight[
                    self.selectedImgIndex].y():
                    self.update_pos = True
                    self.start_pos = e.pos()
                    self.imgLayerNewTopLeft = deepcopy(self.imgLayerTopLeft)
                    self.imgLayerNewBottomRight = deepcopy(self.imgLayerBottomRight)
            elif self.mode == 1:  # RESIZE
                # left top
                self.imgLayerNewTopLeft = deepcopy(self.imgLayerTopLeft)
                self.imgLayerNewBottomRight = deepcopy(self.imgLayerBottomRight)
                # top left
                if abs(self.imgLayerTopLeft[self.selectedImgIndex].x() - e.pos().x()) <= self.resize_and_turn_margin and \
                        abs(self.imgLayerTopLeft[
                                self.selectedImgIndex].y() - e.pos().y()) <= self.resize_and_turn_margin:
                    self.update_corner = 0
                    self.start_pos = e.pos()
                # top right
                elif abs(self.imgLayerBottomRight[
                             self.selectedImgIndex].x() - e.pos().x()) <= self.resize_and_turn_margin and \
                        abs(self.imgLayerTopLeft[
                                self.selectedImgIndex].y() - e.pos().y()) <= self.resize_and_turn_margin:
                    self.update_corner = 1
                    self.start_pos = e.pos()
                # bottom left
                elif abs(self.imgLayerTopLeft[
                             self.selectedImgIndex].x() - e.pos().x()) <= self.resize_and_turn_margin and \
                        abs(self.imgLayerBottomRight[
                                self.selectedImgIndex].y() - e.pos().y()) <= self.resize_and_turn_margin:
                    self.update_corner = 2
                    self.start_pos = e.pos()
                # bottom right
                elif abs(self.imgLayerBottomRight[
                             self.selectedImgIndex].x() - e.pos().x()) <= self.resize_and_turn_margin and \
                        abs(self.imgLayerBottomRight[
                                self.selectedImgIndex].y() - e.pos().y()) <= self.resize_and_turn_margin:
                    self.update_corner = 3
                    self.start_pos = e.pos()

    def mouseMoveEvent(self, e):

        if len(self.imgLayer) > 0 and self.selectedImgIndex > 0:

            if self.mode == 0:
                self.current_pos = e.pos()
                self.imgLayerNewTopLeft[self.selectedImgIndex] = QPointF(
                    self.imgLayerTopLeft[self.selectedImgIndex].x() +
                    self.current_pos.x() - self.start_pos.x(),
                    self.imgLayerTopLeft[self.selectedImgIndex].y() +
                    self.current_pos.y() - self.start_pos.y())
                self.imgLayerNewBottomRight[self.selectedImgIndex] = QPointF(
                    self.imgLayerBottomRight[self.selectedImgIndex].x() +
                    self.current_pos.x() - self.start_pos.x(),
                    self.imgLayerBottomRight[self.selectedImgIndex].y() +
                    self.current_pos.y() - self.start_pos.y())

                # self.selectedImgNewPos = QPointF(self.selectedImgPos.x() + self.current_pos.x() - self.start_pos.x(),
                #                                  self.selectedImgPos.y() + self.current_pos.y() - self.start_pos.y())

                if self.update_pos:
                    self.update()
            elif self.mode == 1 and 0 <= self.update_corner <= 3:
                # print('GGO')
                print(self.start_pos, e.pos())
                self.current_pos = e.pos()
                if self.update_corner == 0:  # left top

                    self.imgLayerNewTopLeft[self.selectedImgIndex].setX(
                        min(
                            max(self.imgLayerTopLeft[
                                    self.selectedImgIndex].x() + self.current_pos.x() - self.start_pos.x(), 0.0),
                            self.imgLayerBottomRight[self.selectedImgIndex].x() - self.minImgSize)
                    )
                    self.imgLayerNewTopLeft[self.selectedImgIndex].setY(
                        min(
                            max(self.imgLayerTopLeft[
                                    self.selectedImgIndex].y() + self.current_pos.y() - self.start_pos.y(), 0.0),
                            self.imgLayerBottomRight[self.selectedImgIndex].y() - self.minImgSize)
                    )
                    self.update()

                elif self.update_corner == 3:  # bottom right
                    print(self.bgsize.width())
                    print(self.bgsize.height())
                    print(self.bgsize)

                    self.imgLayerNewBottomRight[self.selectedImgIndex].setX(
                        max(
                            min(self.imgLayerBottomRight[
                                    self.selectedImgIndex].x() + self.current_pos.x() - self.start_pos.x(),
                                self.bgsize.width()),
                            self.imgLayerTopLeft[self.selectedImgIndex].x() + self.minImgSize)
                    )
                    self.imgLayerNewBottomRight[self.selectedImgIndex].setY(
                        max(
                            min(self.imgLayerBottomRight[
                                    self.selectedImgIndex].y() + self.current_pos.y() - self.start_pos.y(),
                                self.bgsize.height()),
                            self.imgLayerTopLeft[self.selectedImgIndex].y() + self.minImgSize)
                    )
                print('start update')
                self.update()

    def mouseReleaseEvent(self, QMouseEvent):

        if self.mode == 0:  # Move
            self.update_pos = False
            self.imgLayerTopLeft = deepcopy(self.imgLayerNewTopLeft)
            self.imgLayerBottomRight = deepcopy(self.imgLayerNewBottomRight)
            self.setPixmap(self.blending())
        elif self.mode == 1:  # RESIZE
            self.update_corner = -1
            self.imgLayerTopLeft = deepcopy(self.imgLayerNewTopLeft)
            self.imgLayerBottomRight = deepcopy(self.imgLayerNewBottomRight)
            self.setPixmap(self.blending())
