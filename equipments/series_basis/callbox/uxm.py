from connection_interface.connection_visa import VisaComport
from utils.log_init import log_set
import time

logger = log_set('uxm')


class Uxm:
    def __init__(self, equipment):
        self.uxm = VisaComport(equipment)

    def uxm_query(self, command):
        response = self.uxm.query(command).strip()
        logger.info(f'Visa::<<{command}')
        logger.info(f'Visa::>>{response}')
        return response

    def uxm_write(self, command):
        self.uxm.write(command)
        logger.info(f'Visa::<<{command}')

    def get_uxm_check_err(self):
        """
        check error
        :return: 0, 'No error'
        """
        self.uxm_query('SYSTem:ERRor')

    def set_freq_range(self, tech='NR'):
        """

        :param tech:
        :return:
        """
        self.uxm_write(f'BSE:CONFig:NR5G:CELL1:FREQuency:RANGe {tech}')

    def set_duplex_mode_nr(self, tech, mode, cell_port=1):
        """

        :param cell_port:
        :param mode:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:CELL{cell_port}:FREQuency:DUPlex {mode}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:FREQuency:DUPlex {mode}')

    def set_band(self, tech, band, cell_port=1):
        """

        :param cell_port:
        :param band:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:CELL{cell_port}:BAND N{band}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:BAND {band}')

    def set_subcarrier_space_common_nr(self, scs, cell_port=1):
        """

        :param cell_port:
        :param scs: 'MU0'=15khz or 'MU1'=30khz or 'MU2'=60khz or 'MU3'=120khz or 'MU4'=240khz or 'MU5'=480khz
        :return:
        """
        self.uxm_write(f'BSE:CONFig:NR5G:CELL{cell_port}:SUBCarrier:SPACing:COMMon {scs}')

    def set_downlink_channel(self, tech, dl_ch, cell_port=1):
        """

        :param cell_port:
        :param dl_ch:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:CELL{cell_port}:DL:CHANnel {dl_ch}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:DL:CHANnel {dl_ch}')

    def set_downlink_bandwidth_nr(self, tech, bw, cell_port=1):
        """

        :param cell_port:
        :param bw:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:CELL{cell_port}:DL:BW BW{bw}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:DL:BW BW{bw}')

    def set_downlink_power_channel_nr(self, tech, power=-20, cell_port=1):
        """

        :param tech:
        :param cell_port:
        :param power:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFIG:NR5G:CELL{cell_port}:DL:POWer:CHANnel {power}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFIG:LTE:CELL{cell_port}:DL:POWer:CHANnel {power}')

    def set_schdedule_config(self, tech, scenario):
        """

        :param tech:
        :param scenario: 'UL_RMC' or 'DL_RMC' or 'BASIC' or 'FULL_TPUT'
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:SCHeduling:QCONFig:SCENario {scenario}')

    def set_ratio_pdsch_pusch(self, tech, ratio=100):
        """

        :param tech:
        :param ratio:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:SCHeduling:QCONFig:RATIo {ratio}')

    def set_downlink_mcs(self, tech, mcs):
        """

        :param tech:
        :param mcs:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:SCHeduling:QCONFig:DL:MCS {mcs}')

    def set_config_scheduling_apply_all(self, tech):
        """

        :return:
        """
        if tech == 'NR':
            self.uxm_write('BSE:CONFig:NR5G:SCHeduling:QCONFig:APPLy:ALL')
            self.uxm_query('*OPC?')

    def set_port_active(self, tech, on_off, cell_port=1):
        """

        :param on_off:
        :param tech:
        :param cell_port:
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:CELL{cell_port}:ACTive {on_off}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:ACTive {on_off}')

    def get_connection_status(self, tech, cell_port=1):
        """

        :param tech:
        :return: CONN
        """
        if tech == 'NR':
            return self.uxm_query(f'BSE:STATus:NR5G:CELL{cell_port}?')
        elif tech == 'LTE':
            return self.uxm_query(f'BSE:STATus:LTE:CELL{cell_port}?')

    def set_ca_aggregation_downlink(self, range_list, cell_port=1):
        """

        :param range_list: NONE | CELL1 | CELL2 | CELL3 | CELL4 | CELL5 | CELL6 | CELL7 | CELL8
        :param cell_port:
        :return:
        """
        range_str = ','.join(range_list)
        self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:CAGGregation:NRCC:DL {range_str}')

    def set_ca_aggregation_uplink(self, range_list, cell_port=1):
        """

        :param range_list: NONE | CELL1 | CELL2 | CELL3 | CELL4 | CELL5 | CELL6 | CELL7 | CELL8
        :param cell_port:
        :return:
        """
        range_str = ','.join(range_list)
        self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:CAGGregation:NRCC:UL {range_str}')

    def set_ca_aggregation_dl_ul(self, range_list, cell_port=1):
        """

        :param range_list:
        :param cell_port:
        :return:
        """
        range_str = ','.join(range_list)
        self.set_ca_aggregation_downlink(range_list, cell_port)
        self.set_ca_aggregation_uplink(range_list, cell_port)

    def set_ca_aggregation_apply(self, cell_port=1):
        """

        :param cell_port:
        :return:
        """
        self.uxm_write(f'BSE:CONFig:LTE:CELL{cell_port}:CAGGregation:NRCC:APPLy')
        self.uxm_query('*OPC?')

    def set_config_apply(self, tech):
        """

        :param tech:
        :return:
        """
        if tech == 'NR':
            self.uxm_write('BSE:CONFig:NR5G:APPLy')
            self.uxm_query('*OPC?')
        elif tech == 'LTE':
            self.uxm_write('BSE:CONFig:LTE:APPLy')
            self.uxm_query('*OPC?')

    def set_config_scheduling_base(self, tech, param_1, param_2, param_3):
        """

        :param tech:
        :param param_1: "CELLALL" as usual
        :param param_2: "DL:MCSTable", "DL:IMCS", "DL:RBStart", "DL:RBNumber", "DL:APolicy", "UL:MCSTable", "UL:IMCS", "UL:RBStart", "UL:RBNumber", "UL:APolicy"
        :param param_3: "Q64", "21", "0", "50", "ALW"
        :return:
        """
        if tech == 'NR':
            self.uxm_write(f'BSE:CONFig:NR5G:SCHeduling:SETParameter {param_1}, {param_2}, {param_3}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:CONFig:LTE:SCHeduling:SETParameter {param_1}, {param_2}, {param_3}')

    def set_config_scheduling_dl_combo(self, tech, mcs_table, mcs_index, rb_start, rb_number, a_policy='ALW', cell_port='CELLALL'):
        self.set_config_scheduling_base(tech, cell_port, 'DL:MCSTable', mcs_table)
        self.set_config_scheduling_base(tech, cell_port, 'DL:IMCS', mcs_index)
        self.set_config_scheduling_base(tech, cell_port, 'DL:RBStart', rb_start)
        self.set_config_scheduling_base(tech, cell_port, 'DL:RBNumber', rb_number)
        self.set_config_scheduling_base(tech, cell_port, 'DL:APolicy', a_policy)

    def set_config_scheduling_ul_combo(self, tech, mcs_table, mcs_index, rb_start, rb_number, a_policy='ALW', cell_port='CELLALL'):
        self.set_config_scheduling_base(tech, cell_port, 'UL:MCSTable', mcs_table)
        self.set_config_scheduling_base(tech, cell_port, 'UL:IMCS', mcs_index)
        self.set_config_scheduling_base(tech, cell_port, 'UL:RBStart', rb_start)
        self.set_config_scheduling_base(tech, cell_port, 'UL:RBNumber', rb_number)
        self.set_config_scheduling_base(tech, cell_port, 'UL:APolicy', a_policy)

    def set_bler_throughput_clear(self, tech):
        if tech == 'NR':
            self.uxm_write('BSE:NR5G:MEASure:BTHRoughput:CLEar')
        elif tech == 'LTE':
            self.uxm_write('BSE:LTE:MEASure:BTHRoughput:CLEar')

    def set_bler_throughput_state(self, tech, state):
        if tech == 'NR':
            self.uxm_write(f'BSE:NR5G:MEASure:BTHRoughput:STATe {state}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:LTE:MEASure:BTHRoughput:STATe {state}')

        if state == 1:
            self.uxm_query('*OPC?')

    def set_bler_throughput_dl_bler_length(self, tech, length=5000):
        if tech == 'NR':
            self.uxm_write(f'BSE:NR5G:MEASure:BTHRoughput:LENGth:ALL {length}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:LTE:MEASure:BTHRoughput:LENGth:ALL {length}')

    def set_bler_throughput_dl_bler_continue_all(self, tech, on_off=0):
        if tech == 'NR':
            self.uxm_write(f'BSE:NR5G:MEASure:BTHRoughput:CONTinue:ALL {on_off}')
        elif tech == 'LTE':
            self.uxm_write(f'BSE:LTE:MEASure:BTHRoughput:CONTinue:ALL {on_off}')

    def get_bler_throughput_dl_bler(self, tech, cell_port=1):
        """

        :param tech:
        :return: The results array have 10 values:
            progress-count, ack-count, ack-ratio, nack-count, nack-ratio,
            statdtx-count, statdtx-ratio, pdschBlerCount, pdschBlerRatio, pdschTputRatio
        """
        result = None
        if tech == 'NR':
            result = self.uxm_query(f'BSE:NR5G:MEASure:BTHRoughput:DL:BLER:{cell_port}?')
        elif tech == 'LTE':
            result = self.uxm_query(f'BSE:LTE:MEASure:BTHRoughput:DL:BLER:{cell_port}?')

        return result

    def get_bler_throughput_ul_bler(self, tech, cell_port=1):
        """

        :param tech:
        :return: The results array have 10 values:
            progress-count, ack-count, ack-ratio, nack-count, nack-ratio,
            statdtx-count, statdtx-ratio, pdschBlerCount, pdschBlerRatio, pdschTputRatio
        """
        result = None
        if tech == 'NR':
            result = self.uxm_query(f'BSE:NR5G:MEASure:BTHRoughput:UL:BLER:{cell_port}?')
        elif tech == 'LTE':
            result = self.uxm_query(f'BSE:LTE:MEASure:BTHRoughput:UL:BLER:{cell_port}?')

        return result

    def set_bler_throughput_process(self, tech, length, on_off=0):
        self.set_bler_throughput_clear(tech)
        self.set_bler_throughput_state(tech, state=0)
        self.set_bler_throughput_dl_bler_length(tech, length)
        self.set_bler_throughput_dl_bler_continue_all(tech, on_off)
        time.sleep(1)
        # perform the measurement
        self.set_bler_throughput_state(tech, state=1)
        time.sleep(5)
        result_dl = self.get_bler_throughput_dl_bler(tech)
        result_ul = self.get_bler_throughput_ul_bler(tech)
        # expect no error
        self.get_uxm_check_err()

        return result_dl, result_ul