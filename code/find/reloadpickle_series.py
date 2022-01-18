# -*- coding: utf-8 -*-
"""
This script is used to reload the json dict representing each series 
Created on Sun Oct 10 16:58:44 2021

@author: 60183647
"""
import pickle
from datetime import datetime
import pandas as pd
if __name__=='__main__':
    fn='files/all_series_new.pkl'
    with open(fn, 'rb') as loadi:  
        studydict = pickle.load(loadi)
    
    series_uids=[]
    thedates=[]
    status=[]
    notes=[]
    series_uids=[]
    for jsonfile in studydict:
        e=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            series_uid=jsonfile['MainDicomTags']['SeriesInstanceUID']
            series_uids.append(series_uid)
            status.append(True)
            thedates.append(e)
            notes.append(jsonfile['ID_AH'])
        except Exception as e:
            print(e)
            series_uids.append('not found')
            notes.append('not found')
            status.append(False)
            thedates.append(e)
    df=pd.DataFrame(studydict)
    df['status']=status
    df['note']=notes
    df['thedate']=thedates
    df['series_uid']=series_uids
    df.to_csv('files/all_series_new.csv',index=False)
            
    