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