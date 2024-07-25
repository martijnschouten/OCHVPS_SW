########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\ComSelect.py
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
from PyQt6.QtSerialPort import *
from PyQt6.QtWidgets import *


########################################################################################################################
class ComSelect(QDialog):
    """
    This class is a dialog window asking the user for COM port
    """

    def __init__(self, default_search=""):
        super(ComSelect, self).__init__(None)

        self.select_layout = QVBoxLayout(self)

        # ------------------------------------------------------------------------------------------------------------ #
        # Board(s) selection
        self.board_groupBox = QGroupBox("Boards")
        self.board_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.select_layout.addWidget(self.board_groupBox)

        # ------------------------------------------------------------------------------------------------------------ #
        # all available com ports, with the most probable one on top
        com_ports = QSerialPortInfo.availablePorts()
        com_ports_11 = [f"{x.systemLocation()} {x.description()}" for x in com_ports if default_search in
                        x.description()]
        com_ports_12 = [f"{x.systemLocation()} {x.description()}" for x in com_ports if default_search not in
                        x.description()]
        self.com_ports_21 = [f"{x.systemLocation()} {x.description()}" for x in com_ports if default_search in
                             x.description()]
        self.com_ports_22 = [f"{x.systemLocation()} {x.description()}" for x in com_ports if default_search not in
                             x.description()]

        # ------------------------------------------------------------------------------------------------------------ #
        # select if you want to control 1 or 2 boards
        self.number_board_comboBox = QComboBox(self)
        self.number_board_comboBox.addItems(('1 Board', '2 Boards'))
        self.number_board_comboBox.currentTextChanged.connect(self.update_scale_combo)

        # ------------------------------------------------------------------------------------------------------------ #
        # list all available com port in the combobox for board #1
        self.board_1_port_comboBox = QComboBox(self)
        self.board_1_port_comboBox.addItems(com_ports_11)
        self.board_1_port_comboBox.addItems(com_ports_12)

        # ------------------------------------------------------------------------------------------------------------ #
        # list all available com port in the combobox for board #2
        self.board_2_port_comboBox = QComboBox(self)
        self.board_2_port_comboBox.setEnabled(False)
        self.board_2_port_comboBox.addItem("-")

        # ------------------------------------------------------------------------------------------------------------ #
        self.board_groupBox_layout = QFormLayout(self)
        self.board_groupBox_layout.addRow(self.number_board_comboBox)
        self.board_groupBox_layout.addRow(QLabel("\nPlease select COM port with description: 'CP210x...'"))
        self.board_groupBox_layout.addRow(QLabel("Try to disconnect and reconnect board power supply if unable to "
                                                 "connect\n"))
        self.board_groupBox_layout.addRow("Board #1:", self.board_1_port_comboBox)
        self.board_groupBox_layout.addRow("Board #2:", self.board_2_port_comboBox)
        self.board_groupBox.setLayout(self.board_groupBox_layout)

        # ------------------------------------------------------------------------------------------------------------ #
        # Display(s) selection

        self.display_groupBox = QGroupBox("Displays")
        self.display_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.select_layout.addWidget(self.display_groupBox)

        # ------------------------------------------------------------------------------------------------------------ #
        # list all available display in the combobox for voltage(s) display(s)
        self.voltage_display_comboBox = QComboBox(self)
        self.voltage_display_comboBox.addItems(('No display',
                                                'High-Voltage',
                                                'High-Voltage + Low Voltage'))

        # ------------------------------------------------------------------------------------------------------------ #
        # list all available display in the combobox for current(s) display(s)
        self.current_display_comboBox = QComboBox(self)
        self.current_display_comboBox.addItems(('No display',
                                                '1 plot with 8 currents monitoring',
                                                '4 plots with 2 currents monitoring (FB)',
                                                '8 plots with 1 current monitoring (HB)'))

        # ------------------------------------------------------------------------------------------------------------ #
        self.display_groupBox_layout = QFormLayout(self)
        self.display_groupBox_layout.addWidget(QLabel("Please select which currents display you want "))
        self.display_groupBox_layout.addRow("Voltages:", self.voltage_display_comboBox)
        self.display_groupBox_layout.addRow("Currents:", self.current_display_comboBox)
        self.display_groupBox.setLayout(self.display_groupBox_layout)

        # ------------------------------------------------------------------------------------------------------------ #
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
        self.debug_checkBox_title_lbl.setFixedWidth(200)

        # ------------------------------------------------------------------------------------------------------------ #
        # check box to record data
        self.record_checkBox = QCheckBox()
        self.record_checkBox.setChecked(False)
        self.record_checkBox.setFixedWidth(15)

        self.record_checkBox_title_lbl = QLabel("Record data")
        self.record_checkBox_title_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.record_checkBox_title_lbl.setFixedWidth(200)

        # ------------------------------------------------------------------------------------------------------------ #
        self.option_groupBox_layout = QHBoxLayout(self)
        self.option_groupBox_layout.addWidget(self.debug_checkBox)
        self.option_groupBox_layout.addWidget(self.debug_checkBox_title_lbl)
        self.option_groupBox_layout.addWidget(self.record_checkBox)
        self.option_groupBox_layout.addWidget(self.record_checkBox_title_lbl)
        self.options_groupBox.setLayout(self.option_groupBox_layout)

        # ------------------------------------------------------------------------------------------------------------ #
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

        # ------------------------------------------------------------------------------------------------------------ #
        # Window size
        self.setGeometry(100, 100, 450, 100)

    # **************************************************************************************************************** #
    def update_scale_combo(self, text):
        self.board_2_port_comboBox.clear()
        if text == "1 Board":
            self.board_2_port_comboBox.setEnabled(False)
            self.board_2_port_comboBox.addItem("-")
        elif text == "2 Boards":
            self.board_2_port_comboBox.setEnabled(True)
            self.board_2_port_comboBox.addItems(self.com_ports_21)
            self.board_2_port_comboBox.addItems(self.com_ports_22)

    # **************************************************************************************************************** #
    def test_2_boards_different_ports(self):
        if self.number_board_comboBox.currentIndex() == 0:
            self.button_box.accepted.connect(self.accept)
        else:
            if self.board_1_port_comboBox.currentText() != self.board_2_port_comboBox.currentText():
                self.button_box.accepted.connect(self.accept)
            else:
                QMessageBox.critical(self, 'Error', 'Please select 2 different ports')

    # **************************************************************************************************************** #
    def get_settings(self):
        settings = {
            'nb_board': self.number_board_comboBox.currentIndex() + 1,
            'id_board': 0,
            'port_#01': self.board_1_port_comboBox.currentText().split(" ")[0],
            'port_#02': self.board_2_port_comboBox.currentText().split(" ")[0],
            'current': self.current_display_comboBox.currentIndex(),
            'voltage': self.voltage_display_comboBox.currentIndex(),
            'debug': self.debug_checkBox.isChecked(),
            'record': self.record_checkBox.isChecked(),
        }
        return settings
