from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.excel_handler import tx_power_fcc_ce_export_excel_ftm
import utils.parameters.rb_parameters as rb_pmt
import utils.parameters.fcc as fcc
import utils.parameters.ce as ce
from exception.custom_exception import PortTableException

logger = log_set('tx_fcc_ce')


class TxTestFccCe(AtCmd, CMW100):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.sa_nsa_mode = 0
        self.chan_mark = None
        self.rb_state = None
        self.script = None
        self.file_path = None
        self.srs_path_enable = self.state_dict['srs_path_en']
        self.port_table = None
        self.port_mimo_tx1 = None
        self.port_mimo_tx2 = None

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

    def tx_power_pipline_fcc_nr(self):  # band > bw > mcs > rb
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.script = 'FCC'
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
                try:
                    self.port_table_selector(self.band_nr, self.tx_path)
                    if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                        self.tx_power_fcc_nr()
                    else:
                        logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')

                except KeyError:
                    logger.info(f'NR Band {self.band_nr} does not have this tx path {self.tx_path}')
                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                    self.state_dict['progressBar_progress'] += 1

    def tx_power_fcc_nr(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr,
                                                   self.bw_nr)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.loss_tx = self.loss_selector(cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, self.rx_freq_nr), self.state_dict['fdc_en'])
        logger.info('----------Test FCC LMH progress---------')
        self.preset_instrument()
        self.set_measurement_group_gprf()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.select_asw_srs_path()
        self.cmw_query('*OPC?')

        tx_freq_select_list = []
        try:
            tx_freq_select_list = [int(freq * 1000) for freq in
                                   fcc.tx_freq_list_nr[self.band_nr][self.bw_nr]]  # band > bw > tx_fre1_list
        except KeyError as err:
            logger.info(f"this Band: {err} don't have to  test this BW: {self.bw_nr} for FCC")

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            try:
                for self.rb_size_nr, self.rb_start_nr in rb_pmt.FCC_NR[self.band_nr][self.bw_nr][self.mcs_nr]:
                    for num, tx_freq_nr in enumerate(tx_freq_select_list):
                        self.chan_mark = f'chan{num}'
                        self.tx_freq_nr = tx_freq_nr
                        self.tx_power_fcc_subprocess_nr()

                        if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                            # ready to export to excel
                            self.parameters = {
                                'script': self.script,
                                'tech': self.tech,
                                'band': self.band_nr,
                                'bw': self.bw_nr,
                                'rb_size': self.rb_size_nr,
                                'rb_start': self.rb_start_nr,
                                'tx_level': self.tx_level,
                                'mcs': self.mcs_nr,
                                'tx_path': self.tx_path,
                            }
                            self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)

            except KeyError as err:
                logger.debug(f'show error: {err}')
                logger.info(
                    f"Band {self.band_nr}, BW: {self.bw_nr} don't need to test this MCS: {self.mcs_nr} "
                    f"for FCC")

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1

        self.set_test_end_nr()

    def tx_power_pipline_ce_nr(self):  # band > bw > mcs > rb
        self.tx_level = self.state_dict['tx_level']
        self.port_tx = self.state_dict['tx_port']
        self.script = 'CE'
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
                try:
                    self.port_table_selector(self.band_nr, self.tx_path)
                    if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                        self.tx_power_ce_nr()
                    else:
                        logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')
                        self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                        self.state_dict['progressBar_progress'] += 1
                except KeyError:
                    logger.info(f'NR Band {self.band_nr} does not have this tx path {self.tx_path}')

    def tx_power_ce_nr(self):
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr,
                                                   self.bw_nr)  # [L_rx_freq, M_rx_ferq, H_rx_freq]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.loss_tx = self.loss_selector(cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, self.rx_freq_nr), self.state_dict['fdc_en'])
        logger.info('----------Test CE LMH progress---------')
        self.preset_instrument()
        self.set_measurement_group_gprf()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.select_asw_srs_path()

        tx_freq_select_list = []
        try:
            tx_freq_select_list = [int(freq * 1000) for freq in
                                   ce.tx_freq_list_nr[self.band_nr][self.bw_nr]]  # band > bw > tx_fre1_list
        except KeyError as err:
            logger.info(f"this Band: {err} don't have to  test this BW: {self.bw_nr} for CE")

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            try:
                for self.rb_size_nr, self.rb_start_nr in rb_pmt.CE_NR[self.band_nr][self.bw_nr][self.mcs_nr]:

                    for num, tx_freq_nr in enumerate(tx_freq_select_list):
                        self.chan_mark = f'chan{num}'
                        self.tx_freq_nr = tx_freq_nr
                        self.tx_power_ce_subprocess_nr()

                        if self.tx_path in ['TX1', 'TX2']:  # this is for TX1, TX2, not MIMO
                            # ready to export to excel
                            self.parameters = {
                                'script': self.script,
                                'tech': self.tech,
                                'band': self.band_nr,
                                'bw': self.bw_nr,
                                'rb_size': self.rb_size_nr,
                                'rb_start': self.rb_start_nr,
                                'tx_level': self.tx_level,
                                'mcs': self.mcs_nr,
                                'tx_path': self.tx_path,
                            }
                            self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)
            except KeyError as err:
                logger.debug(f'show error: {err}')
                logger.info(
                    f"Band {self.band_nr}, BW: {self.bw_nr} don't need to test this MCS: "
                    f"{self.mcs_nr} for CE")

            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
            self.state_dict['progressBar_progress'] += 1

        self.set_test_end_nr()

    def tx_power_fcc_subprocess_nr(self):
        self.data = data = {}
        self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
        self.set_tx_freq_gprf(self.tx_freq_nr)
        self.set_duty_cycle()
        if self.tx_path in ['TX1', 'TX2']:
            self.tx_set_no_sync_nr()
            power_results = self.get_power_avgerage_gprf()
            self.data[self.tx_freq_nr] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
            logger.debug(self.data)

        elif self.tx_path in ['MIMO']:  # measure two port
            path_count = 1  # this is for mimo path to store tx_path
            for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                self.port_tx = port_tx
                self.set_rf_tx_port_gprf(self.port_tx)
                self.tx_path_mimo = self.tx_path + f'_{path_count}'
                self.tx_set_no_sync_nr()
                power_results = self.get_power_avgerage_gprf()
                data[self.tx_freq_nr] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
                logger.debug(data)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_nr,
                    'bw': self.bw_nr,
                    'rb_size': self.rb_size_nr,
                    'rb_start': self.rb_start_nr,
                    'tx_level': self.tx_level,
                    'mcs': self.mcs_nr,
                    'tx_path': self.tx_path_mimo,
                }
                self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)

                path_count += 1

    def tx_power_ce_subprocess_nr(self):
        self.data = data = {}
        self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
        self.set_tx_freq_gprf(self.tx_freq_nr)
        self.set_duty_cycle()
        if self.tx_path in ['TX1', 'TX2']:
            self.tx_set_no_sync_nr()
            power_results = self.get_power_avgerage_gprf()
            self.data[self.tx_freq_nr] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
            logger.debug(self.data)

        elif self.tx_path in ['MIMO']:  # measure two port
            path_count = 1  # this is for mimo path to store tx_path
            for port_tx in [self.port_mimo_tx1, self.port_mimo_tx2]:
                self.port_tx = port_tx
                self.set_rf_tx_port_gprf(self.port_tx)
                self.tx_path_mimo = self.tx_path + f'_{path_count}'
                self.tx_set_no_sync_nr()
                power_results = self.get_power_avgerage_gprf()
                data[self.tx_freq_nr] = (self.chan_mark, power_results)  # data = {tx_freq:(chan_mark, power)}
                logger.debug(data)

                # ready to export to excel
                self.parameters = {
                    'script': self.script,
                    'tech': self.tech,
                    'band': self.band_nr,
                    'bw': self.bw_nr,
                    'rb_size': self.rb_size_nr,
                    'rb_start': self.rb_start_nr,
                    'tx_level': self.tx_level,
                    'mcs': self.mcs_nr,
                    'tx_path': self.tx_path_mimo,
                }
                self.file_path = tx_power_fcc_ce_export_excel_ftm(self.data, self.parameters)

                path_count += 1

    def run_fcc(self):
        self.tx_power_pipline_fcc_nr()
        self.cmw_close()

    def run_ce(self):
        self.tx_power_pipline_ce_nr()
        self.cmw_close()


