from CDM_Download import iface
import datetime


def utc_to_kst_str(utc_str, time_format=iface.Time_format):
    utc_val = None
    if isinstance(utc_str, str):
        return datetime_to_str(str_to_datetime(utc_str) + datetime.timedelta(hours=9), time_format=time_format)
    elif isinstance(utc_str, datetime.datetime):
        return datetime_to_str(utc_str + datetime.timedelta(hours=9), time_format=time_format)


def kst_to_utc_str(kst_str, time_format=iface.Time_format_2):
    if isinstance(kst_str, str):
        return datetime_to_str(datetime.datetime.strptime(kst_str, time_format) - datetime.timedelta(hours=9), time_format=iface.Time_format)
    elif isinstance(kst_str, datetime.datetime):
        return datetime_to_str(kst_str - datetime.timedelta(hours=9), time_format=iface.Time_format)


def str_to_datetime(str_val, time_format=iface.Time_format):
    if len(str_val) > 19:
        str_val = str_val[:19]

    if " " in str_val:
        str_val = str_val.replace(" ", "T")

    return datetime.datetime.strptime(str_val, time_format)


def stk_to_datetime(access_time, time_format=iface.Time_format_stk):
    return datetime.datetime.strptime(access_time, time_format)


def datetime_to_str(datetime_val, time_format=iface.Time_format):
    return datetime.datetime.strftime(datetime_val, time_format)
