# 관리대상 위성 목록을 업데이트하는 클래스
######
from CDM_Download import DB_Bottom, iface
from data import iface_SQL

class Sat_interest:
    def update_satellite_list(self):
        sql = iface_SQL.iface_SQL
        db_handle = DB_Bottom.DB_Bottom()
        db_handle.db_init(iface.LOC_DB_CDM)
        cur = db_handle.cur

        sat_list = cur.execute(sql.sql_sat_list_query).fetchall()

        for p in sat_list:
            try:
                cur.execute(sql.sql_sat_list_update, (p[0], p[1], p[2]))
            except:
                pass

        db_handle.conn.commit()
        db_handle.db_close()


if __name__ == "__main__":
    Sat_interest().update_satellite_list()