# -*- coding: utf-8 -*-
"""
Spyder Editor

 this script is used for_double_delayed_c_reward in 2020.07 !!!!!
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
class Mouse_data:
    def __init__(self,mouse_id,filedir):
        self.mouse_id = mouse_id
        self.filedir = filedir
        self.filename = ''
        self.selected_filename = ''
        self.all_days = []
        
        self.training_type = []
        self.df_trials = {}
        self.trialtypes = []
        self.df_trials_iscorrect = {}
        self.df_trials_lick = {}
        self.df_eventcode = {}
        self.p_hit = {}
        self.p_correj = {}
        self.licking_actionwindow = {}
        self.licking_latency = {}
        self.licking_baselicking = {}
        self.stats = {}
        self.event_data = ''
        self.odor_bef = 3.0
        self.odor_on = 1.0
        self.delay = 2.5
        self.rew_after = 2
        

    def read_filename(self):
        filedir = self.filedir +'/{}'.format(self.mouse_id)
        filename = []
        for dirpath, dirnames, files in os.walk(filedir): # can walk through all levels down
        #     print(f'Found directory: {dirpath}')
            for f_name in files:
                if f_name.endswith('.xlsx'):
                    filename.append(dirpath+'/'+f_name)
                    print(f_name)
        print('---------------------------------------------')    
        print('The files have been loaded from the following paths')
        print(filename[-45:])
        self.filename = filename
        
    
    def select_dates(self):
        pass
    def delete_date(self, dates):
        for date in dates:
            self.all_days.remove(date)
        
        return self.all_days
        
    def create_eventcode(self, original = True): #{'date':df of eventcode} format from original CSV
        date_list = []
        df = {}
        training_type = []
        
        for file in self.filename:
            date = re.search(r"(\d{4}-\d{1,2}-\d{1,2}-\d{1,2}-\d{1,2})",file).group(0) # extract date: must be like format 2020-02-10
            date_list.append(date) # create a list of emperiment date
            
            train_type = os.path.split(file)[-1][16:-5]
            training_type.append(train_type) ###
                
            
            data = pd.read_excel(file,header = 0 if original else None) #read orginal csv data
            data.columns = ['Time','Event','Type'] # rename columns
            
            df.update({date:data}) # create the dict of key: date and value: data dataframe
        self.df_eventcode = df #individual mouse event code data
        date_format = '%Y-%m-%d-%h-%s'
        index = np.argsort(date_list)
        self.all_days = [date_list[i] for i in index]
        self.training_type = [training_type[i] for i in index]
        
        print('---------------------------------------------')
        print('{0} has data from these days: {1}'.format(self.mouse_id,zip(self.all_days,self.training_type)))

    def create_trials(self): #{'date: df of trials}
        for index , date in enumerate(self.all_days):
            value = self.df_eventcode[date]
        
            new_df = self.generate_trials_dataframe(index,value)
            self.df_trials[date] = new_df
            print('{} done!'.format(date))
     
    
    def generate_trials_dataframe(self,index,ori_df):
        
        lick, trialtype, go_odor, nogo_odor, control_odor, water_on, water_off, trial_end = self.seperate_events(index,ori_df)
        d = {'trialtype' : trialtype, 'go_odor': go_odor, 'nogo_odor': nogo_odor, 'control_odor':control_odor,
             'water_on':water_on,'water_off':water_off,'licking':lick,
             'trial_end':trial_end}
        df_trial = pd.DataFrame(data = d)
        return df_trial
    
    
    def seperate_events(self,index_day,df):
        
        start_trials = 0
        lick          = []
        trialtype     = []
        go_odor       = []
        nogo_odor     = []
        control_odor  = []
        water_on      = []
        water_off     = []
        trial_end     = []
        print(index_day)
        
        for index, row in df.iterrows():
            if row['Event'] == 101:   # trial start
                start_trials = row['Time']                
                temp_licks        = []
                temp_go_odor_on      = np.nan
                temp_go_odor_off      = np.nan
                temp_nogo_odor_on    = np.nan
                temp_nogo_odor_off    = np.nan
                temp_control_odor_on = np.nan
                temp_control_odor_off = np.nan
                
                temp_water_on     = np.nan
                temp_water_off    = np.nan
                temp_trial_end    = np.nan
                
                if row['Type'] == 'trial0':
                    trialtype.append('go')
                elif row['Type'] == 'trial1':
                    trialtype.append('no_go')
                elif row['Type'] == 'trial2':
                    trialtype.append('background')
                elif row['Type'] == 'trial3':
                    trialtype.append('go_omit')
                elif row['Type'] == 'trial4':
                    trialtype.append('unpred_water')
                elif row['Type'] == 'trial5':
                    trialtype.append('c_reward')
                elif row['Type'] == 'trial6':
                    trialtype.append('c_omit')
                elif row['Type'] == 'trial7':
                    trialtype.append('close_unpred_water')
                elif row['Type'] == 'trial8':
                    trialtype.append('far_unpred_water')

            elif row['Event'] == 11:
                lick_time = row['Time'] - start_trials
                temp_licks.append(lick_time)

            elif row['Event'] == 131: # go odor on
                temp_go_odor_on=row['Time']- start_trials
        
            elif row['Event'] == 130:
                temp_go_odor_off=row['Time']- start_trials

            elif row['Event'] == 141: # no go odor on
                temp_nogo_odor_on=row['Time']- start_trials
        
            elif row['Event'] == 140:
                temp_nogo_odor_off=row['Time']- start_trials
            elif row['Event'] == 161: # no go odor on
                temp_control_odor_on=row['Time']- start_trials
        
            elif row['Event'] == 160:
                temp_control_odor_off=row['Time']- start_trials
 
            elif row['Event'] == 51: # water on
                temp_water_on=row['Time']- start_trials
        
            elif row['Event'] == 50:
                temp_water_off=row['Time']- start_trials

            elif row['Event'] == 100: #trial end
                temp_trial_end=row['Time']- start_trials
    
                lick.append(temp_licks)
                go_odor.append([temp_go_odor_on,temp_go_odor_off])
                
                nogo_odor.append([temp_nogo_odor_on,temp_nogo_odor_off])
                control_odor.append([temp_control_odor_on,temp_control_odor_off])
                water_on.append(temp_water_on)
                water_off.append(temp_water_off)
                trial_end.append(temp_trial_end)
        
    
        return  lick, trialtype, go_odor, nogo_odor, control_odor, water_on, water_off, trial_end
    
    def create_trial_iscorrect(self): # create dataframe with trial number, correct or rewarded or not only for conditioning period
        for index , date in enumerate(self.all_days):    
            value = self.df_trials[date]
            new_df = self.eval_trials_correct(value)
            new_df.insert(0,'trialtype',value['trialtype'])
            self.df_trials_iscorrect[date] = new_df
            print('create_trial_iscorrect done!')
            
    def eval_trials_correct(self, df):
        
        is_correct = []
        is_rewarded = []
        for index, row in df.iterrows():
            if row['trialtype'] == 'go':
                is_rewarded.append(1)
                if any(x > row['go_odor'][0] and x < row['go_odor'][1]+self.delay for x in row['licking']):
                    is_correct.append(1)
                else:
                    is_correct.append(0)
                
            elif row['trialtype'] == 'no_go':
                is_rewarded.append(0)
                if any(x > row['nogo_odor'][0] and x < row['nogo_odor'][1]+self.delay for x in row['licking']):
                    is_correct.append(0)
                else:
                    is_correct.append(1)
            
            elif row['trialtype'] == 'c_reward':
                is_rewarded.append(1)
                if any(x > row['control_odor'][0] and x < row['water_on'] for x in row['licking']):
                    is_correct.append(1)
                else:
                    is_correct.append(0)
            elif row['trialtype'] == 'c_omit':
                is_rewarded.append(0)
                if any(x > row['control_odor'][0] and x < row['control_odor'][1]+2*self.delay for x in row['licking']):
                    is_correct.append(1)
                else:
                    is_correct.append(0)
            
            elif row['trialtype'] == 'background':
                is_rewarded.append(0)
                if any(x > 0 and x < row['trial_end'] for x in row['licking']):
                    is_correct.append(0)
                else:
                    is_correct.append(1)
                
            elif row['trialtype'] == 'go_omit':
                is_rewarded.append(0)
                if any(x > row['go_odor'][0] and x < row['go_odor'][1]+self.delay for x in row['licking']):
                    is_correct.append(1)
                else:
                    is_correct.append(0)
            elif row['trialtype'] in ['unpred_water','close_unpred_water','far_unpred_water']:
                is_rewarded.append(1)
                is_correct.append(np.nan)
        d = {'is_Correct':is_correct,'is_Rewarded':is_rewarded}
        new_df = pd.DataFrame(d)
        return new_df
    
    def create_trial_lick(self):
        for index , date in enumerate(self.all_days):
            value = self.df_trials[date]            
            new_df = self.lick_stats(value)               
            new_df.insert(0,'trialtype',value['trialtype'])
            self.df_trials_lick[date] = new_df
            print('lick stats done!')        
            
    def lick_stats(self, df):
        
        lick_num = []
        lick_rate = []
        lick_latent_odor = []
        lick_latent_rew = []
        lick_duration = []
        lick_rate_anti = []
        lick_rate_aftr = []
        tol_interval = self.odor_on + self.delay + self.rew_after
        anti_window = self.odor_on + self.delay
        lick_anti_list = []
        lick_aftr_list = []
        for index, row in df.iterrows():
            if row['trialtype'] in ['go','go_omit'] :
                
                lick_valid = [x for x in row['licking'] if x > row['go_odor'][0] and x < row['go_odor'][0]+tol_interval ] # valid licking: after odor on and 5.5 s after odor off
                #lickingrate for anticipitory period and after water period 3.5 respectively
                anti = [i for i in row['licking']  if i> row['go_odor'][0] and i< row['go_odor'][1]+self.delay] #anticipitory
                aftr = [i for i in row['licking']  if i> row['water_on'] and i< row['water_off']+self.rew_after] #after water
                rate_anti = len(anti)/anti_window                
                rate_aftr = len(aftr)/self.rew_after             
                #num of licking
                num = len(lick_valid)
                if num != 0:
                    latency_odor = min(lick_valid)-row['go_odor'][0]# first licking after odor delivery on
                else:
                    latency_odor = tol_interval
                if row['trialtype'] == 'go':
                    if len(aftr) != 0:
                        latency_rew = min(aftr)-row['water_on']# first licking after odor delivery on
                    else:
                        latency_rew = self.rew_after
                else:
                    latency_rew = np.nan
                try:    
                    duration = max(anti)-min(anti) # anticipitory licking duration after odor presentation
                except:
                    duration = np.nan
                
            elif row['trialtype'] == 'no_go':
                lick_valid = [x for x in row['licking'] if x > row['nogo_odor'][0] and x < row['nogo_odor'][0]+tol_interval ] # valid licking: after odor on and 5.5 s after odor off
                #inter-licking interval for anticipitory period and after water period
                anti = [i for i in row['licking']  if i> row['nogo_odor'][0] and i< row['nogo_odor'][1]+self.delay] #anticipitory
                aftr = []               
                rate_anti = len(anti)/anti_window           
                rate_aftr = np.nan                
                #num of licking
                num = len(lick_valid)
                if num != 0:
                    latency_odor = min(lick_valid)-row['nogo_odor'][0]# first licking after odor delivery on
                else:
                    latency_odor = tol_interval
                latency_rew = np.nan
                try:    
                    duration = max(anti)-min(anti) # anticipitory licking duration after odor presentation
                except:
                    duration = np.nan
            elif row['trialtype'] in ['c_reward','c_omit'] :
                
                lick_valid = [x for x in row['licking'] if x > row['control_odor'][0] and x < row['control_odor'][0]+tol_interval+self.delay ] # valid licking: after odor on and 5.5 s after odor off
                #lickingrate for anticipitory period and after water period 3.5 respectively
                anti = [i for i in row['licking']  if i> row['control_odor'][0] and i< row['water_on']] #anticipitory
                aftr = [i for i in row['licking']  if i> row['water_on'] and i< row['water_off']+self.rew_after] #after water
                rate_anti = len(anti)/(row['water_on']- row['control_odor'][0])           
                rate_aftr = len(aftr)/self.rew_after             
                #num of licking
                num = len(lick_valid)
                if num != 0:
                    latency_odor = min(lick_valid)-row['control_odor'][0]# first licking after odor delivery on
                else:
                    latency_odor = row['water_on']- row['control_odor'][0]
                if row['trialtype'] == 'c_reward':
                    if len(aftr) != 0:
                        latency_rew = min(aftr)-row['water_on']# first licking after odor delivery on
                    else:
                        latency_rew = self.rew_after
                else:
                    latency_rew = np.nan
                try:    
                    duration = max(anti)-min(anti) # anticipitory licking duration after odor presentation
                except:
                    duration = np.nan
                
            elif row['trialtype'] == 'background':
                lick_valid = [x for x in row['licking'] if x > 0 and x < row['trial_end']] # valid licking: after odor on and 5.5 s after odor off
                intvl = row['trial_end']
                anti = lick_valid
                aftr = []
                rate_anti = len(anti)/intvl    
                rate_aftr = np.nan                
                num = len(lick_valid)
                latency_odor = np.nan
                latency_rew = np.nan
                duration = np.nan # licking duration after water delivery
                
            elif row['trialtype'] in ['unpred_water','close_unpred_water','far_unpred_water']:
                lick_valid = [x for x in row['licking'] if x > 0 and x < row['trial_end'] ] # valid licking: after odor on and 5.5 s after odor off                
                #inter-licking interval for anticipitory period and after water period
                anti = [i for i in row['licking']  if i> 0 and i< row['water_on']] #anticipitory
                
                aftr = [i for i in row['licking']  if i> row['water_on'] and i < min((row['water_off']+self.rew_after),row['trial_end'])]               
                rate_anti = len(anti)/(row['water_on'])         
                rate_aftr = len(aftr)/min(self.rew_after,row['trial_end']-row['water_off'])   
                #num of licking
                num = len(lick_valid)
                if len(aftr) != 0:
                    latency_rew = min(aftr)-row['water_on']# first licking after unpredicted water
                else:
                    latency_rew = min(self.rew_after,row['trial_end']-row['water_off'])
                latency_odor = np.nan
                try:    
                    duration = max(aftr)-min(aftr) # anticipitory licking duration after odor presentation
                except:
                    duration = np.nan
            
              
            lick_num.append(num)
            lick_rate.append(num/tol_interval)
            lick_latent_odor.append(latency_odor)
            lick_latent_rew.append(latency_rew)
            lick_duration.append(duration)
            lick_rate_anti.append(rate_anti)
            lick_rate_aftr.append(rate_aftr)
            lick_anti_list.append(anti)
            lick_aftr_list.append(aftr)
                
        d = {'lick_num_whole_trial':lick_num,
             'lick_rate_whole_trial':lick_rate,
             'latency_to_odor':lick_latent_odor,
             'latency_to_rew':lick_latent_rew,
             'anti_duration':lick_duration,
             'rate_antici':lick_rate_anti,
             'rate_after':lick_rate_aftr,
             'anti_lick':lick_anti_list,
             'aftr_lick':lick_aftr_list
             }
        new_df = pd.DataFrame(d)
        return new_df
    

        
    
def save_to_excel(dict_df,path,filename):
    try:
        os.makedirs(path) # create the path first
    except FileExistsError:
        print('the path exist.')
    filename = path +'/{}.xlsx'.format(filename)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    
    # Write each dataframe to a different worksheet. you could write different string like above if you want
    for key, value in dict_df.items():
        value.to_excel(writer, sheet_name= key)
        
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print('save to excel done!')
    
def pickle_dict(df,path,filename):
    try:
        os.makedirs(path) # create the path first
    except FileExistsError:
        print('the path exist.')
    filename = path +'/{}.pickle'.format(filename)
    with open(filename, 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('save to pickle done!')


def load_pickleddata(filename):
    
    with open(filename, 'rb') as handle:
        df = pickle.load(handle)
    return df
        
      

#def sort_list(list1, list2): 
#  
#    zipped_pairs = zip(list2, list1) 
#    zipped = list(zipped_pairs) 
#  
#    # Printing zipped list 
#    print("Initial zipped list - ", str(zipped)) 
#      
#    date_format = '%Y-%m-%d'
#    z = sorted(zipped,key=lambda date: datetime.strptime(date[1], date_format)) #
#    
#    # printing result 
#    print("final list - ", str(res)) 
#      
#    return z                       

    
        

#%%
#%% main code
if __name__ == '__main__':
    
    is_save = True
    is_original = True # when use clean data, change it to False
    
    #********************
    load_path = 'D:/PhD/Behavior/behavior_21_02/close_far_2021_01_Pav/'
    
    # load file
    mouse_names = ['C38','C39','C40']
    # mouse_names = ['D2-04']
    for mouse_name in mouse_names:
        cute = Mouse_data(mouse_name, filedir = load_path)
        cute.read_filename()
        #parse data
        cute.create_eventcode(original = is_original)
        cute.create_trials()
        cute.create_trial_iscorrect()    
        cute.create_trial_lick()
    
        
        if is_save:
            #save data by pickle
            #****************
            save_path = load_path+'/parsed_dataframe_pickle'
            
            filename = '{}_stats'.format(cute.mouse_id)
            pickle_dict(cute,save_path,filename)
            
            #save data to excel for just visualization (it'l all turn into string, so cannot be used later.)
            #****************
            save_path_excel = load_path+'/parsed_dataframe_spreadsheet'
            
            save_to_excel(cute.df_trials_iscorrect,save_path_excel,'{}_trial_iscorrect'.format(cute.mouse_id))
            save_to_excel(cute.df_trials_lick,save_path_excel,'{}_lick_stat'.format(cute.mouse_id))
            save_to_excel(cute.df_trials,save_path_excel,'{}_trials'.format(cute.mouse_id))
            save_to_excel(cute.df_eventcode,save_path_excel,'{}_eventcode'.format(cute.mouse_id)) 
#%% main code
if __name__ == '__main__':
    
    is_save = True
    is_original = False # when use clean data, change it to False
    
    #********************
    load_path = 'D:/PhD/Behavior/behavior_21_01/experiment_data_2021_01_Pav/clean_data/'
    
    # load file
    # mouse_names = ['D1-05-TDT','D2-02','D2-04','D2-05-TDT']
    mouse_names = ['DAT-01']
    for mouse_name in mouse_names:
        cute = Mouse_data(mouse_name, filedir = load_path)
        cute.read_filename()
        #parse data
        cute.create_eventcode(original = is_original)
        cute.create_trials()
        cute.create_trial_iscorrect()    
        cute.create_trial_lick()
    
        
        if is_save:
            #save data by pickle
            #****************
            save_path = load_path+'/parsed_dataframe_pickle'
            
            filename = '{}_stats'.format(cute.mouse_id)
            pickle_dict(cute,save_path,filename)
            
            #save data to excel for just visualization (it'l all turn into string, so cannot be used later.)
            #****************
            save_path_excel = load_path+'/parsed_dataframe_spreadsheet'
            
            save_to_excel(cute.df_trials_iscorrect,save_path_excel,'{}_trial_iscorrect'.format(cute.mouse_id))
            save_to_excel(cute.df_trials_lick,save_path_excel,'{}_lick_stat'.format(cute.mouse_id))
            save_to_excel(cute.df_trials,save_path_excel,'{}_trials'.format(cute.mouse_id))
            save_to_excel(cute.df_eventcode,save_path_excel,'{}_eventcode'.format(cute.mouse_id)) 
    
    
       
    
    
    
    
    
    
    
    
    
        
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
