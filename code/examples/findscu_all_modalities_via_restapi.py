# -*- coding: utf-8 -*-
"""
Example: Get all the series ids for the modality RTRECORD.
"""
import json
import requests
x=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "RTRECORD"}}')

print(x.status_code)
print(len(x.json()))
#save the logs
with open('json_files/RTRECORD.json', 'w') as outfile:
    json.dump(x.json(), outfile)