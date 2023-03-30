import math

from numpy import multiply, sqrt
from numpy.random import normal

from res import params


class single_node_pulse_laser:

    def __init__(self, s0, args=None):
        self.s = s0  # initial state

        self.k = args["k"]  # laser parameters
        self.A = args["A"]  # A logarithmic
        self.alpha = args["a"]  # alpha logarithmic
        self.h = args["h"]  # noise factor
        self.delta = args["d"]  # delta intensity
        self.pulse = args["p"]  # pulse strength
        self.t_range = args["t"]  # time range pulse
        self.sigma = args["s"]  # sigma noise

        self.noise = lambda: multiply(self.sigma, [normal(0, sqrt(params.dt)), 0, 0])
        self.p = lambda t: self.pulse if any([(tr[0] < t) & (t < tr[1]) for tr in self.t_range]) else 0
        self.get_state = lambda s: [abs(s[0]) ** 2, s[1], s[2]]

    def gx(self, x, t):
        return self.A * math.log(1 + (self.alpha * (x + self.p(t))))

    def apply(self, s, t) -> list[complex | float]:
        x = abs(s[0]) ** 2
        xy = x * s[1]
        gx = self.gx(x, t)

        return [
            0.5 * complex(1, 4) * s[0] * (s[1] - 1),
            params.gamma * (self.delta - s[1] + self.k * (s[2] + gx) - xy),
            -params.epsilon * (s[2] + gx)
        ]

    def set(self, s):
        self.s = s
