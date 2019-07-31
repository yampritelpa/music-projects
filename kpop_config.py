# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 23:31:59 2019

API to CSV

This file takes a list of artist URLs from the kpop_playlist file,
calls functions from kpop_helpers, and saves the data as CSV files.

@author: Priyam
"""

from kpop_playlist_v2 import artists
from kpop_helpers_v2 import *

import pandas as pd



artist_info_table = artists_info(artists)

artist_info_table.to_csv('compiled-artist-info.csv',header=True,index=None)

artist_music_table = artists_music(artists)

artist_music_table0 = artist_music_table.drop([0],1)
artist_music_table0.to_csv('compiled-kpop-features.csv',header=True,index=None)

load_test = pd.read_csv('compiled-kpop-features.csv')
