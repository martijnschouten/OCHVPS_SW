########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\cmd\modules\BoardCom.py
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
from serial import *
from threading import RLock
import sys


########################################################################################################################
def check_connection(func):
    """Decorator for checking connection and acquiring multithreading lock"""

    def is_connected_wrapper(*args):
        args[0].serial_com_lock.acquire()
        if args[0].ser.is_open:
            res = func(*args)
            args[0].serial_com_lock.release()
            return res
        else:
            print("HVPS not connected - not calling %s method" % func.__name__)
            args[0].serial_com_lock.release()
            return None

    is_connected_wrapper.__doc__ = func.__doc__
    return is_connected_wrapper


########################################################################################################################
class BoardCom:
    def __init__(self, settings=None):

        self.serial_com_lock = RLock()
        self.ser = None
        self.settings = settings
        # PCB parameters
        self.pcb_prm = {
            'name': '',
            'hw_ver': 0.0,
            'fw_ver': '',
            'max_hv': 0.0,
            'min_hv': 0.0,
            'max_freq': 0.0,
            'min_freq': 0.0,
            'min_pulse': 0.0,
        }

    # **************************************************************************************************************** #
    def connect(self):
        # open serial port
        try:
            if self.settings['id_board'] == 1:
                self.ser = Serial(self.settings['port_#01'], 115200, timeout=0.5)
            elif self.settings['id_board'] == 2:
                self.ser = Serial(self.settings['port_#02'], 115200, timeout=0.5)
            return True
        except Exception as err_com_port:
            print("[ERR.] Please make sure than you use the right COM port: {}".format(err_com_port))
            sys.exit(-1)

    # **************************************************************************************************************** #
    def try_reconnect(self):
        self.ser.close()
        try:
            self.ser.open()
            self.ser.reset_input_buffer()
            print("[INFO] reconnected to the board")
        except Exception as err_connection:
            print(f"[ERR] connection failed: {err_connection}")
            pass

    # **************************************************************************************************************** #
    def disconnect(self):
        """Closes connection with the HVPS"""
        self.write("\r\nEStop\r\n")

        self.ser.close()

        if self.settings['debug']:
            print("[INFO] Disconnected High voltage board")

        return True

    # **************************************************************************************************************** #
    @check_connection
    def read(self):
        try:
            line = self.ser.readline()
        except Exception as err_reading:
            self.try_reconnect()
            line = b""
            print(f"[ERR] reading HVPS failed: {err_reading}")
        return line.decode("utf-8")

    # **************************************************************************************************************** #
    @check_connection
    def write(self, cmd):
        try:
            if self.ser is not None:
                to_send = bytearray(cmd, encoding="utf-8")
                self.ser.write(to_send)
            else:
                print("[ERR] HXL PS not configured")
        except Exception as err_writing:
            self.try_reconnect()
            print(f"[ERR] send to HVPS failed: {err_writing}")

    # **************************************************************************************************************** #
    def get_parameters(self):
        # remove old data in input buffer
        self.ser.reset_input_buffer()

        to_send = "QPRM\r\n"
        self.write(to_send)

        patterns_and_keys = [
            ("[PRM] PCB \t\t ", "name"),
            ("[PRM] HW Version \t v", "hw_ver"),
            ("[PRM] FW Version \t ", "fw_ver"),
            ("[PRM] MAX HV    (V)\t ", "max_hv"),
            ("[PRM] MIN HV    (V)\t ", "min_hv"),
            ("[PRM] MAX FREQ  (Hz)\t ", "max_freq"),
            ("[PRM] MIN FREQ  (Hz)\t ", "min_freq"),
            ("[PRM] MIN PULSE (us)\t ", "min_pulse")
        ]

        for PRM, (pattern, key) in enumerate(patterns_and_keys):
            while 1:
                line = self.read()

                if line.startswith("[PRM]"):
                    break

            value = line.replace(pattern, "").replace("\n", "")

            # convert in float only for numeric values
            if key in ('hw_ver', 'max_hv', 'min_hv', 'max_freq', 'min_freq', 'min_pulse'):
                value = float(value)
            self.pcb_prm[key] = value

        # check compatibility between hardware/firmware and software
        if self.pcb_prm['hw_ver'] != 1.0:
            print("[ERR.] SOFTWARE NOT COMPATIBLE WITH BOARD {}!".format(self.pcb_prm['name']))
            print("Please to use another board!")
            sys.exit(-1)

        return self.pcb_prm
