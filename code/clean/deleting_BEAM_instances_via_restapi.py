# -*- coding: utf-8 -*-
"""deleting all the beams from the orthanc server. 

"""
import pickle
try: 
    #from orthanc_find import find_all_beams_instances
    #a=find_all_beams_instances()
    with open('files/a.pkl', 'rb') as fp:#a contains the result of the function as pickle file.
        a = pickle.load(fp)# a is a list of ids
    
    from orthanc_delete import delete_multiple_objects
    
    fn='files.delete_logs_BEAMS.pkl'
    objecttype='instances'#beams are instances
    
    delete_multiple_objects(a,fn,objecttype)
except Exception as e:
    print(e)

input()
