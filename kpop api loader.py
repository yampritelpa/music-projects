# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 23:31:59 2019

Generates CSV files containing audio features.

This file takes artist URLs (lists) from kpop_playlist_v2, then
calls functions in kpop_helpers to load data from these URLs.



@author: Priyam
"""

from kpop_playlist_v2 import exid,exid_comp,exid_cont,mamamoo,mamamoo_cmp
from kpop_playlist_v2 import redvelvet,rv_cmp,top3,artists0
from kpop_helpers_v2 import *
import pandas as pd

upper_length_limit = 2.5e5
lower_length_limit = 1.5e5


def process_music_table(music_table):
   """Removes rows with missing audio features."""
   
    music_table = music_table.dropna(0)
    return music_table

def to_csv_music_table(artists,filename):
   """
   Pulls data from Spotify API and generates CSV files.
   
   Parameters:
   artists (list): list of artist URLs imported from kpop_playlist_v2
   filename (str): desired output filename for CSV data
   """
    artist_info_table = artists_info(artists)
    artist_music_table = artists_music(artists)
    music_table = process_music_table(artist_music_table)
    
    #length_mask = (music_table['duration_ms']<lower_length_limit) | (music_table['duration_ms']>upper_length_limit)
    
    #music_table =  music_table.drop(music_table[length_mask]).reset_index(drop=True)
    #music_table[['key','mode','time_signature']] = music_table[['key','mode','time_signature']].astype('object')
    artist_music_table.to_csv(filename+'-features.csv',header=True,index=None)
    artist_info_table.to_csv(filename+'-info.csv',header=True,index=None)

to_csv_music_table([exid],'exid')
to_csv_music_table(exid_comp,'exid-comparison')
