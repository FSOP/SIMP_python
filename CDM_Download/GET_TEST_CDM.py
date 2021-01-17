def get_test_cdm():
    fpath = "data\\3CDM json.txt"

    with open(fpath) as fp:
        data = fp.read()
        #print(data)

    return data


if __name__ == "__main__":
    get_test_cdm()