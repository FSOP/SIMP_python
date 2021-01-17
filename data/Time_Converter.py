from CDM_Download import iface
import datetime


def utc_to_kst_str(utc_str, time_format=iface.Time_format):
    utc_val = None
    if isinstance(utc_str, str):
        return datetime_to_str(str_to_datetime(utc_str) + datetime.timedelta(hours=9), time_format=time_format)
    elif isinstance(utc_str, datetime.datetime):
        return datetime_to_str(utc_str + datetime.timedelta(hours=9), time_format=time_format)


def str_to_datetime(str_val, time_format=iface.Time_format):
    if len(str_val) > 19:
        str_val = str_val[:19]

    if " " in str_val:
        str_val = str_val.replace(" ", "T")

    return datetime.datetime.strptime(str_val, time_format)


def datetime_to_str(datetime_val, time_format=iface.Time_format):
    return datetime.datetime.strftime(datetime_val, time_format)
