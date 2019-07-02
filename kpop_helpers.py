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


Then, I can build a recommendation tool
that will suggest me 3 new groups. 


@author: Priyam
"""
import pandas as pd
import requests
from kpop_config import TOKEN

TOKEN = 'Bearer '+ TOKEN

headers={'Authorization': TOKEN}

def extractCode(url):
    c = url.split('/')[-1]
    return c


def getAnalysis(code):
    a = 'https://api.spotify.com/v1/audio-analysis/' + code
    response = requests.get(a,headers=headers)
    js = response.json()
    return js

def url2get(url):
    c = extractCode(url)
    return getAnalysis(c)

def AnalfromDB(db,song):
    url = db[db['song title']==song]['analysis_url'].values[0]
    c = extractCode(url)
    js = getAnalysis(c)
    return(js)

def getManyFeats(list_of_song_nicknames):
    s = 'https://api.spotify.com/v1/audio-features?ids='
    for n in list_of_song_nicknames:
        c = extractCode(n)
        if n==1:
            s = s + c
        else:
            s = s + ',' + c
    return s

def getFeats(s):
    response = requests.get(s,headers = headers)
    js=response.json()
    return pd.DataFrame(js['audio_features'][1:])


def getFeatsPlaylist(playlist):
    url_list = list(playlist.values())
    song_list = pd.DataFrame(playlist.keys())
    song_list = song_list.rename(columns={0:'song title'})
    df = getFeats(getManyFeats(url_list))
    df = df.drop(['id','track_href','type','uri'],1)
    return pd.concat([song_list,df],1)


def hist(group):
    for n in ['acousticness','danceability','duration_ms','energy',
              'loudness','mode','tempo','time_signature','valence']:
        plt.hist(group[n])
        plt.title(n)
        plt.show()
        
def stripFeatsTable(db):
    db = db.drop('analysis_url',1)
    titles = db['song title']
    db = db.drop('song title',1)
    return titles,db