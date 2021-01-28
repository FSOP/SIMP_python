from comtypes.client import CreateObject, GetActiveObject
from data import Time_Converter
from CDM_Download import iface
from STK_conn import int_STK, STK_metadata

import datetime


class bottom_stk:
    root = None

    def start_stk(self):
        try:
            uiApp = CreateObject('STK11.Application')
            uiApp.Visible = True
            uiApp.UserControl = True

            self.root = uiApp.Personality2
            self.root.NewScenario("test_scenario")

        except Exception as e:
            print(e)

    def get_stk(self):
        try:
            uiApp = GetActiveObject('STK11.Application')

            self.root = uiApp.Personality2

        except Exception as e:
            print(e)

    def simple_connect(self, comm):
        val = ""
        error_flag = "S"
        now = Time_Converter.datetime_to_str(datetime.datetime.now())
        if comm[0:1] == "#" or comm is None: return None
        try:
            re_val = self.root.ExecuteCommand(comm)
            for p in range(re_val.Count):
                val += re_val.item(p)
        except Exception as e:
            error_flag = "F"
            print(comm)
            print(e)

        with open(int_STK.LOC_LOG, 'a') as fp:
            fp.write("({}){} - {} \n".format(now, error_flag, comm))
        return val

    # belows
    def get_object_list(self):
        val = {}
        obj_list = self.simple_connect(int_STK.get_list_object)

        for p in obj_list.split(" "):
            if p == "":
                continue
            object_type = p.split("/")[-2]
            object_name = p.split("/")[-1].split("\n")[0]

            if object_type not in val.keys():
                val[object_type] = []
            val[object_type].append(object_name)

        return val

    def get_position_facility(self, target_list):
        dict_facility = {}
        for target in target_list:
            dict_facility[target] = self.simple_connect(int_STK.get_facility_position.format(target)).split(" ")[0:3]

        return dict_facility

    # DB 의 Facility 들을 STK 에 입력 후 Primary, Secondary Target 지정
    def insert_facility_from_db(self):
        fac_data = STK_metadata.get_facility_list()
        for facility in fac_data.keys():
            self.simple_connect(int_STK.insert_facility.format(facility))
            self.simple_connect(int_STK.set_facility.format(facility, str(fac_data[facility][0]), str(fac_data[facility][1]), str(fac_data[facility][2])))

    def set_scenario_interval(self, start_time, stop_time):
        self.simple_connect(int_STK.stk_scenario_interval.format(start_time, stop_time))
        pass

    def add_obj(self, type, name):
        self.simple_connect(int_STK.stk_new_object.format(type, name))

    def unload_obj(self, name):
        self.simple_connect(int_STK.stk_unload_obj.format(name))

    def unload_all_sat(self):
        self.simple_connect("UnloadMulti / */Satellite/SAT_*")

    def unload_child_sat(self, const_name="SATs"):
        self.simple_connect("Unload / */Constellation/{} all".format(const_name))

    def create_delta_constellation(self, num_sat, num_plane, inter_plane, name_const="SATs"):
        num_sat_per_plane = int(int(num_sat) / int(num_plane))
        self.simple_connect("Walker */Satellite/SAT_ Type Delta NumPlanes {} NumSatsPerPlane {} InterPlanePhaseIncrement {} ColorByPlane No ConstellationName {}".format(num_plane, num_sat_per_plane, inter_plane, name_const))

    def add_root_sat(self, altitude, inclination, epoch):
        semi_major_axis = float(altitude) * 1000 + 6378140
        self.add_obj("Satellite", "SAT_")
        self.simple_connect('SetState */Satellite/SAT_ Classical J2Perturbation UseScenarioInterval 60 J2000 "{}" {} 0.0 {} 0 0 0'.format(epoch, semi_major_axis, inclination))

    def add_root_sensor(self, type, set):
        # SAR 설정만 구현함
        # STK SAR Sensor 는 Incidence angle 값이 아니라 Elevation angle 값이 들어감
        # elevation angle = 90 (deg) - incidence angle
        if type == "SAR":
            set = set.split("_")
            elevation_angle_1 = 90 - float(set[0])
            elevation_angle_2 = 90 - float(set[1])
            exclusion_1 = set[2]
            exclusion_2 = set[3]
            self.add_obj("Satellite/SAT_/Sensor", "SAR_")
            self.simple_connect("Define */Satellite/SAT_/Sensor/SAR_ SAR {} {} {} {} TrackParentAltitude On".format(elevation_angle_2, elevation_angle_1, exclusion_1, exclusion_2))

    def set_all_sensors(self, name_const="SENSORs", name_sensor="SAR_"):
        for sat in self.get_object_list()['Satellite']:
            if sat == "SAT_": continue
            self.simple_connect("Chains */Constellation/{} Add Satellite/{}/Sensor/{}".format(name_const, sat, name_sensor))

    def chk_stk(self):
        try:
            self.simple_connect("AllInstanceNames /")
        except Exception as e:
            self.get_stk()

    def points_to_facility(self, name="EEZ1"):
        lat = 0.0
        lon = 0.0
        f_number = 0
        counter = 0
        val = self.simple_connect("Cov_RM */CoverageDefinition/{} GridPoints".format(name))
        print(val)
        for p in val.split(" ")[1:]:
            if counter == 1:
                lat = p
            if counter == 2:
                lon = p
            if counter == 3:
                counter = 0
                f_number += 1
                self.add_obj("Facility", "Facility_{}".format(f_number))
                self.add_obj("Chain", "EEZ_{}".format(f_number))
                self.simple_connect("Graphics */Facility/Facility_{} Label Show Off".format(f_number))
                self.simple_connect("SetPosition */Facility/Facility_{} Geodetic {} {} 0.0".format(f_number, lat, lon))
            counter += 1

    def unload_all_facility(self):
        self.simple_connect("UnloadMulti / */Facility/*")
        self.simple_connect("UnloadMulti / */Chain/EEZ_*")

if __name__ == "__main__":
    stk = bottom_stk()
    stk.get_stk()
    stk.points_to_facility()
