import requests
from CDM_Download import iface


def url_encoder(url):
    return url.replace(" ", "%20").replace(">", "%3E").replace("<", "3C")


class SPlogin:
    def __init__(self):
        self.session = None
        pass
        # self.session = None

    def get_login(self, spid, sppw):
        login_data = {'identity': spid, 'password': sppw}

        self.session = requests.Session()

        # with requests.Session() as session:
        #     resp = session.post(self.baseSP + self.authSP, data=login_data)
        #     print(login_data)
        #     print(resp)

        resp = self.session.post(iface.baseSPurl + iface.SPauthurl, data=login_data)
        # print(resp.status_code)
        # print(resp)
        if resp.status_code != 200:
            print("[SPLogin] Space-Track 로그인 오류")
            print("[SPLogin] status code: " + str(resp.status_code))
            print("[SPLogin] 접속 아이디: {}".format(login_data['identity']))
        else:
            print("[SPLogin] SpaceTrack 로그인 성공, 접속계정: {}".format(login_data['identity']))

    def sp_close(self):
        if self.session is not None:
            self.session.close()

    def get_sp_data(self, query_sp):
        if self.session is None:
            print("[SP REQUEST] 로그인 정보 없음")

        print("[SP CDM DOWN] SpaceTrack 요청 url: {}".format(iface.baseSPurl + url_encoder(query_sp)))
        resp = self.session.get(iface.baseSPurl + url_encoder(query_sp))
        # print(resq.text)

        return resp.text

    def get_cdm_xml(self, message_id):
        resp = self.session.get(iface.baseSPurl + iface.queryCDM_xml.format(message_id))
        return resp.text
