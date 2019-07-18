import json
import os
from os import listdir
from os.path import isfile, join
import re


data_model = "../../../data_models/environment/floodSensor/env_flood_climoPune_0.json"

dm_list = data_model.split("/")
dm_name = dm_list[-1]
path_to_dm = dm_list[dm_list.index("data_models"):-1]
path_to_dm_folder = "".join(a+"/" for a in dm_list[:-1])
folder_path = "".join(a+"/" for a in path_to_dm)
print(folder_path)


core_context = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/core_context.json"
common_context = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/common_context.json"
miscSchemaOrgDefs = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/miscSchemaOrgDefs.json"
geometry_schema = "https://raw.githubusercontent.com/iudx/iudx-ld/master/base_schemas/v0.0.0/geometry-schema.json"

dm_url = "https://raw.githubusercontent.com/iudx/iudx-ld/master/" + folder_path + dm_name + "#/properties/"
dm_context_url = "https://raw.githubusercontent.com/iudx/iudx-ld/master/" + folder_path + folder_path.split("/")[-1] + "_context.json" + "#/properties/"

dm = {}
with open(data_model, "r") as f:
    dm = json.load(f)

props = dm["properties"]

dm["@context"] = []
dm["@context"].append(core_context)
dm["@context"].append(common_context)
dm["@context"].append(miscSchemaOrgDefs)
dm["@context"].append(geometry_schema)
dm["@context"].append(dm_context_url)

dm_context = {}
dm_context["@context"] = {}



for prop in props:
    if(re.search('time', prop, re.IGNORECASE)):
        dm_context["@context"][prop] = {"@id":dm_context_url + prop, "@type": "TimeProperty"}
    else:
        dm_context["@context"][prop] = {"@id":dm_context_url + prop, "@type": "Property"}
    if("describes" in props[prop].keys()):
        dm_context[prop] = props[prop]["describes"]
    if("units" in props[prop].keys()):
        props[prop]["unitText"] = props[prop]["units"]
    if("oneOf" in props[prop].keys()):
        props[prop].pop("oneOf")
    if("valueSchema" in props[prop].keys()):
        props[prop].pop("valueSchema")


print(json.dumps(dm, indent=4, sort_keys=True))
