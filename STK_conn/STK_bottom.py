from comtypes.client import CreateObject, GetActiveObject
from STK_conn import int_STK, STK_metadata


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
        try:
            re_val = self.root.ExecuteCommand(comm)
            for p in range(re_val.Count):
                val += re_val.item(p)
        except Exception as e:
            print(comm)
            print(e)

        return val

    # belows
    def get_object_list(self):
        val = {}
        obj_list = self.simple_connect(int_STK.get_list_object)
        # print(obj_list)

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


if __name__ == "__main__":
    stk = bottom_stk()
    stk.get_stk()
    values = stk.get_object_list()
    print(values)
