from __future__ import print_function
import sys, getopt
from datetime import datetime
from datetime import timedelta
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
                    #print('Exception calculating matchup for {}: {}'.format(batter.name, e.message))
                    # if there is a problem with the field put a 0 in for the batter
                    todays_list[batter_id] = 0

        # now sort
        self.results = [(k, todays_list[k]) for k in sorted(todays_list, key=todays_list.get, reverse=True)]


    def __repr__(self):
        return 'Beat the Streak picking algorithm based on pitcher ERA and batter AVG'


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
                    #print('Exception calculating matchup for {}: {}'.format(batter.name, e.message))
                    # if there is a problem with the field put a 0 in for the batter
                    todays_list[batter_id] = 0

        # now sort
        self.results = [(k, todays_list[k]) for k in sorted(todays_list, key=todays_list.get, reverse=True)]


        def __repr__(self):
            return 'Beat the Streak picking algorithm based on pitcher ERA and batter AVG with filtering by opposite handedness matchup'

if __name__ == "__main__":

    # process the inputs
    data_dir = tempfile.tempdir
    date = datetime.today()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hd:o:', ['directory=', 'ordinal-date='])
    except getopt.GetoptError:
        print('daily_crunch.py -d <data directory> -o <ordinal date>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('daily_crunch.py -d <data directory> -o <ordinal date>')
            sys.exit()
        elif opt in ('-d', '--directory'):
            data_dir = arg
        elif opt in ('-o', '--ordinal-date='):
            date = datetime(2016, 1, 1) + timedelta(int(arg) - 1)

    # run the test for batting average + era considering the opposite pitcher/hitter handedness idea
    this_alg = AVG_ERA_handed(date, data_dir)
    print('Recommendations considering handedness for {} are: '.format(date.strftime("%B %d, %Y")))
    for result in this_alg.get_top_picks(5):
        batter = this_alg.player_data.get_player(result[0])
        print('{} with {} avg at {} combined score and {} hits yesterday'.format(batter.name, batter.summary_stats['avg'], result[1], batter.get_hits(-1)))

    # run the test for batting average + era NOT considering the opposite pitcher/hitter handedness idea
    this_alg = AVG_ERA(date, data_dir)
    print('Recommendations NOT considering handedness for {} are: '.format(date.strftime("%B %d, %Y")))
    for result in this_alg.get_top_picks(5):
        batter = this_alg.player_data.get_player(result[0])
        print('{} with {} avg at {} combined score and {} hits yesterday'.format(batter.name, batter.summary_stats['avg'], result[1], batter.get_hits(-1)))
