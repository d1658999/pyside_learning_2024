# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mega_v2_5.ui'
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
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpinBox, QStatusBar, QTabWidget, QToolBox,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1491, 790)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1491, 790))
        MainWindow.setMaximumSize(QSize(1491, 790))
        icon = QIcon()
        icon.addFile(u"./Wave.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionLoad_file = QAction(MainWindow)
        self.actionLoad_file.setObjectName(u"actionLoad_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(710, 0, 781, 741))
        self.bands = QWidget()
        self.bands.setObjectName(u"bands")
        self.bands_toolBox = QToolBox(self.bands)
        self.bands_toolBox.setObjectName(u"bands_toolBox")
        self.bands_toolBox.setGeometry(QRect(0, 0, 771, 701))
        self.page_nr = QWidget()
        self.page_nr.setObjectName(u"page_nr")
        self.page_nr.setGeometry(QRect(0, 0, 771, 581))
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
        self.gridLayout_lb_nr = QGridLayout(self.layoutWidget)
        self.gridLayout_lb_nr.setObjectName(u"gridLayout_lb_nr")
        self.gridLayout_lb_nr.setContentsMargins(0, 0, 0, 0)
        self.n24_nr = QCheckBox(self.layoutWidget)
        self.n24_nr.setObjectName(u"n24_nr")

        self.gridLayout_lb_nr.addWidget(self.n24_nr, 6, 0, 1, 1)

        self.n20_nr = QCheckBox(self.layoutWidget)
        self.n20_nr.setObjectName(u"n20_nr")

        self.gridLayout_lb_nr.addWidget(self.n20_nr, 5, 0, 1, 1)

        self.n12_nr = QCheckBox(self.layoutWidget)
        self.n12_nr.setObjectName(u"n12_nr")

        self.gridLayout_lb_nr.addWidget(self.n12_nr, 2, 0, 1, 1)

        self.n28_a_nr = QCheckBox(self.layoutWidget)
        self.n28_a_nr.setObjectName(u"n28_a_nr")
        self.n28_a_nr.setEnabled(False)
        self.n28_a_nr.setCheckable(True)
        self.n28_a_nr.setChecked(False)

        self.gridLayout_lb_nr.addWidget(self.n28_a_nr, 0, 1, 1, 1)

        self.n8_nr = QCheckBox(self.layoutWidget)
        self.n8_nr.setObjectName(u"n8_nr")

        self.gridLayout_lb_nr.addWidget(self.n8_nr, 1, 0, 1, 1)

        self.n13_nr = QCheckBox(self.layoutWidget)
        self.n13_nr.setObjectName(u"n13_nr")

        self.gridLayout_lb_nr.addWidget(self.n13_nr, 3, 0, 1, 1)

        self.n5_nr = QCheckBox(self.layoutWidget)
        self.n5_nr.setObjectName(u"n5_nr")

        self.gridLayout_lb_nr.addWidget(self.n5_nr, 0, 0, 1, 1)

        self.n14_nr = QCheckBox(self.layoutWidget)
        self.n14_nr.setObjectName(u"n14_nr")

        self.gridLayout_lb_nr.addWidget(self.n14_nr, 4, 0, 1, 1)

        self.n26_nr = QCheckBox(self.layoutWidget)
        self.n26_nr.setObjectName(u"n26_nr")

        self.gridLayout_lb_nr.addWidget(self.n26_nr, 7, 0, 1, 1)

        self.n71_nr = QCheckBox(self.layoutWidget)
        self.n71_nr.setObjectName(u"n71_nr")

        self.gridLayout_lb_nr.addWidget(self.n71_nr, 8, 0, 1, 1)

        self.n32_nr = QCheckBox(self.layoutWidget)
        self.n32_nr.setObjectName(u"n32_nr")

        self.gridLayout_lb_nr.addWidget(self.n32_nr, 3, 1, 1, 1)

        self.n29_nr = QCheckBox(self.layoutWidget)
        self.n29_nr.setObjectName(u"n29_nr")

        self.gridLayout_lb_nr.addWidget(self.n29_nr, 2, 1, 1, 1)

        self.n28_b_nr = QCheckBox(self.layoutWidget)
        self.n28_b_nr.setObjectName(u"n28_b_nr")
        self.n28_b_nr.setChecked(False)

        self.gridLayout_lb_nr.addWidget(self.n28_b_nr, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_lb_nr)

        self.groupBox_mb_nr = QGroupBox(self.frame_band_nr)
        self.groupBox_mb_nr.setObjectName(u"groupBox_mb_nr")
        self.layoutWidget1 = QWidget(self.groupBox_mb_nr)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 20, 231, 531))
        self.gridLayout_mb_nr = QGridLayout(self.layoutWidget1)
        self.gridLayout_mb_nr.setObjectName(u"gridLayout_mb_nr")
        self.gridLayout_mb_nr.setContentsMargins(0, 0, 0, 0)
        self.n41_nr = QCheckBox(self.layoutWidget1)
        self.n41_nr.setObjectName(u"n41_nr")

        self.gridLayout_mb_nr.addWidget(self.n41_nr, 3, 1, 1, 1)

        self.n25_nr = QCheckBox(self.layoutWidget1)
        self.n25_nr.setObjectName(u"n25_nr")

        self.gridLayout_mb_nr.addWidget(self.n25_nr, 6, 0, 1, 1)

        self.n76_nr = QCheckBox(self.layoutWidget1)
        self.n76_nr.setObjectName(u"n76_nr")

        self.gridLayout_mb_nr.addWidget(self.n76_nr, 6, 1, 1, 1)

        self.n40_nr = QCheckBox(self.layoutWidget1)
        self.n40_nr.setObjectName(u"n40_nr")
        self.n40_nr.setChecked(False)

        self.gridLayout_mb_nr.addWidget(self.n40_nr, 1, 1, 1, 1)

        self.n30_nr = QCheckBox(self.layoutWidget1)
        self.n30_nr.setObjectName(u"n30_nr")

        self.gridLayout_mb_nr.addWidget(self.n30_nr, 5, 0, 1, 1)

        self.n38_nr = QCheckBox(self.layoutWidget1)
        self.n38_nr.setObjectName(u"n38_nr")

        self.gridLayout_mb_nr.addWidget(self.n38_nr, 2, 1, 1, 1)

        self.n3_nr = QCheckBox(self.layoutWidget1)
        self.n3_nr.setObjectName(u"n3_nr")

        self.gridLayout_mb_nr.addWidget(self.n3_nr, 2, 0, 1, 1)

        self.n255_nr = QCheckBox(self.layoutWidget1)
        self.n255_nr.setObjectName(u"n255_nr")

        self.gridLayout_mb_nr.addWidget(self.n255_nr, 7, 1, 1, 1)

        self.n39_nr = QCheckBox(self.layoutWidget1)
        self.n39_nr.setObjectName(u"n39_nr")
        self.n39_nr.setEnabled(False)
        self.n39_nr.setCheckable(True)
        self.n39_nr.setChecked(False)

        self.gridLayout_mb_nr.addWidget(self.n39_nr, 0, 1, 1, 1)

        self.n256_nr = QCheckBox(self.layoutWidget1)
        self.n256_nr.setObjectName(u"n256_nr")

        self.gridLayout_mb_nr.addWidget(self.n256_nr, 8, 1, 1, 1)

        self.n2_nr = QCheckBox(self.layoutWidget1)
        self.n2_nr.setObjectName(u"n2_nr")

        self.gridLayout_mb_nr.addWidget(self.n2_nr, 1, 0, 1, 1)

        self.n4_nr = QCheckBox(self.layoutWidget1)
        self.n4_nr.setObjectName(u"n4_nr")

        self.gridLayout_mb_nr.addWidget(self.n4_nr, 3, 0, 1, 1)

        self.n34_nr = QCheckBox(self.layoutWidget1)
        self.n34_nr.setObjectName(u"n34_nr")

        self.gridLayout_mb_nr.addWidget(self.n34_nr, 4, 1, 1, 1)

        self.n70_nr = QCheckBox(self.layoutWidget1)
        self.n70_nr.setObjectName(u"n70_nr")

        self.gridLayout_mb_nr.addWidget(self.n70_nr, 8, 0, 1, 1)

        self.n1_nr = QCheckBox(self.layoutWidget1)
        self.n1_nr.setObjectName(u"n1_nr")

        self.gridLayout_mb_nr.addWidget(self.n1_nr, 0, 0, 1, 1)

        self.n75_nr = QCheckBox(self.layoutWidget1)
        self.n75_nr.setObjectName(u"n75_nr")

        self.gridLayout_mb_nr.addWidget(self.n75_nr, 5, 1, 1, 1)

        self.n7_nr = QCheckBox(self.layoutWidget1)
        self.n7_nr.setObjectName(u"n7_nr")

        self.gridLayout_mb_nr.addWidget(self.n7_nr, 4, 0, 1, 1)

        self.n66_nr = QCheckBox(self.layoutWidget1)
        self.n66_nr.setObjectName(u"n66_nr")

        self.gridLayout_mb_nr.addWidget(self.n66_nr, 7, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_mb_nr)

        self.groupBox_uhb_nr = QGroupBox(self.frame_band_nr)
        self.groupBox_uhb_nr.setObjectName(u"groupBox_uhb_nr")
        self.layoutWidget_2 = QWidget(self.groupBox_uhb_nr)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 20, 231, 251))
        self.gridLayout_uhb_nr = QGridLayout(self.layoutWidget_2)
        self.gridLayout_uhb_nr.setObjectName(u"gridLayout_uhb_nr")
        self.gridLayout_uhb_nr.setContentsMargins(0, 0, 0, 0)
        self.n48_nr = QCheckBox(self.layoutWidget_2)
        self.n48_nr.setObjectName(u"n48_nr")

        self.gridLayout_uhb_nr.addWidget(self.n48_nr, 2, 0, 1, 1)

        self.n77_nr = QCheckBox(self.layoutWidget_2)
        self.n77_nr.setObjectName(u"n77_nr")

        self.gridLayout_uhb_nr.addWidget(self.n77_nr, 0, 0, 1, 1)

        self.n78_nr = QCheckBox(self.layoutWidget_2)
        self.n78_nr.setObjectName(u"n78_nr")

        self.gridLayout_uhb_nr.addWidget(self.n78_nr, 1, 0, 1, 1)

        self.n79_nr = QCheckBox(self.layoutWidget_2)
        self.n79_nr.setObjectName(u"n79_nr")

        self.gridLayout_uhb_nr.addWidget(self.n79_nr, 3, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox_uhb_nr)

        self.bands_toolBox.addItem(self.page_nr, u"NR")
        self.page_lte = QWidget()
        self.page_lte.setObjectName(u"page_lte")
        self.page_lte.setGeometry(QRect(0, 0, 771, 581))
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
        self.gridLayout_lb_lte = QGridLayout(self.layoutWidget2)
        self.gridLayout_lb_lte.setObjectName(u"gridLayout_lb_lte")
        self.gridLayout_lb_lte.setContentsMargins(0, 0, 0, 0)
        self.b5_lte = QCheckBox(self.layoutWidget2)
        self.b5_lte.setObjectName(u"b5_lte")

        self.gridLayout_lb_lte.addWidget(self.b5_lte, 0, 0, 1, 1)

        self.b26_lte = QCheckBox(self.layoutWidget2)
        self.b26_lte.setObjectName(u"b26_lte")

        self.gridLayout_lb_lte.addWidget(self.b26_lte, 0, 1, 1, 1)

        self.b8_lte = QCheckBox(self.layoutWidget2)
        self.b8_lte.setObjectName(u"b8_lte")

        self.gridLayout_lb_lte.addWidget(self.b8_lte, 1, 0, 1, 1)

        self.b28_a_lte = QCheckBox(self.layoutWidget2)
        self.b28_a_lte.setObjectName(u"b28_a_lte")
        self.b28_a_lte.setEnabled(False)
        self.b28_a_lte.setCheckable(True)
        self.b28_a_lte.setChecked(False)

        self.gridLayout_lb_lte.addWidget(self.b28_a_lte, 1, 1, 1, 1)

        self.b12_lte = QCheckBox(self.layoutWidget2)
        self.b12_lte.setObjectName(u"b12_lte")

        self.gridLayout_lb_lte.addWidget(self.b12_lte, 2, 0, 1, 1)

        self.b28_b_lte = QCheckBox(self.layoutWidget2)
        self.b28_b_lte.setObjectName(u"b28_b_lte")
        self.b28_b_lte.setChecked(False)

        self.gridLayout_lb_lte.addWidget(self.b28_b_lte, 2, 1, 1, 1)

        self.b13_lte = QCheckBox(self.layoutWidget2)
        self.b13_lte.setObjectName(u"b13_lte")

        self.gridLayout_lb_lte.addWidget(self.b13_lte, 3, 0, 1, 1)

        self.b29_lte = QCheckBox(self.layoutWidget2)
        self.b29_lte.setObjectName(u"b29_lte")

        self.gridLayout_lb_lte.addWidget(self.b29_lte, 3, 1, 1, 1)

        self.b14_lte = QCheckBox(self.layoutWidget2)
        self.b14_lte.setObjectName(u"b14_lte")

        self.gridLayout_lb_lte.addWidget(self.b14_lte, 4, 0, 1, 1)

        self.b32_lte = QCheckBox(self.layoutWidget2)
        self.b32_lte.setObjectName(u"b32_lte")

        self.gridLayout_lb_lte.addWidget(self.b32_lte, 4, 1, 1, 1)

        self.b17_lte = QCheckBox(self.layoutWidget2)
        self.b17_lte.setObjectName(u"b17_lte")

        self.gridLayout_lb_lte.addWidget(self.b17_lte, 5, 0, 1, 1)

        self.b71_lte = QCheckBox(self.layoutWidget2)
        self.b71_lte.setObjectName(u"b71_lte")

        self.gridLayout_lb_lte.addWidget(self.b71_lte, 5, 1, 1, 1)

        self.b18_lte = QCheckBox(self.layoutWidget2)
        self.b18_lte.setObjectName(u"b18_lte")

        self.gridLayout_lb_lte.addWidget(self.b18_lte, 6, 0, 1, 1)

        self.b19_lte = QCheckBox(self.layoutWidget2)
        self.b19_lte.setObjectName(u"b19_lte")

        self.gridLayout_lb_lte.addWidget(self.b19_lte, 7, 0, 1, 1)

        self.b20_lte = QCheckBox(self.layoutWidget2)
        self.b20_lte.setObjectName(u"b20_lte")

        self.gridLayout_lb_lte.addWidget(self.b20_lte, 8, 0, 1, 1)

        self.b24_lte = QCheckBox(self.layoutWidget2)
        self.b24_lte.setObjectName(u"b24_lte")

        self.gridLayout_lb_lte.addWidget(self.b24_lte, 6, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_lb_lte)

        self.groupBox_mb_lte = QGroupBox(self.frame_band_lte)
        self.groupBox_mb_lte.setObjectName(u"groupBox_mb_lte")
        self.layoutWidget_4 = QWidget(self.groupBox_mb_lte)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(10, 20, 231, 531))
        self.gridLayout_mb_lte = QGridLayout(self.layoutWidget_4)
        self.gridLayout_mb_lte.setObjectName(u"gridLayout_mb_lte")
        self.gridLayout_mb_lte.setContentsMargins(0, 0, 0, 0)
        self.b38_lte = QCheckBox(self.layoutWidget_4)
        self.b38_lte.setObjectName(u"b38_lte")

        self.gridLayout_mb_lte.addWidget(self.b38_lte, 2, 1, 1, 1)

        self.b39_lte = QCheckBox(self.layoutWidget_4)
        self.b39_lte.setObjectName(u"b39_lte")
        self.b39_lte.setEnabled(False)
        self.b39_lte.setCheckable(True)
        self.b39_lte.setChecked(False)

        self.gridLayout_mb_lte.addWidget(self.b39_lte, 0, 1, 1, 1)

        self.b66_lte = QCheckBox(self.layoutWidget_4)
        self.b66_lte.setObjectName(u"b66_lte")

        self.gridLayout_mb_lte.addWidget(self.b66_lte, 7, 0, 1, 1)

        self.b21_lte = QCheckBox(self.layoutWidget_4)
        self.b21_lte.setObjectName(u"b21_lte")

        self.gridLayout_mb_lte.addWidget(self.b21_lte, 8, 0, 1, 1)

        self.b7_lte = QCheckBox(self.layoutWidget_4)
        self.b7_lte.setObjectName(u"b7_lte")

        self.gridLayout_mb_lte.addWidget(self.b7_lte, 4, 0, 1, 1)

        self.b25_lte = QCheckBox(self.layoutWidget_4)
        self.b25_lte.setObjectName(u"b25_lte")

        self.gridLayout_mb_lte.addWidget(self.b25_lte, 6, 0, 1, 1)

        self.b1_lte = QCheckBox(self.layoutWidget_4)
        self.b1_lte.setObjectName(u"b1_lte")

        self.gridLayout_mb_lte.addWidget(self.b1_lte, 0, 0, 1, 1)

        self.b2_lte = QCheckBox(self.layoutWidget_4)
        self.b2_lte.setObjectName(u"b2_lte")

        self.gridLayout_mb_lte.addWidget(self.b2_lte, 1, 0, 1, 1)

        self.b40_lte = QCheckBox(self.layoutWidget_4)
        self.b40_lte.setObjectName(u"b40_lte")
        self.b40_lte.setChecked(False)

        self.gridLayout_mb_lte.addWidget(self.b40_lte, 1, 1, 1, 1)

        self.b41_lte = QCheckBox(self.layoutWidget_4)
        self.b41_lte.setObjectName(u"b41_lte")

        self.gridLayout_mb_lte.addWidget(self.b41_lte, 3, 1, 1, 1)

        self.b30_lte = QCheckBox(self.layoutWidget_4)
        self.b30_lte.setObjectName(u"b30_lte")

        self.gridLayout_mb_lte.addWidget(self.b30_lte, 5, 0, 1, 1)

        self.b3_lte = QCheckBox(self.layoutWidget_4)
        self.b3_lte.setObjectName(u"b3_lte")

        self.gridLayout_mb_lte.addWidget(self.b3_lte, 2, 0, 1, 1)

        self.b23_lte = QCheckBox(self.layoutWidget_4)
        self.b23_lte.setObjectName(u"b23_lte")

        self.gridLayout_mb_lte.addWidget(self.b23_lte, 4, 1, 1, 1)

        self.b4_lte = QCheckBox(self.layoutWidget_4)
        self.b4_lte.setObjectName(u"b4_lte")

        self.gridLayout_mb_lte.addWidget(self.b4_lte, 3, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_mb_lte)

        self.groupBox_uhb_lte = QGroupBox(self.frame_band_lte)
        self.groupBox_uhb_lte.setObjectName(u"groupBox_uhb_lte")
        self.layoutWidget_5 = QWidget(self.groupBox_uhb_lte)
        self.layoutWidget_5.setObjectName(u"layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(10, 20, 231, 141))
        self.gridLayout_uhb_lte = QGridLayout(self.layoutWidget_5)
        self.gridLayout_uhb_lte.setObjectName(u"gridLayout_uhb_lte")
        self.gridLayout_uhb_lte.setContentsMargins(0, 0, 0, 0)
        self.b48_lte = QCheckBox(self.layoutWidget_5)
        self.b48_lte.setObjectName(u"b48_lte")

        self.gridLayout_uhb_lte.addWidget(self.b48_lte, 1, 0, 1, 1)

        self.b42_lte = QCheckBox(self.layoutWidget_5)
        self.b42_lte.setObjectName(u"b42_lte")

        self.gridLayout_uhb_lte.addWidget(self.b42_lte, 0, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.groupBox_uhb_lte)

        self.bands_toolBox.addItem(self.page_lte, u"LTE")
        self.page_wcdma = QWidget()
        self.page_wcdma.setObjectName(u"page_wcdma")
        self.page_wcdma.setGeometry(QRect(0, 0, 771, 581))
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
        self.gridLayout_lb_wcdma = QGridLayout(self.layoutWidget_3)
        self.gridLayout_lb_wcdma.setObjectName(u"gridLayout_lb_wcdma")
        self.gridLayout_lb_wcdma.setContentsMargins(0, 0, 0, 0)
        self.b5_wcdma = QCheckBox(self.layoutWidget_3)
        self.b5_wcdma.setObjectName(u"b5_wcdma")

        self.gridLayout_lb_wcdma.addWidget(self.b5_wcdma, 0, 0, 1, 1)

        self.b6_wcdma = QCheckBox(self.layoutWidget_3)
        self.b6_wcdma.setObjectName(u"b6_wcdma")

        self.gridLayout_lb_wcdma.addWidget(self.b6_wcdma, 2, 0, 1, 1)

        self.b8_wcdma = QCheckBox(self.layoutWidget_3)
        self.b8_wcdma.setObjectName(u"b8_wcdma")

        self.gridLayout_lb_wcdma.addWidget(self.b8_wcdma, 1, 0, 1, 1)

        self.b19_wcdma = QCheckBox(self.layoutWidget_3)
        self.b19_wcdma.setObjectName(u"b19_wcdma")

        self.gridLayout_lb_wcdma.addWidget(self.b19_wcdma, 3, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_lb_wcdma)

        self.groupBox_mb_wcdma = QGroupBox(self.frame_band_wcdma)
        self.groupBox_mb_wcdma.setObjectName(u"groupBox_mb_wcdma")
        self.layoutWidget_6 = QWidget(self.groupBox_mb_wcdma)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(10, 20, 341, 191))
        self.gridLayout_mb_wcdma = QGridLayout(self.layoutWidget_6)
        self.gridLayout_mb_wcdma.setObjectName(u"gridLayout_mb_wcdma")
        self.gridLayout_mb_wcdma.setContentsMargins(0, 0, 0, 0)
        self.b2_wcdma = QCheckBox(self.layoutWidget_6)
        self.b2_wcdma.setObjectName(u"b2_wcdma")

        self.gridLayout_mb_wcdma.addWidget(self.b2_wcdma, 1, 0, 1, 1)

        self.b4_wcdma = QCheckBox(self.layoutWidget_6)
        self.b4_wcdma.setObjectName(u"b4_wcdma")

        self.gridLayout_mb_wcdma.addWidget(self.b4_wcdma, 2, 0, 1, 1)

        self.b1_wcdma = QCheckBox(self.layoutWidget_6)
        self.b1_wcdma.setObjectName(u"b1_wcdma")

        self.gridLayout_mb_wcdma.addWidget(self.b1_wcdma, 0, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_mb_wcdma)

        self.bands_toolBox.addItem(self.page_wcdma, u"WCDMA")
        self.page_gsm = QWidget()
        self.page_gsm.setObjectName(u"page_gsm")
        self.page_gsm.setGeometry(QRect(0, 0, 771, 581))
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
        self.gridLayout_lb_gsm = QGridLayout(self.layoutWidget_7)
        self.gridLayout_lb_gsm.setObjectName(u"gridLayout_lb_gsm")
        self.gridLayout_lb_gsm.setContentsMargins(0, 0, 0, 0)
        self.gsm850 = QCheckBox(self.layoutWidget_7)
        self.gsm850.setObjectName(u"gsm850")

        self.gridLayout_lb_gsm.addWidget(self.gsm850, 0, 0, 1, 1)

        self.gsm900 = QCheckBox(self.layoutWidget_7)
        self.gsm900.setObjectName(u"gsm900")

        self.gridLayout_lb_gsm.addWidget(self.gsm900, 1, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.groupBox_lb_gsm)

        self.groupBox_mb_gsm = QGroupBox(self.frame_band_gsm)
        self.groupBox_mb_gsm.setObjectName(u"groupBox_mb_gsm")
        self.layoutWidget_8 = QWidget(self.groupBox_mb_gsm)
        self.layoutWidget_8.setObjectName(u"layoutWidget_8")
        self.layoutWidget_8.setGeometry(QRect(10, 20, 341, 121))
        self.gridLayout_mb_gsm = QGridLayout(self.layoutWidget_8)
        self.gridLayout_mb_gsm.setObjectName(u"gridLayout_mb_gsm")
        self.gridLayout_mb_gsm.setContentsMargins(0, 0, 0, 0)
        self.gsm1900 = QCheckBox(self.layoutWidget_8)
        self.gsm1900.setObjectName(u"gsm1900")

        self.gridLayout_mb_gsm.addWidget(self.gsm1900, 1, 0, 1, 1)

        self.gsm1800 = QCheckBox(self.layoutWidget_8)
        self.gsm1800.setObjectName(u"gsm1800")

        self.gridLayout_mb_gsm.addWidget(self.gsm1800, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.groupBox_mb_gsm)

        self.bands_toolBox.addItem(self.page_gsm, u"GSM")
        self.tabWidget.addTab(self.bands, "")
        self.bw = QWidget()
        self.bw.setObjectName(u"bw")
        self.tabWidget.addTab(self.bw, "")
        self.mcs_rb = QWidget()
        self.mcs_rb.setObjectName(u"mcs_rb")
        self.mcs_rb.setEnabled(False)
        self.tabWidget.addTab(self.mcs_rb, "")
        self.temp_psu_tab = QWidget()
        self.temp_psu_tab.setObjectName(u"temp_psu_tab")
        self.tabWidget.addTab(self.temp_psu_tab, "")
        self.frame_button = QFrame(self.centralwidget)
        self.frame_button.setObjectName(u"frame_button")
        self.frame_button.setGeometry(QRect(0, 430, 151, 311))
        sizePolicy1.setHeightForWidth(self.frame_button.sizePolicy().hasHeightForWidth())
        self.frame_button.setSizePolicy(sizePolicy1)
        self.frame_button.setFrameShape(QFrame.StyledPanel)
        self.frame_button.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_button)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.therm_charge_dis_button = QPushButton(self.frame_button)
        self.therm_charge_dis_button.setObjectName(u"therm_charge_dis_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.therm_charge_dis_button.sizePolicy().hasHeightForWidth())
        self.therm_charge_dis_button.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.therm_charge_dis_button)

        self.run_button = QPushButton(self.frame_button)
        self.run_button.setObjectName(u"run_button")
        sizePolicy2.setHeightForWidth(self.run_button.sizePolicy().hasHeightForWidth())
        self.run_button.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.run_button)

        self.stop_button = QPushButton(self.frame_button)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy2.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.stop_button)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout.setStretch(2, 2)
        self.layoutWidget_10 = QWidget(self.centralwidget)
        self.layoutWidget_10.setObjectName(u"layoutWidget_10")
        self.layoutWidget_10.setGeometry(QRect(440, 0, 151, 741))
        self.verticalLayout_path_ue = QVBoxLayout(self.layoutWidget_10)
        self.verticalLayout_path_ue.setObjectName(u"verticalLayout_path_ue")
        self.verticalLayout_path_ue.setContentsMargins(0, 0, 0, 0)
        self.tx_rx_path_group = QGroupBox(self.layoutWidget_10)
        self.tx_rx_path_group.setObjectName(u"tx_rx_path_group")
        self.txrx_path_toolBox = QToolBox(self.tx_rx_path_group)
        self.txrx_path_toolBox.setObjectName(u"txrx_path_toolBox")
        self.txrx_path_toolBox.setGeometry(QRect(10, 20, 131, 261))
        self.tx_path = QWidget()
        self.tx_path.setObjectName(u"tx_path")
        self.tx_path.setGeometry(QRect(0, 0, 131, 201))
        self.layoutWidget_14 = QWidget(self.tx_path)
        self.layoutWidget_14.setObjectName(u"layoutWidget_14")
        self.layoutWidget_14.setGeometry(QRect(0, 0, 101, 74))
        self.verticalLayout_tx_path = QVBoxLayout(self.layoutWidget_14)
        self.verticalLayout_tx_path.setObjectName(u"verticalLayout_tx_path")
        self.verticalLayout_tx_path.setContentsMargins(0, 0, 0, 0)
        self.tx1 = QCheckBox(self.layoutWidget_14)
        self.tx1.setObjectName(u"tx1")

        self.verticalLayout_tx_path.addWidget(self.tx1)

        self.tx2 = QCheckBox(self.layoutWidget_14)
        self.tx2.setObjectName(u"tx2")

        self.verticalLayout_tx_path.addWidget(self.tx2)

        self.ulmimo = QCheckBox(self.layoutWidget_14)
        self.ulmimo.setObjectName(u"ulmimo")

        self.verticalLayout_tx_path.addWidget(self.ulmimo)

        self.txrx_path_toolBox.addItem(self.tx_path, u"Tx Path")
        self.rx_path = QWidget()
        self.rx_path.setObjectName(u"rx_path")
        self.rx_path.setGeometry(QRect(0, 0, 131, 201))
        self.layoutWidget_13 = QWidget(self.rx_path)
        self.layoutWidget_13.setObjectName(u"layoutWidget_13")
        self.layoutWidget_13.setGeometry(QRect(0, 0, 101, 178))
        self.verticalLayout_rx_path = QVBoxLayout(self.layoutWidget_13)
        self.verticalLayout_rx_path.setObjectName(u"verticalLayout_rx_path")
        self.verticalLayout_rx_path.setContentsMargins(0, 0, 0, 0)
        self.rx0 = QCheckBox(self.layoutWidget_13)
        self.rx0.setObjectName(u"rx0")

        self.verticalLayout_rx_path.addWidget(self.rx0)

        self.rx1 = QCheckBox(self.layoutWidget_13)
        self.rx1.setObjectName(u"rx1")

        self.verticalLayout_rx_path.addWidget(self.rx1)

        self.rx2 = QCheckBox(self.layoutWidget_13)
        self.rx2.setObjectName(u"rx2")

        self.verticalLayout_rx_path.addWidget(self.rx2)

        self.rx3 = QCheckBox(self.layoutWidget_13)
        self.rx3.setObjectName(u"rx3")

        self.verticalLayout_rx_path.addWidget(self.rx3)

        self.rx0_rx1 = QCheckBox(self.layoutWidget_13)
        self.rx0_rx1.setObjectName(u"rx0_rx1")

        self.verticalLayout_rx_path.addWidget(self.rx0_rx1)

        self.rx2_rx3 = QCheckBox(self.layoutWidget_13)
        self.rx2_rx3.setObjectName(u"rx2_rx3")

        self.verticalLayout_rx_path.addWidget(self.rx2_rx3)

        self.rx_all_path = QCheckBox(self.layoutWidget_13)
        self.rx_all_path.setObjectName(u"rx_all_path")

        self.verticalLayout_rx_path.addWidget(self.rx_all_path)

        self.txrx_path_toolBox.addItem(self.rx_path, u"Rx Path")

        self.verticalLayout_path_ue.addWidget(self.tx_rx_path_group)

        self.ue_power = QGroupBox(self.layoutWidget_10)
        self.ue_power.setObjectName(u"ue_power")
        self.layoutWidget_17 = QWidget(self.ue_power)
        self.layoutWidget_17.setObjectName(u"layoutWidget_17")
        self.layoutWidget_17.setGeometry(QRect(10, 30, 131, 48))
        self.verticalLayout_ue = QVBoxLayout(self.layoutWidget_17)
        self.verticalLayout_ue.setObjectName(u"verticalLayout_ue")
        self.verticalLayout_ue.setContentsMargins(0, 0, 0, 0)
        self.ue_txmax = QCheckBox(self.layoutWidget_17)
        self.ue_txmax.setObjectName(u"ue_txmax")
        self.ue_txmax.setChecked(True)

        self.verticalLayout_ue.addWidget(self.ue_txmax)

        self.ue_txlow = QCheckBox(self.layoutWidget_17)
        self.ue_txlow.setObjectName(u"ue_txlow")
        self.ue_txlow.setChecked(True)

        self.verticalLayout_ue.addWidget(self.ue_txlow)


        self.verticalLayout_path_ue.addWidget(self.ue_power)

        self.verticalLayout_path_ue.setStretch(0, 4)
        self.verticalLayout_path_ue.setStretch(1, 1)
        self.layoutWidget3 = QWidget(self.centralwidget)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(594, 0, 111, 741))
        self.verticalLayout_tech_ch = QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_tech_ch.setObjectName(u"verticalLayout_tech_ch")
        self.verticalLayout_tech_ch.setContentsMargins(0, 0, 0, 0)
        self.tech_group = QGroupBox(self.layoutWidget3)
        self.tech_group.setObjectName(u"tech_group")
        self.layoutWidget_9 = QWidget(self.tech_group)
        self.layoutWidget_9.setObjectName(u"layoutWidget_9")
        self.layoutWidget_9.setGeometry(QRect(10, 30, 91, 126))
        self.verticalLayout_tech = QVBoxLayout(self.layoutWidget_9)
        self.verticalLayout_tech.setObjectName(u"verticalLayout_tech")
        self.verticalLayout_tech.setContentsMargins(0, 0, 0, 0)
        self.nr_tech = QCheckBox(self.layoutWidget_9)
        self.nr_tech.setObjectName(u"nr_tech")

        self.verticalLayout_tech.addWidget(self.nr_tech)

        self.lte_tech = QCheckBox(self.layoutWidget_9)
        self.lte_tech.setObjectName(u"lte_tech")

        self.verticalLayout_tech.addWidget(self.lte_tech)

        self.wcdma_tech = QCheckBox(self.layoutWidget_9)
        self.wcdma_tech.setObjectName(u"wcdma_tech")

        self.verticalLayout_tech.addWidget(self.wcdma_tech)

        self.gsm_tech = QCheckBox(self.layoutWidget_9)
        self.gsm_tech.setObjectName(u"gsm_tech")

        self.verticalLayout_tech.addWidget(self.gsm_tech)

        self.ulca_lte_tech = QCheckBox(self.layoutWidget_9)
        self.ulca_lte_tech.setObjectName(u"ulca_lte_tech")

        self.verticalLayout_tech.addWidget(self.ulca_lte_tech)


        self.verticalLayout_tech_ch.addWidget(self.tech_group)

        self.channel_group = QGroupBox(self.layoutWidget3)
        self.channel_group.setObjectName(u"channel_group")
        self.layoutWidget4 = QWidget(self.channel_group)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(10, 30, 91, 81))
        self.verticalLayout_ch = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_ch.setObjectName(u"verticalLayout_ch")
        self.verticalLayout_ch.setContentsMargins(0, 0, 0, 0)
        self.lch = QCheckBox(self.layoutWidget4)
        self.lch.setObjectName(u"lch")

        self.verticalLayout_ch.addWidget(self.lch)

        self.mch = QCheckBox(self.layoutWidget4)
        self.mch.setObjectName(u"mch")

        self.verticalLayout_ch.addWidget(self.mch)

        self.hch = QCheckBox(self.layoutWidget4)
        self.hch.setObjectName(u"hch")

        self.verticalLayout_ch.addWidget(self.hch)


        self.verticalLayout_tech_ch.addWidget(self.channel_group)

        self.test_items_groupBox = QGroupBox(self.centralwidget)
        self.test_items_groupBox.setObjectName(u"test_items_groupBox")
        self.test_items_groupBox.setGeometry(QRect(150, 0, 147, 741))
        self.test_items_toolBox = QToolBox(self.test_items_groupBox)
        self.test_items_toolBox.setObjectName(u"test_items_toolBox")
        self.test_items_toolBox.setGeometry(QRect(10, 20, 131, 441))
        self.non_sig = QWidget()
        self.non_sig.setObjectName(u"non_sig")
        self.non_sig.setGeometry(QRect(0, 0, 131, 381))
        self.layoutWidget_11 = QWidget(self.non_sig)
        self.layoutWidget_11.setObjectName(u"layoutWidget_11")
        self.layoutWidget_11.setGeometry(QRect(0, 0, 131, 381))
        self.verticalLayout_ns = QVBoxLayout(self.layoutWidget_11)
        self.verticalLayout_ns.setObjectName(u"verticalLayout_ns")
        self.verticalLayout_ns.setContentsMargins(0, 0, 0, 0)
        self.tx_lmh_ns = QCheckBox(self.layoutWidget_11)
        self.tx_lmh_ns.setObjectName(u"tx_lmh_ns")

        self.verticalLayout_ns.addWidget(self.tx_lmh_ns)

        self.tx_level_sweep_ns = QCheckBox(self.layoutWidget_11)
        self.tx_level_sweep_ns.setObjectName(u"tx_level_sweep_ns")

        self.verticalLayout_ns.addWidget(self.tx_level_sweep_ns)

        self.tx_freq_sweep_ns = QCheckBox(self.layoutWidget_11)
        self.tx_freq_sweep_ns.setObjectName(u"tx_freq_sweep_ns")

        self.verticalLayout_ns.addWidget(self.tx_freq_sweep_ns)

        self.tx_1rb_sweep_ns = QCheckBox(self.layoutWidget_11)
        self.tx_1rb_sweep_ns.setObjectName(u"tx_1rb_sweep_ns")

        self.verticalLayout_ns.addWidget(self.tx_1rb_sweep_ns)

        self.tx_fcc_power_ns = QCheckBox(self.layoutWidget_11)
        self.tx_fcc_power_ns.setObjectName(u"tx_fcc_power_ns")

        self.verticalLayout_ns.addWidget(self.tx_fcc_power_ns)

        self.tx_ce_power_ns = QCheckBox(self.layoutWidget_11)
        self.tx_ce_power_ns.setObjectName(u"tx_ce_power_ns")

        self.verticalLayout_ns.addWidget(self.tx_ce_power_ns)

        self.tx_harmonics_ns = QCheckBox(self.layoutWidget_11)
        self.tx_harmonics_ns.setObjectName(u"tx_harmonics_ns")

        self.verticalLayout_ns.addWidget(self.tx_harmonics_ns)

        self.tx_cbe_ns = QCheckBox(self.layoutWidget_11)
        self.tx_cbe_ns.setObjectName(u"tx_cbe_ns")

        self.verticalLayout_ns.addWidget(self.tx_cbe_ns)

        self.tx_ulca_lte_ns = QCheckBox(self.layoutWidget_11)
        self.tx_ulca_lte_ns.setObjectName(u"tx_ulca_lte_ns")

        self.verticalLayout_ns.addWidget(self.tx_ulca_lte_ns)

        self.tx_ulca_lte_cbe_ns = QCheckBox(self.layoutWidget_11)
        self.tx_ulca_lte_cbe_ns.setObjectName(u"tx_ulca_lte_cbe_ns")

        self.verticalLayout_ns.addWidget(self.tx_ulca_lte_cbe_ns)

        self.rx_normal_ns = QCheckBox(self.layoutWidget_11)
        self.rx_normal_ns.setObjectName(u"rx_normal_ns")

        self.verticalLayout_ns.addWidget(self.rx_normal_ns)

        self.rx_quick_ns = QCheckBox(self.layoutWidget_11)
        self.rx_quick_ns.setObjectName(u"rx_quick_ns")

        self.verticalLayout_ns.addWidget(self.rx_quick_ns)

        self.rx_endc_desense_ns = QCheckBox(self.layoutWidget_11)
        self.rx_endc_desense_ns.setObjectName(u"rx_endc_desense_ns")

        self.verticalLayout_ns.addWidget(self.rx_endc_desense_ns)

        self.test_items_toolBox.addItem(self.non_sig, u"Non-sig")
        self.sig = QWidget()
        self.sig.setObjectName(u"sig")
        self.sig.setGeometry(QRect(0, 0, 131, 381))
        self.layoutWidget_12 = QWidget(self.sig)
        self.layoutWidget_12.setObjectName(u"layoutWidget_12")
        self.layoutWidget_12.setGeometry(QRect(0, 0, 131, 74))
        self.verticalLayout_sig = QVBoxLayout(self.layoutWidget_12)
        self.verticalLayout_sig.setObjectName(u"verticalLayout_sig")
        self.verticalLayout_sig.setContentsMargins(0, 0, 0, 0)
        self.tx_lmh_s = QCheckBox(self.layoutWidget_12)
        self.tx_lmh_s.setObjectName(u"tx_lmh_s")

        self.verticalLayout_sig.addWidget(self.tx_lmh_s)

        self.rx_normal_s = QCheckBox(self.layoutWidget_12)
        self.rx_normal_s.setObjectName(u"rx_normal_s")

        self.verticalLayout_sig.addWidget(self.rx_normal_s)

        self.rxs_sweep_s = QCheckBox(self.layoutWidget_12)
        self.rxs_sweep_s.setObjectName(u"rxs_sweep_s")

        self.verticalLayout_sig.addWidget(self.rxs_sweep_s)

        self.test_items_toolBox.addItem(self.sig, u"Sig")
        self.level_sweep_groupBox = QGroupBox(self.centralwidget)
        self.level_sweep_groupBox.setObjectName(u"level_sweep_groupBox")
        self.level_sweep_groupBox.setGeometry(QRect(300, 420, 137, 141))
        self.verticalLayout_9 = QVBoxLayout(self.level_sweep_groupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.start_level_label = QLabel(self.level_sweep_groupBox)
        self.start_level_label.setObjectName(u"start_level_label")
        sizePolicy1.setHeightForWidth(self.start_level_label.sizePolicy().hasHeightForWidth())
        self.start_level_label.setSizePolicy(sizePolicy1)
        self.start_level_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_9.addWidget(self.start_level_label)

        self.level_sweep_start_spinBox = QSpinBox(self.level_sweep_groupBox)
        self.level_sweep_start_spinBox.setObjectName(u"level_sweep_start_spinBox")
        self.level_sweep_start_spinBox.setAlignment(Qt.AlignCenter)
        self.level_sweep_start_spinBox.setMinimum(-30)
        self.level_sweep_start_spinBox.setMaximum(30)
        self.level_sweep_start_spinBox.setValue(-20)

        self.verticalLayout_9.addWidget(self.level_sweep_start_spinBox)

        self.stop_level_label = QLabel(self.level_sweep_groupBox)
        self.stop_level_label.setObjectName(u"stop_level_label")
        self.stop_level_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_9.addWidget(self.stop_level_label)

        self.level_stop_spinBox = QSpinBox(self.level_sweep_groupBox)
        self.level_stop_spinBox.setObjectName(u"level_stop_spinBox")
        self.level_stop_spinBox.setAlignment(Qt.AlignCenter)
        self.level_stop_spinBox.setMinimum(-30)
        self.level_stop_spinBox.setMaximum(30)
        self.level_stop_spinBox.setValue(26)

        self.verticalLayout_9.addWidget(self.level_stop_spinBox)

        self.freq_sweep_groupBox = QGroupBox(self.centralwidget)
        self.freq_sweep_groupBox.setObjectName(u"freq_sweep_groupBox")
        self.freq_sweep_groupBox.setGeometry(QRect(300, 560, 137, 181))
        self.verticalLayout_12 = QVBoxLayout(self.freq_sweep_groupBox)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.freq_sweep_step_label = QLabel(self.freq_sweep_groupBox)
        self.freq_sweep_step_label.setObjectName(u"freq_sweep_step_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.freq_sweep_step_label.sizePolicy().hasHeightForWidth())
        self.freq_sweep_step_label.setSizePolicy(sizePolicy3)
        self.freq_sweep_step_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_12.addWidget(self.freq_sweep_step_label)

        self.freq_sweep_step = QLineEdit(self.freq_sweep_groupBox)
        self.freq_sweep_step.setObjectName(u"freq_sweep_step")
        self.freq_sweep_step.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.freq_sweep_step)

        self.freq_sweep_start_label = QLabel(self.freq_sweep_groupBox)
        self.freq_sweep_start_label.setObjectName(u"freq_sweep_start_label")
        sizePolicy3.setHeightForWidth(self.freq_sweep_start_label.sizePolicy().hasHeightForWidth())
        self.freq_sweep_start_label.setSizePolicy(sizePolicy3)
        self.freq_sweep_start_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_12.addWidget(self.freq_sweep_start_label)

        self.freq_sweep_start = QLineEdit(self.freq_sweep_groupBox)
        self.freq_sweep_start.setObjectName(u"freq_sweep_start")
        self.freq_sweep_start.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.freq_sweep_start)

        self.freq_sweep_stop_label = QLabel(self.freq_sweep_groupBox)
        self.freq_sweep_stop_label.setObjectName(u"freq_sweep_stop_label")
        sizePolicy3.setHeightForWidth(self.freq_sweep_stop_label.sizePolicy().hasHeightForWidth())
        self.freq_sweep_stop_label.setSizePolicy(sizePolicy3)
        self.freq_sweep_stop_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_12.addWidget(self.freq_sweep_stop_label)

        self.freq_sweep_stop = QLineEdit(self.freq_sweep_groupBox)
        self.freq_sweep_stop.setObjectName(u"freq_sweep_stop")
        self.freq_sweep_stop.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.freq_sweep_stop)

        self.sync_group = QGroupBox(self.centralwidget)
        self.sync_group.setObjectName(u"sync_group")
        self.sync_group.setGeometry(QRect(300, 0, 137, 421))
        self.sync_path_toolBox = QToolBox(self.sync_group)
        self.sync_path_toolBox.setObjectName(u"sync_path_toolBox")
        self.sync_path_toolBox.setGeometry(QRect(10, 20, 121, 391))
        self.general_sync = QWidget()
        self.general_sync.setObjectName(u"general_sync")
        self.general_sync.setGeometry(QRect(0, 0, 121, 331))
        self.layoutWidget5 = QWidget(self.general_sync)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(0, -1, 121, 331))
        self.verticalLayout_genre = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_genre.setObjectName(u"verticalLayout_genre")
        self.verticalLayout_genre.setContentsMargins(0, 0, 0, 0)
        self.sync_path_label = QLabel(self.layoutWidget5)
        self.sync_path_label.setObjectName(u"sync_path_label")
        self.sync_path_label.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.sync_path_label.sizePolicy().hasHeightForWidth())
        self.sync_path_label.setSizePolicy(sizePolicy3)
        self.sync_path_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_genre.addWidget(self.sync_path_label)

        self.sync_path_comboBox = QComboBox(self.layoutWidget5)
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.addItem("")
        self.sync_path_comboBox.setObjectName(u"sync_path_comboBox")
        self.sync_path_comboBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_genre.addWidget(self.sync_path_comboBox)

        self.as_path_en = QCheckBox(self.layoutWidget5)
        self.as_path_en.setObjectName(u"as_path_en")

        self.verticalLayout_genre.addWidget(self.as_path_en)

        self.as_path_comboBox = QComboBox(self.layoutWidget5)
        self.as_path_comboBox.addItem("")
        self.as_path_comboBox.addItem("")
        self.as_path_comboBox.setObjectName(u"as_path_comboBox")
        self.as_path_comboBox.setEnabled(False)
        self.as_path_comboBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_genre.addWidget(self.as_path_comboBox)

        self.srs_path_en = QCheckBox(self.layoutWidget5)
        self.srs_path_en.setObjectName(u"srs_path_en")
        self.srs_path_en.setChecked(False)

        self.verticalLayout_genre.addWidget(self.srs_path_en)

        self.srs_path_comboBox = QComboBox(self.layoutWidget5)
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.addItem("")
        self.srs_path_comboBox.setObjectName(u"srs_path_comboBox")
        self.srs_path_comboBox.setEnabled(False)
        self.srs_path_comboBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_genre.addWidget(self.srs_path_comboBox)

        self.tx_level_nlw_label = QLabel(self.layoutWidget5)
        self.tx_level_nlw_label.setObjectName(u"tx_level_nlw_label")
        sizePolicy3.setHeightForWidth(self.tx_level_nlw_label.sizePolicy().hasHeightForWidth())
        self.tx_level_nlw_label.setSizePolicy(sizePolicy3)
        self.tx_level_nlw_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_genre.addWidget(self.tx_level_nlw_label)

        self.tx_level_spinBox = QSpinBox(self.layoutWidget5)
        self.tx_level_spinBox.setObjectName(u"tx_level_spinBox")
        self.tx_level_spinBox.setAlignment(Qt.AlignCenter)
        self.tx_level_spinBox.setMaximum(30)
        self.tx_level_spinBox.setValue(26)

        self.verticalLayout_genre.addWidget(self.tx_level_spinBox)

        self.pcl_lb_label = QLabel(self.layoutWidget5)
        self.pcl_lb_label.setObjectName(u"pcl_lb_label")
        sizePolicy3.setHeightForWidth(self.pcl_lb_label.sizePolicy().hasHeightForWidth())
        self.pcl_lb_label.setSizePolicy(sizePolicy3)
        self.pcl_lb_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_genre.addWidget(self.pcl_lb_label)

        self.pcl_lb_level_combo = QComboBox(self.layoutWidget5)
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.addItem("")
        self.pcl_lb_level_combo.setObjectName(u"pcl_lb_level_combo")
        self.pcl_lb_level_combo.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_genre.addWidget(self.pcl_lb_level_combo)

        self.pcl_mb_label = QLabel(self.layoutWidget5)
        self.pcl_mb_label.setObjectName(u"pcl_mb_label")
        sizePolicy3.setHeightForWidth(self.pcl_mb_label.sizePolicy().hasHeightForWidth())
        self.pcl_mb_label.setSizePolicy(sizePolicy3)
        self.pcl_mb_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_genre.addWidget(self.pcl_mb_label)

        self.pcl_mb_level_combo = QComboBox(self.layoutWidget5)
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.addItem("")
        self.pcl_mb_level_combo.setObjectName(u"pcl_mb_level_combo")
        self.pcl_mb_level_combo.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_genre.addWidget(self.pcl_mb_level_combo)

        self.horizontalLayout_gsm_mod = QHBoxLayout()
        self.horizontalLayout_gsm_mod.setObjectName(u"horizontalLayout_gsm_mod")
        self.gmsk_radioButton = QRadioButton(self.layoutWidget5)
        self.gmsk_radioButton.setObjectName(u"gmsk_radioButton")
        self.gmsk_radioButton.setChecked(True)

        self.horizontalLayout_gsm_mod.addWidget(self.gmsk_radioButton)

        self.epsk_radioButton = QRadioButton(self.layoutWidget5)
        self.epsk_radioButton.setObjectName(u"epsk_radioButton")
        self.epsk_radioButton.setEnabled(True)
        self.epsk_radioButton.setCheckable(True)

        self.horizontalLayout_gsm_mod.addWidget(self.epsk_radioButton)


        self.verticalLayout_genre.addLayout(self.horizontalLayout_gsm_mod)

        self.sync_path_toolBox.addItem(self.general_sync, u"General")
        self.endc_sync = QWidget()
        self.endc_sync.setObjectName(u"endc_sync")
        self.endc_sync.setGeometry(QRect(0, 0, 121, 331))
        self.layoutWidget_18 = QWidget(self.endc_sync)
        self.layoutWidget_18.setObjectName(u"layoutWidget_18")
        self.layoutWidget_18.setGeometry(QRect(0, 0, 121, 221))
        self.verticalLayout_endc = QVBoxLayout(self.layoutWidget_18)
        self.verticalLayout_endc.setObjectName(u"verticalLayout_endc")
        self.verticalLayout_endc.setContentsMargins(0, 0, 0, 0)
        self.sync_path_label_endc = QLabel(self.layoutWidget_18)
        self.sync_path_label_endc.setObjectName(u"sync_path_label_endc")
        self.sync_path_label_endc.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.sync_path_label_endc.sizePolicy().hasHeightForWidth())
        self.sync_path_label_endc.setSizePolicy(sizePolicy3)
        self.sync_path_label_endc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_endc.addWidget(self.sync_path_label_endc)

        self.sync_path_comboBox_endc = QComboBox(self.layoutWidget_18)
        self.sync_path_comboBox_endc.addItem("")
        self.sync_path_comboBox_endc.addItem("")
        self.sync_path_comboBox_endc.addItem("")
        self.sync_path_comboBox_endc.addItem("")
        self.sync_path_comboBox_endc.setObjectName(u"sync_path_comboBox_endc")
        self.sync_path_comboBox_endc.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_endc.addWidget(self.sync_path_comboBox_endc)

        self.as_path_en_endc = QCheckBox(self.layoutWidget_18)
        self.as_path_en_endc.setObjectName(u"as_path_en_endc")

        self.verticalLayout_endc.addWidget(self.as_path_en_endc)

        self.as_path_comboBox_endc = QComboBox(self.layoutWidget_18)
        self.as_path_comboBox_endc.addItem("")
        self.as_path_comboBox_endc.addItem("")
        self.as_path_comboBox_endc.setObjectName(u"as_path_comboBox_endc")
        self.as_path_comboBox_endc.setEnabled(False)
        self.as_path_comboBox_endc.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_endc.addWidget(self.as_path_comboBox_endc)

        self.tx_level_lte_label_endc = QLabel(self.layoutWidget_18)
        self.tx_level_lte_label_endc.setObjectName(u"tx_level_lte_label_endc")
        sizePolicy3.setHeightForWidth(self.tx_level_lte_label_endc.sizePolicy().hasHeightForWidth())
        self.tx_level_lte_label_endc.setSizePolicy(sizePolicy3)
        self.tx_level_lte_label_endc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_endc.addWidget(self.tx_level_lte_label_endc)

        self.tx_level_lte_spinBox_endc = QSpinBox(self.layoutWidget_18)
        self.tx_level_lte_spinBox_endc.setObjectName(u"tx_level_lte_spinBox_endc")
        self.tx_level_lte_spinBox_endc.setAlignment(Qt.AlignCenter)
        self.tx_level_lte_spinBox_endc.setMaximum(30)
        self.tx_level_lte_spinBox_endc.setValue(20)

        self.verticalLayout_endc.addWidget(self.tx_level_lte_spinBox_endc)

        self.tx_level_nr_label_endc = QLabel(self.layoutWidget_18)
        self.tx_level_nr_label_endc.setObjectName(u"tx_level_nr_label_endc")
        sizePolicy3.setHeightForWidth(self.tx_level_nr_label_endc.sizePolicy().hasHeightForWidth())
        self.tx_level_nr_label_endc.setSizePolicy(sizePolicy3)
        self.tx_level_nr_label_endc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_endc.addWidget(self.tx_level_nr_label_endc)

        self.tx_level_nr_spinBox_endc = QSpinBox(self.layoutWidget_18)
        self.tx_level_nr_spinBox_endc.setObjectName(u"tx_level_nr_spinBox_endc")
        self.tx_level_nr_spinBox_endc.setAlignment(Qt.AlignCenter)
        self.tx_level_nr_spinBox_endc.setMaximum(30)
        self.tx_level_nr_spinBox_endc.setValue(20)

        self.verticalLayout_endc.addWidget(self.tx_level_nr_spinBox_endc)

        self.sync_path_toolBox.addItem(self.endc_sync, u"ENDC")
        self.equipment_groupBox = QGroupBox(self.centralwidget)
        self.equipment_groupBox.setObjectName(u"equipment_groupBox")
        self.equipment_groupBox.setGeometry(QRect(0, 0, 151, 91))
        self.verticalLayout_2 = QVBoxLayout(self.equipment_groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.equipments_comboBox = QComboBox(self.equipment_groupBox)
        self.equipments_comboBox.addItem("")
        self.equipments_comboBox.addItem("")
        self.equipments_comboBox.addItem("")
        self.equipments_comboBox.addItem("")
        self.equipments_comboBox.setObjectName(u"equipments_comboBox")
        sizePolicy1.setHeightForWidth(self.equipments_comboBox.sizePolicy().hasHeightForWidth())
        self.equipments_comboBox.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.equipments_comboBox)

        self.tx_port_groupBox = QGroupBox(self.centralwidget)
        self.tx_port_groupBox.setObjectName(u"tx_port_groupBox")
        self.tx_port_groupBox.setGeometry(QRect(0, 93, 151, 91))
        self.verticalLayout_3 = QVBoxLayout(self.tx_port_groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.port_table_en = QCheckBox(self.tx_port_groupBox)
        self.port_table_en.setObjectName(u"port_table_en")

        self.verticalLayout_3.addWidget(self.port_table_en)

        self.tx_port_comboBox = QComboBox(self.tx_port_groupBox)
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.addItem("")
        self.tx_port_comboBox.setObjectName(u"tx_port_comboBox")
        sizePolicy1.setHeightForWidth(self.tx_port_comboBox.sizePolicy().hasHeightForWidth())
        self.tx_port_comboBox.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.tx_port_comboBox)

        self.other_setting_groupBox = QGroupBox(self.centralwidget)
        self.other_setting_groupBox.setObjectName(u"other_setting_groupBox")
        self.other_setting_groupBox.setGeometry(QRect(0, 190, 151, 241))
        self.verticalLayout_4 = QVBoxLayout(self.other_setting_groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.volt_mipi_en = QCheckBox(self.other_setting_groupBox)
        self.volt_mipi_en.setObjectName(u"volt_mipi_en")

        self.verticalLayout_4.addWidget(self.volt_mipi_en)

        self.get_temp_en = QCheckBox(self.other_setting_groupBox)
        self.get_temp_en.setObjectName(u"get_temp_en")

        self.verticalLayout_4.addWidget(self.get_temp_en)

        self.fdc_en = QCheckBox(self.other_setting_groupBox)
        self.fdc_en.setObjectName(u"fdc_en")

        self.verticalLayout_4.addWidget(self.fdc_en)

        self.fbrx_en = QCheckBox(self.other_setting_groupBox)
        self.fbrx_en.setObjectName(u"fbrx_en")

        self.verticalLayout_4.addWidget(self.fbrx_en)

        self.mipi_read_en = QCheckBox(self.other_setting_groupBox)
        self.mipi_read_en.setObjectName(u"mipi_read_en")

        self.verticalLayout_4.addWidget(self.mipi_read_en)

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
        self.as_path_en_endc.toggled.connect(self.as_path_comboBox_endc.setEnabled)
        self.port_table_en.toggled.connect(self.tx_port_comboBox.setDisabled)

        self.tabWidget.setCurrentIndex(0)
        self.bands_toolBox.setCurrentIndex(1)
        self.txrx_path_toolBox.setCurrentIndex(1)
        self.test_items_toolBox.setCurrentIndex(0)
        self.sync_path_toolBox.setCurrentIndex(0)


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
        self.n48_nr.setText(QCoreApplication.translate("MainWindow", u"N48", None))
        self.n77_nr.setText(QCoreApplication.translate("MainWindow", u"N77", None))
        self.n78_nr.setText(QCoreApplication.translate("MainWindow", u"N78", None))
        self.n79_nr.setText(QCoreApplication.translate("MainWindow", u"N79", None))
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
        self.b48_lte.setText(QCoreApplication.translate("MainWindow", u"B48", None))
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
        self.therm_charge_dis_button.setText(QCoreApplication.translate("MainWindow", u"Thermal\n"
"Protect\n"
"Charge\n"
"Disable", None))
        self.run_button.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.tx_rx_path_group.setTitle(QCoreApplication.translate("MainWindow", u"Tx/Rx Path", None))
        self.tx1.setText(QCoreApplication.translate("MainWindow", u"Tx1", None))
        self.tx2.setText(QCoreApplication.translate("MainWindow", u"Tx2", None))
        self.ulmimo.setText(QCoreApplication.translate("MainWindow", u"MIMO", None))
        self.txrx_path_toolBox.setItemText(self.txrx_path_toolBox.indexOf(self.tx_path), QCoreApplication.translate("MainWindow", u"Tx Path", None))
        self.rx0.setText(QCoreApplication.translate("MainWindow", u"Rx0", None))
        self.rx1.setText(QCoreApplication.translate("MainWindow", u"Rx1", None))
        self.rx2.setText(QCoreApplication.translate("MainWindow", u"Rx2", None))
        self.rx3.setText(QCoreApplication.translate("MainWindow", u"Rx3", None))
        self.rx0_rx1.setText(QCoreApplication.translate("MainWindow", u"Rx0+Rx1", None))
        self.rx2_rx3.setText(QCoreApplication.translate("MainWindow", u"Rx2+Rx3", None))
        self.rx_all_path.setText(QCoreApplication.translate("MainWindow", u"ALL Path", None))
        self.txrx_path_toolBox.setItemText(self.txrx_path_toolBox.indexOf(self.rx_path), QCoreApplication.translate("MainWindow", u"Rx Path", None))
        self.ue_power.setTitle(QCoreApplication.translate("MainWindow", u"UE power(Rx Use)", None))
        self.ue_txmax.setText(QCoreApplication.translate("MainWindow", u"TxMax", None))
        self.ue_txlow.setText(QCoreApplication.translate("MainWindow", u"-10dBm", None))
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
        self.test_items_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Test Items", None))
        self.tx_lmh_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_LMH", None))
        self.tx_level_sweep_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_level_sweep", None))
        self.tx_freq_sweep_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_freq_sweep", None))
        self.tx_1rb_sweep_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_1RB_sweep\n"
"(only for NR)", None))
        self.tx_fcc_power_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_FCC_power", None))
        self.tx_ce_power_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_CE_power", None))
        self.tx_harmonics_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_Harmonics", None))
        self.tx_cbe_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_CBE", None))
        self.tx_ulca_lte_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_ULCA_LTE", None))
        self.tx_ulca_lte_cbe_ns.setText(QCoreApplication.translate("MainWindow", u"Tx_ULCA_LTE_CBE", None))
        self.rx_normal_ns.setText(QCoreApplication.translate("MainWindow", u"Rx_normal", None))
        self.rx_quick_ns.setText(QCoreApplication.translate("MainWindow", u"Rx_quick", None))
        self.rx_endc_desense_ns.setText(QCoreApplication.translate("MainWindow", u"Rx_ENDC_Desense", None))
        self.test_items_toolBox.setItemText(self.test_items_toolBox.indexOf(self.non_sig), QCoreApplication.translate("MainWindow", u"Non-sig", None))
        self.tx_lmh_s.setText(QCoreApplication.translate("MainWindow", u"Tx_LMH", None))
        self.rx_normal_s.setText(QCoreApplication.translate("MainWindow", u"Rx_normal", None))
        self.rxs_sweep_s.setText(QCoreApplication.translate("MainWindow", u"RxS_sweep", None))
        self.test_items_toolBox.setItemText(self.test_items_toolBox.indexOf(self.sig), QCoreApplication.translate("MainWindow", u"Sig", None))
        self.level_sweep_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Level_Sweep(3/4/5G)", None))
        self.start_level_label.setText(QCoreApplication.translate("MainWindow", u"Start_level", None))
        self.stop_level_label.setText(QCoreApplication.translate("MainWindow", u"Stop_level", None))
        self.freq_sweep_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Freq_Sweep(4/5G)", None))
        self.freq_sweep_step_label.setText(QCoreApplication.translate("MainWindow", u"Step(KHz)", None))
        self.freq_sweep_step.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.freq_sweep_start_label.setText(QCoreApplication.translate("MainWindow", u"Start(KHz)", None))
        self.freq_sweep_start.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.freq_sweep_stop_label.setText(QCoreApplication.translate("MainWindow", u"Stop(KHz)", None))
        self.freq_sweep_stop.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.sync_group.setTitle(QCoreApplication.translate("MainWindow", u"Sync/AS/SRS", None))
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

        self.tx_level_nlw_label.setText(QCoreApplication.translate("MainWindow", u"TX Level for 3/4/5G", None))
        self.pcl_lb_label.setText(QCoreApplication.translate("MainWindow", u"PCL LB for 2G", None))
        self.pcl_lb_level_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"5", None))
        self.pcl_lb_level_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"6", None))
        self.pcl_lb_level_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"7", None))
        self.pcl_lb_level_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"8", None))
        self.pcl_lb_level_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"9", None))
        self.pcl_lb_level_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"10", None))
        self.pcl_lb_level_combo.setItemText(6, QCoreApplication.translate("MainWindow", u"11", None))
        self.pcl_lb_level_combo.setItemText(7, QCoreApplication.translate("MainWindow", u"12", None))
        self.pcl_lb_level_combo.setItemText(8, QCoreApplication.translate("MainWindow", u"13", None))
        self.pcl_lb_level_combo.setItemText(9, QCoreApplication.translate("MainWindow", u"14", None))
        self.pcl_lb_level_combo.setItemText(10, QCoreApplication.translate("MainWindow", u"15", None))
        self.pcl_lb_level_combo.setItemText(11, QCoreApplication.translate("MainWindow", u"16", None))
        self.pcl_lb_level_combo.setItemText(12, QCoreApplication.translate("MainWindow", u"17", None))
        self.pcl_lb_level_combo.setItemText(13, QCoreApplication.translate("MainWindow", u"18", None))
        self.pcl_lb_level_combo.setItemText(14, QCoreApplication.translate("MainWindow", u"19", None))

        self.pcl_mb_label.setText(QCoreApplication.translate("MainWindow", u"PCL MB for 2G", None))
        self.pcl_mb_level_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.pcl_mb_level_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.pcl_mb_level_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.pcl_mb_level_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.pcl_mb_level_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.pcl_mb_level_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.pcl_mb_level_combo.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))
        self.pcl_mb_level_combo.setItemText(7, QCoreApplication.translate("MainWindow", u"7", None))
        self.pcl_mb_level_combo.setItemText(8, QCoreApplication.translate("MainWindow", u"8", None))
        self.pcl_mb_level_combo.setItemText(9, QCoreApplication.translate("MainWindow", u"9", None))
        self.pcl_mb_level_combo.setItemText(10, QCoreApplication.translate("MainWindow", u"10", None))
        self.pcl_mb_level_combo.setItemText(11, QCoreApplication.translate("MainWindow", u"11", None))
        self.pcl_mb_level_combo.setItemText(12, QCoreApplication.translate("MainWindow", u"12", None))
        self.pcl_mb_level_combo.setItemText(13, QCoreApplication.translate("MainWindow", u"13", None))
        self.pcl_mb_level_combo.setItemText(14, QCoreApplication.translate("MainWindow", u"14", None))
        self.pcl_mb_level_combo.setItemText(15, QCoreApplication.translate("MainWindow", u"15", None))

        self.gmsk_radioButton.setText(QCoreApplication.translate("MainWindow", u"GMSK", None))
        self.epsk_radioButton.setText(QCoreApplication.translate("MainWindow", u"EPSK", None))
        self.sync_path_toolBox.setItemText(self.sync_path_toolBox.indexOf(self.general_sync), QCoreApplication.translate("MainWindow", u"General", None))
        self.sync_path_label_endc.setText(QCoreApplication.translate("MainWindow", u"Sync Path", None))
        self.sync_path_comboBox_endc.setItemText(0, QCoreApplication.translate("MainWindow", u"Main", None))
        self.sync_path_comboBox_endc.setItemText(1, QCoreApplication.translate("MainWindow", u"CA#1", None))
        self.sync_path_comboBox_endc.setItemText(2, QCoreApplication.translate("MainWindow", u"CA#2", None))
        self.sync_path_comboBox_endc.setItemText(3, QCoreApplication.translate("MainWindow", u"CA#3", None))

        self.as_path_en_endc.setText(QCoreApplication.translate("MainWindow", u"AS Path", None))
        self.as_path_comboBox_endc.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.as_path_comboBox_endc.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))

        self.tx_level_lte_label_endc.setText(QCoreApplication.translate("MainWindow", u"TX Level for 4G", None))
        self.tx_level_nr_label_endc.setText(QCoreApplication.translate("MainWindow", u"TX Level for 5G", None))
        self.sync_path_toolBox.setItemText(self.sync_path_toolBox.indexOf(self.endc_sync), QCoreApplication.translate("MainWindow", u"ENDC", None))
        self.equipment_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Equipment", None))
        self.equipments_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Cmw100", None))
        self.equipments_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Cmw100+Fsw", None))
        self.equipments_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Anritsu8820", None))
        self.equipments_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Anritsu8821", None))

        self.tx_port_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Tx Port", None))
        self.port_table_en.setText(QCoreApplication.translate("MainWindow", u"Port table", None))
        self.tx_port_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.tx_port_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.tx_port_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.tx_port_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.tx_port_comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.tx_port_comboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.tx_port_comboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.tx_port_comboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))

        self.other_setting_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Other Setting", None))
        self.volt_mipi_en.setText(QCoreApplication.translate("MainWindow", u"Volt_mipi", None))
        self.get_temp_en.setText(QCoreApplication.translate("MainWindow", u"Get_temp", None))
        self.fdc_en.setText(QCoreApplication.translate("MainWindow", u"FDC", None))
        self.fbrx_en.setText(QCoreApplication.translate("MainWindow", u"FBRX", None))
        self.mipi_read_en.setText(QCoreApplication.translate("MainWindow", u"Mipi_read", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Loss_file", None))
    # retranslateUi

