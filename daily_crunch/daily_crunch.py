from __future__ import print_function
from player_data import PlayerData
from datetime import datetime


if __name__ == "__main__":

    # get the daily stats data
    pd = PlayerData(datetime.today())

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
    for choice in sorted(todays_list, key = todays_list.get, reverse=True):
        batter = pd.get_player(choice)
        print('{} with {} avg at {} combined score'.format(batter.name, batter.summary_stats['avg'], todays_list[choice]))









