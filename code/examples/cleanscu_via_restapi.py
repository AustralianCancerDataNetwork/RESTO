# -*- coding: utf-8 -*-
"""Example: delete a specific modality for a patient. 
"""
import requests
import json

response=requests.post(url='http://localhost:8042/tools/find', 
                data='{"Level" : "Series","Query" : {"Modality" : "REG","PatientID" : "1111111"}}')


series_to_delete=response.json()
logs=[]
for aseries in series_to_delete:
    deleteurl=f'http://localhost:8042/series/{aseries}'
    deleterequest = requests.delete(deleteurl)
    di={'deleteurl':deleteurl,'response':deleterequest.ok}
    logs.append(di)

#save the logs
with open('json_files/deletelogs.json', 'w') as outfile:
    json.dump(logs, outfile)