########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_plots\CurrentPlots.py
# @brief      Author:             MBE
#             Institute:          EPFL
#             Laboratory:         LMTS
#             Software version:   v1.08 (SYLVAIN/MARTIJN)
#             Created on:         08.11.2023
#             Last modifications: 08.11.2023
#
# Copyright 2021/2023 EPFL-LMTS
# All rights reserved.
# NO HELP WILL BE GIVEN IF YOU MODIFY THIS CODE !!!
########################################################################################################################

# python packages
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import pyqtgraph as pg
# custom packages
from hxl_ps_plots import *

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


class Current9Plots(QWidget):
    def __init__(self, parent=None, plot_tittle=None, y_name=None, y_min=0, y_max=0):
        QWidget.__init__(self, parent=parent)

        self.layout_plot = QHBoxLayout(self)
        self.layout_plot.setSpacing(3)

        self.graphics_layout = pg.GraphicsLayoutWidget(show=True)
        # ************************************************************************************************************ #
        # current plot
        self.current_plot = self.graphics_layout.addPlot(title=plot_tittle)
        self.current_plot.setLabel('bottom', 'Time', units='s')
        self.current_plot.setLabel('left', 'Current', units='uA')
        self.current_plot.setYRange(y_min, y_max)
        # ************************************************************************************************************ #
        # current labels
        self.current_labels_layout = QVBoxLayout(self)
        self.y_plot = []
        self.y_name_label = []
        self.y_value_label = []

        for i in range(9):
            self.y_plot.append(self.current_plot.plot(pen=color[i], name=y_name[i]))

            self.y_name_label.append(QLabel(y_name[i]))
            self.y_name_label[i].setStyleSheet("background-color: rgb{}; color: white; ".format(color[i]))
            self.y_name_label[i].setFixedWidth(60)

            self.y_value_label.append(QLabel("0 uA"))
            self.y_value_label[i].setFixedWidth(60)

            self.current_labels_layout.addWidget(self.y_name_label[i], 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.current_labels_layout.addWidget(self.y_value_label[i], 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.current_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.current_labels_layout.addStretch(1)

        self.layout_plot.addWidget(self.graphics_layout)
        self.layout_plot.addLayout(self.current_labels_layout)

    ####################################################################################################################
    def update_9_plot(self, t, y, labels):
        for i in range(9):
            self.y_plot[i].setData(t, y[i])  # plot
            self.y_value_label[i].setText("{} uA".format(labels[i], '10f'))


class Current8Plots(QWidget):
    def __init__(self, parent=None, plot_tittle=None, y_name=None, y_min=0, y_max=0):
        QWidget.__init__(self, parent=parent)

        self.layout_plot = QHBoxLayout(self)
        self.layout_plot.setSpacing(3)

        self.graphics_layout = pg.GraphicsLayoutWidget(show=True)
        # ************************************************************************************************************ #
        # current plot
        self.current_plot = self.graphics_layout.addPlot(title=plot_tittle)
        self.current_plot.setLabel('bottom', 'Time', units='s')
        self.current_plot.setLabel('left', 'Current', units='uA')
        self.current_plot.setYRange(y_min, y_max)
        # ************************************************************************************************************ #
        # current labels
        self.current_labels_layout = QVBoxLayout(self)
        self.y_plot = []
        self.y_name_label = []
        self.y_value_label = []

        for i in range(8):
            self.y_plot.append(self.current_plot.plot(pen=color[i+1], name=y_name[i+1]))

            self.y_name_label.append(QLabel(y_name[i+1]))
            self.y_name_label[i].setStyleSheet("background-color: rgb{}; color: white; ".format(color[i+1]))
            self.y_name_label[i].setFixedWidth(60)

            self.y_value_label.append(QLabel("0 uA"))
            self.y_value_label[i].setFixedWidth(60)

            self.current_labels_layout.addWidget(self.y_name_label[i], 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.current_labels_layout.addWidget(self.y_value_label[i], 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.current_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.current_labels_layout.addStretch(1)

        self.layout_plot.addWidget(self.graphics_layout)
        self.layout_plot.addLayout(self.current_labels_layout)

    ####################################################################################################################
    def update_8_plot(self, t, y, labels):
        for i in range(8):
            self.y_plot[i].setData(t, y[i+1])  # plot
            self.y_value_label[i].setText("{} uA".format(labels[i+1], '10f'))


########################################################################################################################
class Current2Plots(QWidget):
    def __init__(self, parent=None, plot_tittle=None, plot_name=None, plot_index=None, y_min=0, y_max=0):
        QWidget.__init__(self, parent=parent)

        self.layout_plot = QHBoxLayout(self)
        self.layout_plot.setSpacing(3)

        self.graphics_layout = pg.GraphicsLayoutWidget(show=True)
        # ************************************************************************************************************ #
        # current plot
        self.current_plot = self.graphics_layout.addPlot(title=plot_tittle)
        self.current_plot.setLabel('bottom', 'Time', units='s')
        self.current_plot.setLabel('left', 'Current', units='uA')
        self.current_plot.setYRange(y_min, y_max)
        # ************************************************************************************************************ #
        # current labels
        self.current_labels_layout = QVBoxLayout(self)
        self.y_plot = []
        self.y_name_label = []
        self.y_value_label = []

        for i in range(2):
            color_index = (2*plot_index) - (1-i)
            self.y_plot.append(self.current_plot.plot(pen=color[color_index], name=plot_name[i]))

            self.y_name_label.append(QLabel(plot_name[i]))
            self.y_name_label[i].setStyleSheet("background-color: rgb{}; color: white; ".format(color[color_index]))
            self.y_name_label[i].setFixedWidth(60)

            self.y_value_label.append(QLabel("0 uA"))
            self.y_value_label[i].setFixedWidth(60)

            self.current_labels_layout.addWidget(self.y_name_label[i], 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.current_labels_layout.addWidget(self.y_value_label[i], 0, alignment=Qt.AlignmentFlag.AlignRight)
        # ------------------------------------------------------------------------------------------------------------ #
        self.current_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.current_labels_layout.addStretch(1)
        # ------------------------------------------------------------------------------------------------------------ #
        self.layout_plot.addWidget(self.graphics_layout)
        self.layout_plot.addLayout(self.current_labels_layout)

    ####################################################################################################################
    def update_2_plot(self, t, y, label):
        for i in range(2):
            self.y_plot[i].setData(t, y[i])
            self.y_value_label[i].setText("{} uA".format(label[i], '10f'))


########################################################################################################################
class Current1Plots(QWidget):
    def __init__(self, parent=None, plot_tittle=None, plot_name=None, plot_index=None, y_min=0, y_max=0):
        QWidget.__init__(self, parent=parent)

        self.layout_plot = QHBoxLayout(self)
        self.layout_plot.setSpacing(3)

        self.graphics_layout = pg.GraphicsLayoutWidget(show=True)
        # ************************************************************************************************************ #
        # current plot
        self.current_plot = self.graphics_layout.addPlot(title=plot_tittle)
        self.current_plot.setLabel('bottom', 'Time', units='s')
        self.current_plot.setLabel('left', 'Current', units='uA')
        self.current_plot.setYRange(y_min, y_max)

        self.y_plot = self.current_plot.plot(pen=color[plot_index], name=plot_name)
        # ************************************************************************************************************ #
        # current labels
        self.y_name_label = QLabel(plot_name)
        self.y_name_label.setStyleSheet("background-color: rgb{}; color: white; ".format(color[plot_index]))
        self.y_name_label.setFixedWidth(60)

        self.y_value_label = QLabel("0 uA")
        self.y_value_label.setFixedWidth(60)
        # ------------------------------------------------------------------------------------------------------------ #
        self.current_labels_layout = QVBoxLayout(self)
        self.current_labels_layout.addWidget(self.y_name_label, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.current_labels_layout.addWidget(self.y_value_label, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.current_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.current_labels_layout.addStretch(1)
        # ------------------------------------------------------------------------------------------------------------ #
        self.layout_plot.addWidget(self.graphics_layout)
        self.layout_plot.addLayout(self.current_labels_layout)

    ####################################################################################################################
    def update_1_plot(self, t, y, label):
        self.y_plot.setData(t, y)
        self.y_value_label.setText("{} uA".format(label, '9f'))
