# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:14:30 2021

@author: 60183647
"""
import concurrent.futures
import requests
import time
import pickle


def delete_object(wrappeddetails):
    """Delete a json object from the orthanc server.
    
    """
    try:
        orthanc_uid=wrappeddetails['orthanc_uid']
        print(orthanc_uid)
        objecttype=wrappeddetails['objecttype']
        deleterequest=requests.delete(f'http://localhost:8042/{objecttype}/{orthanc_uid}/')
        return deleterequest.ok
    except Exception as e:
        print(e)
        return -1

def delete_multiple_objects(orthanc_uids=[1234],fn='delete__logs.pkl',objecttype='series'):
    """A function to delete objects from an orthanc server using threading
    
    """
    try:
        start=time.time()
        #wrap the object
        wrapped_data=[]
        for orthanc_uid in orthanc_uids:
            wrapped_data.append({'orthanc_uid':orthanc_uid,'objecttype':objecttype})
        
        json_dicts=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
            #this command stards the task for each URL in urls lists
            future_to_url = (executor.submit(delete_object, w) for w in wrapped_data) 
            #as_completed does not return the values in order. 
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    r= future.result()#get the result of each request
                except Exception as exc:
                    print(exc)
                finally:
                    json_dicts.append(r)
        print(f'saving the logs list to {fn}')          
        with open(fn, 'wb') as outfi:  # Python 3: open(..., 'wb')
            pickle.dump(json_dicts, outfi)
        finish=time.time()
        print(f'Time taken: {finish-start}')
        print('Done, click enter to close the terminal.')
    except Exception as e:
        print(e)
        
    input()