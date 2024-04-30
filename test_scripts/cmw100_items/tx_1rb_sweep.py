from pathlib import Path

from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
from equipments.cmw100 import CMW100
from utils.log_init import log_set
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_ftm as cm_pmt_ftm
from utils.loss_handler import get_loss
from utils.excel_handler import txp_aclr_evm_current_plot_ftm, tx_power_relative_test_export_excel_ftm
from utils.excel_handler import select_file_name_genre_tx_ftm, excel_folder_path
from utils.channel_handler import channel_freq_select
import utils.parameters.rb_parameters as rb_pmt
from exception.custom_exception import FileNotFoundException, PortTableException

logger = log_set('1rb_sweep')


class TxTest1RbSweep(AtCmd, CMW100):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        CMW100.__init__(self)
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.sa_nsa_mode = 0
        self.port_mimo_tx2 = None
        self.port_mimo_tx1 = None
        self.parameters = None
        self.srs_path_enable = self.state_dict['srs_path_en']
        self.file_path = None
        self.script = None
        self.rb_state = None
        self.chan = None
        self.port_table = None
        self.rx_level = self.state_dict['init_rx_sync_level']

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

    def tx_1rb_sweep_pipeline_nr(self):
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
                self.port_table_selector(self.band_nr, self.tx_path)

                if self.bw_nr in cm_pmt_ftm.bandwidths_selected_nr(self.band_nr):
                    self.tx_1rb_sweep_process_nr()
                else:
                    logger.info(f'B{self.band_nr} does not have BW {self.bw_nr}MHZ')
                    skip_count = len(self.state_dict['nr_mcs_list']) * len(
                        self.state_dict['nr_rb_allocation_list']) * len(
                        self.state_dict['tx_path_list']) * len(self.state_dict['channel_str'])
                    self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                    self.state_dict['progressBar_progress'] += skip_count

        for bw in self.state_dict['nr_bw_list']:
            try:
                file_name = select_file_name_genre_tx_ftm(bw, 'NR', '1rb_sweep')
                file_path = Path(excel_folder_path()) / Path(file_name)
                txp_aclr_evm_current_plot_ftm(file_path, {'script': 'GENERAL', 'tech': 'NR'})
            except TypeError:
                logger.info(f'there is no data to plot because the band does not have this BW ')
            except FileNotFoundException as err:
                logger.info(err)
                logger.info(f'there is not file to plot BW{bw} ')

    def tx_1rb_sweep_process_nr(self):
        logger.info('----------1RB Sweep progress ---------')
        rx_freq_list = cm_pmt_ftm.dl_freq_selected('NR', self.band_nr, self.bw_nr)
        # tx_freq_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        self.rx_freq_nr = rx_freq_list[1]
        self.loss_rx = self.loss_selector(rx_freq_list[1], self.state_dict['fdc_en'])
        self.preset_instrument()
        self.set_test_end_nr()
        self.set_test_mode_nr()
        self.select_asw_srs_path()
        self.sig_gen_nr()
        self.sync_nr()

        tx_freq_lmh_list = [cm_pmt_ftm.transfer_freq_rx2tx_nr(self.band_nr, rx_freq) for rx_freq in rx_freq_list]
        tx_freq_select_list = sorted(set(channel_freq_select(self.chan, tx_freq_lmh_list)))

        for mcs in self.state_dict['nr_mcs_list']:
            self.mcs_nr = mcs
            for tx_freq_select in tx_freq_select_list:
                self.tx_freq_nr = tx_freq_select
                self.rb_size_nr, rb_sweep_nr = rb_pmt.GENERAL_NR[self.bw_nr][self.scs][self.type_nr][
                    self.rb_alloc_nr_dict['EDGE_1RB_RIGHT']]  # capture EDGE_1RB_RIGHT
                self.rb_state = '1rb_sweep'
                data = {}
                for rb_start in range(rb_sweep_nr + 1):
                    self.rb_start_nr = rb_start
                    self.loss_tx = self.loss_selector(self.tx_freq_nr, self.state_dict['fdc_en'])
                    self.tx_set_nr()
                    aclr_mod_results = self.tx_measure_nr()
                    logger.debug(aclr_mod_results)
                    data[self.tx_freq_nr] = aclr_mod_results
                    logger.debug(data)
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
                        'test_item': '1rb_sweep',
                    }
                    self.file_path = tx_power_relative_test_export_excel_ftm(data, self.parameters)

                self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                self.state_dict['progressBar_progress'] += 1

        self.set_test_end_nr()

    def run(self):
        for tech in self.state_dict['tech_list']:
            if tech == 'NR':
                self.tx_1rb_sweep_pipeline_nr()
            elif tech == 'LTE':
                pass
            else:
                pass
        self.cmw_close()
