import numpy as np
import py_aco
import matplotlib.pyplot as plt

n_antennas = 64
channel = py_aco.simulation.RandomChannel(n_antennas, snr=1000000)
channel_power_bound = np.square(np.sum(np.abs(channel.channel)))

ACO = py_aco.method.ACO_low(n_antennas)

communication_power = []
channel_estimation_error = []
for iter in range(20):
    codebook = ACO.get_codebook()
    rss = channel.measure_rss(codebook)
    bp = ACO.get_winner_bp(rss)
    # Statistics
    estimated_channel = ACO.channel
    bp_power = np.square(np.abs(
        np.dot(channel.channel, np.conj(bp))
    ))
    estimation_error = np.sqrt(np.maximum(
        np.sum(np.square(np.abs(channel.channel))) +
        np.sum(np.square(np.abs(estimated_channel))) -
        2*np.abs(np.dot(channel.channel, np.conj(estimated_channel)))
        , 0)
    )
    communication_power.append(bp_power)
    channel_estimation_error.append(estimation_error)

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
ax1.plot(communication_power)
ax2.plot(channel_estimation_error)

estimated_channel = ACO.channel

#plt.plot(np.abs(estimated_channel))
len(codebook)
len(ACO.antenna_index)
