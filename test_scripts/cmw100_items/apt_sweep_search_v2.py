import traceback
from pathlib import Path
from utils.log_init import log_set
from utils.loss_handler import get_loss
import utils.parameters.external_paramters as ext_pmt
from utils.excel_handler import txp_aclr_evm_current_plot_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
from test_scripts.cmw100_items.apt_sweep_search import AptSweep

import datetime

logger = log_set('apt_sweep_v2')

# ACLR_LIMIT_USL = -37
# ACLR_MARGIN = 15
# EVM_LIMIT_USL = 2.5
# EVM_LIMIT_ABS = 2.5
# COUNT_BIAS1 = 4
# COUNT_BIAS0 = 4
# COUNT_VCC = 5
ALGR_MODE = 1  # 1:b1b0v, 0:b0b1v


class AptSweepV2(AptSweep):

    def __init__(self):
        super().__init__()
        self.index_lpm_wanted = None
        self.index_hpm_wanted = None

    def tx_apt_sweep_pipeline_fr1(self):
        self.global_parameters()
        self.rx_level = ext_pmt.init_rx_sync_level
        self.tx_level = ext_pmt.tx_level
        self.port_tx = ext_pmt.port_tx
        self.chan = ext_pmt.channel
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
                try:
                    self.port_table_selector(self.band_fr1, self.tx_path)
                    if self.bw_fr1 in cm_pmt_ftm.bandwidths_selected_nr(self.band_fr1):
                        # force to APT mode
                        self.set_apt_mode_force(self.band_fr1, self.tx_path, 0)

                        # check the sw point level
                        # self.sw_point_level = self.get_pa_sw_rise_level(self.band_fr1, self.tx_path, 4)

                        self.select_scs_fr1(self.band_fr1)
                        self.tx_apt_sweep_process_fr1()

                        # to fill out the other level to vcc and bias that are not by apt sweep
                        self.fill_out_rest_vcc_bias(self.TX_LEVEL_START_HPM, self.TX_LEVEL_SOP_HPM, self.band_fr1,
                                                    self.tx_path)

                        # recover to ET/SAPT mode
                        self.set_apt_mode_force(self.band_fr1, self.tx_path, 1)

                        # calibration
                        self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)

                    else:
                        logger.info(f'NR B{self.band_fr1} does not have BW {self.bw_fr1}MHZ')

                except KeyError as err:
                    logger.debug(f'Error {err}')
                    traceback.print_exc()
                    logger.info(f'NR Band {self.band_fr1} does not have this tx path {self.tx_path}')

        for bw in ext_pmt.fr1_bandwidths:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'FR1', 'apt_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'APT', 'tech': 'FR1'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundError:
                logger.info(f'there is no file to plot BW{bw} ')

    def tx_apt_sweep_process_fr1(self):
        """
        band_fr1:
        bw_fr1:
        tx_freq_fr1:
        rb_num:
        rb_start:
        mcs:
        pwr:
        rf_port:
        loss:
        tx_path:
        data {tx_level: [ U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET], ...}
        """
        for mcs in ext_pmt.mcs_fr1:
            self.mcs_fr1 = mcs
            for script in ext_pmt.scripts:
                if script == 'APT':
                    self.script = script
                    for rb_ftm in ext_pmt.rb_ftm_fr1:  # INNER, OUTER
                        self.rb_size_fr1, self.rb_start_fr1 = rb_pmt.GENERAL_NR[self.bw_fr1][self.scs][self.type_fr1][
                            self.rb_alloc_fr1_dict[rb_ftm]]  # INNER: 0, # OUTER: 1
                        self.rb_state = rb_ftm  # INNER, OUTER

                        # initial some freq list, rx sync
                        rx_freq_list = cm_pmt_ftm.dl_freq_selected('FR1', self.band_fr1, self.bw_fr1)
                        tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_fr1, rx_freq) for rx_freq in
                                        rx_freq_list]
                        self.rx_freq_fr1 = rx_freq_list[1]
                        self.tx_freq_fr1 = tx_freq_list[1]
                        self.loss_rx = get_loss(rx_freq_list[1])

                        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_fr1, rx_freq) for rx_freq in
                                            rx_freq_list]
                        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

                        #  initial all before tx level progress
                        for tx_freq_select in tx_freq_select_list:
                            self.tx_freq_fr1 = tx_freq_select
                            self.loss_tx = get_loss(self.tx_freq_fr1)

                            #  following is real change tx level progress
                            self.tx_apt_sweep_subprocess_fr1()

        self.set_test_end_fr1()

    def tx_apt_sweep_subprocess_fr1(self):

        # tx_range_list = ext_pmt.tx_level_range_list  # [tx_level_1, tx_level_2]

        logger.info('----------APT TX Level Sweep progress---------')

        if self.tx_path in ['TX1', 'TX2']:

            self.data = {}
            self.candidate = {}
            vcc_start, bias0_start, bias1_start = self.VCC_START_HPM, self.BIAS0_START_HPM, self.BIAS1_START_HPM
            self.vcc_stop = self.VCC_STOP_HPM
            self.vcc_step = self.VCC_STEP_HPM
            self.bias0_stop = self.BIAS0_STOP_HPM
            self.bias1_stop = self.BIAS1_STOP_HPM
            self.bias0_step = self.BIAS0_STEP_HPM
            self.bias1_step = self.BIAS1_STEP_HPM
            tx_level_start = self.TX_LEVEL_START_HPM
            tx_level_stop = self.TX_LEVEL_SOP_HPM
            tx_level_step = self.TX_LEVEL_STEP_HPM

            for tx_level in range(tx_level_start, tx_level_stop - 1, - tx_level_step):
                self.tx_level = tx_level

                # start to sweep vcc, bias0, bias1
                self.tx_apt_sweep_search(vcc_start, bias0_start, bias1_start, mode=ALGR_MODE)

                # to take over the next level for vcc_start
                vcc_start = self.vcc_new

        elif self.tx_path in ['MIMO']:
            logger.info("MIMO doesn't need this function")
            # for tx_level in range(tx_range_list[0], tx_range_list[1] + step, step):
            #     path_count = 1  # this is for mimo path to store tx_path
            #     for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
            #         self.port_tx = port_tx
            #         self.tx_path_mimo = self.tx_path + f'_{path_count}'
            #         self.tx_level = tx_level
            #         logger.info(f'========Now Tx level = {self.tx_level} dBm========')
            #         self.set_level_fr1(self.tx_level)
            #
            #         # start to sweep vcc, bias0, bias1
            #         self.tx_apt_sweep_search(vcc_start, bias0_start, bias1_start)
            #
            #         # this willuse previous vcc,bias0, bias1 to start sweep
            #         vcc_start = self.candidate[-3]
            #         bias0_start = self.candidate[-2]
            #         bias1_start = self.candidate[-1]

    def loop_tx_test_process(self):
        logger.info(f'========Now Tx level = {self.tx_level} dBm========')
        self.preset_instrument()
        self.set_test_end_fr1()
        self.set_test_mode_fr1()
        self.select_asw_srs_path()
        self.sig_gen_fr1()
        self.sync_fr1()
        self.tx_set_fr1()

    def tx_apt_sweep_search(self, vcc_start, bias0_start, bias1_start, mode=1):
        self.vcc_new = vcc_start
        self.bias0_new = bias0_start
        self.bias1_new = bias1_start

        # to search where the index should be put in apt nv of vcc/bias for HPM/LPM
        max_level_rise = self.get_pa_sw_rise_level(self.band_fr1, self.tx_path, 1)
        self.index_hpm_wanted = 34 - (max_level_rise - self.tx_level)
        self.index_lpm_wanted = 34 - (23 - self.tx_level)

        self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'H', self.index_hpm_wanted, vcc_start)
        self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'H', self.index_hpm_wanted, bias0_start)
        self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'H', self.index_hpm_wanted, bias1_start)
        self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'L', self.index_lpm_wanted, vcc_start)
        self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'L', self.index_lpm_wanted, bias0_start)
        self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'L', self.index_lpm_wanted, bias1_start)

        if mode == 1:
            self.loop_find_bias1(bias1_start)
            self.loop_find_bias0(bias0_start)
            self.loop_find_vcc()

        elif mode == 0:
            self.loop_find_bias0(bias0_start)
            self.loop_find_bias1(bias1_start)
            self.loop_find_vcc()

        # output the lowest current consumption items
        self.apt_sweep_output_best(self.band_fr1, 'H',
                                   [self.tx_level, self.vcc_new, self.bias0_new, self.bias1_new])

    def loop_find_vcc(self):
        count_vcc = self.COUNT_VCC
        for vcc in range(self.vcc_new, self.vcc_stop - 1, - self.vcc_step):
            logger.info(f'Now VCC is {vcc} to run')
            # set nv and calibrate by apt only
            # if self.sw_point_level < self.tx_level * 10:
            self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'H', self.index_hpm_wanted, vcc)
            # time.sleep(0.2)
            # self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)
            # elif self.sw_point_level >= self.tx_level * 10:
            self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'L', self.index_lpm_wanted, vcc)
            # time.sleep(0.2)
            self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)

            # main process
            self.loop_tx_test_process()
            self.aclr_mod_current_results = self.tx_measure_fr1()
            self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
            self.set_test_end_fr1()
            self.aclr_mod_current_results.append(vcc)
            self.aclr_mod_current_results.append(self.bias0_new)
            self.aclr_mod_current_results.append(self.bias1_new)

            logger.debug(
                f'Get the apt result{self.aclr_mod_current_results}, {vcc}, {self.bias0_new}, {self.bias1_new}')
            self.vcc_new, self.bias0_new, self.bias1_new = self.filter_data()
            count_vcc -= 1

            # this is to sync the LPM with HPM and use the best value
            # if 23 >= self.tx_level > self.sw_point_level:
            if self.index_lpm_wanted <= 34:
                self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'L', self.index_lpm_wanted,
                                                self.vcc_new)
            # elif self.sw_point_level > self.tx_level:
            self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'H', self.index_hpm_wanted, self.vcc_new)

            if count_vcc == 0:
                break
            else:
                continue

    def loop_find_bias0(self, bias0_start):
        for bias0 in range(bias0_start, self.bias0_stop - 1, - self.bias0_step):
            logger.info(f'Now Bias0 is {bias0} to run')
            # set nv and calibrate by apt only
            # if self.sw_point_level < self.tx_level * 10:
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'H', self.index_hpm_wanted, bias0)
            # time.sleep(0.2)
            # self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)
            # elif self.sw_point_level >= self.tx_level * 10:
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'L', self.index_lpm_wanted, bias0)
            # time.sleep(0.2)
            self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)

            # main process
            self.loop_tx_test_process()
            self.aclr_mod_current_results = self.tx_measure_fr1()
            self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
            self.set_test_end_fr1()
            self.aclr_mod_current_results.append(self.vcc_new)
            self.aclr_mod_current_results.append(bias0)
            self.aclr_mod_current_results.append(self.bias1_new)

            logger.debug(
                f'Get the apt result{self.aclr_mod_current_results}, {self.vcc_new}, {bias0}, {self.bias1_new}')
            self.vcc_new, self.bias0_new, self.bias1_new = self.filter_data()

        # this is to sync the LPM with HPM and use the best value
        # if 23 >= self.tx_level > self.sw_point_level:
        if self.index_lpm_wanted <= 34:
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'L', self.index_lpm_wanted, self.bias0_new)
        # elif self.sw_point_level > self.tx_level:
        self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'H', self.index_hpm_wanted, self.bias0_new)

    def loop_find_bias1(self, bias1_start):
        for bias1 in range(bias1_start, self.bias1_stop - 1, - self.bias1_step):
            logger.info(f'Now Bias1 is {bias1} to run')
            # set nv and calibrate by apt only
            # if self.sw_point_level < self.tx_level * 10:
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'H', self.index_hpm_wanted, bias1)
            # time.sleep(0.2)
            # self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)
            # elif self.sw_point_level >= self.tx_level * 10:
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'L', self.index_lpm_wanted, bias1)
            # time.sleep(0.2)
            self.apt_calibration_process_fr1(self.band_fr1, self.tx_path, self.tx_freq_fr1)

            # main process
            self.loop_tx_test_process()
            self.aclr_mod_current_results = self.tx_measure_fr1()
            self.aclr_mod_current_results.append(self.measure_current(self.band_fr1))
            self.set_test_end_fr1()
            self.aclr_mod_current_results.append(self.vcc_new)
            self.aclr_mod_current_results.append(self.bias0_new)
            self.aclr_mod_current_results.append(bias1)

            logger.debug(
                f'Get the apt result{self.aclr_mod_current_results}, {self.vcc_new}, {self.bias0_new}, {bias1}')
            self.vcc_new, self.bias0_new, self.bias1_new = self.filter_data()

        # this is to sync the LPM with HPM and use the best value
        # if 23 >= self.tx_level > self.sw_point_level:
        if self.index_lpm_wanted <= 34:
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'L', self.index_lpm_wanted, self.bias1_new)
        # elif self.sw_point_level > self.tx_level:
        self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'H', self.index_hpm_wanted, self.bias1_new)

    def fill_out_rest_vcc_bias(self, level_start, level_stop, band, tx_path):
        max_level_rise = self.get_pa_sw_rise_level(self.band_fr1, self.tx_path, 1)
        rest_hpm2fill_higher_start_index = 34 - (max_level_rise - level_start) + 1
        rest_hpm2fill_lower_stop_index = 34 - (max_level_rise - level_stop)
        rest_lpm2fill_higher_start_index = 34 - (23 - level_start) + 1
        rest_lpm2fill_lower_start_index = 34 - (23 - level_stop)

        # common parameters
        used_band_index = self.get_used_band_index_by_path_fr1(tx_path)
        vcc_nv_hpm = f'CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_HPM_TX{self.tx_path_dict[self.tx_path]}' \
                     f'_N{str(used_band_index[band]).zfill(2)}'
        vcc_nv_lpm = f'CAL.NR_SUB6.TX_APT_DC_TABLE_MIDCH_LPM_TX{self.tx_path_dict[self.tx_path]}' \
                     f'_N{str(used_band_index[band]).zfill(2)}'
        bias0_nv_hpm = f'CAL.NR_SUB6.TX_PA_BIAS0_MIDCH_HPM_TX{self.tx_path_dict[self.tx_path]}' \
                       f'_N{str(used_band_index[band]).zfill(2)}'
        bias0_nv_lpm = f'CAL.NR_SUB6.TX_PA_BIAS0_MIDCH_LPM_TX{self.tx_path_dict[self.tx_path]}' \
                       f'_N{str(used_band_index[band]).zfill(2)}'
        bias1_nv_hpm = f'CAL.NR_SUB6.TX_PA_BIAS1_MIDCH_HPM_TX{self.tx_path_dict[self.tx_path]}' \
                       f'_N{str(used_band_index[band]).zfill(2)}'
        bias1_nv_lpm = f'CAL.NR_SUB6.TX_PA_BIAS1_MIDCH_LPM_TX{self.tx_path_dict[self.tx_path]}' \
                       f'_N{str(used_band_index[band]).zfill(2)}'

        # to fill the rest at hpm higher
        index_upper = 34 - (max_level_rise - level_start)

        vcc_upper = int(self.get_nv_index_value(self.query_google_nv(vcc_nv_hpm))[f'{index_upper - 1}'])
        bias0_upper = int(self.get_nv_index_value(self.query_google_nv(bias0_nv_hpm))[f'{index_upper - 1}'])
        bias1_upper = int(self.get_nv_index_value(self.query_google_nv(bias1_nv_hpm))[f'{index_upper - 1}'])

        for i in range(rest_hpm2fill_higher_start_index, 34 + 1):
            self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'H', i, vcc_upper)
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'H', i, bias0_upper)
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'H', i, bias1_upper)

        # to fill the rest at hpm lower
        index_lower = 34 - (max_level_rise - level_stop)
        vcc_lower = int(self.get_nv_index_value(self.query_google_nv(vcc_nv_hpm))[f'{index_lower - 1}'])
        bias0_lower = int(self.get_nv_index_value(self.query_google_nv(bias0_nv_hpm))[f'{index_lower - 1}'])
        bias1_lower = int(self.get_nv_index_value(self.query_google_nv(bias1_nv_hpm))[f'{index_lower - 1}'])

        for i in range(1, rest_hpm2fill_lower_stop_index):
            self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'H', i, vcc_lower)
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'H', i, bias0_lower)
            self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'H', i, bias1_lower)

        # to fill the rest at lpm higher
        if level_start <= 23:
            index_upper = 34 - (23 - level_start)
            vcc_upper = int(self.get_nv_index_value(self.query_google_nv(vcc_nv_lpm))[f'{index_upper - 1}'])
            bias0_upper = int(self.get_nv_index_value(self.query_google_nv(bias0_nv_lpm))[f'{index_upper - 1}'])
            bias1_upper = int(self.get_nv_index_value(self.query_google_nv(bias1_nv_lpm))[f'{index_upper - 1}'])

            for i in range(rest_lpm2fill_higher_start_index, 34 + 1):
                self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'L', i, vcc_upper)
                self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'L', i, bias0_upper)
                self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'L', i, bias1_upper)

        # to fill the rest at lpm lower
        if level_stop <= 23:
            index_lower = 34 - (23 - level_stop)
            vcc_lower = int(self.get_nv_index_value(self.query_google_nv(vcc_nv_lpm))[f'{index_lower - 1}'])
            bias0_lower = int(self.get_nv_index_value(self.query_google_nv(bias0_nv_lpm))[f'{index_lower - 1}'])
            bias1_lower = int(self.get_nv_index_value(self.query_google_nv(bias1_nv_lpm))[f'{index_lower - 1}'])

            for i in range(1, rest_lpm2fill_lower_start_index):
                self.set_apt_vcc_nv_each_cp_fr1(self.band_fr1, self.tx_path, 'L', i, vcc_lower)
                self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 0, 'L', i, bias0_lower)
                self.set_apt_bias_nv_each_cp_fr1(self.band_fr1, self.tx_path, 1, 'L', i, bias1_lower)


def main():
    start = datetime.datetime.now()

    apt_sweep = AptSweep()
    # apt_sweep.tx_apt_sweep_pipeline_fr1()
    apt_sweep.set_apt_internal_calibration_fr1('TX1', 1950000)
    stop = datetime.datetime.now()

    logger.info(f'Timer: {stop - start}')


if __name__ == '__main__':
    main()
