import numpy as np
from matplotlib import pyplot as plt

import versions.laser_population as ls
from res import params
from res.solvers import solve_population, euler_mayurama
from versions import laser_population


def test_population():
    params.tf = 2e3
    params.sigma = 0.001
    params.p = 0.1
    params.a = 2
    params.t_range = [0, 20]
    params.method = 'sum'
    deltas = [0.995]
    # print(deltas)
    test = ls.laser_array(deltas, params.default_laser_params())  # initialise laser
    ts = np.arange(params.t0, params.tf, params.dt)
    traj = solve_population(ts, test, euler_mayurama)  # create solution trajectory
    plot(test, ts, traj, deltas)


def plot(test, _ts, _traj, d):
    fig, (ax0, ax1) = plt.subplots(1, 2, dpi=300)
    mean_sum = np.sum(_traj[:, :, 0], axis=1) / test.n_iris
    _sum = np.sum(_traj[:, :, 0], axis=1)
    ax0.plot(_ts, _sum if params.method == 'sum' else mean_sum, 'r')
    ax0.set_title(params.method)
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
