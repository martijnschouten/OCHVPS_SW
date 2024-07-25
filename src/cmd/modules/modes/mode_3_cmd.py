########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\cmd\modules\modes\mode_3_cmd.py
# @brief      Author:             MBE
#             Software version:   v1.09
#             Created on:         12.03.2024
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
from collections.abc import Iterable


########################################################################################################################
def _channel_to_channel_key(channel):
    """
    Encode the value of the selected channel.
    """
    if type(channel) is int:
        channel_key = pow(2, channel)
    elif isinstance(channel, Iterable):
        channel_key = sum(pow(2, r) for r in channel)
    else:
        print("[ERR] channel must be int or list")
        return False
    return channel_key


########################################################################################################################
class Mode3Cmd:
    def __init__(self, nb_hb=0, com=None, pcb_prm=None):

        self.nb_hb = nb_hb
        self.com = com
        self.pcb_prm = pcb_prm

    # **************************************************************************************************************** #
    def start(self, nb_channel, freq, pos_duty, phase_shift):
        """
        Check switching parameters, for one or multiple channels, chosen by the user with board parameters.
        Set mode by sending the appropriate command through the serial port and displaying an information message.

        Parameters:
            nb_channel  = number of channels on 8 bits
            freq        = switching frequency
            pos_duty    = duty cycle value for positive width
            phase_shift = phase between two channels
        """

        # ------------------------------------------------------------------------------------------------------------ #
        # get values
        channel_key = 0
        for exponent in range(nb_channel):
            channel_key += _channel_to_channel_key(exponent)

        # ------------------------------------------------------------------------------------------------------------ #
        # check frequency
        if not (self.pcb_prm['min_freq'] <= freq <= self.pcb_prm['max_freq']):
            print(f"[ERR] Frequency range: [{self.pcb_prm['min_freq']} - {self.pcb_prm['max_freq']}] Hz")
            return False

        # check duty cycle value
        pos_pulse_width = float(10 * (pos_duty / freq) * 1000)
        if not (0 <= pos_duty <= 100):
            print(f"[ERR] Positive duty cycle range: [0 - 100] °")
            return False
        elif pos_pulse_width < self.pcb_prm['min_pulse']:
            print(f"[ERR] Positive pulse width: {pos_pulse_width} us < {self.pcb_prm['min_pulse']} us")
            return False

        # check phase shift value
        if not (0 <= phase_shift <= 360):
            print(f"[ERR] Phase shift range: [0 - 360] °")
            return False

        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = f"SMx 3 {channel_key} {freq} {pos_duty} 0 0 {phase_shift}\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()
            print(f"line: {line}")

            if line.startswith("[SM3]"):
                break
        # ------------------------------------------------------------------------------------------------------------ #
        # debug received message
        reply_message = line.replace("[SM3] ", "").replace("\r\n", "")

        # ------------------------------------------------------------------------------------------------------------ #
        # display information message
        if 'ON' in reply_message:
            print(f"[INFO] Mode 3 ON ({nb_channel} Channels | {freq}Hz | {pos_duty}% | {phase_shift}°)")
            return True
        else:
            print("[INFO] Start Mode 3 failed!")
            return False

    # **************************************************************************************************************** #
    def stop(self):
        """
        Stop switching on all channels.
        Clear mode by sending the appropriate command through serial port and displaying an information message.
        """
        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = "CMx 3 0\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()

            if line.startswith("[CM3]"):
                break

        # ------------------------------------------------------------------------------------------------------------ #
        # debug received message
        reply_message = line.replace("[CM3] ", "").replace("\r\n", "")

        # ------------------------------------------------------------------------------------------------------------ #
        # display information message
        if 'OFF' in reply_message:
            print("[INFO] Mode 3 OFF")
            return True
        else:
            print("[INFO] Stop Mode 3 failed!")
            return False
