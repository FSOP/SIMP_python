## class iface
##인터페이스 역할
##프로그램 전체에서 사용되는 변수 정의됨
##################################

LOC_MAIN_UI = "..\\DataFiles\\SIMP_main.ui"

# metadata에 사용
LAST_CDM_UTC = "LAST_CDM_UTC"
SATCAT_UTC = "SATCAT_UTC"
DAILY_REPORT_UTC = "DAILY_REPORT_UTC"
REPORT_REF_TIME = "REPORT_REF_TIME"

LOC_DB_CDM = "..\\DataFiles\\CDM.txt"
LOC_DB_METADATA = "..\\DataFiles\\Metadata.txt"
LOC_REPORT_TEMPLATE = "..\\DataFiles\\Template.docx"
LOC_DAILY_REPORT = "..\\Result_report\\{}_DailyReport.docx"
LOC_CDM_XML = "..\\CDM_XML\\{}.xml"
LOC_CONFIG_TXT = "..\\..\\config.txt"

baseSPurl = "https://www.space-track.org/"

query_limit = 500
queryCDM_creation = "expandedspacedata/query/class/cdm/CREATION_DATE/>{}/orderby/CONSTELLATION asc/limit/" + str(query_limit) + "/format/json/emptyresult/show"
queryCDM_tca = "expandedspacedata/query/class/cdm/TCA/>{}/orderby/CONSTELLATION asc/limit/" + str(query_limit) + "/format/json/emptyresult/show"
queryDecay = "basicspacedata/query/class/decay/INSERT_EPOCH/>{}/orderby/DECAY_EPOCH desc/limit/500/format/json/emptyresult/show"
queryCDM_xml = "expandedspacedata/query/class/cdm/MESSAGE_ID/{}/orderby/CONSTELLATION%20asc/format/xml/emptyresult/show"
SPauthurl = "/ajaxauth/login"
SPauthformat = "identity={}&password={}"
URL_SATCAT = "http://celestrak.com/pub/satcat.txt"

Time_format = "%Y-%m-%dT%H:%M:%S"

META_DATA_TIME_UTC = "2021-01-01T00:00:00"
META_DATA_LIST = {
    LAST_CDM_UTC: META_DATA_TIME_UTC,
    SATCAT_UTC: META_DATA_TIME_UTC,
    DAILY_REPORT_UTC: META_DATA_TIME_UTC,
    REPORT_REF_TIME: META_DATA_TIME_UTC
}


class iface:


    def __init__(self):
        LOC_DB = "test"
        pass
