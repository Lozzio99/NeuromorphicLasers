from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt, cm

from res import params, solvers
from res.solvers import euler_mayurama
from versions.laser_population_fast import laser_array


def run_test_3D():
    pulse_strength = np.arange(0.0001, 0.1, 0.005)
    pulse_length = np.arange(1, 500, 25)
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax0 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1 = fig.add_subplot(1, 2, 2, projection='3d')

    if len(pulse_length) < len(pulse_strength):
        pulse_strength = pulse_strength[:len(pulse_length)]
    if len(pulse_strength) < len(pulse_length):
        pulse_length = pulse_length[:len(pulse_strength)]

    pulse_strength, pulse_length = np.meshgrid(pulse_strength, pulse_length)
    print(f'{pulse_strength}, {pulse_strength.shape}', f'\n{pulse_length}, {pulse_length.shape}')

    @np.vectorize
    def test_avg_response(strength, length):
        print(f'strength:{strength:.4f}, length:{length:.4f}')
        params.p = strength
        params.t_range = [0, length]
        # laser = laser_array([0.995], params.default_laser_params())
        laser = laser_array([0.995])
        sum_response = 0
        sum_response_time = 0

        for p in range(n_pulses):
            laser.s = laser.s0
            response_time, response = solvers.solve_population_until_spike(params.t0, params.tf, params.dt, laser=laser,
                                                                           method=euler_mayurama, spike_thresh=1)
            sum_response += response
            sum_response_time += response_time

        avg_response_rate = sum_response / n_pulses
        avg_response_time = sum_response_time / n_pulses
        return avg_response_rate, avg_response_time

    response_rate, average_response_time = test_avg_response(pulse_strength, pulse_length)

    print(f'z1:{response_rate}')
    print(f'z2:{average_response_time}')

    ax0.plot_wireframe(pulse_strength, pulse_length, response_rate, lw=0.5, rstride=1, cstride=1, )

    surf = ax1.plot_surface(pulse_strength, pulse_length, average_response_time, cmap=cm.coolwarm, rstride=1, cstride=1,
                            alpha=0.6)

    fig.colorbar(surf, extend="max", location="bottom")

    #
    ax0.set_zlim([0, 1])
    ax0.set_xlabel('p strength'), ax0.set_ylabel('p length'), ax0.set_zlabel('Response rate %')
    ax0.set_title('response rate')

    #
    ax1.set_xlabel('strength'), ax1.set_ylabel('p length'), ax1.set_zlabel(r'avg response time (t $\cdot$ dt)')
    ax1.set_title('Average response time')

    ax1.view_init(20, -20)
    ax0.view_init(20, -70)
    plt.tight_layout()
    plt.savefig('pulse_response1.png')
    plt.show()


params.tf = 2e3
params.method = 'sum'
n_pulses = 200

d1 = 0.925

st = datetime.now()
run_test_3D()
print('Duration: {}'.format(datetime.now() - st))
