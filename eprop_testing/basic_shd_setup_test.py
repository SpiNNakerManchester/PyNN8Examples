import spynnaker8 as pynn
import numpy as np
import matplotlib.pyplot as plt
from eprop_testing.frozen_poisson import build_input_spike_train, frozen_poisson_variable_hz
from pyNN.random import NumpyRNG, RandomDistribution
from pyNN.utility.plotting import Figure, Panel
import tables
import pickle

def weight_distribution(pop_size):
    base_weight = np.random.randn() #/ np.sqrt(pop_size)
    # base_weight = 0
    return base_weight

def probability_connector(pre_pop_size, post_pop_size, prob, offset=0, base_weight=0.0):
    connections = []
    max_syn_per_neuron = 0
    for j in range(post_pop_size):
        neuron_syn_count = 0
        delay_count = offset
        for i in range(pre_pop_size):
            if np.random.random() < prob:
                neuron_syn_count += 1
                conn = [i, j, weight_distribution(pre_pop_size)+base_weight, delay_count]
                delay_count += 1
                connections.append(conn)
        if neuron_syn_count > max_syn_per_neuron:
            max_syn_per_neuron = neuron_syn_count
    return connections, max_syn_per_neuron

def shd_to_spike_array(file_name):
    spike_array = [[] for i in range(700)]
    data_labels = []
    h5data = tables.open_file(file_name, mode='r')
    units = h5data.root.spikes.units
    times = h5data.root.spikes.times
    labels = h5data.root.labels
    data_count = 0
    for idx, label in enumerate(labels):
        if label < 10:
            data_labels.append(label)
            spike_times = times[idx]
            neuron_idx = units[idx]
            for spike, unit in zip(spike_times, neuron_idx):
                spike_array[unit].append(spike+(cycle_time*data_count))
            data_count += 1
    return spike_array, data_labels


np.random.seed(272727)

cycle_time = 1000
num_repeats = 10 # 1
# pynn.setup(1.0)

# file_name = '/data/mbaxrap7/Heidelberg speech/shd_train.h5'
# print("formatting data")
# spike_times, labels = shd_to_spike_array(file_name)
# print("pickling")
# filename = "shd_training_english.pickle"
# outfile = open(filename, 'wb')
# pickle.dump([spike_times, labels], outfile)
# outfile.close()
infile = open("shd_training_english.pickle", 'rb')
spike_times, labels = pickle.load(infile)
infile.close()

reg_rate = 0.0000
p_connect_in = 1.
p_connect_rec = 1.
p_connect_out = 1.
recurrent_connections = False
synapse_eta = 0.001
base_weight = 0.35
output_size = 10

pynn.setup(timestep=1, max_delay=1000)


input_size = 700
readout_neuron_params = {
    "v": 0,
    "v_thresh": 30, # controls firing rate of error neurons
    "target_data": labels,
    "eta": 0.001, #synapse_eta + 0.0,
    "update_ready": cycle_time
    }
input_pop = pynn.Population(input_size,
                            pynn.SpikeSourceArray,
                            # {'spike_times': build_input_spike_train(num_repeats, cycle_time, input_size)},
                            # {'spike_times': frozen_poisson_variable_hz(num_repeats, cycle_time, input_split,
                            #                                            input_speed_up, input_size, use_old=False)},
                            {'spike_times': spike_times},

                            label='input_pop')

neuron_pop_size = 100
neuron_params = {
    "v": 0,
    "i_offset": 0,
    "v_rest": 0,
#     "w_fb": [[np.random.random() for j in range(output_size)] for i in range(neuron_pop_size)], # best it seems
    "w_fb": [RandomDistribution("uniform", low=0.0, high=1.0) for i in range(output_size)], # best it seems
    # "w_fb": [(np.random.random() * 2) - 1. for i in range(neuron_pop_size)],
    # "B": 0.0,
    "beta": 0.0,
    "target_rate": 70,#[10 + np.random.randn() for i in range(neuron_pop_size)],
    "eta": synapse_eta / 4.,
    "tau_err": 1000*1.,
    "window_size": cycle_time,
    "input_synapses": input_size,
    "rec_synapses": recurrent_connections * neuron_pop_size,
    "number_of_cues": 1
    }
