########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\voltage\voltage_widget.py
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
from PyQt6.QtWidgets import *
# custom packages
from src.cmd.modules.voltage import *
from src.gui.modules.py_elements import *


########################################################################################################################
class VoltageWidget(QWidget):
    def __init__(self, parent=None, com=None, pcb_prm=None):
        super().__init__(parent=parent)

        self.Voltage_cmd = VoltageCmd(com=com, pcb_prm=pcb_prm)

        self.horizontal_layout = None
        self.hv_grid_layout = None

        self.hv_current_value_label = None
        self.hv_state_label = None
        self.hv_target_edit = None
        self.hv_toggle = None

        self.setup_ui()

    # **************************************************************************************************************** #
    def setup_ui(self):
        """
        Create main vi and attach high voltage controls vi and emergency stop vi
        """
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        voltage_groupbox = QGroupBox("High Voltage")
        voltage_groupbox.setStyleSheet('QGroupBox {font-weight: bold;}')
        voltage_groupbox.setFixedWidth(680)
        main_layout.addWidget(voltage_groupbox)

        self.horizontal_layout = QHBoxLayout(self)
        voltage_groupbox.setLayout(self.horizontal_layout)

        self.hv_grid_layout = QGridLayout(self)
        self.hv_grid_layout.setHorizontalSpacing(20)
        self.horizontal_layout.addLayout(self.hv_grid_layout)

        self.setup_hv_ui()
        self.setup_em_stop_ui()

    # **************************************************************************************************************** #
    def setup_hv_ui(self):
        """
        Create high voltage controls vi
        """
        hv_target_lbl = QLabel("Target:")
        hv_target_lbl.setFixedWidth(75)

        self.hv_target_edit = QLineEdit("0")
        self.hv_target_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hv_target_edit.setFixedWidth(75)
        self.hv_target_edit.returnPressed.connect(self.hv_toggle_set)

        self.hv_toggle = PyToggle(animation_curve=QEasingCurve.Type.InOutQuint)
        self.hv_toggle.clicked.connect(self.hv_toggled)

        hv_current_label = QLabel("Current:")
        hv_current_label.setFixedWidth(75)

        self.hv_current_value_label = QLabel("0")
        self.hv_current_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.hv_current_value_label.setFixedWidth(75)

        self.hv_state_label = QLabel("OFF")
        self.hv_label_off()
        self.hv_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hv_state_label.setFixedSize(75, 25)

        self.hv_grid_layout.addWidget(hv_target_lbl, 0, 0)
        self.hv_grid_layout.addWidget(self.hv_target_edit, 0, 1)
        self.hv_grid_layout.addWidget(self.hv_toggle, 0, 2)
        self.hv_grid_layout.addWidget(hv_current_label, 1, 0)
        self.hv_grid_layout.addWidget(self.hv_current_value_label, 1, 1)
        self.hv_grid_layout.addWidget(self.hv_state_label, 1, 2)

    # **************************************************************************************************************** #
    def setup_em_stop_ui(self):
        """
        Create emergency stop button vi
        """
        e_stop_layout = QVBoxLayout()
        emg_stop_btn = PyEmergencyStop('Stop')
        emg_stop_btn.setFixedWidth(350)
        emg_stop_btn.clicked.connect(self.emg_stop_clicked)
        e_stop_layout.addWidget(emg_stop_btn)
        self.horizontal_layout.addLayout(e_stop_layout)

    # **************************************************************************************************************** #
    def update_label(self, current_voltage):
        """
        Update label for high voltage value with new received value
        """
        self.hv_current_value_label.setText(f"{int(current_voltage)}")

        if current_voltage > 100:
            self.hv_label_on()
        else:
            self.hv_label_off()

    # **************************************************************************************************************** #
    def hv_toggled(self):
        """
        Check new status of high voltage toggle
        """
        if self.hv_toggle.isChecked():
            self.hv_toggle_set()
        else:
            self.hv_toggle_stop()

    # **************************************************************************************************************** #
    def emg_stop_clicked(self):
        """
        Stop all current tasks if this button is clicked and change state of high voltage toggle
        """
        if self.Voltage_cmd.emergency_stop():
            self.hv_toggle_off()

    # **************************************************************************************************************** #
    def hv_toggle_set(self):
        """
        Get high voltage value chosen by the user, check if it matches to high voltage range.
        Change state of high voltage toggle
        """
        new_hv_val = float(self.hv_target_edit.text())

        if self.Voltage_cmd.set(new_hv_val):
            self.hv_toggle_on()
        else:
            self.hv_toggle_stop()

    # **************************************************************************************************************** #
    def hv_toggle_stop(self):
        """
        Stop high voltage and change state of toggle
        """
        if self.Voltage_cmd.stop():
            self.hv_toggle_off()

    # **************************************************************************************************************** #
    def hv_toggle_on(self):
        """
        Change high voltage toggle to indicate when high voltage is activated
        """
        self.hv_toggle.setChecked(True)
        self.hv_toggle.start_transition(1)

    # **************************************************************************************************************** #
    def hv_toggle_off(self):
        """
        Change high voltage toggle to indicate when high voltage is disabled
        """
        self.hv_toggle.setChecked(False)
        self.hv_toggle.start_transition(0)

    # **************************************************************************************************************** #
    def hv_label_on(self):
        """
        Change voltage label to indicate when high voltage is on
        """
        self.hv_state_label.setText("ON")
        self.hv_state_label.setStyleSheet('background-color: green, color: white, position: center; '
                                          'border: 1px solid black;')

    # **************************************************************************************************************** #
    def hv_label_off(self):
        """
        Change voltage label to indicate when high voltage is off
        """
        self.hv_state_label.setText("OFF")
        self.hv_state_label.setStyleSheet('background-color: red, color: white, position: center; '
                                          'border: 1px solid black;')
