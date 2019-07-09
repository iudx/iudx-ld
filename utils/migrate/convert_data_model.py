import json
import os
from os import listdir
from os.path import isfile, join
import re


data_model = "../../temp/data_models/crowdSourced/crowdSourced_type2.json"
dm_list = data_model.split("/")
dm_name = dm_list[-1]
path_to_dm = dm_list[dm_list.index("data_models"):-1]
path_to_dm_folder = "".join(a+"/" for a in dm_list[:-1])
folder_path = "".join(a+"/" for a in path_to_dm)
print(folder_path)


core_context = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_context.json"
dm_url = "https://raw.githubusercontent.com/iudx/iudx-ld/master/" + folder_path + dm_name + "#/properties/"

dm = {}
with open(data_model, "r") as f:
    dm = json.load(f)

props = dm["properties"]

context = {}
context["xsd"] = "http://www.w3.org/2001/XMLSchema#"
context["uo"] = "http://units.open.org/"



def makeOneOf(prop):
    tmpl = {}
    tmpl["oneOf"] = []
    tmpl["oneOf"].append({})
    tmpl["oneOf"][0]["type"] =  "object"
    tmpl["oneOf"][0]["properties"] = { "value": { "$ref": "#/properties/"+"xxx" } }
    tmpl["oneOf"].append({})
    tmpl["oneOf"][1]["type"] = "yyy" 
    tmpl["oneOf"][1]["$ref"] = "zzz" 
    tmpl["oneOf"][0]["properties"]["value"]["$ref"] = "#/properties/"+prop+"/valueSchema"
    tmpl["oneOf"][1]["type"] = props[prop]["type"]
    tmpl["oneOf"][1]["$ref"] = "#/properties/"+prop+"/valueSchema"
    return tmpl

def mkTimeProp(prop):
    return {"allOf": [{ "$ref":  "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_defs.json#/definitions/TimeProperty"}]}




if "locationCoverage" in props.keys():
    props.pop("locationCoverage")
    props["locationCoverage"] = {"allOf": [{ "$ref": "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_defs.json#/definitions/GeoProperty" }]}
    context["locationCoverage"] = {"@id":dm_url + "location", "@type": "GeoProperty"}

if "location" in props.keys():
    props.pop("location")
    props["location"] = {"allOf": [{ "$ref": "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_defs.json#/definitions/GeoProperty" }]}
    context["location"] = {"@id":dm_url + "location", "@type": "GeoProperty"}



if("deviceModelInfo" in props.keys()):
    props["deviceModelInfo"] = {"allOf": [{ "$ref":  "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/miscSchemaOrgDefs.json#/definitions/product"}]}

for prop in props:
    if(re.search('time', prop, re.IGNORECASE)):
        props[prop] = mkTimeProp(prop)
        context[prop] = {"@id":dm_url + prop, "@type": "TimeProperty"}
    if("type" in props[prop]):
        context[prop] = {"@id":dm_url + prop, "@type": "Property"}
        valueSchema = {}
        valueSchema["type"] = props[prop]["type"]
        if("minimum" in prop):
            valueSchema["minimum"] = props[prop]["minimum"]
            props[prop].pop("minimum")
        if("maximum" in props[prop]):
            valueSchema["maximum"] = props[prop]["maximum"]
            props[prop].pop("maximum")
        if("enum" in props[prop]):
            valueSchema["enum"] = props[prop]["enum"]
            props[prop].pop("enum")
        props[prop]["valueSchema"] = valueSchema
        oneOf = makeOneOf(prop)
        props[prop]["allOf"] = []
        props[prop]["allOf"].append({"$ref": "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_defs.json#/definitions/Property"})
        props[prop].pop("type")
        props[prop].update(oneOf)



dm["@context"] = []
dm["@context"].append(core_context)
dm["@context"].append({})
dm["@context"][1] = context
if("required" in dm.keys()):
    dm.pop("required")

print(path_to_dm_folder + dm_name)
with open(path_to_dm_folder + dm_name, "w") as f:
    json.dump(dm, f, indent=4, sort_keys=True)


