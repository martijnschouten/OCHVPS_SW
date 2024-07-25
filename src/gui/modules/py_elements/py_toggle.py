########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\py_elements\py_toggle.py
# @brief      Author:             MBE
#             Software version:   v1.09
#             Created on:         12.02.2024
#             Last modifications: 18.03.2024
#
# HXL_PS © 2021-2024 by MBE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.
#
# NO HELP WILL BE GIVEN IF YOU MODIFY THIS CODE !!!
########################################################################################################################

# https://www.youtube.com/watch?v=NnJFi285s3M

# python packages
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


########################################################################################################################
class PyToggle(QCheckBox):
    def __init__(
            self,
            width=60,
            bg_color="#F00",
            bg_text="FO0",
            circle_color="#DDD",
            active_color="#3aba00",
            active_text="ON",
            animation_curve=QEasingCurve.Type.OutBounce
    ):
        QCheckBox.__init__(self)

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._bg_text = bg_text
        self._circle_color = circle_color
        self._active_color = active_color
        self._active_text = active_text

        # CREATE ANIMATION
        self._circle_position = self.width() - 26
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(250)  # Time in milliseconds

        # CONNECT STAT CHANGED
        self.stateChanged.connect(self.start_transition)

    # **************************************************************************************************************** #
    # CREATE NEW SET AND GET PROPERTY
    @pyqtProperty(int)  # Get
    def circle_position(self):
        return self._circle_position

    # **************************************************************************************************************** #
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    # **************************************************************************************************************** #
    def start_transition(self, value):
        self.animation.stop()  # Stop animation if running
        if value:
            self.animation.setEndValue(3)
        else:
            self.animation.setEndValue(self.width() - 26)

        # START ANIMATION
        self.animation.start()

        # print(f"Status: {self.isChecked()}")

    # **************************************************************************************************************** #
    # SET NEW HIT AREA
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    # **************************************************************************************************************** #
    # DRAW NEW ITEMS
    def paintEvent(self, e):
        # SET PAINTER
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # SET AS NO PEN
        p.setPen(Qt.PenStyle.NoPen)

        # DRAW RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())

        # CHECK IF IS CHECKED
        # if self.isChecked():
        if self._circle_position < 10:
            # DRAW BACKGROUND
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # DRAW CIRCLE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)
        else:
            # DRAW BACKGROUND
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # DRAW CIRCLE
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 22, 22)

        # END DRAW
        p.end()
