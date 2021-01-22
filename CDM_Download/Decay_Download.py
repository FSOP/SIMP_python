from CDM_Download import DB_Bottom, iface, Web_SP
from data import ReadConfig, iface_SQL

import json
import sqlite3


def download_decay():
    query = None
    conf = ReadConfig.read_conf()

    sp = Web_SP.SPlogin()
    sp.get_login(spid=conf['spid'], sppw=conf['sppw'])

    query = query_decay_msg(get_last_msg_time())
    decay_data = sp.get_sp_data(query)
    sp.sp_close()

    # decay_data = get_test_decay_msg()
    insert_decay_msg(decay_data)


def query_decay_msg(last_msg_time_utc):
    if last_msg_time_utc is None:
        return iface.queryDecay_with_blank
    else:
        return iface.queryDecay.format(last_msg_time_utc)


def get_last_msg_time():
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_DECAY)

    last_msg_time_utc = db_handle.cur.execute("select max(msg_epoch) from decay").fetchone()[0]
    print(last_msg_time_utc)

    db_handle.db_close()


def insert_decay_msg(data_text):
    db_handle = DB_Bottom.DB_Bottom()
    db_handle.db_init(iface.LOC_DB_DECAY)

    decay_list = json.loads(data_text)
    for p in decay_list:
        try:
            db_handle.cur.execute(iface_SQL.sql_insert_decay, (p['NORAD_CAT_ID'], p['OBJECT_NUMBER'], p['OBJECT_NAME'], p['INTLDES'], p['OBJECT_ID'], p['RCS'], p['RCS_SIZE'], p['COUNTRY'], p['MSG_EPOCH'], p['DECAY_EPOCH'], p['SOURCE'], p['MSG_TYPE'], p['PRECEDENCE']))
        except sqlite3.IntegrityError as e:
            print(e)

    db_handle.conn.commit()
    db_handle.db_close()


def get_test_decay_msg():
    path = "..\\DataFiles\\test_decay_data.txt"
    with open(path) as fp:
        data = fp.read()

    return data


if __name__ == "__main__":
    download_decay()
