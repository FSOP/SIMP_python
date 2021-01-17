from CDM_Download import DB_Bottom, iface
from data import Time_Converter
import datetime


def get_last_creation_date_utc():
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_CDM)

    last_creation_date_utc = db_handle.cur.execute("select max(creation_date) from cdm").fetchone()[0]
    db_handle.db_close()

    if last_creation_date_utc is None:
        last_creation_date_utc = iface.META_DATA_TIME_UTC

    return last_creation_date_utc


def insert_metadata(val, time_val=Time_Converter.datetime_to_str(datetime.datetime.utcnow())):
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_METADATA)

    db_handle.cur.execute("insert into metadata (updatetime, target) values (?, ?)", (time_val, val))

    db_handle.conn.commit()
    db_handle.db_close()


# 상황일지 작성목록 return
def get_list_report_docx():
    list_report = []
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_METADATA)

    rows = db_handle.cur.execute("select target, updatetime from metadata where target=? order by updatetime desc",
                          (iface.DAILY_REPORT_UTC,)).fetchall()

    for p in rows:
        val = Time_Converter.utc_to_kst_str(p[1], time_format="%Y%m%d_%H%M%S")
        list_report.append("{}".format(val))

    db_handle.db_close()

    return list_report


# 일일상황일지 생성 기준시간은 '현재시간 - 8'시간 보다 작아야 함
def get_last_report_make_utc():
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_METADATA)

    now_minus_eight = datetime.datetime.strftime(datetime.datetime.utcnow() - datetime.timedelta(hours=8),
                                                 iface.Time_format)
    daily_report_time_utc = \
        db_handle.cur.execute("select target, max(updatetime) from metadata where target = ? and updatetime < ?",
                              (iface.DAILY_REPORT_UTC, now_minus_eight)).fetchone()[1]

    db_handle.db_close()

    if daily_report_time_utc is None:
        daily_report_time_utc = iface.META_DATA_TIME_UTC

    return daily_report_time_utc


def get_cdm_count():
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_CDM)

    val = db_handle.cur.execute("select count(*) from cdm").fetchone()[0]
    print("[Metadata] CDM 수: {}".format(val))

    db_handle.db_close()

    return val


class Metadata:
    dict_metadata = iface.META_DATA_LIST

    def get_metadata(self):
        self.get_data_top()
        self.dict_metadata[iface.LAST_CDM_UTC] = get_last_creation_date_utc()
        self.dict_metadata[iface.REPORT_REF_TIME] = get_last_report_make_utc()
        # self.dict_metadata[iface.DAILY_REPORT_UTC] = self.get_last_report_make_utc()

        return self.dict_metadata

    def get_data_top(self):
        db_handle = DB_Bottom.DB_Bottom()
        db_handle.db_init(iface.LOC_DB_METADATA)

        rows = db_handle.cur.execute("select target, max(updatetime) from metadata group by target").fetchall()
        for p in rows:
            self.dict_metadata[p[0]] = p[1]

        db_handle.db_close()


if __name__ == "__main__":
    # Metadata().get_last_creation_date()
    # Metadata().get_cdm_count()

    insert_metadata(iface.DAILY_REPORT_UTC)
    print(Metadata().get_metadata())
