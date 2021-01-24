sql_delete_report = "delete from metadata where target = ? and updatetime = ?"

# Decay 메시지 입력
sql_insert_decay = "INSERT INTO decay (norad_cat_id, object_number, object_name, intldes, object_id ,rcs, rcs_size, country, msg_epoch, decay_epoch, source, msg_type, precedence) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)"

# 예보된 Decay 수
sql_count_decay = "select count(*) from (select norad_cat_id, decay_epoch, max(msg_epoch) from decay where decay_epoch > ? and decay_epoch < ? group by norad_cat_id)"

# 출력할 Decay 메시지 검색
sql_query_decay = "select norad_cat_id, decay_epoch, max(msg_epoch), source, satcat.satellite_name  from decay, satcat where decay.norad_cat_id = satcat.norad and decay_epoch > ? and decay_epoch < ? group by norad_cat_id order by norad_cat_id"

# SATCAT 데이터 쿼리
sql_payload_orbit = 'select count(*) from satcat where payload_flag="*" and operational_status_code is not "D"'
sql_payload_decayed = 'select count(*) from satcat where payload_flag="*" and operational_status_code is "D"'
sql_debris_orbit = 'select count(*) from satcat where payload_flag="" and operational_status_code is not "D"'
sql_debris_decayed = 'select count(*) from satcat where payload_flag="" and operational_status_code is "D"'
sql_active_sat = 'select count(*) from satcat where operational_status_code not in ("D", "-", "")'
sql_count_country = 'select count(*) from satcat where ownership= ? and operational_status_code not in ("D", "-", "")'

class iface_SQL:
    orbit_type_period_criteria = 225  # see Space-track.org Spaceflight safety handbook
    orbit_leo_period_criteria = "< 225"
    orbit_geo_period_criteria = ">= 225"
    miss_distance_leo = 1000
    miss_distance_geo = 5000
    probability_criteria = 0.000001
    SAT_LIST = []
    sql_new_cdm = "SELECT sat1_object_designator, sat1_international_designator, sat1_object_name, count(message_id) " \
                  "FROM cdm WHERE creation_date > ? " \
                  "GROUP BY sat1_object_designator"

    sql_new_cdm_met = "SELECT sat1_object_designator, sat1_international_designator, sat1_object_name, count(message_id) " \
                      "FROM cdm, satcat " \
                      "WHERE cdm.sat1_object_designator = satcat.norad and satcat.orbital_period {} and cdm.miss_distance < ? and creation_date > ? " \
                      "GROUP BY sat1_object_designator"

    ####
    sql_get_satellite_list = "SELECT international_designator from satellites"

    ####
    sql_sat_list_query = "select distinct sat1_object_designator, sat1_international_designator, sat1_object_name from cdm"
    sql_sat_list_update = "insert into satellites (norad, international_designator, satellite_name) values (?, ?, ?)"

    # 전파대상 cdm 검색 LEO
    sql_notice_query_leo = "select message_id from satcat, " \
                           "(select message_id, sat1_international_designator, miss_distance, collision_probability, eventnum, max(creation_date) " \
                           "from cdm where creation_date > ? group by eventnum) o " \
                           "where satcat.international_designator = o.sat1_international_designator and satcat.orbital_period {} and " \
                           "o.miss_distance < {} and o.collision_probability > {}".format(orbit_leo_period_criteria,
                                                                                          miss_distance_leo,
                                                                                          probability_criteria)

    # 전파대상 cdm 검색 GEO
    sql_notice_query_geo = "select message_id from satcat, " \
                           "(select message_id, sat1_international_designator, miss_distance, collision_probability, eventnum, max(creation_date) " \
                           "from cdm where creation_date > ? group by eventnum) o " \
                           "where satcat.international_designator = o.sat1_international_designator and " \
                           "satcat.orbital_period {} and o.miss_distance < {}".format(orbit_geo_period_criteria,
                                                                                      miss_distance_geo)

    # CDM 스크리닝
    sql_screen_cdm = "SELECT creation_date, message_id, satcat.orbital_period, miss_distance, collision_probability, tca, eventnum, event_year, sat1_object_name, sat1_object_designator, sat2_object_name, sat2_object_designator " \
                     "FROM cdm, satcat " \
                     "WHERE cdm.sat1_international_designator = satcat.international_designator and creation_date > ? and satcat.orbital_period {} and miss_distance < {} " \
                     "ORDER BY eventnum desc"


