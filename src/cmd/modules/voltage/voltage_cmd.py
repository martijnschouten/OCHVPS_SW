########################################################################################################################
# @project    HXL_PS_v1.0
# @file       src\cmd\modules\voltage\voltage.py
# @brief      Author:             MBE
#             Institute:          EPFL
#             Laboratory:         LMTS
#             Software version:   v1.09
#             Created on:         12.03.2024
#             Last modifications: 14.03.2024
#
# HXL_PS © 2021-2024 by MBE is licensed under CC BY-NC-ND 4.0
# NO HELP WILL BE GIVEN IF YOU MODIFY THIS CODE !!!
########################################################################################################################


class VoltageCmd:
    def __init__(self, com=None, pcb_prm=None):

        self.com = com
        self.pcb_prm = pcb_prm

    # **************************************************************************************************************** #
    def set(self, voltage):
        """
        Check high voltage to the value chosen by user matches with high voltage range.
        Set it by sending the appropriate command through the serial port and displaying an information message
        """
        # ------------------------------------------------------------------------------------------------------------ #
        # check value
        if not (self.pcb_prm['min_hv'] <= voltage <= self.pcb_prm['max_hv']):
            # display error message
            print(f"[ERR] High Voltage range [{self.pcb_prm['min_hv']};{self.pcb_prm['max_hv']}] V")
            return False

        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = f"SHV {voltage}\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()

            if line.startswith("[HV]"):
                break

        # ------------------------------------------------------------------------------------------------------------ #
        # debug received message
        new_hv_value = float(line.replace("[HV] ", "").replace("\r\n", ""))

        # ------------------------------------------------------------------------------------------------------------ #
        # display information message
        if new_hv_value == voltage:
            print(f"[INFO] HV ON: {voltage} V")
            return True
        else:
            print("[INFO] Start Mode 1 failed!")
            return False

    # **************************************************************************************************************** #
    def stop(self):
        """
        Stop high voltage by sending the appropriate command through the serial port and displaying an information
        message
        """

        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = "SHV 0\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()

            if line.startswith("[HV]"):
                break

        # ------------------------------------------------------------------------------------------------------------ #
        # debug received message
        new_hv_value = float(line.replace("[HV] ", "").replace("\r\n", ""))

        # ------------------------------------------------------------------------------------------------------------ #
        # display information message
        if new_hv_value == 0:
            print(f"[INFO] OFF")
            return True
        else:
            print("[INFO] Stop Mode 1 failed!")
            return False

    # **************************************************************************************************************** #
    def emergency_stop(self):
        """
        Stop all current tasks, by sending the appropriate command through the serial port and displaying an information
        message
        """
        # ------------------------------------------------------------------------------------------------------------ #
        # send through the serial port
        to_send = "EStop\r"
        self.com.write(to_send)

        # ------------------------------------------------------------------------------------------------------------ #
        # read from serial
        while 1:
            line = self.com.read()

            if line.startswith("[EStop]"):
                break

        # ------------------------------------------------------------------------------------------------------------ #
        # debug received message
        reply_message = line.replace("[EStop] ", "").replace("\r\n", "")

        # ------------------------------------------------------------------------------------------------------------ #
        # display information message
        if 'DONE' in reply_message:
            print("[INFO] Emergency stop")
            return True
        else:
            print("[INFO] Emergency stop failed!")
            return False
