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
import matplotlib.pyplot as plt
import seaborn as sns
from kpop_helpers import *
from kpop_playlist import redvelvet,exid,mamamoo
 
exid = getFeatsPlaylist(exid)
mamamoo = getFeatsPlaylist(mamamoo)
redvelvet = getFeatsPlaylist(redvelvet)
top3 = mamamoo.append([exid,redvelvet],0)





badboy = AnalfromDB(redvelvet,'bad boy')
beats = pd.DataFrame(badboy['beats'])
bars = pd.DataFrame(badboy['bars'])
sections = pd.DataFrame(badboy['sections'])
segments = pd.DataFrame(badboy['segments'])
tatums = pd.DataFrame(badboy['tatums'])

sections['timestamp']=sections['duration'].cumsum()

hmm = segments[['start','duration','pitches','timbre']]

