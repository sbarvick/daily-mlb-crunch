from __future__ import print_function
import sys, getopt
from player_data import PlayerData
from datetime import datetime
import tempfile


def main(argv):

    # process the inputs
    data_dir = tempfile.tempdir
    try:
        opts, args = getopt.getopt(argv, 'hd:', ['directory='])
    except getopt.GetoptError:
        print('daily_crunch.py -d <data directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('daily_crunch.py -d <data directory>')
            sys.exit()
        elif opt in ("-d", "--directory"):
            data_dir = arg

    # get the daily stats data
    try:
        pd = PlayerData(datetime.today(), data_dir)
    except Exception as e:
        print(e.message)
        sys.exit(2)

    # simple/sample algorithm
    # find the greatest delta between batter's avg and pitcher's ERA for batters batting opposite the pitcher's throwing
    todays_list = {}
    batter_id = 0
    pitcher_id = 0
    for matchup in pd.today_data:
        batter_id = int(matchup['MLB_ID'])
        pitcher_id = int(matchup['MLB_ID(p)'])

        # only proceed with this matchup if we have pitcher stats to go with
        pitcher = pd.get_player(pitcher_id)
        batter = pd.get_player(batter_id)
        if pitcher != None and batter != None:
            # for simple comparison, scale batting average
            try:
                s_avg = batter.summary_stats['avg'] * 10
                era = pitcher.summary_stats['era']
                if matchup['Bats'] != matchup['Throws']:
                    todays_list[batter_id] = s_avg + era
            except Exception as e:
                print("Exception calculating matchup: " + e.message)

    # now sort and spit out the top picks
    print("Today's top recommendations considering handedness are: ")
    choices = sorted(todays_list, key = todays_list.get, reverse=True)
    for item in choices[:10]:
        batter = pd.get_player(item)
        print('{} with {} avg at {} combined score'.format(batter.name, batter.summary_stats['avg'], todays_list[item]))

    # do it again (what a case for lambdas!
    todays_list = {}
    for matchup in pd.today_data:
        batter_id = int(matchup['MLB_ID'])
        pitcher_id = int(matchup['MLB_ID(p)'])

        # only proceed with this matchup if we have pitcher stats to go with
        pitcher = pd.get_player(pitcher_id)
        batter = pd.get_player(batter_id)
        if pitcher != None and batter != None:
            # for simple comparison, scale batting average
            try:
                s_avg = batter.summary_stats['avg'] * 10
                era = pitcher.summary_stats['era']
                todays_list[batter_id] = s_avg + era
            except Exception as e:
                print("Exception calculating matchup: " + e.message)

    # now sort and spit out the top picks
    print("\nToday's top recommendations NOT considering handedness are: ")
    choices = sorted(todays_list, key=todays_list.get, reverse=True)
    for item in choices[:10]:
        batter = pd.get_player(item)
        print('{} with {} avg at {} combined score'.format(batter.name, batter.summary_stats['avg'], todays_list[item]))


if __name__ == "__main__":
   main(sys.argv[1:])