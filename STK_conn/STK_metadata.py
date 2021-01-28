from CDM_Download import DB_Bottom, iface
from STK_conn import int_STK, STK_bottom
from data import Time_Converter
from DailyReport import MergeReport
import datetime, sys, os


# 분석 메타데이터 저장 STK_meta.txt
def new_task(values):
    now_utc = datetime.datetime.utcnow()
    year = str(now_utc.year)

    db = DB_Bottom.DB_Bottom()
    db.db_init(int_STK.LOC_DB_STK_META)

    last_task = db.cur.execute("select task_name from tasks order by insert_time desc limit 1").fetchone()

    if last_task is None:
        task_year = year
        task_num = "1"
    else:
        last_task = last_task[0].split("_")
        last_year = last_task[0]
        if year != last_year:
            task_year = year
            task_num = "1"
        else:
            task_year = last_year
            task_num = str(int(last_task[1]) + 1)

    task_name = "{}_{}".format(task_year, task_num)
    # task_name = "task_62"
    db.cur.execute("insert into tasks (insert_time, task_name) values (?, ?)",
                   (Time_Converter.datetime_to_str(now_utc), task_name))

    for set_type in ['altitude', 'inclination', 'sats', 'primary', 'secondary', 'Area', 'sensor_type', 'sensor_set', 'grid','inter_plane_space']:
        for q in values[set_type]:
            print("{} value: {}".format(set_type, q))
            db.cur.execute("insert into settings (task_name, set_type, set_value) values (?, ?, ?)",
                           (task_name, set_type, q))

    db.cur.execute("insert into scenario (task_name, scenario_start, scenario_stop) values (?, ?, ?)",
                   (task_name, values['scenario_start'], values['scenario_stop']))

    db.conn.commit()
    db.db_close()

    values.update({'task_name': task_name})
    set_result_file(values)
    return task_name


# 분석 결과를 저장할 테이블 생성 Analysis 폴더 밑에
def set_result_file(values):
    task_name = values['task_name']
    db = DB_Bottom.DB_Bottom()
    db.db_init(int_STK.LOC_DB_STK_RESULT.format(task_name))
    inter_plane_space = values['inter_plane_space'][0]

    # Primary Target 재방문주기 계산 요청 시 Primary_target 이름 사용
    db.cur.execute(
        "create table keys (altitude float, inclination float, number_sat int, number_plane int, inter_plane int, isdone int, primary key (altitude, inclination, number_sat, number_plane))")
    db.cur.execute("create table EEZ (setting string, altitude float, avg_avg float, avg_max float, avg_min float, max_max float, max_min float, max_avg float, primary key(setting, altitude))")
    for target_area in values['Area']:
        db.cur.execute(
            "create table {} (setting string, altitude float, avg_avg float, avg_max float, avg_min float, max_max float, max_min float, max_avg float, primary key(setting, altitude))".format(
                target_area))
    for target_second in values['secondary']:
        db.cur.execute(
            "create table {} (setting string, altitude float, avg float, max float, min float, primary key(setting, altitude))".format(
                target_second))

    for altitude in values['altitude']:
        for inclination in values['inclination']:
            for sats in values['sats']:
                for plane in get_dividor(sats):
                    db.cur.execute(
                        "insert into keys (altitude, inclination, number_sat, number_plane, inter_plane) values (?, ?, ?, ?, ?)",
                        (altitude, inclination, sats, plane, inter_plane_space))
                    # setting = "{}:{}/{}/{}".format(inclination, sats, plane, values['inter_plane_space'])

                    # for target_area in values['Area']:
                    #     db.cur.execute("insert into {} (setting, altitude) values (?, ?)".format(target_area), (setting, altitude))
                    # for target_second in values['secondary']:
                    #     db.cur.execute("insert into {} (setting, altitude) values (?, ?)".format(target_second), (setting, altitude))

    db.conn.commit()
    db.db_close()


def insert_facility_list(dict_facility):
    db = DB_Bottom.DB_Bottom()
    db.db_init(int_STK.LOC_DB_STK_META)
    for facility in dict_facility.keys():
        try:
            db.cur.execute("insert into facility (name, latitude, longitude, altitude) values (?, ?, ?, ?)", (
            facility, dict_facility[facility][0], dict_facility[facility][1], dict_facility[facility][2]))
        except Exception as e:
            print(e)

    db.conn.commit()
    db.db_close()


