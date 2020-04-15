import numpy as np
from . import codebook

##### DESCRIPTION #####
# This part of the module handles the
# high level ACO method logic

class ACO_low(object):
    """
    ACO_low.
    The method itself implemented
    """

# Initialize the method to a given number of antennas and a maximum codebook length
    def __init__(self, n_antennas, maximum_bps=64):                             # n_antennas is the number of antennas thils maximum_bps stands for the maximum codebook length
        super(ACO_low, self).__init__()
        # Parameters
        self.n_antennas = n_antennas
        self.maximum_bps = maximum_bps
        self.initial_codebook = [                                               # The method is provided with a default codebook, overwrite this variable with your own codebook if you have one
            np.array([codebook.get_phased_coef(a) for a in bp])
            for bp in np.fft.fft(np.eye(n_antennas))
        ]
        # Flow control
        self.stage = 0                                                          # The method starts at stage 0
        self.bp = None                                                          # Here will be stored the winner bp for communication
        self.antenna_index = []                                                 # Here will be stored the indices of the antennas that are being estimated with the selected codebook
        # Byproduct
        self.channel = np.zeros(n_antennas, dtype='complex')                    # Here will be stored the channel estimation (only the indices estimated, the rest will be zero)

# Create the codebook for ACO's next estimation
    def get_codebook(self):
        if self.stage == 0:                                                     # During the first stage we return the initial_codebook as we still don't have a good beam-pattern
            return self.initial_codebook[:self.maximum_bps]                     # The codebook is sent trimmed to not exceed the maximum codebook length
        return codebook.get_codebook(self.bp, self.antenna_index)               # Else, we compute the codebook required to estimate the selected channel antenna coefficients

# This function is called to set the antenna_index variable as a function of self.bp
# Keep in mind the formula "codebook length = 1 + 3*n_active_antennas + 4*n_search_antennas"
    def set_antenna_index(self):
        active_antennas = np.argwhere(self.bp != 0)[:, 0]                       # Get the active antennas
        if 1+3*len(active_antennas) >= self.maximum_bps:                        # If the set of active antennas is bigger than what the codebook allows to measure we trim it to a feasible set of indices and return it without search antennas, as active ones are more important
            self.antenna_index = active_antennas[:int(np.floor((self.maximum_bps-1)/3))]
            return
        inactive_antennas = np.argwhere(self.bp[:] == 0)[:, 0]                  # Get the inactive antennas
        n_search_antennas = int(np.floor(                                       # Compute how many inactive antennas we can make fit in the estimation
            (self.maximum_bps-(1+3*len(active_antennas)))/4
        ))
        if n_search_antennas == 0:                                              # If we can't  fit any more antennas in the estimation, just set the antenna_index to the active antennas
            self.antenna_index = active_antennas
            return
        if n_search_antennas > len(inactive_antennas):                          # If we can estimate all antennas, then set antenna_index to the index of all antennas
            self.antenna_index = np.arange(self.n_antennas)
            return
        search_antennas = np.random.choice(inactive_antennas, n_search_antennas)# Otherwise, choose n_search_antennas from the set of inactive antennas
        self.antenna_index = np.concatenate((active_antennas, search_antennas)) # Set the antenna_index to be the union of active_antennas and search_antennas

# Compute the beam-pattern for communication given the RSS measurement from the given codebook
    def get_winner_bp(self, rss):                                               # rss is a vector containing the measurements of the RSS
        if self.stage == 0:
            self.stage = 1                                                      # Mode into the next stage for the next iteration
            bp_max_index = np.argmax(rss)                                       # Find the strongest beam-pattern from the initial_codebook
            self.bp = self.initial_codebook[bp_max_index]                       # Set the beam-pattern for communication as the strongest one
            self.set_antenna_index()                                            # Update the antenna index for generating the codebook
            return self.bp
        else:
            subchannel_est = codebook.get_subchannel(self.bp, self.antenna_index, rss) # Make a subchannel estimation with the rss variable
            self.channel = np.zeros(self.n_antennas, dtype='complex')           # Initialize the channel estimation with zeros
            for ii, coef in zip(self.antenna_index, subchannel_est):
                self.channel[ii] = coef                                         # Fill the know coefficients for the channel
            self.bp = codebook.get_winner_bp(self.channel)                      # Get the winner bp for communication from the channel estimation
            self.set_antenna_index()                                            # Update the antenna index for generating the codebook
            return self.bp
