from CDM_Download import iface


def read_conf():
    with open(iface.LOC_CONFIG_TXT) as fp:
        dict_conf = {}
        data = fp.read()

        for p in data.splitlines():
            row = p.split("=")
            dict_conf[row[0].strip()] = row[1].strip()

    print(dict_conf)
    return dict_conf


