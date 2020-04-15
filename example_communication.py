import numpy as np
import py_aco
import matplotlib.pyplot as plt

# Parameters definition
n_antennas = 64
channel = py_aco.simulation.RandomChannel(n_antennas, snr=10)           # This is a simulation example, substitute this channel with your devices interface
# Note: the SNR above is the virtual SNR of the measurement after applying filters, not the communication one

# Initialize the method
ACO = py_aco.method.ACO_low(n_antennas)

# Initialize the statistical information
communication_power = []
channel_estimation_error = []

# Iterate the method
for iter in range(20):                                                  # At every iteration
    codebook = ACO.get_codebook()                                       # You will be given a codebook to load in your device
    rss = channel.measure_rss(codebook)                                 # You measure the codebook and get the RSS values (or proportional to RSS) in a vector, if there's any missing value you must fill it with a np.nan
    bp = ACO.get_winner_bp(rss)                                         # This function will give you the winner beam-pattern for communication and prepare next step's codebook for estimation
    # Statistics
    estimated_channel = ACO.channel                                     # Get the channel
    bp_power = np.square(np.abs(                                        # Get the power of the chosen beam-pattern for transmission
        np.dot(channel.channel, np.conj(bp))
    ))
    estimation_error = np.sqrt(np.maximum(                              # Compute the cordal complex error
        np.sum(np.square(np.abs(channel.channel))) +
        np.sum(np.square(np.abs(estimated_channel))) -
        2*np.abs(np.dot(channel.channel, np.conj(estimated_channel)))
        , 0)
    )
    communication_power.append(bp_power)
    channel_estimation_error.append(estimation_error)

# Plot the results
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
ax1.plot(communication_power)
ax2.plot(channel_estimation_error)
ax1.set_xlabel('iteration')
ax2.set_xlabel('iteration')
ax1.set_ylabel('Communication power')
ax2.set_ylabel('Channel error')
