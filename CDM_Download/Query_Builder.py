from CDM_Download import iface
from data import Metadata
class Query_Builder:

    def sp_cdm_query_byCreation(self):
        #utc_last_cdm_creation = self.face.utc_last_cdm_creation
        utc_last_cdm_creation = Metadata.Metadata().get_metadata()[iface.LAST_CDM_UTC]

        query = iface.queryCDM_creation.format(utc_last_cdm_creation)

        print("[QueryBuilder] 생성 URL {}".format(query))

        return query

    def sp_cdm_query(self, ref, val):
        query_val = ""
        if ref == "creation_date":
            query_val = iface.queryCDM_creation.format(val)

        elif ref == "tca":
            query_val = iface.queryCDM_tca.format(val)

        else:
            print("[QueryBuilder] 잘못된 ref 값입니다.")
            return None

        print("[QueryBuilder] 생성 URL {}".format(query_val))
        return query_val

