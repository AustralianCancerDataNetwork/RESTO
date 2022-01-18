# -*- coding: utf-8 -*-
"""
Example: delete a set of series saved in a json file from an orthanc server
"""
import requests
import json


logsfilename='json_files/deletelogs.json'
#open the log files
with open(logsfilename) as json_file:
    logs = json.load(json_file)

reg_images_filename='json_files/RTRECORD.json'

with open(reg_images_filename) as json_file:
    series_to_delete = json.load(json_file)


for aseries in series_to_delete:
    print('deleting: ' + aseries)
    deleteurl=f'http://localhost:8042/series/{aseries}'
    deleterequest = requests.delete(deleteurl)
    di={'deleteurl':deleteurl,'response':deleterequest.ok,'series_oid':aseries}
    logs.append(di)

#save the logs
with open('json_files/deletelogs.json', 'w') as outfile:
    json.dump(logs, outfile)