# Copyright (c) 2017 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Simple test for neuromodulated STDP.
Two pre-synaptic spikes are added, at times 1500 and 2400ms.
Post-synaptic neuron is stimulated at 1502 and fires at time 1503ms.
Dendritic delay is 1ms so post-synaptic time is at 1504ms when processed in
STDP. Dopamine neuron spikes at 1600+1ms (Also added dendritic delay).
Calculating weight change in this scenario, according to equations in the
Izhikevich 2007 paper*, gives us the weight change of 10.0552710...
*https://www.ncbi.nlm.nih.gov/pubmed/17220510
Simulation from SpiNNaker gives us the weight change of 10.0654296875.
Some inaccuracy occurs due to precision loss in s5.11 fixed point format
used in STDP traces and exp LUTs. Also, due to long timing constants, exp
LUTs are discretized further by TAU_C_SHIFT and TAU_D_SHIFT to be able to
fit them into memory, adding another level of inaccuracy. Finally, some more
accuracy may be lost due to weight scaling.
"""

import pyNN.spiNNaker as sim

timestep = 1.0
duration = 3000

# Main parameters from Izhikevich 2007 STDP paper
t_pre = [1500, 2400]    # Pre-synaptic neuron times
t_post = [1502]         # Post-synaptic neuron stimuli time
t_dopamine = [1600]     # Dopaminergic neuron spike times
tau_c = 1000            # Eligibility trace decay time constant.
tau_d = 200             # Dopamine trace decay time constant.
DA_concentration = 0.1  # Dopamine trace step increase size

# Initial weight
rewarded_syn_weight = 0.0

cell_params = {
    'cm': 0.3,
    'i_offset': 0.0,
    'tau_m': 10.0,
    'tau_refrac': 4.0,
    'tau_syn_E': 1.0,
    'tau_syn_I': 1.0,
    'v_reset': -70.0,
    'v_rest': -65.0,
    'v_thresh': -55.4}

sim.setup(timestep=timestep)

pre_pop = sim.Population(1, sim.SpikeSourceArray, {
    'spike_times': t_pre})

# Create a population of dopaminergic neurons for reward
reward_pop = sim.Population(1, sim.SpikeSourceArray, {
    'spike_times': t_dopamine}, label='reward')

# Stimulus for post synaptic population
post_stim = sim.Population(1, sim.SpikeSourceArray, {
    'spike_times': t_post})

# Create post synaptic population which will be modulated by DA concentration.
post_pop = sim.Population(
    1, sim.IF_curr_exp, cell_params,
    label='post1')

# Stimulate post-synaptic neuron
sim.Projection(
    post_stim, post_pop,
    sim.AllToAllConnector(),
    synapse_type=sim.StaticSynapse(weight=6),
    receptor_type='excitatory')

# Create STDP dynamics
synapse_dynamics = sim.STDPMechanism(
    timing_dependence=sim.SpikePairRule(
        tau_plus=10, tau_minus=12,
        A_plus=1, A_minus=1),
    weight_dependence=sim.AdditiveWeightDependence(
        w_min=0, w_max=20),
    weight=0.0)

# Create a plastic connection between pre and post neurons
plastic_projection = sim.Projection(
    pre_pop, post_pop,
    sim.AllToAllConnector(),
    synapse_type=synapse_dynamics,
    receptor_type='excitatory', label='Pre-post projection')

# Create dopaminergic connection
reward_projection = sim.Projection(
    reward_pop, post_pop,
    sim.AllToAllConnector(),
    synapse_type=sim.extra_models.Neuromodulation(
        tau_c=1000, tau_d=200, weight=DA_concentration, w_max=20.0),
    receptor_type='reward', label='reward synapses')

sim.run(duration)

# End simulation on SpiNNaker
print("Final weight: " + repr(plastic_projection.get('weight', 'list')))

sim.end()
