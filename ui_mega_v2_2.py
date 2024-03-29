# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mega_v2_2.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QToolBox, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1491, 772)
        icon = QIcon()
        icon.addFile(u"./Wave.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionLoad_file = QAction(MainWindow)
        self.actionLoad_file.setObjectName(u"actionLoad_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(710, 0, 781, 721))
        self.bands = QWidget()
        self.bands.setObjectName(u"bands")
        self.bands_toolBox = QToolBox(self.bands)
        self.bands_toolBox.setObjectName(u"bands_toolBox")
        self.bands_toolBox.setGeometry(QRect(0, 0, 1111, 681))
        self.page_nr = QWidget()
        self.page_nr.setObjectName(u"page_nr")
        self.page_nr.setGeometry(QRect(0, 0, 1111, 561))
        self.frame_band_nr = QFrame(self.page_nr)
        self.frame_band_nr.setObjectName(u"frame_band_nr")
        self.frame_band_nr.setGeometry(QRect(0, -10, 771, 581))
        self.frame_band_nr.setFrameShape(QFrame.StyledPanel)
        self.frame_band_nr.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_band_nr)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_lb_nr = QGroupBox(self.frame_band_nr)
        self.groupBox_lb_nr.setObjectName(u"groupBox_lb_nr")
        self.layoutWidget = QWidget(self.groupBox_lb_nr)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 231, 531))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.n24_nr = QCheckBox(self.layoutWidget)
        self.n24_nr.setObjectName(u"n24_nr")

        self.gridLayout_2.addWidget(self.n24_nr, 6, 0, 1, 1)

        self.n20_nr = QCheckBox(self.layoutWidget)
        self.n20_nr.setObjectName(u"n20_nr")

        self.gridLayout_2.addWidget(self.n20_nr, 5, 0, 1, 1)

        self.n12_nr = QCheckBox(self.layoutWidget)
        self.n12_nr.setObjectName(u"n12_nr")

        self.gridLayout_2.addWidget(self.n12_nr, 2, 0, 1, 1)

        self.n28_a_nr = QCheckBox(self.layoutWidget)
        self.n28_a_nr.setObjectName(u"n28_a_nr")
        self.n28_a_nr.setEnabled(True)
        self.n28_a_nr.setCheckable(True)
        self.n28_a_nr.setChecked(False)

        self.gridLayout_2.addWidget(self.n28_a_nr, 0, 1, 1, 1)

        self.n8_nr = QCheckBox(self.layoutWidget)
        self.n8_nr.setObjectName(u"n8_nr")

        self.gridLayout_2.addWidget(self.n8_nr, 1, 0, 1, 1)

        self.n13_nr = QCheckBox(self.layoutWidget)
        self.n13_nr.setObjectName(u"n13_nr")

        self.gridLayout_2.addWidget(self.n13_nr, 3, 0, 1, 1)

        self.n5_nr = QCheckBox(self.layoutWidget)
        self.n5_nr.setObjectName(u"n5_nr")

        self.gridLayout_2.addWidget(self.n5_nr, 0, 0, 1, 1)

        self.n14_nr = QCheckBox(self.layoutWidget)
        self.n14_nr.setObjectName(u"n14_nr")

        self.gridLayout_2.addWidget(self.n14_nr, 4, 0, 1, 1)

        self.n26_nr = QCheckBox(self.layoutWidget)
        self.n26_nr.setObjectName(u"n26_nr")

        self.gridLayout_2.addWidget(self.n26_nr, 7, 0, 1, 1)

        self.n71_nr = QCheckBox(self.layoutWidget)
        self.n71_nr.setObjectName(u"n71_nr")

        self.gridLayout_2.addWidget(self.n71_nr, 8, 0, 1, 1)

        self.n32_nr = QCheckBox(self.layoutWidget)
        self.n32_nr.setObjectName(u"n32_nr")

        self.gridLayout_2.addWidget(self.n32_nr, 3, 1, 1, 1)

        self.n29_nr = QCheckBox(self.layoutWidget)
        self.n29_nr.setObjectName(u"n29_nr")

        self.gridLayout_2.addWidget(self.n29_nr, 2, 1, 1, 1)

        self.n28_b_nr = QCheckBox(self.layoutWidget)
        self.n28_b_nr.setObjectName(u"n28_b_nr")
        self.n28_b_nr.setChecked(False)

        self.gridLayout_2.addWidget(self.n28_b_nr, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_lb_nr)

        self.groupBox_mb_nr = QGroupBox(self.frame_band_nr)
        self.groupBox_mb_nr.setObjectName(u"groupBox_mb_nr")
        self.layoutWidget1 = QWidget(self.groupBox_mb_nr)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 20, 231, 531))
        self.gridLayout = QGridLayout(self.layoutWidget1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.n41_nr = QCheckBox(self.layoutWidget1)
        self.n41_nr.setObjectName(u"n41_nr")

        self.gridLayout.addWidget(self.n41_nr, 3, 1, 1, 1)

        self.n25_nr = QCheckBox(self.layoutWidget1)
        self.n25_nr.setObjectName(u"n25_nr")

        self.gridLayout.addWidget(self.n25_nr, 6, 0, 1, 1)

        self.n76_nr = QCheckBox(self.layoutWidget1)
        self.n76_nr.setObjectName(u"n76_nr")

        self.gridLayout.addWidget(self.n76_nr, 6, 1, 1, 1)

        self.n40_nr = QCheckBox(self.layoutWidget1)
        self.n40_nr.setObjectName(u"n40_nr")
        self.n40_nr.setChecked(False)

        self.gridLayout.addWidget(self.n40_nr, 1, 1, 1, 1)

        self.n30_nr = QCheckBox(self.layoutWidget1)
        self.n30_nr.setObjectName(u"n30_nr")

        self.gridLayout.addWidget(self.n30_nr, 5, 0, 1, 1)

        self.n38_nr = QCheckBox(self.layoutWidget1)
        self.n38_nr.setObjectName(u"n38_nr")

        self.gridLayout.addWidget(self.n38_nr, 2, 1, 1, 1)

        self.n3_nr = QCheckBox(self.layoutWidget1)
        self.n3_nr.setObjectName(u"n3_nr")

        self.gridLayout.addWidget(self.n3_nr, 2, 0, 1, 1)

        self.n255_nr = QCheckBox(self.layoutWidget1)
        self.n255_nr.setObjectName(u"n255_nr")

        self.gridLayout.addWidget(self.n255_nr, 7, 1, 1, 1)

        self.n39_nr = QCheckBox(self.layoutWidget1)
        self.n39_nr.setObjectName(u"n39_nr")
        self.n39_nr.setEnabled(True)
        self.n39_nr.setCheckable(True)
        self.n39_nr.setChecked(False)

        self.gridLayout.addWidget(self.n39_nr, 0, 1, 1, 1)

        self.n256_nr = QCheckBox(self.layoutWidget1)
        self.n256_nr.setObjectName(u"n256_nr")

        self.gridLayout.addWidget(self.n256_nr, 8, 1, 1, 1)

        self.n2_nr = QCheckBox(self.layoutWidget1)
        self.n2_nr.setObjectName(u"n2_nr")

        self.gridLayout.addWidget(self.n2_nr, 1, 0, 1, 1)

        self.n4_nr = QCheckBox(self.layoutWidget1)
        self.n4_nr.setObjectName(u"n4_nr")

        self.gridLayout.addWidget(self.n4_nr, 3, 0, 1, 1)

        self.n34_nr = QCheckBox(self.layoutWidget1)
        self.n34_nr.setObjectName(u"n34_nr")

        self.gridLayout.addWidget(self.n34_nr, 4, 1, 1, 1)

        self.n70_nr = QCheckBox(self.layoutWidget1)
        self.n70_nr.setObjectName(u"n70_nr")

        self.gridLayout.addWidget(self.n70_nr, 8, 0, 1, 1)

        self.n1_nr = QCheckBox(self.layoutWidget1)
        self.n1_nr.setObjectName(u"n1_nr")

        self.gridLayout.addWidget(self.n1_nr, 0, 0, 1, 1)

        self.n75_nr = QCheckBox(self.layoutWidget1)
        self.n75_nr.setObjectName(u"n75_nr")

        self.gridLayout.addWidget(self.n75_nr, 5, 1, 1, 1)

        self.n7_nr = QCheckBox(self.layoutWidget1)
        self.n7_nr.setObjectName(u"n7_nr")

        self.gridLayout.addWidget(self.n7_nr, 4, 0, 1, 1)

        self.n66_nr = QCheckBox(self.layoutWidget1)
        self.n66_nr.setObjectName(u"n66_nr")

        self.gridLayout.addWidget(self.n66_nr, 7, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_mb_nr)

        self.groupBox_uhb_nr = QGroupBox(self.frame_band_nr)
        self.groupBox_uhb_nr.setObjectName(u"groupBox_uhb_nr")
        self.layoutWidget_2 = QWidget(self.groupBox_uhb_nr)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 20, 231, 251))
        self.gridLayout_3 = QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.n3_nr_2 = QCheckBox(self.layoutWidget_2)
        self.n3_nr_2.setObjectName(u"n3_nr_2")

        self.gridLayout_3.addWidget(self.n3_nr_2, 2, 0, 1, 1)

        self.n1_nr_2 = QCheckBox(self.layoutWidget_2)
        self.n1_nr_2.setObjectName(u"n1_nr_2")

        self.gridLayout_3.addWidget(self.n1_nr_2, 0, 0, 1, 1)

        self.n2_nr_2 = QCheckBox(self.layoutWidget_2)
        self.n2_nr_2.setObjectName(u"n2_nr_2")

        self.gridLayout_3.addWidget(self.n2_nr_2, 1, 0, 1, 1)

        self.n4_nr_2 = QCheckBox(self.layoutWidget_2)
        self.n4_nr_2.setObjectName(u"n4_nr_2")

        self.gridLayout_3.addWidget(self.n4_nr_2, 3, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_uhb_nr)

        self.bands_toolBox.addItem(self.page_nr, u"NR")
        self.page_lte = QWidget()
        self.page_lte.setObjectName(u"page_lte")
        self.page_lte.setGeometry(QRect(0, 0, 1111, 561))
        self.frame_band_lte = QFrame(self.page_lte)
        self.frame_band_lte.setObjectName(u"frame_band_lte")
        self.frame_band_lte.setGeometry(QRect(0, -10, 771, 581))
        self.frame_band_lte.setFrameShape(QFrame.StyledPanel)
        self.frame_band_lte.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_band_lte)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_lb_lte = QGroupBox(self.frame_band_lte)
        self.groupBox_lb_lte.setObjectName(u"groupBox_lb_lte")
        self.layoutWidget2 = QWidget(self.groupBox_lb_lte)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 231, 531))
        self.gridLayout_10 = QGridLayout(self.layoutWidget2)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.b5_lte = QCheckBox(self.layoutWidget2)
        self.b5_lte.setObjectName(u"b5_lte")

        self.gridLayout_10.addWidget(self.b5_lte, 0, 0, 1, 1)

        self.b26_lte = QCheckBox(self.layoutWidget2)
        self.b26_lte.setObjectName(u"b26_lte")

        self.gridLayout_10.addWidget(self.b26_lte, 0, 1, 1, 1)

        self.b8_lte = QCheckBox(self.layoutWidget2)
        self.b8_lte.setObjectName(u"b8_lte")

        self.gridLayout_10.addWidget(self.b8_lte, 1, 0, 1, 1)

        self.b28_a_lte = QCheckBox(self.layoutWidget2)
        self.b28_a_lte.setObjectName(u"b28_a_lte")
        self.b28_a_lte.setEnabled(True)
        self.b28_a_lte.setCheckable(True)
        self.b28_a_lte.setChecked(False)

        self.gridLayout_10.addWidget(self.b28_a_lte, 1, 1, 1, 1)

        self.b12_lte = QCheckBox(self.layoutWidget2)
        self.b12_lte.setObjectName(u"b12_lte")

        self.gridLayout_10.addWidget(self.b12_lte, 2, 0, 1, 1)

        self.b28_b_lte = QCheckBox(self.layoutWidget2)
        self.b28_b_lte.setObjectName(u"b28_b_lte")
        self.b28_b_lte.setChecked(False)

        self.gridLayout_10.addWidget(self.b28_b_lte, 2, 1, 1, 1)

        self.b13_lte = QCheckBox(self.layoutWidget2)
        self.b13_lte.setObjectName(u"b13_lte")

        self.gridLayout_10.addWidget(self.b13_lte, 3, 0, 1, 1)

        self.b29_lte = QCheckBox(self.layoutWidget2)
        self.b29_lte.setObjectName(u"b29_lte")

        self.gridLayout_10.addWidget(self.b29_lte, 3, 1, 1, 1)

        self.b14_lte = QCheckBox(self.layoutWidget2)
        self.b14_lte.setObjectName(u"b14_lte")

        self.gridLayout_10.addWidget(self.b14_lte, 4, 0, 1, 1)

        self.b32_lte = QCheckBox(self.layoutWidget2)
        self.b32_lte.setObjectName(u"b32_lte")

        self.gridLayout_10.addWidget(self.b32_lte, 4, 1, 1, 1)

        self.b17_lte = QCheckBox(self.layoutWidget2)
        self.b17_lte.setObjectName(u"b17_lte")

        self.gridLayout_10.addWidget(self.b17_lte, 5, 0, 1, 1)

        self.b71_lte = QCheckBox(self.layoutWidget2)
        self.b71_lte.setObjectName(u"b71_lte")

        self.gridLayout_10.addWidget(self.b71_lte, 5, 1, 1, 1)

        self.b18_lte = QCheckBox(self.layoutWidget2)
        self.b18_lte.setObjectName(u"b18_lte")

        self.gridLayout_10.addWidget(self.b18_lte, 6, 0, 1, 1)

        self.b19_lte = QCheckBox(self.layoutWidget2)
        self.b19_lte.setObjectName(u"b19_lte")

        self.gridLayout_10.addWidget(self.b19_lte, 7, 0, 1, 1)

        self.b20_lte = QCheckBox(self.layoutWidget2)
        self.b20_lte.setObjectName(u"b20_lte")

        self.gridLayout_10.addWidget(self.b20_lte, 8, 0, 1, 1)

        self.b24_lte = QCheckBox(self.layoutWidget2)
        self.b24_lte.setObjectName(u"b24_lte")

        self.gridLayout_10.addWidget(self.b24_lte, 6, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_lb_lte)

        self.groupBox_mb_lte = QGroupBox(self.frame_band_lte)
        self.groupBox_mb_lte.setObjectName(u"groupBox_mb_lte")
        self.layoutWidget_4 = QWidget(self.groupBox_mb_lte)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(10, 20, 231, 531))
        self.gridLayout_11 = QGridLayout(self.layoutWidget_4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.b38_lte = QCheckBox(self.layoutWidget_4)
        self.b38_lte.setObjectName(u"b38_lte")

        self.gridLayout_11.addWidget(self.b38_lte, 2, 1, 1, 1)

        self.b39_lte = QCheckBox(self.layoutWidget_4)
        self.b39_lte.setObjectName(u"b39_lte")
        self.b39_lte.setEnabled(True)
        self.b39_lte.setCheckable(True)
        self.b39_lte.setChecked(False)

        self.gridLayout_11.addWidget(self.b39_lte, 0, 1, 1, 1)

        self.b66_lte = QCheckBox(self.layoutWidget_4)
        self.b66_lte.setObjectName(u"b66_lte")

        self.gridLayout_11.addWidget(self.b66_lte, 7, 0, 1, 1)

        self.b21_lte = QCheckBox(self.layoutWidget_4)
        self.b21_lte.setObjectName(u"b21_lte")

        self.gridLayout_11.addWidget(self.b21_lte, 8, 0, 1, 1)

        self.b7_lte = QCheckBox(self.layoutWidget_4)
        self.b7_lte.setObjectName(u"b7_lte")

        self.gridLayout_11.addWidget(self.b7_lte, 4, 0, 1, 1)

        self.b25_lte = QCheckBox(self.layoutWidget_4)
        self.b25_lte.setObjectName(u"b25_lte")

        self.gridLayout_11.addWidget(self.b25_lte, 6, 0, 1, 1)

        self.b1_lte = QCheckBox(self.layoutWidget_4)
        self.b1_lte.setObjectName(u"b1_lte")

        self.gridLayout_11.addWidget(self.b1_lte, 0, 0, 1, 1)

        self.b2_lte = QCheckBox(self.layoutWidget_4)
        self.b2_lte.setObjectName(u"b2_lte")

        self.gridLayout_11.addWidget(self.b2_lte, 1, 0, 1, 1)

        self.b40_lte = QCheckBox(self.layoutWidget_4)
        self.b40_lte.setObjectName(u"b40_lte")
        self.b40_lte.setChecked(False)

        self.gridLayout_11.addWidget(self.b40_lte, 1, 1, 1, 1)

        self.b41_lte = QCheckBox(self.layoutWidget_4)
        self.b41_lte.setObjectName(u"b41_lte")

        self.gridLayout_11.addWidget(self.b41_lte, 3, 1, 1, 1)

        self.b30_lte = QCheckBox(self.layoutWidget_4)
        self.b30_lte.setObjectName(u"b30_lte")

        self.gridLayout_11.addWidget(self.b30_lte, 5, 0, 1, 1)

        self.b3_lte = QCheckBox(self.layoutWidget_4)
        self.b3_lte.setObjectName(u"b3_lte")

        self.gridLayout_11.addWidget(self.b3_lte, 2, 0, 1, 1)

        self.b23_lte = QCheckBox(self.layoutWidget_4)
        self.b23_lte.setObjectName(u"b23_lte")

        self.gridLayout_11.addWidget(self.b23_lte, 4, 1, 1, 1)

        self.b4_lte = QCheckBox(self.layoutWidget_4)
        self.b4_lte.setObjectName(u"b4_lte")

        self.gridLayout_11.addWidget(self.b4_lte, 3, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_mb_lte)

        self.groupBox_uhb_lte = QGroupBox(self.frame_band_lte)
        self.groupBox_uhb_lte.setObjectName(u"groupBox_uhb_lte")
        self.layoutWidget_5 = QWidget(self.groupBox_uhb_lte)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(10, 20, 231, 141))
        self.gridLayout_12 = QGridLayout(self.layoutWidget_5)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.n3_nr_8 = QCheckBox(self.layoutWidget_5)
        self.n3_nr_8.setObjectName(u"n3_nr_8")

        self.gridLayout_12.addWidget(self.n3_nr_8, 1, 0, 1, 1)

        self.b42_lte = QCheckBox(self.layoutWidget_5)
        self.b42_lte.setObjectName(u"b42_lte")

        self.gridLayout_12.addWidget(self.b42_lte, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_uhb_lte)

        self.bands_toolBox.addItem(self.page_lte, u"LTE")
        self.page_wcdma = QWidget()
        self.page_wcdma.setObjectName(u"page_wcdma")
        self.page_wcdma.setGeometry(QRect(0, 0, 1111, 561))
        self.frame_band_wcdma = QFrame(self.page_wcdma)
        self.frame_band_wcdma.setObjectName(u"frame_band_wcdma")
        self.frame_band_wcdma.setGeometry(QRect(0, -10, 771, 581))
        self.frame_band_wcdma.setFrameShape(QFrame.StyledPanel)
        self.frame_band_wcdma.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_band_wcdma)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_lb_wcdma = QGroupBox(self.frame_band_wcdma)
        self.groupBox_lb_wcdma.setObjectName(u"groupBox_lb_wcdma")
        self.layoutWidget_3 = QWidget(self.groupBox_lb_wcdma)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(10, 20, 341, 191))
        self.gridLayout_13 = QGridLayout(self.layoutWidget_3)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.b5_wcdma = QCheckBox(self.layoutWidget_3)
        self.b5_wcdma.setObjectName(u"b5_wcdma")

        self.gridLayout_13.addWidget(self.b5_wcdma, 0, 0, 1, 1)

        self.b6_wcdma = QCheckBox(self.layoutWidget_3)
        self.b6_wcdma.setObjectName(u"b6_wcdma")

        self.gridLayout_13.addWidget(self.b6_wcdma, 2, 0, 1, 1)

        self.b8_wcdma = QCheckBox(self.layoutWidget_3)
        self.b8_wcdma.setObjectName(u"b8_wcdma")

        self.gridLayout_13.addWidget(self.b8_wcdma, 1, 0, 1, 1)

        self.b19_wcdma = QCheckBox(self.layoutWidget_3)
        self.b19_wcdma.setObjectName(u"b19_wcdma")

        self.gridLayout_13.addWidget(self.b19_wcdma, 3, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_lb_wcdma)

        self.groupBox_mb_wcdma = QGroupBox(self.frame_band_wcdma)
        self.groupBox_mb_wcdma.setObjectName(u"groupBox_mb_wcdma")
        self.layoutWidget_6 = QWidget(self.groupBox_mb_wcdma)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(10, 20, 341, 191))
        self.gridLayout_14 = QGridLayout(self.layoutWidget_6)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.b2_wcdma = QCheckBox(self.layoutWidget_6)
        self.b2_wcdma.setObjectName(u"b2_wcdma")

        self.gridLayout_14.addWidget(self.b2_wcdma, 1, 0, 1, 1)

        self.b4_wcdma = QCheckBox(self.layoutWidget_6)
        self.b4_wcdma.setObjectName(u"b4_wcdma")

        self.gridLayout_14.addWidget(self.b4_wcdma, 2, 0, 1, 1)

        self.b1_wcdma = QCheckBox(self.layoutWidget_6)
        self.b1_wcdma.setObjectName(u"b1_wcdma")

        self.gridLayout_14.addWidget(self.b1_wcdma, 0, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_mb_wcdma)

        self.bands_toolBox.addItem(self.page_wcdma, u"WCDMA")
        self.page_gsm = QWidget()
        self.page_gsm.setObjectName(u"page_gsm")
        self.page_gsm.setGeometry(QRect(0, 0, 1111, 561))
        self.frame_band_gsm = QFrame(self.page_gsm)
        self.frame_band_gsm.setObjectName(u"frame_band_gsm")
        self.frame_band_gsm.setGeometry(QRect(0, -10, 771, 581))
        self.frame_band_gsm.setFrameShape(QFrame.StyledPanel)
        self.frame_band_gsm.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_band_gsm)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_lb_gsm = QGroupBox(self.frame_band_gsm)
        self.groupBox_lb_gsm.setObjectName(u"groupBox_lb_gsm")
        self.layoutWidget_7 = QWidget(self.groupBox_lb_gsm)
        self.layoutWidget_7.setObjectName(u"layoutWidget_7")
        self.layoutWidget_7.setGeometry(QRect(10, 20, 341, 121))
        self.gridLayout_15 = QGridLayout(self.layoutWidget_7)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gsm850 = QCheckBox(self.layoutWidget_7)
        self.gsm850.setObjectName(u"gsm850")

        self.gridLayout_15.addWidget(self.gsm850, 0, 0, 1, 1)

        self.gsm900 = QCheckBox(self.layoutWidget_7)
        self.gsm900.setObjectName(u"gsm900")

        self.gridLayout_15.addWidget(self.gsm900, 1, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.groupBox_lb_gsm)

        self.groupBox_mb_gsm = QGroupBox(self.frame_band_gsm)
        self.groupBox_mb_gsm.setObjectName(u"groupBox_mb_gsm")
        self.layoutWidget_8 = QWidget(self.groupBox_mb_gsm)
        self.layoutWidget_8.setObjectName(u"layoutWidget_8")
        self.layoutWidget_8.setGeometry(QRect(10, 20, 341, 121))
        self.gridLayout_16 = QGridLayout(self.layoutWidget_8)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.gsm1900 = QCheckBox(self.layoutWidget_8)
        self.gsm1900.setObjectName(u"gsm1900")

        self.gridLayout_16.addWidget(self.gsm1900, 1, 0, 1, 1)

        self.gsm1800 = QCheckBox(self.layoutWidget_8)
        self.gsm1800.setObjectName(u"gsm1800")

        self.gridLayout_16.addWidget(self.gsm1800, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.groupBox_mb_gsm)

        self.bands_toolBox.addItem(self.page_gsm, u"GSM")
        self.tabWidget.addTab(self.bands, "")
        self.bw = QWidget()
        self.bw.setObjectName(u"bw")
        self.tabWidget.addTab(self.bw, "")
        self.mcs_rb = QWidget()
        self.mcs_rb.setObjectName(u"mcs_rb")
        self.mcs_rb.setEnabled(True)
        self.tabWidget.addTab(self.mcs_rb, "")
        self.temp_psu_tab = QWidget()
        self.temp_psu_tab.setObjectName(u"temp_psu_tab")
        self.tabWidget.addTab(self.temp_psu_tab, "")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 340, 141, 381))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.therm_charge_dis = QPushButton(self.frame)
        self.therm_charge_dis.setObjectName(u"therm_charge_dis")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.therm_charge_dis.sizePolicy().hasHeightForWidth())
        self.therm_charge_dis.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.therm_charge_dis)

        self.run = QPushButton(self.frame)
        self.run.setObjectName(u"run")
        sizePolicy1.setHeightForWidth(self.run.sizePolicy().hasHeightForWidth())
        self.run.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.run)

        self.stop = QPushButton(self.frame)
        self.stop.setObjectName(u"stop")
        sizePolicy1.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.stop)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout.setStretch(2, 2)
        self.layoutWidget_10 = QWidget(self.centralwidget)
        self.layoutWidget_10.setObjectName(u"layoutWidget_10")
        self.layoutWidget_10.setGeometry(QRect(470, 0, 121, 721))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget_10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.sync_group = QGroupBox(self.layoutWidget_10)
        self.sync_group.setObjectName(u"sync_group")
        self.sync_path_toolBox = QToolBox(self.sync_group)
        self.sync_path_toolBox.setObjectName(u"sync_path_toolBox")
        self.sync_path_toolBox.setGeometry(QRect(10, 20, 101, 331))
        self.general_sync = QWidget()
        self.general_sync.setObjectName(u"general_sync")
        self.general_sync.setGeometry(QRect(0, 0, 101, 271))
        self.sync_path_toolBox.addItem(self.general_sync, u"General")
        self.endc_sync = QWidget()
        self.endc_sync.setObjectName(u"endc_sync")
        self.endc_sync.setGeometry(QRect(0, 0, 101, 271))
        self.sync_path_toolBox.addItem(self.endc_sync, u"ENDC")

        self.verticalLayout_5.addWidget(self.sync_group)

        self.tx_rx_path_group = QGroupBox(self.layoutWidget_10)
        self.tx_rx_path_group.setObjectName(u"tx_rx_path_group")
        self.txrx_toolBox = QToolBox(self.tx_rx_path_group)
        self.txrx_toolBox.setObjectName(u"txrx_toolBox")
        self.txrx_toolBox.setGeometry(QRect(10, 20, 101, 331))
        self.tx_path = QWidget()
        self.tx_path.setObjectName(u"tx_path")
        self.tx_path.setGeometry(QRect(0, 0, 101, 271))
        self.txrx_toolBox.addItem(self.tx_path, u"Tx Path")
        self.rx_path = QWidget()
        self.rx_path.setObjectName(u"rx_path")
        self.rx_path.setGeometry(QRect(0, 0, 101, 271))
        self.txrx_toolBox.addItem(self.rx_path, u"Rx Path")

        self.verticalLayout_5.addWidget(self.tx_rx_path_group)

        self.layoutWidget3 = QWidget(self.centralwidget)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(594, 0, 111, 721))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tech_group = QGroupBox(self.layoutWidget3)
        self.tech_group.setObjectName(u"tech_group")
        self.layoutWidget_9 = QWidget(self.tech_group)
        self.layoutWidget_9.setObjectName(u"layoutWidget_9")
        self.layoutWidget_9.setGeometry(QRect(10, 30, 91, 126))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget_9)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.nr_tech = QCheckBox(self.layoutWidget_9)
        self.nr_tech.setObjectName(u"nr_tech")

        self.verticalLayout_4.addWidget(self.nr_tech)

        self.lte_tech = QCheckBox(self.layoutWidget_9)
        self.lte_tech.setObjectName(u"lte_tech")

        self.verticalLayout_4.addWidget(self.lte_tech)

        self.wcdma_tech = QCheckBox(self.layoutWidget_9)
        self.wcdma_tech.setObjectName(u"wcdma_tech")

        self.verticalLayout_4.addWidget(self.wcdma_tech)

        self.gsm_tech = QCheckBox(self.layoutWidget_9)
        self.gsm_tech.setObjectName(u"gsm_tech")

        self.verticalLayout_4.addWidget(self.gsm_tech)

        self.ulca_lte_tech = QCheckBox(self.layoutWidget_9)
        self.ulca_lte_tech.setObjectName(u"ulca_lte_tech")

        self.verticalLayout_4.addWidget(self.ulca_lte_tech)


        self.verticalLayout_2.addWidget(self.tech_group)

        self.channel_group = QGroupBox(self.layoutWidget3)
        self.channel_group.setObjectName(u"channel_group")
        self.layoutWidget4 = QWidget(self.channel_group)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(10, 30, 91, 81))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lch = QCheckBox(self.layoutWidget4)
        self.lch.setObjectName(u"lch")

        self.verticalLayout_3.addWidget(self.lch)

        self.mch = QCheckBox(self.layoutWidget4)
        self.mch.setObjectName(u"mch")

        self.verticalLayout_3.addWidget(self.mch)

        self.hch = QCheckBox(self.layoutWidget4)
        self.hch.setObjectName(u"hch")

        self.verticalLayout_3.addWidget(self.hch)


        self.verticalLayout_2.addWidget(self.channel_group)

        self.layoutWidget5 = QWidget(self.centralwidget)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(360, 0, 104, 240))
        self.verticalLayout_8 = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.sync_path_label = QLabel(self.layoutWidget5)
        self.sync_path_label.setObjectName(u"sync_path_label")
        self.sync_path_label.setEnabled(True)
        sizePolicy.setHeightForWidth(self.sync_path_label.sizePolicy().hasHeightForWidth())
        self.sync_path_label.setSizePolicy(sizePolicy)
        self.sync_path_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_7.addWidget(self.sync_path_label)

        self.sync_path_comboBox = QComboBox(self.layoutWidget5)
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.setObjectName(u"sync_path_comboBox")
        self.sync_path_comboBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_7.addWidget(self.sync_path_comboBox)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.as_path_en = QCheckBox(self.layoutWidget5)
        self.as_path_en.setObjectName(u"as_path_en")

        self.verticalLayout_8.addWidget(self.as_path_en)

        self.as_path_comboBox = QComboBox(self.layoutWidget5)
        self.as_path_comboBox.addItem("")
        self.as_path_comboBox.addItem("")
        self.as_path_comboBox.setObjectName(u"as_path_comboBox")
        self.as_path_comboBox.setEnabled(False)
        self.as_path_comboBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_8.addWidget(self.as_path_comboBox)

        self.srs_path_en = QCheckBox(self.layoutWidget5)
        self.srs_path_en.setObjectName(u"srs_path_en")
        self.srs_path_en.setChecked(False)

        self.verticalLayout_8.addWidget(self.srs_path_en)

        self.srs_path_comboBox = QComboBox(self.layoutWidget5)
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.setObjectName(u"srs_path_comboBox")
        self.srs_path_comboBox.setEnabled(False)
        self.srs_path_comboBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_8.addWidget(self.srs_path_comboBox)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.sync_path_label_2 = QLabel(self.layoutWidget5)
        self.sync_path_label_2.setObjectName(u"sync_path_label_2")
        self.sync_path_label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_6.addWidget(self.sync_path_label_2)

        self.spinBox = QSpinBox(self.layoutWidget5)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setAlignment(Qt.AlignCenter)
        self.spinBox.setMaximum(30)
        self.spinBox.setValue(26)

        self.verticalLayout_6.addWidget(self.spinBox)


        self.verticalLayout_8.addLayout(self.verticalLayout_6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1491, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionLoad_file)

        self.retranslateUi(MainWindow)
        self.as_path_en.toggled.connect(self.as_path_comboBox.setEnabled)
        self.srs_path_en.toggled.connect(self.srs_path_comboBox.setEnabled)

        self.tabWidget.setCurrentIndex(0)
        self.bands_toolBox.setCurrentIndex(0)
        self.sync_path_toolBox.setCurrentIndex(0)
        self.txrx_toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mega_Tool", None))
        self.actionLoad_file.setText(QCoreApplication.translate("MainWindow", u"Load file", None))
        self.groupBox_lb_nr.setTitle(QCoreApplication.translate("MainWindow", u"LB", None))
        self.n24_nr.setText(QCoreApplication.translate("MainWindow", u"N24", None))
        self.n20_nr.setText(QCoreApplication.translate("MainWindow", u"N20", None))
        self.n12_nr.setText(QCoreApplication.translate("MainWindow", u"N12", None))
