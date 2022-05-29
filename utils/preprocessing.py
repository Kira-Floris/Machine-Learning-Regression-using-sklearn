#!/usr/bin/env python
# coding: utf-8

# In[96]:


# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# timestamp transformation
import datetime
import time

# encoder
from sklearn.preprocessing import LabelEncoder

class Preprocessing:
    def __init__(self, df:pd.DataFrame, target):
        self.df = df
        self.target = target
    
    def transformToTimestamp(self, columns=[]):
        for column in columns:
            timestamped_dates = []
            for data in self.df[column]:
                date_ = str(data)
                element = datetime.datetime.strptime(date_,"%Y-%m-%d %H:%M:%S")
                timestamp = datetime.datetime.timestamp(element)
                timestamped_dates.append(timestamp)
            self.df[column+' timestamped'] = timestamped_dates
        return self.df
    
    def setDateToIndex(self, column):
        self.df.index = pd.to_datetime(self.df[column], format="%Y-%m-%d %H:%M:%S")
        return self.df
    
    def transformDatesMore(self, columns=[]):
        for column in columns:
            # sample = %Y-%m-%d %H:%M:%S
            month_list = []
            quartile_list = []
            morning_or_night = []
            for data in column:
                # split date and time
                temp = data.split()
                date_ = temp[0]
                time_ = temp[1]
                
                # get month
                date_split = date_.split("-")
                year = date_split[0]
                month = date_split[1]
                day = date_split[2]
                month_list.append(month)
                
                # get quartile
                quartile = 0
                if month <=3:
                    quartile = 1
                if month >3 and month <= 6:
                    quartile = 2
                if month >6 and month <= 9:
                    quartile = 3
                if month >9 and month <= 12:
                    quartile = 4
                quartile_list.append(quartile)
                    
                # get morning or night; 0 or 1
                time_split = time_.split(":")
                hour = time_split[0]
                m_or_n = null
                if hour <= 12:
                    m_or_n = 0
                else:
                    m_or_n = 1
                morning_or_night.append(m_or_n)
            self.df['month'] = month_list
            self.df['quartile'] = quartile_list
            self.df['morning or night'] = morning_or_night
        return self.df
                    
                
                

    def labelEncodingColumns(self, skip=[]):
        columns = list(self.df.columns)
        encoder = LabelEncoder()
        
        # skip specified columns 
        if skip:
            for column in skip:
                columns.remove(column)
                
        # remove target from encoded data
        columns.remove(self.target)
        
        for column in columns:
            # check if column is object or string
            if self.df[column].dtypes == 'object' or self.df[column].dtypes == 'str':
                self.df[column] = encoder.fit_transform(self.df[column])
        return self.df
    
    def featureSelectionCorrelation(self, effect=0.5, plot=False):
        corr = self.df.corr()
        target_corr = corr[self.target]
        selected_columns = []
        
        # plot if true
        if plot:
            plt.figure(figsize=(18,8))
            heatmap = sns.heatmap(self.df.corr(method='pearson'), annot=True, fmt='.1g', vmin=-1, vmax=1, center=0, cmap='inferno', linewidths=1, linecolor='Black')
            heatmap.set_title('correlation heatmap between variables')
            heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=90)
            plt.show()
        
        # select according to specifiedeffect value
        # default 0.5
        for i in range(len(target_corr)):
            # select columns higher or lower than effect value
            if target_corr[i] >= effect or target_corr[i] <= -effect:
                selected_columns.append(corr.columns[i])
                
        return self.df[selected_columns], selected_columns


# In[ ]:




