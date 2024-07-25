########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       ComSelect.py
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
from PyQt6.QtSerialPort import *
from PyQt6.QtWidgets import *


class ComSelect(QDialog):
    """
    This class is a dialog window asking the user for COM port
    """
    def __init__(self, default_search=""):
        super(ComSelect, self).__init__(None)

        self.select_layout = QVBoxLayout(self)

        # ************************************************************************************************************ #
        # Board(s) selection
        self.board_groupBox = QGroupBox("Boards")
        self.board_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.select_layout.addWidget(self.board_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        # all available com ports, with the most probable one on top
        com_ports = QSerialPortInfo.availablePorts()
        com_ports11 = ["{} {}".format(x.systemLocation(), x.description()) for x in com_ports if default_search in
                       x.description()]
        com_ports12 = ["{} {}".format(x.systemLocation(), x.description()) for x in com_ports if default_search not in
                       x.description()]
        com_ports21 = ["{} {}".format(x.systemLocation(), x.description()) for x in com_ports if default_search in
                       x.description()]
        com_ports22 = ["{} {}".format(x.systemLocation(), x.description()) for x in com_ports if default_search not in
                       x.description()]
        # ------------------------------------------------------------------------------------------------------------ #
        # select if you want to control 1 or 2 boards
        self.number_board_comboBox = QComboBox(self)
        self.number_board_comboBox.addItem('1 Board')
        self.number_board_comboBox.addItem('2 Boards')
        # ------------------------------------------------------------------------------------------------------------ #
        # list all available com port in the combobox for board #1
        self.board_1_port_comboBox = QComboBox(self)
        self.board_1_port_comboBox.addItems(com_ports11)
        self.board_1_port_comboBox.addItems(com_ports12)
        # ------------------------------------------------------------------------------------------------------------ #
        # list all available com port in the combobox for board #2
        self.board_2_port_comboBox = QComboBox(self)
        self.board_2_port_comboBox.addItems(com_ports21)
        self.board_2_port_comboBox.addItems(com_ports22)
        # ------------------------------------------------------------------------------------------------------------ #
        self.board_groupBox_layout = QFormLayout(self)
        self.board_groupBox_layout.addRow(self.number_board_comboBox)
        self.board_groupBox_layout.addRow(QLabel("\nPlease select COM port with description: 'CP210x...'"))
        self.board_groupBox_layout.addRow(QLabel("Try to disconnect and reconnect board power supply if unable to "
                                                 "connect\n"))
        self.board_groupBox_layout.addRow("Board #1:", self.board_1_port_comboBox)
        self.board_groupBox_layout.addRow("Board #2:", self.board_2_port_comboBox)
        self.board_groupBox.setLayout(self.board_groupBox_layout)
        # ************************************************************************************************************ #
        # Display(s) selection
        self.display_groupBox = QGroupBox("Displays")
        self.display_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.select_layout.addWidget(self.display_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        # list all available display in the combobox for voltage(s) display(s)
        self.voltage_display_comboBox = QComboBox(self)
        self.voltage_display_comboBox.addItem('No display')
        self.voltage_display_comboBox.addItem('High-Voltage')
        self.voltage_display_comboBox.addItem('High-Voltage + Low Voltage')
        # ------------------------------------------------------------------------------------------------------------ #
        # list all available display in the combobox for current(s) display(s)
        self.current_display_comboBox = QComboBox(self)
        self.current_display_comboBox.addItem('No display')
        self.current_display_comboBox.addItem('1 plot with 8 currents monitoring')
        self.current_display_comboBox.addItem('4 plots with 2 currents monitoring (FB)')
        self.current_display_comboBox.addItem('8 plots with 1 current monitoring (HB)')
        # ------------------------------------------------------------------------------------------------------------ #
        self.display_groupBox_layout = QFormLayout(self)
        self.display_groupBox_layout.addWidget(QLabel("Please select which currents display you want "))
        self.display_groupBox_layout.addRow("Voltages:", self.voltage_display_comboBox)
        self.display_groupBox_layout.addRow("Currents:", self.current_display_comboBox)
        self.display_groupBox.setLayout(self.display_groupBox_layout)
        # ************************************************************************************************************ #
        # Option(s) selection
        self.options_groupBox = QGroupBox("Options")
        self.options_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.select_layout.addWidget(self.options_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        # check box for debug mode
        self.debug_checkBox = QCheckBox()
        self.debug_checkBox.setChecked(True)
        self.debug_checkBox.setFixedWidth(15)
        self.debug_checkBox_title_lbl = QLabel("Debug mode")
        self.debug_checkBox_title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.debug_checkBox_title_lbl.setFixedWidth(100)
        # ------------------------------------------------------------------------------------------------------------ #
        # check box to display received data c
        self.display_cmd_checkBox = QCheckBox()
        self.display_cmd_checkBox.setFixedWidth(15)
        self.display_cmd_checkBox_title_lbl = QLabel("Received data")
        self.display_cmd_checkBox_title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.display_cmd_checkBox_title_lbl.setFixedWidth(100)
        # ------------------------------------------------------------------------------------------------------------ #
        # check box to record data
        self.record_checkBox = QCheckBox()
        self.record_checkBox.setFixedWidth(15)
        self.record_checkBox_title_lbl = QLabel("Record data")
        self.record_checkBox_title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.record_checkBox_title_lbl.setFixedWidth(100)
        # ------------------------------------------------------------------------------------------------------------ #
        self.option_groupBox_layout = QHBoxLayout(self)
        self.option_groupBox_layout.addWidget(self.debug_checkBox)
        self.option_groupBox_layout.addWidget(self.debug_checkBox_title_lbl)
        self.option_groupBox_layout.addWidget(self.display_cmd_checkBox)
        self.option_groupBox_layout.addWidget(self.display_cmd_checkBox_title_lbl)
        self.option_groupBox_layout.addWidget(self.record_checkBox)
        self.option_groupBox_layout.addWidget(self.record_checkBox_title_lbl)
        self.options_groupBox.setLayout(self.option_groupBox_layout)
        # ************************************************************************************************************ #
        # Button to confirm selections
        self.button_layout = QFormLayout(self)
        self.select_layout.addLayout(self.button_layout)
        # ------------------------------------------------------------------------------------------------------------ #
        self.button_box = QDialogButtonBox()
        # self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        # ------------------------------------------------------------------------------------------------------------ #
        self.button_box.clicked.connect(self.test_2_boards_different_ports)
        # ------------------------------------------------------------------------------------------------------------ #
        self.button_layout.addRow(self.button_box)
        # ************************************************************************************************************ #
        # Window size
        self.setGeometry(100, 100, 450, 100)

    ####################################################################################################################
    def test_2_boards_different_ports(self):
        if self.number_board_comboBox.currentIndex() == 0:
            self.button_box.accepted.connect(self.accept)
        else:
            if self.board_1_port_comboBox.currentText() != self.board_2_port_comboBox.currentText():
                self.button_box.accepted.connect(self.accept)
            else:
                QMessageBox.critical(self, 'Error', 'Please select 2 different ports')

    ####################################################################################################################
    def get_number_boards_used(self):
        return self.number_board_comboBox.currentIndex() + 1

    ####################################################################################################################
    def get_board_1_port_results(self):
        return self.board_1_port_comboBox.currentText().split(" ")[0]

    ####################################################################################################################
    def get_board_2_port_results(self):
        return self.board_2_port_comboBox.currentText().split(" ")[0]

    ####################################################################################################################
    def get_currents_display_results(self):
        return self.current_display_comboBox.currentIndex()

    ####################################################################################################################
    def get_voltages_display_results(self):
        return self.voltage_display_comboBox.currentIndex()

    ####################################################################################################################
    def get_debug_mode_results(self):
        return self.debug_checkBox.isChecked()

    ####################################################################################################################
    def get_record_data_results(self):
        return self.record_checkBox.isChecked()

    ####################################################################################################################
    def get_rvc_data_results(self):
        return self.display_cmd_checkBox.isChecked()
