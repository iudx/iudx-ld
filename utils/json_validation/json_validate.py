import jsonschema
import json
import sys
import requests

#schemaFile = "base_schemas/iudx_resourceItem_schema.json"
#itemFile = "ex_items/testItem.json"

#schemaFile = "../base_schemas/iudx_resourceItem_schema.json"

itemFile = sys.argv[1]

#schemaFile = "../data_models/aqm.json"
#itemFile = "../data_models/aqm_item.json"


with open(itemFile, "r") as f:
    item = json.load(f)


base_schema = {}
bs_fl = item["refBaseSchema"]["value"]

if "refDataModel" in item.keys():
    dm_fl = item["refDataModel"]["value"]
else :
    dm_fl = ""


if dm_fl is not "":
    schema = {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "allOf": [
       {"$ref": bs_fl},
       {"$ref": dm_fl}
      ]
    }
else:
    schema = {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "allOf": [
       {"$ref": bs_fl}
      ]
    }

# This will find the correct validator and instantiate it using the resolver.
# Requires that your schema a line like this: "$schema": "http://json-schema.org/draft-04/schema#"
try:
 jsonschema.validate(item, schema )

except jsonschema.exceptions.ValidationError as errV:
 print ("Validation Error Occured")
 #print errV
 v = jsonschema.Draft7Validator(schema, types=(), format_checker=None)
 #for error in sorted(v.iter_errors(data), key=str):
 #    print(error.message)
 errors = sorted(v.iter_errors(item), key=lambda e: e.path)
 for error in errors:
     print (error.message)

except jsonschema.exceptions.SchemaError as errS:
 print ("Schema Error Occured")
 print (errS.message)
