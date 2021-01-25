from STK_conn import STK_bottom, Revisit_Bottom
from PyQt5.QtWidgets import *


class panel_stk:
    def __init__(self, ui):
        self.ui = ui

        self.case_altitude = []
        self.case_inclination = []
        self.case_number_sats = []

        self.stk_handle = STK_bottom.bottom_stk()
        self.update_number_case()
        self.check_fixed_val()

        self.ui.button_startSTK.clicked.connect(lambda: self.stk_handle.start_stk())
        self.ui.button_getSTK.clicked.connect(lambda: self.stk_handle.get_stk())
        self.ui.button_test2.clicked.connect(lambda: self.test_function())
        self.ui.button_executeSTK.clicked.connect(lambda: self.executeButton())
        self.ui.button_start_analysis.clicked.connect(lambda: self.start_analysis())
        self.ui.flush_altitude.clicked.connect(lambda: self.flush_list(self.ui.list_altitude))
        self.ui.flush_inclination.clicked.connect(lambda: self.flush_list(self.ui.list_inclination))
        self.ui.flush_sats.clicked.connect(lambda: self.flush_list(self.ui.list_sats))

        self.ui.list_altitude.itemPressed.connect(lambda: self.get_list_case())
        self.ui.list_inclination.itemPressed.connect(lambda: self.get_list_case())
        self.ui.list_sats.itemPressed.connect(lambda: self.get_list_case())

        self.ui.fixed_altitude.stateChanged.connect(lambda: self.check_fixed_val())
        self.ui.fixed_inclination.stateChanged.connect(lambda: self.check_fixed_val())
        self.ui.fixed_sats.stateChanged.connect(lambda: self.check_fixed_val())

    def update_number_case(self):
        number_altitude = len(self.case_altitude)
        number_inclination = len(self.case_inclination)
        number_sats = len(self.case_number_sats)

        total_number_case = number_altitude * number_inclination * number_sats

        self.ui.label_altitude.setText(str(number_altitude))
        self.ui.label_inclination.setText(str(number_inclination))
        self.ui.label_sats.setText(str(number_sats))
        self.ui.label_all_case.setText(str(total_number_case))

    def check_fixed_val(self):
        if self.ui.fixed_altitude.isChecked():
            self.case_altitude = [self.ui.line_altitude.text()]
            self.ui.list_altitude.setEnabled(False)
        else:
            self.ui.list_altitude.setEnabled(True)
            self.get_list_case()

        if self.ui.fixed_inclination.isChecked():
            self.case_inclination = [self.ui.line_inclination.text()]
            self.ui.list_inclination.setDisabled(True)
        else:
            self.ui.list_inclination.setEnabled(True)
            self.get_list_case()

        if self.ui.fixed_sats.isChecked():
            self.case_number_sats = [self.ui.line_sats.text()]
            self.ui.list_sats.setDisabled(True)
        else:
            self.ui.list_sats.setEnabled(True)
            self.get_list_case()

        self.update_number_case()

    def get_list_case(self):
        if not self.ui.fixed_altitude.isChecked():
            self.case_altitude = []
            for p in self.ui.list_altitude.selectedItems():
                self.case_altitude.append(p.text())

        self.case_inclination = []
        for p in self.ui.list_inclination.selectedItems():
            self.case_inclination.append(p.text())

        self.case_number_sats = []
        for p in self.ui.list_sats.selectedItems():
            self.case_number_sats.append(p.text())

        self.update_number_case()

    def start_analysis(self):
        print("start of analysis")
        print(self.case_altitude)
        print(self.case_inclination)
        print(self.case_number_sats)

    def flush_list(self, obj):
        obj.clear()
        self.check_fixed_val()

    def test_function(self):
        # print(self.stk_handle.simple_connect("Chains_R */Chain/Primary Strands"))
        Revisit_Bottom.core_get_fom(self.stk_handle.simple_connect('Report_RM */CoverageDefinition/North_Korea/FigureOfMerit/FigureOfMerit1 Style "Grid Stats"'))

    def executeButton(self):
        text = self.ui.text_STK_comm.toPlainText()

        for p in text.splitlines():
            re_val = self.stk_handle.simple_connect(p)
            print(re_val)


