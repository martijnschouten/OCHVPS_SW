########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_plots\VoltagePlots.py
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


class VoltagePlots(QWidget):
    def __init__(self, parent=None, plot_tittle=None, y_min=0, y_max=0):
        QWidget.__init__(self, parent=parent)

        self.layout_plot = QHBoxLayout(self)
        self.layout_plot.setSpacing(3)

        self.graphics_layout = pg.GraphicsLayoutWidget(show=True)
        # ************************************************************************************************************ #
        # voltage plot
        self.voltage_plot = self.graphics_layout.addPlot(title=plot_tittle)
        self.voltage_plot.setLabel('bottom', 'Time', units='s')
        self.voltage_plot.setLabel('left', 'Voltage', units='V')
        self.voltage_plot.setYRange(y_min, y_max)
        # ------------------------------------------------------------------------------------------------------------ #
        # V_set // V_vm
        self.v_set_plot = self.voltage_plot.plot(pen=color[2], name="Target voltage")
        self.v_now_plot = self.voltage_plot.plot(pen=color[0], name="Output voltage")
        # ************************************************************************************************************ #
        # voltage labels
        # ------------------------------------------------------------------------------------------------------------ #
        # Vhv_set
        self.hv_set_name_label = QLabel("Target")
        self.hv_set_name_label.setStyleSheet("background-color: rgb{}; color: white" .format(color[2]))
        self.hv_set_name_label.setFixedWidth(60)

        self.hv_set_value_label = QLabel("0 V")
        self.hv_set_value_label.setFixedWidth(60)
        # ------------------------------------------------------------------------------------------------------------ #
        # Vhv_vm
        self.hv_vm_name_label = QLabel("Monitor")
        self.hv_vm_name_label.setStyleSheet("background-color: rgb{}; color: white" .format(color[0]))
        self.hv_vm_name_label.setFixedWidth(60)

        self.hv_vm_value_label = QLabel("0 V")
        self.hv_vm_value_label.setFixedWidth(60)
        # ------------------------------------------------------------------------------------------------------------ #
        # Vhv_err
        self.hv_err_name_label = QLabel("Error")
        self.hv_err_name_label.setStyleSheet("background-color: rgb{}; color: white" .format(color[9]))
        self.hv_err_name_label.setFixedWidth(60)

        self.hv_err_value_label = QLabel("0 V")
        self.hv_vm_value_label.setFixedWidth(60)
        # ------------------------------------------------------------------------------------------------------------ #
        self.voltage_labels_layout = QVBoxLayout(self)
        self.voltage_labels_layout.addWidget(self.hv_set_name_label, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.voltage_labels_layout.addWidget(self.hv_set_value_label, 0, alignment=Qt.AlignmentFlag.AlignRight)
        # self.voltage_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.voltage_labels_layout.addWidget(self.hv_vm_name_label, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.voltage_labels_layout.addWidget(self.hv_vm_value_label, 0, alignment=Qt.AlignmentFlag.AlignRight)
        # self.voltage_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.voltage_labels_layout.addWidget(self.hv_err_name_label, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.voltage_labels_layout.addWidget(self.hv_err_value_label, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.voltage_labels_layout.addSpacerItem(QSpacerItem(10, 16))
        self.voltage_labels_layout.addStretch(1)
        # ------------------------------------------------------------------------------------------------------------ #
        self.layout_plot.addWidget(self.graphics_layout)
        self.layout_plot.addLayout(self.voltage_labels_layout)

    ####################################################################################################################
    def update_plot(self, t, y1, y2):
        self.v_set_plot.setData(t, y1)  # plot
        self.v_now_plot.setData(t, y2)

    ####################################################################################################################
    def update_label(self, label1, label2, label3):
        self.hv_set_value_label.setText("{} V".format(label1, '4.2f'))
        self.hv_vm_value_label.setText("{} V".format(label2, '4.2f'))
        self.hv_err_value_label.setText("{} V".format(label3, '4.2f'))
