from CDM_Download import DB_Bottom
from STK_conn import Revisit_Core, int_STK, STK_bottom, Revisit_Bottom

import os, sys


class revisit_shell:
    def __init__(self, stk_handle, task_name):
        # get instance of STK_bottom
        self.stk = stk_handle
        # self.stk = STK_bottom.bottom_stk()
        self.task_name = task_name

    def revisit_operator_main(self):
        sat_status = {
            'altitude': 0,
            'inclination': 0
        }
        setting = self.load_settings()
        list_remain = self.get_list_remain()

        self.init_stk_scenario(setting)


        # NK area 는 기본으로 추가함
        self.stk.simple_connect('Load / */AreaTarget "{}{}"'.format(os.getcwd(), "\\..\\DataFiles\\Objects\\NK.at"))
        self.stk.simple_connect('Load / */AreaTarget "{}{}"'.format(os.getcwd(), "\\..\\DataFiles\\Objects\\EEZ.at"))
        self.stk.simple_connect("New / */Chain NK")
        self.stk.simple_connect("Chains */Chain/C_primary Add Constellation/SENSORs")
        self.stk.simple_connect("New / */CoverageDefinition EEZ1")
        self.stk.simple_connect("Cov */CoverageDefinition/EEZ1 Grid AreaOfInterest Custom AreaTarget AreaTarget/EEZ")
        self.stk.simple_connect("Cov */CoverageDefinition/EEZ1 Grid PointGranularity LatLon 0.4")

        # EEZ 해양지역 Facility grid Object 로 추가
        self.stk.points_to_facility()
        print(list_remain)
        print(setting)

        for sat in list_remain:
            altitude = sat[0]
            inclination = sat[1]
            num_sat = sat[2]
            num_plane = sat[3]
            inter_plane = sat[4]

            if num_plane == 1:
                inter_plane = 0
            set_iteration = "{}:{}/{}/{}".format(inclination, num_sat, num_plane, inter_plane)
            print("{} {} km 조건의 분석입니다.".format(set_iteration, altitude))

            # 고도나 경사각 조건이 달라지면 root 위성을 새로 만들어야 함
            if altitude != sat_status['altitude'] or inclination != sat_status['inclination']:
                print("root 위성 새로 만듦")
                self.stk.unload_all_sat()
                sat_status['altitude'] = altitude
                sat_status['inclination'] = inclination

                self.stk.add_root_sat(altitude, inclination, setting['scenario_start'])
                self.stk.add_root_sensor(setting['sensor_type'][0], setting['sensor_set'][0])

            # 각 Walker Delta Constellation 의 Iteration 분석을 수행함
            self.stk.unload_child_sat()
            self.stk.create_delta_constellation(num_sat, num_plane, inter_plane, name_const="SATs")
            # Sensor Constellation 에 위성군의 Sensor object 추가
            self.stk.set_all_sensors()

            # self.shell_mode_1(setting, altitude, set_iteration)

    def shell_mode_2(self):
        pass

    def shell_mode_1(self, setting, altitude, set_iteration):
        for area in setting['Area']:
            self.stk.simple_connect("Cov */CoverageDefinition/{} Asset */Constellation/SENSORs Assign".format(area))
            self.stk.simple_connect("Cov */CoverageDefinition/{} Access Compute".format(area))
            avg_data = Revisit_Bottom.core_get_fom(self.stk.simple_connect(
                'Report_RM */CoverageDefinition/{}/FigureOfMerit/Average Style "Grid Stats"'.format(area)))
            max_data = Revisit_Bottom.core_get_fom(self.stk.simple_connect(
                'Report_RM */CoverageDefinition/{}/FigureOfMerit/Maximum Style "Grid Stats"'.format(area)))
            print(avg_data)

            try:
                self.insert_result_into_db("area", setting=set_iteration, altitude=altitude,
                                           res_val=[avg_data, max_data], target=area)
            except Exception as e:
                print(e)
        pass

        #     else:
        #         # delete all satellites WITHOUT SAT_
        #         pass
        #     # create walker-delta constellation
        # 
        #     # compute access for area_targets
        #     for area in setting['Area']:
        #         # compute access for each Area Targets
        #         area_val = compute_area_target(area)
        #         "insert into {} (setting, altitude, avg_avg, avg_max, avg_min, max_max, max_min, max_avg) values (?, ?,?,?,?,?,?,?)".format(area), area_val
        #         pass
        # 
        #     # get Strands access report for primary target from STK
        #     scenario_interval = []
        #     access_primary = ""
        #     for target in setting['secondary']:
        #         # get Strands access report for secondary target from STK
        #         access_secondary = ""
        #         # pass above two values to get_primary_access
        #         secondary_val = Revisit_Core.get_primary_access(access_primary, access_secondary, scenario_interval)
        #         "insert into {} (setting, altitude, avg, max, min) values (?, ?, ?, ?, ?)".format(target), secondary_val
        # 
        #     db.cur.execute("update set isdone=1 where altitude = ? and inclination =? and num_sat = ? and num_plane = ?")
        #     db.conn.commit()
        # 
        # db.db_close()

    def load_settings(self):
        setting = {
            'altitude': [],  # 1
            'inclination': [],  # 2
            'sats': [],  # 3
            'scenario_start': '',  # 4
            'scenario_stop': '',  # 5
            'Area': [],  # 6
            'primary': [],  # 7
            'secondary': [],  # 8
            'inter_plane_space': [],  # 9
            'sensor_type': [],  # 10
            'sensor_set': [],  # incidence angle -> elevation angle   #11
            'grid': []  # km
        }
        db = DB_Bottom.DB_Bottom()
        db.db_init(int_STK.LOC_DB_STK_META)

        setting_list = db.cur.execute("select set_type, set_value from settings where task_name = ?",
                                      (self.task_name,)).fetchall()
        scenario_set = db.cur.execute("select scenario_start, scenario_stop from scenario where task_name=?",
                                      (self.task_name,)).fetchone()

        for set in setting_list:
            set_type = set[0]
            if set_type not in setting.keys():
                setting[set_type] = []
            setting[set_type].append(set[1])

        setting['scenario_start'] = scenario_set[0]
        setting['scenario_stop'] = scenario_set[1]
        db.db_close()

        return setting

    def get_list_remain(self):
        db = DB_Bottom.DB_Bottom()
        db.db_init(int_STK.LOC_DB_STK_RESULT.format(self.task_name))

        remain_list = db.cur.execute(
            "select altitude, inclination, number_sat, number_plane, inter_plane from keys where isdone is null order by altitude asc, inclination asc").fetchall()
        return remain_list

    def init_stk_scenario(self, dict_set):
        # STK 시나리오 분석시간 설정
        self.stk.set_scenario_interval(dict_set['scenario_start'], dict_set['scenario_stop'])

        # STK 시나리오 상 Primary Target 의 Chain, Constellation object 삭제
        self.stk.simple_connect("Unload / */Chain/C_primary")
        self.stk.simple_connect("Unload / */Constellation/SENSORs")
        self.stk.simple_connect("Unload / */Constellation/primary")

        # 분석을 위한 군집 설정: 위성군 센서 군집, 우선 순위 표적 군집
        self.stk.add_obj("Constellation", "SENSORs")
        self.stk.add_obj("Constellation", "primary")
        self.stk.add_obj("Chain", "C_primary")
        # self.stk.simple_connect(int_STK.stk_chain_autocomp_off.format("C_primary"))

        obj_list = self.stk.get_object_list()

        for area in dict_set['Area']:
            self.insert_target_area(area, dict_set['grid'][0])

        for primary in dict_set['primary']:
            if primary not in obj_list['Facility']:
                self.insert_facility(primary)
            self.stk.simple_connect(int_STK.stk_add_constellation.format("primary", "Facility/{}".format(primary)))
            self.stk.simple_connect(int_STK.stk_add_chain.format("C_primary", "Constellation/primary".format(primary)))
            self.stk.simple_connect("Chains */Chain/C_primary AutoRecompute off")

        for secondary in dict_set['secondary']:
            if secondary not in obj_list['Facility']:
                self.insert_facility(secondary)
            self.stk.simple_connect("Unload / */Chain/C_{}".format(secondary))
            self.stk.add_obj("Chain", "C_{}".format(secondary))
            self.stk.simple_connect(
                int_STK.stk_add_chain.format("C_{}".format(secondary), "Facility/{}".format(secondary)))
            self.stk.simple_connect("Chains */Chain/C_{} AutoRecompute off".format(secondary))

    def compute_area_target(self, area):
        pass

    def insert_facility(self, name):
        db = DB_Bottom.DB_Bottom()
        db.db_init(int_STK.LOC_DB_STK_META)
        val = db.cur.execute("select name, latitude, longitude, altitude from facility where name = ?",
                             (name,)).fetchone()
        self.stk.add_obj("Facility", val[0])
        self.stk.simple_connect(int_STK.stk_set_position.format(val[0], val[1], val[2], val[3]))
        db.db_close()

    def insert_target_area(self, target, grid):
        self.stk.simple_connect(
            'Load / */AreaTarget "{}{}"'.format(os.getcwd(), "\\..\\DataFiles\\Objects\\{}.at".format(target)))
        self.stk.unload_obj("CoverageDefinition/{}".format(target))
        self.stk.add_obj("CoverageDefinition", target)

        self.stk.add_obj("CoverageDefinition/{}/FigureOfMerit".format(target), "Average")
        self.stk.add_obj("CoverageDefinition/{}/FigureOfMerit".format(target), "Maximum")
        self.stk.simple_connect(
            "Cov */CoverageDefinition/{} Grid AreaOfInterest Custom AreaTarget AreaTarget/{}".format(target, target))
        self.stk.simple_connect("Cov */CoverageDefinition/{} Grid PointGranularity Distance {}000".format(target, grid))
        self.stk.simple_connect(
            "Cov */CoverageDefinition/{}/FigureOfMerit/Average FOMDefine Definition RevisitTime Compute Average EndGaps Include".format(
                target))
        self.stk.simple_connect(
            "Cov */CoverageDefinition/{}/FigureOfMerit/Maximum FOMDefine Definition RevisitTime Compute Maximum EndGaps Include".format(
                target))
        self.stk.simple_connect("Cov */CoverageDefinition/{} Access AutoRecompute off".format(target))

    def insert_result_into_db(self, type, setting, altitude, res_val, target):
        db = DB_Bottom.DB_Bottom()
        db.db_init(int_STK.LOC_DB_STK_RESULT.format(self.task_name))
        inclination = setting.split(":")[0]
        number_sat = setting.split(":")[1].split("/")[0]
        number_plane = setting.split(":")[1].split("/")[1]
        inter_plane = setting.split(":")[1].split("/")[2]

        if type == "area":
            query = "insert into {} (setting, altitude, avg_min, avg_max, avg_avg, max_min, max_max, max_avg) values " \
                    "(?, ?, ?, ?, ?, ?, ?, ?)".format(target)
            try:
                db.cur.execute(query, (setting, altitude, res_val[0][0], res_val[0][1], res_val[0][2], res_val[1][0], res_val[1][1], res_val[1][2]))
            except Exception as e:
                print(e)

        elif type == "secondary":
            query = "insert into {} (setting, altitude, avg, max, min) values (?, ?, ?, ?, ?)"
            db.cur.execute(query, (setting, altitude, res_val[0], res_val[1], res_val[2]))
        query_insert_key = "update keys set isdone=1 where altitude = ? and inclination = ? and number_sat = ? and number_plane = ? and inter_plane =? "
        # query_insert_key = "insert into keys (altitude,inclination, number_sat, number_plane, inter_plane, isdone) values (?,?, ?, ?, ?, ?)"
        db.cur.execute(query_insert_key, (altitude, inclination, number_sat, number_plane, inter_plane))
        db.conn.commit()
        db.db_close()


if __name__ == "__main__":
    stk = STK_bottom.bottom_stk()
    stk.get_stk()
    shell = revisit_shell(stk, "2021_12")

    print(shell.load_settings())
    print(shell.get_list_remain())
    shell.revisit_operator_main()
