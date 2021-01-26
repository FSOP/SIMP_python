from CDM_Download import DB_Bottom
from STK_conn import Revisit_Core


def revisit_operator(task_name):
    setting = {}
    remain_list = "select altitude, inclination, number_sat, number_plane, number_inter_plane from keys where isdone is null order by altitude asc, inclination asc"
    setting_list = "select set_type, set_value from settings where task_name = ?"
    scenario_set = "select scenario_start, scenario_stop from scenario where task_name=?"

    sat_status = {
        'altitude': 0,
        'inclination': 0
    }

    for set in setting_list:
        set_type = set[0]
        if set_type not in setting.keys():
            setting[set_type] = []
        setting[set_type].append(set[1])
    init_stk_scenario(setting, scenario_set)

    db = DB_Bottom.DB_Bottom()
    db.db_init(task_name)
    for p in remain_list:
        altitude = p[0]
        inclination = p[1]
        num_sat = p[2]
        num_plane = p[3]
        num_inter_plane = p[4]

        if altitude != sat_status['altitude'] and inclination != sat_status['inclination']:
            pass
            # delete all satellites from STK Scenario
            # add new SAT_
            # add new sensor using setting[sensor_Type]

        else:
            # delete all satellites WITHOUT SAT_
            pass
        # create walker-delta constellation

        # compute access for area_targets
        for area in setting['Area']:
            # compute access for each Area Targets
            area_val = compute_area_target(area)
            "insert into {} (setting, altitude, avg_avg, avg_max, avg_min, max_max, max_min, max_avg) values (?, ?,?,?,?,?,?,?)".format(area), area_val
            pass

        # get Strands access report for primary target from STK
        scenario_interval = []
        access_primary = ""
        for target in setting['secondary']:
            # get Strands access report for secondary target from STK
            access_secondary = ""
            # pass above two values to get_primary_access
            secondary_val = Revisit_Core.get_primary_access(access_primary, access_secondary, scenario_interval)
            "insert into {} (setting, altitude, avg, max, min) values (?, ?, ?, ?, ?)".format(target), secondary_val

        db.cur.execute("update set isdone=1 where altitude = ? and inclination =? and num_sat = ? and num_plane = ?")
        db.conn.commit()

    db.db_close()


def init_stk_scenario(dict_set, list_scenario):
    pass


def compute_area_target(area):
    return ()
