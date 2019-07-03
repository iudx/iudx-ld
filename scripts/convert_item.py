import json


dataModelPath = "https://raw.githubusercontent.com/rraks/iudx-ld/master/temp/data_models/environment/floodSensor/env_flood_climoPune_0_ld.json"
itemPath = "../temp/data_models/environment/floodSensor/examples/exItem_env_flood_climoPune_0.json"
itemNameList = itemPath.split("/")
itemName = itemNameList[-1]
path_to_item = "".join(a+"/" for a in itemNameList[:itemNameList.index("examples")+1])


resourceItemSchemaPath = "../base_schemas/resourceItem_schema.json"

item = {}
with open(itemPath,"r") as f:
    item = json.load(f)

schema = {}
with open(resourceItemSchemaPath,"r") as f:
    schema = json.load(f)["properties"]

def mkProperty(prop):
    temp = {}
    temp["type"] = "Property" 
    temp["value"] = prop
    return temp

def mkRelationship(rel):
    temp = {}
    temp["type"] = "Relationship" 
    temp["object"] = rel
    return temp

def mkTimeProperty(prop):
    temp = {}
    temp["type"] = "TimeProperty" 
    temp["value"] = prop
    return temp

def mkLocation(prop):
    temp = {}
    temp["type"] = "GeoProperty"
    temp["value"] = {}
    temp["value"]["type"] = "Point"
    temp["value"]["value"] = [prop["latitude"], prop["longitude"]]
    return temp


item.pop("refBaseSchemaRelease")

item["@id"] = item["id"]
item.pop("id")

item["refBaseSchema"] = mkRelationship(item["refBaseSchema"])

item["provider"] = mkRelationship("iudx_iri:pscdcl")
item["refDataModel"] = mkRelationship(item["refDataModel"])
item["itemDescription"] = mkProperty(item["itemDescription"])

t = item["tags"]
item["tags"] = mkProperty(t)

item["location"] = mkLocation(item["location"])

item["itemType"] = mkProperty("resourceItem" )
item.pop("__itemType")

item["itemStatus"] = mkProperty(item["__itemStatus"])
item.pop("__itemStatus")

item["createdAt"] = mkTimeProperty(item["__createdAt"])
item.pop("__createdAt")

item["accessObjectURL"] = mkRelationship(item["accessInformation"][0]["accessSchema"])
item["resourceServer"] = mkRelationship("iudx_iri:pscdcl_server")

item["resourceId"] = {}
item["resourceId"] = mkProperty(item["accessInformation"][0]["accessVariables"]["resourceId"])

item["accessObjectVariables"] = {}
item["accessObjectVariables"]["type"] = "Property"
item["accessObjectVariables"]["value"] = {}
item["accessObjectVariables"]["value"]["ip"] = item["accessInformation"][0]["accessVariables"]["resourceServerId"][:-4]
item["accessObjectVariables"]["value"]["port"] = item["accessInformation"][0]["accessVariables"]["resourceServerId"][-3:]
item["accessObjectVariables"]["value"]["resourceClass"] = item["accessInformation"][0]["accessVariables"]["resourceClass"]
item["accessObjectVariables"]["value"]["NAME"] = item["NAME"]
item.pop("accessInformation")

if("deviceModelInfo" in item.keys()):
    brand = item["deviceModelInfo"]["brand"]["name"]
    name = item["deviceModelInfo"]["brand"]["name"]
    url = item["deviceModelInfo"]["brand"]["url"]
    item["deviceModelInfo"] = {}
    item["deviceModelInfo"] = mkProperty({"brand":brand, "name":name,"url":url})


item["@context"] = []
item["@context"].append(dataModelPath)


dm_fields = list( set(item.keys()) - set(schema.keys()) - set(["@id"]) ) 
print(dm_fields)

for dmField in dm_fields:
    item[dmField] = mkProperty(item[dmField])

print(path_to_item + itemName[:-5] + "_ld.json")
with open(path_to_item + itemName[:-5] + "_ld.json", "w") as f:
    json.dump(item, f, indent=4, sort_keys=True)



