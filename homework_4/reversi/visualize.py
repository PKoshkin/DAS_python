#!/usr/local/bin python3.6

import sys
import random
import PyQt5.QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QBasicTimer, QRect


from reversi import *


class ReversiVisualizator(QWidget):
    def __init__(self, window_height=800, window_width=800):
        super().__init__()
        self.field = Field()
        self.window_width = window_width
        self.window_height = window_height
        self.cell_width = self.window_width / len(self.field.matrix[0])
        self.cell_height = self.window_height / len(self.field.matrix)

        self.line_width = 4
        self.line_color = QColor(50, 50, 50)
        self.background_color = QColor(150, 150, 150)
        self.cell_padding = int(self.line_width / 2) + 5
        self.black_brush = Qt.black
        self.white_brush = Qt.white
        self.available_color = QColor(70, 120, 70)

        self.select_color()

        self.available_cells = self.field.get_available_strokes()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setWindowTitle("Reversi visualization")
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setBrush(QBrush(self.background_color))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRect(0, 0, self.window_width, self.window_height)

        painter.setBrush(self.available_color)
        painter.setPen(QPen(Qt.NoPen))
        for i, j in self.available_cells:
            painter.drawRect(
                i * self.cell_width, j * self.cell_height,
                self.cell_width, self.cell_height,
            )

        line_pen = QPen(self.line_color)
        line_pen.setWidth(self.line_width)
        painter.setPen(line_pen)
        for i in range(1, len(self.field.matrix)):
            painter.drawLine(
                0, i * self.cell_width,
                self.window_width, i * self.cell_width
            )
        for i in range(1, len(self.field.matrix[0])):
            painter.drawLine(
                i * self.cell_height, 0,
                i * self.cell_height, self.window_height
            )

        painter.setPen(QPen(Qt.NoPen))
        for i in range(len(self.field.matrix)):
            for j, color in enumerate(self.field.matrix[i]):
                if color == 1:
                    painter.setBrush(self.black_brush)
                    painter.drawEllipse(
                        i * self.cell_width + self.cell_padding,
                        j * self.cell_height + self.cell_padding,
                        self.cell_width - self.cell_padding * 2,
                        self.cell_height - self.cell_padding * 2,
                    )
                if color == 2:
                    painter.setBrush(self.white_brush)
                    painter.drawEllipse(
                        i * self.cell_width + self.cell_padding,
                        j * self.cell_height + self.cell_padding,
                        self.cell_width - self.cell_padding * 2,
                        self.cell_height - self.cell_padding * 2,
                    )
        painter.end()

    def get_cell(self, x, y):
        return (int(x / self.cell_width), int(y / self.cell_height))

    def select_color(self):
        reply = QMessageBox.question(
            self, 'Message',
            "Do you want to play black?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if reply == QMessageBox.No:
            self.field.make_random_turn()

    def finish(self):
        winner = self.field.get_winner()
        QMessageBox.information(
            self, 'Message',
            'Game finished. {} won!'.format(
                'Black' if winner == Field.BLACK else
                'White' if winner == Field.WHITE else
                'Friendsip'
            )
        )
        reply = QMessageBox.question(
            self, 'Message',
            "Do you want to play again?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if reply == QMessageBox.Yes:
            self.field = Field()
            self.select_color()
            self.available_cells = self.field.get_available_strokes()
            self.update()
        else:
            exit()

    def mousePressEvent(self, event):
        i, j = self.get_cell(event.localPos().x(), event.localPos().y())
        if (i, j) in self.available_cells:
            self.field.make_turn(i, j)
            while True:
                try:
                    self.field.make_smart_turn()
                    self.available_cells = self.field.get_available_strokes()
                    if len(self.available_cells) == 0:
                        self.field.skip_turn()
                        self.available_cells = self.field.get_available_strokes()
                        if len(self.available_cells) != 0:
                            QMessageBox.information(
                                self, 'Message',
                                'You have to skip turn.'
                            )
                            continue
                        else:
                            self.finish()
                            break
                    else:
                        self.available_cells = self.field.get_available_strokes()
                        self.update()
                        break
                except NoStrokeError:
                    self.field.skip_turn()
                    self.available_cells = self.field.get_available_strokes()
                    if len(self.available_cells) == 0:
                        self.finish()
                        break
                    else:
                        QMessageBox.information(
                            self, 'Message',
                            'You opponent have to skip turn.'
                        )
                        self.update()
                        break


if __name__ == '__main__':
    application = QApplication(sys.argv)
    visualizator = ReversiVisualizator()
    sys.exit(application.exec_())
