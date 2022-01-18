# REST API ORTHANC

This repo contains examples for searching and mining an orthanc server instance. It was also used to clean the Orthanc server by removing unrequired modalities such as RTIMAGE and instances with DoseSummationType as 'BEAM'. 


This repo can be used for two different tasks:

- Finding data in the Orthanc Server
- Cleaning the Orthanc Server

The examples were executed assuming that an Orthanc instance is running at the localhost

This repo allows you to utilise functions to search for content in the Orthanc server:

- If you want to find if a series is on the server, use __check_series_in_orthanc()__ from orthanc_find module
- If you want to find if a study is on the server, use __check_study_in_orthanc()__ from orthanc_find module
- If you want to find if a series is on the server, and you have the StudyUID, use __check_series_in_orthanc_wrapped()__ from orthanc_find module
- If you want to find if a set of seriesUIDs are in the server, used __check_series_in_orthanc_wrapped()__ 
- If you want to find all the tags associated with all the instances/studies/series in the server, use the __get_all()__ function in orthanc_find module

This repo allows you to utilise functions to delete content from the Orthanc server:

- If you want to delete an object in the server, you got the orthanc-id and the type (series,instance, study), use __delete_object()__ from the orthanc_delete module.
- If you want to delete multiple objects, use __delete_multiple_objects()__ from orthanc_delete

Here are some other examples that might help:

- To find if a series is in the Orthanc server. (__code/examples/findscu_via_restapi.py__)
- To find all the ids of a specific modality and save the ids to a json file. (__code/examples/findscu_all_modalities_via_restapi.py__). This is also included in orthanc_fin module
- To delete a specific modality for a patient (__code/examples/cleanscu_via_restapi.py__)
- To delete a set of series saved in a json file from an orthanc server (__code/examples/cleanscu_set_series_via_restapi.py__)
- To find many modalities as save each (__code/examples/findscu_all_modalities_via_restapi.py__)