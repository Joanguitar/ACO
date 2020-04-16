# ACO
Adaptive Codebook Optimization

## Use for communication
Here's an [example](/ACO/example_communication.py).

For communication you can simply load the method as
```python
import py_aco
n_antennas = 16
maximum_bps = 64 # 64 by default if not specified
ACO = py_aco.method.ACO_low(n_antennas, maximum_bps=maximum_bps)
```
Here, `n_antennas` and `maximum_bps` are the number of antennas elements of the device's array and the maximum number of beam-patterns for the codebook.
For each iteration you can ask the method for the codebook to measure like `codebook = ACO.get_codebook()`.
You will then have to measure the RSS of each beam-pattern in the codebook and store those variables into a variable `rss` like in this [example](/ACO/example_communication.py).
In the example, the device is substituted by a simulation, but you should be able to easily design a pipeline.
Then the result is fed to the method like `bp = ACO.get_winner_bp(rss)` which also returns the winner beam-pattern for communication.

All that process becomes a beam-tracking algorithm.

As an additional feature, you can extract the estimated channel that's been used to compute the beam-pattern for communication.
To do so, after getting the beam-pattern you can add `estimated_channel = ACO.get_channel()` to get it. Note that the channel estimation is incomplete as the channel may not have been computed entirely due to the limit imposed by the maximum length of the codebook.

## Channel estimation
Here's an [example](/ACO/example_estimation.py).

If instead of communication you're interested in channel estimation but you only have RSS or RSS related (like SNR) measurements you can also apply this method for channel estimation.

First thing you'll need to do is to get a "good" beam-pattern for communication.
If you don't have one, you can run a few iterations of the ACO algorithm (1 or 2 should be enough), and get the beam-pattern outputted by `bp = ACO.get_winner_bp(rss)`.

Then after deciding the antenna indices you want to measure and store them in an iterable `I`, you can create a codebook for the channel estimation like `codebook = py_aco.codebook.get_codebook(bp, I)`.
If your codebook is too large to load in your device there's no need to panic, you can still batch it and measure it by chunks.
After measuring this codebook and storing the measured RSS values in the variable `rss`, you can get the subchannel corresponding to the antenna indices `I` as `estimated_subchannel = py_aco.codebook.get_subchannel(bp, I, rss)`.

Note that we've been using subchannel because you may be interested only in a subset of antennas, but if that's not your case you can still use `I = np.arange(n_antennas)` to get the whole channel.

## Contributing
This code relies on the idea that you have access to a device capable of measuring RSS.
If you have a tool to measure with a specific device, please contact me and I'll be pleased to link your repo from mine.
