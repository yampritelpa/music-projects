# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:45:41 2019

@author: Priyam
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def length_mask(df,upper=2.7e5,lower=1.5e5):
    length_mask = (df['duration_ms']>upper)|(df['duration_ms']<lower)
    return length_mask

def split_table(music_table):
    labels = music_table.select_dtypes('object')
    labels['release date'] = pd.to_datetime(labels['release date'],errors='coerce')
    music_table[['key','mode','time_signature']] = music_table[['key','mode','time_signature']].astype('object')
    features = music_table.drop(labels,1)
    mask = length_mask(features)
    labels = labels.drop(features[mask].index)
    features = features.drop(features[mask].index)

    return features, labels



def merge_tables(target_feats,target_labels,others_feats,others_labels):
    target_labels['rating']=1
    others_labels['rating']=0
    labels=pd.concat([target_labels,others_labels],0).reset_index(drop=True)
    feats =pd.concat([target_feats,others_feats],0).reset_index(drop=True)
    
    ind=pd.isnull(feats).any(1).nonzero()[0]
    feats = feats.drop(list(ind),0).reset_index(drop=True)
    labels = labels.drop(list(ind),0).reset_index(drop=True)
    
    return labels, feats

def load_data(target_filename,reference_filename):
    mm_feats, mm_labels = split_table(pd.read_csv(target_filename))
    other_feats, other_labels = split_table(pd.read_csv(reference_filename))
    other_feats = other_feats.drop('0',1)
    
    sum_labels, sum_feats = merge_tables(mm_feats,mm_labels,other_feats,other_labels)
    
    y = sum_labels['rating']
    x = sum_feats
    return x,y, sum_labels

#%%

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import GradientBoostingClassifier

x,y,sum_labels = load_data('red-velvet-features.csv','rv-comparison-features.csv')
x_train, x_val, y_train, y_val = train_test_split(x,y)
x_smote, y_smote = SMOTE().fit_resample(x_train,y_train)
x_smote = pd.DataFrame(x_smote,columns=x_train.columns)

num_processor = Pipeline([('scaler',StandardScaler())])
cat_processor = Pipeline([('ohe',OneHotEncoder())])
processor = ColumnTransformer([('num',num_processor,x_smote.select_dtypes('float64').columns),
                               ('cat',cat_processor,x_smote.select_dtypes('object').columns)
                               ])
model = Pipeline([('processor',processor),
                  ('classifier',GradientBoostingClassifier(learning_rate=0.1,n_estimators=1000))])
    
model.fit(x_smote,y_smote)

#%%
from sklearn.metrics import classification_report, roc_auc_score


guesses = model.predict_proba(x_val)[:,1]
answers = sum_labels.iloc[y_val.index][['artist name','rating','song title','release date']]
results = pd.concat([answers.reset_index(drop=True),pd.Series(guesses,name='guesses')],1)
results = results.sort_values(['rating','guesses'],ascending=False)
print(classification_report(y_val,np.round(guesses)))
print(roc_auc_score(y_val,np.round(guesses)))

fn_mask = (results['guesses']<0.2) & (results['rating']==1)
fp_mask = (results['guesses']>0.8) & (results['rating']==0)

fn = results[fn_mask].drop('rating',1)
fp = results[fp_mask].drop('rating',1)



#%%
fp.to_csv('rv-false-positives.csv',header=True,index=None)