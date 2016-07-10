import pandas as pd

class Player(object):
    ''' A batter and all of his stats as collected from various means and
        manipulated using pandas
    '''
    def __init__(self, name, name_display, id):
        """
        Return a player object
        :param name:
        :param name_first_last:
        :param id: The mlbgame id for this batter, more useful than name for stats work
        """
        self.name = name
        self.name_display = name_display
        self.handed = 'R'
        self.summary_stats = {}
        self._id = id

        # initialize the containers for all the stats we will be keeping
        self._columns = []
        self._row = 0
        self._df = pd.DataFrame()

    def __repr__(self):
        return 'Player {}, id {} '.format(self.name_display, self._id)

    @property
    def id(self):
        """
        The id property - the getter
        """
        return self._id

    def update_mlb_stats(self, record):
        '''
        Add an MLB record for a player into the dataframe collecting each playing day's stats.
        It is an MLB record or at least an object with parameters of the right names for to
        result in a __dict__ of the right keys
        :param record:
        :return:
        '''
        update = {'row': self._row}
        # create a dictionary of these stats to then add to the dataframe (except 'row')
        for x in filter(lambda col: col != 'row', self._columns):
            try:
                update[x] = record.__dict__[x]

                # add the current stats to the dataframe
                #self._df = self._df.append(update, ignore_index=True)
                #self._row += 1
            except Exception as e:
                # _columns may contain data elements that are not MLB data
                pass
        self._df = self._df.append(update, ignore_index=True)
        self._row += 1

    def update_stats_by_dict(self, update):
        '''
        This is used for testing at the moment to get stats in without using the MLB record structure
        :param update: A dictionary with the right stats
        '''
        update['row'] = self._row
        self._df = self._df.append(update, ignore_index=True)
        self._row += 1

    @property
    def df(self):
        """
        The stats DataFrame - the getter should anyone want to work with pandas data directly
        """
        return self._df

    @property
    def columns(self):
        """
        The columns list - the getter
        """
        return self._columns

    def summarize(self):
        """
        Return a row of stats summarized appropriate for the type of stat it is.
        This summary can get as sophisticated as it needs to in the future
        :return: Dict of stats by column with the right summarization applied
        """

        # initialize with the last of all stats
        last_row = self._df.iloc[-1]
        for x in self._columns:
            self.summary_stats[x] = last_row[x]

        # some stats should really be the mean so find that for those
        mean_stats = ['ip','s']
        for x in filter(lambda col: col in mean_stats, self._columns):
            self.summary_stats[x] = self._df[x].mean()

        # add in any top level stats/items
        self.summary_stats['handed'] = self.handed

        return self.summary_stats
