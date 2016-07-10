from player import Player

class Batter(Player):
    ''' A batter and all of his stats as collected from various means and
        manipulated in the base Player class most likely
    '''
    def __init__(self, name, name_display, id):
        """
        Return a batter object
        :param name:
        :param name_first_last:
        :param id: The mlbgame id for this batter, more useful than name for stats work
        """
        super(Batter,self).__init__(name, name_display, id)

        # cache the number of hits the last time the stats were calculated
        hits_today = 0

        # initialize the containers for all the stats we will be keeping
        self._columns = ['row','s_rbi','s_r','s_so','s_h','s_bb','so','h','ao','hbp','bb','slg','obp','ops','avg']


    def __repr__(self):
        return 'Batter(%s)' % self.name_display


    def get_hits(self, index):
        '''
        Returns the hits for this batter for the index to be used for testing algorithms
        This could be made easier, but for now the last entry (yesterday) is -1, etc
        :param index: the requested date index (from the start day) of the hits
        :return: The number of hits for the batter
        '''
        return self._df["h"].iloc[index]