from player import Player


class Pitcher(Player):
    ''' A pitcher and all of his stats as collected from various means and
        manipulated in the base Player class most likely
    '''
    def __init__(self, name, name_display, id):
        """
        Return a pitcher object
        :param name:
        :param name_first_last:
        :param id: The mlbgame id for this pitcher, more useful than name for stats work
        """
        super(Pitcher, self).__init__(name, name_display, id)

        # initialize the containers for all the stats we will be keeping
        #self._columns = ['row', 's_h', 'w', 'era', 'h', 'er', 'out', 'np', 's', 'r', 'game_score']  # for testing
        self._columns = ['row','s_ip','s_er','s_r','s_so','s_h','s_bb','w','bs','l','so','era','h', 'er','sv', 'hld', 'out', 'np','s','r', 'bf', 'game_score']


def __repr__(self):
    return 'Pitcher(%s)' % self.name_display