#if QT_CONFIG(statustip)
        self.n28_a_nr.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.n28_a_nr.setText(QCoreApplication.translate("MainWindow", u"N28_A", None))
        self.n8_nr.setText(QCoreApplication.translate("MainWindow", u"N8", None))
        self.n13_nr.setText(QCoreApplication.translate("MainWindow", u"N13", None))
        self.n5_nr.setText(QCoreApplication.translate("MainWindow", u"N5", None))
        self.n14_nr.setText(QCoreApplication.translate("MainWindow", u"N14", None))
        self.n26_nr.setText(QCoreApplication.translate("MainWindow", u"N26", None))
        self.n71_nr.setText(QCoreApplication.translate("MainWindow", u"N71", None))
        self.n32_nr.setText(QCoreApplication.translate("MainWindow", u"N32", None))
        self.n29_nr.setText(QCoreApplication.translate("MainWindow", u"N29", None))
        self.n28_b_nr.setText(QCoreApplication.translate("MainWindow", u"N28_B", None))
        self.groupBox_mb_nr.setTitle(QCoreApplication.translate("MainWindow", u"MB", None))
        self.n41_nr.setText(QCoreApplication.translate("MainWindow", u"N41", None))
        self.n25_nr.setText(QCoreApplication.translate("MainWindow", u"N25", None))
        self.n76_nr.setText(QCoreApplication.translate("MainWindow", u"N76", None))
        self.n40_nr.setText(QCoreApplication.translate("MainWindow", u"N40", None))
        self.n30_nr.setText(QCoreApplication.translate("MainWindow", u"N30", None))
        self.n38_nr.setText(QCoreApplication.translate("MainWindow", u"N38", None))
        self.n3_nr.setText(QCoreApplication.translate("MainWindow", u"N3", None))
        self.n255_nr.setText(QCoreApplication.translate("MainWindow", u"N255", None))