if neuron_pop_size:
    neuron = pynn.Population(neuron_pop_size,
                             pynn.extra_models.EPropAdaptive(**neuron_params),
                             label='eprop_pop')

# Output population
readout_pop = pynn.Population(output_size, # HARDCODED 1
                       pynn.extra_models.SHDReadout(
                            **readout_neuron_params
                           ),
                       label="readout_pop"
                       )

eprop_learning_output = pynn.STDPMechanism(
    timing_dependence=pynn.extra_models.TimingDependenceEprop(),
    weight_dependence=pynn.extra_models.WeightDependenceEpropReg(
        w_min=-2, w_max=2, reg_rate=0.0))

if neuron_pop_size:
    start_w = [weight_distribution(neuron_pop_size*input_size) for i in range(input_size)]
    eprop_learning_neuron = pynn.STDPMechanism(
        timing_dependence=pynn.extra_models.TimingDependenceEprop(),
        weight_dependence=pynn.extra_models.WeightDependenceEpropReg(
            w_min=-2.0, w_max=2.0, reg_rate=reg_rate))

    from_list_in, max_syn_per_input = probability_connector(input_size, neuron_pop_size, p_connect_in, base_weight=base_weight)
    if max_syn_per_input > 100:
        Exception
    else:
        print("max number of synapses per neuron:", max_syn_per_input)
    in_proj = pynn.Projection(input_pop,
                              neuron,
                              pynn.FromListConnector(from_list_in),
                              synapse_type=eprop_learning_neuron,
                              label='input_connections',
                              receptor_type='input_connections')

    # from_list_out = [[i, 0, weight_distribution(input_size), i] for i in range(input_size)]
    from_list_out, max_syn_per_output = probability_connector(neuron_pop_size, 1, p_connect_out)
    if max_syn_per_output > 100:
        Exception
    else:
        print("max number of synapses per readout:", max_syn_per_output)
    out_proj = pynn.Projection(neuron,
                               readout_pop,
                               # pynn.OneToOneConnector(),
                               pynn.FromListConnector(from_list_out),
                               synapse_type=eprop_learning_output,
                               label='input_connections',
                               receptor_type='input_connections')

    learning_proj = pynn.Projection(readout_pop,
                                    neuron,
                                    # pynn.OneToOneConnector(),
                                    # pynn.StaticSynapse(weight=[0.5], delay=[0]),
                                    pynn.AllToAllConnector(),
                                    pynn.StaticSynapse(weight=0.5, delay=0),
                                    receptor_type='learning_signal')
else:
    from_list_out, max_syn_per_output = probability_connector(input_size, 1, p_connect_out, base_weight=base_weight)
    if max_syn_per_output > 100:
        Exception
    else:
        print("max number of synapses per readout:", max_syn_per_output)
    out_proj = pynn.Projection(input_pop,
                               readout_pop,
                               # pynn.OneToOneConnector(),
                               pynn.FromListConnector(from_list_out),
                               synapse_type=eprop_learning_output,
                               label='input_connections',
                               receptor_type='input_connections')

if recurrent_connections:
    eprop_learning_recurrent = pynn.STDPMechanism(
        timing_dependence=pynn.extra_models.TimingDependenceEprop(),
        weight_dependence=pynn.extra_models.WeightDependenceEpropReg(
            w_min=-2, w_max=2, reg_rate=reg_rate))

    from_list_rec, max_syn_per_rec = probability_connector(neuron_pop_size, neuron_pop_size, p_connect_rec, offset=0)
    if max_syn_per_rec > 150:
        Exception
    else:
        print("max number of synapses per neuron:", max_syn_per_rec)
    recurrent_proj = pynn.Projection(neuron,
                                     neuron,
                                     pynn.FromListConnector(from_list_rec),
                                     synapse_type=eprop_learning_recurrent,
                                     label='recurrent_connections',
                                     receptor_type='recurrent_connections')

