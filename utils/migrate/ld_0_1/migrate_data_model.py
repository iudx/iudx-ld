import json
import os
from os import listdir
from os.path import isfile, join
import re


data_model = "../../../data_models/WiFi/hotspot/wifi_hotspot_Pune_0.json"

dm_list = data_model.split("/")
dm_name = dm_list[-1]
path_to_dm = dm_list[dm_list.index("data_models"):-1]
path_to_dm_folder = "".join(a+"/" for a in dm_list[:-1])
folder_path = "".join(a+"/" for a in path_to_dm)
dm_context_file_name =  dm_list[-2] + "_context.json"
path_to_dm_context = "".join(a + "/" for a in dm_list[:-1]) + dm_context_file_name


core_context = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_context.json"
common_context = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/common_context.json"
miscSchemaOrgDefs = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/miscSchemaOrgDefs.json"
geometry_schema = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/geometry-schema.json"

dm_url = "https://raw.githubusercontent.com/iudx/iudx-ld/master/" + folder_path + dm_name + "#/properties/"
dm_context_url = "https://raw.githubusercontent.com/iudx/iudx-ld/master/" + folder_path + dm_context_file_name + "#/"



unitsDict = {}
propsDict = {}

unitsFile = "./units.txt"
propsFile = "./props.txt"

propTypeLink = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_defs.json#/definitions/"

with open(unitsFile,"r") as f:
    rows = f.readlines()[1:]
    for r in rows:
        rsplt = r[:-1].split(",")
        unitsDict[rsplt[0]] = {}
        unitsDict[rsplt[0]]["unitCode"] = rsplt[1]
        unitsDict[rsplt[0]]["unitText"] = rsplt[2]
        unitsDict[rsplt[0]]["symbol"] = rsplt[3]

with open(propsFile,"r") as f:
    rows = f.readlines()[1:]
    for r in rows:
        rsplt = r[:-1].split(",")
        if rsplt[0] == "qp":
            propsDict[rsplt[1]] = "QuantitativeProperty"
        if rsplt[0] == "gp":
            propsDict[rsplt[1]] = "GeoProperty"
        if rsplt[0] == "tp":
            propsDict[rsplt[1]] = "TimeProperty"
        if rsplt[0] == "np":
            propsDict[rsplt[1]] = "Property"

dm = {}
with open(data_model, "r") as f:
    dm = json.load(f)

props = dm["properties"]

dm["@context"] = []
dm["@context"].append(core_context)
dm["@context"].append(common_context)
dm["@context"].append(miscSchemaOrgDefs)
dm["@context"].append(geometry_schema)
dm["@context"].append(dm_context_url[:-2])

dm_context = {}
dm_context["@context"] = {}
dm_context["properties"] = "@nest"
dm_context["@context"][dm_context_file_name[:-5]] = dm_context_url


locRef = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/common_defs.json#/definitions/location"

for prop in props:
    if(re.search('time', prop, re.IGNORECASE)):
        dm_context["@context"][prop] = {"@id":dm_context_file_name[:-5] + ":" + prop, "@type": "TimeProperty"}
    elif(re.search('location', prop, re.IGNORECASE)):
        dm_context["@context"][prop] = {"@id":dm_context_file_name[:-5] + ":" + prop, "@type": "GeoProperty"}
        props[prop]["$ref"] = locRef
        if("allOf" in props[prop].keys()):
            props[prop].pop("allOf")
    else:
        if(prop in propsDict.keys()):
            if propsDict[prop] == "QuantitativeProperty":
                dm_context["@context"][prop] = {"@id": dm_context_file_name[:-5] + ":" + prop, "@type": "QuantitativeProperty"}
                props[prop]["$ref"] = propTypeLink+"QuantitativeProperty"
            else:
                dm_context["@context"][prop] = {"@id": dm_context_file_name[:-5] + ":" + prop, "@type": "Property"}
        else:
            dm_context["@context"][prop] = {"@id":dm_context_file_name[:-5] + ":" + prop, "@type": "Property"}
    if("describes" in props[prop].keys()):
        dm_context[prop] = {}
        dm_context[prop]["describes"] = props[prop]["describes"]
    if(prop in unitsDict.keys()):
        props[prop]["unitText"] = unitsDict[prop]["unitText"]
        props[prop]["unitCode"] = unitsDict[prop]["unitCode"]
        if(unitsDict[prop]["symbol"] != ''):
            props[prop]["symbol"] = unitsDict[prop]["symbol"]
    if("oneOf" in props[prop].keys()):
        props[prop].pop("oneOf")
    if("valueSchema" in props[prop].keys()):
        props[prop].pop("valueSchema")


#print(json.dumps(dm, indent=4, sort_keys=True))
#print(json.dumps(dm_context, indent=4, sort_keys=True))

p = path_to_dm_folder + dm_name
with open(p, "w") as f:
    json.dump(dm, f, indent=4, sort_keys=True)

with open(path_to_dm_context, "w") as f:
    json.dump(dm_context, f, indent=4, sort_keys=True)
