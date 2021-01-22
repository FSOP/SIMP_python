import requests


def get_SATCAT():
    url = "http://celestrak.com/pub/satcat.txt"

    print("[Celestrak_CAT] SATCAT 다운로드 중")

    with requests.Session() as session:
        session = requests.Session()
        resq = session.get(url)
        print("[Celestrak_CAT] SATCAT 다운로드 완료")
        data = resq.text

    return data


class CelestrakCAT:
    pass


if __name__ == "__main__":
    get_SATCAT()
