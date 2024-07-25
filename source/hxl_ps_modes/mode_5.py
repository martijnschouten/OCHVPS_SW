########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_modes\mode_5.py
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


class Mode5(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.hb_ser = None

        # ************************************************************************************************************ #
        self.mode5_groupBox = QGroupBox("Multiple outputs in Unipolar")
        self.mode5_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.mode5_groupBox.setFixedWidth(680)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode5_layout = QVBoxLayout(self)
        self.mode5_layout.addWidget(self.mode5_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode5_groupBox_layout = QGridLayout(self.mode5_groupBox)
        self.mode5_groupBox_layout.setHorizontalSpacing(25)
        # self.mode3_groupBox_layout.setColumnMinimumWidth(80, 80)
        self.mode5_groupBox.setLayout(self.mode5_groupBox_layout)
        # ************************************************************************************************************ #
        # TITLES LINE (only labels)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_number_label = QLabel("Nb Output")
        # self.fb_freq_label.setAlignment(Qt.AlignLeft)
        self.hb_number_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_freq_label = QLabel("Freq. Mod (Hz)")
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
        self.hb_phase_shift_label = QLabel("Freq. Seq (Hz)")
        # self.fb_phase_label.setAlignment(Qt.AlignLeft)
        self.hb_phase_shift_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_on_off_label = QLabel("ON/OFF")
        self.hb_on_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hb_on_off_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode5_groupBox_layout.addWidget(self.hb_number_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_freq_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_pos_duty_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_neg_duty_label, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_pulse_phase_label, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_phase_shift_label, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_on_off_label, 0, 6, Qt.AlignmentFlag.AlignCenter)
        # ************************************************************************************************************ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)
        # ------------------------------------------------------------------------------------------------------------ #
        # list in the combobox all available options for phase shift
        self.hb_comboBox = QComboBox()
        self.hb_comboBox.addItem('3')
        self.hb_comboBox.setFixedWidth(80)
        self.hb_comboBox.setEnabled(False)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_freq_edit = QLineEdit("50")
        self.hb_freq_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hb_freq_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_pos_duty_edit = QLineEdit("50")
        self.hb_pos_duty_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hb_pos_duty_edit.setFixedWidth(80)
        self.hb_pos_duty_edit.setEnabled(False)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_neg_duty_edit = QLineEdit("-")
        self.hb_neg_duty_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hb_neg_duty_edit.setFixedWidth(80)
        self.hb_neg_duty_edit.setEnabled(False)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_pulse_phase_edit = QLineEdit("-")
        self.hb_pulse_phase_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hb_pulse_phase_edit.setFixedWidth(80)
        self.hb_pulse_phase_edit.setEnabled(False)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_phase_shift_edit = QLineEdit("20")
        self.hb_phase_shift_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hb_phase_shift_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_toggle = PyToggle(animation_curve=QEasingCurve.Type.InOutQuint)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode5_groupBox_layout.addWidget(self.hb_comboBox, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_freq_edit, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_pos_duty_edit, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_neg_duty_edit, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_pulse_phase_edit, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_phase_shift_edit, 1, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode5_groupBox_layout.addWidget(self.hb_toggle, 1, 6, Qt.AlignmentFlag.AlignCenter)
        # ------------------------------------------------------------------------------------------------------------ #
        # ACTIONS
        self.hb_toggle.stateChanged.connect(self.hb_toggled)
        self.hb_freq_edit.returnPressed.connect(self.hb_set)
        self.hb_pos_duty_edit.returnPressed.connect(self.hb_set)
        self.hb_phase_shift_edit.returnPressed.connect(self.hb_set)
        self.mode5_layout.addStretch(1)

    ####################################################################################################################
    # ATTACH SERIAL
    def attach_serial(self, serial):
        self.hb_ser = serial

    ####################################################################################################################
    # CHECKBOX TOGGLED
    def hb_toggled(self):
        if self.hb_toggle.isChecked() == 1:
            self.hb_set()
        else:
            self.hb_stop()

    ####################################################################################################################
    # TOGGLE CLICKED = SET STATE
    def hb_set(self):
        try:

            freq_val = float(self.hb_freq_edit.text())
            seq_freq_val = float(self.hb_phase_shift_edit.text())
            # check frequency/duty cycle value
            pos_pulse_width = float(10*(50/freq_val))
            if pos_pulse_width < 2:
                self.hb_stop()
                print("[ERR] Positive pulse width: {} ms < 2 ms".format(pos_pulse_width))
            else:
                # check frequency value
                if (freq_val >= f_min) and (freq_val <= f_max):
                    # change the state of toggle
                    self.hb_toggle_on()
                    # send through the serial port
                    to_send = "\r\nSM5 7 {} {} \r\n".format(freq_val, seq_freq_val)
                    send_command(self.hb_ser, to_send)
                    # display information message
                    print("[INFO] Mode 5 ON (3 Phases | {}Hz | {}Hz)".format(freq_val, seq_freq_val))
                else:
                    self.hb_stop()
        except Exception as err_fb_freq_edit:
            # display error message
            print("[ERR] FB FREQ VAL: {} - {}".format(self.hb_freq_edit.text(), err_fb_freq_edit))
        return

    ####################################################################################################################
    # TOGGLE NOT CLICKED = STOP STATE
    def hb_stop(self):
        # change the state of toggle
        self.hb_toggle_off()
        # send through the serial port
        to_send = "\r\nCM5 0\r\n"
        send_command(self.hb_ser, to_send)
        # display information message
        print("[INFO] Mode 5 OFF")

    ####################################################################################################################
    def hb_toggle_on(self):
        self.hb_toggle.setChecked(True)
        self.hb_toggle.start_transition(1)

    ####################################################################################################################
    def hb_toggle_off(self):
        self.hb_toggle.setChecked(False)
        self.hb_toggle.start_transition(0)
