########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       SerialSender.py
# @brief      Author:             MBE
#             Institute:          EPFL
#             Laboratory:         LMTS
#             Software version:   v1.08 (SYLVAIN/MARTIJN)
#             Created on:         08.11.2023
#             Last modifications: 08.11.2023
#
# Copyright 2021/2023 EPFL-LMTS
# All rights reserved.
# NO HELP WILL BE GIVEN IF YOU MODIFY THIS CODE !!!
########################################################################################################################

def send_command(ser, command):
    to_send = bytearray(command, encoding="utf-8")
    ser.write(to_send)
    # print("[send] {}".format(command.replace("\r\n", "")))
