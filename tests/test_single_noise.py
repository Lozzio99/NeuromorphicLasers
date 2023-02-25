import glob
from math import log

import v1.noise_laser as ls
from res import params
from res.params import default_laser_params, A, a
from res.params import noise_off_initial_condition as off
from res.params import noise_alternate_initial_condition as alternate
from res.params import noise_on_initial_condition as on
from res.solvers import solve_t, euler_mayurama
from res.visual import plot_solution


global make_gif
global phase_space


def test_laser(s0, d, fixed_point, tit):
    test = ls.single_node_noise_laser(s0, d, default_laser_params)  # initialise laser
    ts, traj = solve_t(params.t0, params.tf, params.dt, test, euler_mayurama)  # create solution trajectory
    plot_solution(ts, traj, fixed_point, title=tit, phase_space=phase_space, makegif=make_gif)  # plot
    #   print_solution(ts, traj)                                         # print


def laser_off():
    s_off = [off["e0"], off["y0"], off["w0"]]
    d_off = off["d"]  # pump current
    fixed_point = [0, d_off, 0, d_off]
    test_laser(s_off, d_off, fixed_point, f"noise_off_{params.sigma}")


def laser_alternate():
    s_alternate = [alternate["e0"], alternate["y0"], alternate["w0"]]
    d_alternate = alternate["d"]  # pump current
    fixed_point = [0, 1, -A * log(1 + a * (d_alternate - 1)), d_alternate]
    test_laser(s_alternate, d_alternate, fixed_point, f"noise_alternate_{params.sigma}")


def laser_on():
    s_on = [on["e0"], on["y0"], on["w0"]]  # initial condition
    d_on = on["d"]  # pump current
    fixed_point = [d_on - 1, 1, -A * log(1 + a * (d_on - 1)), d_on]
    test_laser(s_on, d_on, fixed_point, f"noise_on_{params.sigma}")


def run_tests(phasespace=False, makegif=False):
    globals().__setitem__('make_gif', makegif)
    globals().__setitem__('phase_space', phasespace)
    laser_off()
    laser_alternate()
    laser_on()
