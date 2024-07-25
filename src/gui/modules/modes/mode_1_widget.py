########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\modes\mode_1_widget.py
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
from src.cmd.modules.modes import *
from src.gui.modules.py_elements import *


########################################################################################################################
class Mode1Widget(QWidget):
    def __init__(self, parent=None, nb_hb=0, com=None, pcb_prm=None):
        super().__init__(parent)

        self.nb_hb = nb_hb

        self.Mode1_Cmd = Mode1Cmd(nb_hb=self.nb_hb, com=com, pcb_prm=pcb_prm)

        self.hb_toggle = []
        self.hb_widgets = []

    # **************************************************************************************************************** #
    def setup_vi(self):
        """
        Create module vi
        """

        # ------------------------------------------------------------------------------------------------------------ #
        group_box = QGroupBox("DC or unipolar switching")
        group_box.setStyleSheet('QGroupBox {font-weight: bold;}')
        group_box.setFixedWidth(680)

        # ------------------------------------------------------------------------------------------------------------ #
        layout = QVBoxLayout(self)
        layout.addWidget(group_box)

        # ------------------------------------------------------------------------------------------------------------ #
        grid_layout = QGridLayout(group_box)
        grid_layout.setHorizontalSpacing(25)
        group_box.setLayout(grid_layout)

        # ------------------------------------------------------------------------------------------------------------ #
        # TITLES LINE

        titles = ["", "Frequency (Hz)", "PosDuty (%)", "NegDuty (%)", "Pulse Phase (°)", "Phase Shift (°)", "ON/OFF"]
        for i, title in enumerate(titles, start=0):
            label = QLabel(title)
            label.setFixedWidth(80)
            if title == "ON/OFF":
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_layout.addWidget(label, 0, i, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)

        for row in range(self.nb_hb):
            hb_id = row + 1
            widgets = []
            widget_text = [f"Half-Bridge {hb_id}", "1", "50", "-", "-", "-", ]
            for col, text in enumerate(widget_text, start=0):
                if col == 0:
                    widget = QLabel(text)
                    widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                elif text == '-':
                    widget = QLineEdit(text)
                    widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    widget.setEnabled(False)
                else:
                    widget = QLineEdit(text)
                    widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                    widget.returnPressed.connect(lambda row_id=row: self.hb_toggle_set(row=row_id))

                widget.setFixedWidth(80)
                grid_layout.addWidget(widget, row + 1, col, alignment=Qt.AlignmentFlag.AlignCenter)
                widgets.append(widget)

            self.hb_widgets.append(widgets)

            self.hb_toggle.append(PyToggle(animation_curve=QEasingCurve.Type.InOutQuint))
            self.hb_toggle[row].clicked.connect(lambda _unused_, row_id=row: self.hb_toggled(row=row_id))
            grid_layout.addWidget(self.hb_toggle[row], hb_id, 6, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        # STOP ALL CHANNELS BUTTON

        hb_stop_btn = QPushButton("Stop all")
        hb_stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; position: center; "
                                  "border: 1px solid black;")
        hb_stop_btn.setFixedSize(75, 25)
        hb_stop_btn.clicked.connect(self.hb_stop_all_clicked)  # stop target voltage
        grid_layout.addWidget(hb_stop_btn, (self.nb_hb + 1), 6, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        layout.addStretch(1)

    # **************************************************************************************************************** #
    def hb_toggled(self, row):
        """
        Check new status of specific channel toggle.
        """
        if self.hb_toggle[row].isChecked():
            self.hb_toggle_set(row)
        else:
            self.hb_toggle_stop(row)

    # **************************************************************************************************************** #
    def hb_stop_all_clicked(self):
        """
        Deactivate all channel and change state of all toggles.
        """
        if self.Mode1_Cmd.stop_all():
            for row in range(self.nb_hb):
                self.hb_toggle_off(row)

    # **************************************************************************************************************** #
    def hb_toggle_set(self, row):
        """
        Get switching parameters chosen by the user, check if it matches to board parameters.
        Change state of matching toggle
        """
        freq = float(self.hb_widgets[row][1].text())
        pos_duty = int(self.hb_widgets[row][2].text())

        if self.Mode1_Cmd.start(row, freq, pos_duty):
            self.hb_toggle_on(row)
        else:
            self.hb_toggle_off(row)

    # **************************************************************************************************************** #
    def hb_toggle_stop(self, row):
        """
        Stop switching on specific channel and change state of matching toggle.
        """
        if self.Mode1_Cmd.stop(row):
            self.hb_toggle_off(row)

    # **************************************************************************************************************** #
    def hb_toggle_on(self, row):
        """
        Change specific channel toggle state to indicate when channel is activated.
        """
        self.hb_toggle[row].setChecked(True)
        self.hb_toggle[row].start_transition(1)

    # **************************************************************************************************************** #
    def hb_toggle_off(self, row):
        """
        Change specific channel toggle state to indicate when channel is disabled.
        """
        self.hb_toggle[row].setChecked(False)
        self.hb_toggle[row].start_transition(0)
