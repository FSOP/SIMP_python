from data import Metadata, Time_Converter, iface_SQL
from CDM_Download import iface, CDM_download, SATCAT_Download, DB_Bottom
from DailyReport import MakeReport, Get_panel_data

import subprocess, os


class daily_report:
    def __init__(self, ui):
        self.ui = ui
        try:
            self.update_data()

            self.ui.list_report.itemDoubleClicked.connect(self.open_selected_report)
            self.ui.button_update_cdm.clicked.connect(lambda: self.update_cdm())
            self.ui.button_update_satcat.clicked.connect(lambda: self.update_satcat())
            self.ui.button_make_report.clicked.connect(lambda: self.report_make())
            self.ui.button_test_2.clicked.connect(lambda: self.update_data())
            self.ui.button_open_cdm.clicked.connect(lambda: os.startfile(os.getcwd() + "\\..\\CDM_xml"))
            self.ui.button_delete_list.clicked.connect(lambda: self.delete_report_list())

        except Exception as e:
            print(e)

    def update_data(self):
        metadata = Metadata.Metadata().get_metadata()

        self.ui.label_creation_date_utc.setText(metadata[iface.LAST_CDM_UTC])
        self.ui.label_creation_date_kst.setText(Time_Converter.utc_to_kst_str(metadata[iface.LAST_CDM_UTC]))
        self.ui.label_5.setText(metadata[iface.SATCAT_UTC])
        self.ui.label_last_report_utc.setText(metadata[iface.DAILY_REPORT_UTC])
        self.ui.label_last_report_kst.setText(Time_Converter.utc_to_kst_str(metadata[iface.DAILY_REPORT_UTC]))
        self.ui.label_report_ref.setText(metadata[iface.REPORT_REF_TIME])

        self.ui.list_report.clear()
        self.ui.list_report.addItems(Metadata.get_list_report_docx())

    def delete_report_list(self):
        db = DB_Bottom.DB_Bottom()
        db.db_init(iface.LOC_DB_METADATA)

        for p in self.ui.list_report.selectedItems():
            db.cur.execute(iface_SQL.sql_delete_report,
                           (iface.DAILY_REPORT_UTC,
                            Time_Converter.kst_to_utc_str(p.text())))

        db.conn.commit()
        db.db_close()

        self.update_data()

    @staticmethod
    def open_selected_report(i):
        file = iface.LOC_DAILY_REPORT.format(i.text())
        subprocess.Popen(file, shell=True)

    def update_satcat(self):
        SATCAT_Download.update_satcat()
        self.update_data()

    def update_cdm(self):
        CDM_download.download()
        self.update_data()

    def report_make(self):
        MakeReport.make_report(Get_panel_data.get_data_panel(self.ui))
        self.update_data()


if __name__ == "__main__":
    daily_report("").update_data()
