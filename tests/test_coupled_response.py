from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from numpy.random import normal
import multiprocessing as mp
from res import params
from res.solvers import solve_coupled_until_spike, euler_mayurama
from versions.fast.laser_population_fast import coupled_arrays


def run_test(test, delta2, c):
    fig, ax = plt.subplots(1, 2)
    for i in range(len(delta2)):
        test(delta2[i], c, ax)

    # set limits, labels, legend and titles
    ax[0].set_ylim([-0.1, 1.1])
    ax[0].set_xlabel(r'c'), ax[0].set_ylabel('Response rate %')
    ax[0].set_title('response rate'), ax[0].legend()

    ax[1].set_xlabel(r'c'), ax[1].set_ylabel(r'avg response time (t $\cdot$ dt)')
    ax[1].set_title('Average response time'), ax[1].legend()

    plt.tight_layout()
    plt.show()


def test_delta(d, cr, ax):
    print(f' -> delta2 : {d}')

    # initialise value holders
    average_response_time = []
    response_rate = []

    # for all delta2 values
    for c in cr:
        print(f' -> c : {c}')
        params.c = c

        # init sum response time , response rate
        sum_response_time = 0
        response_sum = 0
        laser = coupled_arrays(normal(d1, 0.0001, size=5), [d])

        # until number of pulses is tested
        for p in range(n_pulses):
            # initialise laser
            laser.state0()
            # gather response time if any response with threshold (x >= 1)
            response_time, response = solve_coupled_until_spike(
                params.t0, params.tf, params.dt, laser, 5, euler_mayurama, 1
            )
            # add test instances values to sum
            sum_response_time += response_time
            response_sum += response

        # average sum response time , response rate over n pulses
        average_response_time.append(sum_response_time / n_pulses)
        response_rate.append(response_sum / n_pulses)

    ax[0].plot(cr, response_rate, label=fr"$\delta_2=${d:.4f}")
    ax[1].plot(cr, average_response_time, label=fr"$\delta_2=${d:.4f}")

    return response_rate, average_response_time


def run_test_3D(delta2, cr):
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax0 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1 = fig.add_subplot(1, 2, 2, projection='3d')

    if len(delta2) < len(cr):
        cr = cr[:len(delta2)]
    if len(cr) < len(delta2):
        delta2 = delta2[:len(cr)]

    c_range, delta2_range = np.meshgrid(cr, delta2)
    print(f'{c_range}', f'\n{delta2_range}')

    @np.vectorize
    def test_avg_response(coupling_strength, delta_2):
        print(f'd2:{delta_2:.4f}, c:{coupling_strength:.4f}')
        params.c = coupling_strength
        laser = coupled_arrays(normal(d1, 1e-5, size=n1), [delta_2])
        sum_response = 0
        sum_response_time = 0

        for p in range(n_pulses):
            laser.state0()
            response_time, response = solve_coupled_until_spike(params.t0, params.tf, params.dt, laser=laser,
                                                                n1=n1, method=euler_mayurama, spike_thresh=1)
            sum_response += response
            sum_response_time += response_time

        avg_response_rate = sum_response / n_pulses
        avg_response_time = sum_response_time / n_pulses
        return avg_response_rate, avg_response_time

    response_rate, average_response_time = test_avg_response(c_range, delta2_range)

    print(f'z1:{response_rate}')
    print(f'z2:{average_response_time}')

    ax0.plot_wireframe(c_range, delta2_range, response_rate, lw=0.5, rstride=1, cstride=1,)

    surf = ax1.plot_surface(c_range, delta2_range, average_response_time, cmap=cm.coolwarm, rstride=1, cstride=1,
                            alpha=0.6)

    fig.colorbar(surf, extend="max", location="bottom")

    #
    ax0.set_zlim([0, 1])
    ax0.set_xlabel('coupling'), ax0.set_ylabel(r'$\delta_2$'), ax0.set_zlabel('Response rate %')
    ax0.set_title('response rate')

    #
    ax1.set_xlabel('coupling'), ax1.set_ylabel(r'$\delta_2$'), ax1.set_zlabel(r'avg response time (t $\cdot$ dt)')
    ax1.set_title('Average response time')

    ax1.view_init(20, -20)
    ax0.view_init(20, -70)
    plt.tight_layout()
    plt.savefig('gifs/coupled_response.png')
    plt.show()


params.tf = 2e3
params.p = 0.1
n1 = 3
params.method = 'sum'

n_pulses = 100

d1 = 0.925
# expect same shape
d2 = np.arange(0., 1.1, 0.05)
c_ = np.arange(0.0, .11, 0.005)
st = datetime.now()
run_test_3D(d2, c_)
print('Duration: {}'.format(datetime.now() - st))
