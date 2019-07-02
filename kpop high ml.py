# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:29:13 2019

The motivation for this is to use data to identify my next top 3 in Kpop.
Background: I got into Kpop through Brown Eyed Girls, miss A, and Secret. 
These groups do not perform anymore. Since then, my new top 3 has become
Red Velvet, EXID, and Mamamoo. Now, these 3 are nearing the end of their
career high. Could G-IDLE be next? Or is there some dark horse that I
have not considered.
I want to use musical analysis to drive the comparison. I will use the
Spotify API to get this data. For each track, I can access audio features,
metadata for the whole track, as well as audio analysis throughout the
audio sequence.

For a quick and easy start, I'll load the song features. These features, which
I imagine are calculated from song sequence data and an RNN-based model, gives
a convenienet summary of calculated parameters. It's not clear how these
parameters were calculated, but they give an approximate summary of each track.

Can I classify artist by training a model on these features?
Can I predict whether I like an artist by comparing their features with top 3?

To start with, let's find out if a classifer can distinguish the 3 artists from
only these features... It doesn't seem like it. The songs are pretty similar,
as they are pop songs. Maybe it would be easier to classify a single group...
Nope, not from this data. Will need more songs to compare with...

Ok, after adding a lot more songs from other groups, it seems like the
classifier can pick them out to over 90% accuracy. I'm quite surprised.
A major issue that's preventing me from properly analyzing my old top3 is that
Spotify doesn't have all their songs, nor are their features formatted in the
exact same way as tracks by newer artists. It's a bummer, but I can move
forward with the one-vs-many approach. Simple yet effective!

I tried 3 classifiers: AdaBoost, GradientBoost, and RandomForest. The latter 
two consistently score over 93% on my validation data. Amazingly, AdaBoost
achieves perfect classification on the validation set.
WHOOPS! I forgot to remove the target variable, which is why it scored so well.
After fixing the bug, scores are below 70%. Fun! One thing I can try is the
actual one-vs-many instead of this three-vs-many thing I'm doing. 

First, Mamamoo. IMO they have the most distinctive sound, so if my thinking is
sound, the classifier should recognize this. Validation scores are all above 80%, 
as high as 88%. 
Second, EXID. Again, classifier scores over 80%. This might actually be higher
than Mamamoo's score.
Third, Red Velvet. Once again, scores over 80% and into the 90s. That's great!

If one-vs-many scores in the 80-90% range, I'm not too upset that my attempt at
some-vs-many scored in the 60-70% range. If I assign unique labels to each of
my top3, I get a score in the 70% range. Removing PCA bumps it up to 80%...
Man, my PCA is not useful! 

Then, I can build a recommendation tool
that will suggest me 3 new groups. 


@author: Priyam
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from kpop_helpers import *
from kpop_playlist import redvelvet,exid,mamamoo
from kpop_playlist import apink,aoa,twice,gfriend,girlsday,chungha,sistar,stellar,bravegirls
from kpop_playlist import secret,missA,beg,fourminute,fx


    
exid = getFeatsPlaylist(exid)
mamamoo = getFeatsPlaylist(mamamoo)
redvelvet = getFeatsPlaylist(redvelvet)

secret = getFeatsPlaylist(secret)
beg = getFeatsPlaylist(beg)
missA = getFeatsPlaylist(missA)

apink = getFeatsPlaylist(apink)
aoa = getFeatsPlaylist(aoa)
twice = getFeatsPlaylist(twice)
gfriend = getFeatsPlaylist(gfriend)
girlsday = getFeatsPlaylist(girlsday)
chungha = getFeatsPlaylist(chungha)
sistar = getFeatsPlaylist(sistar)
stellar = getFeatsPlaylist(stellar)
bravegirls = getFeatsPlaylist(bravegirls)
fourminute = getFeatsPlaylist(fourminute)
fx = getFeatsPlaylist(fx)





exid = pd.concat([exid,pd.Series([2]*len(exid),name='group')],1)
mamamoo = pd.concat([mamamoo,pd.Series([1]*len(mamamoo),name='group')],1)
redvelvet = pd.concat([redvelvet,pd.Series([3]*len(redvelvet),name='group')],1)


top3 = mamamoo.append([exid,redvelvet],0)

others = apink.append([aoa,twice,gfriend,girlsday,chungha,sistar,stellar,bravegirls,secret,beg,fourminute,fx],0)
others['group']=0
total = top3.append([others],0)

#%%

from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from skopt import BayesSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier, LogisticRegression, RidgeClassifier
from sklearn.ensemble import GradientBoostingClassifier,AdaBoostClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_curve, roc_auc_score #for evaluating one-vs-many
from sklearn.manifold import TSNE
from sklearn.feature_selection import SelectKBest, VarianceThreshold
#

titles,data = stripFeatsTable(total)
titles.to_csv('songtitles_ratings.csv',header=True)
y = data['group']
X = data.drop(['group','instrumentalness'],1) #for use without PCA or scalers



cats = X[['key','mode','time_signature']].astype(str)
dummycats = pd.get_dummies(cats)



nums = X.drop(['key','mode','time_signature'],1)
nums = pd.DataFrame(nums).reset_index()
dummycats = dummycats.reset_index()
X = pd.concat([nums,dummycats],1).drop('index',1)

#%%
y0 = y.reset_index().drop('index',1).values
X_embedded = TSNE().fit_transform(X);plt.scatter(X_embedded[:,0],X_embedded[:,1],c=y0[:,0]);plt.show()

pca_pipe = make_pipeline(StandardScaler(),PCA(10))
X_pca = pca_pipe.fit_transform(X)

y0 = y.reset_index().drop('index',1).values
X_embedded = TSNE().fit_transform(X_pca);plt.scatter(X_embedded[:,0],X_embedded[:,1],c=y0[:,0]);plt.show()


#%%
xtr,xte,ytr,yte = train_test_split(X,y,train_size=0.75)



gbc = GradientBoostingClassifier()
gbc.get_params()

bayes = BayesSearchCV()

#%%
xtr,xte,ytr,yte = train_test_split(X,y,train_size=0.75)

model_gnb = GaussianNB();model_gnb.fit(xtr,ytr)
bayes_score = model_gnb.score(xte,yte)

model_lr = LogisticRegression();model_lr.fit(xtr,ytr)
logreg_score = model_lr.score(xte,yte)

model_rc = RidgeClassifier();model_rc.fit(xtr,ytr)
ridge_score = model_rc.score(xte,yte)

#model_sgd = SGDClassifier();model_sgd.fit(xtr,ytr)
#sgd_score = model_sgd.score(xte,yte)
#%%
xtr,xte,ytr,yte = train_test_split(X,y,train_size=0.75)
model_gbc = GradientBoostingClassifier(learning_rate=0.01,n_estimators=256)
model_gbc.fit(xtr,ytr)
gbc_score = model_gbc.score(xte,yte)
model_ada = AdaBoostClassifier(learning_rate=0.01);model_ada.fit(xtr,ytr)
ada_score = model_ada.score(xte,yte)
model_rf = RandomForestClassifier(n_estimators=256);model_rf.fit(xtr,ytr)
rf_score = model_rf.score(xte,yte)
avg_guess = (model_gbc.predict(xte)+model_ada.predict(xte)+model_rf.predict(xte))/3

avg_score = np.mean([bayes_score,logreg_score,ridge_score,gbc_score,ada_score,rf_score])

