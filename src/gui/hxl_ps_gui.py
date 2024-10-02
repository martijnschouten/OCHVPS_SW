########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\gui\hxl_ps_gui.py
# @brief      Author:             MBE
#             Software version:   v1.09
#             Created on:         12.02.2024
#             Last modifications: 18.03.2024
#
# OC_HVPS © 2021-2024 by MBE
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
from os.path import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
# custom packages

import os
import sys
#add path to source
print(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import time
# while(True):
#     time.sleep(1)

from src.Userdef import *
from src.gui.hxl_ps_widget import HaxelPowerSupplyWidget


########################################################################################################################
def resource_path(relative_path):
    """
    Method that get the correct path for icon and other dependencies of the program as
    a function of whether it is frozen in an executable package.
    :param relative_path: Relative path of the resource
    :return: Absolute path of the resource
    """
    if getattr(sys, 'frozen', False):
        return join(dirname(sys.executable), relative_path)
    return join(abspath('cmd'), relative_path)


########################################################################################################################
class HaxelPowerSupplyInterface(QWidget):
    def __init__(self):
        super().__init__()

        # ------------------------------------------------------------------------------------------------------------ #
        # create main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ------------------------------------------------------------------------------------------------------------ #
        # add HVPS widget to main layout
        self.hvps = HaxelPowerSupplyWidget()
        layout.addWidget(self.hvps)
        layout.addStretch(1)

        # ------------------------------------------------------------------------------------------------------------ #
        # set main windows
        self.setGeometry(0, 0, 10, 10)
        self.setWindowTitle(f"{PROGRAM_NAME} - {PROGRAM_VERSION}")
        self.show()

    # **************************************************************************************************************** #
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Window Close", "Are you sure you want to close the window?")

        if reply == QMessageBox.StandardButton.Yes:
            self.hvps.stop_com()
            event.accept()

        else:
            event.ignore()


########################################################################################################################
def main():
    app = QApplication(sys.argv)
    app.setApplicationName(PROGRAM_NAME)
    app.setWindowIcon(QIcon('epfl_icon.ico'))

    window = HaxelPowerSupplyInterface()
    window.show()

    app.exec()


########################################################################################################################
if __name__ == '__main__':
    main()
