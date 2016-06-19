from __future__ import print_function
import sys, getopt
from player_data import PlayerData
from datetime import datetime
from datetime import timedelta
import tempfile


class Algorithm(object):
    '''
    Base class that can be overridden with the specifics of an algorithm
    but also provides basic interfaces for calling by wrapper and infrastructure code
    '''

    def __init__(self, date, data_dir):
        '''
        Initialize with the date for which the algorithm should be run and the directory where
        the historical data is kept
        :param date: the date for which the algorithm is run
        :param data_dir: the location of the historical data
        '''

        # basic parameters
        self.date = date
        self.data_dir = data_dir

        # computed data as list of (MLB_ID, value) tuples
        self.results = {}

        # get the stats for this date
        yday = self.date.timetuple().tm_yday
        try:
            self.player_data = PlayerData(datetime(self.date.year, 1, 1) + timedelta(yday - 1), data_dir)
        except Exception as e:
            raise

    def __repr__(self):
        return 'Algorithm for {} with data from {} '.format(self.date, self.data_dir)

    def get_top_picks(self, number):
        '''
        Return the requested number of top picks
        :param number: the number of picks to return
        :return: a sorted (highest to lowest as sorted by execute) list of (MLB_ID, result) tuples.  This assumes the algorithm imposes the desired sorting
        '''
        return self.results[:number]