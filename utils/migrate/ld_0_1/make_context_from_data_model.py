import json


data_model_path = "../../../data_models/traffic/tomtom/traffic_tomtom.json"
domain = data_model_path.split("/")[-3]
domain_path = "".join(path for path in data_model_path.split("/")[-3:-1])
data_model_op_path = "".join(path+"/" for path in data_model_path.split("/")[:-1]) + domain + ".json"

dm = {}

with open(data_model_path, "r") as f:
    dm = json.load(f)

dm_context = {}
dm_context["@context"] = {}
dm_context["@context"][domain] =  "https://raw.githubusercontent.com/iudx/iudx-ld/master/data_models/" + "".join(p for p in domain_path) + domain + ".json"


for attr in dm["properties"]:
    dm_context[attr] = {}
    dm_context[attr]["describes"] = dm["properties"][attr]["describes"]
    dm_context["@context"][attr] = {}
    dm_context["@context"][attr]["@type"] = dm["properties"][attr]["$ref"].split("/")[-1]
    dm_context["@context"][attr]["@id"] = domain + ":" + attr



print(data_model_op_path)
with open(data_model_op_path, "w") as f:
    json.dump(dm_context, f, indent=4)

