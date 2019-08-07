import xlsxwriter
import json
from xlsxwriter.utility import xl_range
import requests

schm_path = "../../base_schemas/v0.0.0/common_defs.json"




schmList = schm_path.split("/")
name = schmList[-1][:-4] + "xlsx"
version = schmList[-2]

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(name)
worksheet = workbook.add_worksheet()

heading_format = workbook.add_format()       # Set properties later.
heading_format.set_bold()

subheading_format = workbook.add_format()       # Set properties later.
subheading_format.set_font_color("blue")

schema = {}
with open(schm_path,"r") as f:
    schema = json.load(f)["definitions"]
    #schema.pop("id")

def writeType(tp, row):
    worksheet.write(xl_range(row,1,row,1), "type", subheading_format)
    worksheet.write(xl_range(row,2,row,2), tp)

def writeValueType(tp, row):
    worksheet.write(xl_range(row,1,row,1), "value-type", subheading_format)
    worksheet.write(xl_range(row,2,row,2), tp)

def writeDescribes(dscr, row):
    worksheet.write(xl_range(row,1,row,1), "description", subheading_format)
    worksheet.write(xl_range(row,2,row,2), dscr)

def findType(attrObj):
    if "allOf" in attrObj.keys():
        if(attrObj["allOf"][0]["$ref"].split("/")[-1] in ["Relationship", "Property", "GeoProperty", "TimeProperty", "QuantitativeProperty"]):
            return attrObj["allOf"][0]["$ref"].split("/")[-1]
    if "$ref" in attrObj.keys():
        if(attrObj["$ref"].split("/")[-1] in ["Relationship", "Property", "GeoProperty", "TimeProperty", "QuantitativeProperty"]):
            return attrObj["$ref"].split("/")[-1]
        else:
            srcSchema = requests.get(attrObj["$ref"]).json()
            jsonPtr = attrObj["$ref"].split("#/")[1].split("/")
            jsonPtrVal = srcSchema[jsonPtr[0]][jsonPtr[1]]
            if("allOf" in jsonPtrVal.keys()):
                return jsonPtrVal["allOf"][0]["$ref"].split("/")[-1]
            elif("$ref" in jsonPtrVal.keys()):
                return jsonPtrVal["$ref"].split("/")[-1]
    return ""


def findValueType(attrObj):
    if("type" in attrObj.keys()):
        if( attrObj["type"] != "object"):
            return attrObj["type"]
        else:
            if ("properties" in attrObj.keys()):
                if( "value" in attrObj["properties"]):
                    return attrObj["properties"]["value"]["type"]
    elif("$ref" in attrObj.keys()):
        if(attrObj["$ref"].split("/")[-1] in ["Relationship", "Property", "GeoProperty", "TimeProperty", "QuantitativeProperty"]):
            tp = attrObj["$ref"].split("/")[-1]
            if tp == "Relationship":
                return "iri"
            if tp == "Property":
                return "string / object / number / array "
            if tp == "GeoProperty":
                return "GeoJSON or address object"
            if tp == "TimeProperty":
                return "Timestamp in date-time format"
        else:
            srcSchema = requests.get(attrObj["$ref"]).json()
            jsonPtr = attrObj["$ref"].split("#/")[1].split("/")
            return findValueType(srcSchema[jsonPtr[0]][jsonPtr[1]])


def findDescr(attrObj):
    if("describes" in attrObj.keys()):
        return attrObj["describes"]
    elif("$ref" in attrObj.keys()):
        srcSchema = requests.get(attrObj["$ref"]).json()
        jsonPtr = attrObj["$ref"].split("#/")[1].split("/")
        return findDescr(srcSchema[jsonPtr[0]][jsonPtr[1]])
    elif("allOf" in attrObj.keys()):
        srcSchema = requests.get(attrObj["allOf"][0]["$ref"]).json()
        jsonPtr = attrObj["allOf"][0]["$ref"].split("#/")[1].split("/")
        return findDescr(srcSchema[jsonPtr[0]][jsonPtr[1]])




row = 0
col = 0

worksheet.set_column(0,0, 20)
worksheet.set_column(1,1, 20)
worksheet.set_column(2,2, 40)


worksheet.write(xl_range(row,0,row,0), "Field Name", heading_format)
worksheet.write(xl_range(row,1,row,1), "Attributes", heading_format)
worksheet.write(xl_range(row,2,row,2), "Value", heading_format)
row += 1

for attr in schema:
    worksheet.set_row(row,20)
    worksheet.set_row(row+1,20)
    worksheet.set_row(row+2,20)
    worksheet.set_row(row+3,20)
    worksheet.merge_range(xl_range(row,0, row+3, 0), attr, heading_format)
    writeType(findType(schema[attr]), row+1)
    writeDescribes(findDescr(schema[attr]), row+2)
    writeValueType(findValueType(schema[attr]), row+3)

    row += 4
    col = 0



workbook.close()
