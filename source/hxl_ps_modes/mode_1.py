########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_modes\mode_1.py
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
# custom packages
from SerialSender import *
from py_toggle import *
from Userdef import *


class Mode1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.hb_ser = None

        # ************************************************************************************************************ #
        self.mode1_groupBox = QGroupBox("Half-Bridges")
        self.mode1_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.mode1_groupBox.setFixedWidth(680)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode1_layout = QVBoxLayout(self)
        self.mode1_layout.addWidget(self.mode1_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode1_groupBox_layout = QGridLayout(self.mode1_groupBox)
        self.mode1_groupBox_layout.setHorizontalSpacing(25)
        self.mode1_groupBox.setLayout(self.mode1_groupBox_layout)
        # ************************************************************************************************************ #
        # TITLES LINE
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_freq_label = QLabel("Frequency (Hz)")
        # self.fb_freq_label.setAlignment(Qt.AlignLeft)
        self.hb_freq_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_pos_duty_label = QLabel("PosDuty (%)")
        # self.fb_duty_label.setAlignment(Qt.AlignLeft)
        self.hb_pos_duty_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_neg_duty_label = QLabel("NegDuty (%)")
        # self.fb_duty_label.setAlignment(Qt.AlignLeft)
        self.hb_neg_duty_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_pulse_phase_label = QLabel("Pulse Phase (°)")
        # self.fb_phase_label.setAlignment(Qt.AlignLeft)
        self.hb_pulse_phase_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_phase_shift_label = QLabel("Phase Shift (°)")
        # self.fb_phase_label.setAlignment(Qt.AlignLeft)
        self.hb_phase_shift_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_on_off_label = QLabel("ON/OFF")
        self.hb_on_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hb_on_off_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode1_groupBox_layout.addWidget(self.hb_freq_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode1_groupBox_layout.addWidget(self.hb_pos_duty_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode1_groupBox_layout.addWidget(self.hb_neg_duty_label, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode1_groupBox_layout.addWidget(self.hb_pulse_phase_label, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode1_groupBox_layout.addWidget(self.hb_phase_shift_label, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode1_groupBox_layout.addWidget(self.hb_on_off_label, 0, 6, Qt.AlignmentFlag.AlignCenter)
        # ************************************************************************************************************ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_lbl = []
        self.hb_freq_edit = []
        self.hb_pos_duty_edit = []
        self.hb_neg_duty_edit = []
        self.hb_pulse_phase_edit = []
        self.hb_phase_shift_edit = []
        self.hb_toggle = []

        for row in range(nbHalfBridges):
            hb_id = row + 1
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_lbl.append(QLabel("Half-Bridge {}".format(hb_id)))
            self.hb_lbl[row].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hb_lbl[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_freq_edit.append(QLineEdit("1"))
            self.hb_freq_edit[row].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.hb_freq_edit[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_pos_duty_edit.append(QLineEdit("50"))
            self.hb_pos_duty_edit[row].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.hb_pos_duty_edit[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_neg_duty_edit.append(QLineEdit("-"))
            self.hb_neg_duty_edit[row].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hb_neg_duty_edit[row].setFixedWidth(80)
            self.hb_neg_duty_edit[row].setEnabled(False)
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_pulse_phase_edit.append(QLineEdit("-"))
            self.hb_pulse_phase_edit[row].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hb_pulse_phase_edit[row].setFixedWidth(80)
            self.hb_pulse_phase_edit[row].setEnabled(False)
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_phase_shift_edit.append(QLineEdit("-"))
            self.hb_phase_shift_edit[row].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hb_phase_shift_edit[row].setFixedWidth(80)
            self.hb_phase_shift_edit[row].setEnabled(False)
            # -------------------------------------------------------------------------------------------------------- #
            self.hb_toggle.append(PyToggle(animation_curve=QEasingCurve.Type.InOutQuint))
            # -------------------------------------------------------------------------------------------------------- #
            self.mode1_groupBox_layout.addWidget(self.hb_lbl[row], hb_id, 0, Qt.AlignmentFlag.AlignCenter)
            self.mode1_groupBox_layout.addWidget(self.hb_freq_edit[row], hb_id, 1, Qt.AlignmentFlag.AlignCenter)
            self.mode1_groupBox_layout.addWidget(self.hb_pos_duty_edit[row], hb_id, 2, Qt.AlignmentFlag.AlignCenter)
            self.mode1_groupBox_layout.addWidget(self.hb_neg_duty_edit[row], hb_id, 3, Qt.AlignmentFlag.AlignCenter)
            self.mode1_groupBox_layout.addWidget(self.hb_pulse_phase_edit[row], hb_id, 4, Qt.AlignmentFlag.AlignCenter)
            self.mode1_groupBox_layout.addWidget(self.hb_phase_shift_edit[row], hb_id, 5, Qt.AlignmentFlag.AlignCenter)
            self.mode1_groupBox_layout.addWidget(self.hb_toggle[row], hb_id, 6, Qt.AlignmentFlag.AlignCenter)
            # -------------------------------------------------------------------------------------------------------- #
            # ACTIONS
            self.hb_toggle[row].stateChanged.connect(lambda _unused_, row_id=row: self.hb_checkbox_toggled(row=row_id))
            self.hb_freq_edit[row].returnPressed.connect(lambda row_id=row: self.hb_set(row=row_id))
            self.hb_pos_duty_edit[row].returnPressed.connect(lambda row_id=row: self.hb_set(row=row_id))
        # ************************************************************************************************************ #
        # STOP HALF-BRIDGES (PushButton)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_stop_btn = QPushButton("Stop all")
        self.hb_stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; position: center; "
                                       "border: 1px solid black;")
        self.hb_stop_btn.setFixedSize(75, 25)
        self.mode1_groupBox_layout.addWidget(self.hb_stop_btn, nbHalfBridges+1, 6, Qt.AlignmentFlag.AlignCenter)
        # ------------------------------------------------------------------------------------------------------------ #
        # ACTIONS
        self.hb_stop_btn.clicked.connect(self.hb_stop_btn_clicked)  # stop target voltage

        self.mode1_layout.addStretch(1)

    ####################################################################################################################
    # ATTACH SERIAL
    def attach_serial(self, serial):
        self.hb_ser = serial

    ####################################################################################################################
    # CHECKBOX TOGGLED
    def hb_checkbox_toggled(self, row=0):
        if self.hb_toggle[row].isChecked() == 1:
            self.hb_set(row)
        else:
            self.hb_stop(row)

    ####################################################################################################################
    # TOGGLE CLICKED = SET STATE
    def hb_set(self, row):
        try:
            channel_val = int(pow(2, row))
            freq_val = float(self.hb_freq_edit[row].text())
            pos_duty_val = float(self.hb_pos_duty_edit[row].text())
            # check frequency/duty cycle value
            if (freq_val == 0) or (pos_duty_val == 100):
                # change the state of the checkbox
                self.hb_toggle_on(row)
                # send through the serial port
                to_send = "\r\nSM1 {} {} {}\r\n" .format(channel_val, 1, 100)
                send_command(self.hb_ser, to_send)
                # display information message
                print("[INFO] Mode 1: Half-Bridge {} ON (NO SWITCH)")
            elif (freq_val >= f_min) and (freq_val <= f_max):
                pos_pulse_width = float(10 * (pos_duty_val / freq_val))
                if pos_pulse_width > 2:
                    # change the state of the checkbox
                    self.hb_toggle_on(row)
                    # send through the serial port
                    to_send = "\r\nSM1 {} {} {}\r\n".format(channel_val, freq_val, pos_duty_val)
                    print("[INFO CMD] {} ".format(to_send))
                    send_command(self.hb_ser, to_send)
                    # display information message
                    print("[INFO] Mode 1 ON ({} | {} Hz | {} %)".format(channel_val, freq_val, pos_duty_val))
                else:
                    self.hb_stop(row)
                    print("[ERR] Positive pulse width: {} ms < 2 ms".format(pos_pulse_width))
            else:
                self.hb_stop(row)

        except Exception as err_hb_freq_edit:
            # display error message
            print("[ERR] HB FREQ VAL: {} - {}".format(self.hb_freq_edit[row].text(), err_hb_freq_edit))
        return

    ####################################################################################################################
    # TOGGLE NOT CLICKED = STOP STATE
    def hb_stop(self, row):
        half_bridge = row + 1
        # change the state of toggle
        self.hb_toggle_off(row)
        # send through the serial port
        to_send = "\r\nCM1 {}\r\n".format(pow(2, row))
        print("[INFO CMD] {} ".format(to_send))
        send_command(self.hb_ser, to_send)
        # display information message
        print("[INFO] Mode 1: Half-Bridge {} OFF".format(half_bridge))

    ####################################################################################################################
    def hb_toggle_on(self, row):
        self.hb_toggle[row].setChecked(True)
        self.hb_toggle[row].start_transition(1)

    ####################################################################################################################
    def hb_toggle_off(self, row):
        self.hb_toggle[row].setChecked(False)
        self.hb_toggle[row].start_transition(0)

    ####################################################################################################################
    def hb_stop_btn_clicked(self):
        try:
            for row in range(nbHalfBridges):
                self.hb_toggle_off(row)
            # send through the serial port
            to_send = "\r\nCM1 0\r\n"
            send_command(self.hb_ser, to_send)
            # display information message
            print("[INFO] Mode 1: All Half-Bridges OFF")
        except Exception as e:
            print(e)
        return
