########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       voltage.py
# @brief      Author:             MBE
#             Institute:          EPFL
#             Laboratory:         LMTS
#             Software version:   v1.08 (SYLVAIN/MARTIJN)
#             Created on:         08.11.2023
#             Last modifications: 08.11.2023
#
# Copyright 2021/2023 EPFL-LMTS
# All rights reserved.
########################################################################################################################

# python packages
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
# custom packages
from py_toggle import PyToggle
from SerialSender import *
from Userdef import *


class Voltage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.ser = None
        self.label = None

        # ************************************************************************************************************ #
        self.voltage_groupBox = QGroupBox("High Voltage")
        self.voltage_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.voltage_groupBox.setFixedWidth(680)
        # ------------------------------------------------------------------------------------------------------------ #
        self.voltage_layout = QVBoxLayout(self)
        self.voltage_layout.addWidget(self.voltage_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.voltage_groupBox_layout = QGridLayout(self.voltage_groupBox)
        self.voltage_groupBox_layout.setHorizontalSpacing(25)
        # self.voltage_groupBox_layout.setColumnMinimumWidth(100, 50)
        self.voltage_groupBox.setLayout(self.voltage_groupBox_layout)
        # ************************************************************************************************************ #
        # TITLES LINE
        # ------------------------------------------------------------------------------------------------------------ #
        self.target_voltage_lbl = QLabel("Target:")
        self.target_voltage_lbl.setFixedWidth(75)
        # ------------------------------------------------------------------------------------------------------------ #
        self.target_voltage_edit = QLineEdit("0")
        self.target_voltage_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.target_voltage_edit.setFixedWidth(75)
        # ------------------------------------------------------------------------------------------------------------ #
        self.target_voltage_update_btn = QPushButton("Update")
        self.target_voltage_update_btn.setFixedWidth(75)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hv_toggle = PyToggle(animation_curve=QEasingCurve.Type.InOutQuint)
        self.hv_toggle_previous_state = 0
        # ------------------------------------------------------------------------------------------------------------ #
        self.current_voltage_lbl = QLabel("Current:")
        self.current_voltage_lbl.setFixedWidth(75)
        # ------------------------------------------------------------------------------------------------------------ #
        self.current_voltage_value_lbl = QLabel("0")
        self.current_voltage_value_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.current_voltage_value_lbl.setFixedWidth(75)
        # ------------------------------------------------------------------------------------------------------------ #
        self.voltage_on_off_label = QLabel("OFF")
        self.voltage_label_off()
        self.voltage_on_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltage_on_off_label.setFixedSize(75, 25)
        # ------------------------------------------------------------------------------------------------------------ #
        self.voltage_groupBox_layout.addWidget(self.target_voltage_lbl, 0, 0)
        self.voltage_groupBox_layout.addWidget(self.target_voltage_edit, 0, 1)
        self.voltage_groupBox_layout.addWidget(self.target_voltage_update_btn, 0, 2)
        self.voltage_groupBox_layout.addWidget(self.hv_toggle, 0, 3)
        self.voltage_groupBox_layout.addWidget(self.current_voltage_lbl, 1, 0)
        self.voltage_groupBox_layout.addWidget(self.current_voltage_value_lbl, 1, 1)
        self.voltage_groupBox_layout.addWidget(self.voltage_on_off_label, 1, 2)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hv_toggle.stateChanged.connect(self.hv_toggled)
        self.target_voltage_edit.returnPressed.connect(self.voltage_set)
        self.target_voltage_update_btn.clicked.connect(self.voltage_set)

    ####################################################################################################################
    # ATTACH SERIAL
    def attach_serial(self, serial):
        self.ser = serial

    ####################################################################################################################
    def update_data(self, current_voltage):
        self.current_voltage_value_lbl.setText("{}".format(int(current_voltage)))

        if current_voltage > 100:
            # change the state of the button
            self.voltage_label_on()
        else:
            # change the state of the button
            self.voltage_label_off()

    ####################################################################################################################
    # CHECKBOX TOGGLED
    def hv_toggled(self):
        if self.hv_toggle.isChecked() == 1 and self.hv_toggle_previous_state == 0:
            self.voltage_set()
        if self.hv_toggle.isChecked() == 1 and self.hv_toggle_previous_state == 1:
            self.voltage_set()
        elif self.hv_toggle.isChecked() == 0 and self.hv_toggle_previous_state == 0:
            self.voltage_set()
        elif self.hv_toggle.isChecked() == 0 and self.hv_toggle_previous_state == 1:
            self.voltage_stop()

    ####################################################################################################################
    # BTN CLICKED (STATE => ON)
    def voltage_set(self):
        try:
            new_hv_val = float(self.target_voltage_edit.text())
            # check value
            if (new_hv_val >= hv_min) and (new_hv_val <= hv_max):
                # change the state of the checkbox
                self.hv_toggle_on()
                self.hv_toggle_previous_state = 1
                # send through the serial port
                to_send = "\r\nSHV {}\r\n".format(new_hv_val)
                send_command(self.ser, to_send)
                # display information message
                print("[INFO] HV ON: {} V".format(new_hv_val))
            elif new_hv_val == 0:
                self.voltage_stop()
                self.hv_toggle_previous_state = 0
            else:
                self.voltage_stop()
                self.hv_toggle_previous_state = 0
                # display error message
                print(f"[ERR] please respect voltage range [{hv_min};{hv_max}] V")
        except Exception as err_voltage_edit:
            # display error message
            print("[ERR] HV VAL: {} - {}".format(self.target_voltage_edit.text(), err_voltage_edit))
        return

    ####################################################################################################################
    # BTN CLICKED (STATE => OFF)
    def voltage_stop(self):
        # change the state of the checkbox
        self.hv_toggle_off()
        # send through the serial port
        to_send = "\r\nSHV 0\r\n"
        send_command(self.ser, to_send)
        # display information message
        print("[INFO] HV OFF")

    ####################################################################################################################
    def hv_toggle_on(self):
        self.hv_toggle.setChecked(True)
        self.hv_toggle.start_transition(1)

    ####################################################################################################################
    def hv_toggle_off(self):
        self.hv_toggle.setChecked(False)
        self.hv_toggle.start_transition(0)

    ####################################################################################################################
    # LABEL STATE ON
    def voltage_label_on(self):
        self.voltage_on_off_label.setText("ON")
        self.voltage_on_off_label.setStyleSheet('background-color: green; '
                                                'color: white; '
                                                'position: center; '
                                                'border: 1px solid black;')

    ####################################################################################################################
    # LABEL STATE OFF
    def voltage_label_off(self):
        self.voltage_on_off_label.setText("OFF")
        self.voltage_on_off_label.setStyleSheet('background-color: red; '
                                                'color: white; '
                                                'position: center; '
                                                'border: 1px solid black;')
