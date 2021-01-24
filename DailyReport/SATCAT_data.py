from CDM_Download import DB_Bottom, iface
from data import iface_SQL


def get_satcat_count():
    satcat_data = {}
    db = DB_Bottom.DB_Bottom()
    db.db_init(iface.LOC_DB_CDM)

    payload_orbit = db.cur.execute(iface_SQL.sql_payload_orbit).fetchone()[0]
    payload_decayed = db.cur.execute(iface_SQL.sql_payload_decayed).fetchone()[0]
    debris_orbit = db.cur.execute(iface_SQL.sql_debris_orbit).fetchone()[0]
    debris_decayed = db.cur.execute(iface_SQL.sql_debris_decayed).fetchone()[0]
    active_sat = db.cur.execute(iface_SQL.sql_active_sat).fetchone()[0]
    payload_all = payload_orbit + payload_decayed
    debris_all = debris_orbit + debris_decayed
    all_orbit = payload_orbit + debris_orbit
    all_decayed = payload_decayed + debris_decayed
    all_all = all_orbit + all_decayed

    satcat_data = {
        'p_1': str(payload_orbit),
        'p_2': str(payload_decayed),
        'p_3': str(payload_all),
        'd_1': str(debris_orbit),
        'd_2': str(debris_decayed),
        'd_3': str(debris_all),
        'a_1': str(all_orbit),
        'a_2': str(all_decayed),
        'a_3': str(all_all),
        'active': str(active_sat)
    }

    db.db_close()

    satcat_data.update(get_satcat_country())

    return satcat_data


def get_satcat_country():
    countries = {}
    count_for_all = 0
    db = DB_Bottom.DB_Bottom()
    db.db_init(iface.LOC_DB_CDM)

    for p in iface.list_of_satcat_country:
        val = db.cur.execute(iface_SQL.sql_count_country, (p,)).fetchone()[0]
        count_for_all += val
        countries[p] = str(val)

    countries['guitar'] = str(db.cur.execute(iface_SQL.sql_active_sat).fetchone()[0] - count_for_all)
    db.db_close()

    return countries


if __name__ == "__main__":
    print(get_satcat_count())
