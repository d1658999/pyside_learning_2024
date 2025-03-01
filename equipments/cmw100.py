import math
import time

from equipments.series_basis.callbox.cmw_series import CMW
from utils.parameters.common_parameters_ftm import TDD_BANDS, NTN_BANDS
import utils.parameters.external_paramters as ext_pmt
from utils.loss_handler import get_loss
from utils.loss_handler import read_fdc_file
from utils.port_tx_handler import port_tx_table_transfer
from utils.log_init import log_set

logger = log_set('CMW100')


class CMW100(CMW):
    def __init__(self, equipment='cmw100'):
        super().__init__(equipment)
        self.mcs_cc1_lte = None
        self.port_tx = None
        self.tech = None
        self.bw_nr = None
        self.bw_lte = None
        self.band_nr = None
        self.band_lte = None
        self.band_wcdma = None
        self.band_gsm = None
        self.tx_level = None
        self.rx_level = None
        self.pcl = None
        self.pwr_init_gsm = None
        self.loss_tx = None
        self.loss_rx = None
        self.tx_freq_nr = None
        self.tx_freq_lte = None
        self.tx_chan_wcdma = None
        self.tx_freq_gsm = None
        self.rx_freq_nr = None
        self.rx_freq_lte = None
        self.rx_freq_wcdma = None
        self.rx_freq_gsm = None
        self.rx_chan_gsm = None
        self.scs = None
        self.type_nr = None
        self.mcs_nr = None
        self.mcs_lte = None
        self.rb_size_nr = None
        self.rb_start_nr = None
        self.rb_size_lte = None
        self.rb_start_lte = None
        self.tsc = None
        self.mod_gsm = None
        self.fdc_en = False

    def preset_instrument(self):
        logger.info('----------Preset CMW----------')
        self.system_preset_all()
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_fd_correction_deactivate_all()
        self.set_fd_correction_ctable_delete()
        self.cmw_query('*OPC?')
        self.system_err_all_query()
        self.cmw_write('*RST')
        self.cmw_query('*OPC?')
        self.set_fdcorrection_create_activate_process()

    def set_measurement_group_gprf(self):
        if self.tech == 'NR':
            self.set_measurement_gprf(self.port_tx, self.bw_nr)
        elif self.tech == 'LTE':
            self.set_measurement_gprf(self.port_tx, self.bw_lte)
        elif self.tech == 'WCDMA':
            self.set_measurement_gprf(self.port_tx, 5)
        elif self.tech == 'GSM':
            self.set_measurement_gprf(self.port_tx, 0.2)

    def set_measurement_gprf(self, port_tx, bw):
        logger.info('----------set GPRF Measurement----------')
        self.set_if_filter_gprf()
        self.set_bandpass_filter_bw_gprf(bw)
        self.set_rf_tx_port_gprf(port_tx)
        self.set_power_count_gprf()
        self.set_repetition_gprf()
        self.set_power_list_mode_gprf()  # default is off listmode
        self.set_trigger_source_gprf('Free Run')
        self.set_trigger_slope_gprf()
        self.set_trigger_step_length_gprf(5.0e-3)
        # self.set_trigger_step_length_gprf(8.0e-3)
        self.set_trigger_measure_length_gprf(5.0e-3)
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 2.1E-3')
        # self.command_cmw100_write(f'TRIGger:GPRF:MEAS:POWer:OFFSet 5E-4')
        self.set_trigger_offset_gprf(0)
        self.set_trigger_mode_gprf('ONCE')
        self.set_expect_power_gprf(self.tx_level)
        self.set_rf_setting_user_margin_gprf(10.00)
        self.set_rf_setting_external_tx_port_attenuation_gprf(self.loss_tx)

    def get_power_avgerage_gprf(self):
        """
        This function is used for FCC and CE certification
        """
        self.set_measure_start_on_gprf()
        self.cmw_query('*OPC?')
        f_state = self.get_power_state_query_gprf()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_gprf()
            self.cmw_query('*OPC?')
        power_average = round(eval(self.get_power_average_query_gprf()[1]), 2)
        logger.info(f'Get the GPRF power: {power_average}')
        return power_average

    def get_power_monitor_avgerage_lte(self):
        f_state = self.get_power_state_query_lte()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_lte()
            self.cmw_query('*OPC?')
        self.cmw_query('*OPC?')
        power_average = self.get_power_monitor_average_query_lte()
        logger.info(f'Get the LTE Monitor power: {power_average}')
        return power_average

    def get_modulation_avgerage_nr(self):
        f_state = self.get_power_state_query_nr()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_nr()
            self.cmw_query('*OPC?')
        # P[3] is EVM, P[15] is Ferr, P[14] is IQ Offset, P[17] is equipment power
        mod_results = self.get_modulation_average_query_nr()
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14], mod_results[17]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'Power: {mod_results[3]}, EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, '
                    f'IQ_OFFSET: {mod_results[2]:.2f}')
        return mod_results

    def get_modulation_avgerage_lte(self):
        # P[3] is EVM, P[15] is Ferr, P[14] is IQ Offset, P[17] is equipment power
        mod_results = self.get_modulation_average_query_lte()
        mod_results = mod_results.split(',')
        mod_results = [mod_results[3], mod_results[15], mod_results[14], mod_results[17]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'Power: {mod_results[3]}, EVM: {mod_results[0]:.2f}, FREQ_ERR: {mod_results[1]:.2f}, '
                    f'IQ_OFFSET: {mod_results[2]:.2f}')
        return mod_results

    def get_modulation_avgerage_wcdma(self):
        # P[1] is EVM, P[9] is Ferr, P[7] is IQ Offset, P[11] is power
        mod_results = self.get_modulation_average_query_wcdma()
        mod_results = mod_results.split(',')
        mod_results = [mod_results[11], mod_results[1], mod_results[9], mod_results[7]]
        mod_results = [eval(m) for m in mod_results]
        logger.info(f'POWER: {mod_results[0]:.1f}, EVM: {mod_results[1]:.2f}, FREQ_ERR: {mod_results[2]:.2f}, '
                    f'IQ_OFFSET: {mod_results[3]:.2f}')
        return mod_results

    def get_modulation_average_gsm(self):
        mod_results = self.get_modulation_average_query_gsm()
        mod_results = mod_results.split(',')  # P12 is Power, P6 is phase_err_rms, P2 is EVM_rms, P10 is ferr
        mod_results = [mod_results[12], mod_results[6], mod_results[7],
                       mod_results[10]]  # power, phase_err_rms, phase_peak, ferr
        mod_results = [round(eval(m), 2) for m in mod_results]
        logger.info(f'Power: {mod_results[0]:.2f}, Phase_err_rms: {mod_results[1]:.2f}, '
                    f'Phase_peak: {mod_results[2]:.2f}, Ferr: {mod_results[3]:.2f}')
        return mod_results

    def get_aclr_average_nr(self):
        aclr_results = self.get_aclr_average_query_nr()
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr) * -1 if num != 3 else eval(aclr) for num, aclr in
                        enumerate(aclr_results)]  # UTRA2(-), UTRA1(-), NR(-), TxP, NR(+), UTRA1(+), UTRA2(+)
        logger.info(f'Carrier Power: {aclr_results[3]:.2f}, '
                    f'E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], '
                    f'UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], '
                    f'UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        return aclr_results

    def get_aclr_average_lte(self):
        f_state = self.get_power_state_query_lte()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_lte()
            self.cmw_query('*OPC?')
        aclr_results = self.get_aclr_average_query_lte()
        aclr_results = aclr_results.split(',')[1:]
        aclr_results = [eval(aclr) * -1 if num != 3 else eval(aclr) for num, aclr in
                        enumerate(aclr_results)]  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2
        logger.info(f'Carrier Power: {aclr_results[3]:.2f}, '
                    f'E-UTRA: [{aclr_results[2]:.2f}, {aclr_results[4]:.2f}], '
                    f'UTRA_1: [{aclr_results[1]:.2f}, {aclr_results[5]:.2f}], '
                    f'UTRA_2: [{aclr_results[0]:.2f}, {aclr_results[6]:.2f}]')
        return aclr_results

    def get_aclr_average_wcdma(self):
        f_state = self.get_power_state_query_wcdma()
        while f_state != 'RDY':
            f_state = self.get_power_state_query_wcdma()
            self.cmw_query('*OPC?')
        spectrum_results = self.get_aclr_average_query_wcdma()
        spectrum_results = spectrum_results.split(',')
        spectrum_results = [
            # round(eval(spectrum_results[1]) + 0.254, 2),  carrier power is smaller than we want about 0.254 dB
            round(eval(spectrum_results[3]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[4]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[2]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[5]) - eval(spectrum_results[1]), 2),
            round(eval(spectrum_results[6]) / 1000000, 2)
        ]  # P1: Power, P2: ACLR_-2, P3: ACLR_-1, P4:ACLR_+1, P5:ACLR_+2, P6:OBW
        logger.info(
            f'ACLR_-1: {spectrum_results[1]:.2f}, ACLR_1: {spectrum_results[2]:.2f}, '
            f'ACLR_-2: {spectrum_results[0]:.2f}, ACLR_+2: {spectrum_results[3]:.2f}, '
            f'OBW: {spectrum_results[4]:.2f}MHz')
        return spectrum_results

    def get_orfs_average_gsm(self):
        f_state = self.get_power_state_query_gsm()
        while f_state != 'RDY':
            time.sleep(0.2)
            f_state = self.get_power_state_query_gsm()
            self.cmw_query('*OPC?')
        pvt = self.get_pvt_average_query_gsm()  # PVT, but it is of no use
        orfs_mod = self.get_orfs_modulation_gsm()  # MOD_ORFS
        orfs_mod = [round(eval(orfs_mod), 2) for orfs_mod in orfs_mod.split(',')[13:29]]
        orfs_mod = [
            orfs_mod[6],  # -200 KHz
            orfs_mod[10],  # 200 KHz
            orfs_mod[4],  # -400 KHz
            orfs_mod[12],  # 400 KHz
            orfs_mod[3],  # -600 KHz
            orfs_mod[13],  # 600 KHz
        ]
        logger.info(f'ORFS_MOD_-200KHz: {orfs_mod[0]}, ORFS_MOD_200KHz: {orfs_mod[1]}')
        logger.info(f'ORFS_MOD_-400KHz: {orfs_mod[2]}, ORFS_MOD_400KHz: {orfs_mod[3]}')
        logger.info(f'ORFS_MOD_-600KHz: {orfs_mod[4]}, ORFS_MOD_600KHz: {orfs_mod[5]}')
        orfs_sw = self.get_orfs_switching_gsm()  # SW_ORFS
        orfs_sw = [round(eval(orfs_sw), 2) for orfs_sw in orfs_sw.split(',')[17:25]]
        orfs_sw = [
            orfs_sw[3],  # -400 KHz
            orfs_sw[5],  # 400 KHz
            orfs_sw[2],  # -600 KHz
            orfs_sw[6],  # 600 KHz
            orfs_sw[1],  # -1200 KHz
            orfs_sw[7],  # 1200 KHz
        ]
        logger.info(f'ORFS_SW_-400KHz: {orfs_sw[0]}, ORFS_SW_400KHz: {orfs_sw[1]}')
        logger.info(f'ORFS_SW_-600KHz: {orfs_sw[2]}, ORFS_SW_600KHz: {orfs_sw[3]}')
        logger.info(f'ORFS_SW_-1200KHz: {orfs_sw[4]}, ORFS_SW_1200KHz: {orfs_sw[5]}')

        return orfs_mod, orfs_sw

    def get_in_band_emissions_nr(self):
        iem_results = self.get_in_band_emission_query_nr()
        iem_results = iem_results.split(',')
        iem = f'{eval(iem_results[2]):.2f}' if iem_results[2] != 'INV' else 'INV'
        logger.info(f'InBandEmissions Margin: {iem}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        return iem_results

    def get_in_band_emissions_lte(self):
        iem_results = self.get_in_band_emission_query_lte()
        iem_results = iem_results.split(',')
        iem = f'{eval(iem_results[2]):.2f}' if iem_results[2] != 'INV' else 'INV'
        logger.info(f'InBandEmissions Margin: {iem}dB')
        # logger.info(f'IEM_MARG results: {iem_results}')
        return iem_results

    def get_flatness_extreme_nr(self):
        esfl_results = self.get_flatness_extreme_query_nr()
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
        # logger.info(f'ESFL results: {esfl_results}')
        return ripple1, ripple2

    def get_flatness_extreme_lte(self):
        esfl_results = self.get_flatness_extreme_query_lte()
        esfl_results = esfl_results.split(',')
        ripple1 = round(eval(esfl_results[2]), 2) if esfl_results[2] != 'NCAP' else esfl_results[2]
        ripple2 = round(eval(esfl_results[3]), 2) if esfl_results[3] != 'NCAP' else esfl_results[3]
        logger.info(f'Equalize Spectrum Flatness: Ripple1:{ripple1} dBpp, Ripple2:{ripple2} dBpp')
        # logger.info(f'ESFL results: {esfl_results}')
        return ripple1, ripple2

    def get_sem_average_and_margin_nr(self):
        sem_results = self.get_sem_margin_all_query_nr()
        logger.info(f'SEM_MARG results: {sem_results}')
        sem_avg_results = self.get_sem_average_query_nr()
        sem_avg_results = sem_avg_results.split(',')
        logger.info(f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, '
                    f'Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
        # logger.info(f'SEM_AVER results: {sem_avg_results}')
        return sem_results, sem_avg_results

    def get_sem_average_and_margin_lte(self):
        sem_results = self.get_sem_margin_all_query_lte()
        logger.info(f'SEM_MARG results: {sem_results}')
        sem_avg_results = self.get_sem_average_query_lte()
        sem_avg_results = sem_avg_results.split(',')
        logger.info(f'OBW: {eval(sem_avg_results[2]) / 1000000:.3f} MHz, '
                    f'Total TX Power: {eval(sem_avg_results[3]):.2f} dBm')
        # logger.info(f'SEM_AVER results: {sem_avg_results}')
        return sem_results, sem_avg_results

    def set_waveform_nr(self, bw, scs, mcs):
        if self.band_nr in TDD_BANDS and self.band_nr not in NTN_BANDS:
            waveform_path = f'C:\\CMW100_WV\\SMU_NodeB_NR_Ant0_NR_{bw}MHz_SCS{scs}_TDD_Sens_MCS{mcs}_rescale.wv'
        else:
            waveform_path = f'C:\\CMW100_WV\\SMU_NodeB_NR_Ant0_LTE_NR_{bw}MHz_SCS{scs}_FDD_Sens_MCS_{mcs}.wv'

        self.set_arb_file_gprf(waveform_path)

    def set_waveform_lte(self, bw):
        if self.band_lte in TDD_BANDS and self.band_lte not in NTN_BANDS:
            # waveform_path = f'C:\\CMW100_WV\\SMU_Channel_CC0_RxAnt0_RF_Verification_10M_SIMO_01.wv'
            # v0.126
            if bw == 10:
                waveform_path = f'C:\\CMW100_WV\\SMU_NodeB_Ant0_LTE_SENS_10MHz_TDD_CFG1_SF_CFG4_SIMO_woCIF_AGL8_RC.wv'
            else:
                # v0.135
                bw_index = {
                    '1.4': '01',
                    '3': '02',
                    '5': '03',
                    '15': '05',
                    '20': '06',
                }
                waveform_path = f'C:\\CMW100_WV\\SMU_NodeB_Ant0_TDD_FULL_{bw_index[str(bw)]}.wv'

        else:
            bw = '1p4' if bw == 1.4 else f'0{bw}' if bw <= 5 else bw
            waveform_path = f'C:\\CMW100_WV\\SMU_NodeB_Ant0_FRC_{bw}MHz.wv'

        self.set_arb_file_gprf(waveform_path)

    def set_waveform_wcdma(self):
        waveform_path = r'C:\CMW100_WV\3G_CAL_FINAL.wv'
        self.set_arb_file_gprf(waveform_path)

    def set_waveform_gsm(self):
        waveform_path = r'C:\CMW100_WV\2G_FINAL.wv'
        self.set_arb_file_gprf(waveform_path)

    def power_init_gsm(self):
        if self.band_gsm in [850, 900]:
            self.pwr_init_gsm = 33 - 2 * (self.pcl - 5)
        elif self.band_gsm in [1800, 1900]:
            self.pwr_init_gsm = 30 - 2 * (self.pcl - 0)

    def sig_gen_nr(self):
        """
        scs: FDD is forced to 15KHz and TDD is to be 30KHz
        """

        logger.info('----------Sig Gen for nr----------')
        self.select_scs_nr(self.band_nr)
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_rf_rx_port_gprf(18)
        self.cmw_query('*OPC?')
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_generator_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.set_uldl_periodicity_nr()
        self.cmw_query('*OPC?')
        self.set_waveform_nr(self.bw_nr, self.scs, mcs=4)
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_nr)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def sig_gen_lte(self):
        logger.info('----------Sig Gen for LTE----------')
        self.system_base_option_version_query('CMW_NRSub6G_Meas')
        self.set_rf_rx_port_gprf(18)
        self.cmw_query('*OPC?')
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_generator_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        # self.band_lte = int(self.band_lte)
        self.set_waveform_lte(self.bw_lte)
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_lte)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def sig_gen_wcdma(self):
        logger.info('----------Sig Gen for WCDMA----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_rf_rx_port_gprf(18)
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_generator_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.set_waveform_wcdma()
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_wcdma)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def sig_gen_gsm(self):
        logger.info('----------Sig Gen for GSM----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.set_rf_rx_port_gprf(18)
        self.set_generator_cmw_port_uasge_all_gprf()
        self.cmw_query('*OPC?')
        self.set_generator_list_mode_gprf()
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_rx_port_attenuation_gprf(self.loss_rx)
        self.cmw_query('*OPC?')
        self.set_generator_base_band_mode_gprf('ARB')
        self.cmw_query('*OPC?')
        self.set_waveform_gsm()
        self.cmw_query('*OPC?')
        self.get_arb_file_query_gprf()
        self.set_rx_freq_gprf(self.rx_freq_gsm)
        self.set_rx_level_gprf(self.rx_level)
        gprf_gen = self.get_generator_state_query_gprf()
        self.cmw_query('*OPC?')
        if gprf_gen == 'OFF':
            self.set_generator_state_gprf()
            self.cmw_query('*OPC?')

    def set_sem_limit_nr(self, bw):
        self.set_spectrum_limit_nr(1, bw, 0.015, 0.0985, round(-13.5 - 10 * math.log10(bw / 5), 1), 'K030')
        self.set_spectrum_limit_nr(2, bw, 1.5, 4.5, -8.5, 'M1')
        self.set_spectrum_limit_nr(3, bw, 5.5, round(-0.5 + bw, 1), -11.5, 'M1')
        self.set_spectrum_limit_nr(4, bw, round(0.5 + bw, 1), round(4.5 + bw, 1), -23.5, 'M1')

    def set_sem_limit_lte(self, bw):
        if bw == 1.4:
            limit_level = -10
        elif bw == 3:
            limit_level = -13
        elif bw == 5:
            limit_level = -15
        elif bw == 10:
            limit_level = -18
        elif bw == 15:
            limit_level = -20
        else:
            limit_level = -21
        self.set_spectrum_limit_lte(1, bw * 10, 'ON', 0, 1, limit_level, 'K030')
        self.set_spectrum_limit_lte(2, bw * 10, 'ON', 1, 2.5, -10, 'M1')
        if bw < 3:
            self.set_spectrum_limit_lte(3, bw * 10, 'ON', 2.5, 2.8, -25, 'M1')
        else:
            self.set_spectrum_limit_lte(3, bw * 10, 'ON', 2.5, 2.8, -10, 'M1')

        if bw >= 3:
            self.set_spectrum_limit_lte(4, bw * 10, 'ON', 2.8, 5, -10, 'M1')
        else:
            self.set_spectrum_limit_lte(4, bw * 10, 'OFF', 2.8, 5, -25, 'M1')

        if bw < 3:
            self.set_spectrum_limit_lte(5, bw * 10, 'OFF', bw * 2, bw * 2, -25, 'M1')
        elif bw == 3:
            self.set_spectrum_limit_lte(5, bw * 10, 'ON', 5, 6, -25, 'M1')
        elif bw > 3:
            self.set_spectrum_limit_lte(5, bw * 10, 'ON', 5, 6, -13, 'M1')

        if bw < 5:
            self.set_spectrum_limit_lte(6, bw * 10, 'OFF', bw * 2, bw * 2, -25, 'M1')
        elif bw == 5:
            self.set_spectrum_limit_lte(6, bw * 10, 'ON', 6, 10, -25, 'M1')
        elif bw > 5:
            self.set_spectrum_limit_lte(6, bw * 10, 'ON', 6, 10, -13, 'M1')

        if bw < 10:
            self.set_spectrum_limit_lte(7, bw * 10, 'OFF', bw * 2, bw * 2, -25, 'M1')
        elif bw == 10:
            self.set_spectrum_limit_lte(7, bw * 10, 'ON', 10, 15, -25, 'M1')
        elif bw > 10:
            self.set_spectrum_limit_lte(7, bw * 10, 'ON', 10, 15, -13, 'M1')

        if bw < 15:
            self.set_spectrum_limit_lte(8, bw * 10, 'OFF', bw * 2, bw * 2, -25, 'M1')
        elif bw == 15:
            self.set_spectrum_limit_lte(8, bw * 10, 'ON', 15, 20, -25, 'M1')
        elif bw > 15:
            self.set_spectrum_limit_lte(8, bw * 10, 'ON', 15, 20, -13, 'M1')

        if bw < 15:
            self.set_spectrum_limit_lte(9, bw * 10, 'OFF', bw * 2, bw * 2, -25, 'M1')
        elif bw == 15:
            self.set_spectrum_limit_lte(9, bw * 10, 'OFF', 20, 20, -25, 'M1')
        elif bw > 15:
            self.set_spectrum_limit_lte(9, bw * 10, 'ON', 20, 25, -25, 'M1')

    def set_rx_level_search(self):
        logger.info(f'==========Search: {self.rx_level} dBm==========')
        self.set_rx_level_gprf(self.rx_level)
        # self.command_cmw100_query('*OPC?')

    def select_mode_fdd_tdd(self, band):
        if isinstance(band, str):
            if band in ['1_docomo', '1_kddi', '8_jrf']:
                band = band[0]
            else:
                band = int(band[:-1])

        if self.tech == 'NR':
            if band in TDD_BANDS:
                self.set_duplexer_mode_nr('TDD')
                logger.debug('========== Set TDD ==========')
            else:
                self.set_duplexer_mode_nr('FDD')
                logger.debug('========== Set FDD ==========')
        elif self.tech == 'LTE' or self.tech == 'ULCA_LTE':
            if band in TDD_BANDS:
                self.set_duplexer_mode_lte('TDD')
                logger.debug('========== Set TDD ==========')
            else:
                self.set_duplexer_mode_lte('FDD')
                logger.debug('========== Set FDD ==========')

    def select_scs_nr(self, band):
        """
        For now FDD is forced to 15KHz and TDD is to be 30KHz
        """
        if band in TDD_BANDS and band not in NTN_BANDS:
            scs = 1
        else:
            scs = 0
        self.scs = 15 * (2 ** scs)  # for now TDD only use 30KHz, FDD only use 15KHz

    def tx_measure_nr(self):
        logger.info('---------Tx Measure----------')
        self.system_base_option_version_query("CMW_NRSub6G_Meas")
        self.select_mode_fdd_tdd(self.band_nr)
        self.select_scs_nr(self.band_nr)
        self.set_band_nr(self.band_nr)
        self.set_tx_freq_nr(self.tx_freq_nr)
        self.cmw_query('*OPC?')
        self.set_plc_nr()
        self.set_meas_on_exception_nr('ON')
        self.set_scs_bw_nr(self.scs, self.bw_nr)
        self.set_sem_limit_nr(self.bw_nr)
        self.set_precoding_nr(self.type_nr)
        self.set_pusch_nr(self.mcs_nr, self.rb_size_nr, self.rb_start_nr)
        self.set_phase_compensation_nr()
        self.cmw_query('*OPC?')
        self.set_repetition_nr('SING')
        self.set_plc_nr()
        self.set_channel_type_nr()
        self.set_uldl_periodicity_nr('MS25')
        self.set_uldl_pattern_nr(self.scs)
        self.set_rf_setting_user_margin_nr(10.00)
        self.set_expect_power_nr(self.tx_level + 5)
        self.set_rf_tx_port_nr(self.port_tx)
        self.set_rf_setting_user_margin_nr(10.00)
        self.set_modulation_count_nr(5)
        self.set_aclr_count_nr(5)
        self.set_sem_count_nr(5)
        self.set_trigger_source_nr('GPRF GEN1: Restart Marker')
        self.set_trigger_threshold_nr(-20)
        self.set_repetition_nr('SING')
        self.set_measurements_enable_all_nr()
        self.set_measured_subframe_nr(10)
        self.set_measured_slot_nr('ALL')
        self.set_scenario_activate_nr('SAL')
        self.set_rf_setting_external_tx_port_attenuation_nr(self.loss_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_gprf(self.port_tx)
        self.cmw_query(f'*OPC?')
        self.set_rf_tx_port_nr(self.port_tx)
        self.cmw_query(f'*OPC?')
        self.system_err_all_query()
        self.set_measure_start_on_nr()
        self.cmw_query(f'*OPC?')
        mod_results = self.get_modulation_avgerage_nr()
        aclr_results = self.get_aclr_average_nr()
        aclr_results[3] = mod_results[-1]  # real measured power, not carrier power
        mod_results.pop()
        self.get_in_band_emissions_nr()
        self.get_flatness_extreme_nr()
        # time.sleep(0.2)
        self.get_sem_average_and_margin_nr()
        self.set_measure_stop_nr()
        self.cmw_query('*OPC?')
        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, NR_-1, Pwr, NR_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def tx_measure_ulca_lte(self):
        # measurement like tx measure button
        self.set_mcs_lte(self.mcs_cc1_lte)
        self.set_type_cyclic_prefix_lte('NORM')
        self.set_plc_lte(0)
        self.set_delta_sequence_shift_lte(0)
        self.set_rf_setting_external_tx_port_attenuation_lte(self.loss_tx)
        self.set_expect_power_lte(self.tx_level)
        self.set_rf_setting_user_margin_lte(10)
        self.set_rb_auto_detect_lte('ON')
        self.set_meas_on_exception_lte('ON')
        self.set_modulation_count_lte(5)
        self.cmw_query('*OPC?')
        self.set_aclr_count_lte(5)
        self.cmw_query('*OPC?')
        self.set_sem_count_lte(5)
        self.cmw_query('*OPC?')
        self.set_trigger_source_lte('GPRF Gen1: Restart Marker')
        self.set_trigger_threshold_lte(-20.0)
        self.set_repetition_lte('SING')
        self.set_measurements_enable_all_lte()
        self.cmw_query('*OPC?')
        self.set_measured_subframe_lte()
        self.system_err_all_query()
        self.set_rf_tx_port_gprf(self.port_tx)
        self.cmw_query('*OPC?')
        self.set_rf_tx_port_lte(self.port_tx)
        self.cmw_query('*OPC?')
        self.set_select_carrier('CC1')
        mod_results_cc1 = self.get_modulation_avgerage_lte()
        self.set_select_carrier('CC2')
        mod_results_cc2 = self.get_modulation_avgerage_lte()
        self.set_measure_start_on_lte()
        self.cmw_query('*OPC?')
        aclr_results_2cc = self.get_aclr_average_lte()
        sem_result_2cc = self.get_sem_average_query_lte().split(',')[-2:]
        sem_result_2cc = [eval(r) for r in sem_result_2cc]

        return sem_result_2cc + aclr_results_2cc + mod_results_cc1 + mod_results_cc2

    def tx_measure_lte(self):
        logger.info('---------Tx Measure----------')
        self.select_mode_fdd_tdd(self.band_lte)
        self.set_band_lte(self.band_lte)
        self.set_tx_freq_lte(self.tx_freq_lte)
        self.cmw_query('*OPC?')
        self.set_bw_lte(self.bw_lte)
        self.set_mcs_lte(self.mcs_lte)
        self.set_rb_size_lte(self.rb_size_lte)
        self.set_rb_start_lte(self.rb_start_lte)
        self.set_type_cyclic_prefix_lte('NORM')
        self.set_plc_lte(0)
        self.set_delta_sequence_shift_lte(0)
        self.set_rb_auto_detect_lte('OFF')
        self.set_meas_on_exception_lte('ON')
        self.set_sem_limit_lte(self.bw_lte)
        self.system_err_all_query()
        self.set_measured_slot_lte('ALL')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_expect_power_lte(self.tx_level + 5)
        self.set_rf_tx_port_lte(1)
        self.cmw_query('*OPC?')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_rb_auto_detect_lte('ON')
        self.set_modulation_count_lte(5)
        self.cmw_query('*OPC?')
        self.set_aclr_count_lte(5)
        self.cmw_query('*OPC?')
        self.set_sem_count_lte(5)
        self.cmw_query('*OPC?')
        self.set_trigger_source_lte('GPRF Gen1: Restart Marker')
        self.set_trigger_threshold_lte(-20.0)
        self.set_repetition_lte('SING')
        self.set_measurements_enable_all_lte()
        self.cmw_query('*OPC?')
        self.set_measured_subframe_lte()
        self.set_scenario_activate_lte('SAL')
        self.system_err_all_query()
        self.set_rf_tx_port_gprf(self.port_tx)
        self.cmw_query('*OPC?')
        self.set_rf_tx_port_lte(self.port_tx)
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_tx_port_attenuation_lte(self.loss_tx)
        self.cmw_query('*OPC?')
        time.sleep(0.2)
        mod_results = self.get_modulation_avgerage_lte()
        self.set_measure_start_on_lte()
        self.cmw_query('*OPC?')
        aclr_results = self.get_aclr_average_lte()
        aclr_results[3] = mod_results[-1]
        mod_results.pop()
        self.get_in_band_emissions_lte()
        self.get_flatness_extreme_lte()
        time.sleep(0.2)
        self.get_sem_average_and_margin_lte()
        self.set_measure_stop_lte()
        self.cmw_query('*OPC?')
        logger.debug(aclr_results + mod_results)
        return aclr_results + mod_results  # U_-2, U_-1, E_-1, Pwr, E_+1, U_+1, U_+2, EVM, Freq_Err, IQ_OFFSET

    def tx_measure_wcdma(self):
        logger.info('---------Tx Measure----------')
        self.cmw_write(f'*CLS')
        self.set_modulation_count_wcdma(5)
        self.set_aclr_count_wcdma(5)
        self.set_rf_tx_port_wcdma(self.port_tx)
        self.set_rf_setting_external_tx_port_attenuation_wcdma(self.loss_tx)
        self.set_rf_setting_user_margin_wcdma(10.00)
        self.set_trigger_source_wcdma('Free Run (Fast sync)')
        self.set_trigger_threshold_wcdma(-30)
        self.set_repetition_wcdma(f'SING')
        self.set_measurements_enable_all_wcdma()
        self.cmw_query('*OPC?')
        self.system_err_all_query()
        self.set_band_wcdma(self.band_wcdma)
        self.set_tx_freq_wcdma(self.tx_chan_wcdma)
        self.set_ul_dpdch_wcdma('ON')
        self.set_ul_dpcch_slot_format_wcdma(0)
        self.set_scrambling_code_wcdma(13496235)
        self.set_ul_signal_config_wcdma('WCDM')
        self.system_err_all_query()
        self.set_rf_setting_user_margin_wcdma(10.00)
        self.set_expect_power_wcdma(self.tx_level + 5)
        mod_results = self.get_modulation_avgerage_wcdma()
        self.set_measure_start_on_wcdma()
        self.cmw_query(f'*OPC?')
        spectrum_results = self.get_aclr_average_wcdma()
        self.set_measure_stop_wcdma()
        self.cmw_query('*OPC?')
        return spectrum_results + mod_results  # U_-2, U_-1, U_+1, U_+2, OBW, PWR, EVM, Freq_Err, IQ_OFFSE

    def tx_measure_gsm(self):
        logger.info('---------Tx Measure----------')
        self.set_pvt_count_gsm(5)
        self.set_modulation_count_gsm(5)
        self.set_spectrum_modulation_count_gsm(5)
        self.set_spectrum_switching_count_gsm(5)
        self.set_scenario_activate_gsm('STAN')
        self.cmw_query('*OPC?')
        self.set_rf_tx_port_gsm(self.port_tx)
        self.set_rf_setting_external_tx_port_attenuation_gsm(self.loss_tx)
        self.set_rf_setting_user_margin_gsm(10.00)
        self.set_trigger_source_gsm('Power')
        self.set_trigger_threshold_gsm(-20.0)
        self.set_repetition_gsm('SING')
        self.set_measurements_enable_all_gsm()
        self.cmw_query('*OPC?')
        self.set_orfs_modulation_measurement_off_gsm()
        self.set_spectrum_modulation_evaluation_area_gsm()
        self.set_orfs_switching_measurement_off_gsm()
        self.system_err_all_query()
        self.set_band_gsm(self.band_gsm)
        self.cmw_query('*OPC?')
        self.set_chan_gsm(self.rx_chan_gsm)
        self.cmw_query('*OPC?')
        self.set_meas_on_exception_gsm('ON')
        self.set_training_sequence_gsm(self.tsc)
        self.set_modulation_view_gsm(self.mod_gsm)
        self.cmw_query('*OPC?')
        self.set_measured_slot_gsm()
        self.cmw_query('*OPC?')
        self.system_err_all_query()
        self.power_init_gsm()
        self.set_expect_power_gsm(self.pwr_init_gsm)
        mod_results = self.get_modulation_average_gsm()
        self.set_measure_start_on_gsm()
        self.cmw_query(f'*OPC?')
        self.set_expect_power_gsm(mod_results[0])
        orfs_mod, orfs_sw = self.get_orfs_average_gsm()
        self.set_measure_stop_gsm()
        self.cmw_query('*OPC?')
        return mod_results + orfs_mod + orfs_sw  # [0~3] + [4~10] + [11~17]

    def tx_monitor_lte(self):
        """
        This is to measure the LTE power before measuring nr sensitivity for ENDC
        """
        logger.info('---------Tx Monitor----------')
        # self.sig_gen_lte()
        self.set_measurement_tx_monitor_enable_lte()
        self.cmw_query('*OPC?')
        self.set_trigger_source_lte('GPRF Gen1: Restart Marker')
        self.set_measured_slot_lte('ALL')
        self.set_trigger_threshold_lte(-20.0)
        self.set_repetition_lte('SING')
        self.set_meas_on_exception_lte('ON')
        self.set_type_cyclic_prefix_lte('NORM')
        self.set_measured_subframe_lte()
        self.set_rb_auto_detect_lte('ON')
        self.select_mode_fdd_tdd(self.band_lte)
        self.set_band_lte(self.band_lte)
        self.set_bw_lte(self.bw_lte)
        self.set_mcs_lte(self.mcs_lte)
        self.set_tx_freq_lte(self.tx_freq_lte)
        self.cmw_query('*OPC?')
        self.set_rf_setting_external_tx_port_attenuation_lte(self.loss_tx)
        self.cmw_query('*OPC?')
        self.set_rf_tx_port_gprf(self.port_tx)
        self.cmw_query('*OPC?')
        self.set_rf_tx_port_lte(self.port_tx)
        self.cmw_query('*OPC?')
        self.set_rf_setting_user_margin_lte(10.00)
        self.set_expect_power_lte(self.tx_level)
        self.cmw_query('*OPC?')
        self.set_measure_start_on_lte()
        power_results = self.get_power_monitor_avgerage_lte()
        power = power_results.strip().split(',')[2]
        logger.info(f'LTE power by Tx monitor: {round(eval(power), 2)}')
        return round(eval(power), 2)

    @staticmethod
    def port_tx_table(txas_select):
        table = port_tx_table_transfer(txas_select)
        return table

    def set_fdcorrection_create_activate_process(self):
        """
        this is to create 8 tables for fd_correction and then set to activate the tables
        """
        if self.fdc_en:
            for p in range(8):
                self.set_fd_correction_create(p + 1, read_fdc_file(p + 1))

            self.set_fd_correction_activate_txrx()

    @staticmethod
    def loss_selector(freq, fdc_en):
        if fdc_en:
            return 0

        else:
            return get_loss(freq)


def main():
    cmw100 = CMW100()
    cmw100.cmw_query('*IDN?')


if __name__ == '__main__':
    main()
