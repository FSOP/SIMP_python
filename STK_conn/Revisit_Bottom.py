# Revisit Core 에서 STK 없이 단순 연산만을 처리하는 function
from data import Time_Converter
from STK_conn import int_STK
import datetime


def get_sample_data(fname):
    with open("..\\DataFiles\\{}".format(fname)) as fp:
        data = fp.read()
    return data


def core_get_gaps(dict_per_sat, scenario_start_str, scenario_stop_str):
    gap_per_sat = {}
    scenario_start = Time_Converter.stk_to_datetime(scenario_start_str, time_format='%d %b %Y %H:%M:%S')
    scenario_stop = Time_Converter.stk_to_datetime(scenario_stop_str, time_format='%d %b %Y %H:%M:%S')

    for p in dict_per_sat.keys():
        dict_per_sat[p][0].append(scenario_stop)
        dict_per_sat[p][1].insert(0, scenario_start)

        gap_per_sat[p] = [[], []]
        for q, z in zip(dict_per_sat[p][1], dict_per_sat[p][0]):
            gap_per_sat[p][0].append(q + datetime.timedelta(minutes=int_STK.margin_for_gap_min))
            gap_per_sat[p][1].append(z - datetime.timedelta(minutes=int_STK.margin_for_gap_min))

    return gap_per_sat


# stk Individual Strands Access 분석 결과를 {'sat':[ [access start time ], [access stop time] ] } 형태로 반환 ( Core 함수 )
def core_strands_to_list(data):
    # 반환을 위한 Dictionary 변수
    sat_access = {}

    for p in data.splitlines():
        # 아무런 결과가 없는 행은 지나침
        if not p:
            continue

        # 날짜 항목이 '한 자리' 인 경우와 '두 자리 수' 인 경우 공백의 수가 달라서 처리에 애로가 있음, remover 함수로 제거
        val = remover(p.split(" "))

        # 분석 대상 Origin Object 처리
        # print(val)
        org_sat = val[2].split("/")[1]

        # Root Object 는 분석에서 제외
        if org_sat == 'SAT_':
            continue

        # Object 키가 없는 경우 empty list 정의
        if org_sat not in sat_access.keys():
            sat_access[org_sat] = [[], []]

        i = -1
        for q in val[5:]:
            i += 1
            # index 는 몇 번째 Access 요일인지를 나타냄
            index = int(i/4)
            # slot 은 날짜, 월, 연도, 시간 을 가르킴
            slot = i % 4

            # 값이 날짜인 경우
            if slot == 0:
                time = q + " "
            # 값이 월 인 경우
            if slot == 1:
                time += (q + " ")
            # 값이 연도 인 경우
            if slot == 2:
                time += (q + " ")
            # 값이 시간 인 경우
            if slot == 3:
                time += q
                # index 가 짝수인 경우 Access 시작 시간임 나타냄
                if iseven(index):
                    sat_access[org_sat][0].append(Time_Converter.stk_to_datetime(time))
                # index 가 홀수인 경우 Access 종료 시간을 나타냄
                else:
                    sat_access[org_sat][1].append(Time_Converter.stk_to_datetime(time))

    # 반환 값은 후 처리를 위해 datetime 형식으로 반환됨
    return sat_access


def core_merge_time(val):
    list_start = val[0]
    list_stop = val[1]

    list_start.sort()
    list_stop.sort()

    trash = datetime.datetime.strptime("1970-01-01", "%Y-%m-%d")

    list_stop.insert(0, trash)
    list_start.append(trash)

    for i, j in zip(list_start, list_stop):
        if i == trash: continue
        if j > i:
            list_start.remove(i)
            list_stop.remove(j)

    list_start.pop(-1)
    list_stop.pop(0)

    return [list_start, list_stop]

def core_second_filter(dict_gaps, dict_access):
    dict_result = [[], []]
    for sat in dict_gaps.keys():
        for ac_start, ac_stop in zip(dict_access[sat][0], dict_access[sat][1]):
            for gap_start, gap_stop in zip(dict_gaps[sat][0], dict_gaps[sat][1]):
                if ac_start > gap_start and ac_stop < gap_stop:
                    dict_result[0].append(ac_start)
                    dict_result[1].append(ac_stop)
                    break
    return dict_result


# 최종 Access 결과로 평균 최대 최소 재방문 주기 계산
def core_revisit_time(dict_access, scenario_start, scenario_stop):
    gaps = []
    num_access = len(dict_access[0])
    datetime_scenario_start = Time_Converter.stk_to_datetime(scenario_start, time_format='%d %b %Y %H:%M:%S')
    datetime_scenario_stop = Time_Converter.stk_to_datetime(scenario_stop, time_format='%d %b %Y %H:%M:%S')
    len_time = (datetime_scenario_stop - datetime_scenario_start).total_seconds()

    # print("length of scenario: "+ str(len_time))
    dict_access[1].insert(0, datetime_scenario_start)
    dict_access[0].append(datetime_scenario_stop)
    for start_time, stop_time in zip(dict_access[0], dict_access[1]):
        gaps.append((start_time - stop_time).total_seconds())

    if len(gaps)==1:
        return -1
    revisit_avg = sum(gaps) / (num_access+1)
    return revisit_avg, max(gaps), min(gaps)


def core_get_fom(val_str):
    return val_str[val_str.find("Average (sec)"):].split("\"")[1].split(",")


def list_popping(list_val, list_to_pop):
    list_to_pop.sort(reverse=True)
    for p in list_to_pop:
        list_val.pop(p)
    return list_val


def list_adder(list_val, number=1):
    ret_val = []
    for p in list_val:
        if not isinstance(p, int):
            break
        ret_val.append(p + number)
    return ret_val

# 날짜의 자리 수에 따라 발생하는 에러 처리를 위해 '' 공백 제거
def remover(val):
    return_val = []
    for p in val:
        if p != '':
            return_val.append(p)
    return return_val

# 짝수 검사 함수
def iseven(val):
    if (val % 2) == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    start = [1, 5, 15, 17, 30, 32, 45]
    stop = [7, 10, 20, 25, 40, 35, 50]
    print(start)
    print(stop)
    core_merge_time(start, stop)