def get_facility_list():
    dict_ret = {}
    db = DB_Bottom.DB_Bottom()
    db.db_init(int_STK.LOC_DB_STK_META)
    rows = db.cur.execute("select name, latitude, longitude, altitude from facility").fetchall()

    if rows is None:
        return None

    for p in rows:
        print(p)
        dict_ret[p[0]] = [p[1], p[2], p[3]]

    db.db_close()
    return dict_ret


def get_dividor(value):
    res = []

    for p in range(1, int(value) + 1):
        if int(value) % p == 0:
            res.append(p)
    return res


def get_list_area_file(path="..\\DataFiles\\Objects"):
    return [p.split(".")[0] for p in os.listdir(path)]


def make_report_result(task_name):
    report_val = {
        'scenario_start': '',  # 4
        'scenario_stop': '',  # 5
        'Area': "",  # 6
        'primary': "",  # 7
        'secondary': "",  # 8
        'sensor_type': "",  # 10
        'sensor_set': "",  # incidence angle -> elevation angle   #11
        'grid': "",  # km
        'name_task': task_name
    }
    target = {
        'Area':[],
        'primary':[],
        'secondary':[]
    }

    report = MergeReport.MergeReport()
    report.merge_init(int_STK.LOC_REPORT_TEMPLATE)
    setting_list = DB_Bottom.simple(int_STK.LOC_DB_STK_META, 'select set_type, set_value from settings where task_name = "{}"'.format(task_name))
    scenario_list = DB_Bottom.simple(int_STK.LOC_DB_STK_META, 'select scenario_start, scenario_stop from scenario where task_name="{}"'.format(task_name))

    for set in setting_list:
        set_type = set[0]
        if set_type in ['Area', 'primary', 'secondary']:
            target[set_type].append(set[1])

        report_val[set_type]=str(set[1])

    print(target)
    print(report_val)
    report_val['scenario_start'] = scenario_list[0][0]
    report_val['scenario_stop'] = scenario_list[0][1]

    for p in target['Area']:
        report.merge_plain_data(report_val)
        table_data = []
        data_list = DB_Bottom.simple(int_STK.LOC_DB_STK_RESULT.format(task_name), 'select setting, altitude, avg_avg, avg_max, avg_min, max_max, max_min, max_avg from {}'.format(p))
        for q in data_list:
            print(q)
            row = {
                'v1': str(q[1]),
                'v2': str(q[0]),
                'v3': "{:.2f}".format(q[2]/60),
                'v4': "{:.2f}".format(q[3]/60),
                'v5': "{:.2f}".format(q[4]/60),
                'v6': "{:.2f}".format(q[5]/60),
                'v7': "{:.2f}".format(q[6]/60),
                'v8': "{:.2f}".format(q[7]/60),
            }
            table_data.append(row)
        report.merge_table_data("v1", table_data)
        report.create_stk_report(int_STK.LOC_ANALYSIS_REPORT.format(task_name, p))



if __name__ == "__main__":
    sample = {
        'altitude': [500],  # 1
        'inclination': [p for p in range(40,51)],  # 2
        'sats': [32],  # 3
        'scenario_start': '1 Jan 2021 03:00:00',  # 4
        'scenario_stop': '2 Jan 2021 03:00:00',  # 5
        'Area': ['NK'],  # 6
        'primary': [],  # 7
        'secondary': [],  # 8
        'inter_plane_space': ["1"],  # 9
        'sensor_type': ["SAR"],  # 10
        'sensor_set': ["15_35_89_89"],  # incidence angle -> elevation angle   #11
        'grid': ['40']  # km
    }
    sample = {
        'Area': [],
        'primary': [],
        'secondary': [],
        'altitude': ['500'],
        'inclination': [str(p) for p in range(39,50)],
        'sats': [str(p) for p in range(30,40)],
        'scenario_start': '1 Jan 2021 03:00:00',
        'scenario_stop': '10 Jan 2021 03:00:00',
        'grid': ['40'],
        'inter_plane_space': ['1'],
        'sensor_type': ['SAR'],
        'sensor_set': ['15_35_89_89'],
        'task_name': 'test_62'
    }
    # make_report_result("2021_12")
    new_task(sample)
    # print(get_list_area_file(""))
    # @print(get_facility_list())
    # print(get_dividor(30))
