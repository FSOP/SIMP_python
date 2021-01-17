from CDM_Download import DB_Bottom, iface
import json
import sqlite3


class insert_CDM:
    def insert_cdm(self, cdm_data):
        loc_db_cdm = iface.LOC_DB_CDM
        db_handle = DB_Bottom.DB_Bottom()
        self.keys = ""

        cdm_data = json.loads(cdm_data)
        # print("[INSERT CDM] ", cdm_data)
        print("[INSERT CDM] 다운로드 받은 CDM 수: {}".format(len(cdm_data)))

        # JSON 형식의 첫 번째 CDM을 이용하여 KEY 값을 저장함
        self.keys = cdm_data[0].keys()

        query = self.query_decorator()

        insert_data = []
        for p in cdm_data:
            t_data = []
            for j in self.keys:
                if len(j) >= 4:
                    if j[-4:] == "UNIT": continue
                t_data.append(p[j])
            insert_data.append(tuple(t_data))

        db_handle.db_init(loc_db_cdm)
        cur = db_handle.cur

        # cur.executemany(query, insert_data)
        for p in insert_data:
            try:
                cur.execute(query, p)
            except sqlite3.IntegrityError as e:
                print(e)

        db_handle.conn.commit()
        db_handle.db_close()

    def query_decorator(self):
        pre_text = "insert into cdm ("
        post_text = ""
        for p in self.keys:
            if len(p) >= 4:
                if p[-4:] == "UNIT": continue
            pre_text += p + ", "
            post_text += "?, "
        # print(pre_text[:-2] +") values (")
        # print(post_text[:-2] + ")")

        return pre_text[:-2] + ") values (" + post_text[:-2] + ")"
