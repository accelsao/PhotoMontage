

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class LayerItem(QtWidgets.QGraphicsRectItem):
    DrawState, EraseState = range(2)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_state = LayerItem.DrawState
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        self.m_line_eraser = QtCore.QLineF()
        self.m_line_draw = QtCore.QLineF()
        self.m_pixmap = QtGui.QPixmap()

    def reset(self):
        r = self.parentItem().pixmap().rect()
        self.setRect(QtCore.QRectF(r))
        self.m_pixmap = QtGui.QPixmap(r.size())
        self.m_pixmap.fill(QtCore.Qt.transparent)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.save()
        painter.drawPixmap(QtCore.QPoint(), self.m_pixmap)
        painter.restore()

    def mousePressEvent(self, event):
        if self.current_state == LayerItem.EraseState:
            self._clear(event.pos().toPoint())
        elif self.current_state == LayerItem.DrawState:
            self.m_line_draw.setP1(event.pos())
            self.m_line_draw.setP2(event.pos())
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.current_state == LayerItem.EraseState:
            self._clear(event.pos().toPoint())
        elif self.current_state == LayerItem.DrawState:
            self.m_line_draw.setP2(event.pos())
            self._draw_line(
                self.m_line_draw, QtGui.QPen(self.pen_color, self.pen_thickness)
            )
            self.m_line_draw.setP1(event.pos())
        super().mouseMoveEvent(event)

    def _draw_line(self, line, pen):
        painter = QtGui.QPainter(self.m_pixmap)
        painter.setPen(pen)
        painter.drawLine(line)
        painter.end()
        self.update()

    def _clear(self, pos):
        painter = QtGui.QPainter(self.m_pixmap)
        r = QtCore.QRect(QtCore.QPoint(), 10 * QtCore.QSize())
        r.moveCenter(pos)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        painter.eraseRect(r)
        painter.end()
        self.update()

    @property
    def pen_thickness(self):
        return self._pen_thickness

    @pen_thickness.setter
    def pen_thickness(self, thickness):
        self._pen_thickness = thickness

    @property
    def pen_color(self):
        return self._pen_color

    @pen_color.setter
    def pen_color(self, color):
        self._pen_color = color

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, state):
        self._current_state = state


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.background_item = QtWidgets.QGraphicsPixmapItem()
        self.foreground_item = LayerItem(self.background_item)

        self.scene().addItem(self.background_item)

    def set_image(self, image):
        self.scene().setSceneRect(
            QtCore.QRectF(QtCore.QPointF(), QtCore.QSizeF(image.size()))
        )
        self.background_item.setPixmap(image)
        self.foreground_item.reset()
        self.fitInView(self.background_item, QtCore.Qt.KeepAspectRatio)
        self.centerOn(self.background_item)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        menu = self.menuBar().addMenu(self.tr("File"))
        open_action = menu.addAction(self.tr("Open image..."))
        open_action.triggered.connect(self.open_image)

        pen_group = QtWidgets.QGroupBox(self.tr("Pen settings"))
        eraser_group = QtWidgets.QGroupBox(self.tr("Eraser"))

        self.pen_button = QtWidgets.QPushButton(clicked=self.showColorDlg)
        color = QtGui.QColor(0, 0, 0)
        self.pen_button.setStyleSheet(
            "background-color: {}".format(color.name())
        )
        self.pen_slider = QtWidgets.QSlider(
            QtCore.Qt.Horizontal,
            minimum=3,
            maximum=21,
            value=5,
            focusPolicy=QtCore.Qt.StrongFocus,
            tickPosition=QtWidgets.QSlider.TicksBothSides,
            tickInterval=1,
            singleStep=1,
            valueChanged=self.onThicknessChanged,
        )

        self.eraser_checkbox = QtWidgets.QCheckBox(
            self.tr("Eraser"), stateChanged=self.onStateChanged
        )

        self.view = GraphicsView()
        self.view.foreground_item.pen_thickness = self.pen_slider.value()
        self.view.foreground_item.pen_color = color

        # layouts
        pen_lay = QtWidgets.QFormLayout(pen_group)
        pen_lay.addRow(self.tr("Pen color"), self.pen_button)
        pen_lay.addRow(self.tr("Pen thickness"), self.pen_slider)

        eraser_lay = QtWidgets.QVBoxLayout(eraser_group)
        eraser_lay.addWidget(self.eraser_checkbox)

        vlay = QtWidgets.QVBoxLayout()
        vlay.addWidget(pen_group)
        vlay.addWidget(eraser_group)
        vlay.addStretch()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        lay = QtWidgets.QHBoxLayout(central_widget)
        lay.addLayout(vlay, stretch=0)
        lay.addWidget(self.view, stretch=1)

        self.resize(640, 480)

    @QtCore.pyqtSlot(int)
    def onStateChanged(self, state):
        self.view.foreground_item.current_state = (
            LayerItem.EraseState
            if state == QtCore.Qt.Checked
            else LayerItem.DrawState
        )

    @QtCore.pyqtSlot(int)
    def onThicknessChanged(self, value):
        self.view.foreground_item.pen_thickness = value

    @QtCore.pyqtSlot()
    def showColorDlg(self):
        color = QtWidgets.QColorDialog.getColor(
            self.view.foreground_item.pen_color, self
        )
        self.view.foreground_item.pen_color = color
        self.pen_button.setStyleSheet(
            "background-color: {}".format(color.name())
        )

    def open_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open File",
            QtCore.QDir.currentPath(),
            filter="Images (*.png *.xpm *.jpg *jpeg)",
        )
        if filename:
            pixmap = QtGui.QPixmap(filename)
            if pixmap.isNull():
                QtWidgets.QMessageBox.information(
                    self, "Image Viewer", "Cannot load %s." % filename
                )
                return
            self.view.set_image(pixmap)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())