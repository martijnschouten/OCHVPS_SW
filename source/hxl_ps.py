########################################################################################################################
# @project    EPFL-HXL_PS_v1.0
# @file       hxl_ps.py
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

# python packages
import numpy as np
from serial import *
import sys
# custom packages
from hxl_ps_plots import *
from hxl_ps_modes import *
from options import *
from StopReboot import *
from Voltage import *


class HaxelPowerSupply(QWidget):
    def __init__(self, parent=None, port_name=None, estimate_rate=None, currents_display=None, voltage_display=None,
                 debug_mode=None, rcv_data=None, record_data=None):

        QWidget.__init__(self, parent=parent)
        # ************************************************************************************************************ #
        self.port_name = port_name
        self.estimateRate = estimate_rate
        self.display_currents = currents_display
        self.display_voltages = voltage_display
        self.debug_mode = debug_mode
        self.rcv_data = rcv_data
        self.record_data = record_data
        # ************************************************************************************************************ #
        # MODULES
        self.em_stop = StopReboot()
        self.voltage = Voltage()
        self.Mode1 = Mode1()
        self.Mode2 = Mode2()
        self.Mode3 = Mode3()
        self.Mode4 = Mode4()
        self.OldMode5 = OldMode5()
        self.Mode5 = Mode5()
        # ------------------------------------------------------------------------------------------------------------ #
        # High Voltage monitor
        self.hv_vm = np.zeros(1000, dtype=float)
        self.hv_vm_now = []
        # ************************************************************************************************************ #
        # VOLTAGE PLOTS
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages != 0:
            # High Voltage plot
            self.hv_plots = VoltagePlots(plot_tittle="High Voltage Monitor", y_min=0, y_max=hv_vm_plot_max)
            # High Voltage set by user
            self.hv_set = np.zeros(1000, dtype=float)
            self.hv_set_now = []
            # High Voltage error
            self.hv_err = np.zeros(1000, dtype=float)
            self.hv_err_now = []
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages == 2:
            # Low Voltage plot
            self.lv_plots = VoltagePlots(plot_tittle="Low Voltage Monitor", y_min=0, y_max=lv_vm_plot_max)
            # Low Voltage set by user
            self.lv_set = np.zeros(1000, dtype=float)
            self.lv_set_now = []
            # Low Voltage monitor
            self.lv_vm = np.zeros(1000, dtype=float)
            self.lv_vm_now = []
            # High Voltage error
            self.lv_err = np.zeros(1000, dtype=float)
            self.lv_err_now = []
        # ************************************************************************************************************ #
        # CURRENTS PLOTS
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_currents != 0:
            self.fb_cm_plots = []
            self.hb_cm_plots = []
            self.cm_val = np.zeros([9, 1000], dtype=int)
            self.cm_val_now = ["", "", "", "", "", "", "", "", ""]
            self.y_name = ["HV CM"]
            for i in range(1, nbHalfBridges + 1):
                self.y_name.append("CH{} CM".format(i))
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_currents == 1:
            self.all_cm_plots = Current8Plots(plot_tittle="All Currents Monitor",
                                              y_name=self.y_name, y_min=0, y_max=5000)
        # ------------------------------------------------------------------------------------------------------------ #
        elif self.display_currents == 2:
            # self.ps_hv_cm_plots = Current1Plots(plot_tittle="DCDC Current Monitor",
            #                                     plot_name=self.y_name[0],
            #                                     plot_index=0, y_min=0, y_max=hb_cm_plot_max)
            # -------------------------------------------------------------------------------------------------------- #
            for FullBridge in range(nbFullBridges):
                y1_index = (2*FullBridge)+1
                y2_index = 2*(FullBridge+1)
                y_name_2 = [self.y_name[y1_index], self.y_name[y2_index]]
                self.fb_cm_plots.append(Current2Plots(plot_tittle="FB{} Current Monitor".format(FullBridge+1),
                                                      plot_name=y_name_2,
                                                      plot_index=FullBridge+1, y_min=0, y_max=hb_cm_plot_max))
        # ------------------------------------------------------------------------------------------------------------ #
        elif self.display_currents == 3:
            # self.ps_hv_cm_plots = Current1Plots(plot_tittle="DCDC Current Monitor",
            #                                     plot_name=self.y_name[0], plot_index=0, y_min=0, y_max=hb_cm_plot_max)
            # -------------------------------------------------------------------------------------------------------- #
            for HalfBridges in range(nbHalfBridges):
                self.hb_cm_plots.append(Current1Plots(plot_tittle="CH{} Current Monitor".format(HalfBridges+1),
                                                      plot_name=self.y_name[HalfBridges+1],
                                                      plot_index=HalfBridges+1, y_min=0, y_max=hb_cm_plot_max))
        # ************************************************************************************************************ #
        # FOR ANY PLOT (CURRENT OR VOLTAGE)
        if (self.display_currents != 0) or (self.display_voltages != 0):
            # init data arrays + time basis,...
            self.tplot = np.arange(-1000 * self.estimateRate, 0.0, self.estimateRate, dtype=float)
            self.t_save = np.zeros(1000, dtype=int)

        # ************************************************************************************************************ #
        # SERIAL COMMUNICATION
        # ------------------------------------------------------------------------------------------------------------ #
        # open serial port
        try:
            self.ser = Serial(self.port_name, 115200, timeout=0.5)
        except Exception as err_com_port:
            print("[ERR.] Please make sure than you use the right COM port: {}".format(err_com_port))
            sys.exit(-1)
        # ------------------------------------------------------------------------------------------------------------ #
        # remove old data in input buffer
        self.ser.flushInput()
        # ------------------------------------------------------------------------------------------------------------ #
        # Enable debug
        to_send = "QName\r\n"
        send_command(self.ser, to_send)
        # ------------------------------------------------------------------------------------------------------------ #
        # Connect widgets to serial port
        self.em_stop.attach_serial(serial=self.ser)
        self.voltage.attach_serial(serial=self.ser)

        if MODE1 == 1:
            self.Mode1.attach_serial(serial=self.ser)

        if MODE2 == 1:
            self.Mode2.attach_serial(serial=self.ser)

        if MODE3 == 1:
            self.Mode3.attach_serial(serial=self.ser)

        if MODE4 == 1:
            self.Mode4.attach_serial(serial=self.ser)

        if OLD_MODE5 == 1:
            self.OldMode5.attach_serial(serial=self.ser)

        if MODE5 == 1:
            self.Mode5.attach_serial(serial=self.ser)

        # ************************************************************************************************************ #
        # Read a first time to ensure connection (?)
        line = self.ser.readline()
        line = line.decode("utf-8")
        if line == "":
            print("[ERR.] no data received... ensure that the board has not been disconnected")
            sys.exit(-1)

        # read from serial
        try:
            line = self.ser.readline()
            line = line.decode("utf-8")
        except Exception as e:
            print("[ERR] unable to read line: {}".format(e))
            self.try_reconnect()
            return

        self.board_name = line.replace("[QName] ", "").replace("\n", "")
        # ------------------------------------------------------------------------------------------------------------ #
        # Enable debug
        to_send = "QVer\r\n"
        send_command(self.ser, to_send)

        for x in range(3):
            line = self.ser.readline()
            line = line.decode("utf-8")
            if line == "":
                print("[ERR.] no data received... ensure that the board has not been disconnected")
                sys.exit(-1)

        # read from serial
        try:
            line = self.ser.readline()
            line = line.decode("utf-8")
        except Exception as e:
            print("[ERR] unable to read line: {}".format(e))
            self.try_reconnect()
            return

        self.board_version = line.replace("[QVer] ", "").replace("\n", "")
        # ************************************************************************************************************ #
        # handle data
        # Remove units, spaces, split with coma
        # Refer to documentation of HVPS to assign data to fields

        self.rcv_data_label = QLabel("Received data: ND")
        self.data_recv_layout = QVBoxLayout()
        self.data_recv_layout.addWidget(self.rcv_data_label)

        # ************************************************************************************************************ #
        # init file to record data
        if self.record_data == 1:
            self.RecordData = RecordData(board_name=self.board_name,
                                         board_version=self.board_version,
                                         port_name=port_name,
                                         sequential=False)
            self.SequentialRecord = SequentialRecord(board_name=self.board_name,
                                                     board_version=self.board_version,
                                                     port_name=port_name)

    ####################################################################################################################
    # INITIALIZE HXL PS VI
    def init_vi(self):
        layout_main = QVBoxLayout()
        self.setLayout(layout_main)
        layout_main.setSpacing(3)
        # ************************************************************************************************************ #
        layout_top = QHBoxLayout()
        self.setLayout(layout_top)
        layout_top.setSpacing(3)
        # ************************************************************************************************************ #
        layout_bottom = QVBoxLayout()
        self.setLayout(layout_bottom)
        layout_bottom.setSpacing(3)
        # ------------------------------------------------------------------------------------------------------------ #
        layout_bottom1 = QHBoxLayout()
        self.setLayout(layout_bottom1)
        layout_bottom1.setSpacing(3)
        # ------------------------------------------------------------------------------------------------------------ #
        layout_bottom2 = QHBoxLayout()
        self.setLayout(layout_bottom2)
        layout_bottom2.setSpacing(3)
        # ************************************************************************************************************ #
        # Plots on the left
        layout_left = QVBoxLayout()
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_currents != 0 or self.display_voltages != 0:
            layout_top.addLayout(layout_left)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages != 0:
            layout_left.addWidget(self.hv_plots)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages == 2:
            layout_left.addWidget(self.lv_plots)

        # ************************************************************************************************************ #
        # add top layout to main layout
        layout_main.addLayout(layout_top)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_currents == 1:
            layout_left.addWidget(self.all_cm_plots)
        elif self.display_currents == 2:
            # layout_left.addWidget(self.ps_hv_cm_plots)
            # -------------------------------------------------------------------------------------------------------- #
            for plots_row in range(4):
                layout_bottom1.addWidget(self.fb_cm_plots[plots_row])
            # -------------------------------------------------------------------------------------------------------- #
            layout_main.addLayout(layout_bottom1)
        elif self.display_currents == 3:
            # layout_left.addWidget(self.ps_hv_cm_plots)
            # -------------------------------------------------------------------------------------------------------- #
            for plots_row in range(4):
                layout_bottom1.addWidget(self.hb_cm_plots[plots_row])
                layout_bottom2.addWidget(self.hb_cm_plots[plots_row+4])
            # -------------------------------------------------------------------------------------------------------- #
            layout_bottom.addLayout(layout_bottom1)
            layout_bottom.addLayout(layout_bottom2)
            # -------------------------------------------------------------------------------------------------------- #
            layout_main.addLayout(layout_bottom)

        # ************************************************************************************************************ #
        # Rest on the right
        layout_right = QVBoxLayout()
        layout_right.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_right.setSpacing(0)
        layout_top.addLayout(layout_right)
        # ------------------------------------------------------------------------------------------------------------ #
        layout_right.addWidget(self.em_stop)
        layout_right.addWidget(self.voltage)
        # ------------------------------------------------------------------------------------------------------------ #
        tab = QTabWidget(self)
        tab.setFixedWidth(700)

        if MODE1 == 1:
            # layout_right.addWidget(self.Mode1)
            tab.addTab(self.Mode1, 'Mode 1')
        # ------------------------------------------------------------------------------------------------------------ #
        if MODE2 == 1:
            # layout_right.addWidget(self.Mode2)
            tab.addTab(self.Mode2, 'Mode 2')
        # ------------------------------------------------------------------------------------------------------------ #
        if MODE3 == 1:
            # layout_right.addWidget(self.Mode3)
            tab.addTab(self.Mode3, 'Mode 3')
        # ------------------------------------------------------------------------------------------------------------ #
        if MODE4 == 1:
            # layout_right.addWidget(self.Mode4)
            tab.addTab(self.Mode4, 'Mode 4')

        # ------------------------------------------------------------------------------------------------------------ #
        if OLD_MODE5 == 1:
            # layout_right.addWidget(self.Mode4)
            tab.addTab(self.OldMode5, 'Mode Go and Back')

        # ------------------------------------------------------------------------------------------------------------ #
        if MODE5 == 1:
            # layout_right.addWidget(self.Mode4)
            tab.addTab(self.Mode5, 'Mode 5')

        layout_right.addWidget(tab)

        # ************************************************************************************************************ #
        # Data save info
        if self.record_data == 1:
            layout_right.addWidget(self.RecordData)
            layout_right.addWidget(self.SequentialRecord)
        # ************************************************************************************************************ #
        # Debug info
        if self.rcv_data == 1:
            layout_right.addLayout(self.data_recv_layout)
        # ************************************************************************************************************ #
        # Layout of all widgets not plot
        layout_left.addStretch(1)
        layout_right.addStretch(1)

        layout_main.addStretch(1)

    ####################################################################################################################
    # CALLBACK
    def data_reader_callback(self):
        # ************************************************************************************************************ #
        # shift data in the array one sample left
        self.hv_vm[:-1] = self.hv_vm[1:]
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages != 0 or self.display_currents != 0:
            # shift time base
            self.tplot[:-1] = self.tplot[1:]
            self.tplot[-1] = self.tplot[-2] + self.estimateRate
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages != 0:
            self.hv_set[:-1] = self.hv_set[1:]
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages == 2:
            self.lv_set[:-1] = self.lv_set[1:]
            self.lv_vm[:-1] = self.lv_vm[1:]
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_currents != 0:
            for x in range(0, 9):
                self.cm_val[x, :-1] = self.cm_val[x, 1:]
        # ************************************************************************************************************ #
        # read from serial
        try:
            line = self.ser.readline()
            line = line.decode("utf-8")
            if self.rcv_data == 1:
                self.rcv_data_label.setText("Received data: {}".format(line))
        except Exception as e:
            print("[ERR] unable to read line: {}".format(e))
            self.try_reconnect()
            return
        # ------------------------------------------------------------------------------------------------------------ #
        if len(line) <= 1:
            # Enable debug
            to_send = "\r\nMoni 1\r\n"
            send_command(self.ser, to_send)
            return
        # ------------------------------------------------------------------------------------------------------------ #
        if not line.startswith("[moni]"):
            return

        # ************************************************************************************************************ #
        # handle data
        # Remove units, spaces, split with coma
        # Refer to documentation of HVPS to assign data to fields
        data = line.replace(" ", "").replace("uA", "").replace("V", "").replace("Hz", "").replace("\r\n", "").split(",")

        try:
            # -------------------------------------------------------------------------------------------------------- #
            self.hv_vm[-1] = float(data[5])
            self.hv_vm_now = format(float(data[5]), '4.0f')
            # -------------------------------------------------------------------------------------------------------- #
            if self.display_voltages != 0 or self.display_currents != 0:
                self.t_save = int(data[1])
            # -------------------------------------------------------------------------------------------------------- #
            if self.display_voltages != 0:
                self.hv_set[-1] = float(data[2])
                self.hv_set_now = format(float(data[2]), '4.0f')

                self.hv_err[-1] = float(data[2]) - float(data[5])
                self.hv_err_now = format((float(data[2]) - float(data[5])), '4.0f')
            # -------------------------------------------------------------------------------------------------------- #
            if self.display_voltages == 2:
                self.lv_set[-1] = float(data[3])
                self.lv_set_now = format(float(data[3]), '2.1f')

                self.lv_vm[-1] = float(data[4])
                self.lv_vm_now = format(float(data[4]), '2.1f')

                self.lv_err[-1] = float(data[3]) - float(data[5])
                self.lv_err_now = format((float(data[3]) - float(data[4])), '2.1f')
            # -------------------------------------------------------------------------------------------------------- #
            if self.display_currents != 0:
                for HalfBridge in range(nbHalfBridges+1):
                    self.cm_val[HalfBridge, -1] = int(data[HalfBridge + 6])
                    self.cm_val_now[HalfBridge] = format(int(data[HalfBridge + 6]))

        except Exception as e:
            print("[ERR] Unable to convert line: {} - {}".format(line, e))

        # ************************************************************************************************************ #
        # UPDATE PLOTS/LABELS
        # ------------------------------------------------------------------------------------------------------------ #
        # update voltage button
        self.voltage.update_data(current_voltage=self.hv_vm[-1])
        # ------------------------------------------------------------------------------------------------------------ #
        # update voltage plots
        if self.display_voltages != 0:
            self.hv_plots.update_plot(t=self.tplot, y1=self.hv_set, y2=self.hv_vm)
            self.hv_plots.update_label(label1=self.hv_set_now, label2=self.hv_vm_now, label3=self.hv_err_now)
        # ------------------------------------------------------------------------------------------------------------ #
        if self.display_voltages == 2:
            self.lv_plots.update_plot(t=self.tplot, y1=self.lv_set, y2=self.lv_vm)
            self.lv_plots.update_label(label1=self.lv_set_now, label2=self.lv_vm_now, label3=self.lv_err_now)
        # ------------------------------------------------------------------------------------------------------------ #
        # update current plots
        if self.display_currents == 1:
            self.all_cm_plots.update_8_plot(t=self.tplot, y=self.cm_val, labels=self.cm_val_now)
        # ------------------------------------------------------------------------------------------------------------ #
        elif self.display_currents == 2:
            # self.ps_hv_cm_plots.update_1_plot(t=self.tplot, y=self.cm_val[0], label=self.cm_val_now[0])
            for FullBridge in range(nbFullBridges):
                y1_index = (2*FullBridge)+1
                y2_index = 2*(FullBridge+1)
                y_val = [self.cm_val[y1_index], self.cm_val[y2_index]]
                y_val_label = [self.cm_val_now[y1_index], self.cm_val_now[y2_index]]
                self.fb_cm_plots[FullBridge].update_2_plot(t=self.tplot, y=y_val, label=y_val_label)
        # ------------------------------------------------------------------------------------------------------------ #
        elif self.display_currents == 3:
            # self.ps_hv_cm_plots.update_1_plot(t=self.tplot, y=self.cm_val[0], label=self.cm_val_now[0])
            for HalfBridges in range(nbHalfBridges):
                self.hb_cm_plots[HalfBridges].update_1_plot(t=self.tplot,
                                                            y=self.cm_val[HalfBridges+1],
                                                            label=self.cm_val_now[HalfBridges+1])
        # ************************************************************************************************************ #
        # save data to file
        if self.record_data == 1:
            self.RecordData.save_data(line)
            self.SequentialRecord.is_recording_now(line)
        # ************************************************************************************************************ #
        # flush input if too much data not handled: avoid keeping very old values
        if self.ser.in_waiting > 200:
            # print(self.ser.in_waiting)
            self.ser.flushInput()

    ####################################################################################################################
    # RECONNECTION WITH BOARD
    def try_reconnect(self):
        self.ser.close()
        try:
            self.ser.open()
            self.ser.flushInput()
            print("[INFO] reconnected to the board")
        except Exception as err_connection:
            print("[ERR] connection failed: {}".format(err_connection))
            pass

    ####################################################################################################################
    # RECONNECTION WITH BOARD
    def stop_comm(self):
        # Disable HV and monitoring
        send_command(self.ser, "\r\nEStop\r\n")
        if self.record_data == 1:
            self.record_data = 0
            self.RecordData.close_record(sequential=False)
