from equipments.anritsu8820 import Anritsu8820
from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
# import utils.parameters.external_paramters as ext_pmt
import utils.parameters.common_parameters_anritsu as cm_pmt_anritsu
from utils.channel_handler import channel_freq_select
from utils.excel_handler import tx_power_relative_test_export_excel_sig, txp_aclr_evm_current_plot_sig
from utils.log_init import log_set
from exception.custom_exception import FileNotFoundException

logger = log_set('8820TxSig')


class TxTestGenre(AtCmd, Anritsu8820):
    def __init__(self, state_dict, obj_progressbar):
        AtCmd.__init__(self)
        Anritsu8820.__init__(self)
        self.ser.com_close()
        self.state_dict = state_dict
        self.progressBar = obj_progressbar
        self.get_temp_en = self.get_temp_en = self.state_dict['get_temp_en']

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

    def tx_core(self, standard, band, dl_ch, bw=None):
        conn_state = int(self.get_calling_state_query())
        self.dl_ch = dl_ch

        # calling process
        if standard == 'LTE':
            if conn_state != cm_pmt_anritsu.ANRITSU_CONNECTED:
                self.set_init_before_calling(standard, self.m_dl_ch, bw)
                self.set_registration_calling(standard)
        elif standard == 'WCDMA' and self.chcoding == 'REFMEASCH':  # this is WCDMA
            if conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                self.set_init_before_calling(standard, self.m_dl_ch, bw)
                self.set_registration_calling(standard)
        elif standard == 'WCDMA' and self.chcoding == 'EDCHTEST':  # this is HSUPA
            if conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                self.set_init_before_calling(standard, self.m_dl_ch, bw)
                self.set_init_hspa()
                self.set_registration_calling(standard)
        elif standard == 'WCDMA' and self.chcoding == 'FIXREFCH':  # this is HSDPA
            if conn_state != cm_pmt_anritsu.ANRITSU_LOOP_MODE_1:
                self.set_init_before_calling(standard, self.m_dl_ch, bw)
                self.set_init_hspa()
                self.set_registration_calling(standard)

        if standard == 'LTE':
            self.chcoding = None
            logger.info(f'Start to measure B{band}, bandwidth: {bw} MHz, downlink_chan: {dl_ch}')
        elif standard == 'WCDMA' and self.chcoding == 'REFMEASCH':  # this is WCDMA
            logger.info(f'Start WCDMA to measure B{band}, downlink_chan: {dl_ch}')
        elif standard == 'WCDMA' and self.chcoding == 'EDCHTEST':  # this is HSUPA
            logger.info(f'Start HSUPA to measure B{band}, downlink_chan: {dl_ch}')
        elif standard == 'WCDMA' and self.chcoding == 'FIXREFCH':  # this is HSDPA
            logger.info(f'Start HSDPA to measure B{band}, downlink_chan: {dl_ch}')

        self.set_handover(standard, dl_ch, bw)

        # HSUPA and HSDPA need to setting some parameters
        if standard == 'WCDMA' and (self.chcoding == 'EDCHTEST' or self.chcoding == 'FIXREFCH'):
            self.set_registration_after_calling_hspa()

        data = self.get_validation(standard)

        if standard == 'LTE':
            self.parameters = {
                'standard': standard,
                'band': band,
                'dl_ch': dl_ch,
                'bw': bw,
                'chcoding': self.chcoding,
                'thermal': self.get_temperature(),  # this is list-data
                'tx_freq': self.get_ul_freq_query(),  # get UL freq kHz
            }

        elif standard == 'WCDMA':  # this is WCDMA
            self.parameters = {
                'standard': standard,
                'band': band,
                'dl_ch': dl_ch,
                'bw': 5,
                'chcoding': self.chcoding,
                'thermal': self.get_temperature(),  # this is list-data
                'tx_freq': self.get_ul_freq_query(),  # get UL freq kHz
            }

        self.excel_path = tx_power_relative_test_export_excel_sig(data, self.parameters)

    def run(self):
        for tech in self.state_dict['tech_list']:
            self.input_level_sig = self.state_dict['input_level_sig_anritsu']
            if tech == 'LTE' and self.state_dict['lte_bands_list'] != []:
                standard = self.set_switch_to_lte()
                self.anritsu_query('*OPC?')
                logger.info(standard)
                self.chcoding = None
                for bw in self.state_dict['lte_bw_list']:
                    for band in self.state_dict['lte_bands_list']:
                        if bw in cm_pmt_anritsu.bandwidths_selected(band):
                            self.set_test_parameter_normal()
                            dl_chan_list = cm_pmt_anritsu.dl_ch_selected(standard, band, bw)
                            ch_list = channel_freq_select(self.state_dict['channel_str'], dl_chan_list)
                            self.m_dl_ch = dl_chan_list[1]  # this is used for the handover smoothly by Mch when calling
                            self.set_dl_chan(self.m_dl_ch)
                            logger.debug(f'Test Channel List: {band}, {bw}MHZ, downlink channel list:{ch_list}')
                            for dl_ch in ch_list:
                                self.tx_core(standard, band, dl_ch, bw)
                                self.set_test_parameter_normal()
                                self.set_tpc('AUTO')
                                self.set_input_level(5)
                                self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                                self.state_dict['progressBar_progress'] += 1

                            self.set_dl_chan(self.m_dl_ch)
                        else:
                            logger.info(f'B{band} do not have BW {bw}MHZ')
                            skip_count = len(self.state_dict['channel_str'])
                            self.progressBar.setValue(self.state_dict['progressBar_progress'] + skip_count)
                            self.state_dict['progressBar_progress'] += skip_count

                    try:
                        txp_aclr_evm_current_plot_sig(standard, self.excel_path)

                    except FileNotFoundException as err:
                        logger.info(err)
                        logger.info(f'there is not file to plot BW{bw} ')

            elif (tech == 'WCDMA' or tech == 'HSUPA' or tech == 'HSDPA') and (
                    self.state_dict['wcdma_bands_list'] != [] or self.state_dict['hsupa_bands_list'] != [] or self.state_dict['hsdpa_bands_list'] != []):
                standard = self.set_switch_to_wcdma()
                self.anritsu_query('*OPC?')
                self.set_end()

                if tech == 'WCDMA':
                    self.set_channel_coding('REFMEASCH')
                    logger.info('Set to WCDMA')
                elif tech == 'HSUPA':
                    self.set_channel_coding('EDCHTEST')
                    logger.info('Set to HSUPA')
                elif tech == 'HSDPA':
                    self.set_channel_coding('FIXREFCH')
                    logger.info('Set to HSDPA')

                self.chcoding = self.get_channel_coding_query()
                logger.info(f'CHCODING: {self.chcoding}')

                bands = None
                if self.chcoding == 'REFMEASCH':  # this is WCDMA
                    bands = self.state_dict['wcdma_bands_list']
                    logger.info(f'WCDMA Bands select: {bands}')
                elif self.chcoding == 'EDCHTEST':  # this is HSUPA
                    bands = self.state_dict['hsupa_bands_list']
                    logger.info(f'HSUPA Bands select: {bands}')
                elif self.chcoding == 'FIXREFCH':  # this is HSDPA
                    bands = self.state_dict['hsdpa_bands_list']
                    logger.info(f'HSDPA Bands select: {bands}')

                if bands:
                    for band in bands:
                        dl_chan_list = cm_pmt_anritsu.dl_ch_selected(standard, band)
                        ch_list = channel_freq_select(self.state_dict['channel_str'], dl_chan_list)
                        logger.debug(f'Test Channel List: {band}, downlink channel list:{ch_list}')
                        self.m_dl_ch = dl_chan_list[1]  # this is used for the handover smoothly by Mch when calling
                        self.set_dl_chan(self.m_dl_ch)
                        for dl_ch in ch_list:
                            self.tx_core(standard, band, dl_ch)
                            self.progressBar.setValue(self.state_dict['progressBar_progress'] + 1)
                            self.state_dict['progressBar_progress'] += 1

                    txp_aclr_evm_current_plot_sig(standard, self.excel_path)
                else:
                    logger.info(f'==========Please check RATs select and related to bands==========')

            elif tech == 'GSM' and self.state_dict['gsm_bands_list'] != []:
                pass

            else:
                logger.info(f'Finished')
