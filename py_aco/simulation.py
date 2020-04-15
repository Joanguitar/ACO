import numpy as np

class Channel(object):
    """
    Base class for channel.
    Channel models need to have the function self.get_channel() defined
    """

# Initialize the channel to have a given number of antennas and an SNR
    def __init__(self, n_antennas, snr=3):
        super(, self).__init__()
        self.n_antennas = n_antennas
        self.snr = 3
        self.channel = self.get_channel() # Each channel model needs to have this function defined to update the channel

# Function to get the noise that applies of the measured complex_gain, can be overwritten to not have AWGN
    def get_noise(self, n_samples):
        noise = (
            np.random.randn(n_samples) +
            np.random.randn(n_samples)*1j
        )*noise_std/np.sqrt(2)                                 # White Gaussian Noise
        return noise

    def measure_rss(self, codebook):
        complex_gains = np.dot(codebook, self.channel)         # Complex gains is computed as the scalar product between a beam-pattern and the channel
        noise_std = np.pow(10, -self.snr/20)                   # We compute the noise std, it's divided by 20 because we want amplitude instead of power
        complex_gains += self.get_noise(len(complex_gains))    # Add complex white Gaussian noise
        rss = np.square(np.abs(complex_gains))                 # Compute the rss as the squared absolute value
        return rss
