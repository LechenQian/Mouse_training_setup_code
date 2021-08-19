# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 11:53:56 2020

@author: qianl
"""
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import os
import random
import matplotlib as mpl
import re
import csv
import pickle



#%%
### generate clean data

# read original eventcode
def read_filename(filedir,mouse_id):
        filedir = filedir +'/{}'.format(mouse_id)
        filenames = []
        for dirpath, dirnames, files in os.walk(filedir): # can walk through all levels down
            for f_name in files:
                if f_name.endswith('.xlsx'):
                    filenames.append(dirpath+'/'+f_name)
                    print(f_name)
        print('---------------------------------------------')    
        print('The files have been loaded from the following paths')
        
        return filenames   

def read_eventcode(file):
    
    date = re.search(r"(\d{4}-\d{1,2}-\d{1,2}-\d{1,2}-\d{1,2})",file).group(0) # extract date: must be like format 2020-02-10            
    train_type = os.path.split(file)[-1][16:-5]
    
    
    data = pd.read_excel(file) #read orginal csv data  
    data.columns = ['Time','Event','Type']
    return data,date,train_type

# find the n th '100'
def find_index(data):
    print(np.sum(data['Event']==100))
    data_series = data['Event']
    
    start_list = []
    start_index = input('where do you want to start?  ')
    
    userList = start_index.split()
    start_list = [ int(i) for i in userList]
    
    stop_list = []
    stop_index = input('where do you want to end?  ')
    userList = stop_index.split()
    stop_list = [ int(i) for i in userList]
    
    
    if len(start_list) != len(stop_list):
        raise('Error: length of two lists should match.')
    
    kept_data = []
    for i in range(len(start_list)):
        
        index1 = [x for x, n in data_series.iteritems() if n == 101][start_list[i]]
        
        index2 = [x for x, n in data_series.iteritems() if n == 100][stop_list[i]-1]
        # take out the chunk of data
        chunk = data[index1:(index2+1)]
        kept_data.append(chunk)
    
    clean_data = kept_data.pop(0)
    if len(start_list) >1:
        for data in kept_data:
            clean_data = pd.concat([clean_data, data],sort=False, ignore_index=True)

    return clean_data

# save the cleaned event code to clean_data in the format of excel

def save_to_excel(df,path,filename):
    try:
        os.makedirs(path) # create the path first
    except FileExistsError:
        print('the path exist.')
    filename = path +'/{}.xlsx'.format(filename)
    df.to_excel(filename, sheet_name='Sheet1',header = False, index = False, engine = 'xlsxwriter')
    print('saved!')
#%%
filedir = 'D:/PhD/Behavior/behavior_21_01/experiment_data_2021_01_Pav'

# mouse_id = ['D1-05-TDT','D2-02','D2-04','D2-05-TDT']
mouse_id = ['DAT-01']
for little_mouse in mouse_id:
    all_filename = read_filename(filedir,little_mouse)
    is_add_clean_only = input('all good?')
    if is_add_clean_only == 'y':
        for i in range(len(all_filename)):
            
            chosen_file = all_filename[i]
            data,date,train_type = read_eventcode(chosen_file)
            
            save_path = os.path.join(filedir,'clean_data/{}'.format(little_mouse))
            postfix = train_type
            save_to_excel(data,save_path,'clean_{0}_{1}'.format(date,postfix))

    
    
    else:
        for i in range(len(all_filename)):
            
            chosen_file = all_filename[i]
            data,date,train_type = read_eventcode(chosen_file)
            print('--------------------------')
            print('Separate multiple number by space')
            print('Date: ',date)
            is_save = input('Keep this data? y or n')
            if is_save == 'y':
            
                clean_data = find_index(data)
                save_path = os.path.join(filedir,'clean_data/{}'.format(little_mouse))
                postfix = train_type
                save_to_excel(clean_data,save_path,'clean_{0}_{1}'.format(date,postfix))
    
    
    
    
    






















