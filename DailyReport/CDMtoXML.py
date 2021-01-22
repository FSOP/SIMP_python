from CDM_Download import Web_SP, iface
from data import ReadConfig


def download_cdm_xml(cdm_list):
    conf = ReadConfig.read_conf()
    sp = Web_SP.SPlogin()
    sp.get_login(spid=conf['spid'], sppw=conf['sppw'])
    # cdm_data = sp.get_cdm_xml(cdm_list)

    for p in cdm_list:
        with open(iface.LOC_CDM_XML.format(p), 'w') as fp:
            fp.write(sp.get_cdm_xml(p))

    sp.sp_close()
