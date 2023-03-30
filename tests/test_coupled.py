from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt

from res import params
from res.params import default_laser_params as pms
from res.solvers import euler_mayurama, solve_population
# from versions.fast.laser_population_fast import coupled_arrays
from versions.coupled_populations import coupled_arrays


def plot(laser, _ts, t1, t2, deltas1, deltas2):
    fig, ax = plt.subplots(2, 2, figsize=(16, 9), dpi=300)
    ms1 = [t1[i, :, 0].sum() / laser.p1.n_iris for i in range(t1.shape[0])]
    ms2 = [t2[i, :, 0].sum() / laser.p2.n_iris for i in range(t2.shape[0])]
    s1 = [t1[i, :, 0].sum() for i in range(t1.shape[0])]
    s2 = [t2[i, :, 0].sum() for i in range(t2.shape[0])]

    ax[0][0].plot(_ts, s1 if params.method == 'sum' else ms1, 'r'), ax[0][0].set_title(f'{params.method} intensity p1')
    ax[0][0].set_ylabel("X1"), ax[0][0].set_xlabel("t")

    ax[1][0].plot(_ts, s2 if params.method == 'sum' else ms2, 'r'), ax[1][0].set_title(f'{params.method} intensity p2')
    ax[1][0].set_ylabel("X2"), ax[1][0].set_xlabel("t")

    n1 = t1.shape[1]
    for i in range(n1):
        laser_x = t1[:, i, 0]
        ax[0][1].plot(_ts, laser_x, label=fr"$\delta_{i}=${deltas1[i]:.4f}")
        ax[0][1].set_title('Individual lasers intensity p1')
        ax[0][1].set_ylabel(r'$X_{1,i}$'), ax[0][1].set_xlabel('t')

    n2 = t2.shape[1]
    for i in range(n2):
        laser_x = t2[:, i, 0]
        ax[1][1].plot(_ts, laser_x, label=fr"$\delta_{i}=${deltas2[i]:.4f}")
        ax[1][1].set_title('Individual lasers intensity p2')
        ax[1][1].set_ylabel(r'$X_{2,i}$'), ax[1][1].set_xlabel('t')

    if n1 < 5:
        ax[0][1].legend()

    if n2 < 5:
        ax[1][1].legend()

    plt.tight_layout()
    plt.show()


def test_coupled():
    params.tf = 5e3
    pms['p'] = 0.01
    pms['t'] = [0, 1000]
    pms['c'] = 0.1
    params.method = 'mean_sum'
    params.method = 'sum'

    d1 = np.random.normal(0.999, 0.0001, size=10)
    d2 = np.random.normal(0.200, 0.0001, size=1)

    st = datetime.now()
    coupled = coupled_arrays(d1, d2, pms)
    # coupled = coupled_arrays(d1, d2)

    ts = np.arange(params.t0, params.tf, params.dt)

    traj = solve_population(ts, coupled, euler_mayurama)

    traj1 = traj[:, :coupled.p1.n_iris, :]
    traj2 = traj[:, coupled.p1.n_iris:traj.shape[1], :]

    plot(coupled, ts, traj1, traj2, d1, d2)
    print('Duration: {}'.format(datetime.now() - st))


test_coupled()
