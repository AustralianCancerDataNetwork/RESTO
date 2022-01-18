# -*- coding: utf-8 -*-
"""Example: Find details about a series using the restapi
"""

import requests
#x=requests.post(url='http://localhost:8042/tools/find', data='{"Level" : "Study","Query" : {"PatientID" : "997690930792"}}')
#x=requests.post(url='http://localhost:8042/tools/find', data='{"Level" : "Series","Query" : {"PatientID" : "1.3.6.1.4.1.32722.168646430484694029921302374968205654515"}}')
x=requests.post(url='http://localhost:8042/tools/find', data='{"Level" : "Series","Query" : {"SeriesInstanceUID" : "1.3.6.1.4.1.32722.58473856751186681780608071808645237531"}}')
print(x.status_code)
print(x.json())
