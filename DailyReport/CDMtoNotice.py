# 전파할 CDM 을 검색하는 클래스
#
# 검색기준
# 1. 보고서 작성시간을 기준으로 이전 보고서 생성 시간부터(현재시간 보다 8시간 이상 차이나야 함) 부터 생성된 CDM 을 기본 검색 대상으로 함
#  - 먼 미래 CDM 의 예측이 부정확하고, 오랜 기간 남아있음 (예를 들어 10일 뒤의 이벤트를 잘못 예측하거나, 위성의 Maneuver 로 근접예측이 무의미해질 경우))
#  - 의미 있는 CDM 이라면, 약 24 시간 내에는 새로 생성된 CDM 이 존재
# 2. 이전 보고서 생성 시간부터 현재까지 업데이트 된 CDM 의 Miss_distance(최대 근접거리)가 저궤도 위성 1000m, 정지궤도 위성 5000m 이내인 경우
#
# 전파기준
# 3. 업데이트 된 CDM 을 기준으로
# 4. 각 이벤트의 가장 최신 CDM 의 Miss_distance, Probability(충돌 확률)이 아래의 기준을 만족하는 경우
#     - 저궤도 위성: Miss_distance < 1000 m & Probability > 1E-5
#     - 정지궤도 위성: Miss_distance < 5000 m
#
# SpaceTrack 궤도 종류별 분류법 (참고자료: https://www.space-track.org/documents/Spaceflight_Safety_Handbook_for_Operators.pdf)
# Near Earth:  궤도의 공전 주기 < 225 분 인 위성 ( 저궤도 위성에 적용 )
# Deep Space: 225 분 < 궤도의 공전 주기 ( 정지궤도 위성에 적용 )
# 본 프로그램에서는 계산의 편의를 위해 위와 같은 분류기준을 적용함 (공전 주가가 225 분 보다 크거나 같으면 정지궤도 기준 적용)
from data import iface_SQL
from CDM_Download import DB_Bottom, iface


class CDMtoNotice:
    sql = iface_SQL.iface_SQL
    last_report_time = None
    list_to_notice = []

    def cdm_to_notice(self):
        db_handle = DB_Bottom.DB_Bottom()
        db_handle.db_init(iface.LOC_DB_CDM)

        leo_notice = db_handle.cur.execute(self.sql.sql_notice_query_leo, (self.last_report_time,)).fetchall()
        geo_notice = db_handle.cur.execute(self.sql.sql_notice_query_geo, (self.last_report_time,)).fetchall()
        # print(geo_notice + leo_notice)

        for p in geo_notice + leo_notice:
            self.list_to_notice.append(p[0])

        print(self.list_to_notice)
        db_handle.db_close()

    def screened_cdm(self, last_report_time_utc):
        list_screened_cdm = []
        dict_screened_data = {}
        cdm_no = 0
        self.last_report_time = last_report_time_utc

        self.cdm_to_notice()

        db_handle = DB_Bottom.DB_Bottom()
        db_handle.db_init(iface.LOC_DB_CDM)

        screened_leo = db_handle.cur.execute(
            self.sql.sql_screen_cdm.format(self.sql.orbit_leo_period_criteria, self.sql.miss_distance_leo),
            (self.last_report_time,)).fetchall()

        screened_geo = db_handle.cur.execute(
            self.sql.sql_screen_cdm.format(self.sql.orbit_geo_period_criteria, self.sql.miss_distance_geo),
            (self.last_report_time,)).fetchall()

        rows = screened_geo + screened_leo

        for p in rows:
            cdm_no += 1
            if p[1] in self.list_to_notice:
                met_criteria = "O"
            else:
                met_criteria = "X"

            if p[4] is None:
                probability = "-"
            else:
                probability = p[4]

            dict_screened_data = {
                'CDM_NO': str(cdm_no),
                'CREATION_DATE': p[0].replace("T", "\n"),
                'SAT1_NAME': p[8],
                'SAT1_NORAD': str(p[9]),
                'SAT2_NAME': p[10],
                'SAT2_NORAD': str(p[11]),
                'TCA': p[5].replace("T","\n"),
                'MISS_DISTANCE': str(p[3]),
                'PROBABILITY': probability,
                'MET_CRITERIA': met_criteria,
                'EVENTNUM': str(p[6])
            }

            list_screened_cdm.append(dict_screened_data)

        db_handle.db_close()

        return list_screened_cdm


if __name__ == "__main__":
    CDMtoNotice().screened_cdm("2021-01-01T00:00:00")
