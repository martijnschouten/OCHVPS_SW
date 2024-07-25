########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\cmd\modules\hxl_ps.py
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

# custom packages
from src.cmd.modules.modes import *
from src.cmd.modules.options import *
from src.cmd.modules.voltage import *
from src.cmd.modules.BoardCom import BoardCom

NB_FULL_BRIDGES = 4
NB_HALF_BRIDGES = 8


########################################################################################################################
class HaxelPowerSupply:
    def __init__(self, settings=None):

        self.settings = settings
        self.data = []

        # ------------------------------------------------------------------------------------------------------------ #
        # SERIAL COMMUNICATION
        self.com = BoardCom(settings=self.settings)
        # open serial port
        if self.com.connect():
            self.board_connected = True
        # read PCB parameters
        self.pcb_prm = self.com.get_parameters()

        # ------------------------------------------------------------------------------------------------------------ #
        # MODULES

        if "MF" not in self.pcb_prm['fw_ver']:
            self.Mode1 = Mode1Cmd(nb_hb=NB_HALF_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)
            self.Mode2 = Mode2Cmd(nb_fb=NB_FULL_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)
            self.Mode3 = Mode3Cmd(nb_hb=NB_HALF_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)
            self.Mode4 = Mode4Cmd(nb_fb=NB_FULL_BRIDGES, com=self.com, pcb_prm=self.pcb_prm)

        self.Voltage = VoltageCmd(com=self.com, pcb_prm=self.pcb_prm)

        # ------------------------------------------------------------------------------------------------------------ #
        # init file to record data
        if self.settings['record']:
            self.rec_data = RecData(pcb_prm=self.pcb_prm, settings=self.settings, seq=False)

    # **************************************************************************************************************** #
    def read_monitoring(self):
        """
        Read monitoring for each board
        # handle data
        # Remove units, spaces, split with coma
        # Refer to documentation of HVPS to assign data to fields
        """

        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = f"Moni 1\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()

            if line.startswith("[moni]"):
                break

        # ------------------------------------------------------------------------------------------------------------ #
        # handle data
        # Remove units, spaces, split with coma. Refer to documentation of HVPS to assign data to fields
        try:
            data_buf = (line.replace(" ", "").replace("uA", "").replace("V", "").replace("Hz", "").replace("\r\n", "")
                        .split(","))
            self.data = [float(x) for x in data_buf[2:15]]
        except Exception as conv_data_err:
            print(f"[ERR] Convert. data: {line} - {conv_data_err}")
            return False

        # save data to file
        if self.settings['record']:
            self.rec_data.save_data(line)

        # flush input if too much data not handled: avoid keeping very old values
        if self.com.ser.in_waiting > 200:
            # print(self.ser.in_waiting)
            self.com.ser.reset_input_buffer()

        return self.data

    # **************************************************************************************************************** #
    # RECONNECTION WITH BOARD
    def stop_comm(self):
        """
        Disable HV and monitoring and stop record
        """
        if self.com.disconnect():
            self.board_connected = False

            if self.settings['record']:
                self.settings['record'] = 0
                self.rec_data.close_record()

            print("[INFO] Program closed.")
