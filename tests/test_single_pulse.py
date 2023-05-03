import versions.pulse_laser as ls
from res import params
from res.solvers import solve_t, euler_mayurama
from res.visual import plot_solution

global make_gif
global phase_space

laser_params = params.default_laser_params_OFF()
laser_params["p"] = 0.1
laser_params["t"] = [[0, 200], [5e4, 5.02e4]]


def test_laser(s0, fixed_point, tit, fn):
    test = ls.single_node_pulse_laser(s0, laser_params)  # initialise laser
    ts, traj = solve_t(params.t0, params.tf, params.dt, test, euler_mayurama)  # create solution trajectory
    plot_solution(ts, traj, fixed_point, title=tit, file_name=fn, phase_space=phase_space, makegif=make_gif)  # plot
    #   analyse_solution(ts, traj)
    #   print_solution(ts, traj)                                         # print


def laser_off():
    s_off = [laser_params["e0"], params.d_off, laser_params["w0"]]
    fixed_point = [0, params.d_off, 0, params.d_off]
    test_laser(s_off, fixed_point,  r"$pulse_{off}$" + f" :{params.d_off:.3f}", "pulse/p_off")


def run_tests(phasespace=True, makegif=True):
    globals().__setitem__('make_gif', makegif)
    globals().__setitem__('phase_space', phasespace)
    laser_off()


run_tests()
