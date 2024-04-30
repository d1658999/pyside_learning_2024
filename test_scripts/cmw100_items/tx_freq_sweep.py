from pathlib import Path

from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
import utils.parameters.rb_parameters as rb_pmt
from exception.custom_exception import FileNotFoundException, PortTableException

logger = log_set('freq_sweep')


class TxTestFreqSweep(AtCmd, CMW100):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.sa_nsa_mode = 0
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.tx_freq_wcdma = None
        self.rb_state = None
        self.script = None
        self.file_path = None
        self.parameters = None
        self.srs_path_enable = self.state_dict['srs_path_en']
        self.chan = None
        self.port_table = None
        self.rx_level = self.rx_level = self.state_dict['init_rx_sync_level']

    def port_table_selector(self, band, tx_path='TX1'):
        """
        This is used for multi-ports connection on Tx
        """
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

    def select_asw_srs_path(self):
        if self.srs_path_enable:
            self.srs_switch()
        else:
            self.antenna_switch_v2()

    def tx_freq_sweep_process_nr(self):
        """
        band_nr:
        bw_nr:
        tx_freq_nr:
        rb_num:
        rb_start:
        mcs:
        tx_level:
        rf_port:
        freq_range_list: [freq_level_1, freq_level_2, freq_step]
        tx_path:
        data: {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        logger.info('----------Freq Sweep progress ---------')
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr, self.bw_nr)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.preset_instrument()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.select_asw_srs_path()
        self.sig_gen_nr()
        self.sync_nr()

        # to judge if there is correct freq filled in the entry
        start = tx_freq_list[0] if self.state_dict['freq_sweep_start'] <= 0 else self.state_dict['freq_sweep_start']
        stop = tx_freq_list[2] if self.state_dict['freq_sweep_stop'] <= 0 else self.state_dict['freq_sweep_stop']
        step = self.state_dict['freq_sweep_step']

        # freq_range_list = [start, stop, step]

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            for rb_ftm in self.state_dict['nr_rb_allocation_list']:  # PRB, FRB
                self.rb_size_nr, self.rb_start_nr = rb_pmt.GENERAL_NR[self.bw_nr][self.scs][self.type_nr][
                    self.rb_alloc_nr_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                self.rb_state = rb_ftm  # PRB, FRB
                data = {}
                for tx_freq_nr in range(start, stop + step, step):
                    self.tx_freq_nr = tx_freq_nr
                    self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
                    self.tx_set_nr()
                    aclr_mod_results = self.tx_measure_nr()
                    logger.debug(aclr_mod_results)
                    data[self.tx_freq_nr] = aclr_mod_results

                logger.debug(data)
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
                    'test_item': 'freq_sweep',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_nr()

        self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
        self.state_dict['progressBar_progress'] += 1

    def tx_freq_sweep_process_lte(self):
        """
        band_lte:
        bw_lte:
        tx_freq_lte:
        rb_num:
        rb_start:
        mcs:
        tx_level:
        rf_port:
        freq_range_list: [freq_level_1, freq_level_2, freq_step]
        tx_path:
        data: {tx_freq: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        logger.info('----------Freq Sweep progress ---------')
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte, self.bw_lte)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_lte = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.sig_gen_lte()
        self.sync_lte()

        # to judge if there is correct freq filled in the entry
        start = tx_freq_list[0] if self.state_dict['freq_sweep_start'] <= 0 else self.state_dict['freq_sweep_start']
        stop = tx_freq_list[2] if self.state_dict['freq_sweep_stop'] <= 0 else self.state_dict['freq_sweep_stop']
        step = self.state_dict['freq_sweep_step']

        # freq_range_list = [start, stop, step]

        for mcs in self.state_dict['lte_mcs_list']:
            self.mcs_lte = mcs
            for rb_ftm in self.state_dict['lte_rb_allocation_list']:  # PRB, FRB
                self.rb_size_lte, self.rb_start_lte = rb_pmt.GENERAL_LTE[self.bw_lte][
                    self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                self.rb_state = rb_ftm  # PRB, FRB
                data = {}
                for tx_freq_lte in range(start, stop + step, step):
                    self.tx_freq_lte = tx_freq_lte
                    self.loss_tx = self.loss_selector(self.tx_freq_lte, self.state_dict['fdc_en'])
                    self.tx_set_lte()
                    aclr_mod_results = self.tx_measure_lte()
                    logger.debug(aclr_mod_results)
                    data[self.tx_freq_lte] = aclr_mod_results

                logger.debug(data)
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
                    'test_item': 'freq_sweep',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_lte()

        self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
        self.state_dict['progressBar_progress'] += 1

    def tx_freq_sweep_process_wcdma(self):
        """
        band_lte:
        bw_lte:
        tx_freq_lte:
        rb_num:
        rb_start:
        mcs:
        tx_level:
        rf_port:
        freq_range_list: [freq_level_1, freq_level_2, freq_step]
        tx_path:
        data: {tx_freq: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        logger.info('----------Freq Sweep progress ---------')
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]

        self.preset_instrument()

        tx_chan_range_list = [tx_chan_list[0], tx_chan_list[2], 1]
        step = tx_chan_range_list[2]

        data = {}
        for tx_chan_wcdma in range(tx_chan_range_list[0], tx_chan_range_list[1] + step, step):
            self.tx_chan_wcdma = tx_chan_wcdma
            self.rx_chan_wcdma = cm_pmt_ftm.transfer_chan_tx2rx_wcdma(self.band_wcdma, tx_chan_wcdma)
            self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma, 'tx')
            self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma, 'rx')
            self.loss_rx = self.loss_selector(self.rx_freq_wcdma, self.state_dict['fdc_en'])
            self.loss_tx = self.loss_selector(self.tx_freq_wcdma, self.state_dict['fdc_en'])
            self.set_test_end_wcdma()
            self.set_test_mode_wcdma()
            self.cmw_query('*OPC?')
            self.sig_gen_wcdma()
            self.sync_wcdma()
            # self.antenna_switch_v2()
            self.tx_set_wcdma()
            self.antenna_switch_v2()
            aclr_mod_results = self.tx_measure_wcdma()
            logger.debug(aclr_mod_results)
            data[self.tx_freq_wcdma] = aclr_mod_results

        logger.debug(data)
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
            'test_item': 'freq_sweep',
        }
        self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_wcdma()

        self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
        self.state_dict['progressBar_progress'] += 1

    def tx_freq_sweep_process_gsm(self):
        """
        band_gsm:
        tx_freq_gsm:
        tx_pcl:
        rf_port:
        freq_range_list: [freq_level_1, freq_level_2, freq_step]
        tx_path:
        data: {tx_freq: [power, phase_err_rms, phase_peak, ferr,orfs_mod_-200,orfs_mod_200,...orfs_sw-400,
                                                                                                orfs_sw400,...], ...}
        """
        logger.info('----------Freq Sweep progress ---------')
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        rx_chan_range_list = [rx_chan_list[0], rx_chan_list[2], 0.2]
        step = int(rx_chan_range_list[2] * 1000 * 5)
        rx_freq_range_list = [cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, rx_chan) for rx_chan in
                              rx_chan_range_list[:2]]
        rx_freq_range_list.append(step)

        data = {}
        for rx_freq_gsm in range(rx_freq_range_list[0], rx_freq_range_list[1] + 1, step):
            self.rx_freq_gsm = rx_freq_gsm
            self.tx_freq_gsm = cm_pmt_ftm.transfer_freq_rx2tx_gsm(self.band_gsm, self.rx_freq_gsm)
            self.rx_chan_gsm = cm_pmt_ftm.transfer_freq2chan_gsm(self.band_gsm, self.rx_freq_gsm)
            self.loss_rx = self.loss_selector(self.rx_freq_gsm, self.state_dict['fdc_en'])
            self.loss_tx = self.loss_selector(self.tx_freq_gsm, self.state_dict['fdc_en'])
            self.set_test_mode_gsm()
            self.antenna_switch_v2()
            self.sig_gen_gsm()
            self.sync_gsm()
            self.tx_set_gsm()
            aclr_mod_results = self.tx_measure_gsm()
            logger.debug(aclr_mod_results)
            data[self.rx_freq_gsm] = aclr_mod_results

        logger.debug(data)
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
            'test_item': 'freq_sweep',
        }
        self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_gsm()

        self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
        self.state_dict['progressBar_progress'] += 1

    def tx_freq_sweep_pipline_nr(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
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
                self.port_table_selector(self.band_nr, self.tx_path)
                if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                    self.tx_freq_sweep_process_nr()
                else:
                    logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')
                    skip_count = len(self.state_dict['nr_mcs_list']) * len(
                        self.state_dict['nr_rb_allocation_list']) * len(
                        self.state_dict['tx_path_list']) * len(self.state_dict['channel_str'])
                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                    self.state_dict['progressBar_progress'] += skip_count

        for bw in self.state_dict['nr_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'NR', 'freq_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'NR'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_freq_sweep_pipline_lte(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        # self.chan = ext_pmt.channel
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

                if self.tx_path in ['TX1', 'TX2']:
                    self.port_table_selector(self.band_lte, self.tx_path)
                    if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                        self.tx_freq_sweep_process_lte()
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
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'freq_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'LTE'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_freq_sweep_pipline_wcdma(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        # self.chan = ext_pmt.channel
        for tech in self.state_dict['tech_list']:
            if tech == 'WCDMA' and self.state_dict['wcdma_bands_list'] != []:
                self.tech = tech
                for band in self.state_dict['wcdma_bands_list']:
                    self.band_wcdma = band
                    self.port_table_selector(self.band_wcdma)
                    self.tx_freq_sweep_process_wcdma()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_freq_sweep_pipline_gsm(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.mod_gsm = self.state_dict['gsm_modulation']
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in self.state_dict['tech_list']:
            if tech == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                self.tech = 'GSM'
                for band in self.state_dict['gsm_bands_list']:
                    self.pcl = self.state_dict['pcl_lb_level'] if band in [850, 900] else self.state_dict[
                        'pcl_mb_level']
                    self.band_gsm = band
                    self.port_table_selector(self.band_gsm)
                    self.tx_freq_sweep_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def run(self):
        for tech in self.state_dict['tech_list']:
            if tech == 'LTE':
                self.tx_freq_sweep_pipline_lte()
            elif tech == 'NR':
                self.tx_freq_sweep_pipline_nr()
            elif tech == 'WCDMA':
                self.tx_freq_sweep_pipline_wcdma()
            elif tech == 'GSM':
                self.tx_freq_sweep_pipline_gsm()
        self.cmw_close()
