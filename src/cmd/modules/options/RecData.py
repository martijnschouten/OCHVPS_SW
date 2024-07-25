########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\cmd\modules\options\RecData.py
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
from datetime import *
from pathlib import *
# custom packages
#from Userdef import *


########################################################################################################################
class RecData:
    def __init__(self, pcb_prm=None, settings=None, seq=None):

        folder = Path("logs")
        folder.mkdir(parents=True, exist_ok=True)

        self.pcb_prm = pcb_prm
        self.settings = settings
        self.seq = seq

        if self.settings['id_board'] == 1:
            com_port = self.settings['port_#01']
        else:
            com_port = self.settings['port_#02']

        if self.seq:
            print("[INFO] Recording sequential data.")
            timestring = datetime.now().strftime("%Y%m%d-%Hh%M.%S")
            self.filename = folder.joinpath(f"HXL_PS_v1.0_log_seq_%s.csv"%(timestring))
        else:
            print("[INFO] Recording data.")
            timestring = datetime.now().strftime("%Y%m%d-%Hh%M.%S")
            self.filename = folder.joinpath(f"HXL_PS_v1.0_log_%s.csv"%(timestring))

        self.file = open(self.filename, 'w')
        self.file.write("Data recorded by HXL PS GUI beta version\r\n")
        timestring = datetime.now().strftime("%Y %m %d - %H:%M:%S")
        self.file.write(f"Date, %s\r\n"%(timestring))
        self.file.write(",Name,Version\n")
        self.file.write(f"Interface,{PROGRAM_NAME},{PROGRAM_VERSION}\n")
        self.file.write(f"Board,{self.pcb_prm['name']},{self.pcb_prm['hw_ver']}\n")
        self.file.write(f"Port,{com_port}\r\n")
        self.file.write("time, [dbg], timestamp[ms], HV target [V], LV target [V], LV VM [V], HV VM [V], HV_CM [uA], "
                        "HB_CM_CH1 [uA], HB_CM_CH2 [uA], HB_CM_CH3 [uA], HB_CM_CH4 [uA], "
                        "HB_CM_CH5 [uA], HB_CM_CH6 [uA], HB_CM_CH7 [uA], HB_CM_CH8 [uA]\r\n")

    # **************************************************************************************************************** #
    def save_data(self, line):
        """
        Save data
        """
        timestring = datetime.now().strftime("%H:%M:%S:%f")
        self.file.write(f"%s, %s"%(timestring, line))

    # **************************************************************************************************************** #
    def close_record(self):
        """
        Stop record by closing file and displaying an information message
        """
        self.file.close()

        if self.settings['debug'] and not self.seq:
            timestring = datetime.now().strftime("%Y %m %d - %H:%M:%S")
            print(f"[INFO] Date/time when closing: %s"%(timestring))
            print(f"[INFO] Data saved to: {self.filename}")
        elif self.settings['debug'] and self.seq:
            print(f"[INFO] Sequential data saved to: {self.filename}")
        return
