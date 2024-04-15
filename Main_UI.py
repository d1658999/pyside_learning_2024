import datetime
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QStyleFactory, QFileDialog
from PySide6.QtCore import QThread, Slot, QSize
import sys
import time
import threading
import pathlib
import signal
import os
import yaml
from ui_mega_v2_9 import Ui_MainWindow
from utils.log_init import log_set, log_clear
from utils.adb_handler import get_serial_devices
from utils.excel_handler import excel_folder_create
from equipments.power_supply import Psu
from equipments.temp_chamber import TempChamber
from utils.regy_handler import regy_replace, regy_extract, regy_extract_2
from utils.log_init import log_set, log_clear


logger = log_set('GUI')


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.volt = None
        self.condition = None
        self.psu = None
        self.tmpcmb = None
        log_clear()
        self.setupUi(self)
        self.init_show()
        self.init_hidden()
        self.custom_signal_slot()
        self.import_gui_setting_yaml()
        self.temp_dict = {
            'HT': self.ht_spinBox.value(),
            'NT': self.nt_spinBox.value(),
            'LT': self.lt_spinBox.value(),
        }
        self.volts_dict = {
            'HV': self.hv_doubleSpinBox.value(),
            'NV': self.nv_doubleSpinBox.value(),
            'LV': self.lv_doubleSpinBox.value(),
        }

    def custom_signal_slot(self):
        self.as_path_en.toggled.connect(self.srs_unchecked)
        self.srs_path_en.toggled.connect(self.as_unchecked)
        self.rx_normal_ns.toggled.connect(self.rx_quick_unchecked)
        self.rx_quick_ns.toggled.connect(self.rx_normal_unchecked)
        self.run_button.clicked.connect(self.run_start)
        self.therm_charge_dis_button.clicked.connect(self.therm_charge_dis)
        self.stop_button.clicked.connect(self.stop)
        self.equipments_comboBox.currentTextChanged.connect(self.equipment_show)
        self.tx_port_comboBox.currentTextChanged.connect(self.tx_port_show)
        self.tx_port_endc_lte_comboBox.currentTextChanged.connect(self.tx_port_endc_lte_show)
        self.rx_endc_desense_ns.stateChanged.connect(self.tx_port_endc_lte_state)
        self.equipments_comboBox.textActivated.connect(self.showout_en)
        self.run_button.clicked.connect(self.selected_show)
        self.rx_quick_ns.toggled.connect(self.rx_path_cumtom_disabled)

    def init_show(self):
        logger.info(f'Equipment: {self.equipments_comboBox.currentText()}')
        logger.info(f'Tx port: {self.tx_port_comboBox.currentText()}')
        logger.info(f'Techs: {self.tech_selected()}')
        logger.info(f'Channels: {self.channel_selected()}')
        logger.info(f'NR bands: {self.nr_bands_selected()}')
        logger.info(f'LTE bands: {self.lte_bands_selected()}')
        logger.info(f'WCDMA bands: {self.wcdma_bands_selected()}')
        logger.info(f'GSM bands: {self.gsm_bands_selected()}')
        logger.info(f'ULCA LTE bands: {self.ulca_lte_bands_selected()}')
        logger.info(f'NR BWs: {self.nr_bw_selected()}')
        logger.info(f'LTE BWs: {self.lte_bw_selected()}')
        logger.info(f'ULCA LTE BWs: {self.ulca_lte_bw_selected()}')
        logger.info(f'NR RB allocation: {self.nr_rb_allocation_selected()}')
        logger.info(f'NR TYPE: {self.nr_type_selected()}')
        logger.info(f'NR MCS: {self.nr_mcs_selected()}')
        logger.info(f'LTE RB allocation: {self.lte_rb_allocation_selected()}')
        logger.info(f'LTE MCS: {self.lte_mcs_selected()}')
        logger.info(f'GSM modulation: {self.gsm_modulation_switch()}')
        logger.info(f'ULCA LTE RB allocation: {self.ulca_lte_rb_allocation_selected()}')
        logger.info(f'ULCA LTE MCS: {self.lte_mcs_selected()}')
        logger.info(f'ULCA LTE criteria: {self.ulca_lte_critera_switch()}')

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
                self.nr_tech.setHidden(True)
                self.nr_tech.setChecked(False)
                self.hsupa_tech.setHidden(False)
                self.hsdpa_tech.setHidden(False)
                self.gsm_tech.setChecked(False)
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

    def rx_path_cumtom_disabled(self):
        if self.rx_quick_ns.isChecked():
            self.rx0.setDisabled(True)
            self.rx1.setDisabled(True)
            self.rx2.setDisabled(True)
            self.rx3.setDisabled(True)
            self.rx0_rx1.setDisabled(True)
            self.rx2_rx3.setDisabled(True)
            self.rx0.setChecked(False)
            self.rx1.setChecked(False)
            self.rx2.setChecked(False)
            self.rx3.setChecked(False)
            self.rx0_rx1.setChecked(False)
            self.rx2_rx3.setChecked(False)

        else:
            self.rx0.setEnabled(True)
            self.rx1.setEnabled(True)
            self.rx2.setEnabled(True)
            self.rx3.setEnabled(True)
            self.rx0_rx1.setEnabled(True)
            self.rx2_rx3.setEnabled(True)

    def selected_show(self):
        logger.info(f'Equipment: {self.equipments_comboBox.currentText()}')
        logger.info(f'Tx port: {self.tx_port_comboBox.currentText()}')
        logger.info(f'Techs: {self.tech_selected()}')
        logger.info(f'Channels: {self.channel_selected()}')
        logger.info(f'NR bands: {self.nr_bands_selected()}')
        logger.info(f'LTE bands: {self.lte_bands_selected()}')
        logger.info(f'WCDMA bands: {self.wcdma_bands_selected()}')
        logger.info(f'GSM bands: {self.gsm_bands_selected()}')
        logger.info(f'ULCA LTE bands: {self.ulca_lte_bands_selected()}')
        logger.info(f'NR BWs: {self.nr_bw_selected()}')
        logger.info(f'LTE BWs: {self.lte_bw_selected()}')
        logger.info(f'ULCA LTE BWs: {self.ulca_lte_bw_selected()}')
        logger.info(f'NR RB allocation: {self.nr_rb_allocation_selected()}')
        logger.info(f'NR TYPE: {self.nr_type_selected()}')
        logger.info(f'NR MCS: {self.nr_mcs_selected()}')
        logger.info(f'LTE RB allocation: {self.lte_rb_allocation_selected()}')
        logger.info(f'LTE MCS: {self.lte_mcs_selected()}')
        logger.info(f'GSM modulation: {self.gsm_modulation_switch()}')
        logger.info(f'ULCA LTE RB allocation: {self.ulca_lte_rb_allocation_selected()}')
        logger.info(f'ULCA LTE MCS: {self.lte_mcs_selected()}')
        logger.info(f'ULCA LTE criteria: {self.ulca_lte_critera_switch()}')

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

    def rx_normal_unchecked(self, checked):
        if checked:
            self.rx_normal_ns.setChecked(False)
    def rx_quick_unchecked(self, checked):
        if checked:
            self.rx_quick_ns.setChecked(False)

    def export_gui_setting_yaml(self):
        logger.info('Export ui setting')
        yaml_file = 'gui_init.yaml'
        content = self.gui_state_get()
        with open(yaml_file, 'w', encoding='utf-8') as outfile:
            yaml.dump(content, outfile, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    def import_gui_setting_yaml(self):
        logger.info('Import the last setting')
        with open('gui_init.yaml', 'r') as s:
            ui_init = yaml.safe_load(s)

        self.gui_state_set(ui_init)

    def gui_state_get(self, state_dict=None):
        if state_dict is None:
            state_dict = dict()
        state_dict['equipment'] = self.equipments_comboBox.currentText()
        state_dict['tx_port_table_en'] = self.port_table_en.isChecked()
        state_dict['tx_port'] = self.tx_port_comboBox.currentText()
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
        state_dict['pn_name'] = self.pn_lineEdit.text()
        state_dict['sync_path_toolBox_index'] = self.sync_path_toolBox.currentIndex()
        state_dict['sync_path'] = self.sync_path_comboBox.currentText()
        state_dict['as_path_en'] = self.as_path_en.isChecked()
        state_dict['as_path'] = self.as_path_comboBox.currentText()
        state_dict['srs_path_en'] = self.srs_path_en.isChecked()
        state_dict['srs_path'] = self.srs_path_comboBox.currentText()
        state_dict['tx_level'] = self.tx_level_spinBox.value()
        state_dict['pcl_lb_level'] = int(self.pcl_lb_level_combo.currentText())
        state_dict['pcl_mb_level'] = int(self.pcl_mb_level_combo.currentText())
        state_dict['gmsk_mod'] = self.gmsk_radioButton.isChecked()
        state_dict['epsk_mod'] = self.epsk_radioButton.isChecked()
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
        state_dict['n48_nr'] = self.n48_nr.isChecked()
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
        state_dict['gsm900'] = self.gsm900.isChecked()
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
        state_dict['b3_78'] = self.b3_n78.isChecked()
        state_dict['b2_77'] = self.b2_n77.isChecked()
        state_dict['b66_77'] = self.b66_n77.isChecked()
        state_dict['b66_n2'] = self.b66_n2.isChecked()
        state_dict['b66_n5'] = self.b66_n5.isChecked()
        state_dict['b12_n78'] = self.b12_n78.isChecked()
        state_dict['b5_n78'] = self.b5_n78.isChecked()
        state_dict['b28_78'] = self.b28_n78.isChecked()
        state_dict['b5_n77'] = self.b5_n77.isChecked()
        state_dict['b13_n5'] = self.b13_n5.isChecked()
        state_dict['bw1p4_lte'] = self.bw1p4_lte.isChecked()
        state_dict['bw3_lte'] = self.bw3_lte.isChecked()
        state_dict['bw5_lte'] = self.bw5_lte.isChecked()
        state_dict['bw10_lte'] = self.bw10_lte.isChecked()
        state_dict['bw15_lte'] = self.bw15_lte.isChecked()
        state_dict['bw20_lte'] = self.bw20_lte.isChecked()
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
        state_dict['one_rb0_null'] = self.one_rb0_null.isChecked()
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
        state_dict['current_count'] = self.count_spinBox.value()
        state_dict['ht_value'] = self.ht_spinBox.value()
        state_dict['nt_value'] = self.nt_spinBox.value()
        state_dict['lt_value'] = self.lt_spinBox.value()
        state_dict['hv_value'] = self.hv_doubleSpinBox.value()
        state_dict['nv_value'] = self.nv_doubleSpinBox.value()
        state_dict['lv_value'] = self.lv_doubleSpinBox.value()
        state_dict['outer_loop'] = self.outer_loop_spinBox.value()
        state_dict['init_rx_sync_level'] = self.init_rx_sync_level_spinBox.value()
        state_dict['et_tracker'] = self.et_tracker_comboBox.currentText()
        state_dict['rfout_port_sig_anritsu'] = self.rfout_port_sig_anritsu_comboBox.currentText()
        state_dict['input_level_sig_anritsu'] = self.input_level_sig_anritsu_spinBox.value()
        state_dict['progressBar_progress'] = 0  # special item for input and output small funciton
        state_dict['nr_mcs_list'] = self.nr_mcs_selected()
        state_dict['lte_mcs_list'] = self.lte_mcs_selected()
        state_dict['nr_rb_allocation_list'] = self.nr_rb_allocation_selected()
        state_dict['lte_rb_allocation_list'] = self.lte_rb_allocation_selected()
        state_dict['ulca_lte_rb_allocation_list'] = self.ulca_lte_rb_allocation_selected()
        state_dict['tech_list'] = self.tech_selected()
        state_dict['channel_str'] = self.channel_selected()
        state_dict['tx_path_list'] = self.tx_path_selected()
        state_dict['rx_path_list'] = self.rx_path_selected()
        state_dict['endc_lte_tx_path'] = self.endc_lte_tx_path_switch()
        state_dict['endc_nr_tx_path'] = self.endc_nr_tx_path_switch()
        state_dict['endc_lte_rx_path_list'] = self.endc_lte_rx_path_selected()
        state_dict['endc_nr_rx_path_list'] = self.endc_nr_rx_path_selected()
        state_dict['ue_power_list'] = self.ue_power_selected()
        state_dict['nr_bw_list'] = self.nr_bw_selected()
        state_dict['lte_bw_list'] = self.lte_bw_selected()
        state_dict['ulca_lte_bw_list'] = self.ulca_lte_bw_selected()
        state_dict['nr_bands_list'] = self.nr_bands_selected()
        state_dict['lte_bands_list'] = self.lte_bands_selected()
        state_dict['wcdma_bands_list'] = self.wcdma_bands_selected()
        state_dict['gsm_bands_list'] = self.gsm_bands_selected()
        state_dict['ulca_lte_band_list'] = self.ulca_lte_bands_selected()
        state_dict['endc_bands_list'] = self.endc_bands_selected()
        state_dict['nr_type_list'] = self.nr_type_selected()
        state_dict['gsm_modulation'] = self.gsm_modulation_switch()
        state_dict['ulca_lte_criteria'] = self.ulca_lte_critera_switch()
        state_dict['temp_volts_list'] = self.temp_volts_selected()
        state_dict['volts_list'] = self.volts_selected()
        state_dict['devices_serial'] = get_serial_devices()
        state_dict['condition'] = self.condition
        state_dict['volt_type'] = self.volt

        return state_dict

    def gui_state_set(self, state_dict):
        self.equipments_comboBox.setCurrentText(state_dict['equipment'])
        self.port_table_en.setChecked(state_dict['tx_port_table_en'])
        self.tx_port_comboBox.setCurrentText(state_dict['tx_port'])
        self.tx_port_endc_lte_comboBox.setCurrentText(state_dict['tx_port_endc_lte'])
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
        self.cbe_margin.setText(str(state_dict['cbe_margin']))
        self.sync_path_toolBox.setCurrentIndex(state_dict['sync_path_toolBox_index'])
        self.sync_path_comboBox.setCurrentText(state_dict['sync_path'])
        self.as_path_en.setChecked(state_dict['as_path_en'])
        self.as_path_comboBox.setCurrentText(state_dict['as_path'])
        self.srs_path_en.setChecked(state_dict['srs_path_en'])
        self.srs_path_comboBox.setCurrentText(state_dict['srs_path'])
        self.tx_level_spinBox.setValue(state_dict['tx_level'])
        self.pcl_lb_level_combo.setCurrentText(str(state_dict['pcl_lb_level']))
        self.pcl_mb_level_combo.setCurrentText(str(state_dict['pcl_mb_level']))
        self.gmsk_radioButton.setChecked(state_dict['gmsk_mod'])
        self.epsk_radioButton.setChecked(state_dict['epsk_mod'])
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
        self.n48_nr.setChecked(state_dict['n48_nr'])
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
        self.b3_n78.setChecked(state_dict['b3_78'])
        self.b2_n77.setChecked(state_dict['b2_77'])
        self.b66_n77.setChecked(state_dict['b66_77'])
        self.b66_n2.setChecked(state_dict['b66_n2'])
        self.b66_n5.setChecked(state_dict['b66_n5'])
        self.b12_n78.setChecked(state_dict['b12_n78'])
        self.b5_n78.setChecked(state_dict['b5_n78'])
        self.b28_n78.setChecked(state_dict['b28_78'])
        self.b5_n77.setChecked(state_dict['b5_n77'])
        self.b13_n5.setChecked(state_dict['b13_n5'])
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
        self.count_spinBox.setValue(state_dict['current_count'])
        self.ht_spinBox.setValue(state_dict['ht_value'])
        self.nt_spinBox.setValue(state_dict['nt_value'])
        self.lt_spinBox.setValue(state_dict['lt_value'])
        self.hv_doubleSpinBox.setValue(state_dict['hv_value'])
        self.nv_doubleSpinBox.setValue(state_dict['nv_value'])
        self.lv_doubleSpinBox.setValue(state_dict['lv_value'])
        self.outer_loop_spinBox.setValue(state_dict['outer_loop'])
        self.init_rx_sync_level_spinBox.setValue(state_dict['init_rx_sync_level'])
        self.et_tracker_comboBox.setCurrentText(state_dict['et_tracker'])
        self.input_level_sig_anritsu_spinBox.setValue(state_dict['input_level_sig_anritsu'])
        self.rfout_port_sig_anritsu_comboBox.setCurrentText(state_dict['rfout_port_sig_anritsu'])

    def tx_port_show(self):
        logger.info(f'Tx Port: {self.tx_port_comboBox.currentText()}')

    def tx_port_endc_lte_show(self):
        logger.info(f'Endc LTE Tx Port: {self.tx_port_endc_lte_comboBox.currentText()}')

    @staticmethod
    def tx_port_endc_lte_state(checked):
        if checked:
            logger.info(f'Endc LTE port Enabled')
        else:
            logger.info(f'Endc LTE port Disabled')

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
                self.nr_tech.setHidden(True)
                self.wcdma_tech.setHidden(False)
                self.gsm_tech.setHidden(True)
                self.ulca_lte_tech.setHidden(False)
                self.hsupa_tech.setHidden(False)
                self.hsdpa_tech.setHidden(False)
                self.nr_tech.setChecked(False)
                self.gsm_tech.setChecked(False)
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
        logger.info(f'Equipment: {self.equipments_comboBox.currentText()}')

    def temp_volts_selected(self):
        temp_volts_list = []
        if self.hthv_en.isChecked():
            temp_volts_list .append('HTHV')
        if self.htlv_en.isChecked():
            temp_volts_list .append('HTLV')
        if self.ntnv_en.isChecked():
            temp_volts_list .append('NTNV')
        if self.lthv_en.isChecked():
            temp_volts_list .append('LTHV')
        if self.ltlv_en.isChecked():
            temp_volts_list .append('LTLV')

        return temp_volts_list

    def volts_selected(self):
        volts_list = []
        if self.hv_en.isChecked():
            volts_list.append('HV')
        if self.nv_en.isChecked():
            volts_list.append('NV')
        if self.lv_en.isChecked():
            volts_list.append('LV')

        return volts_list

    def tx_path_selected(self):
        tx_path_list = []
        if self.tx1.isChecked():
            tx_path_list.append('TX1')
        if self.tx2.isChecked():
            tx_path_list.append('TX2')

        return tx_path_list

    def rx_path_selected(self):
        """
        0: default(free run) | 1: DRX_ONLY | 2: PRX ONLY | 3: PRX+DRX | 4: 4RX_PRX(RX2) ONLY | 8: 4RX_DRX(RX3) ONLY | 12: 4RX_PRX(RX2) + 4RX_DRX(RX3) | 15: ALL PATH
        """
        rx_path_list = []
        if self.rx0.isChecked():
            rx_path_list.append(2)
        if self.rx1.isChecked():
            rx_path_list.append(1)
        if self.rx2.isChecked():
            rx_path_list.append(4)
        if self.rx3.isChecked():
            rx_path_list.append(8)
        if self.rx0_rx1.isChecked():
            rx_path_list.append(3)
        if self.rx2_rx3.isChecked():
            rx_path_list.append(12)
        if self.rx_all_path.isChecked():
            rx_path_list.append(15)

        return rx_path_list

    def endc_lte_tx_path_switch(self):
        if self.endc_tx1_path_lte_radioButton.isChecked():
            return 'TX1'
        elif self.endc_tx2_path_lte_radioButton.isChecked():
            return 'TX2'

    def endc_nr_tx_path_switch(self):
        if self.endc_tx1_path_nr_radioButton.isChecked():
            return 'TX1'
        elif self.endc_tx2_path_nr_radioButton.isChecked():
            return 'TX2'

    def endc_lte_rx_path_selected(self):
        endc_lte_rx_path_list = []
        if self.rx_all_path_endc_nr.isChecked():
            endc_lte_rx_path_list.append(15)

        return endc_lte_rx_path_list

    def endc_nr_rx_path_selected(self):
        endc_nr_rx_path_list = []
        if self.rx_all_path_endc_nr.isChecked():
            endc_nr_rx_path_list.append(15)

        return endc_nr_rx_path_list

    def ue_power_selected(self):
        ue_power_list = []
        if self.ue_txmax.isChecked():
            ue_power_list.append(1)
        if self.ue_txlow.isChecked():
            ue_power_list.append(0)

        return ue_power_list

    def tech_selected(self):
        tech_list = []
        if self.nr_tech.isChecked():
            tech_list.append('NR')
        if self.lte_tech.isChecked():
            tech_list.append('LTE')
        if self.wcdma_tech.isChecked():
            tech_list.append('WCDMA')
        if self.gsm_tech.isChecked():
            tech_list.append('GSM')
        if self.ulca_lte_tech.isChecked():
            tech_list.append('ULCA_LTE')
        if self.hsupa_tech.isChecked():
            tech_list.append('HSUPA')
        if self.hsdpa_tech.isChecked():
            tech_list.append('HSDPA')

        return tech_list

    def channel_selected(self):
        channels_str = ''
        if self.lch.isChecked():
            channels_str += 'L'
        if self.mch.isChecked():
            channels_str += 'M'
        if self.hch.isChecked():
            channels_str += 'H'

        return channels_str

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

        # logger.info(f'NR bands: {nr_bands_list}')
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

        # logger.info(f'LTE bands: {lte_bands_list}')
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

        # logger.info(f'WCDMA bands: {wcdma_bands_list}')
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

        # logger.info(f'GSM bands: {gsm_bands_list}')
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

        # logger.info(f'ULCA LTE bands: {ulca_lte_bands_list}')
        return ulca_lte_bands_list

    def endc_bands_selected(self):
        endc_bands_list = []
        if self.b3_n78.isChecked():
            endc_bands_list.append('3_78')
        if self.b2_n77.isChecked():
            endc_bands_list.append('2_77')
        if self.b66_n77.isChecked():
            endc_bands_list.append('66_77')
        if self.b66_n2.isChecked():
            endc_bands_list.append('66_2')
        if self.b66_n5.isChecked():
            endc_bands_list.append('66_5')
        if self.b12_n78.isChecked():
            endc_bands_list.append('12_78')
        if self.b5_n78.isChecked():
            endc_bands_list.append('5_78')
        if self.b28_n78.isChecked():
            endc_bands_list.append('28_78')
        if self.b5_n77.isChecked():
            endc_bands_list.append('5_77')
        if self.b13_n5.isChecked():
            endc_bands_list.append('13_5')

        return endc_bands_list

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

    def gsm_modulation_switch(self):
        if self.gmsk_radioButton.isChecked():
            return 'GMSK'
        elif self.epsk_radioButton.isChecked():
            return 'EPSK'

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
        if self.prbmax_lte.isChecked():
            allocation_lte_list.append('PRB_MAX')
        if self.frb_lte.isChecked():
            allocation_lte_list.append('FRB')
        if self.one_rb_0_lte.isChecked():
            allocation_lte_list.append('1RB_0')
        if self.one_rb_max_lte.isChecked():
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

    def ulca_lte_critera_switch(self):
        if self.criteria_ulca_lte_fcc_radioButton.isChecked():
            return 'FCC'
        elif self.criteria_ulca_lte_3gpp_radioButton.isChecked():
            return '3GPP'

    @staticmethod
    def items_counts(state_dict):
        tx_test_items_ns_count_nr = 0
        tx_test_items_ns_count_lte = 0
        tx_test_items_ns_count_wcdma = 0
        tx_test_items_ns_count_gsm = 0
        tx_test_items_ns_count_ulca_lte = 0
        tx_test_items_ns_count_nr_freq_sweep = 0
        tx_test_items_ns_count_lte_freq_sweep  = 0
        tx_test_items_ns_count_wcdma_freq_sweep  = 0
        tx_test_items_ns_count_gsm_freq_sweep  = 0
        tx_test_items_ns_count_nr_1rb_sweep = 0
        tx_test_items_ns_count_nr_fcc = 0
        tx_test_items_ns_count_nr_ce = 0
        rx_test_items_ns_count_nr = 0
        rx_test_items_ns_count_lte = 0
        rx_test_items_ns_count_wcdma = 0
        rx_test_items_ns_count_gsm = 0
        rx_test_items_endc_ns_count = 0  # only for Rx_ENDC_Desense
        tx_test_items_s_count = 0
        rx_test_items_s_count = 0
        tx_path_count = 0
        rx_path_count = 0
        ue_power_count = 0
        nr_tech_count = 0
        lte_tech_count = 0
        wcdma_tech_count = 0
        gsm_tech_count = 0
        ulca_lte_tech_count = 0
        hsupa_tech_count = 0
        hsdpa_tech_count = 0
        channel_count = 0
        band_nr_count = 0
        band_lte_count = 0
        band_wcdma_count = 0
        band_gsm_count = 0
        band_ulca_lte_count = 0
        band_endc_desense_count = 0
        bw_nr_count = 0
        bw_lte_count = 0
        bw_ulca_lte_count = 0
        mcs_nr_count = 0
        mcs_lte_count = 0
        type_nr_count = 0
        rb_nr_count = 0
        rb_lte_count = 0
        rb_ulca_lte_count = 0
        temp_volt_count = 0
        volt_count = 0

        for key, value in state_dict.items():
            if key == 'tx_lmh_ns' and value is True:
                tx_test_items_ns_count_nr += 1
                tx_test_items_ns_count_lte += 1
                tx_test_items_ns_count_wcdma += 1
                tx_test_items_ns_count_gsm += 1
            if key == 'tx_level_sweep_ns' and value:
                tx_test_items_ns_count_nr += 1
                tx_test_items_ns_count_lte += 1
                tx_test_items_ns_count_wcdma += 1
                tx_test_items_ns_count_gsm += 1
            if key == 'tx_freq_sweep_ns' and value:
                tx_test_items_ns_count_nr_freq_sweep += 1
                tx_test_items_ns_count_lte_freq_sweep += 1
                tx_test_items_ns_count_wcdma_freq_sweep += 1
                tx_test_items_ns_count_gsm_freq_sweep += 1
            if key == 'tx_1rb_sweep_ns' and value:
                tx_test_items_ns_count_nr_1rb_sweep += 1
            if key == 'tx_fcc_power_ns' and value:
                tx_test_items_ns_count_nr_fcc += 1
            if key == 'tx_ce_power_ns' and value:
                tx_test_items_ns_count_nr_ce += 1
            if key == 'tx_harmonics_ns' and value:
                tx_test_items_ns_count_nr += 1
                tx_test_items_ns_count_lte += 1
                tx_test_items_ns_count_wcdma += 1
                tx_test_items_ns_count_gsm += 1
            if key == 'tx_cbe_ns' and value:
                tx_test_items_ns_count_nr += 1
                tx_test_items_ns_count_lte += 1
                tx_test_items_ns_count_wcdma += 1
                tx_test_items_ns_count_gsm += 1
            if key == 'tx_ulca_lte_ns' and value:
                tx_test_items_ns_count_ulca_lte += 1
            if key == 'tx_ulca_lte_cbe_ns' and value:
                tx_test_items_ns_count_ulca_lte += 1
            if key == 'rx_normal_ns' and value:
                rx_test_items_ns_count_nr += 1
                rx_test_items_ns_count_lte += 1
                rx_test_items_ns_count_wcdma += 1
                rx_test_items_ns_count_gsm += 1
            if key == 'rx_quick_ns' and value:
                rx_test_items_ns_count_nr += 1
                rx_test_items_ns_count_lte += 1
            if key == 'rx_endc_desense_ns' and value:
                rx_test_items_endc_ns_count += 1
            if key == 'tx_lmh_s' and value:
                tx_test_items_s_count += 1
            if key == 'rx_normal_s' and value:
                rx_test_items_s_count += 1
            if key == 'rxs_sweep_s' and value:
                rx_test_items_s_count += 1
            if key == 'tx1' and value:
                tx_path_count += 1
            if key == 'tx2' and value:
                tx_path_count += 1
            if key == 'mimo' and value:
                tx_path_count += 1
            if key == 'rx0' and value:
                rx_path_count += 1
            if key == 'rx1' and value:
                rx_path_count += 1
            if key == 'rx2' and value:
                rx_path_count += 1
            if key == 'rx3' and value:
                rx_path_count += 1
            if key == 'rx0rx1' and value:
                rx_path_count += 1
            if key == 'rx2rx3' and value:
                rx_path_count += 1
            if key == 'rx_all_path' and value:
                rx_path_count += 1
            if key == 'ue_txmax' and value:
                ue_power_count += 1
            if key == 'ue_txlow' and value:
                ue_power_count += 1
            if key == 'nr_tech' and value:
                nr_tech_count += 1
            if key == 'lte_tech' and value:
                lte_tech_count += 1
            if key == 'wcdma_tech' and value:
                wcdma_tech_count += 1
            if key == 'gsm_tech' and value:
                gsm_tech_count += 1
            if key == 'ulca_lte_tech' and value:
                ulca_lte_tech_count += 1
            if key == 'hsupa_tech' and value:
                hsupa_tech_count += 1
            if key == 'hsdpa_tech' and value:
                hsdpa_tech_count += 1
            if key == 'lch' and value:
                channel_count += 1
            if key == 'mch' and value:
                channel_count += 1
            if key == 'hch' and value:
                channel_count += 1
            if key == 'n5_nr' and value:
                band_nr_count += 1
            if key == 'n8_nr' and value:
                band_nr_count += 1
            if key == 'n12_nr' and value:
                band_nr_count += 1
            if key == 'n13_nr' and value:
                band_nr_count += 1
            if key == 'n14_nr' and value:
                band_nr_count += 1
            if key == 'n20_nr' and value:
                band_nr_count += 1
            if key == 'n24_nr' and value:
                band_nr_count += 1
            if key == 'n26_nr' and value:
                band_nr_count += 1
            if key == 'n71_nr' and value:
                band_nr_count += 1
            if key == 'n28_a_nr' and value:
                band_nr_count += 1
            if key == 'n28_b_nr' and value:
                band_nr_count += 1
            if key == 'n29_nr' and value:
                band_nr_count += 1
            if key == 'n32_nr' and value:
                band_nr_count += 1
            if key == 'n1_nr' and value:
                band_nr_count += 1
            if key == 'n2_nr' and value:
                band_nr_count += 1
            if key == 'n3_nr' and value:
                band_nr_count += 1
            if key == 'n4_nr' and value:
                band_nr_count += 1
            if key == 'n7_nr' and value:
                band_nr_count += 1
            if key == 'n30_nr' and value:
                band_nr_count += 1
            if key == 'n25_nr' and value:
                band_nr_count += 1
            if key == 'n66_nr' and value:
                band_nr_count += 1
            if key == 'n70_nr' and value:
                band_nr_count += 1
            if key == 'n39_nr' and value:
                band_nr_count += 1
            if key == 'n40_nr' and value:
                band_nr_count += 1
            if key == 'n38_nr' and value:
                band_nr_count += 1
            if key == 'n41_nr' and value:
                band_nr_count += 1
            if key == 'n34_nr' and value:
                band_nr_count += 1
            if key == 'n75_nr' and value:
                band_nr_count += 1
            if key == 'n76_nr' and value:
                band_nr_count += 1
            if key == 'n255_nr' and value:
                band_nr_count += 1
            if key == 'n256_nr' and value:
                band_nr_count += 1
            if key == 'n77_nr' and value:
                band_nr_count += 1
            if key == 'n78_nr' and value:
                band_nr_count += 1
            if key == 'n48_nr' and value:
                band_nr_count += 1
            if key == 'n79_nr' and value:
                band_nr_count += 1
            if key == 'b5_lte' and value:
                band_lte_count += 1
            if key == 'b8_lte' and value:
                band_lte_count += 1
            if key == 'b12_lte' and value:
                band_lte_count += 1
            if key == 'b13_lte' and value:
                band_lte_count += 1
            if key == 'b14_lte' and value:
                band_lte_count += 1
            if key == 'b17_lte' and value:
                band_lte_count += 1
            if key == 'b18_lte' and value:
                band_lte_count += 1
            if key == 'b19_lte' and value:
                band_lte_count += 1
            if key == 'b20_lte' and value:
                band_lte_count += 1
            if key == 'b26_lte' and value:
                band_lte_count += 1
            if key == 'b28_a_lte' and value:
                band_lte_count += 1
            if key == 'b28_b_lte' and value:
                band_lte_count += 1
            if key == 'b29_lte' and value:
                band_lte_count += 1
            if key == 'b32_lte' and value:
                band_lte_count += 1
            if key == 'b71_lte' and value:
                band_lte_count += 1
            if key == 'b24_lte' and value:
                band_lte_count += 1
            if key == 'b1_lte' and value:
                band_lte_count += 1
            if key == 'b2_lte' and value:
                band_lte_count += 1
            if key == 'b3_lte' and value:
                band_lte_count += 1
            if key == 'b4_lte' and value:
                band_lte_count += 1
            if key == 'b7_lte' and value:
                band_lte_count += 1
            if key == 'b30_lte' and value:
                band_lte_count += 1
            if key == 'b39_lte' and value:
                band_lte_count += 1
            if key == 'b40_lte' and value:
                band_lte_count += 1
            if key == 'b38_lte' and value:
                band_lte_count += 1
            if key == 'b41_lte' and value:
                band_lte_count += 1
            if key == 'b23_lte' and value:
                band_lte_count += 1
            if key == 'b42_lte' and value:
                band_lte_count += 1
            if key == 'b48_lte' and value:
                band_lte_count += 1
            if key == 'b5_wcdma' and value:
                band_wcdma_count += 1
            if key == 'b8_wcdma' and value:
                band_wcdma_count += 1
            if key == 'b6_wcdma' and value:
                band_wcdma_count += 1
            if key == 'b19_wcdma' and value:
                band_wcdma_count += 1
            if key == 'b1_wcdma' and value:
                band_wcdma_count += 1
            if key == 'b2_wcdma' and value:
                band_wcdma_count += 1
            if key == 'b4_wcdma' and value:
                band_wcdma_count += 1
            if key == 'gsm850' and value:
                band_gsm_count += 1
            if key == 'gsm900' and value:
                band_gsm_count += 1
            if key == 'gsm1800' and value:
                band_gsm_count += 1
            if key == 'gsm1900' and value:
                band_gsm_count += 1
            if key == 'ulca_5b' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_1c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_3c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_7c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_66b' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_66c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_40c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_38c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_41c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_42c' and value:
                band_ulca_lte_count += 1
            if key == 'ulca_48c' and value:
                band_ulca_lte_count += 1
            if key == 'b3_n78' and value:
                band_endc_desense_count += 1
            if key == 'b2_n77' and value:
                band_endc_desense_count += 1
            if key == 'b66_n77' and value:
                band_endc_desense_count += 1
            if key == 'b66_n2' and value:
                band_endc_desense_count += 1
            if key == 'b66_n5' and value:
                band_endc_desense_count += 1
            if key == 'b12_n78' and value:
                band_endc_desense_count += 1
            if key == 'b5_n78' and value:
                band_endc_desense_count += 1
            if key == 'b28_n78' and value:
                band_endc_desense_count += 1
            if key == 'b5_n77' and value:
                band_endc_desense_count += 1
            if key == 'b13_n5' and value:
                band_endc_desense_count += 1
            if key == 'bw5_nr' and value:
                bw_nr_count += 1
            if key == 'bw10_nr' and value:
                bw_nr_count += 1
            if key == 'bw15_nr' and value:
                bw_nr_count += 1
            if key == 'bw20_nr' and value:
                bw_nr_count += 1
            if key == 'bw25_nr' and value:
                bw_nr_count += 1
            if key == 'bw30_nr' and value:
                bw_nr_count += 1
            if key == 'bw40_nr' and value:
                bw_nr_count += 1
            if key == 'bw50_nr' and value:
                bw_nr_count += 1
            if key == 'bw60_nr' and value:
                bw_nr_count += 1
            if key == 'bw80_nr' and value:
                bw_nr_count += 1
            if key == 'bw90_nr' and value:
                bw_nr_count += 1
            if key == 'bw100_nr' and value:
                bw_nr_count += 1
            if key == 'bw70_nr' and value:
                bw_nr_count += 1
            if key == 'bw35_nr' and value:
                bw_nr_count += 1
            if key == 'bw45_nr' and value:
                bw_nr_count += 1
            if key == 'bw1p4_lte' and value:
                bw_lte_count += 1
            if key == 'bw3_lte' and value:
                bw_lte_count += 1
            if key == 'bw5_lte' and value:
                bw_lte_count += 1
            if key == 'bw10_lte' and value:
                bw_lte_count += 1
            if key == 'bw15_lte' and value:
                bw_lte_count += 1
            if key == 'bw20_lte' and value:
                bw_lte_count += 1
            if key == 'bw20_5' and value:
                bw_ulca_lte_count += 1
            if key == 'bw5_20' and value:
                bw_ulca_lte_count += 1
            if key == 'bw20_10' and value:
                bw_ulca_lte_count += 1
            if key == 'bw10_20' and value:
                bw_ulca_lte_count += 1
            if key == 'bw20_15' and value:
                bw_ulca_lte_count += 1
            if key == 'bw15_20' and value:
                bw_ulca_lte_count += 1
            if key == 'bw20_20' and value:
                bw_ulca_lte_count += 1
            if key == 'bw15_15' and value:
                bw_ulca_lte_count += 1
            if key == 'bw15_10' and value:
                bw_ulca_lte_count += 1
            if key == 'bw10_15' and value:
                bw_ulca_lte_count += 1
            if key == 'bw5_10' and value:
                bw_ulca_lte_count += 1
            if key == 'bw10_5' and value:
                bw_ulca_lte_count += 1
            if key == 'bw10_10' and value:
                bw_ulca_lte_count += 1
            if key == 'bw5_15' and value:
                bw_ulca_lte_count += 1
            if key == 'bw15_5' and value:
                bw_ulca_lte_count += 1
            if key == 'bw40' and value:
                bw_ulca_lte_count += 1
            if key == 'qpsk_nr' and value:
                mcs_nr_count += 1
            if key == 'q16_nr' and value:
                mcs_nr_count += 1
            if key == 'q64_nr' and value:
                mcs_nr_count += 1
            if key == 'q256_nr' and value:
                mcs_nr_count += 1
            if key == 'bpsk_nr' and value:
                mcs_nr_count += 1
            if key == 'dfts_nr' and value:
                type_nr_count += 1
            if key == 'cp_nr' and value:
                type_nr_count += 1
            if key == 'qpsk_lte' and value:
                mcs_lte_count += 1
            if key == 'q16_lte' and value:
                mcs_lte_count += 1
            if key == 'q64_lte' and value:
                mcs_lte_count += 1
            if key == 'q256_lte' and value:
                mcs_lte_count += 1
            if key == 'inner_full_nr' and value:
                rb_nr_count += 1
            if key == 'outer_full_nr' and value:
                rb_nr_count += 1
            if key == 'inner_1rb_left_nr' and value:
                rb_nr_count += 1
            if key == 'inner_1rb_right_nr' and value:
                rb_nr_count += 1
            if key == 'edge_1rb_left_nr' and value:
                rb_nr_count += 1
            if key == 'edge_1rb_right_nr' and value:
                rb_nr_count += 1
            if key == 'edge_full_left_nr' and value:
                rb_nr_count += 1
            if key == 'edge_full_right_nr' and value:
                rb_nr_count += 1
            if key == 'prb0_lte' and value:
                rb_lte_count += 1
            if key == 'prbmax_lte' and value:
                rb_lte_count += 1
            if key == 'frb_lte' and value:
                rb_lte_count += 1
            if key == 'one_rb_0_lte' and value:
                rb_lte_count += 1
            if key == 'one_rb_max_lte' and value:
                rb_lte_count += 1
            if key == 'one_rb0_null' and value:
                rb_ulca_lte_count += 1
            if key == 'prb0_null' and value:
                rb_ulca_lte_count += 1
            if key == 'frb_null' and value:
                rb_ulca_lte_count += 1
            if key == 'frb_frb' and value:
                rb_ulca_lte_count += 1
            if key == 'one_rb0_one_rbmax' and value:
                rb_ulca_lte_count += 1
            if key == 'one_rbmax_one_rb0' and value:
                rb_ulca_lte_count += 1
            if key == 'hthv' and value:
                temp_volt_count += 1
            if key == 'htlv' and value:
                temp_volt_count += 1
            if key == 'ntnv' and value:
                temp_volt_count += 1
            if key == 'lthv' and value:
                temp_volt_count += 1
            if key == 'ltlv' and value:
                temp_volt_count += 1
            if key == 'hv' and value:
                volt_count += 1
            if key == 'nv' and value:
                volt_count += 1
            if key == 'lv' and value:
                volt_count += 1

        count_total = tx_test_items_ns_count_nr * tx_path_count * nr_tech_count * channel_count * band_nr_count * bw_nr_count * mcs_nr_count * type_nr_count * rb_nr_count + \
                      tx_test_items_ns_count_lte * tx_path_count * lte_tech_count * channel_count * band_lte_count * bw_lte_count * mcs_lte_count * rb_lte_count + \
                      tx_test_items_ns_count_wcdma * wcdma_tech_count * channel_count * band_wcdma_count + \
                      tx_test_items_ns_count_gsm * gsm_tech_count * channel_count * band_gsm_count + \
                      tx_test_items_ns_count_ulca_lte * ulca_lte_tech_count * channel_count * band_ulca_lte_count * bw_ulca_lte_count + \
                      tx_test_items_ns_count_nr_freq_sweep * tx_path_count * nr_tech_count * band_nr_count * bw_nr_count * mcs_nr_count * type_nr_count * rb_nr_count + \
                      tx_test_items_ns_count_lte_freq_sweep * tx_path_count * lte_tech_count * band_lte_count * bw_lte_count * mcs_lte_count * rb_lte_count + \
                      tx_test_items_ns_count_wcdma_freq_sweep * wcdma_tech_count * band_wcdma_count + \
                      tx_test_items_ns_count_gsm_freq_sweep * gsm_tech_count * band_gsm_count + \
                      tx_test_items_ns_count_nr_1rb_sweep * tx_path_count * nr_tech_count * channel_count * band_nr_count * bw_nr_count * mcs_nr_count * type_nr_count * rb_nr_count + \
                      rx_test_items_ns_count_nr * rx_path_count * channel_count * band_nr_count * bw_nr_count * ue_power_count + \
                      rx_test_items_ns_count_lte * rx_path_count * channel_count * band_lte_count * bw_lte_count * ue_power_count + \
                      rx_test_items_ns_count_wcdma * rx_path_count * channel_count * band_wcdma_count * ue_power_count + \
                      rx_test_items_ns_count_gsm * rx_path_count * channel_count * band_gsm_count + \
                      rx_test_items_endc_ns_count * band_endc_desense_count * ue_power_count + \
                      tx_test_items_s_count * lte_tech_count * channel_count * band_lte_count + \
                      tx_test_items_s_count * wcdma_tech_count * channel_count * band_wcdma_count + \
                      tx_test_items_s_count * hsupa_tech_count * channel_count * band_wcdma_count + \
                      tx_test_items_s_count * hsdpa_tech_count * channel_count * band_wcdma_count + \
                      rx_test_items_s_count * channel_count * band_lte_count * ue_power_count + \
                      rx_test_items_s_count * channel_count * band_wcdma_count * ue_power_count  + \
                      tx_test_items_ns_count_nr_fcc * tx_path_count * nr_tech_count * band_nr_count * bw_nr_count * mcs_nr_count * type_nr_count + \
                      tx_test_items_ns_count_nr_ce * tx_path_count * nr_tech_count * band_nr_count * bw_nr_count * mcs_nr_count * type_nr_count

        count_total_outer_loop = count_total * state_dict['outer_loop']

        return count_total_outer_loop

    def measure(self):
        start = datetime.datetime.now()

        self.run_button.setEnabled(False)

        if self.tmpchmb_en.isChecked():  # with temp chamber and PSU
            self.tmpcmb = TempChamber()
            self.psu = Psu()
            for temp_volt in self.temp_volts_selected():
                self.condition = temp_volt
                temp = self.temp_dict[temp_volt[:2]]
                volt = self.volt = self.volts_dict[temp_volt[2:]]
                wait = int(self.wait_time_comboBox.currentText())
                self.tmpcmb.tpchb_init(temp, wait)
                self.psu.psu_init(volt)

                self.measure_process()

        elif self.psu_en.isChecked():  # with only PSU
            self.psu = Psu()
            for volt in self.volts_selected():
                self.condition = volt  # HV, NV, LV
                self.psu.psu_init(self.volts_dict[volt])
                self.volt = self.volts_dict[volt]

                self.measure_process()

        else:  # without temp chamber and psu controlled
            self.condition = None
            self.volt = 3.8

            self.measure_process()

        self.run_button.setEnabled(True)

        stop = datetime.datetime.now()
        logger.info(f'Timer: {stop - start}')

    def measure_process(self):
        import utils.excel_handler as excel_hdl
        import utils.adb_handler as adb_hdl
        import equipments.series_basis.modem_usb_serial.serial_series as ss

        self.export_gui_setting_yaml()  # export state_dict to yaml file
        state_dict = self.gui_state_get()
        ss.STATE_SERIAL = adb_hdl.STATE_ADB = excel_hdl.STATE_DICT_EXCEL = state_dict
        counts_total = self.items_counts(state_dict)
        self.progressBar.reset()
        if counts_total != 0:
            self.progressBar.setMaximum(counts_total)
            self.progressBar.setValue(0)
        for loop in range(state_dict['outer_loop']):
            self.measure_base(state_dict)

    def measure_base(self, state_dict):
        logger.info('Measure...')
        match state_dict['equipment']:
            case 'Cmw100':
                from test_scripts.cmw100_items.tx_lmh import TxTestGenre
                from test_scripts.cmw100_items.rx_lmh import RxTestGenre
                from test_scripts.cmw100_items.tx_level_sweep import TxTestLevelSweep
                from test_scripts.cmw100_items.tx_freq_sweep import TxTestFreqSweep
                from test_scripts.cmw100_items.tx_1rb_sweep import TxTest1RbSweep
                from test_scripts.cmw100_items.tx_power_fcc_ce import TxTestFccCe
                from test_scripts.cmw100_items.tx_ulca_combo import TxTestCa
                from test_scripts.cmw100_items.apt_sweep_search import AptSweep
                from test_scripts.cmw100_items.apt_sweep_search_v2 import AptSweepV2

                # First step to create a foldr to storage the files
                excel_folder_create()

                if state_dict['tx_lmh_ns']:
                    inst = TxTestGenre(state_dict, self.progressBar)
                    inst.run()
                    inst.ser.com_close()

                if state_dict['tx_level_sweep_ns']:
                    inst = TxTestLevelSweep(state_dict, self.progressBar)
                    inst.run()
                    inst.ser.com_close()

                if state_dict['tx_freq_sweep_ns']:
                    inst = TxTestFreqSweep(state_dict, self.progressBar)
                    inst.run()
                    inst.ser.com_close()

                if state_dict['tx_1rb_sweep_ns']:
                    inst = TxTest1RbSweep(state_dict, self.progressBar)
                    inst.run()
                    inst.ser.com_close()

                if state_dict['tx_fcc_power_ns']:
                    inst = TxTestFccCe(state_dict, self.progressBar)
                    inst.run_fcc()
                    inst.ser.com_close()

                if state_dict['tx_ce_power_ns']:
                    inst = TxTestFccCe(state_dict, self.progressBar)
                    inst.run_ce()
                    inst.ser.com_close()

                if state_dict['tx_ulca_lte_ns']:
                    ...
                if state_dict['rx_normal_ns'] or state_dict['rx_quick_ns']:
                    inst = RxTestGenre(state_dict, self.progressBar)
                    inst.run_genre()
                    inst.ser.com_close()
                if state_dict['rx_endc_desense_ns']:
                    inst = RxTestGenre(state_dict, self.progressBar)
                    inst.run_endc()
                    inst.ser.com_close()

            case 'Cmw100+Fsw':
                from test_scripts.harmonics_cbe.tx_harmonics import TxHarmonics
                from test_scripts.harmonics_cbe.tx_cbe import TxCBE
                from test_scripts.harmonics_cbe.tx_ulca_cbe import TxTestCaCBE

                if state_dict['tx_harmonics_ns']:
                    ...
                if state_dict['tx_cbe_ns']:
                    ...
                if state_dict['tx_ulca_lte_cbe_ns']:
                    ...

            case 'Anritsu8820':
                from test_scripts.anritsu_items.mt8820_tx_lmh import TxTestGenre
                from test_scripts.anritsu_items.mt8820_rx import RxTestGenre
                from test_scripts.anritsu_items.mt8820_rx_freq_sweep import RxTestFreqSweep

                excel_folder_create()
                if state_dict['tx_lmh_s']:
                    ...
                if state_dict['rx_normal_s']:
                    ...
                if state_dict['rxs_sweep_s']:
                    ...
            case 'Anritsu8821':
                from test_scripts.anritsu_items.mt8821_tx_lmh import TxTestGenre
                from test_scripts.anritsu_items.mt8821_rx import RxTestGenre
                from test_scripts.anritsu_items.mt8821_rx_freq_sweep import RxTestFreqSweep

                if state_dict['tx_lmh_s']:
                    ...
                if state_dict['rx_normal_s']:
                    ...
                if state_dict['rxs_sweep_s']:
                    ...

            case 'Agilent8960':
                pass

    def run_start(self):
        t = threading.Thread(target=self.measure, daemon=True)
        t.start()

    @staticmethod
    def therm_charge_dis():
        from utils.adb_handler import thermal_charger_disable
        thermal_charger_disable()

    @staticmethod
    def stop():
        sys.exit()


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
