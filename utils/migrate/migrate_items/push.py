import json
import requests
import subprocess

url = "https://catalogue.iudx.org.in/catalogue/v1/items?item-type=resourceItem"
authString = ""
headers = {"Authorization":"Basic " + authString, 'skip_validation':"true"}
fl_name = "./exItem_crowdSourced_type2_0.json"
items = []

curl_cmd = "curl -ik -XPOST \"https://catalogue.iudx.org.in/catalogue/v1/items?item-type=resourceItem\" --cert certificate.pem --key private.pem  -H \'authorization :Basic YXJ1bjphcnVucmJjY3Bz\' -H \'skip_validation :true' -d \'"


with open(fl_name,"r") as f:
    items = json.load(f)

for item in items:
    new_cmd = curl_cmd+json.dumps(item)+"\'"
    print(new_cmd)

    p = subprocess.Popen(new_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print (line,)
    retval = p.wait()


