from pathlib import Path
from test_scripts.cmw100_items.tx_lmh import TxTestGenre
from equipments.fsw50 import FSW50
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler_harmonic import get_loss_cmw100
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
import time


logger = log_set('Tx_Harmonics')


class TxHarmonics(TxTestGenre, FSW50):
    def __init__(self, state_dict, obj_progressbar):
        TxTestGenre.__init__(self, state_dict, obj_progressbar)
        FSW50.__init__(self)

    def tx_harmonics_pipline_nr(self):
        """
        this pipline is same as tx_lmh
        """
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
                if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                    self.tx_harmonics_process_nr()
                else:
                    logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')
        for bw in self.state_dict['nr_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'NR', 'harmonics')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'CSE', 'tech': 'NR'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_harmonics_process_nr(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr,
                                                   self.bw_nr)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = get_loss_cmw100(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.select_asw_srs_path()
        self.sig_gen_nr()
        self.sync_nr()

        # scs = 1 if self.band_nr in [34, 38, 39, 40, 41, 42, 48, 77, 78,  # temp
        #                              79] else 0  # for now FDD is forced to 15KHz and TDD is to be 30KHz  # temp
        # scs = 15 * (2 ** scs)  # temp
        # self.scs = scs  # temp

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = channel_freq_select(self.chan, tx_freq_lmh_list)

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            for rb_ftm in self.state_dict['nr_rb_allocation_list']:  # INNER_FULL, OUTER_FULL
                self.rb_size_nr, self.rb_start_nr = \
                    rb_pmt.GENERAL_NR[self.bw_nr][self.scs][self.type_nr][self.rb_alloc_nr_dict[rb_ftm]]
                self.rb_state = rb_ftm  # INNER_FULL, OUTER_FULL
                data_freq = {}
                for tx_freq_nr in tx_freq_select_list:
                    self.tx_freq_nr = tx_freq_nr
                    self.rx_freq_nr = cm_pmt_ftm.transfer_freq_tx2rx_nr(self.band_nr, tx_freq_nr)  # temp
                    self.loss_tx = get_loss_cmw100(self.tx_freq_nr)
                    # self.loss_rx = get_loss(rx_freq_list[1])  # temp
                    # self.set_test_end_nr()  # temp
                    # self.set_test_mode_nr()  # temp
                    # self.select_asw_srs_path() # temp
                    # self.sig_gen_nr()  # temp
                    # self.sync_nr()  # temp
                    self.tx_set_nr()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_nr()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current(self.band_nr))
                    data_freq[self.tx_freq_nr] = aclr_mod_current_results + self.get_temperature() \
                                                  + [
                                                      self.get_harmonics_order(self.tech, self.band_nr, 2,
                                                                               tx_freq_nr),
                                                      self.get_harmonics_order(self.tech, self.band_nr, 3,
                                                                               tx_freq_nr),
                                                  ]
                logger.debug(data_freq)
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
                    'test_item': 'harmonics',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1
        self.set_test_end_nr()

    def tx_harmonics_pipline_lte(self):
        """
        this pipline is same as tx_lmh
        """
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
                if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                    self.tx_harmonics_process_lte()
                else:
                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
        for bw in self.state_dict['lte_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'harmonics')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'CSE', 'tech': 'LTE'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_harmonics_process_lte(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_lte = rx_freq_list[1]
        self.loss_rx = get_loss_cmw100(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.sig_gen_lte()
        self.sync_lte()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = channel_freq_select(self.chan, tx_freq_lmh_list)

        for mcs in self.state_dict['lte_mcs_list']:
            self.mcs_lte = mcs
            for rb_ftm in self.state_dict['lte_rb_allocation_list']:  # PRB, FRB
                self.rb_size_lte, self.rb_start_lte = rb_pmt.GENERAL_LTE[self.bw_lte][
                    self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                self.rb_state = rb_ftm  # PRB, FRB
                data_freq = {}
                for tx_freq_lte in tx_freq_select_list:
                    self.tx_freq_lte = tx_freq_lte
                    self.loss_tx = get_loss_cmw100(self.tx_freq_lte)
                    self.tx_set_lte()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_lte()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current(self.band_lte))
                    data_freq[self.tx_freq_lte] = aclr_mod_current_results + self.get_temperature() \
                                                  + [
                                                      self.get_harmonics_order(self.tech, self.band_lte, 2,
                                                                               tx_freq_lte),
                                                      self.get_harmonics_order(self.tech, self.band_lte, 3,
                                                                               tx_freq_lte),
                                                  ]

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
                    'test_item': 'harmonics',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)
        self.set_test_end_lte()

    def tx_harmonics_pipline_wcdma(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        for tech in self.state_dict['tech_list']:
            if tech == 'WCDMA' and self.state_dict['wcdma_bands_list'] != []:
                self.tech = 'WCDMA'
                for band in self.state_dict['wcdma_bands_list']:
                    self.band_wcdma = band
                    self.tx_harmonics_process_wcdma()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_harmonics_process_wcdma(self):
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
            self.loss_rx = get_loss_cmw100(self.rx_freq_wcdma)
            self.loss_tx = get_loss_cmw100(self.tx_freq_wcdma)
            self.set_test_end_wcdma()
            self.set_test_mode_wcdma()
            self.cmw_query('*OPC?')
            self.sig_gen_wcdma()
            self.sync_wcdma()
            self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
            self.tx_set_wcdma()
            self.antenna_switch_v2()
            aclr_mod_current_results = aclr_mod_results = self.tx_measure_wcdma()
            logger.debug(aclr_mod_results)
            aclr_mod_current_results.append(self.measure_current(self.band_wcdma))
            tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma)
            data_chan[tx_freq_wcdma] = aclr_mod_current_results + self.get_temperature() \
                                       + [
                                           self.get_harmonics_order(self.tech, self.band_wcdma, 2,
                                                                    tx_freq_wcdma),
                                           self.get_harmonics_order(self.tech, self.band_wcdma, 3,
                                                                    tx_freq_wcdma),
                                       ]

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
            'test_item': 'harmonics',
        }
        self.file_path = tx_power_relative_test_export_excel_ftm(data_chan, self.parameters)  # mode=1: LMH mode
        self.set_test_end_wcdma()

    def tx_harmonics_pipline_gsm(self):
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mod_gsm = self.state_dict['gsm_modulation']
        self.tsc = 0 if self.mod_gsm == 'GMSK' else 5
        for tech in self.state_dict['tech_list']:
            if tech == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                self.tech = 'GSM'
                for band in self.state_dict['gsm_bands_list']:
                    self.pcl = self.state_dict['pcl_lb_level'] if band in [850, 900] else self.state_dict['pcl_mb_level']
                    self.band_gsm = band
                    self.tx_harmonics_process_gsm()
                txp_aclr_evm_current_plot_ftm(self.file_path, self.parameters)

    def tx_harmonics_process_gsm(self):
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
            self.loss_rx = get_loss_cmw100(self.rx_freq_gsm)
            self.loss_tx = get_loss_cmw100(self.tx_freq_gsm)
            self.set_test_mode_gsm()
            self.antenna_switch_v2()
            self.sig_gen_gsm()
            self.sync_gsm()
            self.tx_set_gsm()
            aclr_mod_current_results = aclr_mod_results = self.tx_measure_gsm()
            logger.debug(aclr_mod_results)
            aclr_mod_current_results.append(self.measure_current(self.band_gsm))
            data_chan[self.rx_freq_gsm] = aclr_mod_current_results + self.get_temperature() \
                                          + [
                                              self.get_harmonics_order(self.tech, self.band_gsm, 2,
                                                                       self.tx_freq_gsm),
                                              self.get_harmonics_order(self.tech, self.band_gsm, 3,
                                                                       self.tx_freq_gsm),
                                          ]

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
            'test_item': 'harmonics',
        }
        self.file_path = tx_power_relative_test_export_excel_ftm(data_chan, self.parameters)  # mode=1: LMH mode
        self.set_test_end_gsm()

    def run(self):
        for tech in self.state_dict['tech_list']:
            if tech == 'NR':
                self.tx_harmonics_pipline_nr()
            elif tech == 'LTE':
                self.tx_harmonics_pipline_lte()
            elif tech == 'WCDMA':
                self.tx_harmonics_pipline_wcdma()
            elif tech == 'GSM':
                self.tx_harmonics_pipline_gsm()
        self.cmw_close()
        self.fsw_close()
