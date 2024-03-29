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
        self.toolBox.setCurrentIndex(index)

    def toolbox_index_get(self):
        return self.toolBox.currentIndex()

    def tab_index_set(self, index):
        self.tabWidget.setCurrentIndex(index)

    def tab_index_get(self, index):
        return self.tabWidget.currentIndex()




def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()