import numpy as np
from . import core

##### DESCRIPTION #####
# This part of the module handles the
# beam-pattern design and usage in the estimation

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

# Round a number to the closest possible coefficient (1, 1j, -1 or -1j)
def get_phased_coef(a):                                   # a is the number we want to approax
    a_re = np.real(a)                                     # Real part
    a_im = np.imag(a)                                     # Real part
    if abs(a_im) > abs(a_re):                             # If the imaginary part is stronger, then it's closer to the imaginary axis
        return np.sign(a_im)*1j                           # Assign the sign of the imaginary axis
    else:                                                 # If the real part is stronger, then it's closer to the real axis
        return np.sign(a_re)                              # Assign the sign of the real axis

# Compute the beam-pattern described by the paper for analog beam-forming
def get_winner_bp(channel):                               # channel is the measured channel, note that it can be a subchannnel
    bp = np.zeros_like(channel)                           # Initialize the beam-pattern to zeros
    channel_abs = np.abs(channel)                         # Compute the amplitude of each channel coefficient
    I = np.argsort(channel_abs)[::-1]                     # Get the strongest antenna indices
    max_term = np.cumsum(                                 # Compute the term described in the paper for deciding the number of on antennas
        [channel_abs[ii] for ii in I]
    )/np.sqrt(np.arange(1, 1+len(channel)))               # \frac{sum_ii^k |a_ii|}{\sqrt{k}}
    n_active = np.argmax(max_term)+1                      # Compute the number of active antennas that maximizes previous expression
    for ii in I[:n_active]:                               # Set the n_active strongest antennas on
        bp[ii] = get_phased_coef(channel[ii])             # Assign it the closest possible coefficient to the corresponding channel coefficient
    return bp