#if QT_CONFIG(statustip)
        self.n39_nr.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.n39_nr.setText(QCoreApplication.translate("MainWindow", u"N39", None))
        self.n256_nr.setText(QCoreApplication.translate("MainWindow", u"N256", None))
        self.n2_nr.setText(QCoreApplication.translate("MainWindow", u"N2", None))
        self.n4_nr.setText(QCoreApplication.translate("MainWindow", u"N4", None))
        self.n34_nr.setText(QCoreApplication.translate("MainWindow", u"N34", None))
        self.n70_nr.setText(QCoreApplication.translate("MainWindow", u"N70", None))
        self.n1_nr.setText(QCoreApplication.translate("MainWindow", u"N1", None))
        self.n75_nr.setText(QCoreApplication.translate("MainWindow", u"N75", None))
        self.n7_nr.setText(QCoreApplication.translate("MainWindow", u"N7", None))
        self.n66_nr.setText(QCoreApplication.translate("MainWindow", u"N66", None))
        self.groupBox_uhb_nr.setTitle(QCoreApplication.translate("MainWindow", u"UHB", None))
        self.n3_nr_2.setText(QCoreApplication.translate("MainWindow", u"N48", None))
        self.n1_nr_2.setText(QCoreApplication.translate("MainWindow", u"N77", None))
        self.n2_nr_2.setText(QCoreApplication.translate("MainWindow", u"N78", None))
        self.n4_nr_2.setText(QCoreApplication.translate("MainWindow", u"N79", None))
        self.bands_toolBox.setItemText(self.bands_toolBox.indexOf(self.page_nr), QCoreApplication.translate("MainWindow", u"NR", None))
        self.groupBox_lb_lte.setTitle(QCoreApplication.translate("MainWindow", u"LB", None))
        self.b5_lte.setText(QCoreApplication.translate("MainWindow", u"B5", None))
        self.b26_lte.setText(QCoreApplication.translate("MainWindow", u"B26", None))
        self.b8_lte.setText(QCoreApplication.translate("MainWindow", u"B8", None))
