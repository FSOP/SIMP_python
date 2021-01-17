from CDM_Download import DB_Bottom, Web_Celestrak, iface
from data import Metadata


def clear_cat():
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_CDM)
    db_handle.cur.execute("delete from satcat")
    db_handle.conn.commit()
    db_handle.db_close()


def update_satcat():
    clear_cat()
    update_query = "insert into satcat values (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    db_handle = DB_Bottom.DB_Bottom()
    data = Web_Celestrak.CelestrakCAT().get_SATCAT()

    db_handle.db_init(iface.LOC_DB_CDM)
    cur = db_handle.cur

    for p in data.splitlines():
        intd = p[0:11].strip()
        norad = p[13:18].strip()
        multiple_name_flag = p[19:20].strip()
        payload_flag = p[20:21].strip()
        operational_status_code = p[21:22].strip()
        sat_name = p[23:47].strip()
        ownership = p[49:54].strip()
        launch_date = p[56:66].strip()
        launch_site = p[68:73].strip()
        decay_date = p[75:85].strip()
        orbital_period = p[87:94].strip()
        inclination = p[96:101].strip()
        apogee = p[103:109].strip()
        perigee = p[111:117].strip()
        rcs = p[119:127].strip()
        orbital_status_code = p[129:132].strip()

        try:
            cur.execute(update_query, (
                intd, norad, multiple_name_flag, payload_flag, operational_status_code, sat_name, ownership,
                launch_date, launch_site, decay_date, orbital_period, inclination,
                apogee, perigee, rcs, orbital_status_code))

        except Exception as e:
            print(e)

    Metadata.insert_metadata(iface.SATCAT_UTC)
    db_handle.conn.commit()
    db_handle.db_close()


class SATCAT_Download:
    pass


if __name__ == "__main__":
    update_satcat()
