from datetime import datetime
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from res import params
from res.solvers import solve_until_individual_spikes, euler_mayurama
from versions.masked_population import masked_array


def run_tests(d1, d2):
    print(f"d1: {d1:.2f}, d2: {d2:.2f}")
    for mask in masks:
        print(f"MASK : {mask}")
        plt.figure()
        fig, ax = plt.subplots(1, 2)

        test_pulse_masked(d1, d2, mask, ax)

        # set limits, labels, legend and titles
        ax[0].set_ylim([-0.1, 1.1])
        ax[0].set_xlabel('p'), ax[0].set_ylabel('Response rate %')
        ax[0].set_title('Response rate'), ax[0].legend()

        ax[1].set_xlabel('p'), ax[1].set_ylabel(r'avg response time (t $\cdot$ dt)')
        ax[1].set_title('Average response time'), ax[1].legend()

        plt.suptitle(f"mask {mask}")
        plt.tight_layout()
        output_file = Path(f"../imgs/xor/d[{d1:.2f},{d2:.2f}]/m{mask}.png")
        output_file.parent.mkdir(exist_ok=True, parents=True)
        plt.savefig(output_file)
        plt.show()


def test_pulse_masked(d1, d2, mask, ax):
    laser = masked_array([d1, d2], mask)

    # initialise value holders
    average_response_time1 = []
    average_response_time2 = []
    response_rate1 = []
    response_rate2 = []

    # for all pulse strength values
    for i, pulse_strength in enumerate(p_range):
        params.p = pulse_strength
        print(f' -> p : {pulse_strength}')
        sum_response_time1 = 0
        sum_response_time2 = 0
        sum_response1 = 0
        sum_response2 = 0

        for ps in range(n_pulses):
            laser.state0()
            response_time, response = solve_until_individual_spikes(
                params.t0,
                params.tf,
                params.dt,
                laser=laser,
                method=euler_mayurama,
                spike_thresh=[1, 1]
            )

            sum_response_time1 += response_time[0]
            sum_response_time2 += response_time[1]
            sum_response1 += response[0]
            sum_response2 += response[1]

        average_response_time1.append(sum_response_time1 / n_pulses)
        average_response_time2.append(sum_response_time2 / n_pulses)
        response_rate1.append(sum_response1 / n_pulses)
        response_rate2.append(sum_response2 / n_pulses)

    ax[0].plot(p_range, response_rate1, label=r'$\delta_1 :$' + f"{d1:.2f}")
    ax[0].plot(p_range, response_rate2, '--', label=r'$\delta_2 :$' + f"{d2:.2f}")
    ax[1].plot(p_range, average_response_time1, label=r'$\delta_1 :$' + f"{d1:.2f}")
    ax[1].plot(p_range, average_response_time2, '--', label=r'$\delta_2 :$' + f"{d2:.2f}")


params.tf = 2e3
d1_range = np.arange(0.45, 0.5, 0.1)
d2_range = np.arange(0.95, 1.0, 0.1)
print(d1_range, d2_range)
n_pulses = 25
params.t_range = [0, 500]
p_range = np.arange(0, 0.4, 0.001)

masks = [
    # [0.5, 0.5],
    # [1, 0],
    [0, 1]
]

for delta1 in d1_range:
    for delta2 in d2_range:
        if (delta1 != delta2) and (delta1 < delta2):
            st = datetime.now()
            run_tests(delta1, delta2)
            print('Duration: {}'.format(datetime.now() - st))

#
