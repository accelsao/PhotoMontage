from PyQt5.QtCore import Qt, QPointF, QRectF, QSize, QLine, QLineF
from PyQt5.QtGui import QPainter, QPen, QPixmap, QTransform, QImage, QPolygonF
from PyQt5.QtWidgets import QLabel
from copy import deepcopy


# def getflipImg(src):
#     # (qPixmap) src
#     dst = QImage(src.width(), src.height(), QImage.Format_ARGB32)
#



class ImgLabel(QLabel):
    def __init__(self):
        super(ImgLabel, self).__init__()

        self.imgLayer = []
        self.imgLayerTopLeft = []
        self.imgLayerNewTopLeft = []
        self.imgLayerBottomRight = []
        self.imgLayerNewBottomRight = []
        self.imgLayerAngle = []
        self.imgLayerNewAngle = []


        self.resize_and_turn_margin = 30

        self.update_move = False
        self.update_resize = -1  # 0 for left top, 1 for right top, 2 for bottom right, 3 for bottom left
        self.update_flip = False
        self.update_rotate = False

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
        self.mode = 0
        self.selectedImgIndex = -1
        self.drawRectmode = False
        self.bgsize = QSize()

    def blending(self):
        # out = QPixmap(self.imgLayer[0].size())
        out = QPixmap(self.bgsize)
        out.fill(Qt.transparent)
        pt = QPainter(out)
        # pt.setCompositionMode(0)

        for i, (img, tl, br, ang) in enumerate(
                zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight, self.imgLayerNewAngle)):
            resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
            center = QPointF(tl.x() + (br.x() - tl.x()) / 2, tl.y() + (br.y() - tl.y()) / 2)
            pt.translate(center)
            pt.rotate(-ang)
            pt.translate(-center)
            pt.drawPixmap(tl, resized_img)

        # for i, (img, tl, br) in enumerate(zip(self.imgLayer, self.imgLayerTopLeft, self.imgLayerBottomRight)):
        #     resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
        #     pt.drawPixmap(tl, resized_img)
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

        self.imgLayerAngle.append(0.0)
        self.imgLayerNewAngle.append(0.0)

        self.selectedImgIndex = -1

        self.setPixmap(self.blending())

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

            for i, (img, tl, br, ang) in enumerate(
                    zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight, self.imgLayerNewAngle)):
                resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
                center = QPointF(tl.x() + (br.x() - tl.x()) / 2, tl.y() + (br.y() - tl.y()) / 2)
                painter.translate(center)
                print(ang)
                painter.rotate(-ang)
                painter.translate(-center)
                painter.drawPixmap(tl, resized_img)

            print(self.drawRectmode)
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

        if self.selectedImgIndex > 0 and self.mode >= 0:
            print('Start')
            tl = self.imgLayerTopLeft[self.selectedImgIndex]
            br = self.imgLayerBottomRight[self.selectedImgIndex]
            ang = self.imgLayerAngle[self.selectedImgIndex]
            print(tl, br, ang)
            ct = QPointF((tl.x() + br.x()) / 2, (tl.y() + br.y()) / 2)
            print(ct)
            rect = QRectF(tl, br)
            print(rect)
            trans = QTransform()
            trans.translate(ct.x(), ct.y())
            trans.rotate(-ang)
            trans.translate(-ct.x(), -ct.y())


            tran_polygon = trans.map(QPolygonF(rect))
            self.start_pos = e.pos()

            if self.mode == 0 or self.mode == 3:  # MOVE or ROTATE
                if tran_polygon.containsPoint(self.start_pos, 0):
                    if self.mode == 0:
                        self.update_move = True
                        self.imgLayerNewTopLeft = deepcopy(self.imgLayerTopLeft)
                        self.imgLayerNewBottomRight = deepcopy(self.imgLayerBottomRight)
                    else:
                        self.update_rotate = True
                        self.imgLayerNewAngle = deepcopy(self.imgLayerAngle)
            elif self.mode == 2:  # FLIP
                self.update_flip = True
            elif self.mode == 1:  # RESIZE

                #  topleft
                topLeftBox = trans.map(QPolygonF(
                    QRectF(tl.x() - self.resize_and_turn_margin, tl.y() - self.resize_and_turn_margin,
                           self.resize_and_turn_margin * 2, self.resize_and_turn_margin * 2)))
                # topRight
                topRightBox = trans.map(QPolygonF(
                    QRectF(br.x() - self.resize_and_turn_margin, tl.y() - self.resize_and_turn_margin,
                           self.resize_and_turn_margin * 2, self.resize_and_turn_margin * 2)))
                # bottomLeft
                bottomLeftBox = trans.map(QPolygonF(
                    QRectF(tl.x() - self.resize_and_turn_margin, br.y() - self.resize_and_turn_margin,
                           self.resize_and_turn_margin * 2, self.resize_and_turn_margin * 2)))
                # bottomRight
                bottomRightBox = trans.map(QPolygonF(
                    QRectF(br.x() - self.resize_and_turn_margin, br.y() - self.resize_and_turn_margin,
                           self.resize_and_turn_margin * 2, self.resize_and_turn_margin * 2)))

                self.imgLayerNewTopLeft = deepcopy(self.imgLayerTopLeft)
                self.imgLayerNewBottomRight = deepcopy(self.imgLayerBottomRight)
                if topLeftBox.containsPoint(self.start_pos, 0):
                    self.update_resize = 0
                elif topRightBox.containsPoint(self.start_pos, 0):
                    self.update_resize = 1
                elif bottomLeftBox.containsPoint(self.start_pos, 0):
                    self.update_resize = 2
                elif bottomRightBox.containsPoint(self.start_pos, 0):
                    self.update_resize = 3

    def mouseMoveEvent(self, e):

        if len(self.imgLayer) > 0 and self.selectedImgIndex > 0:

            if self.mode == 0 and self.update_move:
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
                self.update()
            elif self.mode == 1 and 0 <= self.update_resize <= 3:
                self.current_pos = e.pos()
                if self.update_resize == 0:  # left top
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

                elif self.update_resize == 3:  # bottom right
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
                self.update()

            elif self.mode == 3 and self.update_rotate:  # rotate
                self.current_pos = e.pos()
                center = QPointF((self.imgLayerTopLeft[self.selectedImgIndex].x() + self.imgLayerBottomRight[
                    self.selectedImgIndex].x()) / 2,
                                 (self.imgLayerTopLeft[self.selectedImgIndex].y() + self.imgLayerBottomRight[
                                     self.selectedImgIndex].y()) / 2,
                                 )
                # vector_a = QLineF(self.start_pos, center)
                # vector_b = QLineF(self.current_pos, center)
                vector_a = QLineF(center, self.start_pos)
                vector_b = QLineF(center, self.current_pos)
                self.imgLayerNewAngle[self.selectedImgIndex] = vector_b.angle() - vector_a.angle() + self.imgLayerAngle[self.selectedImgIndex]
                self.update()




    def mouseReleaseEvent(self, QMouseEvent):

        if self.mode == 0:  # Move
            self.update_move = False
            self.imgLayerTopLeft = deepcopy(self.imgLayerNewTopLeft)
            self.imgLayerBottomRight = deepcopy(self.imgLayerNewBottomRight)

        elif self.mode == 1:  # RESIZE
            self.update_resize = -1
            self.imgLayerTopLeft = deepcopy(self.imgLayerNewTopLeft)
            self.imgLayerBottomRight = deepcopy(self.imgLayerNewBottomRight)

        elif self.mode == 2:
            print(self.update_flip)
            if self.update_flip:
                self.update_flip = False
                print(self.imgLayer[self.selectedImgIndex])
                print(self.selectedImgIndex)
                print(self.imgLayer)
                self.imgLayer[self.selectedImgIndex] = self.imgLayer[self.selectedImgIndex].transformed(QTransform().scale(-1, 1))
                # print(self.imgLayerq)
                print(self.imgLayer[self.selectedImgIndex])
                self.update()

        elif self.mode == 3:
            if self.update_rotate:
                self.update_rotate = False
                print(self.imgLayerNewAngle)
                self.imgLayerAngle = deepcopy(self.imgLayerNewAngle)
                print(self.imgLayerAngle)


        if 0 <= self.mode < 4:
            self.setPixmap(self.blending())
