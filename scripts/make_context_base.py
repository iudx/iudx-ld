import json

fl = "base_schemas/iudx_base.json"
iudx_base_iri = "https://raw.githubusercontent.com/rraks/iudx-ld/master/base_schemas/iudx_base.jsonld"

doc = {}

with open(fl,"r") as f:
    doc = json.load(f)

props = doc["properties"]

context = {}

for prop in props:
    context[prop] = iudx_base_iri + "#/properties/" + prop

doc["@context"] = context
with open(fl[:-4]+"jsonld", "w") as f:
    json.dump(doc, f, indent=4, sort_keys=True)