input_pop.record('spikes')
if neuron_pop_size:
    neuron.record('all')
#     neuron.record('spikes')
#     neuron.record(['gsyn_exc', 'v', 'gsyn_inh'], indexes=[0, 1, 9, 17, 25, 33])
readout_pop.record('all')

# experiment_label = "eta:{}/{} - size:{}/{} - reg_rate:{} - p_conn:{}/{}/{} - rec:{} - 10*{}hz all2all".format(
#     readout_neuron_params["eta"], neuron_params["eta"], input_size, neuron_pop_size, reg_rate, p_connect_in, p_connect_rec, p_connect_out, recurrent_connections, input_split)
experiment_label = "english training"
print("\n", experiment_label, "\n")

runtime = cycle_time * num_repeats
pynn.run(runtime)
in_spikes = input_pop.get_data('spikes')
if neuron_pop_size:
    neuron_res = neuron.get_data('all')
readout_res = readout_pop.get_data(['v', 'gsyn_exc', 'gsyn_inh'])  # ('all')

total_error = 0.0
cycle_error = [0.0 for i in range(num_repeats)]
for cycle in range(num_repeats):
    for time_index in range(cycle_time):
        instantaneous_error = np.abs(float(
            readout_res.segments[0].filter(name='v')[0][time_index+(cycle*cycle_time)][0]))
        cycle_error[cycle] += instantaneous_error
        total_error += instantaneous_error

if neuron_pop_size:
    new_connections_in = []#in_proj.get('weight', 'delay').connections[0]#[]
    for partition in in_proj.get('weight', 'delay').connections:
        for conn in partition:
            new_connections_in.append(conn)
    new_connections_in.sort(key=lambda x:x[1])
    from_list_in.sort(key=lambda x:x[1])
    connection_diff_in = []
    for i in range(len(from_list_in)):
        connection_diff_in.append(new_connections_in[i][2] - from_list_in[i][2])
    print("Input connections\noriginal\n", np.array(from_list_in))
    print("new\n", np.array(new_connections_in))
    print("diff\n", np.array(connection_diff_in))

new_connections_out = []#out_proj.get('weight', 'delay').connections[0]#[]
for partition in out_proj.get('weight', 'delay').connections:
    for conn in partition:
        new_connections_out.append(conn)
new_connections_out.sort(key=lambda x:x[1])
from_list_out.sort(key=lambda x:x[1])
connection_diff_out = []
for i in range(len(from_list_out)):
    connection_diff_out.append(new_connections_out[i][2] - from_list_out[i][2])
print("Output connections\noriginal\n", np.array(from_list_out))
print("new\n", np.array(new_connections_out))
print("diff\n", np.array(connection_diff_out))

if recurrent_connections:
    new_connections_rec = []#out_proj.get('weight', 'delay').connections[0]#[]
    for partition in recurrent_proj.get('weight', 'delay').connections:
        for conn in partition:
            new_connections_rec.append(conn)
    new_connections_rec.sort(key=lambda x:x[1])
    from_list_rec.sort(key=lambda x:x[1])
    connection_diff_rec = []
    for i in range(len(from_list_out)):
        connection_diff_rec.append(new_connections_rec[i][2] - from_list_rec[i][2])
    print("Recurrent connections\noriginal\n", np.array(from_list_out))
    print("new\n", np.array(new_connections_out))
    print("diff\n", np.array(connection_diff_out))

pynn.end()
print("job done")

