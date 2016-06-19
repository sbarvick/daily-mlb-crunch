from __future__ import print_function
import sys, getopt
from player_data import PlayerData
from datetime import datetime
import tempfile
from algorithm import Algorithm


class AVG_ERA(Algorithm):
    '''
    Algorithm that just adds the pitcher's ERA and the batter's AVG (x10) and finds the biggest number
    '''
    def __init__(self, date, data_dir):
        super(AVG_ERA, self).__init__(date, data_dir)

        # simple/sample algorithm
        # find the greatest delta between batter's avg and pitcher's ERA for batters batting opposite the pitcher's throwing
        todays_list = {}
        for matchup in self.player_data.today_data:
            batter_id = int(matchup['MLB_ID'])
            pitcher_id = int(matchup['MLB_ID(p)'])

            # only proceed with this matchup if we have pitcher stats to go with
            pitcher = self.player_data.get_player(pitcher_id)
            batter = self.player_data.get_player(batter_id)
            if pitcher != None and batter != None:
                # for simple comparison, scale batting average
                try:
                    s_avg = batter.summary_stats['avg'] * 10
                    era = pitcher.summary_stats['era']
                    todays_list[batter_id] = s_avg + era
                except Exception as e:
                    print("Exception calculating matchup: " + e.message)

        # now sort (don't reverse so that the resulting list is in the correct order)
        self.results = [(k, todays_list[k]) for k in sorted(todays_list, key=todays_list.get, reverse=True)]


class AVG_ERA_handed(Algorithm):
    '''
        Algorithm that adds the pitcher's ERA and the batter's AVG (x10) and finds the biggest number but then filters on the
        '''
    def __init__(self, date, data_dir):
        super(AVG_ERA_handed, self).__init__(date, data_dir)

        # simple/sample algorithm
        # find the greatest delta between batter's avg and pitcher's ERA for batters batting opposite the pitcher's throwing
        todays_list = {}
        for matchup in self.player_data.today_data:
            batter_id = int(matchup['MLB_ID'])
            pitcher_id = int(matchup['MLB_ID(p)'])

            # only proceed with this matchup if we have pitcher stats to go with
            pitcher = self.player_data.get_player(pitcher_id)
            batter = self.player_data.get_player(batter_id)
            if pitcher != None and batter != None:
                # for simple comparison, scale batting average
                try:
                    s_avg = batter.summary_stats['avg'] * 10
                    era = pitcher.summary_stats['era']
                    if matchup['Bats'] != matchup['Throws']:
                        todays_list[batter_id] = s_avg + era
                except Exception as e:
                    print("Exception calculating matchup: " + e.message)

        # now sort (don't reverse so that the resulting list is in the correct order)
        self.results = [(k, todays_list[k]) for k in sorted(todays_list, key=todays_list.get, reverse=True)]


if __name__ == "__main__":

    # process the inputs
    data_dir = tempfile.tempdir
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hd:', ['directory='])
    except getopt.GetoptError:
        print('daily_crunch.py -d <data directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('daily_crunch.py -d <data directory>')
            sys.exit()
        elif opt in ("-d", "--directory"):
            data_dir = arg

    # run the test for batting average + era considering the opposite pitcher/hitter handedness idea
    this_alg = AVG_ERA_handed(datetime.today(), data_dir)
    print("Today's top recommendations considering handedness are: ")
    for result in this_alg.get_top_picks(5):
        batter = this_alg.player_data.get_player(result[0])
        print('{} with {} avg at {} combined score'.format(batter.name, batter.summary_stats['avg'], result[1]))

    # run the test for batting average + era NOT considering the opposite pitcher/hitter handedness idea
    this_alg = AVG_ERA(datetime.today(), data_dir)
    print("Today's top recommendations NOT considering handedness are: ")
    for result in this_alg.get_top_picks(5):
        batter = this_alg.player_data.get_player(result[0])
        print('{} with {} avg at {} combined score'.format(batter.name, batter.summary_stats['avg'], result[1]))