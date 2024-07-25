########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_modes\mode_4.py
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
from py_toggle import *
from SerialSender import *
from Userdef import *


class Mode4(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.fb_ser = None

        # ************************************************************************************************************ #
        self.mode4_groupBox = QGroupBox("Multiple outputs in Bipolar")
        self.mode4_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.mode4_groupBox.setFixedWidth(680)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode4_layout = QVBoxLayout(self)
        self.mode4_layout.addWidget(self.mode4_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode4_groupBox_layout = QGridLayout(self.mode4_groupBox)
        self.mode4_groupBox_layout.setHorizontalSpacing(25)
        # self.mode3_groupBox_layout.setColumnMinimumWidth(80, 80)
        self.mode4_groupBox.setLayout(self.mode4_groupBox_layout)
        # ************************************************************************************************************ #
        # TITLES LINE (only labels)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_number_label = QLabel("Nb Output")
        # self.fb_freq_label.setAlignment(Qt.AlignLeft)
        self.fb_number_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_freq_label = QLabel("Frequency (Hz)")
        # self.fb_freq_label.setAlignment(Qt.AlignLeft)
        self.fb_freq_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_pos_duty_label = QLabel("PosDuty (%)")
        # self.fb_pos_duty_label.setAlignment(Qt.AlignLeft)
        self.fb_pos_duty_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_neg_duty_label = QLabel("NegDuty (%)")
        # self.fb_neg_duty_label.setAlignment(Qt.AlignLeft)
        self.fb_neg_duty_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_pulse_phase_label = QLabel("Pulse Phase (°)")
        # self.fb_pulse_phase_label.setAlignment(Qt.AlignLeft)
        self.fb_pulse_phase_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_phase_shift_label = QLabel("Phase Shift (°)")
        # self.fb_phase_label.setAlignment(Qt.AlignLeft)
        self.fb_phase_shift_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_on_off_label = QLabel("ON/OFF")
        self.fb_on_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fb_on_off_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode4_groupBox_layout.addWidget(self.fb_number_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_freq_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_pos_duty_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_neg_duty_label, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_pulse_phase_label, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_phase_shift_label, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_on_off_label, 0, 6, Qt.AlignmentFlag.AlignCenter)
        # ************************************************************************************************************ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)
        # ------------------------------------------------------------------------------------------------------------ #
        # list in the combobox all available options for phase shift
        self.fb_comboBox = QComboBox()
        self.fb_comboBox.addItem('1')
        self.fb_comboBox.addItem('2')
        self.fb_comboBox.addItem('3')
        self.fb_comboBox.addItem('4')
        self.fb_comboBox.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_freq_edit = QLineEdit("1")
        self.fb_freq_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fb_freq_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_pos_duty_edit = QLineEdit("50")
        self.fb_pos_duty_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fb_pos_duty_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_neg_duty_edit = QLineEdit("50")
        self.fb_neg_duty_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fb_neg_duty_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_pulse_phase_edit = QLineEdit("180")
        self.fb_pulse_phase_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fb_pulse_phase_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_phase_shift_edit = QLineEdit("0")
        self.fb_phase_shift_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fb_phase_shift_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_toggle = PyToggle(animation_curve=QEasingCurve.Type.InOutQuint)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode4_groupBox_layout.addWidget(self.fb_comboBox, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_freq_edit, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_pos_duty_edit, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_neg_duty_edit, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_pulse_phase_edit, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_phase_shift_edit, 1, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode4_groupBox_layout.addWidget(self.fb_toggle, 1, 6, Qt.AlignmentFlag.AlignCenter)
        # ------------------------------------------------------------------------------------------------------------ #
        # ACTIONS
        self.fb_toggle.stateChanged.connect(self.fb_toggled)
        self.fb_freq_edit.returnPressed.connect(self.fb_set)
        self.fb_pos_duty_edit.returnPressed.connect(self.fb_set)
        self.fb_neg_duty_edit.returnPressed.connect(self.fb_set)
        self.fb_pulse_phase_edit.returnPressed.connect(self.fb_set)
        self.fb_phase_shift_edit.returnPressed.connect(self.fb_set)

        self.mode4_layout.addStretch(1)

    ####################################################################################################################
    # ATTACH SERIAL
    def attach_serial(self, serial):
        self.fb_ser = serial

    ####################################################################################################################
    # CHECKBOX TOGGLED
    def fb_toggled(self):
        if self.fb_toggle.isChecked() == 1:
            self.fb_set()
        else:
            self.fb_stop()

    ####################################################################################################################
    # TOGGLE CLICKED = SET STATE
    def fb_set(self):
        try:
            channel_val = 0
            fb_val = int(self.fb_comboBox.currentIndex())+1
            for exponent in range(fb_val):
                channel_val += pow(2, exponent)
            freq_val = float(self.fb_freq_edit.text())
            pos_duty_val = int(self.fb_pos_duty_edit.text())
            neg_duty_val = int(self.fb_neg_duty_edit.text())
            pulse_phase_val = int(self.fb_pulse_phase_edit.text())
            phase_shift_val = int(self.fb_phase_shift_edit.text())
            # check frequency/duty cycle value
            pos_pulse_width = float(10*(pos_duty_val/freq_val))
            neg_pulse_width = float(10*(pos_duty_val/freq_val))
            if pos_pulse_width < 2:
                self.fb_stop()
                print("[ERR] Positive pulse width: {} ms < 2 ms".format(pos_pulse_width))
            if neg_pulse_width < 2:
                self.fb_stop()
                print("[ERR] Negative pulse width: {} ms < 2 ms".format(neg_pulse_width))
            else:
                if (freq_val >= f_min) and (freq_val <= f_max):
                    # change the state of toggle
                    self.fb_toggle_on()
                    # send through the serial port
                    to_send = "\r\nSM4 {} {} {} {} {} {}\r\n".format(channel_val, freq_val, pos_duty_val, neg_duty_val,
                                                                     pulse_phase_val, phase_shift_val)
                    print("[CMD]  {} ".format(to_send))
                    send_command(self.fb_ser, to_send)
                    # display information message
                    print("[INFO] Mode 4 ON ({}Hz | {}% | {}% | {}° | {}°)".format(freq_val, pos_duty_val, neg_duty_val,
                                                                                   pulse_phase_val, phase_shift_val))
                else:
                    self.fb_stop()
        except Exception as err_fb_freq_edit:
            # display error message
            print("[ERR] FB FREQ VAL: {} - {}".format(self.fb_freq_edit.text(), err_fb_freq_edit))
        return

    ####################################################################################################################
    # TOGGLE NOT CLICKED = STOP STATE
    def fb_stop(self):
        # change the state of toggle
        self.fb_toggle_off()
        # send through the serial port
        to_send = "\r\nCM4 0\r\n"
        send_command(self.fb_ser, to_send)
        # display information message
        print("[INFO]  Mode 4 OFF")

    ####################################################################################################################
    def fb_toggle_on(self):
        self.fb_toggle.setChecked(True)
        self.fb_toggle.start_transition(1)

    ####################################################################################################################
    def fb_toggle_off(self):
        self.fb_toggle.setChecked(False)
        self.fb_toggle.start_transition(0)
