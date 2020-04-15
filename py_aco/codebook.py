import numpy as np
from . import core

# Create a codebook for estimating the channel coefficients corresponding to some given antennas
def get_codebook(bp_ref, antenna_index):                  # bp_ref is the reference beam-pattern, antenna_index is the index of the antenna
    possible_coefs = [1, 1j, -1, -1j]
    bp_copy = bp_ref.copy()                               # Create a copy of the reference beam-pattern
    codebook = [bp_ref]                                   # Initialize the cobeboos to that beam-pattern
    for ii_antenna in antenna_index:                      # Generate the set of beam-patterns for computing each antenna
        if bp_ref[ii_antenna] == 0:                       # Design from when the antenna is off
            for coef in possible_coefs:                   # Assign all possible coefficients
                bp_copy[ii_antenna] = coef                # Assign that coefficient to the antenna
                codebook.append(bp_copy.copy())           # Append a copy of the beam-pattern to the dictionary
            bp_copy[ii_antenna] = 0                       # Restore the original value to the beam-pattern
        else:                                             # Design for when the antenna is on
            coef_0 = bp_copy[ii_antenna]                  # Store the original value of the coefficient
            for coef in possible_coefs:                   # Assign all possible coefficients to the antenna excluding the one already assigned
                if coef != coef_0:                        # Filter the coefficient already assigned there's no need to repeat values
                    bp_copy[ii_antenna] = coef            # Assign that coefficient to the antenna
                    codebook.append(bp_copy.copy())       # Append a copy of the beam-pattern to the dictionary
            bp_copy[ii_antenna] = coef_0                  # Restore the original value to the beam-pattern
    return codebook

# Estimated the sub-channel coefficients corresponding to the indices of antenna_index
def get_subchannel(bp_ref, antenna_index, rss):           # bp_ref is the reference beam-pattern, antenna_index is the index of the antenna and rss the measured RSS vector
    possible_coefs = [1, 1j, -1, -1j]
    rss_copy = rss.copy().tolist()                        # Make a copy of the measured rss
    ref_rss = rss_copy.pop(0)                             # Store the measurement of the reference beam-pattern
    channel = []                                          # Initialize the channel to an empty list
    for ii_antenna in antenna_index:                      # Compute the antenna coefficient for all selected antennas
        if bp_ref[ii_antenna] == 0:                       # Antenna is off
            rss_4coef = [rss_copy.pop(0) for _ in range(4)] # All next 4 values correspong to the measurements for that antenna
            channel.append(core.get_coef_off(rss_4coef))  # Get that antenna channel coefficient and append it to the computed subchannnel
        else:                                             # Antenn is on
            coef_0 = bp_ref[ii_antenna]                   # Get the value of the antenna coefficient for the reference beam-pattern
            rss_4coef = []                                # Initialize the 4 rss values for computing the channel coefficient
            for coef in possible_coefs:                   # Get the measures for all coefficients
                if coef == coef_0:                        # If the coefficient is the one that had previously assigned, then it's not contained in the array
                    rss_4coef.append(ref_rss)             # Just assign the bp_ref measurement
                else:                                     # Is the measured beam-pattern is not the reference one
                    rss_4coef.append(rss_copy.pop(0))     # then get the measured value from the list
            channel.append(core.get_coef_on(rss_4coef, np.angle(coef_0))) # Get that antenna channel coefficient and append it to the computed subchannnel
    return channel
