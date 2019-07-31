This repository contains Priyam's music-related projects. This branch is specifically to organize files for EXID song analysis, classification, and recommendation.

* **kpop_helpers.py** contains functions to pull audio features from Spotify's API (via spotipy).
* **kpop_playlist.py** contains URLs for 100 Korean pop artists on Spotify.
* **kpop api loader.py** combines the two to generate CSV files containing audio features for specified artists.
* **kpop exploration-exid.ipynb** walks through the exploratory data analysis for the group EXID and some of their contemporaries.
* **kpop-exid-model.ipynb** demonstrates a tree-based artist classifier and song recommender based on audio features.

Here's a quick rundown on how to use these scripts:
- First, specify artists in **kpop_playlist.py**. You want two lists, one containing your target artist(s) and one containing several contemporary artists for comparison.
- Then, run **kpop api loader.py** to generate CSV files for each of your lists.
- Next, do some EDA with Pandas and Matplotlib to understand the data better before building a model. My EDA for EXID revealed some unique qualities such as high danceability, compared to other groups. I wrote **kpop exploration-exid.ipynb** as a Jupyter notebook so it flows.
- Finally, build a classifier. The Jupyter notebook **kpop-exid-model.ipynb** continues where EDA left off. It concatenates the target artist(s) CSV with the other groups. This is a one-vs-many binary classification problem. 

False positives are songs from other artists that share similar audio features to the target artist. [My blog post](https://yampritelpa.wordpress.com/2019/07/01/project-kpop-classifier-recommender/) explains it with YouTube links so you can actually hear and compare yourself. 
