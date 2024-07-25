########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\hxl_ps_widget.py
# @brief      Author:             MBE
#             Software version:   v1.09
#             Created on:         12.02.2024
#             Last modifications: 18.03.2024
#
# OC_HVPS © 2021-2024 by MBE
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
import sys
# custom packages
from src.gui.modules.ComSelect import ComSelect
from src.gui.modules.hxl_ps import HaxelPowerSupply


########################################################################################################################
class HaxelPowerSupplyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # ------------------------------------------------------------------------------------------------------------ #
        # open a dialog to ask port
        dialog = ComSelect("CP210")
        if not dialog.exec():
            print("[ERR] Canceled")
            sys.exit(0)

        # ------------------------------------------------------------------------------------------------------------ #
        # GET SETTINGS
        self.settings = dialog.get_settings()

        # ------------------------------------------------------------------------------------------------------------ #
        # Estimation of data rate transmission used for nice beginning of plot and not totally inaccurate time basis on
        # plots
        time_map = {0: 50, 1: 50, 2: 50, 3: 50}
        estimate_rate_map = {0: 0.05, 1: 0.05, 2: 0.05, 3: 0.05}

        current_setting = self.settings['current']
        self.time = time_map.get(current_setting, 5)
        self.estimateRate = estimate_rate_map.get(current_setting, 1)

        # ------------------------------------------------------------------------------------------------------------ #
        # Creation of HaxelPowerSupply depending on the number of boards selected by user
        self.boards = {}
        for x in range(self.settings['nb_board']):
            self.settings['id_board'] = x+1
            self.boards[x] = HaxelPowerSupply(settings=self.settings, estimate_rate=self.estimateRate)

        # ------------------------------------------------------------------------------------------------------------ #
        # Display settings selected by user
        if self.settings['debug']:
            for x in range(self.settings['nb_board']):
                com_port = self.settings['port_#01'] if x == 0 else self.settings['port_#02']
                print(f"[INFO] Selected Board {self.boards[x].pcb_prm['name']} (com port {com_port})")

            print(f"[INFO] User selected display_voltage: {self.settings['voltage']}")
            print(f"[INFO] User selected display_current: {self.settings['current']}")

            print(f"[INFO] User selected Debug: {self.settings['debug']}")
            print(f"[INFO] User selected Record: {self.settings['record']}")

        # ------------------------------------------------------------------------------------------------------------ #
        self.setup_vi()

        # ------------------------------------------------------------------------------------------------------------ #
        # set a timer with the callback function which reads data from serial port and plot
        # period is 50ms => 20Hz, if enough data sent by the board
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_reader_callback)
        self.timer.start(self.time)

    # **************************************************************************************************************** #
    def setup_vi(self):
        """
        Create a main layout and add on or two boards instances depending on number selected by user
        """
        main_layout = QHBoxLayout(self)

        # ------------------------------------------------------------------------------------------------------------ #
        for x in range(self.settings['nb_board']):
            board_groupbox = QGroupBox(f"Board {self.boards[x].pcb_prm['name']}")
            board_groupbox.setStyleSheet('QGroupBox {font-weight: bold;}')

            main_layout.addWidget(board_groupbox, 0)

            board_groupbox_layout = QFormLayout(self)
            board_groupbox_layout.addRow(self.boards[x])
            board_groupbox.setLayout(board_groupbox_layout)

            self.boards[x].init_vi()

        # ------------------------------------------------------------------------------------------------------------ #
        if self.settings['nb_board'] == 1:
            if self.settings['voltage'] == 0:
                self.setGeometry(0, 0, 10, 10)
            elif self.settings['voltage'] == 1:
                self.setGeometry(0, 0, 1500, 500)
            else:
                self.setGeometry(0, 0, 1500, 500)
        else:
            self.setGeometry(0, 0, 20, 20)

        # ------------------------------------------------------------------------------------------------------------ #
        main_layout.addStretch(1)

    # **************************************************************************************************************** #
    def data_reader_callback(self):
        """
        Read monitoring for each board
        # handle data
        # Remove units, spaces, split with coma
        # Refer to documentation of HVPS to assign data to fields
        """
        for x in range(self.settings['nb_board']):
            self.boards[x].data_reader_callback()

    # **************************************************************************************************************** #
    def stop_com(self):
        """
        Stop communication with all boards
        """
        for x in range(self.settings['nb_board']):
            self.boards[x].stop_comm()

        print("[INFO] Program closed.")
