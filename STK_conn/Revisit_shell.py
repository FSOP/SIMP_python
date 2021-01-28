from CDM_Download import DB_Bottom
from STK_conn import Revisit_Core, int_STK, STK_bottom, Revisit_Bottom

import os, sys


# 해경 분석 요구조건에 맞춰서 새로 짬
# STK bottom 은 start_stk, get_stk, simple_connect 정도만 사용하자..
class revisit_shell:
    def __init__(self, stk_handle=STK_bottom.bottom_stk(), task_name="test"):
        self.stk = stk_handle
        self.task_name = task_name

    def main_analysis_shell(self):
        print("start of analysis")
        altitude = 0
        inclination = 0
        new_root_sat_flag = False

        dict_setting = self.load_settings()
        list_remain = self.get_list_remain()
        epoch = dict_setting['scenario_interval'][0]

        self.unload_all_objects()
        self.set_stk_scenario_interval(dict_setting['scenario_interval'])
        self.load_area_targets(["NK", "EEZ"])
        self.add_obj_constellation(["SENSORs"])
        list_point = self.set_facility_grid("EEZ")

        for each in list_remain:
            if altitude != each[0] or inclination != each[1]:
                new_root_sat_flag = True
            altitude = each[0]
            inclination = each[1]
            num_sat = each[2]
            num_plane = each[3]
            inter_plane = each[4]
            str_set = "{}:{}/{}/{}".format(inclination, num_sat, num_plane, inter_plane)
            print("{} alt: {} km 조건을 분석합니다.".format(str_set, altitude))

            if new_root_sat_flag:
                self.add_root_sat(epoch, altitude=altitude, inclination=inclination)
                self.add_root_sensor(sensor_val=dict_setting['sensor_set'], sensor_type="SAR")
            self.set_walker_delta(num_sat, num_plane, inter_plane)
            self.set_sensor_constellation()

            strands_nk = self.get_strands("NK")
            dict_result_secondary = Revisit_Core.get_primary_access(self.stk, dict_setting['scenario_interval'], strands_nk, list_point)
            print(dict_result_secondary)
        pass

    def get_strands(self, name_chain):
        self.stk.simple_connect('Chains */Chain/{} Remove Constellation/SENSORs'.format(name_chain))
        self.stk.simple_connect('Chains */Chain/{} Add Constellation/SENSORs'.format(name_chain))
        res = self.stk.simple_connect('Chains_R */Chain/{} Strands'.format(name_chain))
        return res

    def unload_all_objects(self):
        self.stk.simple_connect("UnloadMulti / */Facility/*")
        self.stk.simple_connect("UnloadMulti / */Satellite/*")
        self.stk.simple_connect("UnloadMulti / */Chain/*")
        self.stk.simple_connect("UnloadMulti / */Constellation/*")
        self.stk.simple_connect("UnloadMulti / */AreaTarget/*")
        self.stk.simple_connect("UnloadMulti / */CoverageDefinition/*")

    def set_stk_scenario_interval(self, interval):
        self.stk.simple_connect(int_STK.stk_scenario_interval.format(interval[0], interval[1]))

    def load_area_targets(self, targets):
        for target in targets:
            self.stk.simple_connect(
                'Load / */AreaTarget "{}"'.format("{}\\..\\DataFiles\\Objects\\{}.at".format(os.getcwd(), target)))
            self.stk.simple_connect('New / */Chain {}'.format(target))
            self.stk.simple_connect('Chains */Chain/{} AutoRecompute off'.format(target))
            self.stk.simple_connect('Chains */Chain/{} Add AreaTarget/{}'.format(target, target))

    def set_facility_grid(self, target):
        list_point = []
        lat = 0

        self.add_coverage_definition([target], grid=100000, add_fom=False)
        val = self.stk.simple_connect("Cov_RM */CoverageDefinition/{} GridPoints".format(target))
        for i, p in enumerate(val.split(" ")[2:]):
            if i % 3 == 0:
                lat = p
            if i % 3 == 1:
                lon = p
                name = str(int(i / 3))
                list_point.append(name)
                self.stk.simple_connect('New / */Facility facility_{}'.format(name))
                self.stk.simple_connect('New / */Chain point_{}'.format(name))
                self.stk.simple_connect('Chains */Chain/point_{} AutoRecompute off'.format(name))
                self.stk.simple_connect('Chains */Chain/point_{} Add Facility/facility_{}'.format(name, name))
                self.stk.simple_connect('Chains */Chain/point_{} Add Constellation/SENSORs'.format(name))
                self.stk.simple_connect("Graphics */Facility/Facility_{} Label Show Off".format(name))
                self.stk.simple_connect("SetPosition */Facility/Facility_{} Geodetic {} {} 0.0".format(name, lat, lon))
            if i % 3 == 2:
                pass

        return list_point

    def add_coverage_definition(self, targets, grid=20000, add_fom=True):
        for target in targets:
            self.stk.simple_connect('New / */CoverageDefinition {}'.format(target))
            self.stk.simple_connect(
                'Cov */CoverageDefinition/{} Grid AreaOfInterest Custom AreaTarget AreaTarget/{}'.format(target,
                                                                                                         target))
            self.stk.simple_connect(
                'Cov */CoverageDefinition/{} Grid PointGranularity Distance {}'.format(target, grid))
            if add_fom:
                self.stk.simple_connect('New / */CoverageDefinition/{}/FigureOfMerit Average'.format(target))
                self.stk.simple_connect('New / */CoverageDefinition/{}/FigureOfMerit Maximum'.format(target))
                self.stk.simple_connect('New / */CoverageDefinition/{}/FigureOfMerit Minimum'.format(target))

    def add_obj_constellation(self, names):
        for const in names:
            self.stk.simple_connect('New / */Constellation {}'.format(const))

    def add_root_sat(self, epoch, altitude, inclination, name="SAT_"):
        semi_major = float(altitude) * 1000 + 6378140
        self.stk.simple_connect("UnloadMulti / */Satellite/*")
        self.stk.simple_connect('New / */Satellite {}'.format(name))
        self.stk.simple_connect(
            'SetState */Satellite/{} Classical J2Perturbation UseScenarioInterval 60 J2000 "{}" {} 0.0 {} 0 0 0'.format(
                name, epoch, semi_major, inclination))

    def add_root_sensor(self, sensor_val, sensor_type="SAR", name_sat="SAT_", name_sensor="SAR_"):
        if sensor_type == "SAR":
            sensor = sensor_val[0].split("_")
            elevation_angle_1 = 90 - float(sensor[0])
            elevation_angle_2 = 90 - float(sensor[1])
            exclusion_1 = sensor[2]
            exclusion_2 = sensor[3]
            self.stk.simple_connect("New / */Satellite/{}/Sensor {}".format(name_sat, name_sensor))
            self.stk.simple_connect(
                "Define */Satellite/{}/Sensor/{} SAR {} {} {} {} TrackParentAltitude On".format(name_sat, name_sensor,
                                                                                                elevation_angle_2,
                                                                                                elevation_angle_1,
                                                                                                exclusion_1,
                                                                                                exclusion_2))

    def set_walker_delta(self, num_sat, num_plane, inter_plane='1', sat_name="SAT_"):
        sat_per_plane = int(int(num_sat) / int(num_plane))
        if num_plane == 1:
            inter_plane = '0'
        self.stk.simple_connect('Walker */Satellite/{} Type Delta NumPlanes {} NumSatsPerPlane {} InterPlanePhaseIncrement {} ColorByPlane No'.format(sat_name, num_plane, sat_per_plane, inter_plane))

    def set_sensor_constellation(self, name_sensor="SAR_"):
        for sat in self.stk.get_object_list()['Satellite']:
            if sat == "SAT_": continue
            self.stk.simple_connect(
                "Chains */Constellation/SENSORs Add Satellite/{}/Sensor/{}".format(sat, name_sensor))


    def load_settings(self):
        setting = int_STK.shell_setting
        db = DB_Bottom.DB_Bottom()
        db.db_init(int_STK.LOC_DB_STK_META)

        setting_list = db.cur.execute("select set_type, set_value from settings where task_name = ?",
                                      (self.task_name,)).fetchall()
        scenario_set = db.cur.execute("select scenario_start, scenario_stop from scenario where task_name=?",
                                      (self.task_name,)).fetchone()

        for set in setting_list:
            set_type = set[0]
            setting[set_type].append(set[1])

        setting['scenario_interval'] = [scenario_set[0], scenario_set[1]]
        # setting['scenario_start'] = scenario_set[0]
        # setting['scenario_stop'] = scenario_set[1]
        db.db_close()
        return setting

    def get_list_remain(self):
        db = DB_Bottom.DB_Bottom()
        db.db_init(int_STK.LOC_DB_STK_RESULT.format(self.task_name))

        remain_list = db.cur.execute(
            "select altitude, inclination, number_sat, number_plane, inter_plane from keys where isdone is null order by altitude asc, inclination asc").fetchall()
        return remain_list


if __name__ == "__main__":
    shell = revisit_shell()
    shell.stk.get_stk()
    shell.main_analysis_shell()
