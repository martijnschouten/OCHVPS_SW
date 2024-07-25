########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\modes\mode_2_widget.py
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
class Mode2Widget(QWidget):
    def __init__(self, parent=None, nb_fb=0, com=None, pcb_prm=None):
        super().__init__(parent)

        self.nb_fb = nb_fb

        self.Mode2_Cmd = Mode2Cmd(nb_fb=self.nb_fb, com=com, pcb_prm=pcb_prm)

        self.fb_toggle = []
        self.fb_widgets = []

    # **************************************************************************************************************** #
    def setup_vi(self):
        """
        Create module vi
        """

        # ------------------------------------------------------------------------------------------------------------ #
        group_box = QGroupBox("Bipolar switching")
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

        for row in range(self.nb_fb):
            fb_id = row + 1
            widgets = []
            widget_text = [f"Full-Bridge {fb_id}", "1", "50", "50", "180", "-", ]
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
                    widget.returnPressed.connect(lambda row_id=row: self.fb_toggle_set(row=row_id))

                widget.setFixedWidth(80)
                grid_layout.addWidget(widget, row + 1, col, alignment=Qt.AlignmentFlag.AlignCenter)
                widgets.append(widget)

            self.fb_widgets.append(widgets)

            self.fb_toggle.append(PyToggle(animation_curve=QEasingCurve.Type.InOutQuint))
            self.fb_toggle[row].clicked.connect(lambda _unused_, row_id=row: self.fb_toggled(row=row_id))
            grid_layout.addWidget(self.fb_toggle[row], fb_id, 6, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        # STOP ALL CHANNELS BUTTON

        fb_stop_btn = QPushButton("Stop all")
        fb_stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; position: center; "
                                  "border: 1px solid black;")
        fb_stop_btn.setFixedSize(75, 25)
        fb_stop_btn.clicked.connect(self.fb_stop_all_clicked)
        grid_layout.addWidget(fb_stop_btn, (self.nb_fb + 1), 6, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        layout.addStretch(1)

    # **************************************************************************************************************** #
    # CHECKBOX TOGGLED
    def fb_toggled(self, row):
        """
        Check new status of specific channel toggle
        """
        if self.fb_toggle[row].isChecked():
            self.fb_toggle_set(row)
        else:
            self.fb_toggle_stop(row)

    # **************************************************************************************************************** #
    def fb_stop_all_clicked(self):
        """
        Deactivate all channel and change state of all toggles
        """
        if self.Mode2_Cmd.stop_all():
            for row in range(self.nb_fb):
                self.fb_toggle_off(row)

    # **************************************************************************************************************** #
    def fb_toggle_set(self, row):
        """
        Get switching parameters chosen by the user, check if it matches to board parameters
        Change state of matching toggle
        """
        # get values
        freq = float(self.fb_widgets[row][1].text())
        pos_duty = float(self.fb_widgets[row][2].text())
        neg_duty = float(self.fb_widgets[row][3].text())
        pulse_phase = float(self.fb_widgets[row][4].text())

        if self.Mode2_Cmd.start(row, freq, pos_duty, neg_duty, pulse_phase):
            # change the state of the checkbox
            self.fb_toggle_on(row)
        else:
            self.fb_toggle_off(row)

    # **************************************************************************************************************** #
    # BTN CLICKED (STOP STATE)
    def fb_toggle_stop(self, row):
        """
        Stop switching on specific channel and change state of matching toggle
        """
        if self.Mode2_Cmd.stop(row):
            # change the state of the checkbox
            self.fb_toggle_off(row)

    # **************************************************************************************************************** #
    def fb_toggle_on(self, row):
        """
        Change specific channel toggle to indicate when channel is activated
        """
        self.fb_toggle[row].setChecked(True)
        self.fb_toggle[row].start_transition(1)

    # **************************************************************************************************************** #
    def fb_toggle_off(self, row):
        """
        Change specific channel toggle to indicate when channel is disabled
        """
        self.fb_toggle[row].setChecked(False)
        self.fb_toggle[row].start_transition(0)
