import requests

class CelestrakCAT:
    def get_SATCAT(self):
        url = "http://celestrak.com/pub/satcat.txt"

        print("[Celestrak_CAT] SATCAT 다운로드 중")

        with requests.Session() as session:
            session = requests.Session()
            resq = session.get(url)
            print("[Celestrak_CAT] SATCAT 다운로드 완료")
            data = resq.text

        return data



if __name__ == "__main__":
    CelestrakCAT().get_SATCAT()
