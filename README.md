daily-crunch
============

Daily Crunch is a basic processor of [MLBGAME](http://panz.io/mlbgame)  
and [DailyBaseballData.com](http://dailybaseballdata.com/cgi-bin/dailyhit.pl)
data into a few classes and other data structures that can then be used to run your own data science 
experiments on the data, for instance, if you happen to by trying to [Beat The Streak](http://mlb.mlb.com/mlb/fantasy/bts/y2016/splash_index.jsp)   

# Data Sources
As mentioned, this code relies on two data sources.   You will need to go to those web sites and follow those instructions to ensure that you have access to that data in your python environment.  DailyBaseballData requires a subscription to get the daialy matchups.  It is not very much and it unlocks a whole lot of interesting things.

# Setup
This is not yet (if ever) to be in PyPi so you will need to pip install the following manually:

* pandas
* requests
* mlbgame
* datetime


# Quick Start

It is pretty raw, for personal and non-commercial use, so the current steps are:

1. Do pip install for the modules listed above
2. Usually daily, before the games start, run 

```
    python daily_download.py -u <username> -k <key> -d <full path to data directory>
```

3. To get sampple recommendations, run 

```
    python daily-crunch.py -d <full path to data directory>
```

# More Advanced

Add you own crunching algorithms on the data and see your results
