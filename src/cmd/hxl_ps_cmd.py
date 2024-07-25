########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\cmd\hxl_ps_cmd.py
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
import time
# custom packages
from src.cmd.modules.hxl_ps import HaxelPowerSupply
from src.cmd.modules.options import *


########################################################################################################################
class HaxelPowerSupplyCmd:
    def __init__(self, settings=None):

        self.boards = {}
        self.seq_rec = {}
        self.settings = settings
        self.seq_rec_state = False

    # **************************************************************************************************************** #
    # COM SELECT MODULE
    def connect(self):
        """
        Creation of HaxelPowerSupply depending on the number of boards selected by user and connection
        """
        for x in range(self.settings['nb_board']):
            self.settings['id_board'] = x + 1
            self.boards[x] = HaxelPowerSupply(settings=self.settings)

    def try_reconnect(self):
        """
        """
        for x in range(self.settings['nb_board']):
            self.boards[x].com.try_reconnect()

    # -----------------------------------------------------------------------------------------------------------------#
    def disconnect(self):
        """
        Closes connection with the HVPS
        """
        for x in range(self.settings['nb_board']):
            if self.seq_rec_state:
                self.seq_rec[x].close_record()
            self.boards[x].stop_comm()

    ####################################################################################################################
    # COM MODULE
    def get_parameters(self, id_board):
        parameters = self.boards[id_board - 1].pcb_prm
        return parameters

    def get_monitoring(self, id_board):
        return self.boards[id_board-1].read_monitoring()

    ####################################################################################################################
    # MODE 1 MODULE
    def mode1_start(self, id_board, channel, freq, pos_duty):
        """
        Check switching parameters, for one or multiple channels, chosen by the user with board parameters.
        Set mode by sending the appropriate command through the serial port and displaying an information message.

        Parameters:
            id_board    =
            channel     = channel number value on 8 bits
            freq        = switching frequency
            pos_duty    = duty cycle value for positive width
        """
        self.boards[id_board - 1].Mode1.start(channel - 1, freq, pos_duty)

    def mode1_stop(self, id_board, channel):
        """
        Stop switching on one or multiple channels.
        Clear mode by sending the appropriate command through serial port and displaying an information message.

        Parameters:
            channel     = channel number value on 8 bits
        """
        self.boards[id_board - 1].Mode1.stop(channel - 1)

    def mode1_stop_all(self, id_board):
        """
        Stop switching on all channels by sending the appropriate command through serial port and displaying an
        information message.
        """
        self.boards[id_board - 1].Mode1.stop_all()

    ####################################################################################################################
    # MODE 2 MODULE
    def mode2_start(self, id_board, channel, freq, pos_duty, neg_duty, pulse_phase):
        """
        Check switching parameters, for one or multiple channels, chosen by the user with board parameters.
        Set mode by sending the appropriate command through the serial port and displaying an information message.

        Parameters:
            channel     = channel number value on 4 bits
            freq        = switching frequency
            pos_duty    = duty cycle value for positive width
            neg_duty    = duty cycle value for negative width
            pulse_phase = phase between positive and negative pulse of a full-bridge
        """
        self.boards[id_board - 1].Mode2.start(channel - 1, freq, pos_duty, neg_duty, pulse_phase)

    def mode2_stop(self, id_board, channel):
        """
        Stop switching on one or multiple channels.
        Clear mode by sending the appropriate command through serial port and displaying an information message.

        Parameters:
            channel     = channel number value on 4 bits
        """
        self.boards[id_board - 1].Mode2.stop(channel - 1)

    def mode2_stop_all(self, id_board):
        """
        Stop switching on all channels.
        Clear mode by sending the appropriate command through serial port and displaying an information message.
        """
        self.boards[id_board - 1].Mode2.stop_all()

    ####################################################################################################################
    # MODE 3 MODULE
    def mode3_start(self, id_board, nb_channel, freq, pos_duty, phase_shift):
        """
        Check switching parameters, for one or multiple channels, chosen by the user with board parameters.
        Set mode by sending the appropriate command through the serial port and displaying an information message.

        Parameters:
            channel     = channel number value on 8 bits
            freq        = switching frequency
            pos_duty    = duty cycle value for positive width
            phase_shift = phase between two channels
        """
        self.boards[id_board - 1].Mode3.start(nb_channel, freq, pos_duty, phase_shift)

    def mode3_stop(self, id_board):
        """
        Stop switching on all channels.
        Clear mode by sending the appropriate command through serial port and displaying an information message.
        """
        self.boards[id_board - 1].Mode3.stop()

    ####################################################################################################################
    # MODE 4 MODULE
    def mode4_start(self, id_board, nb_channel, freq, pos_duty, neg_duty, pulse_phase, phase_shift):
        """
        Check switching parameters, for one or multiple channels, chosen by the user with board parameters.
        Set mode by sending the appropriate command through the serial port and displaying an information message.

        Parameters:
            channel     = channel number value on 4 bits
            freq        = switching frequency
            pos_duty    = duty cycle value for positive width
            neg_duty    = duty cycle value for negative width
            pulse_phase = phase between positive and negative pulse of a full-bridge
            phase_shift = phase between two channels
        """
        self.boards[id_board - 1].Mode4.start(nb_channel, freq, pos_duty, neg_duty, pulse_phase, phase_shift)

    def mode4_stop(self, id_board):
        """
        Stop switching on all channels.
        Clear mode by sending the appropriate command through serial port and displaying an information message.
        """
        self.boards[id_board - 1].Mode4.stop()

    ####################################################################################################################
    # RECORD DATA MODULE
    def seq_rec_start(self, id_board):
        """
        Start sequential record
        """
        self.seq_rec[id_board - 1] = RecData(pcb_prm=self.boards[id_board - 1].pcb_prm, settings=self.settings,
                                             seq=True)
        self.seq_rec_state = True

    def seq_rec_stop(self, id_board):
        """
        Stop sequential record
        """
        self.seq_rec[id_board - 1].close_record()
        self.seq_rec_state = False

    ####################################################################################################################
    # VOLTAGE MODULE
    def set_voltage(self, id_board, voltage):
        """
        Check high voltage to the value chosen by user matches with high voltage range.
        Set it by sending the appropriate command through the serial port and displaying an information message
        """
        self.boards[id_board - 1].Voltage.set(voltage)

    def stop_voltage(self, id_board):
        """
        Stop high voltage by sending the appropriate command through the serial port and displaying an information
        message
        """
        self.boards[id_board - 1].Voltage.stop()

    def emergency_stop(self):
        """
        Stop all current tasks, by sending the appropriate command through the serial port and displaying an information
        message
        """
        for x in range(self.settings['nb_board']):
            self.boards[x].Voltage.emergency_stop()


########################################################################################################################
if __name__ == '__main__':
    test_pcb = HaxelPowerSupplyCmd({
        'nb_board': 1,
        'id_board': 0,
        'port_#01': r'\\.\COM4',
        'port_#02': '-',
        'debug': True,
        'record': True})

    test_pcb.connect()

    test_pcb.seq_rec_start(1)

    test_pcb.set_voltage(1, 1000)

    data = test_pcb.get_monitoring(1)
    print(f"data = {data}")

    test_pcb.mode4_start(1, 1, 10, 25, 25, 90, 0)

    time.sleep(2)

    test_pcb.mode4_stop(1)

    time.sleep(1)

    test_pcb.set_voltage(1, 2000)

    test_pcb.mode4_start(1, 2, 10, 50, 50, 180, 180)

    time.sleep(1)

    data = test_pcb.get_monitoring(1)
    print(f"data = {data}")

    test_pcb.mode4_stop(1)

    time.sleep(1)

    test_pcb.emergency_stop()

    test_pcb.disconnect()
