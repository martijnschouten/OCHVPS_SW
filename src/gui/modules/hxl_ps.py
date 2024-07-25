########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\hxl_ps.py
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
import numpy as np
# custom packages
from src.cmd.modules.BoardCom import BoardCom
from src.cmd.modules.options import RecData

from src.gui.modules.modes import *
from src.gui.modules.options import RecSeqDataWidget
from src.gui.modules.plots import *
from src.gui.modules.voltage import *

NB_FULL_BRIDGES = 4
NB_HALF_BRIDGES = 8


########################################################################################################################
class HaxelPowerSupply(QWidget):
    def __init__(self, settings=None, estimate_rate=None):

        QWidget.__init__(self)

        self.settings = settings
        self.estimateRate = estimate_rate
        self.data = []

        # ------------------------------------------------------------------------------------------------------------ #
        # SERIAL COMMUNICATION
        self.com = BoardCom(settings=self.settings)
        # open serial port
        if self.com.connect():
            self.board_connected = True
        # read PCB parameters
        self.pcb_prm = self.com.get_parameters()

        # ------------------------------------------------------------------------------------------------------------ #
        # MODULES

        if "MF" not in self.pcb_prm['fw_ver']:
            self.Mode1 = Mode1Widget(nb_hb=NB_HALF_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)
            self.Mode2 = Mode2Widget(nb_fb=NB_FULL_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)
            self.Mode3 = Mode3Widget(nb_hb=NB_HALF_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)
            self.Mode4 = Mode4Widget(nb_fb=NB_FULL_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)

        self.Voltage = VoltageWidget(com=self.com, pcb_prm=self.pcb_prm)

        # ------------------------------------------------------------------------------------------------------------ #
        # init file to record data
        if self.settings['record']:
            self.rec_data = RecData(pcb_prm=self.pcb_prm, settings=self.settings, seq=False)
            self.rec_seq_data = RecSeqDataWidget(pcb_prm=self.pcb_prm, settings=self.settings)

        # ------------------------------------------------------------------------------------------------------------ #
        # High Voltage monitor
        self.hv_vm = np.zeros(200, dtype=float)
        self.hv_vm_now = []

        # ------------------------------------------------------------------------------------------------------------ #
        # FOR ANY PLOT (CURRENT OR VOLTAGE)
        if (self.settings['current'] != 0) or (self.settings['voltage'] != 0):
            # init data arrays + time basis,...
            self.tplot = np.arange(-100*self.estimateRate, 100*self.estimateRate, self.estimateRate, dtype=float)
            self.t_save = np.zeros(500, dtype=int)

        # ------------------------------------------------------------------------------------------------------------ #
        # VOLTAGE PLOTS

        if self.settings['voltage'] != 0:
            # High Voltage plot
            self.hv_plots = VoltagePlots(title="High Voltage Monitor", y_max=self.pcb_prm['max_hv'] + 1500)
            # High Voltage set by user
            self.hv_set = np.zeros(200, dtype=float)
            self.hv_set_now = []
            # High Voltage error
            self.hv_diff = np.zeros(200, dtype=float)
            self.hv_diff_now = []

        if self.settings['voltage'] == 2:
            # Low Voltage plot
            self.lv_plots = VoltagePlots(title="Low Voltage Monitor", y_max=15)
            # Low Voltage set by user
            self.lv_set = np.zeros(200, dtype=float)
            self.lv_set_now = []
            # Low Voltage monitor
            self.lv_vm = np.zeros(200, dtype=float)
            self.lv_vm_now = []
            # High Voltage error
            self.lv_diff = np.zeros(200, dtype=float)
            self.lv_diff_now = []

        # ------------------------------------------------------------------------------------------------------------ #
        # CURRENTS PLOTS

        if self.settings['current'] != 0:
            self.fb_cm_plots = []
            self.hb_cm_plots = []
            self.cm_val = np.zeros([9, 200], dtype=int)
            self.cm_val_now = ["", "", "", "", "", "", "", "", ""]
            self.y_name = ["HV CM"]
            for i in range(1, NB_HALF_BRIDGES + 1):
                self.y_name.append(f"CH{i} CM")

        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['current'] == 1:
            self.all_cm_plots = CurrentPlots(title="All Currents Monitor", y_names=self.y_name, index=0, y_max=2000)

        elif self.settings['current'] == 2:
            for FullBridge in range(NB_FULL_BRIDGES):
                y1_index = (2 * FullBridge) + 1
                y2_index = 2 * (FullBridge + 1)
                y_name_2 = [self.y_name[y1_index], self.y_name[y2_index]]
                self.fb_cm_plots.append(CurrentPlots(title=f"FB{FullBridge + 1} Current Monitor",
                                                     y_names=y_name_2, index=FullBridge + 1, y_max=2000))

        elif self.settings['current'] == 3:
            for HalfBridge in range(NB_HALF_BRIDGES):
                y_name_2 = [self.y_name[HalfBridge + 1]]
                self.hb_cm_plots.append(CurrentPlots(title=f"CH{HalfBridge + 1} Current Monitor",
                                                     y_names=y_name_2, index=HalfBridge + 1, y_max=2000))

    # **************************************************************************************************************** #
    def init_vi(self):
        """
        INITIALIZE HXL PS VI
        """
        layout_main = QVBoxLayout()
        layout_main.setSpacing(3)
        self.setLayout(layout_main)

        # ------------------------------------------------------------------------------------------------------------ #
        layout_top = QHBoxLayout()
        layout_top.setSpacing(3)
        self.setLayout(layout_top)

        # ------------------------------------------------------------------------------------------------------------ #
        layout_bottom = QVBoxLayout()
        layout_bottom.setSpacing(3)
        self.setLayout(layout_bottom)

        # ------------------------------------------------------------------------------------------------------------ #
        layout_bottom1 = QHBoxLayout()
        layout_bottom1.setSpacing(3)
        self.setLayout(layout_bottom1)

        # ------------------------------------------------------------------------------------------------------------ #
        layout_bottom2 = QHBoxLayout()
        layout_bottom2.setSpacing(3)
        self.setLayout(layout_bottom2)

        # ------------------------------------------------------------------------------------------------------------ #
        # Plots on the left
        layout_left = QVBoxLayout()

        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['current'] != 0 or self.settings['voltage'] != 0:
            layout_top.addLayout(layout_left)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['voltage'] != 0:
            layout_left.addWidget(self.hv_plots)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['voltage'] == 2:
            layout_left.addWidget(self.lv_plots)

        # ------------------------------------------------------------------------------------------------------------ #
        # add top layout to main layout
        layout_main.addLayout(layout_top)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['current'] == 1:
            layout_left.addWidget(self.all_cm_plots)
        elif self.settings['current'] == 2:
            # layout_left.addWidget(self.ps_hv_cm_plots)
            # -------------------------------------------------------------------------------------------------------- #
            for plots_row in range(4):
                layout_bottom1.addWidget(self.fb_cm_plots[plots_row])
            # -------------------------------------------------------------------------------------------------------- #
            layout_main.addLayout(layout_bottom1)
        elif self.settings['current'] == 3:
            # layout_left.addWidget(self.ps_hv_cm_plots)
            # -------------------------------------------------------------------------------------------------------- #
            for plots_row in range(4):
                layout_bottom1.addWidget(self.hb_cm_plots[plots_row])
                layout_bottom2.addWidget(self.hb_cm_plots[plots_row + 4])
            # -------------------------------------------------------------------------------------------------------- #
            layout_bottom.addLayout(layout_bottom1)
            layout_bottom.addLayout(layout_bottom2)
            # -------------------------------------------------------------------------------------------------------- #
            layout_main.addLayout(layout_bottom)

        # ------------------------------------------------------------------------------------------------------------ #
        # Rest on the right
        layout_right = QVBoxLayout()
        layout_right.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_right.setSpacing(0)
        layout_top.addLayout(layout_right)
        # ------------------------------------------------------------------------------------------------------------ #
        layout_right.addWidget(self.Voltage)
        # ------------------------------------------------------------------------------------------------------------ #

        tab = QTabWidget(self)
        tab.setFixedWidth(700)

        modes = [(self.Mode1, 'Mode 1'), (self.Mode2, 'Mode 2'), (self.Mode3, 'Mode 3'), (self.Mode4, 'Mode 4')]

        for mode, name in modes:
            mode.setup_vi()
            tab.addTab(mode, name)

        layout_right.addWidget(tab)

        # ------------------------------------------------------------------------------------------------------------ #
        # Data save info
        if self.settings['record']:
            layout_right.addWidget(self.rec_seq_data)

        # ------------------------------------------------------------------------------------------------------------ #
        # Layout of all widgets not plot
        layout_left.addStretch(1)
        layout_right.addStretch(1)
        layout_main.addStretch(1)

    # **************************************************************************************************************** #
    def data_reader_callback(self):
        """
        Call monitoring function and update plots/labels.
        """
        if self.board_connected:
            # shift data in the array one sample left
            self.shift_data()

            if self.read_monitoring():
                self.update_data()
                self.Voltage.update_label(self.hv_vm[-1])
                self.update_plots()
        else:
            return

    # **************************************************************************************************************** #
    def read_monitoring(self):
        """
        Read monitoring for each board
        # handle data
        # Remove units, spaces, split with coma
        # Refer to documentation of HVPS to assign data to fields
        """

        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = f"Moni 1\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()

            if line.startswith("[moni]"):
                break

        # ------------------------------------------------------------------------------------------------------------ #
        # handle data
        # Remove units, spaces, split with coma. Refer to documentation of HVPS to assign data to fields
        try:
            data_buf = (line.replace(" ", "").replace("uA", "").replace("V", "").replace("Hz", "").replace("\r\n", "")
                        .split(","))
            self.data = [float(x) for x in data_buf[2:15]]
        except Exception as conv_data_err:
            print(f"[ERR] Convert. data: {line} - {conv_data_err}")
            return False

        # save data to file
        if self.settings['record']:
            self.rec_data.save_data(line)
            self.rec_seq_data.is_seq_recording_now(line)

        # flush input if too much data not handled: avoid keeping very old values
        if self.com.ser.in_waiting > 200:
            # print(self.ser.in_waiting)
            self.com.ser.reset_input_buffer()

        return True

    # **************************************************************************************************************** #
    def shift_data(self):
        """
        Shift data lists to prepare for reception of new values
        """
        # shift data in the array one sample left
        self.hv_vm[:-1] = self.hv_vm[1:]
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['voltage'] != 0 or self.settings['current'] != 0:
            # shift time base
            self.tplot[:-1] = self.tplot[1:]
            self.tplot[-1] = self.tplot[-2] + self.estimateRate
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['voltage'] != 0:
            self.hv_set[:-1] = self.hv_set[1:]
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['voltage'] == 2:
            self.lv_set[:-1] = self.lv_set[1:]
            self.lv_vm[:-1] = self.lv_vm[1:]
        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['current'] != 0:
            for HalfBridge in range(0, NB_HALF_BRIDGES + 1):
                self.cm_val[HalfBridge, :-1] = self.cm_val[HalfBridge, 1:]

    # **************************************************************************************************************** #
    def update_data(self):
        """
        Update data lists depending on received data
        """
        # -------------------------------------------------------------------------------------------------------- #
        self.hv_vm[-1] = self.data[3] if self.data[3] > 5 else 0
        self.hv_vm_now = format(float(self.data[3] if self.data[3] > 5 else 0), '4.0f')
        # -------------------------------------------------------------------------------------------------------- #
        if self.settings['voltage'] != 0:
            self.hv_set[-1] = self.data[0]
            self.hv_set_now = format(float(self.data[0]), '4.0f')

            self.hv_diff[-1] = self.data[0] - self.data[3] if self.data[3] > 5 else 0
            self.hv_diff_now = format((self.data[0] - self.data[3]) if self.data[3] > 5 else 0, '4.0f')
        # -------------------------------------------------------------------------------------------------------- #
        if self.settings['voltage'] == 2:
            self.lv_set[-1] = self.data[1]
            self.lv_set_now = format(float(self.data[1]), '2.1f')

            self.lv_vm[-1] = self.data[2]
            self.lv_vm_now = format(float(self.data[2]), '2.1f')

            self.lv_diff[-1] = self.data[1] - self.data[2]
            self.lv_diff_now = format((self.data[1] - self.data[2]), '2.1f')
        # -------------------------------------------------------------------------------------------------------- #
        if self.settings['current'] != 0:
            for HalfBridge in range(NB_HALF_BRIDGES + 1):
                self.cm_val[HalfBridge, -1] = int(self.data[HalfBridge + 4])
                self.cm_val_now[HalfBridge] = format(int(self.data[HalfBridge + 4]))
        return True

    # **************************************************************************************************************** #
    def update_plots(self):
        """
        Update plots and labels with new received data
        """
        # ------------------------------------------------------------------------------------------------------------ #
        # update voltage plots
        if self.settings['voltage'] != 0:
            y_plots = [self.hv_set, self.hv_vm]
            y_value_label = [self.hv_set_now, self.hv_vm_now, self.hv_diff_now]
            self.hv_plots.update_plot(t=self.tplot, y=y_plots, labels=y_value_label)

        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['voltage'] == 2:
            y_plots = [self.lv_set, self.lv_vm]
            y_value_label = [self.lv_set_now, self.lv_vm_now, self.lv_diff_now]
            self.lv_plots.update_plot(t=self.tplot, y=y_plots, labels=y_value_label)

        # ------------------------------------------------------------------------------------------------------------ #
        # update current plots
        if self.settings['current'] == 1:
            self.all_cm_plots.update_plot(t=self.tplot, y=self.cm_val, labels=self.cm_val_now)
        elif self.settings['current'] == 2:
            for FullBridge in range(NB_FULL_BRIDGES):
                y1_index = (2 * FullBridge) + 1
                y2_index = 2 * (FullBridge + 1)
                y_val = [self.cm_val[y1_index], self.cm_val[y2_index]]
                y_val_label = [self.cm_val_now[y1_index], self.cm_val_now[y2_index]]
                self.fb_cm_plots[FullBridge].update_plot(t=self.tplot, y=y_val, labels=y_val_label)
        elif self.settings['current'] == 3:
            for HalfBridges in range(NB_HALF_BRIDGES):
                self.hb_cm_plots[HalfBridges].update_plot(t=self.tplot,
                                                          y=self.cm_val[HalfBridges + 1],
                                                          labels=self.cm_val_now[HalfBridges + 1])

    # **************************************************************************************************************** #
    # RECONNECTION WITH BOARD
    def stop_comm(self):
        """
        Disable HV and monitoring and stop record
        """
        if self.com.disconnect():
            self.board_connected = False

        if self.settings['record']:
            self.settings['record'] = 0
            filename, datetime = self.rec_data.close_record()

            QMessageBox.information(self, '', f"Data saved to: {filename}")