#if QT_CONFIG(statustip)
        self.b28_a_lte.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.b28_a_lte.setText(QCoreApplication.translate("MainWindow", u"B28_A", None))
        self.b12_lte.setText(QCoreApplication.translate("MainWindow", u"B12", None))
        self.b28_b_lte.setText(QCoreApplication.translate("MainWindow", u"B28_B", None))
        self.b13_lte.setText(QCoreApplication.translate("MainWindow", u"B13", None))
        self.b29_lte.setText(QCoreApplication.translate("MainWindow", u"B29", None))
        self.b14_lte.setText(QCoreApplication.translate("MainWindow", u"B14", None))
        self.b32_lte.setText(QCoreApplication.translate("MainWindow", u"B32", None))
        self.b17_lte.setText(QCoreApplication.translate("MainWindow", u"B17", None))
        self.b71_lte.setText(QCoreApplication.translate("MainWindow", u"B71", None))
        self.b18_lte.setText(QCoreApplication.translate("MainWindow", u"B18", None))
        self.b19_lte.setText(QCoreApplication.translate("MainWindow", u"B19", None))
        self.b20_lte.setText(QCoreApplication.translate("MainWindow", u"B20", None))
        self.b24_lte.setText(QCoreApplication.translate("MainWindow", u"B24", None))
        self.groupBox_mb_lte.setTitle(QCoreApplication.translate("MainWindow", u"MB", None))
        self.b38_lte.setText(QCoreApplication.translate("MainWindow", u"B38", None))
