"""

"""
from datetime import datetime
import concurrent.futures
import requests
import json
import pandas as pd
import time
import pickle


def check_study_in_orthanc(studyuid):
    """This function is used to check if the study is in the current PACS, it takes the hashed_study uid as index
    and returns three parameters (true/false,id|not found| connection error, datechecked)
    
    """
    q='{"Level" : "Study","Query" : {"StudyInstanceUID" : "'+studyuid+'"}}'
    x=requests.post(url='http://localhost:8042/tools/find', data=q)
    e=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if x.status_code==200:
        suid=x.json()
        if len(suid)>0:
            return True,suid[0],e
        else:
            return False,'not found',e
    if x.status_code!=200:
        return False,'connection error',e
    
def check_series_in_orthanc(seriesuid=None,studyuid=None):
    """This function is used to check if the series is in the current PACS, it takes the hashed_study uid as index
    and returns three parameters.
    
    """
    print(seriesuid)
    e=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if studyuid is not None:
        a1,a2,a3=check_study_in_orthanc(studyuid)
        if not a1:
            return False,'not found',e      
    q='{"Level" : "Series","Query" : {"SeriesInstanceUID" : "'+seriesuid+'"}}'
    x=requests.post(url='http://localhost:8042/tools/find', data=q)
    e=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if x.status_code==200:
        suid=x.json()
        if len(suid)>0:
            return True,suid[0],e,seriesuid,studyuid
        else:
            return False,'not found',e,seriesuid,studyuid
    if x.status_code!=200:
        return False,'connection error',e,seriesuid,studyuid
    
def cfind_multiple_series_uids(seriesuids,studyuids):
    """Checks if series are in the orthanc server. NOT USED CURRENTLY. use cfind_multiple_series_uids_wrapped instead as it is faster.
    
    """
    print('Starting to check')
    status=[]
    notes=[]
    thedates=[]
    suids=[]
    studyuids=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        print('a')
        #this command stards the task for each URL in urls lists
        #future_to_url = (executor.submit(check_series_in_orthanc, seriesuid,studyuid) for seriesuid,studyuid in zip(seriesuids,studyuids))
        future_to_url = (executor.submit(check_series_in_orthanc, seriesuid) for seriesuid in seriesuids)
        #after running the task, check the results in each one. 
        #as_completed does not return the values in order. 
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                print('x')
                a,b,c,d,e = future.result()#get the result of each request
            except Exception as exc:
                print(exc)
                s = str(exc)
                print(s)
            finally:
                status.append(a)
                notes.append(b) 
                thedates.append(c)
                suids.append(d)
                studyuids.append(e)

    df=pd.DataFrame({'series_uid':suids,'study_uids':studyuids,'status':status,'note':notes,'thedate':thedates})

    df.to_csv('check_required_series.csv',index=False)
    print('Done')
    input()

def check_series_in_orthanc_wrapped(wrapped):
    """This function is used to check if the series is in the current PACS, it takes the hashed_study uid as index
    and returns three parameters.
    
    """
    
    seriesuid=wrapped['series']
    studyuid=wrapped['study']
    print(seriesuid)
    e=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if studyuid is not None:
        a1,a2,a3=check_study_in_orthanc(studyuid)
        if not a1:
            return False,'not found',e,seriesuid,studyuid    
    q='{"Level" : "Series","Query" : {"SeriesInstanceUID" : "'+seriesuid+'"}}'
    x=requests.post(url='http://localhost:8042/tools/find', data=q)
    e=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if x.status_code==200:
        suid=x.json()
        if len(suid)>0:
            return True,suid[0],e,seriesuid,studyuid
        else:
            return False,'not found',e,seriesuid,studyuid
    if x.status_code!=200:
        return False,'connection error',e,seriesuid,studyuid


    
def cfind_multiple_series_uids_wrapped(seriesuids=[],studyuids=[],fn='check_required_series1.csv'):
    """Checks which series in the server, and saved output to a csv file
    
    """
    start=time.time()
    print('Starting to check series uids')
    
    wrapped_data=[]
    for i,j in zip(seriesuids,studyuids):
        wrapped_data.append({'series':i,'study':j})
    status=[]
    notes=[]
    thedates=[]
    suids=[]
    studyuids=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        print('collecting multiple series')
        #this command stards the task for each URL in urls lists
        future_to_url = (executor.submit(check_series_in_orthanc_wrapped, w) for w in wrapped_data)
        #after running the task, check the results in each one. 
        #as_completed does not return the values in order. 
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                a,b,c,d,e = future.result()#get the result of each request
            except Exception as exc:
                print(exc)
                s = str(exc)
                print(s)
            finally:
                status.append(a)
                notes.append(b) 
                thedates.append(c)
                suids.append(d)
                studyuids.append(e)

    df=pd.DataFrame({'series_uid':suids,'study_uids':studyuids,'status':status,'note':notes,'thedate':thedates})

    df.to_csv(fn,index=False)
    finish=time.time()
    print(f'Time taken: {finish-start}')
    print('Done')
    input()


