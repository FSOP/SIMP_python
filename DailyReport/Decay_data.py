from CDM_Download import iface, DB_Bottom
from data import iface_SQL, Time_Converter

import datetime


def count_decay_forecast():
    count_decay = {
        'DECAY_week': "",
        'DECAY_month': ""
    }

    now_utc = datetime.datetime.utcnow()
    now_utc_str = Time_Converter.datetime_to_str(now_utc, "%Y-%m-%d")

    db = DB_Bottom.DB_Bottom()
    db.db_init(iface.LOC_DB_DECAY)
    count_decay['DECAY_month'] = db.cur.execute(iface_SQL.sql_count_decay, (
        now_utc_str, Time_Converter.datetime_to_str(now_utc + datetime.timedelta(days=30), "%Y-%m-%d"))).fetchone()[0]

    count_decay['DECAY_week'] = db.cur.execute(iface_SQL.sql_count_decay, (
        now_utc_str, Time_Converter.datetime_to_str(now_utc + datetime.timedelta(days=7), "%Y-%m-%d"))).fetchone()[0]
    db.db_close()

    count_decay['DECAY_month'] = str(count_decay['DECAY_month'])
    count_decay['DECAY_week'] = str(count_decay['DECAY_week'])

    return count_decay


def get_decay_list():
    list_decay_msg = []
    decay_msg = {}
    now_utc_str = Time_Converter.datetime_to_str(datetime.datetime.utcnow(), "%Y-%m-%d")
    after_week_utc_str = Time_Converter.datetime_to_str(datetime.datetime.utcnow() + datetime.timedelta(days=7), "%Y-%m-%d")

    msg_index = 0

    db = DB_Bottom.DB_Bottom()
    db.db_init(iface.LOC_DB_DECAY)

    msg = db.cur.execute(iface_SQL.sql_query_decay, (now_utc_str, after_week_utc_str)).fetchall()

    for p in msg:
        msg_index += 1
        decay_msg = {
            'norad_id': str(p[0]),
            'name': p[4],
            'decay_epoch': p[1],
            'message_epoch': p[2],
            'msg_num': str(msg_index)
        }
        list_decay_msg.append(decay_msg)

    db.db_close()

    return list_decay_msg


if __name__ == "__main__":
    print(get_decay_list())
