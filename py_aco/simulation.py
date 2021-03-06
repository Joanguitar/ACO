import numpy as np

##### DESCRIPTION #####
# This part of the module provides for
# tools in case you want to do simulations
# It's not fully developed yet, but I'll
# try to implement more channel models

class Channel(object):
    """
    Base class for channel.
    Channel models need to have the function self.get_channel() defined
    """

# Initialize the channel to have a given number of antennas and an SNR
    def __init__(self, n_antennas, snr=3):
        super().__init__()
        self.n_antennas = n_antennas
        self.snr = snr
        self.channel = self.get_channel() # Each channel model needs to have this function defined to update the channel

# Function to get the noise that applies of the measured complex_gain, can be overwritten to not have AWGN
    def get_noise(self, n_samples):
        noise_std = np.power(10, -self.snr/20)                 # We compute the noise std, it's divided by 20 because we want amplitude instead of power
        noise = (
            np.random.randn(n_samples) +
            np.random.randn(n_samples)*1j
        )*noise_std/np.sqrt(2)                                 # White Gaussian Noise
        return noise

# Function that simulates the rss measure
    def measure_rss(self, codebook):
        complex_gains = np.dot(codebook, np.conj(self.channel))         # Complex gains is computed as the scalar product between a beam-pattern and the channel
        complex_gains += self.get_noise(len(complex_gains))    # Add complex white Gaussian noise
        rss = np.square(np.abs(complex_gains))                 # Compute the rss as the squared absolute value
        return rss

class RandomChannel(Channel):
    """
    RandomChannel. Extends Channel.
    Gaussian randomly generated channel
    """

    def __init__(self, *args, **kwargs):
        super(RandomChannel, self).__init__(*args, **kwargs)

# Function to get the channel
    def get_channel(self):
        channel = (                                            # Channel as random complex i.i.d. Gaussian
            np.random.randn(self.n_antennas) +
            1j*np.random.randn(self.n_antennas)
        )
        channel /= np.sqrt(                                    # Channel normallized to have an average (per antenna) power of 1
            np.mean(np.square(np.abs(channel)))
        )
        return channel
