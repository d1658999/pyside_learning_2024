from pathlib import Path
import math

from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
import utils.parameters.rb_parameters as scrpt_set
from utils.loss_handler import get_loss
from utils.excel_handler import rxs_relative_plot_ftm, rxs_endc_plot_ftm, rx_power_endc_test_export_excel_ftm
from utils.excel_handler import rx_power_relative_test_export_excel_ftm, rx_desense_process_ftm
from utils.excel_handler import rx_desense_endc_process_ftm, select_file_name_rx_ftm, excel_folder_path
from utils.channel_handler import channel_freq_select
from exception.custom_exception import FileNotFoundException, PortTableException
from utils.excel_handler import color_format_nr_sens_ftm, color_format_lte_sens_ftm


logger = log_set('rx_lmh')
SDL_BANDS = [29, 32, 46, 75, 76]


class RxTestGenre(AtCmd, CMW100):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.power_endc_lte = None
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.sa_nsa_mode = None
        self.rx_quick_test_enable = state_dict['rx_quick_ns']
        self.tx_freq_wcdma = None
        self.file_path = None
        self.power_monitor_endc_lte = None
        self.power_endc_nr = None
        self.chan_rb = None
        self.band_combo = None
        self.port_tx_nr = None
        self.port_tx_lte = None
        self.tx_level_endc_nr = None
        self.tx_level_endc_lte = None
        self.mcs_wcdma = None
        self.ue_power_bool = None
        self.chan = None
        self.resolution = None
        self.port_table = None

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

    def get_temperature(self, state=False):
        """
        for P22, AT+GOOGTHERMISTOR=1,1 for MHB LPAMid/ MHB Rx1 LFEM, AT+GOOGTHERMISTOR=0,1
        for LB LPAMid, MHB ENDC LPAMid, UHB(n77/n79 LPAF)
        :return:
        """
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

    # def query_rx_measure_wcdma(self):
    #     self.query_rsrp_cinr_wcdma()
    #     self.query_agc_wcdma()
    #     self.get_esens_wcdma()

    def query_rx_measure_lte(self):
        self.query_rsrp_cinr_lte()
        self.query_agc_lte()
        self.get_esens_lte()

    def query_rx_measure_nr(self):
        self.query_rsrp_cinr_nr()
        self.query_agc_nr()
        self.get_esens_nr()

    def query_fer_measure_gsm(self):
        self.sig_gen_gsm()
        self.sync_gsm()
        self.query_rssi_measure_gsm()

    def search_process_nr(self):
        self.query_fer_measure_nr()
        while self.fer < 500:
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            self.set_rx_level_search()
            self.query_fer_measure_nr()
            # self.command_cmw100_query('*OPC?')

    def search_process_lte(self):
        self.query_fer_measure_lte()
        while self.fer < 500:
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            self.set_rx_level_search()
            self.query_fer_measure_lte()
            # self.command_cmw100_query('*OPC?')

    def search_process_wcdma(self):
        self.query_fer_measure_wcdma()
        while self.fer < 100:
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            self.set_rx_level_search()
            self.query_fer_measure_wcdma()
            # self.command_cmw100_query('*OPC?')

    def search_process_gsm(self):
        self.query_fer_measure_gsm()
        rssi = self.rssi
        while self.fer < 2:
            rssi = self.rssi
            self.rx_level = round(self.rx_level - self.resolution, 1)  # to reduce a unit
            # self.set_rx_level()
            self.query_fer_measure_gsm()
        return rssi
        # self.command_cmw100_query('*OPC?')

    def search_sensitivity_nr(self):
        reset_rx_level = -80
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_nr()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = coarse_2
        self.search_process_nr()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = fine
        self.search_process_nr()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        logger.info(f'Final Rx Level: {self.rx_level}')

        return self.rx_level

    def search_sensitivity_lte(self):
        reset_rx_level = -80
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_lte()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = coarse_2
        self.search_process_lte()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = fine
        self.search_process_lte()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        logger.info(f'Final Rx Level: {self.rx_level}')

        return self.rx_level

    def search_sensitivity_wcdma(self):
        reset_rx_level = -106
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_wcdma()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = coarse_2
        self.search_process_wcdma()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        self.set_rx_level_search()
        self.resolution = fine
        self.search_process_wcdma()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        logger.info(f'Final Rx Level: {self.rx_level}')

    def search_sensitivity_gsm(self):
        reset_rx_level = -104
        self.rx_level = reset_rx_level
        coarse_1 = 2
        coarse_2 = 1
        fine = 0.2
        logger.info('----------Search RX Level----------')
        self.resolution = coarse_1
        self.search_process_gsm()  # first time by coarse_1
        logger.info('Second time to search')
        self.rx_level += coarse_1 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        # self.set_rx_level()
        self.resolution = coarse_2
        self.search_process_gsm()  # second time by coarse_2
        logger.info('Third time to search')
        self.rx_level += coarse_2 * 2
        logger.info(f'==========Back to Search: {self.rx_level} dBm==========')
        # self.set_rx_level()
        self.resolution = fine
        rssi = self.search_process_gsm()  # second time by fine
        self.rx_level = round(self.rx_level + fine, 1)
        self.rssi = rssi
        logger.info(f'Final Rx Level: {self.rx_level}')
        logger.info(f'Final RSSI: {self.rssi}')
        self.command('AT+TESTRESET')

    def search_sensitivity_pipline_nr(self):
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.type_nr = 'DFTS'
        self.mcs_nr = 'QPSK'
        items = [
            (tech, tx_path, bw, ue_power_bool, band)
            for tech in self.state_dict['tech_list']
            for tx_path in self.state_dict['tx_path_list']
            for bw in self.state_dict['nr_bw_list']
            for band in self.state_dict['nr_bands_list']
            for ue_power_bool in self.state_dict['ue_power_list']
        ]
        for item in items:
            if item[0] == 'NR' and self.state_dict['nr_bands_list'] != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_nr = item[2]
                self.ue_power_bool = item[3]
                self.tx_level = self.state_dict['tx_level'] if self.ue_power_bool == 1 else -10
                self.band_nr = item[4]
                self.port_table_selector(self.band_nr, self.tx_path)

                if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                    self.search_sensitivity_lmh_process_nr()
                else:
                    logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')

        for bw in self.state_dict['nr_bw_list']:
            try:
                parameters = {
                    'tech': 'NR',
                    'mcs': self.mcs_nr,
                }
                # self.bw_nr = bw
                file_name = select_file_name_rx_ftm(bw, 'NR')
                file_path = Path(excel_folder_path()) / Path(file_name)
                rx_desense_process_ftm(file_path, self.mcs_nr)
                rxs_relative_plot_ftm(file_path, parameters)
                color_format_nr_sens_ftm(file_path)

            except TypeError as err:
                logger.debug(err)
                logger.info(
                    'It might not have the Bw in this Band, so it cannot to be calculated for desens')
            except KeyError as err:
                logger.debug(err)
                logger.info(
                    f"N{self.band_nr} doesn't have this BW{self.bw_nr}, so desens progress cannot run")
            except FileNotFoundError as err:
                logger.debug(err)
                logger.info(f"There is not file to plot BW{bw}")

    def search_sensitivity_pipline_lte(self):
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mcs_lte = 'QPSK'
        items = [
            (tech, tx_path, bw, ue_power_bool, band)
            for tech in self.state_dict['tech_list']
            for tx_path in self.state_dict['tx_path_list']
            for bw in self.state_dict['lte_bw_list']
            for band in self.state_dict['lte_bands_list']
            for ue_power_bool in self.state_dict['ue_power_list']
        ]
        for item in items:
            if item[0] == 'LTE' and self.state_dict['lte_bands_list'] != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.bw_lte = item[2]
                self.ue_power_bool = item[3]
                self.tx_level = self.state_dict['tx_level'] if self.ue_power_bool == 1 else -10
                self.band_lte = item[4]
                self.port_table_selector(self.band_lte, self.tx_path)

                if self.bw_lte in cm_pmt_ftm.bandwidths_selected_lte(self.band_lte):
                    self.search_sensitivity_lmh_process_lte()
                else:
                    logger.info(f'B{self.band_lte} does not have BW {self.bw_lte}MHZ')

        for bw in self.state_dict['lte_bw_list']:
            try:
                parameters = {
                    'tech': 'LTE',
                    'mcs': self.mcs_lte,
                }
                # self.bw_lte = bw
                file_name = select_file_name_rx_ftm(bw, 'LTE')
                file_path = Path(excel_folder_path()) / Path(file_name)
                rx_desense_process_ftm(file_path, self.mcs_lte)
                rxs_relative_plot_ftm(file_path, parameters)
                color_format_lte_sens_ftm(file_path)

            except TypeError as err:
                logger.debug(err)
                logger.info(
                    'It might not have the Bw in this Band, so it cannot to be calculated for desens')
            except KeyError as err:
                logger.debug(err)
                logger.info(
                    f"B{self.band_lte} doesn't have this BW{self.bw_lte}, so desens progress cannot run")
            except FileNotFoundError as err:
                logger.debug(err)
                logger.info(f"There is not file to plot BW{bw}")

    def search_sensitivity_pipline_wcdma(self):
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mcs_wcdma = 'QPSK'
        self.script = 'GENERAL'
        items = [
            (tech, tx_path, band)
            for tech in self.state_dict['tech_list']
            for tx_path in self.state_dict['tx_path_list']
            for band in self.state_dict['wcdma_bands_list']
        ]
        for item in items:
            if item[0] == 'WCDMA' and self.state_dict['wcdma_bands_list'] != []:
                self.tech = item[0]
                self.tx_path = item[1]
                self.band_wcdma = item[2]
                self.port_table_selector(self.band_wcdma)
                self.search_sensitivity_lmh_process_wcdma()
        # file_name = f'Sensitivty_5MHZ_{self.tech}_LMH.xlsx'
        # file_path = Path(excel_folder_path()) / Path(file_name)
        parameters = {
            'tech': self.tech,
            'mcs': self.mcs_wcdma,
        }
        rxs_relative_plot_ftm(self.file_path, parameters)

    def search_sensitivity_pipline_gsm(self):
        self.port_tx = self.state_dict['tx_port']
        self.chan = self.state_dict['channel_str']
        self.mod_gsm = self.state_dict['gsm_modulation']
        items = [
            (tech, band)
            for tech in self.state_dict['tech_list']
            for band in self.state_dict['gsm_bands_list']
        ]
        for item in items:
            if item[0] == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                self.tech = item[0]
                self.band_gsm = item[1]
                self.port_table_selector(self.band_gsm)
                self.pcl = self.state_dict['pcl_lb_level'] if self.band_gsm in [850, 900] else self.state_dict['pcl_mb_level']
                self.search_sensitivity_lmh_process_gsm()
        # file_name = f'Sensitivty_0MHZ_{self.tech}_LMH.xlsx'
        # file_path = Path(excel_folder_path()) / Path(file_name)
        parameters = {
            'tech': self.tech,
            'mcs': 'GMSK',
        }
        rxs_relative_plot_ftm(self.file_path, parameters)

    def search_sensitivity_pipline_endc(self):
        self.tx_level_endc_lte = self.state_dict['tx_level_lte_endc']
        self.tx_level_endc_nr = self.state_dict['tx_level_nr_endc']
        self.port_tx_lte = self.state_dict['tx_port_endc_lte']
        self.port_tx_nr = self.state_dict['tx_port']
        self.type_nr = 'DFTS'
        self.mcs_lte = self.mcs_nr = 'QPSK'
        self.tx_path = None
        self.rx_path_lte = None
        self.rx_path_nr = None
        file_path = None

        items = [
            ('ENDC', band_combo, bw_lte, bw_nr, chan_rb, ue_power_bool, rx_path_lte, rx_path_nr)
            # for tech in ext_pmt.tech
            for band_combo in self.state_dict['endc_bands_list']
            for bw_lte in scrpt_set.ENDC[band_combo]
            for bw_nr in scrpt_set.ENDC[band_combo][bw_lte]
            for chan_rb in scrpt_set.ENDC[band_combo][bw_lte][bw_nr]
            for rx_path_lte in self.state_dict['endc_lte_rx_path_list']
            for rx_path_nr in self.state_dict['endc_nr_rx_path_list']
            for ue_power_bool in self.state_dict['ue_power_list']
        ]

        items_counts = len(items)
        prog_max_value = self.progressBar.maximum()
        new_prog_max_value = prog_max_value + items_counts - 1
        self.progressBar.setMaximum(new_prog_max_value)

        # data = []
        for item in items:
            self.band_combo = item[1]
            self.bw_lte = item[2]
            self.bw_nr = item[3]
            self.chan_rb = item[4]
            self.ue_power_bool = item[5]
            self.rx_path_lte = item[6]
            self.rx_path_nr = item[7]
            [band_lte_str, band_nr_str] = self.band_combo.split('_')
            self.band_lte = int(band_lte_str)
            self.band_nr = int(band_nr_str)
            (self.tx_freq_lte, self.tx_freq_nr) = self.chan_rb[0]
            (self.rb_size_lte, self.rb_start_lte) = self.chan_rb[1]
            (self.rb_size_nr, self.rb_start_nr) = self.chan_rb[2]
            self.tx_freq_lte = int(self.tx_freq_lte * 1000)
            self.tx_freq_nr = int(self.tx_freq_nr * 1000)
            loss_tx_lte = self.loss_selector(self.tx_freq_lte, self.state_dict['fdc_en'])
            loss_tx_nr = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
            self.rx_freq_nr = cm_pmt_ftm.transfer_freq_tx2rx_nr(self.band_nr, self.tx_freq_nr)
            self.rx_freq_lte = cm_pmt_ftm.transfer_freq_tx2rx_lte(self.band_lte, self.tx_freq_lte)
            self.preset_instrument()

            # set end at initial
            self.set_test_end_lte(delay=0.5)
            self.set_test_end_nr(delay=0.5)
            self.rx_level = self.state_dict['init_rx_sync_level']

            # sync lte
            self.set_test_mode_lte()
            self.loss_rx = self.loss_selector(self.rx_freq_lte, self.state_dict['fdc_en'])
            self.sig_gen_lte()
            self.sync_lte()

            # sync fr1
            self.set_test_mode_nr()
            self.loss_rx = self.loss_selector(self.rx_freq_nr, self.state_dict['fdc_en'])
            self.sig_gen_nr()
            self.sync_nr()

            # set LTE power
            self.tx_level = self.tx_level_endc_lte if self.ue_power_bool == 1 else -10
            self.loss_tx = loss_tx_lte
            self.port_tx = self.port_tx_lte
            self.tx_path = self.state_dict['endc_lte_tx_path']
            self.tx_set_lte()
            self.tech = 'LTE'
            self.antenna_switch_v2()
            self.rx_path_setting_lte()

            # lte tx measurement by fbrx power
            self.port_tx = self.port_tx_lte
            self.state_dict['fbrx_en'] = True
            self.power_endc_lte = round(self.query_fbrx_power('LTE')[0], 2)  # modulation power
            logger.info(f'LTE FBRX Power: {self.power_endc_lte}')

            # set FR1 power
            self.tx_level = self.tx_level_endc_nr
            self.loss_tx = loss_tx_nr
            self.port_tx = self.port_tx_nr
            self.tx_path = self.state_dict['endc_nr_tx_path']
            self.tx_set_nr()
            self.tech = 'NR'
            self.antenna_switch_v2()
            self.rx_path_setting_nr()

            # FR1 tx measurement
            self.port_tx = self.port_tx_nr
            fbrx_power_nr = self.query_fbrx_power('NR')[0]
            logger.debug(fbrx_power_nr)
            logger.info(f'FR1 FBRX Power: {fbrx_power_nr}')  # modulation power
            self.power_endc_nr = round(fbrx_power_nr, 2)

            # FR1 RxS
            # rxs_nr = self.search_sensitivity_nr()
            self.query_rx_measure_nr()
            rxs_nr = self.esens_list  # [rx0, rx1, rx2, rx3]
            # # set LTE power and get ENDC power for LTE
            # self.tx_level = ext_pmt.tx_level_endc_lte if self.ue_power_bool == 1 else -10
            # self.loss_tx = loss_tx_lte
            # self.port_tx = self.port_tx_lte
            # self.power_monitor_endc_lte = self.tx_monitor_lte()

            # LTE sync2
            self.rx_level = -70
            self.loss_rx = self.loss_selector(self.rx_freq_lte, self.state_dict['fdc_en'])
            self.sig_gen_lte()
            self.sync_lte()

            # FR1 tx set
            self.tx_path = self.state_dict['endc_nr_tx_path']
            self.tx_level = self.tx_level_endc_nr
            self.tx_set_nr()
            self.tech = 'NR'
            self.antenna_switch_v2()
            self.rx_path_setting_nr()

            # LTE tx set
            self.tx_level = self.tx_level_endc_lte if self.ue_power_bool == 1 else -10
            self.loss_tx = loss_tx_lte
            self.port_tx = self.port_tx_lte
            self.tx_path = self.state_dict['endc_lte_tx_path']
            self.tx_set_lte()
            self.tech = 'LTE'
            self.antenna_switch_v2()
            self.rx_path_setting_lte()

            # LTE RxS
            self.query_rx_measure_lte()
            rxs_lte = self.esens_list[0]  # [rx0, rx1, rx2, rx3]

            # save data to excel
            data = [
                int(self.band_lte), int(self.band_nr),
                self.power_endc_lte, self.power_endc_nr,
                rxs_lte, rxs_nr[0], rxs_nr[1], rxs_nr[2], rxs_nr[3],
                self.bw_lte, self.bw_nr,
                self.tx_freq_lte, self.tx_freq_nr,
                self.tx_level, self.tx_level_endc_nr,
                self.rb_size_lte, self.rb_start_lte,
                self.rb_size_nr, self.rb_start_nr,
                'RX0',
                # self.rx_path_lte_dict[self.rx_path_lte],
            ]

            self.set_test_end_nr(delay=0.5)
            self.set_test_end_lte(delay=0.5)
            if data:
                file_path = rx_power_endc_test_export_excel_ftm(data)

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1

        # file_name = 'Sensitivty_ENDC.xlsx'
        # file_path = Path(excel_folder_path()) / Path(file_name)
        if file_path is not None:
            rx_desense_endc_process_ftm(file_path)
            rxs_endc_plot_ftm(file_path)
        else:
            logger.info('please check the test items that are not selected')

    def search_sensitivity_lmh_process_nr(self):
        # [L_rx_freq, M_rx_ferq, H_rx_freq]
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr, self.bw_nr)

        rx_freq_select_list = sorted(set(channel_freq_select(self.chan, rx_freq_list)))

        for rx_path in self.state_dict['rx_path_list']:
            self.rx_path_nr = rx_path

            for rx_freq in rx_freq_select_list:
                # self.rx_level = -70
                self.rx_level_select_nr()  # this is determination of rx if fast test is enable
                self.rx_freq_nr = rx_freq
                self.tx_freq_nr = cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, self.rx_freq_nr)
                self.loss_rx = self.loss_selector(self.rx_freq_nr, self.state_dict['fdc_en'])
                self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
                logger.info('----------Test LMH progress---------')
                self.preset_instrument()
                self.set_test_end_nr()
                self.set_test_mode_nr()
                # self.command_cmw100_query('*OPC?')
                self.sig_gen_nr()
                self.sync_nr()
                self.rx_path_setting_nr()
                if self.band_nr not in SDL_BANDS:
                    self.rb_size_nr, self.rb_start_nr = cm_pmt_ftm.special_uplink_config_sensitivity_nr(
                        self.band_nr,
                        self.scs,
                        self.bw_nr)  # for RB set(including special tx setting)
                    self.antenna_switch_v2()
                    self.tx_set_nr()
                    # aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET
                    aclr_mod_results = self.tx_measure_nr()
                    measured_power = round(aclr_mod_results[3], 1)
                else:
                    measured_power = None
                # self.command_cmw100_query('*OPC?')
                self.sensitivity_solution_select_nr()
                logger.info(f'Power: {measured_power}, Sensitivity: {self.rx_level}')

                # measured_power, measured_rx_level, rsrp_list, cinr_list, agc_list, thermistor_list
                if self.rx_quick_test_enable:
                    data_quick = {}
                    for rp, esens in enumerate(self.esens_list):
                        data_quick[self.tx_freq_nr] = [measured_power, esens, self.rsrp_list, self.cinr_list,
                                                 self.agc_list, self.get_temperature()]
                        parameters = {
                            'tech': self.tech,
                            'band': self.band_nr,
                            'bw': self.bw_nr,
                            'tx_level': self.tx_level,
                            'mcs': self.mcs_nr,
                            'tx_path': self.tx_path,
                            'rx_path': f'RX{rp}',
                            'rb_size': self.rb_size_nr,
                            'rb_start': self.rb_start_nr,
                        }
                        self.file_path = rx_power_relative_test_export_excel_ftm(data_quick, parameters)

                else:
                    data_normal = {}
                    rsrp_list = [None, None, None, None]
                    cinr_list = [None, None, None, None]
                    agc_list = [None, None, None, None]

                    data_normal[self.tx_freq_nr] = [measured_power, self.rx_level, rsrp_list, cinr_list,
                                          agc_list, self.get_temperature()]
                    self.set_test_end_nr()
                    parameters = {
                        'tech': self.tech,
                        'band': self.band_nr,
                        'bw': self.bw_nr,
                        'tx_level': self.tx_level,
                        'mcs': self.mcs_nr,
                        'tx_path': self.tx_path,
                        'rx_path': rx_path,
                        'rb_size': self.rb_size_nr,
                        'rb_start': self.rb_start_nr,
                    }
                    self.file_path = rx_power_relative_test_export_excel_ftm(data_normal, parameters)

                self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                self.state_dict['progressBar_progress'] += 1

    def search_sensitivity_lmh_process_lte(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('LTE', self.band_lte,
                                                   self.bw_lte)  # [L_rx_freq, M_rx_ferq, H_rx_freq]

        rx_freq_select_list = sorted(set(channel_freq_select(self.chan, rx_freq_list)))

        for rx_path in self.state_dict['rx_path_list']:
            self.rx_path_lte = rx_path
            for rx_freq in rx_freq_select_list:
                # self.rx_level = -70
                self.rx_level_select_lte()  # this is determination of rx if fast test is enable
                self.rx_freq_lte = rx_freq
                self.tx_freq_lte = cm_pmt_ftm.transfer_freq_rx2tx_lte(self.band_lte, self.rx_freq_lte)
                self.loss_rx = self.loss_selector(self.rx_freq_lte, self.state_dict['fdc_en'])
                self.loss_tx = self.loss_selector(self.tx_freq_lte, self.state_dict['fdc_en'])
                logger.info('----------Test LMH progress---------')
                self.preset_instrument()
                self.set_test_end_lte()
                self.set_test_mode_lte()
                # self.command_cmw100_query('*OPC?')
                self.sig_gen_lte()
                self.sync_lte()
                self.rx_path_setting_lte()
                if self.band_lte not in SDL_BANDS:
                    self.rb_size_lte, self.rb_start_lte = cm_pmt_ftm.special_uplink_config_sensitivity_lte(
                        self.band_lte,
                        self.bw_lte)  # for RB set
                    self.antenna_switch_v2()
                    self.tx_set_lte()
                    aclr_mod_results = self.tx_measure_lte()  # aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr,
                    measured_power = round(aclr_mod_results[3], 1)
                else:
                    measured_power = None
                # E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET
                # self.command_cmw100_query('*OPC?')
                # self.search_sensitivity_lte()
                # self.query_rx_measure_lte()
                self.sensitivity_solution_select_lte()
                logger.info(f'Power: {measured_power}, Sensitivity: {self.rx_level}')

                # measured_power, measured_rx_level, rsrp_list, cinr_list, agc_list, thermistor_list
                if self.rx_quick_test_enable:
                    data_quick = {}
                    for rp, esens in enumerate(self.esens_list):
                        data_quick[self.tx_freq_lte] = [measured_power, esens, self.rsrp_list, self.cinr_list,
                                                 self.agc_list, self.get_temperature()]
                        parameters = {
                            'tech': self.tech,
                            'band': self.band_lte,
                            'bw': self.bw_lte,
                            'tx_level': self.tx_level,
                            'mcs': self.mcs_lte,
                            'tx_path': self.tx_path,
                            'rx_path': f'RX{rp}',
                            'rb_size': self.rb_size_lte,
                            'rb_start': self.rb_start_lte,
                        }
                        self.file_path = rx_power_relative_test_export_excel_ftm(data_quick, parameters)

                else:
                    data_normal = {}
                    rsrp_list = [None, None, None, None]
                    cinr_list = [None, None, None, None]
                    agc_list = [None, None, None, None]

                    data_normal[self.tx_freq_lte] = [measured_power, self.rx_level, rsrp_list, cinr_list,
                                          agc_list, self.get_temperature()]
                    self.set_test_end_nr()
                    parameters = {
                        'tech': self.tech,
                        'band': self.band_nr,
                        'bw': self.bw_nr,
                        'tx_level': self.tx_level,
                        'mcs': self.mcs_nr,
                        'tx_path': self.tx_path,
                        'rx_path': rx_path,
                        'rb_size': self.rb_size_nr,
                        'rb_start': self.rb_start_nr,
                    }
                    self.file_path = rx_power_relative_test_export_excel_ftm(data_normal, parameters)

                self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                self.state_dict['progressBar_progress'] += 1

    def search_sensitivity_lmh_process_wcdma(self):
        rx_chan_list = cm_pmt_ftm.dl_chan_select_wcdma(self.band_wcdma)
        tx_chan_list = [cm_pmt_ftm.transfer_chan_rx2tx_wcdma(self.band_wcdma, rx_chan) for rx_chan in rx_chan_list]
        tx_rx_chan_list = list(zip(tx_chan_list, rx_chan_list))  # [(tx_chan, rx_chan),...]

        tx_rx_chan_select_list = channel_freq_select(self.chan, tx_rx_chan_list)

        self.preset_instrument()
        for rx_path in self.state_dict['rx_path_list']:
            self.rx_path_wcdma = rx_path
            if self.rx_path_wcdma in [1, 2, 3, 15]:
                data = {}
                for tx_rx_chan_wcdma in tx_rx_chan_select_list:
                    self.rx_level = -70
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_wcdma = tx_rx_chan_wcdma[1]
                    self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    self.rx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.rx_chan_wcdma,
                                                                             'rx')
                    self.tx_freq_wcdma = cm_pmt_ftm.transfer_chan2freq_wcdma(self.band_wcdma, self.tx_chan_wcdma,
                                                                             'tx')
                    self.loss_rx = self.loss_selector(self.rx_freq_wcdma, self.state_dict['fdc_en'])
                    self.loss_tx = self.loss_selector(self.tx_freq_wcdma, self.state_dict['fdc_en'])
                    self.set_test_end_wcdma()
                    self.set_test_mode_wcdma()
                    self.cmw_query('*OPC?')
                    self.rx_path_setting_wcdma()
                    self.sig_gen_wcdma()
                    self.sync_wcdma()
                    self.antenna_switch_v2()
                    # self.tx_chan_wcdma = tx_rx_chan_wcdma[0]
                    # self.tx_set_wcdma()
                    # aclr_mod_results = self.tx_measure_wcdma()
                    # logger.debug(aclr_mod_results)
                    # data[self.tx_chan_wcdma] = aclr_mod_results
                    self.search_sensitivity_wcdma()
                    data[self.rx_chan_wcdma] = self.rx_level
                    # self.query_rx_measure_wcdma()
                    # logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.rx_level}')
                    # data[self.tx_freq_lte] = [aclr_mod_results[3], self.rx_level, self.rsrp_list, self.cinr_list,
                    #                           self.agc_list]  # measured_power, measured_rx_level, rsrp_list
                    #                           , cinr_list, agc_list
                    self.set_test_end_wcdma()
                parameters = {
                    'tech': self.tech,
                    'band': self.band_wcdma,
                    'bw': 5,
                    'tx_level': self.tx_level,
                    'mcs': 'QPSK',
                    'tx_path': self.tx_path,
                    'rx_path': rx_path,
                }
                self.file_path = rx_power_relative_test_export_excel_ftm(data, parameters)
            else:
                logger.info(f"WCDMA doesn't have this RX path {self.rx_path_wcdma_dict[self.rx_path_wcdma]}")
                continue

    def search_sensitivity_lmh_process_gsm(self):
        rx_chan_list = cm_pmt_ftm.dl_chan_select_gsm(self.band_gsm)

        rx_chan_select_list = channel_freq_select(self.chan, rx_chan_list)

        self.preset_instrument()
        self.set_test_mode_gsm()
        self.set_test_end_gsm()

        for rx_path in self.state_dict['rx_path_list']:
            self.rx_path_gsm = rx_path
            if self.rx_path_gsm in [1, 2]:
                data = {}
                for rx_chan_gsm in rx_chan_select_list:
                    self.rx_level = -70
                    logger.info('----------Test LMH progress---------')
                    self.rx_chan_gsm = rx_chan_gsm
                    self.rx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'rx')
                    self.tx_freq_gsm = cm_pmt_ftm.transfer_chan2freq_gsm(self.band_gsm, self.rx_chan_gsm, 'tx')
                    self.loss_rx = self.loss_selector(self.rx_freq_gsm, self.state_dict['fdc_en'])
                    self.loss_tx = self.loss_selector(self.tx_freq_gsm, self.state_dict['fdc_en'])
                    self.set_test_mode_gsm()
                    self.rx_path_setting_gsm()
                    self.sig_gen_gsm()
                    self.sync_gsm()
                    # self.antenna_switch_v2()
                    self.search_sensitivity_gsm()
                    data[self.rx_chan_gsm] = [self.rx_level, self.rssi]
                    # logger.info(f'Power: {aclr_mod_results[3]:.1f}, Sensitivity: {self.rx_level}')
                    # data[self.tx_freq_lte] = [aclr_mod_results[3], self.rx_level, self.rsrp_list, self.cinr_list,
                    #                           self.agc_list]  # measured_power, measured_rx_level, rsrp_list
                    #                           , cinr_list, agc_list
                    self.set_test_end_gsm()
                parameters = {
                    'tech': self.tech,
                    'band': self.band_gsm,
                    'bw': 0,
                    'tx_level': self.tx_level,
                    'mcs': 'GMSK',
                    'tx_path': self.tx_path,
                    'rx_path': rx_path,
                }
                self.file_path = rx_power_relative_test_export_excel_ftm(data, parameters)
            else:
                logger.info(f"GSM doesn't have this RX path {self.rx_path_gsm_dict[self.rx_path_gsm]}")

    def rx_level_select_nr(self):
        if self.rx_quick_test_enable:
            self.rx_level = self.state_dict['init_rx_sync_level']
        else:
            if self.bw_nr in [5]:
                self.rx_level = -100
            else:
                self.rx_level = -80

    def rx_level_select_lte(self):
        if self.rx_quick_test_enable:
            self.rx_level = self.state_dict['init_rx_sync_level']
        else:
            if self.bw_lte in [10, 15, 20]:
                self.rx_level = -80
            elif self.bw_lte in [1.4, 3, 5]:
                self.rx_level = -100

    def sensitivity_solution_select_nr(self):
        try:
            if not self.rx_quick_test_enable:
                self.search_sensitivity_nr()
            else:
                self.query_rx_measure_nr()

        except Exception as err:
            logger.info(err)
            logger.info('Need to check the environments')
            self.rx_level = 0

    def sensitivity_solution_select_lte(self):
        try:
            if not self.rx_quick_test_enable:
                self.search_sensitivity_lte()
            else:
                self.query_rx_measure_lte()

        except Exception as err:
            logger.info(err)
            logger.info('Need to check the environments')
            self.rx_level = 0

    @staticmethod
    def sens_calculation(real_sens_list):
        """
        if the list len is equal to 1, and then return directly
        others are calculation of sensitivity to combine their value:
        step1: to sum all the magnitude of individual sensitivity of Rx path
        step2: to get the -10log10 of step1
        """
        if len(real_sens_list) == 1:
            return round(real_sens_list[0], 1)
        elif not real_sens_list:
            return 0
        else:
            sum_sens = 0
            # sum_sens_square = 0
            for sens in real_sens_list:
                sum_sens += math.pow(10, abs(sens) / 10)
            sens_sum = round(-10 * math.log10(sum_sens), 1)
            return sens_sum
        # """
        #         if the list len is equal to 1, and then return directly
        #         others are calculation of sensitivity to combine their value:
        #         step1: to sum all the square of magnitude of individual sensitivity of Rx path
        #         step2: to square root the step1
        #         step3: to get the -10log10 of step2
        #         """
        # if len(real_sens_list) == 1:
        #     return round(real_sens_list[0], 1)
        # elif not real_sens_list:
        #     return 0
        # else:
        #     sum_sens_square = 0
        #     for sens in real_sens_list:
        #         sum_sens_square += math.pow(math.pow(10, abs(sens) / 10), 2)
        #     sum_sens_sqrt = math.sqrt(sum_sens_square)
        #     sens_sum = round(-10 * math.log10(sum_sens_sqrt), 1)
        #     return sens_sum

    def run_genre(self):
        self.sa_nsa_mode = 0
        for tech in self.state_dict['tech_list']:
            if tech == 'NR':
                self.search_sensitivity_pipline_nr()
            elif tech == 'LTE':
                self.search_sensitivity_pipline_lte()
            elif tech == 'WCDMA':
                self.search_sensitivity_pipline_wcdma()
            elif tech == 'GSM':
                self.search_sensitivity_pipline_gsm()

    def run_endc(self):
        self.sa_nsa_mode = 1
        self.search_sensitivity_pipline_endc()


def main():
    p = Path.cwd()
    print(p)


if __name__ == '__main__':
    main()
