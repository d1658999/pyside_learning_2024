from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PySide6.QtCore import QThread, Slot
import sys

from ui_mega_v2_2 import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow, QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.custom_signal_slot()


    def custom_signal_slot(self):
        self.as_path_en.toggled.connect(self.srs_unchecked)
        self.srs_path_en.toggled.connect(self.as_unchecked)

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

    def toolbox_index_set(self, index_dict):
        self.bands_toolBox.setCurrentIndex(index_dict['bands_toolBox_index'])
        self.sync_path_toolBox.setCurrentIndex(index_dict['sync_path_toolBox_index'])
        self.txrx_path_toolBox.setCurrentIndex(index_dict['txrx_path_toolBox_index'])

    def toolbox_index_get(self, index_dict):
        index_dict['bands_toolBox_index'] = self.bands_toolBox.currentIndex()
        index_dict['sync_path_toolBox_index'] = self.sync_path_toolBox.currentIndex()
        index_dict['txrx_path_toolBox_index'] = self.txrx_path_toolBox.currentIndex()
        return index_dict

    def tab_index_set(self, index_dict):
        self.tabWidget.setCurrentIndex(index_dict['tabWidget'])

    def tab_index_get(self, index_dict):
        index_dict['tabWidget'] = self.tabWidget.currentIndex()
        return index_dict




def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()