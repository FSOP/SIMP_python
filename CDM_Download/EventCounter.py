from CDM_Download import DB_Bottom, iface
import datetime

class EventCounter:
    def event_count(self):

        db_handle = DB_Bottom.DB_Bottom()
        self.event_year_count()
        max_event = self.get_max_eventnum()

        db_handle.db_init(iface.LOC_DB_CDM)
        cur = db_handle.cur

        #이매 해당 이벤트에 대한 기록이 존재하는 경우 해당 이벤트 번호를 불러옴
        query_exist = "select distinct eventnum from cdm where ? < tca and tca < ? and sat1_object_name = ? and sat2_object_name = ? and eventnum is not null"
        update_new = "update cdm set eventnum = ? where ? < tca and tca < ? and sat1_object_name = ? and sat2_object_name = ?"
        while(True):
            update_eventnum = None
            cdm_left = cur.execute("select count(*) from cdm where eventnum is null").fetchall()[0][0]
            if cdm_left == 0:break

            query = cur.execute("select message_id, tca, sat1_object_name, sat2_object_name, event_year from cdm where eventnum is null limit 1").fetchone()
            message_id = query[0]
            tca = query[1][:19]
            sat1_name = query[2]
            sat2_name = query[3]
            event_year = query[4]
            tca_stop = datetime.datetime.strptime(tca, "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(minutes=15)
            tca_start = datetime.datetime.strptime(tca, "%Y-%m-%dT%H:%M:%S") - datetime.timedelta(minutes=15)

            tca_stop = datetime.datetime.strftime(tca_stop, "%Y-%m-%dT%H:%M:%S")
            tca_start = datetime.datetime.strftime(tca_start, "%Y-%m-%dT%H:%M:%S")

            exist_num = cur.execute(query_exist,(tca_start, tca_stop, sat1_name, sat2_name)).fetchone()

            #해당 이벤트에 대한 기록이 있는 경우
            if exist_num != None:
                update_eventnum = exist_num[0]

            #해당 이벤트에 대한 기록이 없는 경우
            else:
                max_event[event_year] = max_event[event_year] + 1
                update_eventnum = max_event[event_year]

            if update_eventnum != None:
                #print(update_eventnum, str(tca_start)[:19], str(tca_stop)[:19], sat1_name, sat2_name)
                cur.execute(update_new, (str(update_eventnum), str(tca_start)[:19], str(tca_stop)[:19], sat1_name, sat2_name))
                db_handle.conn.commit()
            else:
                print("[EventCounter] Event 번호 none 데이터 발생")


        db_handle.db_close()

    def event_year_count(self):
        loc_db_cdm = iface.LOC_DB_CDM
        query_null_eventyear = "select message_id, tca from cdm where event_year is null"
        query_update_year = "update cdm set event_year = ? where message_id = ?"
        db_handle = DB_Bottom.DB_Bottom()

        db_handle.db_init(loc_db_cdm)
        cur = db_handle.cur

        cur.execute(query_null_eventyear)
        rows = cur.fetchall()
        #print(rows)

        for p in rows:
            cur.execute(query_update_year, (p[1][:4], p[0]))

        db_handle.conn.commit()
        db_handle.db_close()

    def get_max_eventnum(self):
        max_eventnum = {}
        query = "select event_year, max(eventnum) from cdm group by event_year"
        db_handle = DB_Bottom.DB_Bottom()

        db_handle.db_init(iface.LOC_DB_CDM)
        cur = db_handle.cur

        rows = cur.execute(query)
        data = rows.fetchall()

        db_handle.db_close()

        for p in data:
            if p[1] != None: max_eventnum[p[0]] = p[1]
            else: max_eventnum[p[0]] = 0

        return max_eventnum