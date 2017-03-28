#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import random
import PyQt5.QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QBasicTimer


from ocean import *


class OceanVisualizator(QWidget):
    def __init__(self, interval, ocean, window_height=1000, window_width=1000):
        super().__init__()
        self.ocean = ocean
        self.window_width = window_width
        self.window_height = window_height
        self.cell_width = self.window_width / self.ocean.width
        self.cell_heigth = self.window_height / self.ocean.height

        self.timer = QBasicTimer()
        self.init_ui()
        self.timer.start(interval * 1000, self)

    def init_ui(self):
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setWindowTitle("Ocean visualization")
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        for y in range(self.ocean.height):
            for x in range(self.ocean.width):
                if type(ocean.field[y][x]) != EmptyCell:
                    if type(ocean.field[y][x]) == Obstacle:
                        painter.fillRect(
                            x * self.cell_width, y * self.cell_heigth,
                            self.cell_width, self.cell_heigth,
                            PyQt5.QtCore.Qt.black
                        )
                    elif type(ocean.field[y][x]) == Victim:
                        painter.setBrush(PyQt5.QtCore.Qt.green)
                        painter.drawEllipse(
                            x * self.cell_width, y * self.cell_heigth,
                            self.cell_width, self.cell_heigth
                        )
                    elif type(ocean.field[y][x]) == Predator:
                        color = QColor(255, 0, 0)
                        live_rate = (
                            (ocean.field[y][x].full_health -
                                ocean.field[y][x].health) *
                            200 / ocean.field[y][x].full_health
                        )
                        painter.setBrush(QBrush(color.darker(100 + live_rate)))
                        painter.drawEllipse(
                            x * self.cell_width, y * self.cell_heigth,
                            self.cell_width, self.cell_heigth
                        )

        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.ocean.make_turn()
            self.update()

if __name__ == '__main__':
    application = QApplication(sys.argv)
    if len(sys.argv) == 1:
        ocean = Ocean(100, 100)
    else:
        ocean = Ocean(100, 100, map_file=sys.argv[1])
    visualizator = OceanVisualizator(0.2, ocean)
    sys.exit(application.exec_())