def cfind_multiple_series_uids_locally(seriesuids=[],fn='check_required_series_locally.csv',series_files='D:/AH/RESTO/code/find/files/all_series_new.csv'):
    """There could be files that are generated to save all the series ids. Rather than checking the orthanc server, such files can be checked.
    
    """
    #link to all series uids in the orthanc server:
    all_series=pd.read_csv(series_files)
    all_series_uids=all_series['series_uid'].unique().tolist()#all the series in the orthanc pacs
    orthanc_uids=all_series['series_uid'].unique().tolist()#all the series in the orthanc pacs
    
    status=[]
    notes=[]
    thedates=[]
    for idx,series in enumerate(seriesuids):
        if series in all_series_uids:
            status.append(True)
            notes.append(orthanc_uids[idx]) 
            thedates.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            status.append(False)
            notes.append('not found') 
            thedates.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
    df=pd.DataFrame({'series_uid':seriesuids,'status':status,'note':notes,'thedate':thedates})

    df.to_csv(fn,index=False)



def get_object_json(wrappeddetails):
    """Get a json object associated with a file in the orthanc server
    
    """
    try:
        orthanc_uid=wrappeddetails['orthanc_uid']
        print(orthanc_uid)
        objecttype=wrappeddetails['objecttype']
        a1=requests.get(f'http://localhost:8042/{objecttype}/{orthanc_uid}/')
        b=a1.json()
        b['ID_AH']=orthanc_uid
        return b
    except Exception as e:
        print(e)
        return {'ID_AH':orthanc_uid}
        
   
    
def get_multiple_objects_json(orthanc_uids=[],fn='files/all_series.pkl',objecttype='series'):
    """A function to collect json tags associated with studies, series, or instances.
    
    """
    print('Start getting all json objects.')
    try:
        if len(orthanc_uids)==0:#if no lists, then all
            x=requests.get(f'http://localhost:8042/{objecttype}')
            orthanc_uids=x.json()
        start=time.time()
        print(f'Get uids of files: {len(orthanc_uids)}')
        #wrap the object
        wrapped_data=[]
        for orthanc_uid in orthanc_uids:
            wrapped_data.append({'orthanc_uid':orthanc_uid,'objecttype':objecttype})
        
        json_dicts=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            print('collecting all series, started')
            #this command stards the task for each URL in urls lists
            future_to_url = (executor.submit(get_object_json, w) for w in wrapped_data) 
            #as_completed does not return the values in order. 
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    series_json_object= future.result()#get the result of each request
                except Exception as exc:
                    print(exc)
                finally:
                    json_dicts.append(series_json_object)
        print(f'saving the generated list to {fn}')          
        with open(fn, 'wb') as outfi:  # Python 3: open(..., 'wb')
            pickle.dump(json_dicts, outfi)
        finish=time.time()
        print(f'Time taken: {finish-start}')
        print('Done, click enter to close the terminal.')
    except Exception as e:
        print(e)
        
    input()
    
    
def get_all(objecttype='instances',fn='all_instances.pkl'):
    """A function to get all the tags associated with particular instances in the orthanc server.
    
    """
    try: 
        orthanc_uids=[]
        get_multiple_objects_json(orthanc_uids,fn,objecttype)
        
    except Exception as e:
        print(e)
    input()
    
    
    
def find_all_ids_of_a_modality(moda='RTDOSE'):
    """A function to get all the ids of a modalities and save to a json file.
    
    """
    d='{"Level" : "Series","Query" : {"Modality" : "'+moda+'"}}'
    print(d)
    x=requests.post(url='http://localhost:8042/tools/find', 
                data=d)
    
    print(x.status_code)
    print(len(x.json()))
    #save the logs
    with open(f'{moda}.json', 'w') as outfile:
        json.dump(x.json(), outfile)


        
        
def find_all_beams_instances():
    """A function to find all the beam instances in an Orthanc Server and return their orthanc ids.
    
    """
    d='{"Level" : "Instance","Query" : {"Modality" : "RTDOSE","DoseSummationType": "BEAM"}}'
    print(d)
    x=requests.post(url='http://localhost:8042/tools/find', 
                data=d)
    
    print(x.status_code)
    print(len(x.json()))    
    return x