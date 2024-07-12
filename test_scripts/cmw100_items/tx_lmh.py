from pathlib import Path
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
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
from utils.excel_handler import color_format_nr_aclr_ftm, color_format_lte_aclr_ftm, color_format_clear
from utils.excel_handler import color_format_wcdma_aclr_ftm, color_format_gsm_orfs_ftm
from utils.excel_handler import color_format_nr_evm_ftm, color_format_lte_evm_ftm
from utils.excel_handler import color_format_wcdma_evm_ftm, color_format_gsm_evm_ftm

logger = log_set('tx_lmh_ns')


class TxTestGenre(AtCmd, CMW100):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.sa_nsa_mode = 0
        self.tx_path_mimo = None
        self.data_freq = None
        self.aclr_mod_current_results = None
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.psu = None
        self.tx_freq_wcdma = None
        self.file_path = None
        self.parameters = None
        self.rb_state = None
        self.script = None
        self.chan = None
        self.srs_path_enable = self.state_dict['srs_path_en']
        self.odpm2 = None
        self.psu = None
        self.port_table = None
        self.get_temp_en = self.state_dict['get_temp_en']
        self.mipi_usid_addr_series = None  # this should have other function
        self.rx_level = self.state_dict['init_rx_sync_level']
        self.fdc_en = self.state_dict['fdc_en']

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

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

    def tx_power_aclr_evm_lmh_process_nr(self):
        """
        order: tx_path > bw > band > mcs > rb > chan
        band_nr:
        bw_nr:
        tx_level:
        rf_port:
        freq_select: 'LMH'
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr,
                                                   self.bw_nr)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.sig_gen_nr()
        self.sync_nr()
        self.select_asw_srs_path()

        # scs = 1 if self.band_nr in [34, 38, 39, 40, 41, 42, 48, 77, 78,  # temp
        #                              79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz  # temp
        # scs = 15 * (2 ** scs)  # temp
        # self.scs = scs  # temp

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            for rb_ftm in self.state_dict['nr_rb_allocation_list']:  # INNER_FULL, OUTER_FULL
                self.rb_size_nr, self.rb_start_nr = \
                    rb_pmt.GENERAL_NR[self.bw_nr][self.scs][self.type_nr][self.rb_alloc_nr_dict[rb_ftm]]
                self.rb_state = rb_ftm  # INNER_FULL, OUTER_FULL
                for tx_freq_nr in tx_freq_select_list:
                    self.tx_freq_nr = tx_freq_nr
                    self.tx_power_aclr_evm_lmh_subprocess_nr()

                    if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                        # ready to export to excel
                        self.parameters = {
                            'script': self.script,
                            'tech': self.tech,
                            'band': self.band_nr,
                            'bw': self.bw_nr,
                            'tx_freq_level': self.tx_level,
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
                            'test_item': 'lmh',
                        }
                        self.file_path = tx_power_relative_test_export_excel_ftm(self.data_freq,
                                                                                 self.parameters)
                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                    self.state_dict['progressBar_progress'] += 1

        self.set_test_end_nr()

    def tx_power_aclr_evm_lmh_process_lte(self):
        """
        order: tx_path > bw > band > mcs > rb > chan
        band_lte:
        bw_lte:
        tx_level:
        rf_port:
        freq_select: 'LMH'
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_lte = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
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
                data_freq = {}
                for tx_freq_lte in tx_freq_select_list:
                    self.tx_freq_lte = tx_freq_lte
                    self.loss_tx = self.loss_selector(self.tx_freq_lte, self.state_dict['fdc_en'])
                    self.tx_set_lte()
                    self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_lte()
                    logger.debug(aclr_mod_results)
                    self.aclr_mod_current_results.append(self.measure_current(self.band_lte))
                    data_freq[self.tx_freq_lte] = self.results_combination_nlw()

                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                    self.state_dict['progressBar_progress'] += 1
                logger.debug(data_freq)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_lte,
                    'bw': self.bw_lte,
                    'tx_freq_level': self.tx_level,
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
                    'test_item': 'lmh',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)

        self.set_test_end_lte()

    def tx_power_aclr_evm_lmh_process_wcdma(self):
        """
                order: tx_path > bw > band > mcs > rb > chan
                band_wcdma:
                tx_level:
                rf_port:
                freq_select: 'LMH'
                tx_path:
                data: {tx_level: [Pwr, U_-1, U_+1, U_-2, U_+2, OBW, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = channel_freq_select(self.chan, tx_rx_chan_list)

        self.preset_instrument()

        data_chan = {}
        for tx_rx_chan_wcdma in tx_rx_chan_select_list:
            logger.info('----------Test LMH progress---------')
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
            self.tx_set_wcdma()
            self.antenna_switch_v2()
            self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_wcdma()
            logger.debug(aclr_mod_results)
            self.aclr_mod_current_results.append(self.measure_current(self.band_wcdma))
            tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma)
            data_chan[tx_freq_wcdma] = self.results_combination_nlw()

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1
        logger.debug(data_chan)

        # ready to export to excel
        self.parameters = {
            'script': self.script,
            'tech': self.tech,
            'band': self.band_wcdma,
            'bw': 5,
            'tx_freq_level': self.tx_level,
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
            'test_item': 'lmh',
        }
        self.file_path = tx_power_relative_test_export_excel_ftm(data_chan, self.parameters)  # mode=1: LMH mode
        self.set_test_end_wcdma()

    def tx_power_aclr_evm_lmh_process_gsm(self):
        """
                order: tx_path > band > chan
                band_gsm:
                tx_pcl:
                rf_port:
                freq_select: 'LMH'
                tx_path:
                data: {rx_freq: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...
                orfs_sw-400,orfs_sw400,...], ...}
        """
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = channel_freq_select(self.chan, rx_chan_list)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        data_chan = {}
        for rx_chan_gsm in rx_chan_select_list:
            logger.info('----------Test LMH progress---------')
            self.rx_chan_gsm = rx_chan_gsm
            self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
            self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
            self.loss_rx = self.loss_selector(self.rx_freq_gsm, self.state_dict['fdc_en'])
            self.loss_tx = self.loss_selector(self.tx_freq_gsm, self.state_dict['fdc_en'])
            self.set_test_mode_gsm()
            self.antenna_switch_v2()
            self.sig_gen_gsm()
            self.sync_gsm()
            self.tx_set_gsm()
            aclr_mod_current_results = aclr_mod_results = self.tx_measure_gsm()
            logger.debug(aclr_mod_results)
            aclr_mod_current_results.append(self.measure_current(self.band_gsm))
            data_chan[self.rx_freq_gsm] = aclr_mod_current_results + self.get_temperature()

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1
        logger.debug(data_chan)

        # ready to export to excel
        self.parameters = {
            'script': self.script,
            'tech': self.tech,
            'band': self.band_gsm,
            'bw': 0,
            'tx_freq_level': self.pcl,
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
            'test_item': 'lmh',
        }
        self.file_path = tx_power_relative_test_export_excel_ftm(data_chan, self.parameters)  # mode=1: LMH mode
        self.set_test_end_gsm()

    def tx_power_aclr_evm_lmh_subprocess_nr(self):
        self.data_freq = data_freq = {}
        self.rx_freq_nr = cm_pmt_ftm.transfer_freq_tx2rx_nr(self.band_nr, self.tx_freq_nr)  # temp
        self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
        # self.loss_rx = get_loss(rx_freq_list[1])  # temp
        # self.set_test_end_nr()  # temp
        # self.set_test_mode_nr()  # temp
        # self.select_asw_srs_path() # temp
        # self.sig_gen_nr()  # temp
        # self.sync_nr()  # temp
        if self.tx_path in ['TX1', 'TX2']:
            self.tx_set_nr()
            self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_nr()
            logger.debug(aclr_mod_results)
            self.aclr_mod_current_results.append(self.measure_current(self.band_nr))
            self.data_freq[self.tx_freq_nr] = self.results_combination_nlw()
            logger.debug(self.data_freq)

        elif self.tx_path in ['MIMO']:  # measure two port
            path_count = 1  # this is for mimo path to store tx_path
            for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                self.port_tx = port_tx
                self.tx_path_mimo = self.tx_path + f'_{path_count}'
                self.tx_set_nr()
                self.aclr_mod_current_results = aclr_mod_results = self.tx_measure_nr()
                logger.debug(aclr_mod_results)
                self.aclr_mod_current_results.append(self.measure_current(self.band_nr))
                data_freq[self.tx_freq_nr] = self.results_combination_nlw()
                logger.debug(data_freq)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_nr,
                    'bw': self.bw_nr,
                    'tx_freq_level': self.tx_level,
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
                    'test_item': 'lmh',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)

                path_count += 1

    def tx_power_aclr_evm_lmh_pipeline_nr(self):
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
                self.port_table_selector(self.band_nr, self.tx_path)  # this is determined if using port table

                if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                    self.tx_power_aclr_evm_lmh_process_nr()
                else:
                    logger.info(f'NR B{self.band_nr} does not have BW {self.bw_nr}MHZ')
                    skip_count = len(self.state_dict['nr_mcs_list']) * len(self.state_dict['nr_rb_allocation_list']) * len(
                        self.state_dict['tx_path_list']) * len(self.state_dict['channel_str'])
                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                    self.state_dict['progressBar_progress'] += skip_count

        for bw in self.state_dict['nr_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'NR', 'lmh')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'tech': 'NR'})
                color_format_clear(file_path)
                color_format_nr_aclr_ftm(file_path)
                color_format_nr_evm_ftm(file_path)

            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

            except Exception as err:
                logger.info(err)

    def tx_power_aclr_evm_lmh_pipeline_lte(self):
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
                    self.port_table_selector(self.band_lte, self.tx_path)  # this is determined if using port table
                    if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                        self.tx_power_aclr_evm_lmh_process_lte()
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
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'lmh')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'tech': 'LTE'})
                color_format_clear(file_path)
                color_format_lte_aclr_ftm(file_path)
                color_format_lte_evm_ftm(file_path)

            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

            except Exception as err:
                logger.info(err)

    def tx_power_aclr_evm_lmh_pipeline_wcdma(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mipi_usid_addr_series = mipi_settings_dict(self.tx_path, self.tech, self.band_wcdma)

        for tech in self.state_dict['tech_list']:
            if tech == 'WCDMA' and self.state_dict['wcdma_bands_list'] != []:
                self.tech = 'WCDMA'
                for band in self.state_dict['wcdma_bands_list']:
                    self.band_wcdma = band
                    self.port_table_selector(self.band_wcdma)  # this is determined if using port table
                    self.tx_power_aclr_evm_lmh_process_wcdma()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)
                color_format_clear(self.file_path)
                color_format_wcdma_aclr_ftm(self.file_path)
                color_format_wcdma_evm_ftm(self.file_path)

    def tx_power_aclr_evm_lmh_pipeline_gsm(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mod_gsm = self.state_dict['gsm_modulation']
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in self.state_dict['tech_list']:
            if tech == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                self.tech = 'GSM'
                for band in self.state_dict['gsm_bands_list']:
                    self.pcl = self.state_dict['pcl_lb_level'] if band in [850, 900] else self.state_dict[
                        'pcl_mb_level']
                    self.band_gsm = band
                    self.port_table_selector(self.band_gsm)  # this is determined if using port table
                    self.tx_power_aclr_evm_lmh_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)
                color_format_clear(self.file_path)
                color_format_gsm_orfs_ftm(self.file_path)
                color_format_gsm_evm_ftm(self.file_path)

    def run(self):
        for tech in self.state_dict['tech_list']:
            if tech == 'NR':
                self.tx_power_aclr_evm_lmh_pipeline_nr()
            elif tech == 'LTE':
                self.tx_power_aclr_evm_lmh_pipeline_lte()
            elif tech == 'WCDMA':
                self.tx_power_aclr_evm_lmh_pipeline_wcdma()
            elif tech == 'GSM':
                self.tx_power_aclr_evm_lmh_pipeline_gsm()
        self.cmw_close()


def main():
    pass


if __name__ == '__main__':
    main()
