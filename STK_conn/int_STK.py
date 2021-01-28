# STK Connect 명령어 인터페이스

LOC_DB_STK_META = "..\\DataFiles\\STK_meta.txt"
LOC_DB_STK_RESULT = "..\\DataFiles\\Analysis\\{}.txt"
LOC_STK_OBJECT = "..\\DataFiles\\Objects\\{}.at"
LOC_LOG = "..\\Log\\Log.txt"
LOC_REPORT_TEMPLATE = "..\\DataFiles\\Analysis_Template.docx"
LOC_ANALYSIS_REPORT = "..\\AnalysisReport\\{}_{}.docx"

conn_get_chain_access = "Chains_R */Chain/{} Strands"
get_list_object = "AllInstanceNames /"
get_facility_position = "Position */Facility/{}"
insert_facility = "New / */Facility {}"
set_facility = "SetPosition */Facility/{} Geodetic {} {} {}"

stk_scenario_interval = 'SetAnalysisTimePeriod * "{}" "{}"'
stk_new_object = 'New / */{} {}'
stk_set_position = 'SetPosition */Facility/{} Geodetic {} {} {}'
stk_chain_autocomp_off = 'Chains */Chain/{} AutoRecompute off'
stk_add_chain = 'Chains */Chain/{} Add {}'
stk_add_constellation = 'Chains */Constellation/{} Add {}'
stk_load_obj = 'Load */{} "{}"'
stk_cov_autocomp_off = "Cov */CoverageDefinition/{} AutoRecompute off"
stk_unload_obj = "Unload / */{}"


shell_setting = {
            'altitude': [],  # 1
            'inclination': [],  # 2
            'sats': [],  # 3
            'scenario_start': '',  # 4
            'scenario_stop': '',  # 5
            'Area': [],  # 6
            'primary': [],  # 7
            'secondary': [],  # 8
            'inter_plane_space': [],  # 9
            'sensor_type': [],  # 10
            'sensor_set': [],  # incidence angle -> elevation angle   #11
            'grid': []  # km
        }

margin_for_gap_min = 5
