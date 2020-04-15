import numpy as np

##### DESCRIPTION #####
# This part of the module handles the mathematic
# formulation for channel coefficients estimation

# Compute the first and second coefficients of the fft considering that the third one is 0
def get_fft_01(rss):                         # Vector with the 4 rrs-like values corresponding to the required measurements [paper]
    n_nan = sum(np.isnan(rss))               # Number of NaNs in rss (maximum of 1)
    if n_nan > 1:                            # If there's more than 1, return a NaN
        return np.nan
    if n_nan == 1:
        ii = np.where(np.isnan(rss))[0]      # If there's only one, then solve it using that the third coefficient
        fft_3_coefs = np.array([1, -1, 1, -1])
        if ii%2 == 0:
            rss[ii] = -np.nansum(rss*fft_3_coefs)
        else:
            rss[ii] = np.nansum(rss*fft_3_coefs)
    fft_0 = np.mean(rss)                     # First coefficient
    fft_1 = np.dot(rss, [1, 1j, -1, -1j])/4  # Second coefficient
    return fft_0, fft_1

# Compute the channe coefficient from the measures corresponding to that antenna assuming the antenna is off
def get_coef_off(rss):                       # Vector with the 4 rrs-like values corresponding to the required measurements [paper]
    fft_0, fft_1 = get_fft_01(rss)           # Get first and second fft coefficients
    a = 2*np.abs(fft_1)                      # Amplitude of the wave
    b = np.max((fft_0, a))                   # Constant offset of the wave
    top = np.sqrt(b+a)                       # High point of the wave (undoing the square)
    bot = np.sqrt(b-a)                       # Low point of the wave  (undoing the square)
    amplitude = (top - bot)/2                # The amplitude of the coefficient is half the difference between top and bot
    coef = amplitude*fft_1/np.abs(fft_1)     # The coefficient has the same phase as fft_1
    return coef

# Compute the channel coefficient from the measures corresponding to that antenna assuming the antenna is on
def get_coef_on(rss, phase_0):               # Vector with the 4 rrs-like values corresponding to the required measurements [paper] and phase of the antenna when it was on
    fft_0, fft_1 = get_fft_01(rss)
    a = 2*np.abs(fft_1)
    b = np.max((fft_0, a))
    top = np.sqrt(b+a)
    bot = np.sqrt(b-a)
    amplitude = (top - bot)/2                # So far its the same as for get_coef_off
    phase = np.angle(fft_1)                  # This time we compute the phase to later correct it
    amplitude_0 = (top + bot)/2              # The amplitude of the array response of all the other antennas is the middle point between top and bot
    phase -= np.angle(amplitude_0 + amplitude*np.exp((phase - phase_0)*1j)) # Phase correction described in the paper
    return amplitude*np.exp(1j*phase)
