import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
from mnist import MNIST
import math


def test(g_A=0.8, g_B=1, g_L=0.1, g_D=1.0, gsom=0.8):

    runtime = 6000

    data = MNIST('./datasets')

    images, labels = data.load_training()

    refresh_rate = 10

    n_images = int(math.ceil(runtime / (refresh_rate + 1))) + 1

    p.setup(timestep=1)

    # Weights
    exc_apical_weight = 1
    inh_apical_weight = 0.25
    basal_weight = 0.125
    sst_dend_weight = 0.5
    sst_soma_weight = 0

    #learning rates
    lPP32 = 0.01
    lPP21 = 0.0333
    lPP10 = 0.1111
    lIP22 = 0.02
    lIP11 = 0.0667
    # Not indicated in the paper
    lPI22 = 0.04
    lPI11 = 0.1111

    top_down = p.Population(10, p.RateLiveTeacher(10, refresh_rate, labels[:n_images], partitions=1),
                            label='top_down_input')

    source = p.Population(784, p.RateSourceLive(784, refresh_rate, images[:n_images], partitions=7), label='input_source')


    pyramidalL1 = p.Population(500, p.extra_models.PyramidalRate(g_A=g_A, g_B=g_B, g_L=g_L),
        label='pyramidalL1', in_partitions=[3, 7, 4, 0], out_partitions=7)
    interneuronL1 = p.Population(500, p.extra_models.IFExpRateTwoComp(g_L=g_L, g_D=g_D, g_som=gsom),
        label='interneuronL1', in_partitions=[3, 7, 0, 0], out_partitions=4)
    pyramidalL2 = p.Population(500, p.extra_models.PyramidalRate(g_A=g_A, g_B=g_B, g_L=g_L),
        label='pyramidalL2', in_partitions=[1, 7, 1, 0], out_partitions=3)
    interneuronL2 = p.Population(10, p.extra_models.IFExpRateTwoComp(g_L=g_L, g_D=g_D, g_som=gsom),
        label='interneuronL2', in_partitions=[1, 3, 0, 0], out_partitions=1)
    output_neurons = p.Population(10, p.extra_models.IFExpRateTwoComp(g_L=g_L, g_D=g_D, g_som=gsom),
        label='top_down_neurons', in_partitions=[1, 3, 0, 0], out_partitions=1)

    basal_plasticityL1 = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependencePyramidal(w_min=-100, w_max=100,
                                                                   learning_rates=(lPP10, 0, 0, 0)),
        weight=basal_weight)

    apical_plasticityL1 = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependencePyramidal(w_min=-100, w_max=100,
                                                                   learning_rates=(lPI11, 0, 0, 0)),
        weight=inh_apical_weight)

    sst_plasticityL1 = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependenceMultiplicativeMulticompBern(w_min=-100, w_max=100,
                                                                                     learning_rate=lIP11),
        weight=sst_dend_weight)

    basal_plasticityL2 = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependencePyramidal(w_min=-100, w_max=100,
                                                                   learning_rates=(lPP21, 0, 0, 0)),
        weight=basal_weight)

    apical_plasticityL2 = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependencePyramidal(w_min=-100, w_max=100,
                                                                   learning_rates=(lPI22, 0, 0, 0)),
        weight=inh_apical_weight)

    sst_plasticityL2 = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependenceMultiplicativeMulticompBern(w_min=-100, w_max=100,
                                                                                     learning_rate=lIP22),
        weight=sst_dend_weight)

    basal_plasticityOUT = p.STDPMechanism(
        timing_dependence=p.extra_models.TimingDependenceMulticompBern(),
        weight_dependence=p.extra_models.WeightDependenceMultiplicativeMulticompBern(w_min=-100, w_max=100,
                                                                                     learning_rate=lPP32),
        weight=basal_weight)

    # LAYER 1
    p.Projection(source, pyramidalL1, p.AllToAllConnector(), synapse_type=basal_plasticityL1,
                 receptor_type="basal_exc")

    p.Projection(pyramidalL1, interneuronL1, p.AllToAllConnector(), synapse_type=sst_plasticityL1,
                 receptor_type='dendrite_exc')

    p.Projection(interneuronL1, pyramidalL1, p.AllToAllConnector(), synapse_type=apical_plasticityL1,
                 receptor_type="apical_inh")

    p.Projection(pyramidalL2, pyramidalL1, p.AllToAllConnector(), p.StaticSynapse(weight=exc_apical_weight),
                 receptor_type="apical_exc")

    p.Projection(pyramidalL2, interneuronL1, p.OneToOneConnector(), p.StaticSynapse(weight=sst_soma_weight),
                 receptor_type='soma_exc')

    # LAYER 2
    p.Projection(pyramidalL1, pyramidalL2, p.AllToAllConnector(), synapse_type=basal_plasticityL2,
                 receptor_type='basal_exc')

    p.Projection(pyramidalL2, interneuronL2, p.AllToAllConnector(), synapse_type=sst_plasticityL2,
                 receptor_type='dendrite_exc')

    p.Projection(interneuronL2, pyramidalL2, p.AllToAllConnector(), synapse_type=apical_plasticityL2,
                 receptor_type="apical_inh")

    p.Projection(output_neurons, pyramidalL2, p.AllToAllConnector(), p.StaticSynapse(weight=exc_apical_weight),
                 receptor_type="apical_exc")

    p.Projection(output_neurons, interneuronL2, p.OneToOneConnector(), p.StaticSynapse(weight=sst_soma_weight),
                 receptor_type='soma_exc')


    # OUTPUT LAYER
    p.Projection(pyramidalL2, output_neurons, p.AllToAllConnector(), synapse_type=basal_plasticityOUT,
                 receptor_type='dendrite_exc')

    p.Projection(top_down, output_neurons, p.OneToOneConnector(), p.StaticSynapse(weight=sst_soma_weight),
                 receptor_type='soma_exc')

    output_neurons.record(['v', 'gsyn_exc', 'gsyn_inh'])

    p.run(runtime)

    u = output_neurons.get_data('v').segments[0].filter(name='v')[0]

    v = output_neurons.get_data('gsyn_exc').segments[0].filter(name='gsyn_exc')[0]

    out_rate = output_neurons.get_data('gsyn_inh').segments[0].filter(name='gsyn_inh')[0]


    # Plot values from SpiNNaker
    Figure(
        # membrane potential of the postsynaptic neuron
        Panel(u, ylabel="somatic potential",
              data_labels=[output_neurons.label], yticks=True, xlim=(0, runtime)),
        Panel(v, ylabel="dendritic potential",
              data_labels=[output_neurons.label], yticks=True, xlim=(0, runtime)),
        Panel(out_rate, ylabel="Output_rate",
              data_labels=[output_neurons.label], yticks=True, xlim=(0, runtime)),
        title="MNIST output",
        annotations="Simulated with {}".format(p.name())
    )

    plt.grid(True)

    plt.show()

    p.end()

    return True


def success_desc():
    return "MNIST microcircuit test PASSED"


def failure_desc():
    return "MNIST microcircuit test FAILED"


if __name__ == "__main__":

    if test():
        print(success_desc())
    else:
        print(failure_desc())
