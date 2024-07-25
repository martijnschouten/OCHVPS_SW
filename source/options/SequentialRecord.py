########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       SequentialRecord.py
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
from options import *


class SequentialRecord(QWidget):
    def __init__(self, parent=None, board_name=None, board_version=None, port_name=None):

        QWidget.__init__(self, parent=parent)

        self.board_name = board_name
        self.board_version = board_version
        self.port_name = port_name
        self.RecordData = None

        # ************************************************************************************************************ #
        self.record_groupBox = QGroupBox("Record")
        self.record_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.record_groupBox.setFixedWidth(400)
        # ------------------------------------------------------------------------------------------------------------ #
        self.record_layout = QVBoxLayout(self)
        self.record_layout.addWidget(self.record_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.record_groupBox_layout = QVBoxLayout(self.record_groupBox)
        self.record_groupBox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.record_groupBox.setLayout(self.record_groupBox_layout)
        # ************************************************************************************************************ #
        self.record_button = QPushButton("START")
        self.record_button.setFixedWidth(300)
        self.record_button.setFixedHeight(50)
        self.record_groupBox_layout.addWidget(self.record_button)
        self.record_now = 0
        # ------------------------------------------------------------------------------------------------------------ #
        self.record_button.clicked.connect(self.record_button_clicked)

    def record_button_clicked(self):
        if self.record_now == 0:
            self.RecordData = RecordData(board_name=self.board_name,
                                         board_version=self.board_version,
                                         port_name=self.port_name,
                                         sequential=True)
            self.record_button.setText("STOP")
            self.record_button.setStyleSheet('QPushButton {;color: red;}')
            self.record_now = 1
        else:
            self.RecordData.close_record(sequential=True)
            self.record_button.setText("START")
            self.record_button.setStyleSheet('QPushButton {color: black;}')
            self.record_now = 0

    def is_recording_now(self, line=None):
        if self.record_now == 1:
            self.RecordData.save_data(line)