print(experiment_label)
print("cycle_error =", cycle_error)
print("total error =", total_error)
print("average error = ", np.average(cycle_error))
print("weighted average", np.average(cycle_error, weights=[i for i in range(num_repeats)]))
print("minimum error = ", np.min(cycle_error))
print("minimum iteration = ", cycle_error.index(np.min(cycle_error)), "- with time stamp =", cycle_error.index(np.min(cycle_error)) * 1024)


if neuron_pop_size:
    plt.figure()
    Figure(
        Panel(neuron_res.segments[0].filter(name='v')[0], ylabel='Membrane potential (mV)', yticks=True, xticks=True, xlim=(0, runtime)),

        Panel(neuron_res.segments[0].filter(name='gsyn_exc')[0], ylabel='gsyn_exc', yticks=True, xticks=True, xlim=(0, runtime)),

        Panel(neuron_res.segments[0].filter(name='gsyn_inh')[0], ylabel='gsyn_inh', yticks=True, xticks=True, xlim=(0, runtime)),

        Panel(in_spikes.segments[0].spiketrains, ylabel='in_spikes', xlabel='in_spikes', yticks=True, xticks=True, xlim=(runtime-cycle_time*3, runtime)),

        Panel(neuron_res.segments[0].spiketrains, ylabel='neuron_spikes', xlabel='neuron_spikes', yticks=True,
              xticks=True, xlim=(0, cycle_time * 3)),

        Panel(neuron_res.segments[0].spiketrains, ylabel='neuron_spikes', xlabel='neuron_spikes', yticks=True,
              xticks=True, xlim=(runtime - cycle_time * 3, runtime)),

        Panel(readout_res.segments[0].filter(name='v')[0], ylabel='Membrane potential (mV)', yticks=True, xticks=True, xlim=(runtime-cycle_time*3, runtime)),

        Panel(readout_res.segments[0].filter(name='gsyn_exc')[0], ylabel='gsyn_exc', yticks=True, xticks=True, xlim=(0, runtime)),

        Panel(readout_res.segments[0].filter(name='gsyn_inh')[0], ylabel='gsyn_inh', yticks=True, xticks=True, xlim=(0, runtime)),

        title="neuron data for {}".format(experiment_label)
    )
    plt.show()
else:
    plt.figure()
    Figure(
        Panel(in_spikes.segments[0].spiketrains, ylabel='in_spikes', xlabel='in_spikes', yticks=True, xticks=True, xlim=(runtime-cycle_time*3, runtime)),

        Panel(readout_res.segments[0].filter(name='v')[0], ylabel='Membrane potential (mV)', yticks=True, xticks=True,
              xlim=(runtime-cycle_time*3, runtime)),

        Panel(readout_res.segments[0].filter(name='gsyn_exc')[0], ylabel='gsyn_exc', yticks=True, xticks=True,
              xlim=(0, runtime)),

        Panel(readout_res.segments[0].filter(name='gsyn_inh')[0], ylabel='gsyn_inh', yticks=True, xticks=True,
              xlim=(0, runtime)),

        title="neuron data for {}".format(experiment_label)
    )
    plt.show()

plt.figure()
plt.scatter([i for i in range(num_repeats)], cycle_error)
plt.title(experiment_label)
plt.show()

# pynn.end()
# print("job done")

'''
plt.figure()
plt.scatter([i for i in range(num_repeats)], cycle_error)
plt.title(experiment_label)
plt.show()

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

v_mem = []
sine_wave = []
for timestep in readout_res.segments[0].filter(name='v')[0]:
    v_mem.append(timestep[0])
    sine_wave.append(timestep[1])

ave_mem = moving_average(v_mem, 20)
ave_sine = moving_average(sine_wave, 20)

plt.figure()
plt.plot([i for i in range(len(ave_mem))], cum_mem)
plt.plot([i for i in range(len(ave_sine))], cum_sine)
plt.title(experiment_label)
plt.show()
'''