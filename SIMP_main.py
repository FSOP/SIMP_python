# 메인 클래스
import sys
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

        # self.ui.button_test.clicked.connect(self.test)
        # self.ui.button_test_2.clicked.connect(self.test3)

    def daily_report(self):
        self.ui.stackedWidget.setCurrentIndex(0)


    # def test(self):
    #     try:
    #         # QListWidget.addItem(QListWidgetItem.setText("asd"))
    #         # QListWidget.DoubleClicked.connect(self.test2)
    #         # QListWidget.itemClicked()
    #
    #         #item = QListWidgetItem()
    #         #item.setText("asdf")
    #         #self.ui.list_report.addItem(item)
    #         #self.ui.list_report.addItems(["item", "item"])
    #         self.ui.list_report.itemDoubleClicked.connect(self.test2)
    #
    #     except Exception as e:
    #         print(e)
    #
    # def test3(self):
    #     # QListWidget.selectedItems()
    #     print(self.ui.list_report.selectedItems()[0].text())
    #     try:
    #         # QListWidget.removeItemWidget(self.ui.list_report.selectedItems())
    #         # self.ui.list_report.removeItemWidget(self.ui.list_report.selectedItems()[0])      removeItemWidget 작동안함, 대신 takeItem 사용
    #         # self.ui.list_report.takeItem(self.ui.list_report.row(self.ui.list_report.selectedItems()[0]))
    #         self.ui.list_report.clear()
    #     except Exception as e:
    #         print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SIMP_main()
    form.show()
    exit(app.exec_())
