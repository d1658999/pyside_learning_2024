from pathlib import Path
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
import time
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.adb_handler import get_odpm_current, RecordCurrent
from equipments.power_supply import Psu
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
from utils.mipi_read_handler import mipi_settings_dict
from exception.custom_exception import FileNotFoundException, PortTableException

logger = log_set('level_sweep')


class TxTestLevelSweep(AtCmd, CMW100):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.tx_path_mimo = None
        self.data = None
        self.aclr_mod_current_results = None
        self.rb_state = None
        self.tx_freq_wcdma = None
        self.script = None
        self.parameters = None
        self.file_path = None
        self.srs_path_enable = self.state_dict['srs_path_en']
        self.chan = None
        self.odpm2 = None
        self.psu = None
        self.port_table = None
        self.get_temp_en = self.state_dict['get_temp_en']
        self.mipi_usid_addr_series = None  # this should have other function
        self.sa_nsa_mode = 0
        self.rx_level = self.state_dict['init_rx_sync_level']

    def port_table_selector(self, band, tx_path='TX1'):
        """
        This is used for multi-ports connection on Tx
        """
        if isinstance(band, str):
            if band in ['1_docomo', '1_kddi', '8_jrf']:
                band = band[0]
            else:
                band = int(band[:-1])
        try:
            if self.port_table is None:  # to initial port table at first time
                if not self.state_dict['as_path_en']:
                    txas_select = 0
                    self.port_table = self.port_tx_table(txas_select)
                else:
                    self.port_table = self.port_tx_table(self.asw_path)

            if self.state_dict['tx_port_table_en'] and tx_path in ['TX1', 'TX2']:
                self.port_tx = int(self.port_table[tx_path][str(band)])

            elif self.state_dict['tx_port_table_en'] and tx_path in ['MIMO']:
                self.port_mimo_tx1 = int(self.port_table['MIMO_TX1'][str(band)])
                self.port_mimo_tx2 = int(self.port_table['MIMO_TX2'][str(band)])
            else:
                pass

        except Exception as err:
            raise PortTableException(f'Tx path {tx_path} and Band {band} not in port table') from err

    def get_temperature(self):
        """
        for P22, AT+GOOGTHERMISTOR=1,1 for MHB LPAMid/ MHB Rx1 LFEM, AT+GOOGTHERMISTOR=0,1
        for LB LPAMid, MHB ENDC LPAMid, UHB(n77/n79 LPAF)
        :return:
        """
        state = self.get_temp_en
        if state is True:
            res0 = self.query_thermister0()
            res1 = self.query_thermister1()
            res_list = [res0, res1]
            therm_list = []
            for res in res_list:
                for r in res:
                    if 'TEMPERATURE' in r.decode().strip():
                        try:
                            temp = eval(r.decode().strip().split(':')[1]) / 1000
                            therm_list.append(temp)
                        except Exception as err:
                            logger.debug(err)
                            therm_list.append(None)
            logger.info(f'thermistor0 get temp: {therm_list[0]}')
            logger.info(f'thermistor1 get temp: {therm_list[1]}')

        else:
            therm_list = [None, None]

        return therm_list

    def volt_mipi_handler(self, tech, band, tx_path):
        if self.state_dict['volt_mipi_en']:
            volt_mipi_handler = self.query_voltage_collection(self.state_dict['et_tracker'])
            return volt_mipi_handler(tech, band, tx_path)
        else:
            return [None]

    def results_combination_nlw(self):
        results = None
        if self.state_dict['volt_mipi_en'] or self.state_dict['fbrx_en'] or self.state_dict['mipi_read_en']:
            if self.tech == 'NR':
                results = self.aclr_mod_current_results + self.get_temperature() + self.volt_mipi_handler(
                    self.tech, self.band_nr, self.tx_path) + self.query_fbrx_power(
                    self.tech) + self.query_comprehensive_mipi(self.tech, self.mipi_usid_addr_series)
            elif self.tech == 'LTE':
                results = self.aclr_mod_current_results + self.get_temperature() + self.volt_mipi_handler(
                    self.tech, self.band_lte, self.tx_path) + self.query_fbrx_power(
                    self.tech) + self.query_comprehensive_mipi(self.tech, self.mipi_usid_addr_series)
            elif self.tech == 'WCDMA':
                results = self.aclr_mod_current_results + self.get_temperature() + self.volt_mipi_handler(
                    self.tech, self.band_wcdma, self.tx_path) + self.query_comprehensive_mipi(self.tech,
                                                                                              self.mipi_usid_addr_series)
            return results

        else:
            results = self.aclr_mod_current_results + self.get_temperature()
            return results

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

    def measure_current_select(self, n=1):
        if self.state_dict['odpm2_en']:
            if self.odpm2 is None:
                self.odpm2 = RecordCurrent()
                self.odpm2.record_current_index_search()
                return self.odpm2.record_current(n)
            else:
                return self.odpm2.record_current(n)

        elif self.state_dict['psu_en']:
            if self.psu is None:
                self.psu = Psu()
                return self.psu.psu_current_average(n)
            else:
                return self.psu.psu_current_average(n)

    def measure_current(self, band):
        count = self.state_dict['current_count']
        if not self.state_dict['psu_en'] and not self.state_dict['odpm2_en']:
            return None

        elif self.tech == 'GSM':
            current_list = []
            for _ in range(5):  # addtional average again
                current_list.append(self.measure_current_select(count))
            avg_sample = sum(current_list) / len(current_list)
            logger.info(f'Average of above current for GSM: {avg_sample}')
            return avg_sample
        else:
            # if band in [34, 38, 39, 40, 41, 42, 48, 77, 78, 79]:
            #     n = count
            # else:
            #     n = 2
            # return self.measure_current_select(n)
            return self.measure_current_select(count)

    def tx_power_relative_test_initial_gsm(self):
        logger.info('----------Relatvie test initial----------')
        self.set_pvt_count_gsm(5)
        self.set_modulation_count_gsm(5)
        self.set_spectrum_modulation_count_gsm(5)
        self.set_spectrum_switching_count_gsm(5)
        self.set_scenario_activate_gsm()
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_gsm(self.port_tx)
        self.set_rf_setting_external_tx_port_attenuation_gsm(self.loss_tx)
        self.set_rf_setting_user_margin_gsm(10.00)
        self.set_trigger_source_gsm('Power')
        self.set_trigger_threshold_gsm(-20.0)
        self.set_repetition_gsm('SING')
        self.set_measurements_enable_all_gsm()
        self.cmw_query(f'*OPC?')
        self.set_orfs_modulation_measurement_off_gsm()
        self.set_spectrum_modulation_evaluation_area_gsm()
        self.set_orfs_switching_measurement_off_gsm()
        self.system_err_all_query()

    def tx_power_relative_test_initial_wcdma(self):
        logger.info('----------Relatvie test initial----------')
        self.cmw_write(f'*CLS')
        self.set_modulation_count_wcdma(5)
        self.set_aclr_count_wcdma(5)
        self.set_rf_tx_port_wcdma(self.port_tx)
        self.set_rf_setting_external_tx_port_attenuation_wcdma(self.loss_tx)
        self.set_rf_setting_user_margin_wcdma(10.00)
        self.set_trigger_source_wcdma('Free Run (Fast sync)')
        self.set_trigger_threshold_wcdma(-30)
        self.set_repetition_wcdma('SING')
        self.set_measurements_enable_all_wcdma()
        self.cmw_query(f'*OPC?')
        self.system_err_all_query()
        self.set_band_wcdma(self.band_wcdma)
        self.set_tx_freq_wcdma(self.tx_chan_wcdma)
        self.set_ul_dpdch_wcdma('ON')
        self.set_ul_dpcch_slot_format_wcdma(0)
        self.set_scrambling_code_wcdma(13496235)
        self.set_ul_signal_config_wcdma('WCDM')
        self.system_err_all_query()

    def tx_power_relative_test_initial_lte(self):
        logger.info('----------Relatvie test initial----------')
        self.select_mode_fdd_tdd(self.band_lte)
        self.set_tx_freq_lte(self.tx_freq_lte)
        self.cmw_query(f'*OPC?')
        self.set_bw_lte(self.bw_lte)
        self.set_mcs_lte(self.mcs_lte)
        self.set_rb_size_lte(self.rb_size_lte)
        self.set_rb_start_lte(self.rb_start_lte)
        self.set_type_cyclic_prefix_lte('NORM')
        self.set_plc_lte(0)
        self.set_delta_sequence_shift_lte(0)
        self.set_rb_auto_detect_lte('OFF')
        self.set_meas_on_exception_lte('ON')
        self.set_sem_limit_lte(self.bw_lte)
        self.system_err_all_query()
        self.set_measured_slot_lte('ALL')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_expect_power_lte(self.tx_level + 5)
        self.set_rf_tx_port_lte(self.port_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_rb_auto_detect_lte('ON')
        self.set_modulation_count_lte(5)
        self.cmw_query(f'*OPC?')
        self.set_aclr_count_lte(5)
        self.cmw_query(f'*OPC?')
        self.set_sem_count_lte(5)
        self.cmw_query(f'*OPC?')
        self.set_trigger_source_lte('GPRF Gen1: Restart Marker')
        self.set_trigger_threshold_lte(-20.0)
        self.set_repetition_lte('SING')
        self.set_measurements_enable_all_lte()
        self.cmw_query(f'*OPC?')
        self.set_measured_subframe_lte()
        self.set_scenario_activate_lte('SAL')
        self.system_err_all_query()
        self.set_rf_setting_external_tx_port_attenuation_lte(self.loss_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_gprf(self.port_tx)
        self.set_power_count_gprf(2)
        self.set_repetition_gprf('SING')
        self.set_power_list_mode_gprf('OFF')
        self.set_trigger_source_gprf('Free Run')
        self.set_trigger_slope_gprf('REDG')
        self.set_trigger_step_length_gprf(5.0e-3)
        self.set_trigger_measure_length_gprf(8.0e-4)
        self.set_trigger_offset_gprf(2.1E-3)
        self.set_trigger_mode_gprf('ONCE')
        self.set_rf_setting_user_margin_gprf(10.00)
        self.set_expect_power_gprf(self.tx_level + 5)

    def tx_power_relative_test_initial_nr(self):
        logger.info('----------Relatvie test initial----------')
        self.select_mode_fdd_tdd(self.band_nr)
        self.set_band_nr(self.band_nr)
        self.set_tx_freq_nr(self.tx_freq_nr)
        self.cmw_query(f'*OPC?')
        self.set_plc_nr(0)
        self.set_meas_on_exception_nr('ON')
        self.set_scs_bw_nr(self.scs, self.bw_nr)
        self.set_sem_limit_nr(self.bw_nr)
        self.set_pusch_nr(self.mcs_nr, self.rb_size_nr, self.rb_start_nr)
        self.set_precoding_nr(self.type_nr)
        self.set_phase_compensation_nr()
        self.cmw_query(f'*OPC?')
        self.set_repetition_nr('SING')
        self.set_plc_nr(0)
        self.set_channel_type_nr()
        self.set_uldl_periodicity_nr('MS25')
        self.set_uldl_pattern_nr(self.scs)
        self.set_measured_slot_nr('ALL')
        self.set_rf_tx_port_nr(self.port_tx)
        self.set_rf_setting_user_margin_nr(10.00)
        self.set_modulation_count_nr(5)
        self.set_aclr_count_nr(5)
        self.set_sem_count_nr(5)
        self.set_trigger_source_nr('GPRF GEN1: Restart Marker')
        self.set_trigger_threshold_nr(-20)
        self.set_repetition_nr('SING')
        self.set_measurements_enable_all_nr()
        self.set_measured_subframe_nr(10)
        self.set_measured_slot_nr('ALL')
        self.set_scenario_activate_nr('SAL')
        self.set_rf_setting_external_tx_port_attenuation_nr(self.loss_tx)
        self.cmw_query(f'*OPC?')

    def tx_level_sweep_process_nr(self):
        """
        band_nr:
        bw_nr:
        tx_freq_nr:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr, self.bw_nr)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_nr = rx_freq_list[1]
        self.tx_freq_nr = tx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.preset_instrument()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.sig_gen_nr()
        self.sync_nr()
        self.select_asw_srs_path()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            for rb_ftm in self.state_dict['nr_rb_allocation_list']:  # INNER, OUTER
                self.rb_size_nr, self.rb_start_nr = rb_pmt.GENERAL_NR[self.bw_nr][self.scs][self.type_nr][
                    self.rb_alloc_nr_dict[rb_ftm]]  # INNER: 0, # OUTER: 1
                self.rb_state = rb_ftm  # INNER, OUTER

                #  initial all before tx level prgress
                for tx_freq_select in tx_freq_select_list:
                    self.tx_freq_nr = tx_freq_select
                    self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
                    self.tx_set_nr()
                    self.tx_power_relative_test_initial_nr()

                    #  following is real change tx level prgress
                    self.tx_level_sweep_subprocess_nr()

                    if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                        self.parameters = {
                            'script': self.script,
                            'tech': self.tech,
                            'band': self.band_nr,
                            'bw': self.bw_nr,
                            'tx_freq_level': self.tx_freq_nr,
                            'mcs': self.mcs_nr,
                            'tx_path': self.tx_path,
                            'mod': None,
                            'rb_state': self.rb_state,
                            'rb_size': self.rb_size_nr,
                            'rb_start': self.rb_start_nr,
                            'sync_path': self.sync_path,
                            'asw_srs_path': self.asw_srs_path,
                            'scs': self.scs,
                            'type': self.type_nr,
                            'test_item': 'level_sweep',
                        }
                        self.file_path = tx_power_relative_test_export_excel_ftm(self.data, self.parameters)

                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                    self.state_dict['progressBar_progress'] += 1
        self.set_test_end_nr()

    def tx_level_sweep_process_lte(self):
        """
        band_lte:
        bw_lte:
        tx_freq_lte:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_lte = rx_freq_list[1]
        self.tx_freq_lte = tx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.cmw_query('*OPC?')
        self.sig_gen_lte()
        self.sync_lte()
        self.antenna_switch_v2()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in self.state_dict['lte_mcs_list']:
            self.mcs_lte = mcs
            for rb_ftm in self.state_dict['lte_rb_allocation_list']:  # PRB, FRB
                self.rb_size_lte, self.rb_start_lte = rb_pmt.GENERAL_LTE[self.bw_lte][
                    self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                self.rb_state = rb_ftm  # PRB, FRB

                #  initial all before tx level prgress
                for tx_freq_select in tx_freq_select_list:
                    self.tx_freq_lte = tx_freq_select
                    self.loss_tx = self.loss_selector(self.tx_freq_lte, self.state_dict['fdc_en'])
                    self.tx_set_lte()
                    self.tx_power_relative_test_initial_lte()

                    tx_range_list = [
                        self.state_dict['level_sweep_start'], self.state_dict['level_sweep_stop']
                    ]  # [tx_level_1, tx_level_2]

                    logger.info('----------TX Level Sweep progress---------')
                    logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

                    step = -1 if tx_range_list[0] > tx_range_list[1] else 1

                    #  following is real change tx level process
                    data = {}
                    for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                        self.tx_level = tx_level
                        logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                        self.set_level_lte(self.tx_level)
                        self.set_chan_request_lte()
                        self.set_rf_setting_user_margin_lte(10.00)
                        self.set_expect_power_lte(self.tx_level + 5)
                        mod_results = self.get_modulation_avgerage_lte()
                        # logger.info(f'mod_results = {mod_results}')
                        self.set_measure_start_on_lte()
                        self.cmw_query('*OPC?')
                        aclr_results = self.get_aclr_average_lte()
                        aclr_results[3] = mod_results[-1]
                        mod_results.pop()
                        self.get_in_band_emissions_lte()
                        self.get_flatness_extreme_lte()
                        time.sleep(0.2)
                        self.get_sem_average_and_margin_lte()
                        self.set_measure_stop_lte()
                        self.cmw_query('*OPC?')
                        self.aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                        logger.debug(aclr_mod_results)
                        self.aclr_mod_current_results.append(self.measure_current(self.band_lte))
                        data[tx_level] = self.results_combination_nlw()

                    logger.debug(data)
                    self.parameters = {
                        'script': self.script,
                        'tech': self.tech,
                        'band': self.band_lte,
                        'bw': self.bw_lte,
                        'tx_freq_level': self.tx_freq_lte,
                        'mcs': self.mcs_lte,
                        'tx_path': self.tx_path,
                        'mod': None,
                        'rb_state': self.rb_state,
                        'rb_size': self.rb_size_lte,
                        'rb_start': self.rb_start_lte,
                        'sync_path': self.sync_path,
                        'asw_srs_path': self.asw_srs_path,
                        'scs': None,
                        'type': None,
                        'test_item': 'level_sweep',
                    }
                    self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)

                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                    self.state_dict['progressBar_progress'] += 1
        self.set_test_end_lte()

    def tx_level_sweep_process_wcdma(self):
        """
        band_wcdma:
        bw_wcdma:
        tx_freq_wcdma:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = channel_freq_select(self.chan, tx_rx_chan_list)

        self.preset_instrument()

        #  initial all before tx level process
        for tx_rx_chan_wcdma in tx_rx_chan_select_list:
            self.rx_chan_wcdma = tx_rx_chan_wcdma[1]
            self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
            self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma, 'rx')
            self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma, 'tx')
            self.loss_rx = self.loss_selector(self.rx_freq_wcdma, self.state_dict['fdc_en'])
            self.loss_tx = self.loss_selector(self.tx_freq_wcdma, self.state_dict['fdc_en'])
            self.set_test_end_wcdma()
            self.set_test_mode_wcdma()
            self.cmw_query('*OPC?')
            self.sig_gen_wcdma()
            self.sync_wcdma()

            self.tx_power_relative_test_initial_wcdma()

            tx_range_list = [
                self.state_dict['level_sweep_start'], self.state_dict['level_sweep_stop']
            ]  # [tx_level_1, tx_level_2]

            logger.info('----------TX Level Sweep progress---------')
            logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

            step = -1 if tx_range_list[0] > tx_range_list[1] else 1

            #  following is real change tx level process
            data = {}
            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                self.tx_level = tx_level
                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                self.tx_set_wcdma_level_use()
                # self.tx_set_wcdma()
                self.antenna_switch_v2()

                # self.command(f'AT+HTXPERSTART={self.tx_chan_wcdma}')
                # self.command(f'AT+HSETMAXPOWER={self.tx_level * 10}')
                #
                self.set_rf_setting_user_margin_wcdma(10.00)
                self.set_expect_power_wcdma(self.tx_level + 5)
                mod_results = self.get_modulation_avgerage_wcdma()
                self.set_measure_start_on_wcdma()
                self.cmw_query(f'*OPC?')
                spectrum_results = self.get_aclr_average_wcdma()
                self.set_measure_stop_wcdma()

                self.aclr_mod_current_results = spectrum_results + mod_results
                logger.debug(self.aclr_mod_current_results)
                self.aclr_mod_current_results.append(self.measure_current(self.band_wcdma))
                data[tx_level] = self.results_combination_nlw()

            logger.debug(data)
            self.parameters = {
                'script': self.script,
                'tech': self.tech,
                'band': self.band_wcdma,
                'bw': 5,
                'tx_freq_level': self.tx_freq_wcdma,
                'mcs': 'QPSK',
                'tx_path': None,
                'mod': None,
                'rb_state': None,
                'rb_size': None,
                'rb_start': None,
                'sync_path': None,
                'asw_srs_path': self.asw_srs_path,
                'scs': None,
                'type': None,
                'test_item': 'level_sweep',
            }
            self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1

        self.set_test_end_wcdma()

    def tx_level_sweep_process_gsm(self):
        """
        band_gsm:
        tx_freq_gsm:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_pcl: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...orfs_sw-400,
                                                                                                orfs_sw400,...], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = channel_freq_select(self.chan, rx_chan_list)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        #  initial all before tx level prgress
        for rx_chan_gsm in rx_chan_select_list:
            self.rx_chan_gsm = rx_chan_gsm
            self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
            self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
            self.loss_rx = self.loss_selector(self.rx_freq_gsm, self.state_dict['fdc_en'])
            self.loss_tx = self.loss_selector(self.tx_freq_gsm, self.state_dict['fdc_en'])
            self.set_test_mode_gsm()
            self.antenna_switch_v2()
            self.sig_gen_gsm()
            self.sync_gsm()

            # self.tx_power_relative_test_initial_gsm()

            tx_pcl_range_list_lb = [19, 5]  # tx_pcl_1, tx_pcl_2; GMSK_LB: 5 ~ 19, EPSK_LB: 8~19
            tx_pcl_range_list_mb = [15, 0]  # tx_pcl_1, tx_pcl_2; GMSK_MB: 0 ~ 15, EPSK_MB: 2~15

            tx_range_list = tx_pcl_range_list_lb if self.band_gsm in [850, 900] \
                else tx_pcl_range_list_mb  # [tx_pcl_1, tx_pcl_2]

            logger.info('----------TX Level Sweep progress---------')
            logger.info(f'----------from PCL{tx_range_list[0]} to PCL{tx_range_list[1]}----------')

            step = -1 if tx_range_list[0] > tx_range_list[1] else 1

            #  following is real change tx pcl prgress

            data = {}
            for tx_pcl in range(tx_range_list[0], tx_range_list[1] + step, step):
                self.pcl = tx_pcl
                logger.info(f'========Now Tx PCL = PCL{self.pcl} ========')
                self.tx_set_gsm()
                mod_orfs_current_results = mod_orfs_results = self.tx_measure_gsm()
                logger.debug(mod_orfs_results)
                mod_orfs_current_results.append(self.measure_current(self.band_gsm))
                data[tx_pcl] = mod_orfs_current_results + self.get_temperature()

            logger.debug(data)
            self.parameters = {
                'script': self.script,
                'tech': self.tech,
                'band': self.band_gsm,
                'bw': 0,
                'tx_freq_level': self.rx_freq_gsm,
                'mcs': None,
                'tx_path': None,
                'mod': self.mod_gsm,
                'rb_state': None,
                'rb_size': None,
                'rb_start': None,
                'sync_path': None,
                'asw_srs_path': self.asw_srs_path,
                'scs': None,
                'type': None,
                'test_item': 'level_sweep',
            }
            self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1
        self.set_test_end_gsm()

    def tx_level_sweep_subprocess_nr(self):
        tx_range_list = [
            self.state_dict['level_sweep_start'], self.state_dict['level_sweep_stop']
        ]  # [tx_level_1, tx_level_2]

        logger.info('----------TX Level Sweep progress---------')
        logger.info(f'----------from {tx_range_list[0]} dBm to {tx_range_list[1]} dBm----------')

        step = -1 if tx_range_list[0] > tx_range_list[1] else 1

        self.data = data = {}
        if self.tx_path in ['TX1', 'TX2']:
            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                self.tx_level = tx_level
                logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                self.set_level_nr(self.tx_level)
                self.set_rf_setting_user_margin_nr(10.00)
                self.set_expect_power_nr(self.tx_level + 5)
                self.set_measure_start_on_nr()
                self.cmw_query('*OPC?')
                mod_results = self.get_modulation_avgerage_nr()
                aclr_results = self.get_aclr_average_nr()
                aclr_results[3] = mod_results[-1]
                mod_results.pop()
                self.get_in_band_emissions_nr()
                self.get_flatness_extreme_nr()
                # time.sleep(0.2)
                self.get_sem_average_and_margin_nr()
                self.set_measure_stop_nr()
                self.cmw_query('*OPC?')
                self.aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                logger.debug(aclr_mod_results)
                self.aclr_mod_current_results.append(self.measure_current(self.band_nr))
                self.data[tx_level] = self.results_combination_nlw()
            logger.debug(self.data)

        elif self.tx_path in ['MIMO']:
            for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
                path_count = 1  # this is for mimo path to store tx_path
                for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                    self.port_tx = port_tx
                    self.tx_path_mimo = self.tx_path + f'_{path_count}'
                    self.tx_level = tx_level
                    logger.info(f'========Now Tx level = {self.tx_level} dBm========')
                    self.set_level_nr(self.tx_level)
                    self.set_rf_setting_user_margin_nr(10.00)
                    self.set_expect_power_nr(self.tx_level + 5)
                    self.set_measure_start_on_nr()
                    self.cmw_query('*OPC?')
                    mod_results = self.get_modulation_avgerage_nr()
                    aclr_results = self.get_aclr_average_nr()
                    aclr_results[3] = mod_results[-1]
                    mod_results.pop()
                    self.get_in_band_emissions_nr()
                    self.get_flatness_extreme_nr()
                    # time.sleep(0.2)
                    self.get_sem_average_and_margin_nr()
                    self.set_measure_stop_nr()
                    self.cmw_query('*OPC?')
                    self.aclr_mod_current_results = aclr_mod_results = aclr_results + mod_results
                    logger.debug(aclr_mod_results)
                    self.aclr_mod_current_results.append(self.measure_current(self.band_nr))
                    data[tx_level] = self.results_combination_nlw()
                    logger.debug(data)
                    self.parameters = {
                        'script': self.script,
                        'tech': self.tech,
                        'band': self.band_nr,
                        'bw': self.bw_nr,
                        'tx_freq_level': self.tx_freq_nr,
                        'mcs': self.mcs_nr,
                        'tx_path': self.tx_path_mimo,
                        'mod': None,
                        'rb_state': self.rb_state,
                        'rb_size': self.rb_size_nr,
                        'rb_start': self.rb_start_nr,
                        'sync_path': self.sync_path,
                        'asw_srs_path': self.asw_srs_path,
                        'scs': self.scs,
                        'type': self.type_nr,
                        'test_item': 'level_sweep',
                    }
                    self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)

                    path_count += 1
                    data = {}

    def tx_level_sweep_pipeline_nr(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        items = [
            (tech, tx_path, bw, band, type_)
            for tech in self.state_dict['tech_list']
            for tx_path in self.state_dict['tx_path_list']
            for bw in self.state_dict['nr_bw_list']
            for band in self.state_dict['nr_bands_list']
            for type_ in self.state_dict['nr_type_list']
        ]

        for item in items:
            if item[0] == 'NR' and self.state_dict['nr_bands_list'] != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_nr = item[2]
                self.band_nr = item[3]
                self.type_nr = item[4]
                self.mipi_usid_addr_series = mipi_settings_dict(self.tx_path, self.tech, self.band_nr)
                self.port_table_selector(self.band_nr, self.tx_path)

                if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                    self.tx_level_sweep_process_nr()
                else:
                    logger.info(f'NR B{self.band_nr} does not have BW {self.bw_nr}MHZ')
                    skip_count = len(self.state_dict['nr_mcs_list']) * len(
                        self.state_dict['nr_rb_allocation_list']) * len(
                        self.state_dict['tx_path_list']) * len(self.state_dict['channel_str'])
                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                    self.state_dict['progressBar_progress'] += skip_count

        for bw in self.state_dict['nr_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'NR', 'level_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'NR'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_level_sweep_pipeline_lte(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']

        items = [
            (tech, tx_path, bw, band)
            for tech in self.state_dict['tech_list']
            for tx_path in self.state_dict['tx_path_list']
            for bw in self.state_dict['lte_bw_list']
            for band in self.state_dict['lte_bands_list']
        ]
        for item in items:
            if item[0] == 'LTE' and self.state_dict['lte_bands_list'] != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_lte = item[2]
                self.band_lte = item[3]
                self.mipi_usid_addr_series = mipi_settings_dict(self.tx_path, self.tech, self.band_lte)

                if self.tx_path in ['TX1', 'TX2']:
                    self.port_table_selector(self.band_lte, self.tx_path)
                    if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                        self.tx_level_sweep_process_lte()
                    else:
                        logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
                        skip_count = len(self.state_dict['lte_mcs_list']) * len(
                            self.state_dict['lte_rb_allocation_list']) * len(
                            self.state_dict['tx_path_list']) * len(self.state_dict['channel_str'])
                        self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                        self.state_dict['progressBar_progress'] += skip_count

                else:
                    logger.info(f'LTE Band {self.band_lte} does not have this tx path {self.tx_path}')

        for bw in self.state_dict['lte_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'level_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'LTE'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_level_sweep_pipeline_wcdma(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mipi_usid_addr_series = mipi_settings_dict(self.tx_path, self.tech, self.band_wcdma)

        for tech in self.state_dict['tech_list']:
            if tech == 'WCDMA' and self.state_dict['wcdma_bands_list'] != []:
                self.tech = 'WCDMA'
                for band in self.state_dict['wcdma_bands_list']:
                    self.band_wcdma = band
                    self.port_table_selector(self.band_wcdma)
                    self.tx_level_sweep_process_wcdma()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_level_sweep_pipeline_gsm(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mod_gsm = self.state_dict['gsm_modulation']
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in self.state_dict['tech_list']:
            if tech == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                self.tech = tech
                for band in self.state_dict['gsm_bands_list']:
                    self.pcl = self.state_dict['pcl_lb_level'] if band in [850, 900] else self.state_dict[
                        'pcl_mb_level']
                    self.band_gsm = band
                    self.port_table_selector(self.band_gsm)
                    self.tx_level_sweep_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def run(self):
        for tech in self.state_dict['tech_list']:
            if tech == 'NR':
                self.tx_level_sweep_pipeline_nr()
            elif tech == 'LTE':
                self.tx_level_sweep_pipeline_lte()
            elif tech == 'WCDMA':
                self.tx_level_sweep_pipeline_wcdma()
            elif tech == 'GSM':
                self.tx_level_sweep_pipeline_gsm()
        self.cmw_close()
