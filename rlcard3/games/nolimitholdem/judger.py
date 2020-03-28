from rlcard3.games.limitholdem.judger import LimitholdemJudger

class NolimitholdemJudger(LimitholdemJudger):
    ''' The Judger class for Texas Hold'em
    '''

    def __init__(self):
        ''' Initialize a judger class
        '''
        super(NolimitholdemJudger, self).__init__()
