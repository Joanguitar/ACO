import numpy as np
import py_aco

n_antennas = 4
my_channel = py_aco.simulation.RandomChannel(n_antennas, snr=1000000)

bp_ref = [3, 0, 1j, 1]
my_channel.channel = bp_ref.copy()

my_channel.channel[1] += 0.5j

codebook = py_aco.codebook.get_codebook(bp_ref, np.arange(n_antennas))

rss = my_channel.measure_rss(codebook)

my_channel_est = py_aco.codebook.get_subchannel(bp_ref, np.arange(n_antennas), rss)

my_bp = py_aco.codebook.get_winner_bp(my_channel_est)