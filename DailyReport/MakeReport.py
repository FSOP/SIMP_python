# 보고서 생성 메인 클래스
#######################

from CDM_Download import iface, Web_SP
from data import Metadata, Update_satellites, Time_Converter
from DailyReport import CountNewCDM, MergeReport, CDMtoNotice, CDMtoXML
import datetime


def make_report(panel_data):
    # 보고서 작성 시간(현재시간)
    make_time_utc = datetime.datetime.utcnow()
    file_name = Time_Converter.datetime_to_str(make_time_utc + datetime.timedelta(hours=9),
                                               time_format="%Y%m%d_%H%M%S")

    # 보고서 생성을 위해 MergeReport 클래스에 넘겨줄 파일
    report_data = {}
    report_table_data = []

    # DOCX Merge 인스턴스 생성
    report_builder = MergeReport.MergeReport()

    # Update list of satellites of interest
    Update_satellites.Sat_interest().update_satellite_list()

    # 보고서 생성 전 이전일자 보고서 생성시간 검색
    last_report_made_utc = Metadata.Metadata().get_metadata()[iface.REPORT_REF_TIME]
    print("[MakeReport] 보고서를 생성합니다. {} (UTC) 부터 업데이트된 내용을 검색합니다".format(last_report_made_utc))

    # 보고서 작성 데이터 업데이트
    report_data.update({'last_cdm_creation': last_report_made_utc})
    report_data.update(CountNewCDM.CountNewCDM().count_cdm(last_report_made_utc))
    report_data.update(panel_data)

    cdm_list_data = CDMtoNotice.CDMtoNotice()
    report_table_data = cdm_list_data.screened_cdm(last_report_made_utc)
    CDMtoXML.download_cdm_xml(cdm_list_data.list_to_notice)

    report_builder.merge_init()
    report_builder.merge_plain_data(report_data)
    report_builder.merge_table_data("CDM_NO", report_table_data)
    # 보고서 파일의 이름은 KST 시간으로 생성됨
    report_builder.merge_create_report(file_name)

    # 보고서 생성 후 보고서 생성시간 메타데이터 입력
    Metadata.insert_metadata(iface.DAILY_REPORT_UTC, time_val=Time_Converter.datetime_to_str(make_time_utc))

    print("[MAKE REPORT] 보고서 생성 완료")


class MakeReport:
    pass


if __name__ == "__main__":
    make_report()
