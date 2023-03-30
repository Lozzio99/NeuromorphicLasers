from random import uniform

from res.params import dt, gamma
from res.solvers import solve_t, improved_euler
from res.visual import plot_solution, analyze


class laser:
    def __init__(self, s0, d):
        self.s = s0
        self.delta = d

    def xdot(self):
        x = self.s[0]
        y = self.s[1]
        return -x * (1 - y)

    def ydot(self):
        x = self.s[0]
        y = self.s[1]
        return gamma * (self.delta - y - (x * y))

    def apply(self, s=None):
        if s is not None:
            self.s = s
        return [self.xdot(), self.ydot()]


# test non-lasing fixed point : [x=0, y=d], stable for d<1
delta_off = 0.99995
initial_state = [uniform(0, 1), uniform(0, 1)]
ls = laser(initial_state, delta_off)
ts, traj = solve_t(0, 2500, dt, ls, improved_euler)
plot_solution(ts, traj, [0, delta_off], 'Non-lasing fp (stable)')
print(analyze(ts, traj))
#
#
#
#
#
delta_on = 1.5
initial_state = [uniform(0, 1), uniform(0, 1)]
ls = laser(initial_state, delta_on)
ts, traj = solve_t(0, 2500, dt, ls, improved_euler)
plot_solution(ts, traj, [delta_on-1, 1], 'Lasing fp (stable)')
