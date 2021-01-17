from CDM_Download import Web_SP
from data import ReadConfig


def download_cdm_xml(cdm_list):
    conf = ReadConfig.read_conf()
    sp = Web_SP.SPlogin()
    sp.get_login(spid=conf['spid'], sppw=conf['sppw'])
    cdm_data = sp.get_cdm_xml(cdm_list)
    sp.sp_close()
