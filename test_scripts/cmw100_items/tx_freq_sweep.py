from pathlib import Path

from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
import utils.parameters.rb_parameters as rb_pmt
from exception.custom_exception import FileNotFoundException, PortTableException

logger = log_set('freq_sweep')


class TxTestFreqSweep(AtCmd, CMW100):
    def __init__(self):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.tx_freq_wcdma = None
        self.rb_state = None
        self.script = None
        self.file_path = None
        self.parameters = None
        self.srs_path_enable = ext_pmt.srs_path_enable
        self.chan = None
        self.port_table = None

    def port_table_selector(self, band, tx_path='TX1'):
        """
        This is used for multi-ports connection on Tx
        """
        try:
            if self.port_table is None:  # to initial port table at first time
                if ext_pmt.asw_path_enable is False:
                    txas_select = 0
                    self.port_table = self.port_tx_table(txas_select)
                else:
                    self.port_table = self.port_tx_table(self.asw_path)

            if ext_pmt.port_table_en and tx_path in ['TX1', 'TX2']:
                self.port_tx = int(self.port_table[tx_path][str(band)])

            elif ext_pmt.port_table_en and tx_path in ['MIMO']:
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

    def tx_freq_sweep_process_fr1(self):
        """
        band_fr1:
        bw_fr1:
        tx_freq_fr1:
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
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_fr1, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_fr1 = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], ext_pmt.fdc_en)
        self.preset_instrument()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()
        self.sig_gen_fr1()
        self.sync_fr1()

        # to judge if there is correct freq filled in the entry
        start = tx_freq_list[0] if ext_pmt.freq_sweep_start <= 0 else ext_pmt.freq_sweep_start
        stop = tx_freq_list[2] if ext_pmt.freq_sweep_stop <= 0 else ext_pmt.freq_sweep_stop

        freq_range_list = [start, stop, ext_pmt.freq_sweep_step]
        step = freq_range_list[2]

        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in ext_pmt.rb_ftm_fr1:  # PRB, FRB
                        self.rb_size_fr1, self.rb_start_fr1 = rb_pmt.GENERAL_NR[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                        self.rb_state = rb_ftm  # PRB, FRB
                        data = {}
                        for tx_freq_fr1 in range(freq_range_list[0], freq_range_list[1] + step, step):
                            self.tx_freq_fr1 = tx_freq_fr1
                            self.loss_tx = self.loss_selector(self.tx_freq_fr1, ext_pmt.fdc_en)
                            self.tx_set_fr1()
                            aclr_mod_results = self.tx_measure_fr1()
                            logger.debug(aclr_mod_results)
                            data[self.tx_freq_fr1] = aclr_mod_results
                        logger.debug(data)
                        self.parameters = {
                            'script': self.script,
                            'tech': self.tech,
                            'band': self.band_fr1,
                            'bw': self.bw_fr1,
                            'tx_freq_level': self.tx_level,
                            'mcs': self.mcs_fr1,
                            'tx_path': self.tx_path,
                            'mod': None,
                            'rb_state': self.rb_state,
                            'rb_size': self.rb_size_fr1,
                            'rb_start': self.rb_start_fr1,
                            'sync_path': self.sync_path,
                            'asw_srs_path': self.asw_srs_path,
                            'scs': self.scs,
                            'type': self.type_fr1,
                            'test_item': 'freq_sweep',
                        }
                        self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)
        self.set_test_end_fr1()

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
        self.loss_rx = self.loss_selector(rx_freq_list[1], ext_pmt.fdc_en)
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.sig_gen_lte()
        self.sync_lte()

        # to judge if there is correct freq filled in the entry
        start = tx_freq_list[0] if ext_pmt.freq_sweep_start <= 0 else ext_pmt.freq_sweep_start
        stop = tx_freq_list[2] if ext_pmt.freq_sweep_stop <= 0 else ext_pmt.freq_sweep_stop

        freq_range_list = [start, stop, ext_pmt.freq_sweep_step]
        step = freq_range_list[2]

        for mcs in ext_pmt.mcs_lte:
            self.mcs_lte = mcs
            for script in ext_pmt.scripts:
                if script == 'GENERAL':
                    self.script = script
                    for rb_ftm in ext_pmt.rb_ftm_lte:  # PRB, FRB
                        self.rb_size_lte, self.rb_start_lte = rb_pmt.GENERAL_LTE[self.bw_lte][
                            self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                        self.rb_state = rb_ftm  # PRB, FRB
                        data = {}
                        for tx_freq_lte in range(freq_range_list[0], freq_range_list[1] + step, step):
                            self.tx_freq_lte = tx_freq_lte
                            self.loss_tx = self.loss_selector(self.tx_freq_lte, ext_pmt.fdc_en)
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

        for script in ext_pmt.scripts:
            if script == 'GENERAL':
                self.script = script
                data = {}
                for tx_chan_wcdma in range(tx_chan_range_list[0], tx_chan_range_list[1] + step, step):
                    self.tx_chan_wcdma = tx_chan_wcdma
                    self.rx_chan_wcdma = cm_pmt_ftm.transfer_chan_tx2rx_wcdma(self.band_wcdma, tx_chan_wcdma)
                    self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma, 'tx')
                    self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma, 'rx')
                    self.loss_rx = self.loss_selector(self.rx_freq_wcdma, ext_pmt.fdc_en)
                    self.loss_tx = self.loss_selector(self.tx_freq_wcdma, ext_pmt.fdc_en)
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

        for script in ext_pmt.scripts:
            if script == 'GENERAL':
                self.script = script
                data = {}
                for rx_freq_gsm in range(rx_freq_range_list[0], rx_freq_range_list[1] + 1, step):
                    self.rx_freq_gsm = rx_freq_gsm
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_freq_rx2tx_gsm(self.band_gsm, self.rx_freq_gsm)
                    self.rx_chan_gsm = cm_pmt_ftm.transfer_freq2chan_gsm(self.band_gsm, self.rx_freq_gsm)
                    self.loss_rx = self.loss_selector(self.rx_freq_gsm, ext_pmt.fdc_en)
                    self.loss_tx = self.loss_selector(self.tx_freq_gsm, ext_pmt.fdc_en)
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

    def tx_freq_sweep_pipline_fr1(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level_spin
        self.port_tx = ext_pmt.port_tx
        # self.chan = ext_pmt.channel
        self.sa_nsa_mode = ext_pmt.sa_nsa
        items = [
            (tech, tx_path, bw, band, type_)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.fr1_bandwidths
            for band in ext_pmt.fr1_bands
            for type_ in ext_pmt.type_fr1
        ]

        for item in items:
            if item[0] == 'FR1' and ext_pmt.fr1_bands != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_fr1 = item[2]
                self.band_fr1 = item[3]
                self.type_fr1 = item[4]
                self.port_table_selector(self.band_fr1, self.tx_path)
                if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_nr(self.band_fr1):
                    self.tx_freq_sweep_process_fr1()
                else:
                    logger.info(f'B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')


        for bw in ext_pmt.fr1_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'FR1', 'freq_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'FR1'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_freq_sweep_pipline_lte(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level_spin
        self.port_tx = ext_pmt.port_tx
        # self.chan = ext_pmt.channel
        items = [
            (tech, tx_path, bw, band)
            for tech in ext_pmt.tech
            for tx_path in ext_pmt.tx_paths
            for bw in ext_pmt.lte_bandwidths
            for band in ext_pmt.lte_bands
        ]
        for item in items:
            if item[0] == 'LTE' and ext_pmt.lte_bands != []:
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

                else:
                    logger.info(f'LTE Band {self.band_lte} does not have this tx path {self.tx_path}')


        for bw in ext_pmt.lte_bandwidths:
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
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level_spin
        self.port_tx = ext_pmt.port_tx
        # self.chan = ext_pmt.channel
        for tech in ext_pmt.tech:
            if tech == 'WCDMA' and ext_pmt.wcdma_bands != []:
                self.tech = tech
                for band in ext_pmt.wcdma_bands:
                    self.band_wcdma = band
                    self.port_table_selector(self.band_wcdma)
                    self.tx_freq_sweep_process_wcdma()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_freq_sweep_pipline_gsm(self):
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level_spin
        self.port_tx = ext_pmt.port_tx
        # self.chan = ext_pmt.channel
        self.mod_gsm = ext_pmt.mod_gsm
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in ext_pmt.tech:
            if tech == 'GSM' and ext_pmt.gsm_bands != []:
                self.tech = tech
                for band in ext_pmt.gsm_bands:
                    self.pcl = ext_pmt.tx_pcl_lb if band in [850, 900] else ext_pmt.tx_pcl_mb
                    self.band_gsm = band
                    self.port_table_selector(self.band_gsm)
                    self.tx_freq_sweep_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def run(self):
        for tech in ext_pmt.tech:
            if tech == 'LTE':
                self.tx_freq_sweep_pipline_lte()
            elif tech == 'FR1':
                self.tx_freq_sweep_pipline_fr1()
            elif tech == 'WCDMA':
                self.tx_freq_sweep_pipline_wcdma()
            elif tech == 'GSM':
                self.tx_freq_sweep_pipline_gsm()
        self.cmw_close()
