########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       options\RecordData.py
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
from datetime import *
from pathlib import *
from PyQt6.QtWidgets import *
from Userdef import *


class RecordData(QWidget):
    def __init__(self, parent=None, board_name=None, board_version=None, port_name=None, sequential=None):

        QWidget.__init__(self, parent=parent)

        folder = Path("logs")
        folder.mkdir(parents=True, exist_ok=True)

        if sequential == 1:
            print("[INFO] Recording sequential data.")
            self.filename = folder.joinpath("HXL_PS_v1.0_log_seq_{}.csv"
                                            .format(datetime.now().strftime("%Y%m%d-%Hh%M.%S")))
        else:
            print("[INFO] Recording data.")
            self.filename = folder.joinpath("HXL_PS_v1.0_log_{}.csv"
                                            .format(datetime.now().strftime("%Y%m%d-%Hh%M.%S")))

        self.file = open(self.filename, 'w')
        self.file.write("Data recorded by HXL PS GUI beta version\r\n")
        self.file.write("Date, {}\r\n".format(datetime.now().strftime("%Y %m %d - %H:%M:%S")))
        self.file.write(",Name,Version\n")
        self.file.write("Interface,{},{}\n".format(PROGRAM_NAME, PROGRAM_VERSION))
        self.file.write("Board,{},{}\n".format(board_name, board_version))
        self.file.write("Port,{}\r\n".format(port_name))
        self.file.write("time, [dbg], timestamp[ms], HV target [V], LV target [V], LV VM [V], HV VM [V], HV_CM [uA], "
                        "HB_CM_CH1 [uA], HB_CM_CH2 [uA], HB_CM_CH3 [uA], HB_CM_CH4 [uA], "
                        "HB_CM_CH5 [uA], HB_CM_CH6 [uA], HB_CM_CH7 [uA], HB_CM_CH8 [uA]\r\n")

        self.data_save_label = QLabel("Saving file to: {}".format(self.filename.as_posix()))
        data_save_layout = QVBoxLayout()
        data_save_layout.addWidget(self.data_save_label)

    def save_data(self, line):
        self.file.write("{},".format(datetime.now().strftime("%H:%M:%S:%f")))
        self.file.write(line)

    def close_record(self, sequential=None):
        self.file.close()
        if sequential == 0:
            QMessageBox.information(self, '', "Data saved to: {}".format(self.filename))
            print("[INFO] Date/time when closing: {}"
                  .format(datetime.now().strftime("%Y %m %d - %H:%M:%S")))
            print("[INFO] Data saved to: {}".format(self.filename))
        else:
            print("[INFO] Sequential data saved to: {}".format(self.filename))
