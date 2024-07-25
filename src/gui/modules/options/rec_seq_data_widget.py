########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\modules\options\rec_seq_data_widget.py
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
from src.cmd.modules.options import RecData


########################################################################################################################
class RecSeqDataWidget(QWidget):
    def __init__(self, parent=None, pcb_prm=None,  settings=None):

        QWidget.__init__(self, parent=parent)

        self.pcb_prm = pcb_prm
        self.settings = settings

        self.record_button = None

        self.rec_seq = None
        self.seq_rec_state = False

        self.setup_ui()

    # **************************************************************************************************************** #
    def setup_ui(self):
        """
        Create record vi
        """
        # ------------------------------------------------------------------------------------------------------------ #
        record_groupbox = QGroupBox("Record")
        record_groupbox.setStyleSheet('QGroupBox {font-weight: bold;}')
        record_groupbox.setFixedWidth(400)

        # ------------------------------------------------------------------------------------------------------------ #
        layout = QVBoxLayout(self)
        layout.addWidget(record_groupbox)

        # ------------------------------------------------------------------------------------------------------------ #
        record_groupbox_layout = QVBoxLayout(record_groupbox)
        record_groupbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        record_groupbox.setLayout(record_groupbox_layout)

        # ------------------------------------------------------------------------------------------------------------ #
        self.record_button = QPushButton("START SEQ")
        self.record_button.setFixedWidth(300)
        self.record_button.setFixedHeight(50)
        record_groupbox_layout.addWidget(self.record_button)

        # ------------------------------------------------------------------------------------------------------------ #
        self.record_button.clicked.connect(self.record_seq_clicked)

    # **************************************************************************************************************** #
    def record_seq_clicked(self):
        """
        Start or stop sequential record
        """
        if not self.seq_rec_state:
            self.rec_seq = RecData(pcb_prm=self.pcb_prm, settings=self.settings, seq=True)
            self.record_button.setText("STOP SEQ")
            self.record_button.setStyleSheet('QPushButton {;color: red;}')
            self.seq_rec_state = True
        else:
            self.rec_seq.close_record()
            self.record_button.setText("START SEQ")
            self.record_button.setStyleSheet('QPushButton {color: black;}')
            self.seq_rec_state = False

    # **************************************************************************************************************** #
    def is_seq_recording_now(self, line):
        """
        Save data in case of sequential record
        """
        if self.seq_rec_state:
            self.rec_seq.save_data(line)
