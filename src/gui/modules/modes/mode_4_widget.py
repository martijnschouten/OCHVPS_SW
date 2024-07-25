########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\modes\mode_4_widget.py
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
class Mode4Widget(QWidget):
    def __init__(self, parent=None, nb_fb=0, com=None, pcb_prm=None):
        super().__init__(parent)

        self.nb_fb = nb_fb

        self.Mode4_Cmd = Mode4Cmd(nb_fb=self.nb_fb, com=com, pcb_prm=pcb_prm)

        self.fb_toggle = None
        self.fb_widgets = []

    # **************************************************************************************************************** #
    def setup_vi(self):
        """
        Create module vi
        """

        # ------------------------------------------------------------------------------------------------------------ #
        group_box = QGroupBox("Bipolar switching in simultaneous")
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
        # TITLES LINE (only labels)

        titles = ["Nb Output", "Frequency (Hz)", "PosDuty (%)", "NegDuty (%)", "Pulse Phase (°)", "Phase Shift (°)",
                  "ON/OFF"]
        for i, title in enumerate(titles, start=0):
            label = QLabel(title)
            label.setFixedWidth(80)
            if title == "ON/OFF":
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_layout.addWidget(label, 0, i, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        # PARAMETERS LINE (LineEdit + ComboBox + PyToggle)

        widget_text = [f"", "1", "50", "50", "180", "0", ]

        for col, text in enumerate(widget_text, start=0):
            if col == 0:
                widget = QComboBox(self)
                widget.addItems(('1', '2', '3', '4'))
            else:
                widget = QLineEdit(text)
                widget.setAlignment(Qt.AlignmentFlag.AlignRight)
                widget.returnPressed.connect(self.fb_toggle_set)

            widget.setFixedWidth(80)
            grid_layout.addWidget(widget, 1, col, alignment=Qt.AlignmentFlag.AlignCenter)
            self.fb_widgets.append(widget)

        # ------------------------------------------------------------------------------------------------------------ #
        self.fb_toggle = PyToggle(animation_curve=QEasingCurve.Type.InOutQuint)
        self.fb_toggle.clicked.connect(self.fb_toggled)
        grid_layout.addWidget(self.fb_toggle, 1, 6, Qt.AlignmentFlag.AlignCenter)

        # ------------------------------------------------------------------------------------------------------------ #
        layout.addStretch(1)

    # **************************************************************************************************************** #
    def fb_toggled(self):
        """
        Check new status of toggle
        """
        if self.fb_toggle.isChecked():
            self.fb_toggle_set()
        else:
            self.fb_toggle_stop()

    # **************************************************************************************************************** #
    def fb_toggle_set(self):
        """
        Get switching parameters chosen by the user, check if it matches to board parameters.
        Change state of toggle
        """
        # get values
        nb_channel = int(self.fb_widgets[0].currentIndex()) + 1
        freq = float(self.fb_widgets[1].text())
        pos_duty = int(self.fb_widgets[2].text())
        neg_duty = int(self.fb_widgets[3].text())
        pulse_phase = int(self.fb_widgets[4].text())
        phase_shift = int(self.fb_widgets[5].text())

        if self.Mode4_Cmd.start(nb_channel, freq, pos_duty, neg_duty, pulse_phase, phase_shift):
            self.fb_toggle_on()
        else:
            self.fb_toggle_off()

    # **************************************************************************************************************** #
    def fb_toggle_stop(self):
        """
        Stop switching on channel(s) and change state of toggle
        """
        if self.Mode4_Cmd.stop():
            self.fb_toggle_off()

    # **************************************************************************************************************** #
    def fb_toggle_on(self):
        """
        Change toggle state to indicate when mode is activated.
        """
        self.fb_toggle.setChecked(True)
        self.fb_toggle.start_transition(1)

    # **************************************************************************************************************** #
    def fb_toggle_off(self):
        """
        Change toggle state to indicate when mode is disabled.
        """
        self.fb_toggle.setChecked(False)
        self.fb_toggle.start_transition(0)
