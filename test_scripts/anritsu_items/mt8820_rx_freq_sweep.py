import time

from equipments.anritsu8820 import Anritsu8820
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
from utils.channel_handler import channel_freq_select
from utils.excel_handler import rx_freq_sweep_power_relative_test_export_excel_sig
from utils.excel_handler import rxs_freq_relative_plot_sig
from utils.log_init import log_set

logger = log_set('8820RxSigSweep')


class RxTestFreqSweep(AtCmd, Anritsu8820):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        Anritsu8820.__init__(self)
        self.ser.com_close()
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.get_temp_en = self.get_temp_en = self.state_dict['get_temp_en']
        self.rx_path = None

    def get_temperature(self):
        """
        for P22, AT+GOOGTHERMISTOR=1,1 for MHB LPAMid/ MHB Rx1 LFEM, AT+GOOGTHERMISTOR=0,1
        for LB LPAMid, MHB ENDC LPAMid, UHB(n77/n79 LPAF)
        :return:
        """
        state = self.get_temp_en
        if state is True:
            self.ser.com_open()
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
            self.ser.com_close()

        else:
            therm_list = [None, None]

        return therm_list

    def rx_sweep_core(self, standard, band, dl_ch, bw=None):
        conn_state = int(self.get_calling_state_query())
        if standard == 'LTE':
            if conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                self.set_init_before_calling(standard, dl_ch, bw)
                self.set_registration_calling(standard)
        elif standard == 'WCDMA':
            if conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                self.set_init_before_calling(standard, dl_ch, bw)
                self.set_registration_calling(standard)

        if standard == 'LTE':
            logger.info(f'Start to sweep B{band}, bandwidth: {bw} MHz, downlink_chan: {dl_ch}')
        elif standard == 'WCDMA':
            logger.info(f'Start to sweep B{band}, downlink_chan: {dl_ch}')

        self.set_init_rx(standard)

        for power_selected in self.state_dict['ue_power_list']:
            self.set_rf_out_port(self.state_dict['rfout_port_sig_anritsu'])
            if power_selected == 1:
                self.tx_level = self.state_dict['tx_level']
                self.set_tpc('ALL1')
                self.set_input_level(self.tx_level + 3)

                # if rx_path is used by checking box methoc, or it is used by rf out
                if isinstance(self.rx_path, int):
                    if standard == 'LTE':
                        self.rx_path_setting_sig_lte()
                    elif standard == 'WCDMA':
                        self.rx_path_setting_sig_wcdma()

                sens_list = self.get_sensitivity(standard, band, dl_ch, bw)  # sens_list = [power, sensitivity, per]
                logger.debug(f'Sensitivity list:{sens_list}')
                self.parameters_dict = {
                    'tech': standard,
                    'bw': bw,
                    'band': band,
                    'dl_ch': dl_ch,
                    'tx_level': self.tx_level,
                    'rx_path': self.rx_path,
                    'rb_size': self.get_ul_rb_size_query(standard),
                    'rb_start': self.get_ul_rb_start_query(standard),
                    'thermal': self.get_temperature(),
                    'mcs': 'QPSK',
                    'tx_freq': self.get_ul_freq_query(),

                }
                self.excel_path = rx_freq_sweep_power_relative_test_export_excel_sig(sens_list, self.parameters_dict)
                self.set_output_level(-70)

            elif power_selected == 0:
                self.tx_level = -10
                if standard == 'LTE':
                    self.set_tpc('AUTO')
                elif standard == 'WCDMA':
                    self.set_tpc('ILPC')
                self.set_input_level(self.tx_level)

                # if rx_path is used by checking box methoc, or it is used by rf out
                if isinstance(self.rx_path, int):
                    if standard == 'LTE':
                        self.rx_path_setting_sig_lte()
                    elif standard == 'WCDMA':
                        self.rx_path_setting_sig_wcdma()

                sens_list = self.get_sensitivity(standard, band, dl_ch, bw)
                logger.debug(f'Sensitivity list:{sens_list}')
                self.parameters_dict = {
                    'tech': standard,
                    'bw': bw,
                    'band': band,
                    'dl_ch': dl_ch,
                    'tx_level': -10,
                    'rx_path': self.rx_path,
                    'rb_size': self.get_ul_rb_size_query(standard),
                    'rb_start': self.get_ul_rb_start_query(standard),
                    'thermal': self.get_temperature(),
                    'mcs': 'QPSK',
                    'tx_freq': self.get_ul_freq_query(),
                }
                self.excel_path = rx_freq_sweep_power_relative_test_export_excel_sig(sens_list, self.parameters_dict)
                self.set_output_level(-70)
            self.set_rf_out_port('MAIN')

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1

    def run(self):
        self.set_rf_out_port('MAIN')
        for tech in self.state_dict['tech_list']:
            if tech == 'LTE' and self.state_dict['lte_bands_list'] != []:
                standard = self.set_switch_to_lte()
                logger.info(standard)
                self.chcoding = None
                try:
                    for bw in self.state_dict['lte_bw_list']:
                        for band in self.state_dict['lte_bands_list']:
                            if self.state_dict['rx_path_list']:
                                for rx_path in self.state_dict['rx_path_list']:
                                    self.rx_path = rx_path
                                    if bw in cm_pmt_anritsu.bandwidths_selected(band):
                                        self.set_test_parameter_normal()
                                        lch = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[0]  # lch
                                        hch = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[2]  # hch
                                        step = cm_pmt_anritsu.SWEEP_STEP
                                        if cm_pmt_anritsu.CHAN_LIST:
                                            ch_list = cm_pmt_anritsu.CHAN_LIST
                                        else:
                                            ch_list = range(lch, hch + 1, step)

                                        for dl_ch in ch_list:
                                            self.rx_sweep_core(standard, band, dl_ch, bw)

                                        time.sleep(1)
                            else:
                                self.rx_path = self.state_dict['rfout_port_sig_anritsu']
                                if bw in cm_pmt_anritsu.bandwidths_selected(band):
                                    self.set_test_parameter_normal()
                                    lch = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[0]  # lch
                                    hch = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)[2]  # hch
                                    step = cm_pmt_anritsu.SWEEP_STEP
                                    if cm_pmt_anritsu.CHAN_LIST:
                                        ch_list = cm_pmt_anritsu.CHAN_LIST
                                    else:
                                        ch_list = range(lch, hch + 1, step)

                                    for dl_ch in ch_list:
                                        self.rx_sweep_core(standard, band, dl_ch, bw)

                                    time.sleep(1)

                                else:
                                    logger.info(f'B{band} do not have BW {bw}MHZ')
                                    skip_count = len(self.state_dict['channel_str']) * len(
                                        self.state_dict['ue_power_list'])
                                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                                    self.state_dict['progressBar_progress'] += skip_count

                except Exception as err:
                    logger.debug(err)
                    logger.info('Rx path is unchecked')
                    logger.info('It might forget to choose Band or Channel or BW or others')

                else:
                    # rx_desense_process_sig(standard, self.excel_path)
                    # rxs_relative_plot_sig(standard, self.excel_path, self.parameters_dict)
                    rxs_freq_relative_plot_sig(self.excel_path, self.parameters_dict)

            elif tech == 'WCDMA' and self.state_dict['wcdma_bands_list'] != []:
                standard = self.set_switch_to_wcdma()
                self.chcoding = 'REFMEASCH'
                try:
                    for band in self.state_dict['wcdma_bands_list']:
                        if self.state_dict['rx_path_list']:
                            for rx_path in self.state_dict['rx_path_list']:
                                self.rx_path = rx_path
                                lch = cm_pmt_anritsu.dl_ch_selected(standard, band)[0]  # lch
                                hch = cm_pmt_anritsu.dl_ch_selected(standard, band)[2]  # hch
                                step = cm_pmt_anritsu.SWEEP_STEP
                                if cm_pmt_anritsu.CHAN_LIST:
                                    ch_list = cm_pmt_anritsu.CHAN_LIST
                                else:
                                    ch_list = range(lch, hch + 1, step)

                                for dl_ch in ch_list:
                                    self.rx_sweep_core(standard, band, dl_ch, 5)

                        else:
                            self.rx_path = self.state_dict['rfout_port_sig_anritsu']
                            lch = cm_pmt_anritsu.dl_ch_selected(standard, band)[0]  # lch
                            hch = cm_pmt_anritsu.dl_ch_selected(standard, band)[2]  # hch
                            step = cm_pmt_anritsu.SWEEP_STEP
                            if cm_pmt_anritsu.CHAN_LIST:
                                ch_list = cm_pmt_anritsu.CHAN_LIST
                            else:
                                ch_list = range(lch, hch + 1, step)

                            for dl_ch in ch_list:
                                self.rx_sweep_core(standard, band, dl_ch, 5)


                except Exception as err:
                    logger.debug(err)
                    logger.info('Rx path is unchecked')
                    logger.info('It might forget to choose Band or Channel or BW or others')

                else:
                    # rx_desense_process_sig(standard, self.excel_path)
                    # rxs_relative_plot_sig(standard, self.excel_path, self.parameters_dict)
                    rxs_freq_relative_plot_sig(self.excel_path, self.parameters_dict)

            elif tech == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                pass
            else:
                logger.info(f'Finished')
