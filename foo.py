
#@title Data loading
print("Åtter")
import numpy as np

fname = []

for j in range(3):
   fname.append('steinmetz_part%d.npz'%j)

alldat = np.array([])
for j in range(len(fname)):
  alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))

print("data loading done")

# select just one of the recordings here. 11 is nice because it has some neurons in vis ctx.
dat = alldat[11]
print(dat.keys())

import matplotlib.pyplot as plt

spikes = dat["spks"]

def plot_raster(trail_number, spike_data=spikes):
  trail = np.array([neuron for neuron in spike_data[:, trail_number, :]])
  most_active_neuron_N = np.argmax(np.sum(trail, axis=1))
  spiketimes = np.zeros((len(trail), 300))

  for i, neuron in enumerate(trail):
    times = np.array([])
    for j, time in enumerate(neuron):
      if time == 1:
        times = np.append(times, ((j+1) * 10)/1000)
      elif time == 2:
        times = np.append(times, [((j+1) * 10)/1000, ((j+1) * 10)/1000-0.005])
      elif time == 3:
        times = np.append(times, [((j+1) * 10)/1000, ((j+1) * 10)/1000-0.003, ((j+1) * 10)/1000-0.006])
      elif time == 4:
        times = np.append(times, [((j+1) * 10)/1000, ((j+1) * 10)/1000-0.0025, ((j+1) * 10)/1000-0.005, ((j+1) * 10)/1000-0.0075])
    spiketimes[i] = np.pad(times, (0, 300 - len(times)))
  spiketimes = np.array([np.trim_zeros(train) for train in spiketimes])

  plt.eventplot(spiketimes, color=".2")
  plt.xlabel("Time (s)")
  plt.ylabel(f"{len(trail)} neurons")
  plt.yticks([]);
  plt.savefig("raster_plot.png")
plot_raster(42)



def spikes_to_spike_times(spikes):
  '''
  Converts a binary array of spikes into an array of spike timepoints

  Input: N x T array of binary spikes, either 1 or 0, for N neurons over T time steps
  Returns: N x n array of precise times at which the n spikes occurred
  '''

  spike_times = []

  for neuron in spikes:
    spike_times_neuron = []
    for idx, spike in enumerate(neuron):
        if spike == 1:
          spike_times_neuron.append(idx)

    spike_times.append(spike_times_neuron)

  spike_times = np.array([np.array(xi) for xi in spike_times])

  return spike_times

spikes = dat['spks'][:, 0, :]
spike_times = spikes_to_spike_times(spikes)
