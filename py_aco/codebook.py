import numpy as np
from . import core

# Create a codebook for estimating the channel coefficients corresponding to some given antennas
def get_codebook(bp_ref, antenna_index):                  # bp_ref is the reference beam-pattern, antenna_index is the index of the antenna
    possible_coefs = [1, 1j, -1, -1j]
    bp_copy = [coef for coef in bp_ref]                   # Create a copy of the reference beam-pattern
    codebook = [bp_ref]                                   # Initialize the cobeboos to that beam-pattern
    for ii_antenna in antenna_index:                      # Generate the set of beam-patterns for computing each antenna
        if bp_ref[ii_antenna] == 0:                       # Design from when the antenna is off
            for coef in possible_coefs:                   # Assign all possible coefficients
                bp_copy[ii_antenna] = coef                # Assign that coefficient to the antenna
                codebook.append([aa for aa in bp_copy])   # Append a copy of the beam-pattern to the dictionary
            bp_copy[ii_antenna] = 0                       # Restore the original value to the beam-pattern
        else:                                             # Design for when the antenna is on
            coef_0 = bp_copy[ii_antenna]                  # Store the original value of the coefficient
            for coef in possible_coefs:                   # Assign all possible coefficients to the antenna excluding the one already assigned
                if coef == bp_copy:                       # Filter the coefficient already assigned there's no need to repeat values


def get_subchannel(bp_ref, antenna_index, rss):
    pass
