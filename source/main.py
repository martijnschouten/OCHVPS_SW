########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       main.py
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

import os
import sys
#add path to source
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# custom packages
from ComSelect import *
from hxl_ps import *
from Userdef import *


class HaxelPowerSupplyInterface(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # open a dialog to ask port
        dialog = ComSelect("CP210")
        if not dialog.exec():
            print("[ERR] Canceled")
            sys.exit(0)

        self.debug_mode = dialog.get_debug_mode_results()
        display_cmd = dialog.get_rvc_data_results()
        # ************************************************************************************************************ #
        # RECORD DATA
        record_data = dialog.get_record_data_results()
        # ************************************************************************************************************ #
        # VOLTAGES PLOTS
        display_currents = dialog.get_currents_display_results()
        # ************************************************************************************************************ #
        # CURRENTS PLOTS
        display_voltages = dialog.get_voltages_display_results()
        # ************************************************************************************************************ #
        # Estimation of data rate transmission used for nice beginning of plot and not totally inaccurate time basis on
        # plots
        if display_currents == 0:
            self.time = 5    # 5
            self.estimateRate = 1
        if display_currents == 1:
            self.time = 5    # 5
            self.estimateRate = 0.01
        if display_currents == 2:
            self.time = 5
            self.estimateRate = 0.01
        if display_currents == 3:
            self.time = 1
            self.estimateRate = 0.005
        # ************************************************************************************************************ #
        self.number_board = dialog.get_number_boards_used()
        # ------------------------------------------------------------------------------------------------------------ #
        # BOARD #1
        board_1_port = dialog.get_board_1_port_results()
        self.board_1 = HaxelPowerSupply(port_name=board_1_port,
                                        estimate_rate=self.estimateRate,
                                        currents_display=display_currents,
                                        voltage_display=display_voltages,
                                        debug_mode=self.debug_mode,
                                        rcv_data=display_cmd,
                                        record_data=record_data)

        # ------------------------------------------------------------------------------------------------------------ #
        # BOARD #2
        board_2_port = None
        if self.number_board == 2:
            board_2_port = dialog.get_board_2_port_results()
            self.board_2 = HaxelPowerSupply(port_name=board_2_port,
                                            estimate_rate=self.estimateRate,
                                            currents_display=display_currents,
                                            voltage_display=display_voltages,
                                            debug_mode=self.debug_mode,
                                            rcv_data=display_cmd,
                                            record_data=record_data)

        # ************************************************************************************************************ #
        # DEBUG MODE
        if self.debug_mode == 1:
            print("[INFO] Selected Board {} (com port {})".format(self.board_1.board_name, board_1_port))
            if self.number_board == 2:
                print("[INFO] Selected Board {} (com port {})".format(self.board_2.board_name, board_2_port))

            print("[INFO] User selected display_voltage: {}".format(display_voltages))
            print("[INFO] User selected display_current: {}".format(display_currents))

            print("[INFO] User selected display: {}".format(display_cmd))
            print("[INFO] User selected Debug: {}".format(self.debug_mode))
            print("[INFO] User selected Record: {}".format(record_data))

        # ************************************************************************************************************ #
        # INITIALIZE PROGRAM
        # init user interface + callback for buttons...
        self.setWindowTitle("{} - {}" .format(PROGRAM_NAME, PROGRAM_VERSION))

        self.main_layout = QHBoxLayout(self)
        # ************************************************************************************************************ #
        # BOARD #1
        self.board_1_groupBox = QGroupBox("Board {}".format(self.board_1.board_name))
        self.board_1_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')

        self.main_layout.addWidget(self.board_1_groupBox, 0)

        self.board_1_groupBox_layout = QFormLayout(self)

        self.board_1_groupBox_layout.addRow(self.board_1)
        self.board_1_groupBox.setLayout(self.board_1_groupBox_layout)

        self.board_1.init_vi()

        if self.number_board == 1:
            if display_voltages == 0:
                self.setGeometry(0, 0, 10, 10)
            elif display_voltages == 1:
                self.setGeometry(0, 0, 1500, 500)
            else:
                self.setGeometry(0, 0, 1500, 500)
        # ************************************************************************************************************ #
        # BOARD #2
        elif self.number_board == 2:
            # -------------------------------------------------------------------------------------------------------- #
            # Board #2
            self.board_2_groupBox = QGroupBox("Board {}".format(self.board_2.board_name))
            self.board_2_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
            self.main_layout.addWidget(self.board_2_groupBox, 0)

            self.board_2_groupBox_layout = QFormLayout(self)
            self.board_2_groupBox_layout.addRow(self.board_2)
            self.board_2_groupBox.setLayout(self.board_2_groupBox_layout)

            self.board_2.init_vi()
            self.setGeometry(0, 0, 20, 20)

        self.main_layout.addStretch(1)

        # ************************************************************************************************************ #
        self.show()

        # set a timer with the callback function which reads data from serial port and plot
        # period is 30ms => 33Hz, if enough data sent by the board
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_reader_callback)
        self.timer.start(self.time)

    def data_reader_callback(self):
        self.board_1.data_reader_callback()
        if self.number_board == 2:
            self.board_2.data_reader_callback()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Window Close", "Are you sure you want to close the window?")

        if reply == QMessageBox.StandardButton.Yes:
            self.board_1.stop_comm()
            if self.number_board == 2:
                self.board_2.stop_comm()

            event.accept()
            if self.debug_mode == 1:
                print("[INFO] Program closed.")

        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(PROGRAM_NAME)

    window = HaxelPowerSupplyInterface()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
