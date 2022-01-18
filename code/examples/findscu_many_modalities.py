# -*- coding: utf-8 -*-
"""Example: Find all the specific modalities  in an Orthanc server.
"""
import json
import requests
x=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "RTIMAGE"}}')

print(x.status_code)
print(len(x.json()))
#save the logs
with open('RTIMAGE.json', 'w') as outfile:
    json.dump(x.json(), outfile)
    
x=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "REG"}}')

print(x.status_code)
print(len(x.json()))
#save the logs
with open('REG.json', 'w') as outfile:
    json.dump(x.json(), outfile)
    
x=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "CT"}}')

print(x.status_code)
print(len(x.json()))
#save the logs
with open('CT.json', 'w') as outfile:
    json.dump(x.json(), outfile)
    
x=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "RTDOSE"}}')

print(x.status_code)
print(len(x.json()))
#save the logs
with open('RTDOSE.json', 'w') as outfile:
    json.dump(x.json(), outfile)
    
x=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "RTSTRUCT"}}')

print(x.status_code)
print(len(x.json()))
#save the logs
with open('RTSTRUCT.json', 'w') as outfile:
    json.dump(x.json(), outfile)
    
    