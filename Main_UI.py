from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QStyleFactory
from PySide6.QtCore import QThread, Slot, QSize
import sys

from ui_mega_v2_5 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow, QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.custom_signal_slot()

    def custom_signal_slot(self):
        self.as_path_en.toggled.connect(self.srs_unchecked)
        self.srs_path_en.toggled.connect(self.as_unchecked)
        self.run_button.clicked.connect(self.run)
        self.therm_charge_dis_button.clicked.connect(self.therm_charge_dis)
        self.stop_button.clicked.connect(self.stop)

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

    def toolbox_index_get(self, state_dict):
        state_dict['bands_toolBox_index'] = self.bands_toolBox.currentIndex()
        state_dict['sync_path_toolBox_index'] = self.sync_path_toolBox.currentIndex()
        state_dict['txrx_path_toolBox_index'] = self.txrx_path_toolBox.currentIndex()
        return state_dict

    def tab_index_set(self, state_dict):
        self.tabWidget.setCurrentIndex(state_dict['tabWidget'])

    def tab_index_get(self, state_dict):
        state_dict['tabWidget'] = self.tabWidget.currentIndex()
        return state_dict

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
