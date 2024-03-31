from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QStyleFactory
from PySide6.QtCore import QThread, Slot, QSize
import sys

from ui_mega_v2_5 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow, QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_show()
        self.init_hidden()
        self.custom_signal_slot()

    def custom_signal_slot(self):
        self.as_path_en.toggled.connect(self.srs_unchecked)
        self.srs_path_en.toggled.connect(self.as_unchecked)
        self.run_button.clicked.connect(self.run)
        self.therm_charge_dis_button.clicked.connect(self.therm_charge_dis)
        self.stop_button.clicked.connect(self.stop)
        self.equipments_comboBox.currentTextChanged.connect(self.equipment_show)
        self.tx_port_comboBox.currentTextChanged.connect(self.tx_port_show)
        self.tx_port_endc_lte_comboBox.currentTextChanged.connect(self.tx_port_endc_lte_show)
        self.rx_endc_desense_ns.stateChanged.connect(self.tx_port_endc_lte_state)
        self.equipments_comboBox.textActivated.connect(self.showout_en)

    def init_show(self):
        print(f'Equipment: {self.equipments_comboBox.currentText()}')
        print(f'Tx port: {self.tx_port_comboBox.currentText()}')

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

    def toolbox_index_set(self, state_dict):
        self.bands_toolBox.setCurrentIndex(state_dict['bands_toolBox_index'])
        self.sync_path_toolBox.setCurrentIndex(state_dict['sync_path_toolBox_index'])
        self.txrx_path_toolBox.setCurrentIndex(state_dict['txrx_path_toolBox_index'])
        self.tabWidget.setCurrentIndex((state_dict['tabWidget_index']))

    def toolbox_index_get(self, state_dict):
        state_dict['bands_toolBox_index'] = self.bands_toolBox.currentIndex()
        state_dict['sync_path_toolBox_index'] = self.sync_path_toolBox.currentIndex()
        state_dict['txrx_path_toolBox_index'] = self.txrx_path_toolBox.currentIndex()
        state_dict['tabWidget_index'] = self.tabWidget.currentIndex()
        return state_dict

    def tab_index_set(self, state_dict):
        self.tabWidget.setCurrentIndex(state_dict['tabWidget'])

    def tab_index_get(self, state_dict):
        state_dict['tabWidget'] = self.tabWidget.currentIndex()
        return state_dict

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

    def run(self):
        print('run')

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
