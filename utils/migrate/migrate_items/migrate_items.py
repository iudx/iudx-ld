import json
import requests


exItem_fl = "../../../data_models/WiFi/hotspot/examples/exItem_wifi_hotspot_Pune_0.json"
cat_array_link = "https://catalogue.iudx.org.in/cat/search/attribute?tags=(wifi)"

category = cat_array_link.split("=")[-1].replace("(","").replace(")","")
out_fl = "../../../temp/cat_new/"+category+".json"

exItem = {}
with open(exItem_fl,"r") as f:
    exItem = json.load(f)


items = []
items = requests.get(cat_array_link, verify=False).json()

new_items = []

# Flood
#def makeItem(old_item):
#    new_item = exItem.copy()
#    new_item["provider"] = "pscdcl"
#    new_item["resourceServer"] = "pscdcl"
#    new_item["id"] = old_item["id"]
#    new_item["latestResourceData"]["value"] = old_item["latestResourceData"]
#    new_item["NAME"]["value"] = old_item["NAME"]
#    new_item["location"]["value"]["geometry"]["coordinates"] = [old_item["location"]["longitude"], old_item["location"]["latitude"]]
#    new_item["accessInformation"][0]["accessObjectVariables"]["value"]["NAME"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
#    new_item["resourceId"]["value"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
#    return new_item

#air
#def makeItem(old_item):
#    new_item = exItem.copy()
#    new_item["provider"] = "pscdcl"
#    new_item["resourceServer"] = "pscdcl"
#    new_item["id"] = old_item["id"]
#    new_item["latestResourceData"]["value"] = old_item["latestResourceData"]
#    new_item["DEVICEID"]["value"] = old_item["DEVICEID"]
#    new_item["NAME"]["value"] = old_item["NAME"]
#    new_item["location"]["value"]["geometry"]["coordinates"] = [old_item["location"]["longitude"], old_item["location"]["latitude"]]
#    new_item["accessInformation"][0]["accessObjectVariables"]["value"]["NAME"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
#    new_item["resourceId"]["value"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
#    return new_item

#sl
#def makeItem(old_item):
#    new_item = exItem.copy()
#    new_item["provider"] = "pscdcl"
#    new_item["resourceServer"] = "pscdcl"
#    new_item["id"] = old_item["id"]
#    new_item["latestResourceData"]["value"] = old_item["latestResourceData"]
#    new_item["PANEL_NAME"]["value"] = old_item["PANEL_NAME"]
#    new_item["PANEL_ID"]["value"] = old_item["PANEL_ID"]
#    new_item["NAME"]["value"] = old_item["NAME"]
#    new_item["location"]["value"]["geometry"]["coordinates"] = [old_item["location"]["longitude"], old_item["location"]["latitude"]]
#    new_item["accessInformation"][0]["accessObjectVariables"]["value"]["NAME"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
#    new_item["resourceId"]["value"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
#    return new_item

#WiFi
def makeItem(old_item):
    new_item = exItem.copy()
    new_item["provider"] = "pscdcl"
    new_item["resourceServer"] = "pscdcl"
    new_item["id"] = old_item["id"]
    new_item["latestResourceData"]["value"] = old_item["latestResourceData"]
    new_item["HOTSPOT_ID"]["value"] = old_item["HOTSPOT_ID"]
    new_item["NAME"]["value"] = old_item["NAME"]
    new_item["location"]["value"]["geometry"]["coordinates"] = [old_item["location"]["longitude"], old_item["location"]["latitude"]]
    new_item["accessInformation"][0]["accessObjectVariables"]["value"]["NAME"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
    new_item["resourceId"]["value"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
    return new_item

for itm in items:
    try:
        new_items.append(makeItem(itm))
    except Exception as e:
        print(e)
        input()
        print(json.dumps(itm))

with open(out_fl, "w") as f:
    json.dump(new_items, f, indent=4, sort_keys=True)


