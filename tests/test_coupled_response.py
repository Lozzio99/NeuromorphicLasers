from matplotlib import pyplot as plt
from numpy import arange
from numpy.random import normal

import res.params as args
from res.solvers import solve_coupled_until_spike, euler_mayurama
from versions.fast.laser_population_fast import coupled_arrays


def run_test(test, n, c):

    fig, ax = plt.subplots(1, 2)
    args.c = c
    for i in range(len(n)):
        test(n[i], ax)

    # set limits, labels, legend and titles
    ax[0].set_ylim([-0.1, 1.1])
    ax[0].set_xlabel(r'$\delta_2$'), ax[0].set_ylabel('Response rate %')
    ax[0].set_title('response rate'), ax[0].legend()

    ax[1].set_xlabel(r'$\delta_2$'), ax[1].set_ylabel(r'avg response time (t $\cdot$ dt)')
    ax[1].set_title('Average response time'), ax[1].legend()

    plt.tight_layout()
    plt.show()


def test_n(n, ax):
    print(f' -> n : {n}')

    # initialise value holders
    average_response_time = []
    response_rate = []

    # for all pulse strength values
    for delta in d2:
        print(f' -> d : {delta}')

        # init sum response time , response rate
        sum_response_time = 0
        response_sum = 0
        laser = coupled_arrays(normal(d1, 1e-4, n), [delta])

        # until number of pulses is tested
        for ps in range(n_pulses):
            # initialise laser
            laser.state0()
            # gather response time if any response with threshold (x >= 1)
            response_time, response = solve_coupled_until_spike(args.t0, args.tf, args.dt, laser, n, euler_mayurama, 1)
            # add test instances values to sum
            sum_response_time += response_time
            response_sum += response

        # average sum response time , response rate over n pulses
        average_response_time.append(sum_response_time / n_pulses)
        response_rate.append(response_sum / n_pulses)

    ax[0].plot(d2, response_rate, label=f'{n} lasers')
    ax[1].plot(d2, average_response_time, label=f'{n} lasers')

    return response_rate, average_response_time


args.tf = 5e3
args.p = 0.01
args.t_range = [0, 1000]
args.method = 'sum'

n_pulses = 1


d1 = [0.999]
d2 = arange(0.100, 1.000, 0.050)
n_lasers = [1, 2, 3, 5]
run_test(test_n, n_lasers, 0.1)


