import numpy as np
from . import codebook

class ACO_low(object):
    """
    ACO_low.
    The method itself implemented
    """

    def __init__(self, n_antennas, maximum_bps=64):
        super(ACO_low, self).__init__()
        # Parameters
        self.n_antennas = n_antennas
        self.maximum_bps = maximum_bps
        self.initial_codebook = [
            [codebook.get_phased_coef(a) for a in bp]
            for bp in np.fft.fft(np.eye(n_antennas))
        ]
        # Flow control
        self.stage = 0
        self.bp = None
        self.antenna_index = []
        # Byproduct
        self.channel = np.zeros(n_antennas, dtype='complex')

    def get_codebook(self):
        if self.stage == 0:
            return self.initial_codebook
        return codebook.get_codebook(self.bp, self.antenna_index)

    def set_antenna_index(self):
        active_antennas = np.where(self.bp != 0)
        inactive_antennas = np.where(self.bp == 0)
        n_search_antennas = np.floor(
            (self.maximum_bps-(1+3*len(active_antennas)))/4
        )
        if n_search_antennas > len(inactive_antennas):
            self.antenna_index = np.arange(self.n_antennas)
            return
        search_antennas = np.random.choose(inactive_antennas, n_search_antennas)
        self.antenna_index = np.concatenate((active_antennas, search_antennas))

    def get_winner_bp(self, rss):
        if self.stage == 0:
            self.stage = 1
            bp_max_index = np.argmax(rss)
            self.bp = self.initial_codebook[bp_max_index]
            self.set_antenna_index()
            return self.bp
        else:
            subchannel_est = codebook.get_subchannel(self.bp, self.antenna_index, rss)
            self.channel = np.zeros(self.n_antennas, dtype='complex')
            for ii, coef in zip(self.antenna_index, subchannel_est):
                self.channel[ii] = coef
            self.bp = codebook.get_winner_bp(self.channel)
            self.set_antenna_index()
            return self.bp
