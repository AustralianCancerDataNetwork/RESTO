# -*- coding: utf-8 -*-
"""
This script gets all the instances/studies/ or series details in the orthanc server and save the dicts to a pickle file.

"""
if __name__=='__main__':
    try: 
        from orthanc_find import get_multiple_objects_json
        orthanc_uids=[]
        objecttype='series'
        fn='files/all_series_new.pkl'
        get_multiple_objects_json(orthanc_uids,fn,objecttype)
        
    except Exception as e:
        print(e)
    input()