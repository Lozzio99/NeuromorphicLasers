import numpy as np
from matplotlib import pyplot as plt

from res import params
from res.solvers import solve_population, euler_mayurama
from versions.masked_population import masked_array


def plot(test, _ts, _traj, d):
    fig, (ax0, ax1) = plt.subplots(1, 2, dpi=300)
    mean_sum = np.sum(_traj[:, :, 0], axis=1) / test.n_iris
    _sumX = np.sum(_traj[:, :, 0], axis=1)
    ax0.plot(_ts, _sumX if params.method == 'sum' else mean_sum, 'r', label="X(t)")
    ax0.set_title(params.method)
    ax0.set_ylabel("X"), ax0.set_xlabel("t")
    n = _traj.shape[1]

    for i in range(n):
        ax1.plot(_ts, _traj[:, i, 0], label=f"delta{d[i]:.4f}")
        ax1.set_title('Individual lasers intensity')
        ax1.set_ylabel(r"$X_{i}$"), ax1.set_xlabel('t')

    if n <= 5:
        ax1.legend()

    plt.tight_layout()
    plt.suptitle(f"pulse {params.p}")
    plt.show()


def test_population(mask):
    test = masked_array(deltas, mask)  # initialise laser
    traj = solve_population(ts, test, euler_mayurama)  # create solution trajectory
    plot(test, ts, traj, deltas)


params.tf = 2000
params.p = 0.5
params.t_range = [0, 500]
ts = np.arange(params.t0, params.tf, params.dt)
deltas = [0.45, 0.95]
params.method = "mean_sum"

mask_00 = [0.5, 0.5]
mask_01 = [1, 0]
mask_10 = [0, 1]
mask_11 = [0.5, 0.5]

test_population(mask_00)
test_population(mask_01)
test_population(mask_10)
test_population(mask_11)
