import numpy as np
import py_aco
import matplotlib.pyplot as plt

# Parameters definition
n_antennas = 16
maximum_bps = 128
channel = py_aco.simulation.RandomChannel(n_antennas, snr=10)           # This is a simulation example, substitute this channel with your devices interface
# Note: the SNR above is the virtual SNR of the measurement after applying filters, not the communication one

# Initialize the method
ACO = py_aco.method.ACO_low(n_antennas)

# Iterate the method to get a good beam-pattern for communication
for iter in range(4):                                                   # At every iteration
    codebook = ACO.get_codebook()                                       # You will be given a codebook to load in your device
    rss = channel.measure_rss(codebook)                                 # You measure the codebook and get the RSS values (or proportional to RSS) in a vector, if there's any missing value you must fill it with a np.nan
    bp = ACO.get_winner_bp(rss)                                         # This function will give you the winner beam-pattern for communication and prepare next step's codebook for estimation

I = np.arange(n_antennas)                                               # Select all antennas because we want to get the whole channel
codebook = py_aco.codebook.get_codebook(bp, I)                          # Get the required codebook for the estimation

# if your codebook is bigger that the maximum length allowed, split it into batches
if len(codebook) > maximum_bps:
    codebook_batches = np.array_split(
        codebook,
        int(np.ceil(len(codebook)/maximum_bps))
    )
    rss = []                                                            # Initialize your measures
    for codebook_batch in codebook_batches:
        rss.extend(channel.measure_rss(codebook_batch))                 # Concatenate each new measure batch to the total measures
else:
    rss = channel.measure_rss(codebook)

estimated_channel = py_aco.codebook.get_subchannel(bp, I, rss)          # Get the channel from the measurements

# Solution analysis
estimation_error = np.sqrt(np.maximum(                                  # Compute the cordal complex error
    np.sum(np.square(np.abs(channel.channel))) +
    np.sum(np.square(np.abs(estimated_channel))) -
    2*np.abs(np.dot(channel.channel, np.conj(estimated_channel)))
    , 0)
)
print('The total chordal complex error for the simulated channel is: {:3.5f}'.format(estimation_error))
print('That accounts for {:3.1}% of the total channel'.format(estimation_error/np.linalg.norm(channel.channel)))
