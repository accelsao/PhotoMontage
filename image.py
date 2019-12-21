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
        self.minImgSize = 50

        self.update_move = False
        """
        topLeft: 0, topRight: 1, bottomLeft: 2, bottomRight: 3
        """
        self.update_resize = -1
        self.update_flip = False
        self.update_rotate = False
        self.drawRectmode = False
        self.selectedImgIndex = -1
        self.mode = 0
        self.bgsize = QSize()

    def initialize(self):
        self.imgLayer = []
        self.imgLayerTopLeft = []
        self.imgLayerNewTopLeft = []
        self.imgLayerBottomRight = []
        self.imgLayerNewBottomRight = []
        self.imgLayerAngle = []
        self.imgLayerNewAngle = []
        # (default) MOVE
        self.mode = 0
        # (default) None
        self.selectedImgIndex = -1
        self.drawRectmode = False
        self.bgsize = QSize()

    def blending(self):
        # out = QPixmap(self.imgLayer[0].size())
        out = QPixmap(self.bgsize)
        out.fill(Qt.transparent)
        pt = QPainter(out)
        # pt.setCompositionMode(0)
        # print('self.imgLayerAngle: {}'.format(self.imgLayerAngle))
        # print('self.imgLayerNewAngle: {}'.format(self.imgLayerNewAngle))

        for i, (img, tl, br, ang) in enumerate(
                zip(self.imgLayer, self.imgLayerTopLeft, self.imgLayerBottomRight, self.imgLayerAngle)):
            resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
            center = QPointF(tl.x() + (br.x() - tl.x()) / 2, tl.y() + (br.y() - tl.y()) / 2)
            # print('ang[{}]: {}'.format(i, ang))
            pt.translate(center)
            pt.rotate(-ang)
            pt.translate(-center)
            pt.drawPixmap(tl, resized_img)
            pt.resetTransform()


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

        # self.order.append(len(self.order))

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
        print('self.imgLayerAngle: {}'.format(self.imgLayerAngle))
        print('self.imgLayerNewAngle: {}'.format(self.imgLayerNewAngle))
        self.selectedImgIndex = -1
        # (default) MOVE
        self.mode = 0
        self.drawRectmode = False

        self.setPixmap(self.blending())

    def selectImage(self, index):
        print(index)
        if self.selectedImgIndex == index or index == 0:
            self.selectedImgIndex = -1
            self.drawRectmode = False
        elif index > 0:
            self.selectedImgIndex = index
            self.drawRectmode = True

        print(self.selectedImgIndex)
        self.repaint()

    def paintEvent(self, event):
        super(ImgLabel, self).paintEvent(event)

        if len(self.imgLayer) > 0:
            self.resize(self.imgLayer[0].size())
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            if self.mode == 1:
                for i, (img, ntl, nbr, ang, tl, br) in enumerate(
                        zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight, self.imgLayerNewAngle, self.imgLayerTopLeft, self.imgLayerBottomRight)):
                    resized_img = img.copy().scaled(nbr.x() - ntl.x(), nbr.y() - ntl.y())
                    center = QPointF(tl.x() + (br.x() - tl.x()) / 2, tl.y() + (br.y() - tl.y()) / 2)
                    painter.translate(center)
                    painter.rotate(-ang)
                    painter.translate(-center)
                    painter.drawPixmap(ntl, resized_img)
                    painter.resetTransform()

                if self.drawRectmode:
                    ntl = self.imgLayerNewTopLeft[self.selectedImgIndex]
                    nbr = self.imgLayerNewBottomRight[self.selectedImgIndex]
                    tl = self.imgLayerTopLeft[self.selectedImgIndex]
                    br = self.imgLayerBottomRight[self.selectedImgIndex]
                    ang = self.imgLayerNewAngle[self.selectedImgIndex]
                    center = QPointF(tl.x() + (br.x() - tl.x()) / 2, tl.y() + (br.y() - tl.y()) / 2)
                    painter.translate(center)
                    painter.rotate(-ang)
                    painter.translate(-center)

                    qpen = QPen(Qt.red)
                    if self.mode == 1:
                        qpen = QPen(Qt.cyan)
                    elif self.mode == 2:
                        qpen = QPen(Qt.green)
                    elif self.mode == 3:
                        qpen = QPen(Qt.blue)

                    qpen.setWidth(5)

                    painter.setPen(qpen)
                    painter.drawRect(QRectF(ntl, nbr))

            else:

                for i, (img, tl, br, ang) in enumerate(
                        zip(self.imgLayer, self.imgLayerNewTopLeft, self.imgLayerNewBottomRight, self.imgLayerNewAngle)):
                    resized_img = img.copy().scaled(br.x() - tl.x(), br.y() - tl.y())
                    center = QPointF(tl.x() + (br.x() - tl.x()) / 2, tl.y() + (br.y() - tl.y()) / 2)
                    painter.translate(center)
                    painter.rotate(-ang)
                    painter.translate(-center)
                    painter.drawPixmap(tl, resized_img)
                    painter.resetTransform()

                if self.drawRectmode:
                    ntl = self.imgLayerNewTopLeft[self.selectedImgIndex]
                    nbr = self.imgLayerNewBottomRight[self.selectedImgIndex]
                    # tl = self.imgLayerTopLeft[self.selectedImgIndex]
                    # br = self.imgLayerBottomRight[self.selectedImgIndex]
                    ang = self.imgLayerNewAngle[self.selectedImgIndex]
                    center = QPointF(ntl.x() + (nbr.x() - ntl.x()) / 2, ntl.y() + (nbr.y() - ntl.y()) / 2)
                    painter.translate(center)
                    painter.rotate(-ang)
                    painter.translate(-center)

                    qpen = QPen(Qt.red)
                    if self.mode == 1:
                        qpen = QPen(Qt.cyan)
                    elif self.mode == 2:
                        qpen = QPen(Qt.green)
                    elif self.mode == 3:
                        qpen = QPen(Qt.blue)

                    qpen.setWidth(5)

                    painter.setPen(qpen)
                    painter.drawRect(QRectF(ntl, nbr))




    def mousePressEvent(self, e):
        print('self.mode: {}'.format(self.mode))
        print('self.selectedImgIndex: {}'.format(self.selectedImgIndex))
        if self.selectedImgIndex > 0 and self.mode != -1:
            tl = self.imgLayerTopLeft[self.selectedImgIndex]
            br = self.imgLayerBottomRight[self.selectedImgIndex]
            ang = self.imgLayerAngle[self.selectedImgIndex]
            ct = QPointF((tl.x() + br.x()) / 2, (tl.y() + br.y()) / 2)
            rect = QRectF(tl, br)
            trans = QTransform()
            trans.translate(ct.x(), ct.y())
            trans.rotate(-ang)
            trans.translate(-ct.x(), -ct.y())
            tran_polygon = trans.map(QPolygonF(rect))
            self.start_pos = e.pos()
            # MOVE or ROTATE
            if (self.mode == 0 or self.mode == 3) and tran_polygon.containsPoint(self.start_pos, 0):
                    if self.mode == 0:
                        self.update_move = True
                        self.imgLayerNewTopLeft = deepcopy(self.imgLayerTopLeft)
                        self.imgLayerNewBottomRight = deepcopy(self.imgLayerBottomRight)
                    else:
                        self.update_rotate = True
                        self.imgLayerNewAngle = deepcopy(self.imgLayerAngle)
            # FLIP
            elif self.mode == 2:
                self.update_flip = True
            # RESIZE
            elif self.mode == 1:
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

                tl = self.imgLayerTopLeft[self.selectedImgIndex]
                br = self.imgLayerBottomRight[self.selectedImgIndex]
                ang = self.imgLayerAngle[self.selectedImgIndex]
                lin = QLineF(self.start_pos, e.pos())
                lin.setAngle(lin.angle() - ang)
                # topLeft
                if self.update_resize == 0:
                    self.imgLayerNewTopLeft[self.selectedImgIndex].setX(
                        min(
                            self.imgLayerTopLeft[self.selectedImgIndex].x() + lin.dx(),
                            self.imgLayerBottomRight[self.selectedImgIndex].x() - self.minImgSize)
                    )
                    self.imgLayerNewTopLeft[self.selectedImgIndex].setY(
                        min(
                            self.imgLayerTopLeft[
                                    self.selectedImgIndex].y() + lin.dy(),
                            self.imgLayerBottomRight[self.selectedImgIndex].y() - self.minImgSize)
                    )
                    self.update()
                # topRight
                elif self.update_resize == 1:
                    self.imgLayerNewBottomRight[self.selectedImgIndex].setX(
                        max(
                            self.imgLayerBottomRight[
                                    self.selectedImgIndex].x() + lin.dx(),
                            self.imgLayerTopLeft[self.selectedImgIndex].x() + self.minImgSize)
                    )
                    self.imgLayerNewTopLeft[self.selectedImgIndex].setY(
                        min(
                            self.imgLayerTopLeft[
                                    self.selectedImgIndex].y() + lin.dy(),
                            self.imgLayerBottomRight[self.selectedImgIndex].y() - self.minImgSize)
                    )
                    self.update()
                # bottomLeft
                elif self.update_resize == 2:
                    self.imgLayerNewTopLeft[self.selectedImgIndex].setX(
                        min(
                            self.imgLayerTopLeft[self.selectedImgIndex].x() + lin.dx(),
                            self.imgLayerBottomRight[self.selectedImgIndex].x() - self.minImgSize)
                    )
                    self.imgLayerNewBottomRight[self.selectedImgIndex].setY(
                        max(
                            self.imgLayerBottomRight[
                                self.selectedImgIndex].y() + lin.dy(),
                            self.imgLayerTopLeft[self.selectedImgIndex].y() + self.minImgSize)
                    )
                    self.update()
                elif self.update_resize == 3:  # bottom right
                    self.imgLayerNewBottomRight[self.selectedImgIndex].setX(
                        max(
                            self.imgLayerBottomRight[
                                    self.selectedImgIndex].x() + lin.dx(),
                            self.imgLayerTopLeft[self.selectedImgIndex].x() + self.minImgSize)
                    )
                    self.imgLayerNewBottomRight[self.selectedImgIndex].setY(
                        max(
                            self.imgLayerBottomRight[
                                    self.selectedImgIndex].y() + lin.dy(),
                            self.imgLayerTopLeft[self.selectedImgIndex].y() + self.minImgSize)
                    )
                    self.update()

            elif self.mode == 3 and self.update_rotate:  # rotate
                center = QPointF((self.imgLayerTopLeft[self.selectedImgIndex].x() + self.imgLayerBottomRight[
                    self.selectedImgIndex].x()) / 2,
                                 (self.imgLayerTopLeft[self.selectedImgIndex].y() + self.imgLayerBottomRight[
                                     self.selectedImgIndex].y()) / 2,
                                 )
                # vector_a = QLineF(self.start_pos, center)
                # vector_b = QLineF(self.current_pos, center)
                vector_a = QLineF(center, self.start_pos)
                vector_b = QLineF(center, e.pos())
                self.imgLayerNewAngle[self.selectedImgIndex] = vector_b.angle() - vector_a.angle() + self.imgLayerAngle[self.selectedImgIndex]
                self.update()




    def mouseReleaseEvent(self, QMouseEvent):

        if self.mode == 0:  # Move
            self.update_move = False
            self.imgLayerTopLeft = deepcopy(self.imgLayerNewTopLeft)
            self.imgLayerBottomRight = deepcopy(self.imgLayerNewBottomRight)

        elif self.mode == 1:  # RESIZE
            self.update_resize = -1
            print('resize release')
            tras = QTransform()
            tl = self.imgLayerTopLeft[self.selectedImgIndex]
            br = self.imgLayerBottomRight[self.selectedImgIndex]
            ntl = self.imgLayerNewTopLeft[self.selectedImgIndex]
            nbr = self.imgLayerNewBottomRight[self.selectedImgIndex]
            ang = self.imgLayerAngle[self.selectedImgIndex]
            ct = QRectF(tl, br).center()
            tras.translate(ct.x(), ct.y())
            tras.rotate(-ang)
            tras.translate(-ct.x(), -ct.y())
            ct2 = QRectF(ntl, nbr).center()
            tras.translate(ct2.x(), ct2.y())
            tras.rotate(+ang)
            tras.translate(-ct2.x(), -ct2.y())
            rect = tras.map(QPolygonF(QRectF(ntl, nbr))).boundingRect()
            self.imgLayerNewTopLeft[self.selectedImgIndex] = rect.topLeft()
            self.imgLayerNewBottomRight[self.selectedImgIndex] = rect.bottomRight()
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

    def reorder(self, indexFrom, indexTo):
        assert indexFrom > 0 and indexTo > 0
        item = self.imgLayer[indexFrom]
        del self.imgLayer[indexFrom]
        self.imgLayer.insert(indexTo, item)
        print('start reorder')
        item = self.imgLayerTopLeft[indexFrom]
        del self.imgLayerTopLeft[indexFrom]
        self.imgLayerTopLeft.insert(indexTo, item)
        print('start reorder1')
        item = self.imgLayerBottomRight[indexFrom]
        del self.imgLayerBottomRight[indexFrom]
        self.imgLayerBottomRight.insert(indexTo, item)
        print('start reorder2')
        item = self.imgLayerNewTopLeft[indexFrom]
        del self.imgLayerNewTopLeft[indexFrom]
        self.imgLayerNewTopLeft.insert(indexTo, item)
        print('start reorder3')
        item = self.imgLayerNewBottomRight[indexFrom]
        del self.imgLayerNewBottomRight[indexFrom]
        self.imgLayerNewBottomRight.insert(indexTo, item)
        print('start reorder4')
        item = self.imgLayerAngle[indexFrom]
        del self.imgLayerAngle[indexFrom]
        self.imgLayerAngle.insert(indexTo, item)
        print('start reorder5')
        item = self.imgLayerNewAngle[indexFrom]
        del self.imgLayerNewAngle[indexFrom]
        self.imgLayerNewAngle.insert(indexTo, item)

        # self.imgLayerTopLeft.append(QPointF(0, 0))
        # self.imgLayerNewTopLeft.append(QPointF(0, 0))
        # 
        # self.imgLayerTopLeft.append(QPointF(0, 0))
        # self.imgLayerNewTopLeft.append(QPointF(0, 0))
        # 
        # self.imgLayerBottomRight.append(QPointF(qPixmap.width(), qPixmap.height()))
        # self.imgLayerNewBottomRight.append(QPointF(qPixmap.width(), qPixmap.height()))
        # 
        # self.imgLayerAngle.append(0.0)
        # self.imgLayerNewAngle.append(0.0)
        self.selectedImgIndex = indexTo
        self.update()

    def removeImg(self, index):
        print('index: {}'.format(index))
        if index > 0:
            # print('len(self.imgLayer): {}'.format(len(self.imgLayer)))
            # print(self.imgLayer)
            # print(self.imgLayer[index])
            del self.imgLayer[index]
            del self.imgLayerTopLeft[index]
            del self.imgLayerNewTopLeft[index]
            del self.imgLayerBottomRight[index]
            del self.imgLayerNewBottomRight[index]
            del self.imgLayerAngle[index]
            del self.imgLayerNewAngle[index]
            self.selectedImgIndex = -1
            self.drawRectmode = False
            self.update()