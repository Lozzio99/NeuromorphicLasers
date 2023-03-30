from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt

from res import params
from res.solvers import solve_population_until_spike, euler_mayurama
from versions.laser_population import laser_array as ls


def run_test(test, pms, r):

    fig, ax = plt.subplots(1, 2)

    for i in range(len(pms)):
        p = np.arange(r[i][0], r[i][1], 1e-4)
        test(pms[i], p, ax)

    # set limits, labels, legend and titles
    ax[0].set_ylim([-0.1, 1.1])
    ax[0].set_xlabel('p'), ax[0].set_ylabel('Response rate %')
    ax[0].set_title('response rate'), ax[0].legend()

    ax[1].set_xlabel('p'), ax[1].set_ylabel(r'avg response time (t $\cdot$ dt)')
    ax[1].set_title('Average response time'), ax[1].legend()

    plt.tight_layout()
    plt.show()


def test_alpha(alpha, p, ax):
    args['a'] = alpha
    print(f' -> a : {alpha}')

    # initialise value holders
    average_response_time = []
    response_rate = []

    # for all pulse strength values
    for pulse_strength in p:
        args['p'] = pulse_strength
        print(f' -> p : {pulse_strength}')

        # init sum response time , response rate
        sum_response_time = 0
        response_sum = 0

        # until number of pulses is tested
        for ps in range(n_pulses):
            # if ps % 100 == 0:
            #    print(f'pulses {ps}/{n_pulses}')
            # initialise laser
            laser = ls([args['d']], args)
            # gather response time if any response with threshold (x >= 1)
            response_time, response = solve_population_until_spike(params.t0,
                                                                   params.tf, params.dt, laser, euler_mayurama, 1)
            # add test instances values to sum
            sum_response_time += response_time
            response_sum += response

        # average sum response time , response rate over n pulses
        average_response_time.append(sum_response_time / n_pulses)
        response_rate.append(response_sum / n_pulses)

    ax[0].plot(p, response_rate, label=r'$\alpha = $' + f'{alpha}')
    ax[1].plot(p, average_response_time, label=r'$\alpha = $' + f'{alpha}')

    return response_rate, average_response_time


def test_n_lasers(n, p, ax):
    print(f' -> n : {n}')

    # initialise value holders
    average_response_time = []
    response_rate = []

    # for all pulse strength values
    for pulse_strength in p:
        args['p'] = pulse_strength
        print(f' -> p : {pulse_strength}')

        # init sum response time , response rate
        sum_response_time = 0
        response_sum = 0

        # until number of pulses is tested
        for ps in range(n_pulses):
            # if ps % 100 == 0:
            #    print(f'pulses {ps}/{n_pulses}')
            # initialise laser
            deltas = [args['d'] for _ in range(n)]
            # print(deltas)
            # deltas = np.random.normal(args['d'], 0.05, n)
            laser = ls(deltas, args)
            # gather response time if any response with threshold (x >= 1)
            response_time, response = solve_population_until_spike(params.t0,
                                                                   params.tf, params.dt, laser, euler_mayurama, 1)
            # add test instances values to sum
            sum_response_time += response_time
            response_sum += response

        # average sum response time , response rate over n pulses
        average_response_time.append(sum_response_time / n_pulses)
        response_rate.append(response_sum / n_pulses)

    ax[0].plot(p, response_rate, label=f'{n} {"laser" if n == 1 else "lasers"}')
    ax[1].plot(p, average_response_time, label=f'{n} {"laser" if n == 1 else "lasers"}')

    return response_rate, average_response_time


#
#
#
#
#
#

params.tf = 5e3
args = params.default_laser_params
args['d'] = 0.995
args['s'] = 0.001
args['t'] = [0, 1e3]

n_pulses = 100
pa = [
    [0, 0.01],
    [0, 0.006],
    [0, 0.004],
    [0, 0.002]
]

pn = [
    [0.0050, 0.0150],
    [0.0025, 0.0100],
    [0.0000, 0.0075],
    [0.0000, 0.0050]
]


# pn2 = [
#    [0.0045, 0.0055],
#    [0.0045, 0.0055],
#    [0.0045, 0.0055],
#    [0.0045, 0.0055]
# ]


st = datetime.now()

# run_test(test_alpha, [2, 4, 10, 40], pa)  # 5h11
run_test(test_n_lasers, [1, 2, 5, 20], pn)  # 6h30

print('Duration: {}'.format(datetime.now() - st))
