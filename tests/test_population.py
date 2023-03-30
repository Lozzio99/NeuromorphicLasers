import numpy as np
from matplotlib import pyplot as plt

import versions.laser_population as ls
from res import params
from res.params import default_laser_params as pms
from res.solvers import solve_population, euler_mayurama
from versions import laser_population


def test_population():
    params.tf = 5e4
    pms['e0'] = 0
    pms['w0'] = 0
    pms['s'] = 1/(510 ** 2)
    pms['p'] = 0.01
    pms['a'] = 2
    pms['t'] = [0, 1000]
    deltas = [1.7, 1.5]
    # print(deltas)
    test = ls.laser_array(deltas, args=pms)  # initialise laser
    ts = np.arange(params.t0, params.tf, params.dt)
    traj = solve_population(ts, test, euler_mayurama)  # create solution trajectory
    plot(test, ts, traj, deltas)


def plot(test, _ts, _traj, d):
    fig, (ax0, ax1) = plt.subplots(1, 2, dpi=300)
    mean_sum = np.sum(_traj[:, :, 0], axis=1) / test.n_iris
    # mean_sum = _traj[:, :, 0]
    ax0.plot(_ts, mean_sum, 'r'), ax0.set_title(laser_population.method)
    ax0.set_ylabel("X"), ax0.set_xlabel("t")
    n = _traj.shape[1]

    for i in range(n):
        ax1.plot(_ts, _traj[:, i, 0], label=f"delta{d[i]}")
        ax1.set_title('Individual lasers intensity')
        ax1.set_ylabel(r"$X_{i}$"), ax1.set_xlabel('t')

    if n <= 5:
        ax1.legend()

    plt.tight_layout()
    plt.show()


test_population()