#if QT_CONFIG(statustip)
        self.b39_lte.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.b39_lte.setText(QCoreApplication.translate("MainWindow", u"B39", None))
        self.b66_lte.setText(QCoreApplication.translate("MainWindow", u"B66", None))
        self.b21_lte.setText(QCoreApplication.translate("MainWindow", u"B21", None))
        self.b7_lte.setText(QCoreApplication.translate("MainWindow", u"B7", None))
        self.b25_lte.setText(QCoreApplication.translate("MainWindow", u"B25", None))
        self.b1_lte.setText(QCoreApplication.translate("MainWindow", u"B1", None))
        self.b2_lte.setText(QCoreApplication.translate("MainWindow", u"B2", None))
        self.b40_lte.setText(QCoreApplication.translate("MainWindow", u"B40", None))
        self.b41_lte.setText(QCoreApplication.translate("MainWindow", u"B41", None))
        self.b30_lte.setText(QCoreApplication.translate("MainWindow", u"B30", None))
        self.b3_lte.setText(QCoreApplication.translate("MainWindow", u"B3", None))
        self.b23_lte.setText(QCoreApplication.translate("MainWindow", u"B23", None))
        self.b4_lte.setText(QCoreApplication.translate("MainWindow", u"B4", None))
        self.groupBox_uhb_lte.setTitle(QCoreApplication.translate("MainWindow", u"UHB", None))
        self.n3_nr_8.setText(QCoreApplication.translate("MainWindow", u"B48", None))
        self.b42_lte.setText(QCoreApplication.translate("MainWindow", u"B42", None))
        self.bands_toolBox.setItemText(self.bands_toolBox.indexOf(self.page_lte), QCoreApplication.translate("MainWindow", u"LTE", None))
        self.groupBox_lb_wcdma.setTitle(QCoreApplication.translate("MainWindow", u"LB", None))
        self.b5_wcdma.setText(QCoreApplication.translate("MainWindow", u"B5", None))
        self.b6_wcdma.setText(QCoreApplication.translate("MainWindow", u"B6", None))
        self.b8_wcdma.setText(QCoreApplication.translate("MainWindow", u"B8", None))
        self.b19_wcdma.setText(QCoreApplication.translate("MainWindow", u"B19", None))
        self.groupBox_mb_wcdma.setTitle(QCoreApplication.translate("MainWindow", u"MB", None))
        self.b2_wcdma.setText(QCoreApplication.translate("MainWindow", u"B2", None))
        self.b4_wcdma.setText(QCoreApplication.translate("MainWindow", u"B4", None))
        self.b1_wcdma.setText(QCoreApplication.translate("MainWindow", u"B1", None))
        self.bands_toolBox.setItemText(self.bands_toolBox.indexOf(self.page_wcdma), QCoreApplication.translate("MainWindow", u"WCDMA", None))
        self.groupBox_lb_gsm.setTitle(QCoreApplication.translate("MainWindow", u"LB", None))
        self.gsm850.setText(QCoreApplication.translate("MainWindow", u"GSM850", None))
        self.gsm900.setText(QCoreApplication.translate("MainWindow", u"GSM900", None))
        self.groupBox_mb_gsm.setTitle(QCoreApplication.translate("MainWindow", u"MB", None))
        self.gsm1900.setText(QCoreApplication.translate("MainWindow", u"GSM1900", None))
        self.gsm1800.setText(QCoreApplication.translate("MainWindow", u"GSM1800", None))
        self.bands_toolBox.setItemText(self.bands_toolBox.indexOf(self.page_gsm), QCoreApplication.translate("MainWindow", u"GSM", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bands), QCoreApplication.translate("MainWindow", u"Bands", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bw), QCoreApplication.translate("MainWindow", u"BW", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mcs_rb), QCoreApplication.translate("MainWindow", u"MCS_RB", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.temp_psu_tab), QCoreApplication.translate("MainWindow", u"Temp_PSU", None))
        self.therm_charge_dis.setText(QCoreApplication.translate("MainWindow", u"Thermal\n"
"Protect\n"
"Charge\n"
"Disable", None))
        self.run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.sync_group.setTitle(QCoreApplication.translate("MainWindow", u"Sync/AS/SRS", None))
        self.sync_path_toolBox.setItemText(self.sync_path_toolBox.indexOf(self.general_sync), QCoreApplication.translate("MainWindow", u"General", None))
        self.sync_path_toolBox.setItemText(self.sync_path_toolBox.indexOf(self.endc_sync), QCoreApplication.translate("MainWindow", u"ENDC", None))
        self.tx_rx_path_group.setTitle(QCoreApplication.translate("MainWindow", u"Tx/Rx Path", None))
        self.txrx_toolBox.setItemText(self.txrx_toolBox.indexOf(self.tx_path), QCoreApplication.translate("MainWindow", u"Tx Path", None))
        self.txrx_toolBox.setItemText(self.txrx_toolBox.indexOf(self.rx_path), QCoreApplication.translate("MainWindow", u"Rx Path", None))
        self.tech_group.setTitle(QCoreApplication.translate("MainWindow", u"Tech", None))
        self.nr_tech.setText(QCoreApplication.translate("MainWindow", u"NR", None))
        self.lte_tech.setText(QCoreApplication.translate("MainWindow", u"LTE", None))
        self.wcdma_tech.setText(QCoreApplication.translate("MainWindow", u"WCDMA", None))
        self.gsm_tech.setText(QCoreApplication.translate("MainWindow", u"GSM", None))
        self.ulca_lte_tech.setText(QCoreApplication.translate("MainWindow", u"ULCA_LTE", None))
        self.channel_group.setTitle(QCoreApplication.translate("MainWindow", u"Channel", None))
        self.lch.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.mch.setText(QCoreApplication.translate("MainWindow", u"M", None))
        self.hch.setText(QCoreApplication.translate("MainWindow", u"H", None))
        self.sync_path_label.setText(QCoreApplication.translate("MainWindow", u"Sync Path", None))
        self.sync_path_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Main", None))
        self.sync_path_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"CA#1", None))
        self.sync_path_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"CA#2", None))
        self.sync_path_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"CA#3", None))

        self.as_path_en.setText(QCoreApplication.translate("MainWindow", u"AS Path", None))
        self.as_path_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.as_path_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))

        self.srs_path_en.setText(QCoreApplication.translate("MainWindow", u"SRS Path", None))
        self.srs_path_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.srs_path_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.srs_path_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.srs_path_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))

        self.sync_path_label_2.setText(QCoreApplication.translate("MainWindow", u"TX Level for 3/4/5G", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Loss_file", None))
    # retranslateUi

