# 다운로드 받은 CDM 계수 클래스
################

from CDM_Download import DB_Bottom, iface
from data import iface_SQL
import datetime


class CountNewCDM:
    def count_cdm(self, last_report_make_time_utc):
        dict_count_cdm = {}
        new_cdm_count = 0
        sql = iface_SQL.iface_SQL
        db_handle = DB_Bottom.DB_Bottom()
        db_handle.db_init(iface.LOC_DB_CDM)

        # Get dict type frame will deliver cdm count data
        dict_count_cdm = self.sat_frame(db_handle.cur)

        #새로 다운로드 받은 CDM 수
        new_cdm = db_handle.cur.execute(sql.sql_new_cdm, (last_report_make_time_utc,)).fetchall()

        #
        new_cdm_met_leo = db_handle.cur.execute(
            sql.sql_new_cdm_met.format(sql.orbit_leo_period_criteria), (sql.miss_distance_leo, last_report_make_time_utc)
        ).fetchall()

        new_cdm_met_geo = db_handle.cur.execute(
            sql.sql_new_cdm_met.format(sql.orbit_geo_period_criteria), (sql.miss_distance_geo, last_report_make_time_utc)
        ).fetchall()

        db_handle.db_close()

        # print(new_cdm)
        # print(new_cdm_met_leo)
        # print(new_cdm_met_geo)

        for p in new_cdm:
            international_designator = p[1]
            count_val = p[3]
            new_cdm_count += count_val
            dict_count_cdm[international_designator] = str(count_val)

        for p in (new_cdm_met_geo + new_cdm_met_leo):
            international_designator = p[1]
            count_val = p[3]
            dict_count_cdm["{}_met".format(international_designator)] = str(count_val)

        # Number of updated cdm for all satellites
        dict_count_cdm.update({'cdm_total':str(new_cdm_count)})
        return dict_count_cdm

    # return dictionary type frame which will contain cdm count data
    @staticmethod
    def sat_frame(cur):
        sql = iface_SQL.iface_SQL
        dict_frame = {}
        rows = cur.execute(sql.sql_get_satellite_list).fetchall()

        for p in rows:
            dict_frame[p[0]] = '0'
            dict_frame["{}_met".format(p[0])] = '0'

        return dict_frame


if __name__ == "__main__":
    CountNewCDM().count_cdm()
