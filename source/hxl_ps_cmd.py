########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps_cmd.py
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


class HaxelPowerSupplyCmd:
    def __init__(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    ####################################################################################################################
    def get_board_version(self):
        pass

    ####################################################################################################################
    def set_voltage(self, voltage):
        pass

    def clear_voltage(self, voltage):
        pass

    ####################################################################################################################
    def set_half_bridge(self, fb_number, freq, duty):
        pass

    def clear_half_bridge(self, hb_number):
        pass

    ####################################################################################################################
    def set_full_bridge(self, fb_number, freq, duty):
        pass

    def clear_full_bridge(self, hb_number):
        pass

    ####################################################################################################################
    def get_monitoring(self, hb_number):
        pass