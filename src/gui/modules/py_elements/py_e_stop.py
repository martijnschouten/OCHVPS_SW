########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\py_elements\py_e_stop.py
# @brief      Author:             MBE
#             Software version:   v1.09
#             Created on:         28.02.2024
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

# python packages
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


########################################################################################################################
class PyEmergencyStop(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(100, 100)

    # **************************************************************************************************************** #
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Outer yellow circle
        outer_circle_color = QColor("#FFFF00")  # Yellow
        painter.setBrush(outer_circle_color)
        painter.drawEllipse(0, 0, 100, 100)

        # Inner red circle
        inner_circle_color = QColor("#FF0000")  # Red
        painter.setBrush(inner_circle_color)
        painter.drawEllipse(10, 10, 80, 80)

        # Text
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        text_rect = painter.fontMetrics().boundingRect(self.text())
        text_position = QPoint(int(50 - text_rect.width() / 2), int(50 + text_rect.height() / 2))
        painter.drawText(text_position, self.text())
