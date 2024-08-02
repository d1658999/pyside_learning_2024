from pathlib import Path
from test_scripts.cmw100_items.tx_lmh import TxTestGenre
from equipments.fsw50 import FSW50
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.loss_handler_harmonic import get_loss_cmw100
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
import time

logger = log_set('Tx_CBE')


class TxCBE(TxTestGenre, FSW50):
    def __init__(self, state_dict, obj_progressbar):
        TxTestGenre.__init__(self, state_dict, obj_progressbar)
        FSW50.__init__(self)
        self.file_folder = None

    def tx_cbe_pipline_nr(self):
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
                    self.tx_cbe_process_nr()
                else:
                    logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')
        for bw in self.state_dict['nr_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'NR', 'cbe')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'CSE', 'tech': 'NR'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_cbe_process_nr(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr,
                                                   self.bw_nr)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
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
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))
        chan_list = [ch for ch in self.chan]

        # create dict to reverse lookup
        zip_dict_chan = {}
        for tx_freq in tx_freq_select_list:
            if tx_freq < tx_freq_lmh_list[1]:
                zip_dict_chan[tx_freq] = 'L'
            elif tx_freq == tx_freq_lmh_list[1]:
                zip_dict_chan[tx_freq] = 'M'
            elif tx_freq > tx_freq_lmh_list[1]:
                zip_dict_chan[tx_freq] = 'H'

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
                    self.loss_tx = get_loss(self.tx_freq_nr)
                    # self.loss_rx = get_loss(rx_freq_list[1])  # temp
                    # self.set_test_end_nr()  # temp
                    # self.set_test_mode_nr()  # temp
                    # self.select_asw_srs_path() # temp
                    # self.sig_gen_nr()  # temp
                    # self.sync_nr()  # temp

                    # spectrum setting for spurios emission
                    self.system_preset()
                    self.set_reference_level_offset('NR', self.band_nr, self.loss_tx)
                    self.set_spur_initial()
                    spur_state = self.set_spur_spec_limit_line(self.band_nr, zip_dict_chan[self.tx_freq_nr],
                                                               self.bw_nr)

                    # if the bands cannot go with FCC request, then skip it
                    if spur_state == 1:
                        continue

                    # start to set tx
                    self.tx_set_nr()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_nr()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current(self.band_nr))
                    data_freq[self.tx_freq_nr] = aclr_mod_current_results + self.get_temperature()

                    # start measure spurious
                    logger.info('----------Start to measure CBE----------')
                    self.set_suprious_emissions_measure()
                    self.fsw_query('*OPC?')
                    worse_margin = max(self.get_spur_limit_margin())

                    # show the pass or fail
                    pass_fail_state = self.get_limits_state().strip()
                    if pass_fail_state == '0':
                        logger.info('For internal spec: PASS')
                        spec_state = 'PASS'
                    else:
                        logger.info('For internal spec: FAIL')
                        spec_state = 'FAIL'

                    # screenshot
                    asw_path = 0 if self.asw_path != 1 else 1
                    file_name = f'{self.tech}_Band{self.band_nr}_BE_{self.bw_nr}_' \
                                f'{zip_dict_chan[self.tx_freq_nr]}_' \
                                f'{self.type_nr}_{self.rb_state}_{self.mcs_nr}_ftm_' \
                                f'{round(aclr_mod_results[3], 2)}dBm_' \
                                f'margin_{worse_margin:.2f}dB_' \
                                f'{self.tx_path}_TxAS{asw_path}_' \
                                f'{spec_state}' \
                                f'.png'  # this is power level
                    local_file_path = self.file_folder / Path(file_name)
                    self.get_spur_screenshot(local_file_path)

                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                    self.state_dict['progressBar_progress'] += 1

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
                    'test_item': 'cbe',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)

                self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                self.state_dict['progressBar_progress'] += 1
        self.set_test_end_nr()

    def tx_cbe_pipline_lte(self):
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
                    self.tx_cbe_process_lte()
                else:
                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')
        for bw in self.state_dict['lte_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'LTE', 'cbe')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'CSE', 'tech': 'LTE'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_cbe_process_lte(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_lte = rx_freq_list[1]
        self.loss_rx = get_loss(rx_freq_list[1])
        logger.info('----------Test LMH progress---------')
        self.preset_instrument()
        self.set_test_end_lte()
        self.set_test_mode_lte()
        self.antenna_switch_v2()
        self.sig_gen_lte()
        self.sync_lte()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))
        chan_list = [ch for ch in self.chan]

        # create dict to reverse lookup
        zip_dict_chan = {}
        for tx_freq in tx_freq_select_list:
            if tx_freq < tx_freq_lmh_list[1]:
                zip_dict_chan[tx_freq] = 'L'
            elif tx_freq == tx_freq_lmh_list[1]:
                zip_dict_chan[tx_freq] = 'M'
            elif tx_freq > tx_freq_lmh_list[1]:
                zip_dict_chan[tx_freq] = 'H'

        for mcs in self.state_dict['lte_mcs_list']:
            self.mcs_lte = mcs
            for rb_ftm in self.state_dict['lte_rb_allocation_list']:  # PRB, FRB
                self.rb_size_lte, self.rb_start_lte = rb_pmt.GENERAL_LTE[self.bw_lte][
                    self.rb_select_lte_dict[rb_ftm]]  # PRB: 0, # FRB: 1
                self.rb_state = rb_ftm  # PRB, FRB
                data_freq = {}
                for tx_freq_lte in tx_freq_select_list:
                    self.tx_freq_lte = tx_freq_lte
                    self.loss_tx = get_loss(self.tx_freq_lte)

                    # spectrum setting for spurios emission
                    self.system_preset()
                    self.set_reference_level_offset('LTE', self.band_lte, self.loss_tx)
                    self.set_spur_initial()
                    spur_state = self.set_spur_spec_limit_line(self.band_lte, zip_dict_chan[self.tx_freq_lte],
                                                               self.bw_lte)

                    # if the bands cannot go with FCC request, then skip it
                    if spur_state == 1:
                        self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                        self.state_dict['progressBar_progress'] += 1
                        continue

                    # start to set tx
                    self.tx_set_lte()
                    aclr_mod_current_results = aclr_mod_results = self.tx_measure_lte()
                    logger.debug(aclr_mod_results)
                    aclr_mod_current_results.append(self.measure_current(self.band_lte))
                    data_freq[self.tx_freq_lte] = aclr_mod_current_results + self.get_temperature()

                    # start measure spurious
                    logger.info('----------Start to measure CBE----------')
                    self.set_suprious_emissions_measure()
                    self.fsw_query('*OPC?')
                    worse_margin = max(self.get_spur_limit_margin())

                    # show the pass or fail

                    pass_fail_state = self.get_limits_state()
                    if pass_fail_state == '0':
                        logger.info('For internal spec: PASS')
                        spec_state = 'PASS'

                    else:
                        logger.info('For internal spec: FAIL')
                        spec_state = 'FAIL'

                    # screenshot
                    asw_path = 0 if self.asw_path != 1 else 1
                    file_name = f'{self.tech}_Band{self.band_lte}_BE_{self.bw_lte}_' \
                                f'{zip_dict_chan[self.tx_freq_lte]}_' \
                                f'{self.rb_state}_{self.mcs_lte}_ftm_' \
                                f'{round(aclr_mod_results[3], 2)}dBm_' \
                                f'margin_{worse_margin:.2f}dB_' \
                                f'{self.tx_path}_TxAS{asw_path}_' \
                                f'{spec_state}' \
                                f'.png'  # this is power level
                    local_file_path = self.file_folder / Path(file_name)
                    self.get_spur_screenshot(local_file_path)

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
                    'test_item': 'cbe',
                }
                self.file_path = tx_power_relative_test_export_excel_ftm(data_freq, self.parameters)
        self.set_test_end_lte()

    def run(self):
        self.file_folder = excel_folder_path()
        for tech in self.state_dict['tech_list']:
            if tech == 'NR':
                self.tx_cbe_pipline_nr()
            elif tech == 'LTE':
                self.tx_cbe_pipline_lte()

        self.cmw_close()
        self.fsw_close()
