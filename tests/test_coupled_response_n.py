from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt

from res import params
from res.solvers import solve_coupled_until_spike, euler_mayurama
from versions.laser_population_fast import coupled_arrays

params.p = 0.1
params.t_range = [0, 500]
params.tf = 1e3
params.method = 'mean_sum'

d1 = 0.995
d2 = 0.975
n_lasers = [1, 2, 5, 20]
n_pulses = 1000
p_range = np.arange(0.02, 0.08, 0.0025)


def run_test():
    fig, ax = plt.subplots(1, 2)

    for n in n_lasers:
        test_n_lasers(n, ax)

    # set limits, labels, legend and titles
    ax[0].set_ylim([-0.1, 1.1])
    ax[0].set_xlabel('p'), ax[0].set_ylabel('Response rate %')
    ax[0].set_title('Response rate'), ax[0].legend()

    ax[1].set_xlabel('p'), ax[1].set_ylabel(r'avg response time (t $\cdot$ dt)')
    ax[1].set_title('Average response time'), ax[1].legend()

    plt.tight_layout()
    plt.show()


def test_n_lasers(n, ax):
    print(f' -> n : {n}')
    deltas_p1 = np.random.normal(d1, 0.005, n)
    laser = coupled_arrays(deltas_p1, [d2])

    # initialise value holders
    average_response_time = []
    response_rate = []

    # for all pulse strength values
    for coupling_strength in p_range:
        params.c = coupling_strength
        print(f' -> c : {coupling_strength}')
        sum_response_time = 0
        response_sum = 0

        for ps in range(n_pulses):
            laser.state0()
            response_time, response = solve_coupled_until_spike(
                params.t0,
                params.tf,
                params.dt,
                laser=laser,
                n1=n,
                method=euler_mayurama,
                spike_thresh=1
            )
            sum_response_time += response_time
            response_sum += response

        average_response_time.append(sum_response_time / n_pulses)
        response_rate.append(response_sum / n_pulses)

    ax[0].plot(p_range, response_rate, label=f'{n} {"laser" if n == 1 else "lasers"}')
    ax[1].plot(p_range, average_response_time, label=f'{n} {"laser" if n == 1 else "lasers"}')

    return response_rate, average_response_time


st = datetime.now()
run_test()
print('Duration: {}'.format(datetime.now() - st))
