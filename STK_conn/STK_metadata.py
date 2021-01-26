from CDM_Download import DB_Bottom
from STK_conn import int_STK, STK_bottom
from data import Time_Converter
import datetime

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

    db.cur.execute("insert into tasks (insert_time, task_name) values (?, ?)", (Time_Converter.datetime_to_str(now_utc), task_name))

    for set_type in ['altitude', 'inclination', 'sats', 'primary', 'secondary', 'Area', 'sensor_type', 'sensor_set']:
        for q in values[set_type]:
            print("{} value: {}".format(set_type, q))
            db.cur.execute("insert into settings (task_name, set_type, set_value) values (?, ?, ?)", (task_name, set_type, q))

    db.cur.execute("insert into scenario (task_name, scenario_start, scenario_stop) values (?, ?, ?)", (task_name, values['scenario_start'], values['scenario_stop'] ))

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

    # Primary Target 재방문주기 계산 요청 시 Primary_target 이름 사용
    db.cur.execute("create table keys (altitude float, inclination float, number_sat int, number_plane int, inter_plane int, isdone int)")
    for target_area in values['Area']:
        db.cur.execute("create table {} (setting string, altitude float, avg_avg float, avg_max float, avg_min float, max_max float, max_min float, max_avg float, primary key(setting, altitude))".format(target_area))
    for target_second in values['secondary']:
        db.cur.execute("create table {} (setting string, altitude float, avg float, max float, min float, primary key(setting, altitude))".format(target_second))

    for altitude in values['altitude']:
        for inclination in values['inclination']:
            for sats in values['sats']:
                for plane in get_dividor(sats):
                    db.cur.execute("insert into keys (altitude, inclination, number_sat, number_plane, inter_plane) values (?, ?, ?, ?, ?)", (altitude, inclination, sats, plane, values['inter_plane_space']))
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
            db.cur.execute("insert into facility (name, latitude, longitude, altitude) values (?, ?, ?, ?)", (facility, dict_facility[facility][0], dict_facility[facility][1], dict_facility[facility][2]))
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
    for p in range(1, value+1):
        if value % p == 0:
            res.append(p)
    return res


if __name__ == "__main__":
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
        'sensor_type': ["SAR"],
        'sensor_set': ["20_50_83_83"]
    }
    new_task(sample)
    #@print(get_facility_list())
    #print(get_dividor(30))
