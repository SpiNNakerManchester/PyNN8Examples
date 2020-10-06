import numpy as np

number_of_cues = 1
cycle_time = (number_of_cues * 150) + 1000 + 150
num_repeats = 2000
learning_threshold = 0.9

reg_rate = 0.000
p_connect_in = 1.
p_connect_rec = 1.
p_connect_out = 1.
recurrent_connections = False
synapse_eta = 0.03
tau_a = 3500  # [cycle_time - 150 + (np.random.randn() * 200) for i in range(100)]
input_split = 100
window_cycles = 2
window_size = cycle_time * window_cycles
threshold_beta = 3

max_weight = 8.0
in_weight = 0.55
prompt_weight = 0.55
rec_weight = 0  # -0.5
out_weight = 0  # 0.01
weight_string = "i{}-p{}-r{}-o{}".format(in_weight, prompt_weight, rec_weight, out_weight)
free_label = 't35'

input_size = 40
readout_neuron_params = {
    "v": 0,
    "v_thresh": 30,  # controls firing rate of error neurons
    "poisson_pop_size": input_size / 4,
    "rate_on": 100,
    "rate_off": 0,
    # "tau_m": tau_a,
    "w_fb": [1, -1, 0],
    "eta": synapse_eta * 10.,
    "window_size": window_size,
    "number_of_cues": number_of_cues
}
rates = []
for i in range(input_size):
    if i >= (3 * input_size) / 4:
        rates.append(10)
    else:
        rates.append(0)

neuron_pop_size = 4 * 25
# from_list_in, from_list_rec, from_list_out = load_connections('good 1 cue 20n recT', neuron_pop_size)

ratio_of_LIF = 0.5
beta = []
for i in range(neuron_pop_size):
    if i < neuron_pop_size / 2:
        # if i % 2 == 0:
        beta.append(threshold_beta)
    else:
        beta.append(threshold_beta)
neuron_params = {
    "v": 0,
    "i_offset": 0,
    "v_rest": 0,
    # "w_fb": [np.random.random() for i in range(neuron_pop_size)], # best it seems
    # "w_fb": [(np.random.random() * 2) - 1. for i in range(neuron_pop_size)],
    # "w_fb": [4*np.random.random() - 4*np.random.random() for i in range(neuron_pop_size)],  ## for both feedback weights
    # "w_fb": [-3]*(neuron_pop_size/2) + [3]*(neuron_pop_size/2),
    "w_fb": [3] * int(neuron_pop_size / 4) + [-3] * int(neuron_pop_size / 4) + [3] * int(neuron_pop_size / 4) + [
        -3] * int(neuron_pop_size / 4),
    # "B": 0.0,
    "beta": beta,
    "target_rate": 10,
    "tau_a": tau_a,
    "eta": synapse_eta * 5,  # / 20.,
    "window_size": window_size,
    "number_of_cues": number_of_cues
}