from __future__ import print_function
from batter import Batter
from pitcher import Pitcher
import mlbgame
from datetime import datetime
from datetime import timedelta
from dateutil import parser
import requests
import tempfile
from csv import DictReader


class PlayerData(object):
    ''' Pitcher and Batter data collected and stored from the various sources so that it can
        be accessed from data mining or model exercising code

        This code depends upon mlbgame data and remember to run mlbgame-update to get the latest
        See: http://panz.io/mlbgame/ for more info
    '''

    # Main configuration parameters - these don't change very often...
    YEAR = 2016
    STATS_SCOPE = 5   # number of days back to look at the stats
    USER = 'XXXX'
    KEY = 'XXXX'

    # dicts for pitcher and batter objects indexed by mlb id
    _pitcher_stats = {}
    _batter_stats = {}

    # file and list of dictionary stats collected for today
    today_file = ""
    today_data = []

    def __init__(self, date):
        '''
        Initialize with the desired stats date and assume the desired output based on the stats date
        :param datetime date: The desired stats processing date
        '''
        self._date = date

        # process the stats for the current year from the beginning of the season through the date
        # if stats don't exist, either because it is before the season starts or haven't been loaded
        # year, catch the Exception and move on
        today_yday = self._date.timetuple().tm_yday
        for yday in range(today_yday - self.STATS_SCOPE, today_yday):
            self._process_mlb_day_stats(yday)

        # process the daily stats for today
        self._process_dailybaseballdata_stats()

        # run the summarization
        for id, pitcher in self._pitcher_stats.items():
            pitcher.summarize()
        for id, batter in self._batter_stats.items():
            batter.summarize()


    def _process_mlb_day_stats(self, yday):
        '''
        Process the mlbgame data for a single day
        :param int yday: The day of the year to grab the stats for
        '''

        # get the month and day from the yday number
        date = datetime(self.YEAR, 1, 1) + timedelta(yday - 1)
        print("Adding stats for {} {}".format(date.strftime("%B"), date.day))

        # walk through all games for this day
        for gamenumber in range(0, 16):
            try:
                game = mlbgame.day(2016, date.month, date.day)[gamenumber]
                stats = mlbgame.player_stats(game.game_id)

                # do pitchers first
                p_stats = stats['home_pitching'] + stats['away_pitching']
                for pitcher in p_stats:
                    if pitcher.id in self._pitcher_stats:
                        pitcher_record = self._pitcher_stats[pitcher.id]
                    else:
                        pitcher_record = Pitcher(pitcher.name, pitcher.name_display_first_last, pitcher.id)
                        self._pitcher_stats[pitcher.id] = pitcher_record
                        #print('Added pitcher stats for {}'.format(pitcher_record))
                    pitcher_record.update_mlb_stats(pitcher)

                # now do batters, but don't add pitchers into batter_stats{}
                b_stats = stats['home_batting'] + stats['away_batting']
                for batter in filter (lambda b: b.id not in self._pitcher_stats, b_stats):
                    if batter.id in self._batter_stats:
                        batter_record = self._batter_stats[batter.id]
                    else:
                        batter_record = Batter(batter.name, batter.name_display_first_last, batter.id)
                        self._batter_stats[batter.id] = batter_record
                        #print('Added batter stats for {}'.format(batter_record))
                    batter_record.update_mlb_stats(batter)

            except Exception as e:
                #print(e.message)
                pass

    def _process_dailybaseballdata_stats(self):
        '''
        Process the daily stats from dailybaseballdata.com (requires a subscription
        '''
        # request the daily data
        r = requests.get(
            'http://dailybaseballdata.com/cgi-bin/dailyhit.pl?date=&xyear=2015&pa=1&showdfs=&sort=ops&r40=0&scsv=2&user={}&key={}&nohead=1'.
        format(self.USER, self.KEY))

        # write the data to a temporary file to more easily use the csv library
        self.today_file = tempfile.NamedTemporaryFile(delete=False)
        #print("writing to " + self.today_file.name)
        try:
            # write only the data starting with the second line
            self.today_file.write(r.text[r.text.find('MLB'):])
            self.today_file.close()

            # now read it back as a processed csv and make into dictionary
            today_dict = DictReader(open(self.today_file.name))
            for line in today_dict:
                # add this to a basic list for public use
                self.today_data.append(line)

                # add other interesting information to the player objects that we have (if we have one for the player)
                mlb_id = int(line['MLB_ID'])
                if mlb_id in self._batter_stats:
                    self._batter_stats[mlb_id].handed = line['Bats']
                if mlb_id in self._pitcher_stats:
                    self._pitcher_stats[mlb_id].handed = line['Throws']
                # if we start to pull out more interesting information, might need to pull this into a function

        except Exception as e:
            print("Exception: " + e.message)
        finally:
            pass

    def get_player(self, mlb_id):
        '''
        Return the player object for a specfic player by his mlb id
        (currently assumes we don't care as much about a pitcher's batting stats)
        :param int mlb_id: A player's mlb id (if 0, get the first (order unreliable))
        :return: the player object for a specific player or None if not found
        '''
        if mlb_id in self._pitcher_stats:
            return self._pitcher_stats[mlb_id]
        if mlb_id in self._batter_stats:
            return self._batter_stats[mlb_id]
        return None
