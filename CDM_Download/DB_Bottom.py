import sqlite3
from CDM_Download import iface


class DB_Bottom:
    conn = ""
    cur = ""
    # def init_DB(self):
    #     face = iface.iface
    #     print(face.LOC_DB)
    #     conn = sqlite3.connect(face.LOC_DB)
    #
    #     cur = conn.cursor()
    #
    #     print("sqlite 3 connected")
    #     cur.execute("CREATE TABLE cdm (TCA  datetime, RELATIVE_POSITION_N  real, RELATIVE_POSITION_R  real, RELATIVE_POSITION_T  real, RELATIVE_SPEED  real, RELATIVE_VELOCITY_N  real, RELATIVE_VELOCITY_R  real, RELATIVE_VELOCITY_T  real, ORIGINATOR  string, MISS_DISTANCE  real, MESSAGE_FOR  string, MESSAGE_ID  string primary key, INSERT_EPOCH  datetime, GID  real, FILENAME  string, CREATION_DATE  datetime, CONSTELLATION  string, COMMENT_EMERGENCY_REPORTABLE  string, COMMENT_SCREENING_OPTION  string, COLLISION_PROBABILITY  real, COLLISION_PROBABILITY_METHOD  real, CDM_ID  int, CCSDS_CDM_VERS  int, SAT1_ACTUAL_OD_SPAN  real, SAT1_AREA_PC  real, SAT1_ATMOSPHERIC_MODEL  string, SAT1_CATALOG_NAME  string, SAT1_CD_AREA_OVER_MASS  real, SAT1_CDRG_DRG  real, SAT1_CDRG_N  real, SAT1_CDRG_NDOT  real, SAT1_CDRG_R  real, SAT1_CDRG_RDOT  real, SAT1_CDRG_T  real, SAT1_CDRG_TDOT  real, SAT1_CN_N  real, SAT1_CN_R  real, SAT1_CN_T  real, SAT1_CNDOT_N  real, SAT1_CNDOT_NDOT  real, SAT1_CNDOT_R  real, SAT1_CNDOT_RDOT  real, SAT1_CNDOT_T  real, SAT1_CNDOT_TDOT  real, SAT1_COMMENT_APOGEE  string, SAT1_COMMENT_COVARIANCE_SCALE_FACTOR  string, SAT1_COMMENT_DCP_DENSITY_FORECAST_UNCERTAINTY  string, SAT1_COMMENT_DCP_SENSITIVITY_VECTOR_POSITION  string, SAT1_COMMENT_DCP_SENSITIVITY_VECTOR_VELOCITY  string, SAT1_COMMENT_EXCLUSION_VOLUME_RADIUS  string, SAT1_COMMENT_INCLINATION  string, SAT1_COMMENT_OPERATOR_HARD_BODY_RADIUS  string, SAT1_COMMENT_PERIGEE  string, SAT1_COMMENT_SCREENING_DATA_SOURCE  string, SAT1_COVARIANCE_METHOD  string, SAT1_CR_AREA_OVER_MASS  real, SAT1_CR_R  real, SAT1_CRDOT_N  real, SAT1_CRDOT_R  real, SAT1_CRDOT_RDOT  real, SAT1_CRDOT_T  real, SAT1_CSRP_DRG  real, SAT1_CSRP_N  real, SAT1_CSRP_NDOT  real, SAT1_CSRP_R  real, SAT1_CSRP_RDOT  real, SAT1_CSRP_SRP  real, SAT1_CSRP_T  real, SAT1_CSRP_TDOT  real, SAT1_CT_R  real, SAT1_CT_T  real, SAT1_CTDOT_N  real, SAT1_CTDOT_R  real, SAT1_CTDOT_RDOT  real, SAT1_CTDOT_T  real, SAT1_CTDOT_TDOT  real, SAT1_EARTH_TIDES  string, SAT1_EPHEMERIS_NAME  string, SAT1_GRAVITY_MODEL  string, SAT1_INTERNATIONAL_DESIGNATOR  string, SAT1_INTRACK_THRUST  string, SAT1_MANEUVERABLE  string, SAT1_N_BODY_PERTURBATIONS  string, SAT1_OBJECT  string, SAT1_OBJECT_DESIGNATOR  int, SAT1_OBJECT_NAME  string, SAT1_OBJECT_TYPE  string, SAT1_OBS_AVAILABLE  int, SAT1_OBS_USED  int, SAT1_OPERATOR_CONTACT_POSITION  string, SAT1_OPERATOR_EMAIL  string, SAT1_OPERATOR_ORGANIZATION  string, SAT1_OPERATOR_PHONE  string, SAT1_RECOMMENDED_OD_SPAN  real, SAT1_REF_FRAME  string, SAT1_RESIDUALS_ACCEPTED  real, SAT1_SEDR  real, SAT1_SOLAR_RAD_PRESSURE  string, SAT1_THRUST_ACCELERATION  real, SAT1_TIME_LASTOB_END  datetime, SAT1_TIME_LASTOB_START  datetime, SAT1_WEIGHTED_RMS  real, SAT1_X  real, SAT1_X_DOT  real, SAT1_Y  real, SAT1_Y_DOT  real, SAT1_Z  real, SAT1_Z_DOT  real, SAT2_ACTUAL_OD_SPAN  real, SAT2_AREA_PC  real, SAT2_ATMOSPHERIC_MODEL  string, SAT2_CATALOG_NAME  string, SAT2_CD_AREA_OVER_MASS  real, SAT2_CDRG_DRG  real, SAT2_CDRG_N  real, SAT2_CDRG_NDOT  real, SAT2_CDRG_R  real, SAT2_CDRG_RDOT  real, SAT2_CDRG_T  real, SAT2_CDRG_TDOT  real, SAT2_CN_N  real, SAT2_CN_R  real, SAT2_CN_T  real, SAT2_CNDOT_N  real, SAT2_CNDOT_NDOT  real, SAT2_CNDOT_R  real, SAT2_CNDOT_RDOT  real, SAT2_CNDOT_T  real, SAT2_CNDOT_TDOT  real, SAT2_COMMENT_APOGEE  string, SAT2_COMMENT_COVARIANCE_SCALE_FACTOR  string, SAT2_COMMENT_DCP_DENSITY_FORECAST_UNCERTAINTY  string, SAT2_COMMENT_DCP_SENSITIVITY_VECTOR_POSITION  string, SAT2_COMMENT_DCP_SENSITIVITY_VECTOR_VELOCITY  string, SAT2_COMMENT_EXCLUSION_VOLUME_RADIUS  string, SAT2_COMMENT_INCLINATION  string, SAT2_COMMENT_OPERATOR_HARD_BODY_RADIUS  string, SAT2_COMMENT_PERIGEE  string, SAT2_COMMENT_SCREENING_DATA_SOURCE  string, SAT2_COVARIANCE_METHOD  string, SAT2_CR_AREA_OVER_MASS  real, SAT2_CR_R  real, SAT2_CRDOT_N  real, SAT2_CRDOT_R  real, SAT2_CRDOT_RDOT  real, SAT2_CRDOT_T  real, SAT2_CSRP_DRG  real, SAT2_CSRP_N  real, SAT2_CSRP_NDOT  real, SAT2_CSRP_R  real, SAT2_CSRP_RDOT  real, SAT2_CSRP_SRP  real, SAT2_CSRP_T  real, SAT2_CSRP_TDOT  real, SAT2_CT_R  real, SAT2_CT_T  real, SAT2_CTDOT_N  real, SAT2_CTDOT_R  real, SAT2_CTDOT_RDOT  real, SAT2_CTDOT_T  real, SAT2_CTDOT_TDOT  real, SAT2_EARTH_TIDES  string, SAT2_EPHEMERIS_NAME  string, SAT2_GRAVITY_MODEL  string, SAT2_INTERNATIONAL_DESIGNATOR  string, SAT2_INTRACK_THRUST  string, SAT2_MANEUVERABLE  string, SAT2_N_BODY_PERTURBATIONS  string, SAT2_OBJECT  string, SAT2_OBJECT_DESIGNATOR  int, SAT2_OBJECT_NAME  string, SAT2_OBJECT_TYPE  string, SAT2_OBS_AVAILABLE  int, SAT2_OBS_USED  int, SAT2_OPERATOR_CONTACT_POSITION  string, SAT2_OPERATOR_EMAIL  string, SAT2_OPERATOR_ORGANIZATION  string, SAT2_OPERATOR_PHONE  string, SAT2_RECOMMENDED_OD_SPAN  real, SAT2_REF_FRAME  string, SAT2_RESIDUALS_ACCEPTED  real, SAT2_SEDR  real, SAT2_SOLAR_RAD_PRESSURE  string, SAT2_THRUST_ACCELERATION  real, SAT2_TIME_LASTOB_END  datetime, SAT2_TIME_LASTOB_START  datetime, SAT2_WEIGHTED_RMS  real, SAT2_X  real, SAT2_X_DOT  real, SAT2_Y  real, SAT2_Y_DOT  real, SAT2_Z  real, SAT2_Z_DOT  real, eventnum int, event_year int)")
    #     conn.close()

    def db_init(self, db_loc):
        # print("[DB_BOTTOM] db open at {}".format(db_loc))
        self.conn = sqlite3.connect(db_loc)
        self.cur = self.conn.cursor()

    def db_close(self):
        self.conn.close()
        self.conn = None
        self.cur = None

    def db_simple_execute(self, query, db):
        self.db_init(db)

        rows = self.cur.execute(query).fetchall()

        self.conn.commit()
        self.db_close()

        return rows




if __name__ == "__main__":
    DB_Bottom().init_DB()