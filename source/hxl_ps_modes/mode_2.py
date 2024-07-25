########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_modes\mode_2.py
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
from py_toggle.py_toggle import *
from SerialSender import *
from Userdef import *


class Mode2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.fb_ser = None

        # ************************************************************************************************************ #
        self.mode2_groupBox = QGroupBox("Full-Bridges")
        self.mode2_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.mode2_groupBox.setFixedWidth(680)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode2_layout = QVBoxLayout(self)
        self.mode2_layout.addWidget(self.mode2_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode2_groupBox_layout = QGridLayout(self.mode2_groupBox)
        self.mode2_groupBox_layout.setHorizontalSpacing(25)
        self.mode2_groupBox.setLayout(self.mode2_groupBox_layout)
        # ************************************************************************************************************ #
        # TITLES LINE
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_freq_label = QLabel("Frequency (Hz)")
        self.fb_freq_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_pos_duty_label = QLabel("PosDuty (%)")
        self.fb_pos_duty_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_neg_duty_label = QLabel("NegDuty (%)")
        self.fb_neg_duty_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_pulse_phase_label = QLabel("Pulse Phase (°)")
        # self.fb_pulse_phase_label.setAlignment(Qt.AlignmentFlag.AAlignCenter)
        self.fb_pulse_phase_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_phase_shift_label = QLabel("Phase Shift (°)")
        # self.fb_phase_shift_label.setAlignment(Qt.AlignmentFlag.AAlignCenter)
        self.fb_phase_shift_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_on_off_label = QLabel("ON/OFF")
        self.fb_on_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fb_on_off_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode2_groupBox_layout.addWidget(self.fb_freq_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode2_groupBox_layout.addWidget(self.fb_pos_duty_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode2_groupBox_layout.addWidget(self.fb_neg_duty_label, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode2_groupBox_layout.addWidget(self.fb_pulse_phase_label, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode2_groupBox_layout.addWidget(self.fb_phase_shift_label, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode2_groupBox_layout.addWidget(self.fb_on_off_label, 0, 6, Qt.AlignmentFlag.AlignCenter)
        # ************************************************************************************************************ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_lbl = []
        self.fb_state_label = []
        self.fb_freq_edit = []
        self.fb_pos_duty_edit = []
        self.fb_neg_duty_edit = []
        self.fb_pulse_phase_edit = []
        self.fb_phase_shift_edit = []
        self.fb_toggle = []

        for row in range(nbFullBridges):
            full_bridge = row + 1
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_lbl.append(QLabel("Full-Bridge {}".format(full_bridge)))
            self.fb_lbl[row].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.fb_lbl[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_freq_edit.append(QLineEdit("1"))
            self.fb_freq_edit[row].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.fb_freq_edit[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_pos_duty_edit.append(QLineEdit("50"))
            self.fb_pos_duty_edit[row].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.fb_pos_duty_edit[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_neg_duty_edit.append(QLineEdit("50"))
            self.fb_neg_duty_edit[row].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.fb_neg_duty_edit[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_pulse_phase_edit.append(QLineEdit("180"))
            self.fb_pulse_phase_edit[row].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.fb_pulse_phase_edit[row].setFixedWidth(80)
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_phase_shift_edit.append(QLineEdit("-"))
            self.fb_phase_shift_edit[row].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.fb_phase_shift_edit[row].setFixedWidth(80)
            self.fb_phase_shift_edit[row].setEnabled(False)
            # -------------------------------------------------------------------------------------------------------- #
            self.fb_toggle.append(PyToggle(animation_curve=QEasingCurve.Type.InOutQuint))
            # -------------------------------------------------------------------------------------------------------- #
            self.mode2_groupBox_layout.addWidget(self.fb_lbl[row], full_bridge, 0, Qt.AlignmentFlag.AlignCenter)
            self.mode2_groupBox_layout.addWidget(self.fb_freq_edit[row], full_bridge, 1, Qt.AlignmentFlag.AlignCenter)
            self.mode2_groupBox_layout.addWidget(self.fb_pos_duty_edit[row], full_bridge, 2, Qt.AlignmentFlag.AlignCenter)
            self.mode2_groupBox_layout.addWidget(self.fb_neg_duty_edit[row], full_bridge, 3, Qt.AlignmentFlag.AlignCenter)
            self.mode2_groupBox_layout.addWidget(self.fb_pulse_phase_edit[row], full_bridge, 4, Qt.AlignmentFlag.AlignCenter)
            self.mode2_groupBox_layout.addWidget(self.fb_phase_shift_edit[row], full_bridge, 5, Qt.AlignmentFlag.AlignCenter)
            self.mode2_groupBox_layout.addWidget(self.fb_toggle[row], full_bridge, 6, Qt.AlignmentFlag.AlignCenter)
            # -------------------------------------------------------------------------------------------------------- #
            # ACTIONS
            self.fb_toggle[row].stateChanged.connect(lambda _unused_, row_id=row: self.fb_toggled(row=row_id))
            self.fb_freq_edit[row].returnPressed.connect(lambda row_id=row: self.fb_set(row=row_id))
            self.fb_pos_duty_edit[row].returnPressed.connect(lambda row_id=row: self.fb_set(row=row_id))
            self.fb_neg_duty_edit[row].returnPressed.connect(lambda row_id=row: self.fb_set(row=row_id))
            self.fb_pulse_phase_edit[row].returnPressed.connect(lambda row_id=row: self.fb_set(row=row_id))
        # ************************************************************************************************************ #
        # STOP HALF-BRIDGES (PushButton)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_stop_btn = QPushButton("Stop all")
        self.fb_stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; position: center; "
                                       "border: 1px solid black;")
        self.fb_stop_btn.setFixedSize(75, 25)
        self.mode2_groupBox_layout.addWidget(self.fb_stop_btn, nbFullBridges + 1, 6, Qt.AlignmentFlag.AlignCenter)
        # ------------------------------------------------------------------------------------------------------------ #
        # ACTIONS
        self.fb_stop_btn.clicked.connect(self.fb_stop_btn_clicked)  # stop target voltage

        self.mode2_layout.addStretch(1)

    ####################################################################################################################
    # ATTACH SERIAL
    def attach_serial(self, serial):
        self.fb_ser = serial

    ####################################################################################################################
    # CHECKBOX TOGGLED
    def fb_toggled(self, row=0):
        if self.fb_toggle[row].isChecked() == 1:
            self.fb_set(row)
        else:
            self.fb_stop(row)

    ####################################################################################################################
    # TOGGLE CLICKED = SET STATE
    def fb_set(self, row):
        try:
            channel_val = pow(2, row)
            freq_val = float(self.fb_freq_edit[row].text())
            pos_duty_val = int(self.fb_pos_duty_edit[row].text())
            neg_duty_val = int(self.fb_neg_duty_edit[row].text())
            pulse_phase_val = int(self.fb_pulse_phase_edit[row].text())
            # check frequency/duty cycle value
            pos_pulse_width = float(5 * (pos_duty_val / freq_val) * 5)
            neg_pulse_width = float(5 * (pos_duty_val / freq_val) * 5)
            if pos_pulse_width < 2:
                self.fb_stop(row)
                print("[ERR] Positive pulse width: {} ms < 2 ms".format(pos_pulse_width))
            elif neg_pulse_width < 2:
                self.fb_stop(row)
                print("[ERR] Negative pulse width: {} ms < 2 ms".format(neg_pulse_width))
            else:
                if (freq_val >= f_min) and (freq_val <= f_max):
                    # change the state of the checkbox
                    self.fb_toggle_on(row)
                    # send through the serial port
                    to_send = "\r\nSM2 {} {} {} {} {}\r\n".format(channel_val, freq_val, pos_duty_val, neg_duty_val,
                                                                  pulse_phase_val)
                    send_command(self.fb_ser, to_send)
                    # display information message
                    print("[INFO] Mode 2  ON ({} | {}Hz | {}% | {}% | {}°)".format(channel_val, freq_val, pos_duty_val,
                                                                                   neg_duty_val, pulse_phase_val))
                else:
                    self.fb_stop(row)
        except Exception as err_fb_freq_edit:
            # display error message
            print("[ERR] HB FREQ VAL: {} - {}".format(self.fb_freq_edit[row].text(), err_fb_freq_edit))
        return

    ####################################################################################################################
    # BTN CLICKED (STOP STATE)
    def fb_stop(self, row):
        full_bridge = row + 1
        # change the state of toggle
        self.fb_toggle_off(row)
        # send through the serial port
        to_send = "\r\nCM2 {}\r\n".format(pow(2, row))
        print("[INFO CMD] {} ".format(to_send))
        send_command(self.fb_ser, to_send)
        # display information message
        print("[INFO] Mode 2 - Full-Bridge {} OFF".format(full_bridge))

    ####################################################################################################################
    def fb_toggle_on(self, row):
        self.fb_toggle[row].setChecked(True)
        self.fb_toggle[row].start_transition(1)

    ####################################################################################################################
    def fb_toggle_off(self, row):
        self.fb_toggle[row].setChecked(False)
        self.fb_toggle[row].start_transition(0)

    ####################################################################################################################
    def fb_stop_btn_clicked(self):
        try:
            for row in range(nbFullBridges):
                self.fb_toggle_off(row)
            # send through the serial port
            to_send = "\r\nCM2 0\r\n"
            send_command(self.fb_ser, to_send)
            # display information message
            print("[INFO] Mode 2: All Full-Bridges OFF")
        except Exception as e:
            print(e)
        return
