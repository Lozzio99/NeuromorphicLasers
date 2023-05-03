import math

from numpy import multiply, sqrt
from numpy.random import normal

from res import params


class single_node_noise_laser:

    def __init__(self, s0, d, args=None):
        self.s = s0  # initial state
        self.d = d  # laser pump current (lasing threshold)

        if args is None:
            self.params = params.default_laser_params_OFF()
        else:
            self.params = args

        self.k = self.params["k"]  # laser parameters
        self.A = self.params["A"]
        self.a = self.params["a"]
        self.h = self.params["h"]

        self.noise = lambda: multiply(params.sigma, [normal(0, sqrt(params.dt)), 0, 0])

    def x(self) -> complex:
        return abs(self.s[0]) ** 2

    def gx(self) -> complex:
        return self.A * math.log(1 + (self.a * self.x()))

    def x_dot(self) -> complex:
        return self.x() * (self.s[1] - 1)

    def y_dot(self) -> complex:
        xy = self.x() * self.s[1]
        return params.gamma * (self.d - self.s[1] + self.k * (self.s[2] + self.gx()) - xy)

    def w_dot(self) -> complex:
        return -params.epsilon * (self.s[2] + self.gx())

    # Error ######################################################################

    def e_dot(self) -> complex:
        return 0.5 * complex(1, 4) * self.s[0] * (self.s[1] - 1)

    ##############################################################################

    def set(self, s):
        if s is not None:
            self.s = s

    def get_state(self, s=None) -> list[complex | float]:
        if s is not None:
            return [abs(self.s[0]) ** 2, s[1], s[2]]
        return [self.x(), self.s[1], self.s[2]]

    def apply(self, s=None, t=None) -> list[complex | float]:
        self.set(s)
        return [self.e_dot(), self.y_dot(), self.w_dot()]

