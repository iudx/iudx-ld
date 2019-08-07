import xlsxwriter
import json
from xlsxwriter.utility import xl_range
import requests

types = ["../../base_schemas/v0.0.0/providerItem_schema.json", "../../base_schemas/v0.0.0/resourceItem_schema.json", "../../base_schemas/v0.0.0/resourceServer_schema.json", "../../base_schemas/v0.0.0/resourceServerGroup_schema.json"]


opflName = "types.xlsx"

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(opflName)
worksheet = workbook.add_worksheet()

heading_format = workbook.add_format()       # Set properties later.
heading_format.set_bold()

subheading_format = workbook.add_format()       # Set properties later.
subheading_format.set_font_color("blue")


row = 0
col = 0

worksheet.set_column(0,0, 20)
worksheet.set_column(1,1, 80)


worksheet.write(xl_range(row,0,row,0), "itemType", heading_format)
worksheet.write(xl_range(row,1,row,1), "core attributes", heading_format)
row += 1


for tp in types:
    schm = {}
    with open(tp,"r") as f:
        schm = json.load(f)
    worksheet.write(xl_range(row,0,row,0), tp.split("/")[-1].replace("_schema.json",""), subheading_format)
    worksheet.write(xl_range(row,1,row,1), "".join( req+", " for req in schm["required"])[:-2])
    row += 1
    col = 0


workbook.close()
