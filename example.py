import numpy as np
import py_aco
import matplotlib.pyplot as plt

n_antennas = 64
channel = py_aco.simulation.RandomChannel(n_antennas, snr=1000000)
channel_power_bound = np.square(np.sum(np.abs(channel.channel)))

ACO = py_aco.method.ACO_low(n_antennas)

communication_power = []
channel_estimation_error = []
for iter in range(10):
    codebook = ACO.get_codebook()
    rss = channel.measure_rss(codebook)
    bp = ACO.get_winner_bp(rss)
    # Statistics
    estimated_channel = ACO.channel
    bp_power = np.square(np.abs(
        np.dot(channel.channel, np.conj(bp))
    ))
    if len(estimated_channel) > 0:
        estimation_error = np.sqrt(np.maximum(
            np.sum(np.square(np.abs(channel.channel))) +
            np.sum(np.square(np.abs(estimated_channel))) -
            2*np.abs(np.dot(channel.channel, np.conj(estimated_channel)))
            , 0)
        )
    else:
        estimation_error = -1
    communication_power.append(bp_power)
    channel_estimation_error.append(estimation_error)

plt.plot(communication_power)
plt.plot(channel_estimation_error)

estimated_channel = ACO.channel
