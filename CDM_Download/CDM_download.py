#
# CDM 다운로드, 이벤트 분류 를 수행하는 메인 클래스
#####################################
from CDM_Download import EventCounter, Query_Builder, iface, Insert_CDM, Web_SP
from data import Metadata, ReadConfig


def download():
    # CDM 업데이트 전 DB에 남아있는 CDM 수 계수
    Metadata.get_cdm_count()

    # 마지막 CDM Creation_Date 를 검색하여 Space-Track.org 에 검색 쿼리문 제작
    sp_query = Query_Builder.Query_Builder().sp_cdm_query_byCreation()

    # tca 를 기준으로 CDM 다운로드 받을 때 사용
    # sp_query = Query_Builder.Query_Builder().sp_cdm_query("tca", "2020-01-01")

    # Config 파일에서 SpaceTrack 계정정보 불러오기
    conf = ReadConfig.read_conf()

    # SpaceTrack 로그인 및 CDM 다운로드 수행
    SP = Web_SP.SPlogin()
    SP.get_login(spid=conf['spid'], sppw=conf['sppw'])
    cdm_data = SP.get_sp_cdm(sp_query)
    SP.sp_close()

    # 테스트를 위해 텍스트로 저장된 CDM 불러옴
    # 테스트가 필요한 경우 주석 해제
    # cdm_data = GET_TEST_CDM.get_test_cdm()

    # 다운로드 받은 CDM 을 데이터베이스에 입력
    Insert_CDM.insert_CDM().insert_cdm(cdm_data)

    # CDM 이벤트별로 분류
    EventCounter.EventCounter().event_count()

    # CDM 업데이트 후 DB에 남은 CDM 수 계수
    Metadata.get_cdm_count()

    print("[CDM DOWNLOAD MAIN] CDM 다운로드 완료")


class CDM_Download(object):
    pass


# ress the green button in the gutter to run the script.
if __name__ == '__main__':
    download()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
