########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\plots\VoltagePlots.py
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

# python packages
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyqtgraph as pg
# custom packages
from plots import *

########################################################################################################################
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


########################################################################################################################
class VoltagePlots(QWidget):
    def __init__(self, parent=None, title=None, y_max=0):
        QWidget.__init__(self, parent=parent)

        self.y_plot = []
        self.y_value_label = {}

        self.setup_vi(title, y_max)

    # **************************************************************************************************************** #
    def setup_vi(self, title=None, y_max=0):
        """
        Create plots vi with label next to them to read current value
        """

        layout = QHBoxLayout(self)
        layout.setSpacing(3)

        graphics_layout = pg.GraphicsLayoutWidget(show=True)

        # ------------------------------------------------------------------------------------------------------------ #
        # voltage plot
        voltage_plot = graphics_layout.addPlot(title=title)
        voltage_plot.setLabel('bottom', 'Time', units='s')
        voltage_plot.setLabel('left', 'Voltage', units='V')
        voltage_plot.setYRange(0, y_max)

        # ------------------------------------------------------------------------------------------------------------ #
        # voltage labels
        labels_layout = QVBoxLayout(self)
        y_names = ["Target", "Monitor", "Difference"]
        y_color = [color[2], color[0], color[9]]
        y_name_label = {}

        for i, y_name in enumerate(y_names):

            y_name_label[i] = QLabel(y_name)
            y_name_label[i].setFixedWidth(60)
            y_name_label[i].setStyleSheet(f"background-color: rgb{y_color[i]}; color: white")

            self.y_value_label[i] = QLabel("0 V")
            self.y_value_label[i].setFixedWidth(60)

            if y_name != "Error":
                self.y_plot.append(voltage_plot.plot(pen=y_color[i], name=y_name))

            labels_layout.addWidget(y_name_label[i], 0, alignment=Qt.AlignmentFlag.AlignLeft)
            labels_layout.addWidget(self.y_value_label[i], 0, alignment=Qt.AlignmentFlag.AlignRight)

        labels_layout.addSpacerItem(QSpacerItem(10, 16))
        labels_layout.addStretch(1)

        # ------------------------------------------------------------------------------------------------------------ #
        layout.addWidget(graphics_layout)
        layout.addLayout(labels_layout)

    # **************************************************************************************************************** #
    def update_plot(self, t, y, labels):
        """
        Update plots and labels
        """
        for i, y_data in enumerate(y):
            self.y_plot[i].setData(t, y_data)  # plot
            self.y_value_label[i].setText(f"{labels[i]} V")

        self.y_value_label[2].setText(f"{labels[2]} V")
