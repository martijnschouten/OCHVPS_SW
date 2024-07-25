########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_modes\old_mode_5.py
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
import time


class OldMode5(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.hb_ser = None

        # ************************************************************************************************************ #
        self.mode3_groupBox = QGroupBox("Multiple outputs in Unipolar")
        self.mode3_groupBox.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.mode3_groupBox.setFixedWidth(680)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode3_layout = QVBoxLayout(self)
        self.mode3_layout.addWidget(self.mode3_groupBox)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode3_groupBox_layout = QGridLayout(self.mode3_groupBox)
        self.mode3_groupBox_layout.setHorizontalSpacing(25)
        # self.mode3_groupBox_layout.setColumnMinimumWidth(80, 80)
        self.mode3_groupBox.setLayout(self.mode3_groupBox_layout)
        # ************************************************************************************************************ #
        # TITLES LINE (only labels)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_number_label = QLabel("Nb Output")
        # self.fb_freq_label.setAlignment(Qt.AlignLeft)
        self.hb_number_label.setFixedWidth(80)
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
        self.hb_on_off_label = QLabel("State")
        self.hb_on_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hb_on_off_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode3_groupBox_layout.addWidget(self.hb_number_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_freq_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_pos_duty_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_neg_duty_label, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_pulse_phase_label, 0, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_phase_shift_label, 0, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_on_off_label, 0, 6, Qt.AlignmentFlag.AlignCenter)
        # ************************************************************************************************************ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)
        # ------------------------------------------------------------------------------------------------------------ #
        # list in the combobox all available options for phase shift
        self.hb_comboBox = QComboBox()
        self.hb_comboBox.addItem('1')
        self.hb_comboBox.addItem('2')
        self.hb_comboBox.addItem('3')
        self.hb_comboBox.addItem('4')
        self.hb_comboBox.addItem('5')
        self.hb_comboBox.addItem('6')
        self.hb_comboBox.addItem('7')
        self.hb_comboBox.addItem('8')
        self.hb_comboBox.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_freq_edit = QLineEdit("1")
        self.hb_freq_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hb_freq_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.hb_pos_duty_edit = QLineEdit("50")
        self.hb_pos_duty_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hb_pos_duty_edit.setFixedWidth(80)
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
        self.hb_phase_shift_edit = QLineEdit("-")
        self.hb_phase_shift_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hb_phase_shift_edit.setFixedWidth(80)
        self.hb_phase_shift_edit.setEnabled(False)
        # ------------------------------------------------------------------------------------------------------------ #
        self.change_btn = QPushButton("SET")
        self.change_btn.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.mode3_groupBox_layout.addWidget(self.hb_comboBox, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_freq_edit, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_pos_duty_edit, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_neg_duty_edit, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_pulse_phase_edit, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.hb_phase_shift_edit, 1, 5, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.change_btn, 1, 6, Qt.AlignmentFlag.AlignCenter)
        # ------------------------------------------------------------------------------------------------------------ #
        self.t_switch_label = QLabel("Time (s)")
        # self.fb_duty_label.setAlignment(Qt.AlignLeft)
        self.t_switch_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.t_switch_edit = QLineEdit("1")
        self.t_switch_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.t_switch_edit.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.sequence_time_label = QLabel("Sequences")
        # self.fb_duty_label.setAlignment(Qt.AlignLeft)
        self.sequence_time_label.setFixedWidth(80)
        # ------------------------------------------------------------------------------------------------------------ #
        self.sequence_time_edit = QLineEdit("1")
        self.sequence_time_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.sequence_time_edit.setFixedWidth(80)

        # ------------------------------------------------------------------------------------------------------------ #
        self.mode3_groupBox_layout.addWidget(self.t_switch_label, 2, 0, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.t_switch_edit, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.sequence_time_label, 2, 2, Qt.AlignmentFlag.AlignCenter)
        self.mode3_groupBox_layout.addWidget(self.sequence_time_edit, 2, 3, Qt.AlignmentFlag.AlignCenter)
        # ------------------------------------------------------------------------------------------------------------ #
        # ACTIONS
        self.change_btn.clicked.connect(self.hb_set)
        self.mode3_layout.addStretch(1)

    ####################################################################################################################
    # ATTACH SERIAL
    def attach_serial(self, serial):
        self.hb_ser = serial

    ####################################################################################################################
    # TOGGLE CLICKED = SET STATE
    def hb_set(self):
        try:
            channel_val = 0
            hb_val = int(self.hb_comboBox.currentIndex())+1
            for exponent in range(hb_val):
                channel_val += pow(2, exponent)
            freq_val = float(self.hb_freq_edit.text())
            pos_duty_val = float(self.hb_pos_duty_edit.text())
            t_switch_val = float(self.t_switch_edit.text())
            sequence_time_total_val = int(self.sequence_time_edit.text())
            # check frequency/duty cycle value
            pos_pulse_width = float(10*(pos_duty_val/freq_val))
            if pos_pulse_width < 2:
                print("[ERR] Positive pulse width: {} ms < 2 ms".format(pos_pulse_width))
            else:
                # check frequency value
                if (freq_val >= f_min) and (freq_val <= f_max):
                    # display information message
                    print("[INFO] Mode 5 ON")
                    # self.chx_set_state_label_on()
                    for sequence in range(sequence_time_total_val):
                        # send through the serial port
                        to_send = "\r\nSM3 {} {} {} 120 \r\n".format(channel_val, freq_val, pos_duty_val)
                        send_command(self.hb_ser, to_send)
                        # wait....
                        time.sleep(t_switch_val)
                        # send through the serial port
                        to_send = "\r\nSM3 {} {} {} 240 \r\n".format(channel_val, freq_val, pos_duty_val)
                        send_command(self.hb_ser, to_send)
                        # wait....
                        time.sleep(t_switch_val)

                    # send through the serial port
                    to_send = "\r\nCM3 0\r\n"
                    send_command(self.hb_ser, to_send)
                    # display information message
                    print("[INFO] Mode 5 OFF")
                else:
                    print("[ERR] Frequency value:  {}".format(freq_val))
        except Exception as err_fb_freq_edit:
            # display error message
            print("[ERR] FB FREQ VAL: {} - {}".format(self.hb_freq_edit.text(), err_fb_freq_edit))
        return

