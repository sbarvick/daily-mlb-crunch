from __future__ import print_function
from datetime import datetime
import sys, getopt, os
import requests
import tempfile
import subprocess

#
# Fetch the daily mlbgame and dailybaseballdata.com data
#
# dailybaseballdata.com requires a subscription with a username and key
# access useful data so this will warn if you don't have that
def main(argv):

    # process the args
    username = ''
    userkey = ''
    data_dir = tempfile.tempdir
    try:
        opts, args = getopt.getopt(argv, 'hu:k:d:', ['username=', 'userkey=', 'directory='])
    except getopt.GetoptError:
        print('daily_update.py -u <username> -k <userkey> -d <data directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('daily_download.py -u <username> -k <userkey> -d <data directory>')
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-k", "--userkey"):
            userkey = arg
        elif opt in ("-d", "--directory"):
            data_dir = arg

    # update mlbgame is up to date
    print('Updating mlbgame data')
    subprocess.call('mlbgame-update')

    # request the daily data and write it to a file for later user
    if username == '' or userkey == '':
        print("Running without user information, only default data will be retrieved")

    try:
        r = requests.get(
        'http://dailybaseballdata.com/cgi-bin/dailyhit.pl?date=&xyear=2015&pa=1&showdfs=&sort=ops&r40=0&scsv=2&user={}&key={}&nohead=1'.
        format(username, userkey))
    except Exception as e:
        print('Exception encountered getting daily data: ' + e.message)

    today = datetime.today()
    today_file = os.path.join(data_dir,'{:02d}{:02d}{:4d}.txt'.format(today.month, today.day, today.year))
    print("Writing today's game data to " + today_file)
    with open(today_file, 'w') as f:
        # write only the data starting with the second line
        f.write(r.text[r.text.find('MLB'):])

if __name__ == "__main__":
   main(sys.argv[1:])