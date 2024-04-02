from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QStyleFactory, QFileDialog
from PySide6.QtCore import QThread, Slot, QSize
import sys
import time
import threading

from ui_mega_v2_7 import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_show()
        self.init_hidden()
        self.custom_signal_slot()
        self.measured_counts = None

    def custom_signal_slot(self):
        self.as_path_en.toggled.connect(self.srs_unchecked)
        self.srs_path_en.toggled.connect(self.as_unchecked)
        self.run_button.clicked.connect(self.run_start)
        self.therm_charge_dis_button.clicked.connect(self.therm_charge_dis)
        self.stop_button.clicked.connect(self.stop)
        self.equipments_comboBox.currentTextChanged.connect(self.equipment_show)
        self.tx_port_comboBox.currentTextChanged.connect(self.tx_port_show)
        self.tx_port_endc_lte_comboBox.currentTextChanged.connect(self.tx_port_endc_lte_show)
        self.rx_endc_desense_ns.stateChanged.connect(self.tx_port_endc_lte_state)
        self.equipments_comboBox.textActivated.connect(self.showout_en)
        self.run_button.clicked.connect(self.selected_show)

    def init_show(self):
        print(f'Equipment: {self.equipments_comboBox.currentText()}')
        print(f'Tx port: {self.tx_port_comboBox.currentText()}')
        print(f'NR bands: {self.nr_bands_selected()}')
        print(f'LTE bands: {self.lte_bands_selected()}')
        print(f'WCDMA bands: {self.wcdma_bands_selected()}')
        print(f'GSM bands: {self.gsm_bands_selected()}')
        print(f'ULCA LTE bands: {self.ulca_lte_bands_selected()}')
        print(f'NR BWs: {self.nr_bw_selected()}')
        print(f'LTE BWs: {self.lte_bw_selected()}')
        print(f'ULCA LTE BWs: {self.ulca_lte_bw_selected()}')
        print(f'NR RB allocation: {self.nr_rb_allocation_selected()}')
        print(f'NR TYPE: {self.nr_type_selected()}')
        print(f'NR MCS: {self.nr_mcs_selected()}')
        print(f'LTE RB allocation: {self.lte_rb_allocation_selected()}')
        print(f'LTE MCS: {self.lte_mcs_selected()}')
        print(f'ULCA LTE RB allocation: {self.ulca_lte_rb_allocation_selected()}')
        print(f'ULCA LTE MCS: {self.lte_mcs_selected()}')
        print(f'ULCA LTE criteria: {self.ulca_lte_critera_selected()}')

    def init_hidden(self):
        match self.equipments_comboBox.currentText():
            case 'Cmw100':
                self.hsupa_tech.setHidden(True)
                self.hsdpa_tech.setHidden(True)
                self.hsupa_tech.setChecked(False)
                self.hsdpa_tech.setChecked(False)
            case 'Cmw100+Fsw':
                self.hsupa_tech.setHidden(True)
                self.hsdpa_tech.setHidden(True)
                self.hsupa_tech.setChecked(False)
                self.hsdpa_tech.setChecked(False)
            case 'Anritsu8820':
                self.hsupa_tech.setHidden(False)
                self.hsdpa_tech.setHidden(False)
            case 'Anritsu8821':
                self.nr_tech.setHidden(True)
                self.wcdma_tech.setHidden(True)
                self.gsm_tech.setHidden(True)
                self.ulca_lte_tech.setHidden(True)
                self.hsupa_tech.setHidden(True)
                self.hsdpa_tech.setHidden(True)
                self.nr_tech.setChecked(False)
                self.wcdma_tech.setChecked(False)
                self.gsm_tech.setChecked(False)
                self.ulca_lte_tech.setChecked(False)
                self.hsupa_tech.setChecked(False)
                self.hsdpa_tech.setChecked(False)

    def selected_show(self):
        print(f'NR bands: {self.nr_bands_selected()}')
        print(f'LTE bands: {self.lte_bands_selected()}')
        print(f'WCDMA bands: {self.wcdma_bands_selected()}')
        print(f'GSM bands: {self.gsm_bands_selected()}')
        print(f'ULCA LTE bands: {self.ulca_lte_bands_selected()}')
        print(f'NR BWs: {self.nr_bw_selected()}')
        print(f'LTE BWs: {self.lte_bw_selected()}')
        print(f'ULCA LTE BWs: {self.ulca_lte_bw_selected()}')
        print(f'NR RB allocation: {self.nr_rb_allocation_selected()}')
        print(f'NR TYPE: {self.nr_type_selected()}')
        print(f'NR MCS: {self.nr_mcs_selected()}')
        print(f'LTE RB allocation: {self.lte_rb_allocation_selected()}')
        print(f'LTE MCS: {self.lte_mcs_selected()}')
        print(f'ULCA LTE RB allocation: {self.ulca_lte_rb_allocation_selected()}')
        print(f'ULCA LTE MCS: {self.lte_mcs_selected()}')
        print(f'ULCA LTE criteria: {self.ulca_lte_critera_selected()}')

    def srs_unchecked(self, checked):
        # if self.as_path_en.isChecked():
        #     self.srs_path_en.setChecked(False)
        if checked:
            self.srs_path_en.setChecked(False)

    def as_unchecked(self, checked):
        # if self.srs_path_en.isChecked():
        #     self.as_path_en.setChecked(False)
        if checked:
            self.as_path_en.setChecked(False)

    def gui_state_get(self, state_dict):
        state_dict['equipment'] = self.equipments_comboBox.currentText()
        state_dict['tx_port_table_en'] = self.port_table_en.isChecked()
        state_dict['tx_port'] = self.tx_port_comboBox.CurrentText()
        state_dict['tx_port_endc_lte'] = self.tx_port_endc_lte_comboBox.currentText()
        state_dict['volt_mipi_en'] = self.volt_mipi_en.isChecked()
        state_dict['get_temp_en'] = self.get_temp_en.isChecked()
        state_dict['fdc_en'] = self.fdc_en.isChecked()
        state_dict['fbrx_en'] = self.fbrx_en.isChecked()
        state_dict['mipi_read_en'] = self.mipi_read_en.isChecked()
        state_dict['test_items_toolbox_index'] = self.test_items_toolBox.currentIndex()
        state_dict['tx_lmh_ns'] = self.tx_lmh_ns.isChecked()
        state_dict['tx_level_sweep_ns'] = self.tx_level_sweep_ns.isChecked()
        state_dict['tx_freq_sweep_ns'] = self.tx_freq_sweep_ns.isChecked()
        state_dict['tx_1rb_sweep_ns'] = self.tx_1rb_sweep_ns.isChecked()
        state_dict['tx_fcc_power_ns'] = self.tx_fcc_power_ns.isChecked()
        state_dict['tx_ce_power_ns'] = self.tx_ce_power_ns.isChecked()
        state_dict['tx_harmonics_ns'] = self.tx_harmonics_ns.isChecked()
        state_dict['tx_cbe_ns'] = self.tx_cbe_ns.isChecked()
        state_dict['tx_ulca_lte_ns'] = self.tx_ulca_lte_ns.isChecked()
        state_dict['tx_ulca_lte_cbe_ns'] = self.tx_ulca_lte_cbe_ns.isChecked()
        state_dict['rx_normal_ns'] = self.rx_normal_ns.isChecked()
        state_dict['rx_quick_ns'] = self.rx_quick_ns.isChecked()
        state_dict['rx_endc_desense_ns'] = self.rx_endc_desense_ns.isChecked()
        state_dict['tx_lmh_s'] = self.tx_lmh_s.isChecked()
        state_dict['rx_normal_s'] = self.rx_normal_s.isChecked()
        state_dict['rxs_sweep_s'] = self.rxs_sweep_s.isChecked()
        state_dict['cbe_margin'] = float(self.cbe_margin.text())
        state_dict['sync_path_toolBox_index'] = self.sync_path_toolBox.currentIndex()
        state_dict['sync_path'] = self.sync_path_comboBox.currentText()
        state_dict['as_path_en'] = self.as_path_en.isChecked()
        state_dict['as_path'] = self.as_path_comboBox.currentText()
        state_dict['srs_path_en'] = self.srs_path_en.isChecked()
        state_dict['srs_path'] = self.srs_path_comboBox.currentText()
        state_dict['tx_level'] = self.tx_level_spinBox.value()
        state_dict['pcl_lb_level'] = self.pcl_lb_level_combo.currentText()
        state_dict['pcl_mb_level'] = self.pcl_mb_level_combo.currentText()
        state_dict['sync_path_endc'] = self.sync_path_comboBox_endc.currentText()
        state_dict['as_path_en_endc'] = self.as_path_en_endc.isChecked()
        state_dict['as_path_endc'] = self.as_path_comboBox_endc.currentText()
        state_dict['tx_level_lte_endc'] = self.tx_level_lte_spinBox_endc.value()
        state_dict['tx_level_nr_endc'] = self.tx_level_nr_spinBox_endc.value()
        state_dict['level_sweep_start'] = self.level_sweep_start_spinBox.value()
        state_dict['level_sweep_stop'] = self.level_stop_spinBox.value()
        state_dict['freq_sweep_step'] = int(self.freq_sweep_step.text())
        state_dict['freq_sweep_start'] = int(self.freq_sweep_start.text())
        state_dict['freq_sweep_stop'] = int(self.freq_sweep_stop.text())
        state_dict['txrx_path_toolBox_index'] = self.txrx_path_toolBox.currentIndex()
        state_dict['tx1'] = self.tx1.isChecked()
        state_dict['tx2'] = self.tx2.isChecked()
        state_dict['mimo'] = self.ulmimo.isChecked()
        state_dict['rx0'] = self.rx0.isChecked()
        state_dict['rx1'] = self.rx1.isChecked()
        state_dict['rx2'] = self.rx2.isChecked()
        state_dict['rx3'] = self.rx3.isChecked()
        state_dict['rx0rx1'] = self.rx0_rx1.isChecked()
        state_dict['rx2rx3'] = self.rx2_rx3.isChecked()
        state_dict['rx_all_path'] = self.rx_all_path.isChecked()
        state_dict['endc_tx1_path_lte'] = self.endc_tx1_path_lte_radioButton.isChecked()
        state_dict['endc_tx2_path_lte'] = self.endc_tx2_path_lte_radioButton.isChecked()
        state_dict['endc_tx1_path_nr'] = self.endc_tx1_path_nr_radioButton.isChecked()
        state_dict['endc_tx2_path_nr'] = self.endc_tx2_path_nr_radioButton.isChecked()
        state_dict['rx_all_path_endc_lte'] = self.rx_all_path_endc_lte.isChecked()
        state_dict['rx_all_path_endc_nr'] = self.rx_all_path_endc_nr.isChecked()
        state_dict['ue_txmax'] = self.ue_txmax.isChecked()
        state_dict['ue_txlow'] = self.ue_txlow.isChecked()
        state_dict['nr_tech'] = self.nr_tech.isChecked()
        state_dict['lte_tech'] = self.lte_tech.isChecked()
        state_dict['wcdma_tech'] = self.wcdma_tech.isChecked()
        state_dict['gsm_tech'] = self.gsm_tech.isChecked()
        state_dict['ulca_lte_tech'] = self.ulca_lte_tech.isChecked()
        state_dict['hsupa_tech'] = self.hsupa_tech.isChecked()
        state_dict['hsdpa_tech'] = self.hsdpa_tech.isChecked()
        state_dict['lch'] = self.lch.isChecked()
        state_dict['mch'] = self.mch.isChecked()
        state_dict['hch'] = self.hch.isChecked()
        state_dict['tabWidget_index'] = self.tabWidget.currentIndex()
        state_dict['bands_toolBox_index'] = self.bands_toolBox.currentIndex()
        state_dict['n5_nr'] = self.n5_nr.isChecked()
        state_dict['n8_nr'] = self.n8_nr.isChecked()
        state_dict['n12_nr'] = self.n12_nr.isChecked()
        state_dict['n13_nr'] = self.n13_nr.isChecked()
        state_dict['n14_nr'] = self.n14_nr.isChecked()
        state_dict['n20_nr'] = self.n20_nr.isChecked()
        state_dict['n24_nr'] = self.n24_nr.isChecked()
        state_dict['n26_nr'] = self.n26_nr.isChecked()
        state_dict['n71_nr'] = self.n71_nr.isChecked()
        state_dict['n28_a_nr'] = self.n28_a_nr.isChecked()
        state_dict['n28_b_nr'] = self.n28_b_nr.isChecked()
        state_dict['n29_nr'] = self.n29_nr.isChecked()
        state_dict['n32_nr'] = self.n32_nr.isChecked()
        state_dict['n1_nr'] = self.n1_nr.isChecked()
        state_dict['n2_nr'] = self.n2_nr.isChecked()
        state_dict['n3_nr'] = self.n3_nr.isChecked()
        state_dict['n4_nr'] = self.n4_nr.isChecked()
        state_dict['n7_nr'] = self.n7_nr.isChecked()
        state_dict['n30_nr'] = self.n30_nr.isChecked()
        state_dict['n25_nr'] = self.n25_nr.isChecked()
        state_dict['n66_nr'] = self.n66_nr.isChecked()
        state_dict['n70_nr'] = self.n70_nr.isChecked()
        state_dict['n39_nr'] = self.n39_nr.isChecked()
        state_dict['n40_nr'] = self.n40_nr.isChecked()
        state_dict['n38_nr'] = self.n38_nr.isChecked()
        state_dict['n41_nr'] = self.n41_nr.isChecked()
        state_dict['n34_nr'] = self.n34_nr.isChecked()
        state_dict['n75_nr'] = self.n75_nr.isChecked()
        state_dict['n76_nr'] = self.n76_nr.isChecked()
        state_dict['n255_nr'] = self.n255_nr.isChecked()
        state_dict['n256_nr'] = self.n256_nr.isChecked()
        state_dict['n77_nr'] = self.n77_nr.isChecked()
        state_dict['n78_nr'] = self.n78_nr.isChecked()
        state_dict['n79_nr'] = self.n79_nr.isChecked()
        state_dict['b5_lte'] = self.b5_lte.isChecked()
        state_dict['b8_lte'] = self.b8_lte.isChecked()
        state_dict['b12_lte'] = self.b12_lte.isChecked()
        state_dict['b13_lte'] = self.b13_lte.isChecked()
        state_dict['b14_lte'] = self.b14_lte.isChecked()
        state_dict['b17_lte'] = self.b17_lte.isChecked()
        state_dict['b18_lte'] = self.b18_lte.isChecked()
        state_dict['b19_lte'] = self.b19_lte.isChecked()
        state_dict['b20_lte'] = self.b20_lte.isChecked()
        state_dict['b26_lte'] = self.b26_lte.isChecked()
        state_dict['b28_a_lte'] = self.b28_a_lte.isChecked()
        state_dict['b28_b_lte'] = self.b28_b_lte.isChecked()
        state_dict['b29_lte'] = self.b29_lte.isChecked()
        state_dict['b32_lte'] = self.b32_lte.isChecked()
        state_dict['b71_lte'] = self.b71_lte.isChecked()
        state_dict['b24_lte'] = self.b24_lte.isChecked()
        state_dict['b1_lte'] = self.b1_lte.isChecked()
        state_dict['b2_lte'] = self.b2_lte.isChecked()
        state_dict['b3_lte'] = self.b3_lte.isChecked()
        state_dict['b4_lte'] = self.b4_lte.isChecked()
        state_dict['b7_lte'] = self.b7_lte.isChecked()
        state_dict['b30_lte'] = self.b30_lte.isChecked()
        state_dict['b25_lte'] = self.b25_lte.isChecked()
        state_dict['b66_lte'] = self.b66_lte.isChecked()
        state_dict['b21_lte'] = self.b21_lte.isChecked()
        state_dict['b39_lte'] = self.b39_lte.isChecked()
        state_dict['b40_lte'] = self.b40_lte.isChecked()
        state_dict['b38_lte'] = self.b38_lte.isChecked()
        state_dict['b41_lte'] = self.b41_lte.isChecked()
        state_dict['b23_lte'] = self.b23_lte.isChecked()
        state_dict['b42_lte'] = self.b42_lte.isChecked()
        state_dict['b48_lte'] = self.b48_lte.isChecked()
        state_dict['b5_wcdma'] = self.b5_wcdma.isChecked()
        state_dict['b8_wcdma'] = self.b8_wcdma.isChecked()
        state_dict['b6_wcdma'] = self.b6_wcdma.isChecked()
        state_dict['b19_wcdma'] = self.b19_wcdma.isChecked()
        state_dict['b1_wcdma'] = self.b1_wcdma.isChecked()
        state_dict['b2_wcdma'] = self.b2_wcdma.isChecked()
        state_dict['b4_wcdma'] = self.b4_wcdma.isChecked()
        state_dict['gsm850'] = self.gsm850.isChecked()
        state_dict['gsm900'] = self.gsm850.isChecked()
        state_dict['gsm1800'] = self.gsm1800.isChecked()
        state_dict['gsm1900'] = self.gsm1900.isChecked()
        state_dict['ulca_5b'] = self.ulca_5b.isChecked()
        state_dict['ulca_1c'] = self.ulca_1c.isChecked()
        state_dict['ulca_3c'] = self.ulca_3c.isChecked()
        state_dict['ulca_7c'] = self.ulca_7c.isChecked()
        state_dict['ulca_66b'] = self.ulca_66b.isChecked()
        state_dict['ulca_66c'] = self.ulca_66c.isChecked()
        state_dict['ulca_40c'] = self.ulca_40c.isChecked()
        state_dict['ulca_38c'] = self.ulca_38c.isChecked()
        state_dict['ulca_41c'] = self.ulca_41c.isChecked()
        state_dict['ulca_42c'] = self.ulca_42c.isChecked()
        state_dict['ulca_48c'] = self.ulca_48c.isChecked()
        state_dict['bw1p4_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw3_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw5_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw10_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw15_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw20_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw5_nr'] = self.bw5_nr.isChecked()
        state_dict['bw10_nr'] = self.bw10_nr.isChecked()
        state_dict['bw15_nr'] = self.bw15_nr.isChecked()
        state_dict['bw20_nr'] = self.bw20_nr.isChecked()
        state_dict['bw25_nr'] = self.bw25_nr.isChecked()
        state_dict['bw30_nr'] = self.bw30_nr.isChecked()
        state_dict['bw40_nr'] = self.bw40_nr.isChecked()
        state_dict['bw50_nr'] = self.bw50_nr.isChecked()
        state_dict['bw60_nr'] = self.bw60_nr.isChecked()
        state_dict['bw80_nr'] = self.bw80_nr.isChecked()
        state_dict['bw90_nr'] = self.bw90_nr.isChecked()
        state_dict['bw100_nr'] = self.bw100_nr.isChecked()
        state_dict['bw70_nr'] = self.bw70_nr.isChecked()
        state_dict['bw35_nr'] = self.bw35_nr.isChecked()
        state_dict['bw45_nr'] = self.bw45_nr.isChecked()
        state_dict['bw20_5'] = self.bw20_5.isChecked()
        state_dict['bw5_20'] = self.bw5_20.isChecked()
        state_dict['bw20_10'] = self.bw20_10.isChecked()
        state_dict['bw10_20'] = self.bw10_20.isChecked()
        state_dict['bw20_15'] = self.bw20_15.isChecked()
        state_dict['bw15_20'] = self.bw15_20.isChecked()
        state_dict['bw20_20'] = self.bw20_20.isChecked()
        state_dict['bw15_15'] = self.bw15_15.isChecked()
        state_dict['bw15_10'] = self.bw15_10.isChecked()
        state_dict['bw10_15'] = self.bw10_15.isChecked()
        state_dict['bw5_10'] = self.bw5_10.isChecked()
        state_dict['bw10_5'] = self.bw10_5.isChecked()
        state_dict['bw10_10'] = self.bw10_10.isChecked()
        state_dict['bw5_15'] = self.bw5_15.isChecked()
        state_dict['bw15_5'] = self.bw15_5.isChecked()
        state_dict['bw40'] = self.bw40.isChecked()
        state_dict['qpsk_lte'] = self.qpsk_lte.isChecked()
        state_dict['q16_lte'] = self.q16_lte.isChecked()
        state_dict['q64_lte'] = self.q64_lte.isChecked()
        state_dict['q256_lte'] = self.q256_lte.isChecked()
        state_dict['qpsk_nr'] = self.qpsk_nr.isChecked()
        state_dict['q16_nr'] = self.q16_nr.isChecked()
        state_dict['q64_nr'] = self.q64_nr.isChecked()
        state_dict['q256_nr'] = self.q256_nr.isChecked()
        state_dict['bpsk_nr'] = self.bpsk_nr.isChecked()
        state_dict['dfts_nr'] = self.dfts_nr.isChecked()
        state_dict['cp_nr'] = self.cp_nr.isChecked()
        state_dict['prb0_lte'] = self.prb0_lte.isChecked()
        state_dict['prbmax_lte'] = self.prbmax_lte.isChecked()
        state_dict['frb_lte'] = self.frb_lte.isChecked()
        state_dict['one_rb_0_lte'] = self.one_rb_0_lte.isChecked()
        state_dict['one_rb_max_lte'] = self.one_rb_max_lte.isChecked()
        state_dict['one_rb0_null'] = self.one_rb0_null.setChecked()
        state_dict['prb0_null'] = self.prb0_null.isChecked()
        state_dict['frb_null'] = self.frb_null.isChecked()
        state_dict['frb_frb'] = self.frb_frb.isChecked()
        state_dict['one_rb0_one_rbmax'] = self.one_rb0_one_rbmax.isChecked()
        state_dict['one_rbmax_one_rb0'] = self.one_rbmax_one_rb0.isChecked()
        state_dict['criteria_ulca_lte_3gpp'] = self.criteria_ulca_lte_3gpp_radioButton.isChecked()
        state_dict['criteria_ulca_lte_fcc'] = self.criteria_ulca_lte_fcc_radioButton.isChecked()
        state_dict['inner_full_nr'] = self.inner_full_nr.isChecked()
        state_dict['outer_full_nr'] = self.outer_full_nr.isChecked()
        state_dict['inner_1rb_left_nr'] = self.inner_1rb_left_nr.isChecked()
        state_dict['inner_1rb_right_nr'] = self.inner_1rb_right_nr.isChecked()
        state_dict['edge_1rb_left_nr'] = self.edge_1rb_left_nr.isChecked()
        state_dict['edge_1rb_right_nr'] = self.edge_1rb_right_nr.isChecked()
        state_dict['edge_full_left_nr'] = self.edge_full_left_nr.isChecked()
        state_dict['edge_full_right_nr'] = self.edge_full_right_nr.isChecked()
        state_dict['tmpchmb_en'] = self.tmpchmb_en.isChecked()
        state_dict['hthv_en'] = self.hthv_en.isChecked()
        state_dict['htlv_en'] = self.htlv_en.isChecked()
        state_dict['ntnv_en'] = self.ntnv_en.isChecked()
        state_dict['lthv_en'] = self.lthv_en.isChecked()
        state_dict['ltlv_en'] = self.ltlv_en.isChecked()
        state_dict['wait_time'] = int(self.wait_time_comboBox.currentText())
        state_dict['psu_en'] = self.psu_en.isChecked()
        state_dict['hv_en'] = self.hv_en.isChecked()
        state_dict['nv_en'] = self.nv_en.isChecked()
        state_dict['lv_en'] = self.lv_en.isChecked()
        state_dict['odpm2_en'] = self.odpm2_en.isChecked()
        state_dict['ht_value'] = self.ht_spinBox.value()
        state_dict['nt_value'] = self.nt_spinBox.value()
        state_dict['lt_value'] = self.lt_spinBox.value()
        state_dict['hv_value'] = self.hv_doubleSpinBox.value()
        state_dict['nv_value'] = self.nv_doubleSpinBox.value()
        state_dict['lv_value'] = self.lv_doubleSpinBox.value()
        state_dict['input_level_sig_anritsu'] = self.input_level_sig_anritsu_spinBox.value()
        state_dict['rfout_port_sig_anritsu'] = self.rfout_port_sig_anritsu_comboBox.value()

        return state_dict

    def gui_state_set(self, state_dict):
        self.equipments_comboBox.setCurrentText(state_dict['equipment'])
        self.port_table_en.setChecked(state_dict['tx_port_table_en'])
        self.tx_port_comboBox.setCurrentText(state_dict['tx_port'])
        self.tx_port_endc_lte_comboBox.setcurrentText(state_dict['tx_port_endc_lte'])
        self.volt_mipi_en.setChecked(state_dict['volt_mipi_en'])
        self.get_temp_en.setChecked(state_dict['get_temp_en'])
        self.fdc_en.setChecked(state_dict['fdc_en'])
        self.fbrx_en.setChecked(state_dict['fbrx_en'])
        self.mipi_read_en.setChecked(state_dict['mipi_read_en'])
        self.test_items_toolBox.setCurrentIndex(state_dict['test_items_toolbox_index'])
        self.tx_lmh_ns.setChecked(state_dict['tx_lmh_ns'])
        self.tx_level_sweep_ns.setChecked(state_dict['tx_level_sweep_ns'])
        self.tx_freq_sweep_ns.setChecked(state_dict['tx_freq_sweep_ns'])
        self.tx_1rb_sweep_ns.setChecked(state_dict['tx_1rb_sweep_ns'])
        self.tx_fcc_power_ns.setChecked(state_dict['tx_fcc_power_ns'])
        self.tx_ce_power_ns.setChecked(state_dict['tx_ce_power_ns'])
        self.tx_harmonics_ns.setChecked(state_dict['tx_harmonics_ns'])
        self.tx_cbe_ns.setChecked(state_dict['tx_cbe_ns'])
        self.tx_ulca_lte_ns.setChecked(state_dict['tx_ulca_lte_ns'])
        self.tx_ulca_lte_cbe_ns.setChecked(state_dict['tx_ulca_lte_cbe_ns'])
        self.rx_normal_ns.setChecked(state_dict['rx_normal_ns'])
        self.rx_quick_ns.setChecked(state_dict['rx_quick_ns'])
        self.rx_endc_desense_ns.setChecked(state_dict['rx_endc_desense_ns'])
        self.tx_lmh_s.setChecked(state_dict['tx_lmh_s'])
        self.rx_normal_s.setChecked(state_dict['rx_normal_s'])
        self.rxs_sweep_s.setChecked(state_dict['rxs_sweep_s'])
        self.cbe_margin.setText((state_dict['cbe_margin']))
        self.sync_path_toolBox.setCurrentIndex(state_dict['sync_path_toolBox_index'])
        self.sync_path_comboBox.setCurrentText(state_dict['sync_path'])
        self.as_path_en.setChecked(state_dict['as_path_en'])
        self.as_path_comboBox.setCurrentText(state_dict['as_path'])
        self.srs_path_en.setChecked(state_dict['srs_path_en'])
        self.srs_path_comboBox.setCurrentText(state_dict['srs_path'])
        self.tx_level_spinBox.setValue(state_dict['tx_level'])
        self.pcl_lb_level_combo.setCurrentText(state_dict['pcl_lb_level'])
        self.pcl_mb_level_combo.setCurrentText(state_dict['pcl_mb_level'])
        self.sync_path_comboBox_endc.setCurrentText(state_dict['sync_path_endc'])
        self.as_path_en_endc.setChecked(state_dict['as_path_en_endc'])
        self.as_path_comboBox_endc.setCurrentText(state_dict['as_path_endc'])
        self.tx_level_lte_spinBox_endc.setValue(state_dict['tx_level_lte_endc'])
        self.tx_level_nr_spinBox_endc.setValue(state_dict['tx_level_nr_endc'])
        self.level_sweep_start_spinBox.setValue(state_dict['level_sweep_start'])
        self.level_stop_spinBox.setValue(state_dict['level_sweep_stop'])
        self.freq_sweep_step.setText(str(state_dict['freq_sweep_step']))  # Convert to string
        self.freq_sweep_start.setText(str(state_dict['freq_sweep_start']))
        self.freq_sweep_stop.setText(str(state_dict['freq_sweep_stop']))
        self.txrx_path_toolBox.setCurrentIndex(state_dict['txrx_path_toolBox_index'])
        self.tx1.setChecked(state_dict['tx1'])
        self.tx2.setChecked(state_dict['tx2'])
        self.ulmimo.setChecked(state_dict['mimo'])
        self.rx0.setChecked(state_dict['rx0'])
        self.rx1.setChecked(state_dict['rx1'])
        self.rx2.setChecked(state_dict['rx2'])
        self.rx3.setChecked(state_dict['rx3'])
        self.rx0_rx1.setChecked(state_dict['rx0rx1'])
        self.rx2_rx3.setChecked(state_dict['rx2rx3'])
        self.rx_all_path.setChecked(state_dict['rx_all_path'])
        self.endc_tx1_path_lte_radioButton.setChecked(state_dict['endc_tx1_path_lte'])
        self.endc_tx2_path_lte_radioButton.setChecked(state_dict['endc_tx2_path_lte'])
        self.endc_tx1_path_nr_radioButton.setChecked(state_dict['endc_tx1_path_nr'])
        self.endc_tx2_path_nr_radioButton.setChecked(state_dict['endc_tx2_path_nr'])
        self.rx_all_path_endc_lte.setChecked(state_dict['rx_all_path_endc_lte'])
        self.rx_all_path_endc_nr.setChecked(state_dict['rx_all_path_endc_nr'])
        self.ue_txmax.setChecked(state_dict['ue_txmax'])
        self.ue_txlow.setChecked(state_dict['ue_txlow'])
        self.nr_tech.setChecked(state_dict['nr_tech'])
        self.lte_tech.setChecked(state_dict['lte_tech'])
        self.wcdma_tech.setChecked(state_dict['wcdma_tech'])
        self.gsm_tech.setChecked(state_dict['gsm_tech'])
        self.ulca_lte_tech.setChecked(state_dict['ulca_lte_tech'])
        self.hsupa_tech.setChecked(state_dict['hsupa_tech'])
        self.hsdpa_tech.setChecked(state_dict['hsdpa_tech'])
        self.lch.setChecked(state_dict['lch'])
        self.mch.setChecked(state_dict['mch'])
        self.hch.setChecked(state_dict['hch'])
        self.tabWidget.setCurrentIndex(state_dict['tabWidget_index'])
        self.bands_toolBox.setCurrentIndex(state_dict['bands_toolBox_index'])
        self.n5_nr.setChecked(state_dict['n5_nr'])
        self.n8_nr.setChecked(state_dict['n8_nr'])
        self.n12_nr.setChecked(state_dict['n12_nr'])
        self.n13_nr.setChecked(state_dict['n13_nr'])
        self.n14_nr.setChecked(state_dict['n14_nr'])
        self.n20_nr.setChecked(state_dict['n20_nr'])
        self.n24_nr.setChecked(state_dict['n24_nr'])
        self.n26_nr.setChecked(state_dict['n26_nr'])
        self.n71_nr.setChecked(state_dict['n71_nr'])
        self.n28_a_nr.setChecked(state_dict['n28_a_nr'])
        self.n28_b_nr.setChecked(state_dict['n28_b_nr'])
        self.n29_nr.setChecked(state_dict['n29_nr'])
        self.n32_nr.setChecked(state_dict['n32_nr'])
        self.n1_nr.setChecked(state_dict['n1_nr'])
        self.n2_nr.setChecked(state_dict['n2_nr'])
        self.n3_nr.setChecked(state_dict['n3_nr'])
        self.n4_nr.setChecked(state_dict['n4_nr'])
        self.n7_nr.setChecked(state_dict['n7_nr'])
        self.n30_nr.setChecked(state_dict['n30_nr'])
        self.n25_nr.setChecked(state_dict['n25_nr'])
        self.n66_nr.setChecked(state_dict['n66_nr'])
        self.n70_nr.setChecked(state_dict['n70_nr'])
        self.n39_nr.setChecked(state_dict['n39_nr'])
        self.n40_nr.setChecked(state_dict['n40_nr'])
        self.n38_nr.setChecked(state_dict['n38_nr'])
        self.n41_nr.setChecked(state_dict['n41_nr'])
        self.n34_nr.setChecked(state_dict['n34_nr'])
        self.n75_nr.setChecked(state_dict['n75_nr'])
        self.n76_nr.setChecked(state_dict['n76_nr'])
        self.n255_nr.setChecked(state_dict['n255_nr'])
        self.n256_nr.setChecked(state_dict['n256_nr'])
        self.n77_nr.setChecked(state_dict['n77_nr'])
        self.n78_nr.setChecked(state_dict['n78_nr'])
        self.n79_nr.setChecked(state_dict['n79_nr'])
        self.b5_lte.setChecked(state_dict['b5_lte'])
        self.b8_lte.setChecked(state_dict['b8_lte'])
        self.b12_lte.setChecked(state_dict['b12_lte'])
        self.b13_lte.setChecked(state_dict['b13_lte'])
        self.b14_lte.setChecked(state_dict['b14_lte'])
        self.b17_lte.setChecked(state_dict['b17_lte'])
        self.b18_lte.setChecked(state_dict['b18_lte'])
        self.b19_lte.setChecked(state_dict['b19_lte'])
        self.b20_lte.setChecked(state_dict['b20_lte'])
        self.b26_lte.setChecked(state_dict['b26_lte'])
        self.b28_a_lte.setChecked(state_dict['b28_a_lte'])
        self.b28_b_lte.setChecked(state_dict['b28_b_lte'])
        self.b29_lte.setChecked(state_dict['b29_lte'])
        self.b32_lte.setChecked(state_dict['b32_lte'])
        self.b71_lte.setChecked(state_dict['b71_lte'])
        self.b24_lte.setChecked(state_dict['b24_lte'])
        self.b1_lte.setChecked(state_dict['b1_lte'])
        self.b2_lte.setChecked(state_dict['b2_lte'])
        self.b3_lte.setChecked(state_dict['b3_lte'])
        self.b4_lte.setChecked(state_dict['b4_lte'])
        self.b7_lte.setChecked(state_dict['b7_lte'])
        self.b30_lte.setChecked(state_dict['b30_lte'])
        self.b25_lte.setChecked(state_dict['b25_lte'])
        self.b66_lte.setChecked(state_dict['b66_lte'])
        self.b21_lte.setChecked(state_dict['b21_lte'])
        self.b39_lte.setChecked(state_dict['b39_lte'])
        self.b40_lte.setChecked(state_dict['b40_lte'])
        self.b38_lte.setChecked(state_dict['b38_lte'])
        self.b41_lte.setChecked(state_dict['b41_lte'])
        self.b23_lte.setChecked(state_dict['b23_lte'])
        self.b42_lte.setChecked(state_dict['b42_lte'])
        self.b48_lte.setChecked(state_dict['b48_lte'])
        self.b5_wcdma.setChecked(state_dict['b5_wcdma'])
        self.b8_wcdma.setChecked(state_dict['b8_wcdma'])
        self.b6_wcdma.setChecked(state_dict['b6_wcdma'])
        self.b19_wcdma.setChecked(state_dict['b19_wcdma'])
        self.b1_wcdma.setChecked(state_dict['b1_wcdma'])
        self.b2_wcdma.setChecked(state_dict['b2_wcdma'])
        self.b4_wcdma.setChecked(state_dict['b4_wcdma'])
        self.gsm850.setChecked(state_dict['gsm850'])
        self.gsm900.setChecked(state_dict['gsm900'])
        self.gsm1800.setChecked(state_dict['gsm1800'])
        self.gsm1900.setChecked(state_dict['gsm1900'])
        self.ulca_5b.setChecked(state_dict['ulca_5b'])
        self.ulca_1c.setChecked(state_dict['ulca_1c'])
        self.ulca_3c.setChecked(state_dict['ulca_3c'])
        self.ulca_7c.setChecked(state_dict['ulca_7c'])
        self.ulca_66b.setChecked(state_dict['ulca_66b'])
        self.ulca_66c.setChecked(state_dict['ulca_66c'])
        self.ulca_40c.setChecked(state_dict['ulca_40c'])
        self.ulca_38c.setChecked(state_dict['ulca_38c'])
        self.ulca_41c.setChecked(state_dict['ulca_41c'])
        self.ulca_42c.setChecked(state_dict['ulca_42c'])
        self.ulca_48c.setChecked(state_dict['ulca_48c'])
        self.bw1p4_lte.setChecked(state_dict['bw1p4_lte'])
        self.bw3_lte.setChecked(state_dict['bw3_lte'])
        self.bw5_lte.setChecked(state_dict['bw5_lte'])
        self.bw10_lte.setChecked(state_dict['bw10_lte'])
        self.bw15_lte.setChecked(state_dict['bw15_lte'])
        self.bw20_lte.setChecked(state_dict['bw20_lte'])
        self.bw5_nr.setChecked(state_dict['bw5_nr'])
        self.bw10_nr.setChecked(state_dict['bw10_nr'])
        self.bw15_nr.setChecked(state_dict['bw15_nr'])
        self.bw20_nr.setChecked(state_dict['bw20_nr'])
        self.bw25_nr.setChecked(state_dict['bw25_nr'])
        self.bw30_nr.setChecked(state_dict['bw30_nr'])
        self.bw40_nr.setChecked(state_dict['bw40_nr'])
        self.bw50_nr.setChecked(state_dict['bw50_nr'])
        self.bw60_nr.setChecked(state_dict['bw60_nr'])
        self.bw80_nr.setChecked(state_dict['bw80_nr'])
        self.bw90_nr.setChecked(state_dict['bw90_nr'])
        self.bw100_nr.setChecked(state_dict['bw100_nr'])
        self.bw70_nr.setChecked(state_dict['bw70_nr'])
        self.bw35_nr.setChecked(state_dict['bw35_nr'])
        self.bw45_nr.setChecked(state_dict['bw45_nr'])
        self.bw20_5.setChecked(state_dict['bw20_5'])
        self.bw5_20.setChecked(state_dict['bw5_20'])
        self.bw20_10.setChecked(state_dict['bw20_10'])
        self.bw10_20.setChecked(state_dict['bw10_20'])
        self.bw20_15.setChecked(state_dict['bw20_15'])
        self.bw15_20.setChecked(state_dict['bw15_20'])
        self.bw20_20.setChecked(state_dict['bw20_20'])
        self.bw15_15.setChecked(state_dict['bw15_15'])
        self.bw15_10.setChecked(state_dict['bw15_10'])
        self.bw10_15.setChecked(state_dict['bw10_15'])
        self.bw5_10.setChecked(state_dict['bw5_10'])
        self.bw10_5.setChecked(state_dict['bw10_5'])
        self.bw10_10.setChecked(state_dict['bw10_10'])
        self.bw5_15.setChecked(state_dict['bw5_15'])
        self.bw15_5.setChecked(state_dict['bw15_5'])
        self.bw40.setChecked(state_dict['bw40'])
        self.qpsk_lte.setChecked(state_dict['qpsk_lte'])
        self.q16_lte.setChecked(state_dict['q16_lte'])
        self.q64_lte.setChecked(state_dict['q64_lte'])
        self.q256_lte.setChecked(state_dict['q256_lte'])
        self.qpsk_nr.setChecked(state_dict['qpsk_nr'])
        self.q16_nr.setChecked(state_dict['q16_nr'])
        self.q64_nr.setChecked(state_dict['q64_nr'])
        self.q256_nr.setChecked(state_dict['q256_nr'])
        self.bpsk_nr.setChecked(state_dict['bpsk_nr'])
        self.dfts_nr.setChecked(state_dict['dfts_nr'])
        self.cp_nr.setChecked(state_dict['cp_nr'])
        self.prb0_lte.setChecked(state_dict['prb0_lte'])
        self.prbmax_lte.setChecked(state_dict['prbmax_lte'])
        self.frb_lte.setChecked(state_dict['frb_lte'])
        self.one_rb_0_lte.setChecked(state_dict['one_rb_0_lte'])
        self.one_rb_max_lte.setChecked(state_dict['one_rb_max_lte'])
        self.one_rb0_null.setChecked(state_dict['one_rb0_null'])
        self.prb0_null.setChecked(state_dict['prb0_null'])
        self.frb_null.setChecked(state_dict['frb_null'])
        self.frb_frb.setChecked(state_dict['frb_frb'])
        self.one_rb0_one_rbmax.setChecked(state_dict['one_rb0_one_rbmax'])
        self.one_rbmax_one_rb0.setChecked(state_dict['one_rbmax_one_rb0'])
        self.criteria_ulca_lte_3gpp_radioButton.setChecked(state_dict['criteria_ulca_lte_3gpp'])
        self.criteria_ulca_lte_fcc_radioButton.setChecked(state_dict['criteria_ulca_lte_fcc'])
        self.inner_full_nr.setChecked(state_dict['inner_full_nr'])
        self.outer_full_nr.setChecked(state_dict['outer_full_nr'])
        self.inner_1rb_left_nr.setChecked(state_dict['inner_1rb_left_nr'])
        self.inner_1rb_right_nr.setChecked(state_dict['inner_1rb_right_nr'])
        self.edge_1rb_left_nr.setChecked(state_dict['edge_1rb_left_nr'])
        self.edge_1rb_right_nr.setChecked(state_dict['edge_1rb_right_nr'])
        self.edge_full_left_nr.setChecked(state_dict['edge_full_left_nr'])
        self.edge_full_right_nr.setChecked(state_dict['edge_full_right_nr'])
        self.tmpchmb_en.setChecked(state_dict['tmpchmb_en'])
        self.hthv_en.setChecked(state_dict['hthv_en'])
        self.htlv_en.setChecked(state_dict['htlv_en'])
        self.ntnv_en.setChecked(state_dict['ntnv_en'])
        self.lthv_en.setChecked(state_dict['lthv_en'])
        self.ltlv_en.setChecked(state_dict['ltlv_en'])
        self.wait_time_comboBox.setCurrentText(str(state_dict['wait_time']))
        self.psu_en.setChecked(state_dict['psu_en'])
        self.hv_en.setChecked(state_dict['hv_en'])
        self.nv_en.setChecked(state_dict['nv_en'])
        self.lv_en.setChecked(state_dict['lv_en'])
        self.odpm2_en.setChecked(state_dict['odpm2_en'])
        self.ht_spinBox.setValue(state_dict['ht_value'])
        self.nt_spinBox.setValue(state_dict['nt_value'])
        self.lt_spinBox.setValue(state_dict['lt_value'])
        self.hv_doubleSpinBox.setValue(state_dict['hv_value'])
        self.nv_doubleSpinBox.setValue(state_dict['nv_value'])
        self.lv_doubleSpinBox.setValue(state_dict['lv_value'])
        self.input_level_sig_anritsu_spinBox.setValue(state_dict['input_level_sig_anritsu'])
        self.rfout_port_sig_anritsu_comboBox.setValue(state_dict['rfout_port_sig_anritsu'])

    def tx_port_show(self):
        print(f'Tx Port: {self.tx_port_comboBox.currentText()}')

    def tx_port_endc_lte_show(self):
        print(f'Endc LTE Tx Port: {self.tx_port_endc_lte_comboBox.currentText()}')

    @staticmethod
    def tx_port_endc_lte_state(checked):
        if checked:
            print(f'Endc LTE port Enabled')
        else:
            print(f'Endc LTE port Disabled')

    def showout_en(self):
        match self.equipments_comboBox.currentText():
            case 'Cmw100':
                self.nr_tech.setHidden(False)
                self.wcdma_tech.setHidden(False)
                self.gsm_tech.setHidden(False)
                self.ulca_lte_tech.setHidden(False)
                self.hsupa_tech.setHidden(True)
                self.hsdpa_tech.setHidden(True)
                self.hsupa_tech.setChecked(False)
                self.hsdpa_tech.setChecked(False)
            case 'Cmw100+Fsw':
                self.nr_tech.setHidden(False)
                self.wcdma_tech.setHidden(False)
                self.gsm_tech.setHidden(False)
                self.ulca_lte_tech.setHidden(False)
                self.hsupa_tech.setHidden(True)
                self.hsdpa_tech.setHidden(True)
                self.hsupa_tech.setChecked(False)
                self.hsdpa_tech.setChecked(False)
            case 'Anritsu8820':
                self.nr_tech.setHidden(False)
                self.wcdma_tech.setHidden(False)
                self.gsm_tech.setHidden(False)
                self.ulca_lte_tech.setHidden(False)
                self.hsupa_tech.setHidden(False)
                self.hsdpa_tech.setHidden(False)
            case 'Anritsu8821':
                self.nr_tech.setHidden(True)
                self.wcdma_tech.setHidden(True)
                self.gsm_tech.setHidden(True)
                self.ulca_lte_tech.setHidden(True)
                self.hsupa_tech.setHidden(True)
                self.hsdpa_tech.setHidden(True)
                self.nr_tech.setChecked(False)
                self.wcdma_tech.setChecked(False)
                self.gsm_tech.setChecked(False)
                self.ulca_lte_tech.setChecked(False)
                self.hsupa_tech.setChecked(False)
                self.hsdpa_tech.setChecked(False)

    def equipment_show(self):
        print(f'Equipment: {self.equipments_comboBox.currentText()}')

    def nr_bands_selected(self):
        nr_bands_list = []
        if self.n5_nr.isChecked():
            nr_bands_list.append(5)
        if self.n8_nr.isChecked():
            nr_bands_list.append(8)
        if self.n12_nr.isChecked():
            nr_bands_list.append(12)
        if self.n13_nr.isChecked():
            nr_bands_list.append(13)
        if self.n14_nr.isChecked():
            nr_bands_list.append(14)
        if self.n20_nr.isChecked():
            nr_bands_list.append(20)
        if self.n24_nr.isChecked():
            nr_bands_list.append(24)
        if self.n26_nr.isChecked():
            nr_bands_list.append(26)
        if self.n71_nr.isChecked():
            nr_bands_list.append(71)
        if self.n28_a_nr.isChecked():
            nr_bands_list.append('28_a')
        if self.n28_b_nr.isChecked():
            nr_bands_list.append('28_b')
        if self.n29_nr.isChecked():
            nr_bands_list.append(29)
        if self.n32_nr.isChecked():
            nr_bands_list.append(32)
        if self.n1_nr.isChecked():
            nr_bands_list.append(1)
        if self.n2_nr.isChecked():
            nr_bands_list.append(2)
        if self.n3_nr.isChecked():
            nr_bands_list.append(3)
        if self.n4_nr.isChecked():
            nr_bands_list.append(4)
        if self.n7_nr.isChecked():
            nr_bands_list.append(7)
        if self.n30_nr.isChecked():
            nr_bands_list.append(30)
        if self.n25_nr.isChecked():
            nr_bands_list.append(25)
        if self.n66_nr.isChecked():
            nr_bands_list.append(66)
        if self.n70_nr.isChecked():
            nr_bands_list.append(70)
        if self.n39_nr.isChecked():
            nr_bands_list.append(39)
        if self.n40_nr.isChecked():
            nr_bands_list.append(40)
        if self.n38_nr.isChecked():
            nr_bands_list.append(38)
        if self.n41_nr.isChecked():
            nr_bands_list.append(41)
        if self.n34_nr.isChecked():
            nr_bands_list.append(34)
        if self.n75_nr.isChecked():
            nr_bands_list.append(75)
        if self.n76_nr.isChecked():
            nr_bands_list.append(76)
        if self.n255_nr.isChecked():
            nr_bands_list.append(255)
        if self.n256_nr.isChecked():
            nr_bands_list.append(256)
        if self.n48_nr.isChecked():
            nr_bands_list.append(48)
        if self.n77_nr.isChecked():
            nr_bands_list.append(77)
        if self.n78_nr.isChecked():
            nr_bands_list.append(78)
        if self.n79_nr.isChecked():
            nr_bands_list.append(79)

        # print(f'NR bands: {nr_bands_list}')
        return nr_bands_list

    def lte_bands_selected(self):
        lte_bands_list = []
        if self.b5_lte.isChecked():
            lte_bands_list.append(5)
        if self.b8_lte.isChecked():
            lte_bands_list.append(8)
        if self.b12_lte.isChecked():
            lte_bands_list.append(12)
        if self.b13_lte.isChecked():
            lte_bands_list.append(13)
        if self.b14_lte.isChecked():
            lte_bands_list.append(14)
        if self.b17_lte.isChecked():
            lte_bands_list.append(17)
        if self.b18_lte.isChecked():
            lte_bands_list.append(18)
        if self.b19_lte.isChecked():
            lte_bands_list.append(19)
        if self.b20_lte.isChecked():
            lte_bands_list.append(20)
        if self.b26_lte.isChecked():
            lte_bands_list.append(26)
        if self.b28_a_lte.isChecked():
            lte_bands_list.append('28_a')
        if self.b28_b_lte.isChecked():
            lte_bands_list.append('28_b')
        if self.b29_lte.isChecked():
            lte_bands_list.append(29)
        if self.b32_lte.isChecked():
            lte_bands_list.append(32)
        if self.b71_lte.isChecked():
            lte_bands_list.append(71)
        if self.b24_lte.isChecked():
            lte_bands_list.append(24)
        if self.b1_lte.isChecked():
            lte_bands_list.append(1)
        if self.b2_lte.isChecked():
            lte_bands_list.append(2)
        if self.b3_lte.isChecked():
            lte_bands_list.append(3)
        if self.b4_lte.isChecked():
            lte_bands_list.append(4)
        if self.b7_lte.isChecked():
            lte_bands_list.append(7)
        if self.b30_lte.isChecked():
            lte_bands_list.append(30)
        if self.b25_lte.isChecked():
            lte_bands_list.append(25)
        if self.b66_lte.isChecked():
            lte_bands_list.append(66)
        if self.b21_lte.isChecked():
            lte_bands_list.append(21)
        if self.b39_lte.isChecked():
            lte_bands_list.append(39)
        if self.b40_lte.isChecked():
            lte_bands_list.append(40)
        if self.b38_lte.isChecked():
            lte_bands_list.append(38)
        if self.b41_lte.isChecked():
            lte_bands_list.append(41)
        if self.b23_lte.isChecked():
            lte_bands_list.append(23)
        if self.b42_lte.isChecked():
            lte_bands_list.append(42)
        if self.b48_lte.isChecked():
            lte_bands_list.append(48)

        # print(f'LTE bands: {lte_bands_list}')
        return lte_bands_list

    def wcdma_bands_selected(self):
        wcdma_bands_list = []
        if self.b5_wcdma.isChecked():
            wcdma_bands_list.append(5)
        if self.b8_wcdma.isChecked():
            wcdma_bands_list.append(8)
        if self.b6_wcdma.isChecked():
            wcdma_bands_list.append(6)
        if self.b19_wcdma.isChecked():
            wcdma_bands_list.append(19)
        if self.b1_wcdma.isChecked():
            wcdma_bands_list.append(1)
        if self.b2_wcdma.isChecked():
            wcdma_bands_list.append(2)
        if self.b4_wcdma.isChecked():
            wcdma_bands_list.append(4)

        # print(f'WCDMA bands: {wcdma_bands_list}')
        return wcdma_bands_list

    def gsm_bands_selected(self):
        gsm_bands_list = []
        if self.gsm850.isChecked():
            gsm_bands_list.append(850)
        if self.gsm900.isChecked():
            gsm_bands_list.append(900)
        if self.gsm1800.isChecked():
            gsm_bands_list.append(1800)
        if self.gsm1900.isChecked():
            gsm_bands_list.append(1900)

        # print(f'GSM bands: {gsm_bands_list}')
        return gsm_bands_list

    def ulca_lte_bands_selected(self):
        ulca_lte_bands_list = []
        if self.ulca_5b.isChecked():
            ulca_lte_bands_list.append('5b')
        if self.ulca_1c.isChecked():
            ulca_lte_bands_list.append('1c')
        if self.ulca_3c.isChecked():
            ulca_lte_bands_list.append('3c')
        if self.ulca_7c.isChecked():
            ulca_lte_bands_list.append('7c')
        if self.ulca_66b.isChecked():
            ulca_lte_bands_list.append('66b')
        if self.ulca_66c.isChecked():
            ulca_lte_bands_list.append('66c')
        if self.ulca_40c.isChecked():
            ulca_lte_bands_list.append('40c')
        if self.ulca_38c.isChecked():
            ulca_lte_bands_list.append('38c')
        if self.ulca_41c.isChecked():
            ulca_lte_bands_list.append('41c')
        if self.ulca_42c.isChecked():
            ulca_lte_bands_list.append('42c')
        if self.ulca_48c.isChecked():
            ulca_lte_bands_list.append('48c')

        # print(f'ULCA LTE bands: {ulca_lte_bands_list}')
        return ulca_lte_bands_list

    def nr_bw_selected(self):
        bw_nr_list = []
        if self.bw5_nr.isChecked():
            bw_nr_list.append(5)
        if self.bw10_nr.isChecked():
            bw_nr_list.append(10)
        if self.bw15_nr.isChecked():
            bw_nr_list.append(15)
        if self.bw20_nr.isChecked():
            bw_nr_list.append(20)
        if self.bw25_nr.isChecked():
            bw_nr_list.append(25)
        if self.bw30_nr.isChecked():
            bw_nr_list.append(30)
        if self.bw40_nr.isChecked():
            bw_nr_list.append(40)
        if self.bw50_nr.isChecked():
            bw_nr_list.append(50)
        if self.bw60_nr.isChecked():
            bw_nr_list.append(60)
        if self.bw80_nr.isChecked():
            bw_nr_list.append(80)
        if self.bw90_nr.isChecked():
            bw_nr_list.append(90)
        if self.bw100_nr.isChecked():
            bw_nr_list.append(100)
        if self.bw70_nr.isChecked():
            bw_nr_list.append(70)
        if self.bw35_nr.isChecked():
            bw_nr_list.append(35)
        if self.bw45_nr.isChecked():
            bw_nr_list.append(45)

        return bw_nr_list

    def lte_bw_selected(self):
        bw_lte_list = []
        if self.bw1p4_lte.isChecked():
            bw_lte_list.append(1.4)
        if self.bw3_lte.isChecked():
            bw_lte_list.append(3)
        if self.bw5_lte.isChecked():
            bw_lte_list.append(5)
        if self.bw10_lte.isChecked():
            bw_lte_list.append(10)
        if self.bw15_lte.isChecked():
            bw_lte_list.append(15)
        if self.bw20_lte.isChecked():
            bw_lte_list.append(20)

        return bw_lte_list

    def ulca_lte_bw_selected(self):
        bw_ulca_lte_list = []
        if self.bw20_5.isChecked():
            bw_ulca_lte_list.append('20+5')
        if self.bw5_20.isChecked():
            bw_ulca_lte_list.append('5+20')
        if self.bw20_10.isChecked():
            bw_ulca_lte_list.append('20+10')
        if self.bw10_20.isChecked():
            bw_ulca_lte_list.append('10+20')
        if self.bw20_15.isChecked():
            bw_ulca_lte_list.append('20+15')
        if self.bw15_20.isChecked():
            bw_ulca_lte_list.append('15+20')
        if self.bw20_20.isChecked():
            bw_ulca_lte_list.append('20+20')
        if self.bw15_15.isChecked():
            bw_ulca_lte_list.append('15+15')
        if self.bw15_10.isChecked():
            bw_ulca_lte_list.append('15+10')
        if self.bw10_15.isChecked():
            bw_ulca_lte_list.append('10+5')
        if self.bw5_10.isChecked():
            bw_ulca_lte_list.append('5+10')
        if self.bw10_5.isChecked():
            bw_ulca_lte_list.append('10+5')
        if self.bw10_10.isChecked():
            bw_ulca_lte_list.append('10+10')
        if self.bw5_15.isChecked():
            bw_ulca_lte_list.append('5+15')
        if self.bw15_5.isChecked():
            bw_ulca_lte_list.append('15+5')
        if self.bw40.isChecked():
            bw_ulca_lte_list.append('40')

        return bw_ulca_lte_list

    def nr_mcs_selected(self):
        mcs_nr_list = []
        if self.qpsk_nr.isChecked():
            mcs_nr_list.append('QPSK')
        if self.q16_nr.isChecked():
            mcs_nr_list.append('Q16')
        if self.q64_nr.isChecked():
            mcs_nr_list.append('Q64')
        if self.q256_nr.isChecked():
            mcs_nr_list.append('Q256')
        if self.bpsk_nr.isChecked():
            mcs_nr_list.append('BPSK')

        return mcs_nr_list

    def nr_type_selected(self):
        type_nr_list = []
        if self.dfts_nr.isChecked():
            type_nr_list.append('DFTS')
        if self.cp_nr.isChecked():
            type_nr_list.append('CP')

        return type_nr_list

    def lte_mcs_selected(self):
        mcs_lte_list = []
        if self.qpsk_lte.isChecked():
            mcs_lte_list.append('QPSK')
        if self.q16_lte.isChecked():
            mcs_lte_list.append('Q16')
        if self.q64_lte.isChecked():
            mcs_lte_list.append('Q64')
        if self.q256_lte.isChecked():
            mcs_lte_list.append('Q256')

        return mcs_lte_list

    def nr_rb_allocation_selected(self):
        allocation_nr_list = []
        if self.inner_full_nr.isChecked():
            allocation_nr_list.append('INNER_FULL')
        if self.outer_full_nr.isChecked():
            allocation_nr_list.append('OUTER_FULL')
        if self.inner_1rb_left_nr.isChecked():
            allocation_nr_list.append('INNER_1RB_LEFT')
        if self.inner_1rb_right_nr.isChecked():
            allocation_nr_list.append('INNER_1RB_RIGHT')
        if self.edge_1rb_left_nr.isChecked():
            allocation_nr_list.append('EDGE_1RB_LEFT')
        if self.edge_1rb_right_nr.isChecked():
            allocation_nr_list.append('EDGE_1RB_RIGHT')
        if self.edge_full_left_nr.isChecked():
            allocation_nr_list.append('EDGE_FULL_LEFT')
        if self.edge_full_right_nr.isChecked():
            allocation_nr_list.append('EDGE_FULL_RIGHT')

        return allocation_nr_list

    def lte_rb_allocation_selected(self):
        allocation_lte_list = []
        if self.prb0_lte.isChecked():
            allocation_lte_list.append('PRB_0')
        if self.prb0_lte.isChecked():
            allocation_lte_list.append('PRB_MAX')
        if self.prb0_lte.isChecked():
            allocation_lte_list.append('FRB')
        if self.prb0_lte.isChecked():
            allocation_lte_list.append('1RB_0')
        if self.prb0_lte.isChecked():
            allocation_lte_list.append('1RB_MAX')

        return allocation_lte_list

    def ulca_lte_rb_allocation_selected(self):
        allocation_ulca_lte_list = []
        if self.one_rb0_null.isChecked():
            allocation_ulca_lte_list.append('1PRB_N')
        if self.prb0_null.isChecked():
            allocation_ulca_lte_list.append('PRB_N')
        if self.frb_null.isChecked():
            allocation_ulca_lte_list.append('FRB_N')
        if self.frb_frb.isChecked():
            allocation_ulca_lte_list.append('FRB_FRB')
        if self.one_rb0_one_rbmax.isChecked():
            allocation_ulca_lte_list.append('1RB0_1RBmax')
        if self.one_rbmax_one_rb0.isChecked():
            allocation_ulca_lte_list.append('1RBmax_1RB0')

        return allocation_ulca_lte_list

    def ulca_lte_critera_selected(self):
        if self.criteria_ulca_lte_fcc_radioButton.isChecked():
            return 'FCC'
        elif self.criteria_ulca_lte_3gpp_radioButton.isChecked():
            return '3GPP'

    def measure(self):
        self.run_button.setEnabled(False)
        # self.progressBar.setMaximum(78)
        # for i in range(78):
        #     print(i)
        #     self.progressBar.setValue(i+1)
        #     time.sleep(1)
        self.measure_base()
        self.run_button.setEnabled(True)

    def measure_base(self, state_dict=None):
        print('measure...')
        # match state_dict['equipment']:
        #     case 'Cmw100':
        #         # import somthing
        #         if state_dict['tx_lmh_ns']:
        #             ...
        #         if state_dict['tx_level_sweep_ns']:
        #             ...
        #         if state_dict['tx_freq_sweep_ns']:
        #             ...
        #         if state_dict['tx_1rb_sweep_ns']:
        #             ...
        #         if state_dict['tx_fcc_power_ns']:
        #             ...
        #         if state_dict['tx_ce_power_ns']:
        #             ...
        #
        #         if state_dict['tx_ulca_lte_ns']:
        #             ...
        #         if state_dict['rx_normal_ns']:
        #             ...
        #         if state_dict['rx_quick_ns']:
        #             ...
        #         if state_dict['rx_endc_desense_ns']:
        #             ...
        #
        #     case 'Cmw100+Fsw':
        #         # import somthing
        #         if state_dict['tx_harmonics_ns']:
        #             ...
        #         if state_dict['tx_cbe_ns']:
        #             ...
        #         if state_dict['tx_ulca_lte_cbe_ns']:
        #             ...
        #
        #     case 'Anritsu8820':
        #         # import somthing
        #         if state_dict['tx_lmh_s']:
        #             ...
        #         if state_dict['rx_normal_s']:
        #             ...
        #         if state_dict['rxs_sweep_s']:
        #             ...
        #     case 'Anritsu8821':
        #         # import somthing
        #         if state_dict['tx_lmh_s']:
        #             ...
        #         if state_dict['rx_normal_s']:
        #             ...
        #         if state_dict['rxs_sweep_s']:
        #             ...

    def run_start(self):
        print('run')
        t = threading.Thread(target=self.measure, daemon=True)
        t.start()

    def therm_charge_dis(self):
        print('therm dis')

    def stop(self):
        print('stop')


def main():
    app = QApplication(sys.argv)
    style = QStyleFactory.create('Fusion')
    app.setStyle(style)
    win = MainWindow()
    # win.setMaximumSize(QSize(1491, 776))
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
