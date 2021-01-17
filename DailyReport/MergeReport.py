# Docx
# 보고서 생성 클래스
###############
from mailmerge import MailMerge
from CDM_Download import iface


class MergeReport:
    document = None

    def merge_init(self):
        template = iface.LOC_REPORT_TEMPLATE
        self.document = MailMerge(template)

    def merge_table_data(self, anchor, data):
        self.document.merge_rows(anchor, data)

    def merge_plain_data(self, data):
        self.document.merge_templates([data], separator='page_break')

    def merge_create_report(self, fname):
        self.document.write(iface.LOC_DAILY_REPORT.format(fname))

    def merge_test(self):
        template = "..\\data\\Template.docx"

        document = MailMerge(template)
        print(document.get_merge_fields())

        data = {
            'cdm_total': "232",
            'made_by': "최인수",
            'KOMPSAT-2': "123",
            'asdfasd': '12321'
        }

        row = {
            'last_cdm_creation': "test",
            'CDM_NO': "test",
            'CREATION_DATE': "test",
            'PROBABILITY': "test",
            'TCA': "test",
            'EVENTNUM': "test",
            'MISS_DISTANCE': "test",
            'SAT1_NAME': "test",
            'SAT1_NORAD': "test",
        }

        rows = [row, row]

        print(type(data))
        document.merge_rows('CDM_NO', rows)
        document.merge_templates([data], separator='page_break')

        document.write("..\\data\\result.docx")


if __name__ == "__main__":
    MergeReport().merge_test()
