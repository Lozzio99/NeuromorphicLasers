import versions.pulse_laser as ls
from res import params
from res.analysis import analyse_solution
from res.solvers import solve_t, euler_mayurama
from res.visual import plot_solution

global make_gif
global phase_space


def test_laser(s0, laser_params, fixed_point, tit):
    test = ls.single_node_pulse_laser(s0, laser_params)  # initialise laser
    ts, traj = solve_t(params.t0, params.tf, params.dt, test, euler_mayurama)  # create solution trajectory
    plot_solution(ts, traj, fixed_point, title=tit, phase_space=phase_space, makegif=make_gif)  # plot
    analyse_solution(ts, traj)
    #   print_solution(ts, traj)                                         # print


def laser_off(args):
    laser_params = params.default_laser_params

    laser_params["a"] = args["a"]
    laser_params["p"] = args["p"]
    laser_params["t"] = args["t"]
    laser_params["d"] = args["d"]
    laser_params["s"] = args["s"]

    s_off = [laser_params["e0"], params.d_off, laser_params["w0"]]
    fixed_point = [0, params.d_off, 0, params.d_off]
    test_laser(s_off, laser_params, fixed_point, f"pulse_a{args['a']}_p{args['p']}")

