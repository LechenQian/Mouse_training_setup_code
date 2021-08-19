#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:39:00 2020

@author: lechenqian
"""

from datetime import datetime
from datetime import date
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
import sys
# sys.path.insert(0,os.path.join(path,'functions'))
from parse_data_v2 import Mouse_data
from parse_data_v2 import pickle_dict
from parse_data_v2 import load_pickleddata
#%%
def event_plot(df,save_dir,mouse_id = '', exp_date = '', filename = 'test',save = False, width = 3.5, figuresize = [12,20],gocolor = '#EBA0B1',nogocolor = '#F9CD69', rewardcolor = '#3083D1',lickcolor = 'grey'):
    lineoffsets2 = 1
    linelengths2 = 1
    
    
    # create a horizontal plot
    figure = plt.figure()

    for i, row in df.iterrows():
        
        
        plt.hlines(i, row['go_odor'][0], row['go_odor'][1],color = gocolor,alpha = 1,
                   linewidth = width,label = 'go odor' if i ==0 else '')
        plt.hlines(i, row['water_on'], row['water_off'],color = rewardcolor,
                   linewidth = width,label = 'water' if i ==0 else '')
        plt.hlines(i, row['nogo_odor'][0], row['nogo_odor'][1],color = nogocolor,alpha = 1,
                   linewidth = width,label = 'no go odor' if i ==0 else '')
        plt.hlines(i, 0, row['trial_end'],color = 'grey',alpha = 0.2,
                   linewidth = width)
        plt.hlines(i, row['control_odor'][0], row['control_odor'][1],alpha = 1,
                   linewidth = width,label = 'control odor' if i ==0 else '')
        
    plt.eventplot(df.licking, colors=lickcolor, lineoffsets=lineoffsets2,linelengths=linelengths2,alpha = 0.5, label = 'licking')
    
    ax = plt.subplot(111)    
    ax.spines["top"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    draw_loc = ax.get_xlim()[1]
    draw_loc2 = ax.get_ylim()[1]
    # create is correct
    try:
        
        for i in range(len(df.index)):
            #try:
            appear1 = 0
            appear2 = 0
            if df['trialtype'][i] in ['go','go_omit','c_reward','c_omit']:
                position = 1
            elif df['trialtype'][i] in ['no_go','background']:
                position = 2.3
            if df['is_Correct'][i]:
                plt.hlines(i, draw_loc+position, draw_loc+position+0.5,
                           color = '#A8DEA3',alpha = 1,linewidth = width,label = 'correct' if appear1 ==0 else '' ) #green
                appear1 = 1
            else:
                plt.hlines(i, draw_loc+position, draw_loc+position+0.5,
                           color = '#F9634B',alpha = 1,linewidth = width ,label = 'wrong' if appear2 ==0 else '') # red
                appear2 = 1
    
            
            
            #except:
            #    print("--------is_Correct data hasn't been merged ---------")
        #plt.xticks(fontsize=14)    
        ax.set_xlim([ax.get_xlim()[0],draw_loc+4])
    except:
        pass
    
    ax.get_xaxis().tick_bottom() 
    
    ax.get_yaxis().tick_left()
    plt.tick_params(axis="both", which="both", bottom=False, left = False, top = False, right = False,
                    labelbottom="on", labelleft="on",labelsize = 14)   
    plt.ylabel('Trials',fontsize = 18)
    plt.xlabel('Time(s)',fontsize = 18)
    ax.set_ylim(bottom=-1,ymax = len(df.index))
    ax.set_xlim(left=-0.2)
    
    plt.text(draw_loc +0.8, draw_loc2-3, 'hit', fontsize=14)
    plt.text(draw_loc +1.6, draw_loc2-3, 'rejection', fontsize=14)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(),prop={'size': 14},loc='upper center', bbox_to_anchor=(0.5, 1.07),
          frameon=False,fancybox=False, shadow=False, ncol=3)
    datetime.now().strftime("%Y-%m-%d-%H-%M")
    plt.suptitle('{} eventplot on {}'.format(mouse_id, exp_date),fontsize = 20, y = 0.96)
    if save:
        try:
            savepath = "{1}/{0}/{2}".format(mouse_id,save_dir,date.today())
            os.makedirs(savepath)
        except:
            pass
        figure.set_size_inches(figuresize[0], figuresize[1])
    
        plt.savefig("{0}/{1}_{2}.png".format(savepath,exp_date,filename), bbox_inches="tight", dpi = 100)

        
        #    print('error while saving')
    
    plt.show()
    return figure



#-------------------------
#%% import data
    ### change path in the function import part
mouse_names = ['C37','C38','C39','C40']

path = 'D:/PhD/Behavior/behavior_21_02/close_far_2021_01_Pav/'
for mouse_id in mouse_names:    
    
    load_path = os.path.join(path,'parsed_dataframe_pickle/{0}_stats.pickle'.format(mouse_id))
    mouse = load_pickleddata(load_path)
    
    #event plot with trials and iscorerct data
    
    # assign two df 
    mouse_trials = mouse.df_trials
    mouse_iscorrect = mouse.df_trials_iscorrect
    # choose a date
    all_days = mouse.all_days
    print('-----------------------------------------------------------')
    print('there are ', len(all_days),'days, condition days is ', len([x for x in mouse.training_type if x == 'cond']))
    for index in range(len(all_days)):
        print('you are looking at day ', all_days[index],'training type is ',mouse.training_type[index] )
        day = all_days[index] 
        
        save_dir = os.path.join(path,'figures')
        # concatenate data
        merge_trials_iscorrect = mouse_trials[day].copy() # need to be hard copy
        try: # for condition days
            merge_trials_iscorrect['is_Correct'] = mouse_iscorrect[day]['is_Correct']# join df_trials and df_isccorect serial
        except: # degradation days don't have is_correct
            pass
        # plot
        figure = event_plot(merge_trials_iscorrect,mouse_id = mouse.mouse_id,exp_date = day,filename = 'all_trials',save = True,save_dir = save_dir)
        
        # only choose go trials for above day
        is_go_trials = merge_trials_iscorrect['trialtype'] == 'go' #or 'go_omit' # index of go trials
        merged_go_trials = merge_trials_iscorrect[is_go_trials] # select out the go trials from the merged dataset
        merged_go_trials.index = range(len(merged_go_trials)) # reindex the index; otherwise the index will be original index like 1,4,14,23,etc
        
        # plot
        figure = event_plot(merged_go_trials,mouse_id = mouse.mouse_id,exp_date = day,filename = 'go_trials',save = True, save_dir = save_dir,width = 3,figuresize = [12,15])
        # only choose no_go trials for above day
        is_nogo_trials = merge_trials_iscorrect['trialtype'] == 'no_go' # index of no_go trials
        merged_nogo_trials = merge_trials_iscorrect[is_nogo_trials] # select out the no_go trials from the merged dataset
        merged_nogo_trials.index = range(len(merged_nogo_trials)) # reindex the index; otherwise the index will be original index like 1,4,14,23,etc
        # plot
        figure = event_plot(merged_nogo_trials,mouse_id = mouse.mouse_id,exp_date = day,filename = 'no_go_trials',save = True, save_dir = save_dir,width = 3,figuresize = [12,15])
        
        # only choose empty trials for above day
        is_background_trials = merge_trials_iscorrect['trialtype'] == 'background' # index of background trials
        merged_background_trials = merge_trials_iscorrect[is_background_trials] # select out the background trials from the merged dataset
        merged_background_trials.index = range(len(merged_background_trials)) # reindex the index; otherwise the index will be original index like 1,4,14,23,etc
        # plot
        figure = event_plot(merged_background_trials,mouse_id = mouse.mouse_id,exp_date = day,filename = 'background_trials',save = True, save_dir = save_dir,width = 3,figuresize = [12,15])
    
    
    
    
    
    
    # #%%
    # # only choose go trials for above day
    # is_go_trials = merge_trials_iscorrect['trialtype'] == 'go' #or 'go_omit' # index of go trials
    # merged_go_trials = merge_trials_iscorrect[is_go_trials] # select out the go trials from the merged dataset
    # merged_go_trials.index = range(len(merged_go_trials)) # reindex the index; otherwise the index will be original index like 1,4,14,23,etc
    # # plot
    # figure = event_plot(merged_go_trials,mouse_id = mouse.mouse_id,exp_date = day,filename = 'go_trials',save = True, save_dir = save_dir,width = 3,figuresize = [12,10])
    
    # # only choose no_go trials for above day
    # is_nogo_trials = merge_trials_iscorrect['trialtype'] == 'no_go' # index of no_go trials
    # merged_nogo_trials = merge_trials_iscorrect[is_nogo_trials] # select out the no_go trials from the merged dataset
    # merged_nogo_trials.index = range(len(merged_nogo_trials)) # reindex the index; otherwise the index will be original index like 1,4,14,23,etc
    # # plot
    # figure = event_plot(merged_nogo_trials,mouse_id = mouse.mouse_id,exp_date = day,filename = 'no_go_trials',save = True, save_dir = save_dir,width = 3,figuresize = [10,5])
    
    # # only choose empty trials for above day
    # is_background_trials = merge_trials_iscorrect['trialtype'] == 'background' # index of background trials
    # merged_background_trials = merge_trials_iscorrect[is_background_trials] # select out the background trials from the merged dataset
    # merged_background_trials.index = range(len(merged_background_trials)) # reindex the index; otherwise the index will be original index like 1,4,14,23,etc
    # # plot
    # figure = event_plot(merged_background_trials,mouse_id = mouse.mouse_id,exp_date = day,filename = 'background_trials',save = True, save_dir = save_dir,width = 3,figuresize = [10,6])
    
    
    # #%%
    # del_date = []



                       