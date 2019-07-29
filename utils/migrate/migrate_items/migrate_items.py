import json
import requests


exItem_fl = "../../../data_models/environment/floodSensor/examples/exItem_env_flood_climoPune_0.json"
cat_array_link = "https://catalogue.iudx.org.in/cat/search?tags=flood"

exItem = {}
with open(exItem_fl,"r") as f:
    exItem = json.load(f)


items = []
items = requests.get(cat_array_link, verify=False).json()


def makeItem(old_item):
    new_item = exItem.copy()
    new_item["@id"] = old_item["id"]
    new_item["latestResourceData"]["value"] = old_item["latestResourceData"]
    new_item["NAME"]["value"] = old_item["NAME"]
    new_item["itemStatus"]["value"] = old_item["itemStatus"]
    new_item["location"]["value"]["geometry"]["coordinates"] = [old_item["location"]["longitude"], old_item["location"]["latitude"]]
    new_item["STATION_ID"]["value"] = old_item["STATION_ID"]
    new_item["accessInformation"][0]["accessObjectVariables"]["value"]["NAME"] = old_item["accessInformation"][0]["accessVariables"]["resourceId"]
    new_item["resourceId"]["value"] = old_item["resourceId"]


