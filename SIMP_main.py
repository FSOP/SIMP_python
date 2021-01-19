# 메인 클래스
import sys, os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from CDM_Download import iface
from DailyReport import DailyReport_panel


class SIMP_main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = uic.loadUi(iface.LOC_MAIN_UI, self)

        DailyReport_panel.daily_report(self.ui)

        self.ui.button_daily_report.clicked.connect(self.daily_report)
        self.ui.button_manage_data.clicked.connect(lambda v: self.ui.stackedWidget.setCurrentIndex(1))

    def daily_report(self):
        self.ui.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    os.chdir(".\\data")
    app = QApplication(sys.argv)
    form = SIMP_main()
    form.show()
    exit(app.exec_())
