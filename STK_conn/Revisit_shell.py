from CDM_Download import DB_Bottom
from STK_conn import Revisit_Core, int_STK, STK_bottom, Revisit_Bottom

import os, sys
import numpy

# 해경 분석 요구조건에 맞춰서 새로 짬
# STK bottom 은 start_stk, get_stk, simple_connect 정도만 사용하자..
def compress_result(dict_res):
    val = []
    for p in dict_res.keys():
        val.append(dict_res[p])

    ar = numpy.array(val)
    group_avg = ar[:,0:1]/60
    group_max = ar[:,1:2]/60
    group_min = ar[:,2:3]/60

    return [numpy.average(group_avg), numpy.max(group_avg), numpy.min(group_avg),
            numpy.average(group_max), numpy.max(group_max), numpy.min(group_max),
            numpy.average(group_min), numpy.max(group_min), numpy.min(group_min)]


class revisit_shell:
    def __init__(self, stk_handle=STK_bottom.bottom_stk(), task_name="task_62"):
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
            # 음영지역 (shadow point) 관리방법 찾아랍
            res = compress_result(dict_result_secondary[0])

            with open("..\\Log\\computeLog_{}.txt".format(self.task_name), 'a') as fp:
                # 분석결과 모음
                fp.write("raw {} {} km: {}\n".format(str_set, altitude, dict_result_secondary[0]))
                fp.write("RESULT {} {} km: {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}\n".format(str_set, altitude, res[0], res[1], res[2], res[3], res[4], res[5]))
                # 음영지역 모음
                fp.write("shadow {} {} km: {}\n".format(str_set, altitude, dict_result_secondary[1]))
                # 로그
                for p in dict_result_secondary[2].splitlines():
                    fp.write("filtered {} {} km {}\n".format(str_set, altitude, p))
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

        self.add_coverage_definition([target], grid=40000, add_fom=False)
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
    #res = {'0': (76797.31188888889, 86397.029, 86396.933), '1': (69117.56100000002, 86396.989, 86396.905), '2': (74054.72257142856, 86397.292, 86397.104), '3': (76797.38377777778, 86397.205, 86396.914), '4': (76797.4717777778, 86397.196, 86397.119), '5': (76797.45322222222, 86397.275, 86396.956), '6': (74054.72285714286, 86397.279, 86397.109), '7': (69117.8218, 86397.296, 86397.255), '8': (76797.37766666667, 86397.19, 86396.913), '9': (69117.71280000001, 86397.172, 86397.107), '10': (69117.58459999999, 86397.017, 86396.937), '11': (99999999.0, 99999999, 99999999), '12': (76797.31044444445, 86397.062, 86396.906), '13': (69117.66459999999, 86397.288, 86396.872), '14': (77757.5201, 86397.733, 86396.877), '15': (76797.52777777778, 86397.274, 86397.142), '16': (76797.39088888888, 86397.146, 86396.962), '17': (74054.80071428572, 86397.298, 86397.244), '18': (74054.61471428572, 86397.29, 86396.912), '19': (76797.47, 86397.22, 86397.097), '20': (71997.54766666667, 86397.128, 86396.874), '21': (69117.66880000001, 86397.107, 86397.069), '22': (69117.50959999999, 86396.915, 86396.865), '23': (69117.75600000001, 86397.205, 86397.179), '24': (57597.90966666667, 86396.867, 86396.862), '25': (69117.6152, 86397.034, 86396.993), '26': (69117.73019999999, 86397.175, 86397.143)}
    #shell.compress_result(res)
