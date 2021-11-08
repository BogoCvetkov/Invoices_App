import pandas as pd

# This Module is responsible for manipulating the excel file. It can create different sheets
# and store the scraped data in them.#.

class TablesTool:

    headers = ['Transaction ID','Date','Amount','Payment Method','Payment REF','Status','Status1','VAT Invoice ID','Action']

    def __init__(self,table_file,vat_info):
        self.writer = pd.ExcelWriter(table_file,engine="xlsxwriter")
        self.vat_info=vat_info

    def new_sheet(self,data,name):
        df = pd.DataFrame(data, columns=self.headers)
        condition_col = [self.vat_info if x[-4:] in ["8612", "2424", "5303","1551","1746","9495","1284"] else "" for x in df["Payment Method"]]
        df["Company"] = condition_col
        df = df.drop(["Action", "Status1"], axis=1)
        df.to_excel(self.writer, sheet_name=name)

    def close_file(self):
        self.writer.save()
        self.writer.close()