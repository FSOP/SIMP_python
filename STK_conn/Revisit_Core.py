# 표적의 우선순위를 고려한 재방문주기 분석 - 계산 클래스
# 분석을 위한 모든 조건이 갖추어진 상태를 가정함
#
# 1. 모든 조건: 아래의 Object 들이 STK 시나리오 상에 존재하는 상태
# 1.1. Constellation: Sensor, Primary_Target
#       - Sensor Constellation: 각 위성에 부착된 Sensor 들이 모두 포함된 Constellation (Root 위성 제외)
#       - Primary_Target Constellation: 1순위 표적 (Facility)로 구성된 Constellation
# 1.2. Facility: Secondary Target(Selected on Panel)
# 1.3. Chain: Primary_Target, Secondary_Target(각각의 Facility 에 대응하는 Chain Object 가 존재해야 함)
#       - Primary_Target Chain: Sensor Constellation - Primary_Target Constellation 이 순서대로 추가된 Chain
#       - Secondary_Target Chain: 각 Secondary Target Facility - Sensor Constellation 이 순서대로 추가된 Chain
#
# 2. 분석 순서
# 2.1. Primary_Target Chain 을 Strands 분석하여 각 위성별로 Primary Target 과의 Access 시간을 구함
#       - Strands Access 밖에 계산되지 않으므로, [각 위성 - 각 표적] 을 [각 위성 - 표적군] 으로 변환해야 함 ( core_merge_time 함수 )
# 2.2. 위의 Access 시간의 전, 후 10 분의 시간을 추가하여 '1순위 표적 우선시간' 을 계산 ( core_get_gaps 함수)
# 2.3. 전체 시나리오 시간에서 '1순위 표적 우선시간' 을 제외한 시간을 '2순위 표적 가능시간' 을 계산
# 2.4. Secondary_Target Chain 의 Strands Access 시간 계산
# 2.5. '2순위 표적 가능시간' 에 해당하는 2순위 표적 Access 필터링 ( core_second_filter 함수)
# 2.6. 각 위성의 Access 시간을 Complete Chain Access 로 변환 ( core_merge_time 함수 )
# 2.6. 최대/최소/평균 재방문주기 계산
######################################

from STK_conn import STK_bottom, int_STK, Revisit_Bottom


def get_primary_access():
    stk_scenario_start = "12 Jan 2021 03:00:00.000"
    stk_scenario_stop = "15 Jan 2021 03:00:00.000"
    list_second_target = ["Dokdo"]

    stk = STK_bottom.bottom_stk()

    # raw_primary_access = stk.simple_connect(int_STK.conn_get_chain_access.format("Primary"))
    # dict_primary_access = Revisit_Bottom.core_strands_to_list(raw_primary_access)

    # sample 데이터 불러옴
    dict_primary_access = Revisit_Bottom.core_strands_to_list(Revisit_Bottom.get_sample_data("stk_sample_2.txt"))

    # 1순위 표적에 대한 Access Time 형식을 [각 위성 - 각 표적] 을 [각 위성 - 표적군] 으로 변환
    for p in dict_primary_access.keys():
        dict_primary_access[p] = Revisit_Bottom.core_merge_time(dict_primary_access[p])

    # 분석 결과로 GAP 시간 구함
    dict_gaps = Revisit_Bottom.core_get_gaps(dict_primary_access, stk_scenario_start, stk_scenario_stop )

    print("primary_access")
    print(dict_primary_access)
    print("gap time")
    print(dict_gaps)

    for p in list_second_target:
        # raw_second_access = stk.simple_connect(int_STK.conn_get_chain_access.format("D_{}".format(p)))
        # dict_second_access = Revisit_Bottom.core_strands_to_list(raw_second_access)

        dict_second_access = Revisit_Bottom.core_strands_to_list(Revisit_Bottom.get_sample_data("stk_sample_3.txt"))
        print("secondary_access")
        print(dict_second_access)

        # secondary Target 임무 할당 가능시간 [[access_start], [access_stop]]
        filtered_access = Revisit_Bottom.core_merge_time(Revisit_Bottom.core_second_filter(dict_gaps, dict_second_access))
        print("filtered_secondary_access")
        print(filtered_access)
        print("number of access: {}".format(len(filtered_access[0])))

        print(Revisit_Bottom.core_revisit_time(filtered_access, stk_scenario_start, stk_scenario_stop))


if __name__ == "__main__":
    get_primary_access()
