from STK_conn import STK_bottom, Revisit_Bottom, STK_metadata, Revisit_shell
from PyQt5.QtWidgets import *


class panel_stk:
    def __init__(self, ui):
        self.ui = ui

        self.case_altitude = []
        self.case_inclination = []
        self.case_number_sats = []
        self.case_target_primary = []
        self.case_target_secondary= []
        self.case_area = []
        self.case_sensor_type = ""
        self.case_sensor_set = [0, 0, 0, 0]
        self.case_scenario_start = ""
        self.case_scenario_stop = ""

        self.stk_handle = STK_bottom.bottom_stk()
        self.update_number_case()
        self.check_fixed_val()

        self.ui.button_startSTK.clicked.connect(lambda: self.stk_handle.start_stk())
        self.ui.button_getSTK.clicked.connect(lambda: self.stk_handle.get_stk())
        self.ui.button_test2.clicked.connect(lambda: self.test_function())
        self.ui.button_executeSTK.clicked.connect(lambda: self.executeButton())
        self.ui.button_start_analysis.clicked.connect(lambda: self.start_analysis())
        self.ui.button_add_altitude.clicked.connect(lambda: self.insert_list("altitude"))
        self.ui.button_add_inclination.clicked.connect(lambda: self.insert_list("inclination"))
        self.ui.button_add_sats.clicked.connect(lambda: self.insert_list("sats"))
        self.ui.flush_altitude.clicked.connect(lambda: self.flush_list(self.ui.list_altitude))
        self.ui.flush_inclination.clicked.connect(lambda: self.flush_list(self.ui.list_inclination))
        self.ui.flush_sats.clicked.connect(lambda: self.flush_list(self.ui.list_sats))
        self.ui.button_set1.clicked.connect(lambda: self.ui.stacked_STK.setCurrentIndex(0))
        self.ui.button_set2.clicked.connect(lambda: self.ui.stacked_STK.setCurrentIndex(1))
        self.ui.button_load_facility.clicked.connect(lambda: self.load_facility())

        self.ui.list_altitude.itemPressed.connect(lambda: self.get_list_case())
        self.ui.list_inclination.itemPressed.connect(lambda: self.get_list_case())
        self.ui.list_sats.itemPressed.connect(lambda: self.get_list_case())

        self.ui.fixed_altitude.stateChanged.connect(lambda: self.check_fixed_val())
        self.ui.fixed_inclination.stateChanged.connect(lambda: self.check_fixed_val())
        self.ui.fixed_sats.stateChanged.connect(lambda: self.check_fixed_val())

    # 분석 시작
    def start_analysis(self):
        self.check_fixed_val()
        sample = {
            'altitude': [400, 500],
            'inclination': [40, 50],
            'sats': [28, 30],
            'scenario_start': '1 Jan 2020 03:00:00',
            'scenario_stop': '10 Jan 2020 03:00:00',
            'Area': ['NK'],
            'primary': ['seoul', 'daegu'],
            'secondary': ['dokdo', 'westSea'],
            'inter_plane_space': "1",
            'sensor_type': "SAR",
            'sensor_set': "20_50_83_83"
        }

        print("start of analysis")
        print(self.case_altitude)
        print(self.case_inclination)
        print(self.case_number_sats)

        try:
            # 분석에 사용하는 Facility 만 추가
            # STK_metadata.insert_facility_list(self.stk_handle.get_position_facility(self.case_target_primary + self.case_target_secondary))
            # Scenario 에 포함된 모든 Facility db 에 추가
            STK_metadata.insert_facility_list(self.stk_handle.get_position_facility(self.stk_handle.get_object_list()['Facility']))
        except Exception as e:
            print(e)

        task_name = STK_metadata.new_task(sample)
        # 재방문주기 계산 반복작업
        Revisit_shell.revisit_operator(task_name)
        # 분석 결과를 docx 보고서로 제작함

    def load_facility(self):
        print("시작")
        self.stk_handle.insert_facility_from_db()


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

    def insert_list(self, loc):
        item_list = []
        start = 0
        stop = 0
        step = 0
        try:
            if loc == "altitude":
                list_obj = self.ui.list_altitude
                self.flush_list(list_obj)
                start = int(self.ui.altitude_start.toPlainText())
                stop = int(self.ui.altitude_stop.toPlainText())
                step = int(self.ui.altitude_step.toPlainText())

            elif loc == "inclination":
                list_obj = self.ui.list_inclination
                self.flush_list(list_obj)
                start = float(self.ui.inclination_start.toPlainText())
                stop = float(self.ui.inclination_stop.toPlainText())
                step = float(self.ui.inclination_step.toPlainText())

            elif loc == "sats":
                list_obj = self.ui.list_sats
                self.flush_list(list_obj)
                start = int(self.ui.sats_start.toPlainText())
                stop = int(self.ui.sats_stop.toPlainText())
                step = int(self.ui.sats_step.toPlainText())

            i = start
            while i <= stop:
                item_list.append(str(i))
                i += step

            list_obj.addItems(item_list)
        except Exception as e:
            print(e)




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


