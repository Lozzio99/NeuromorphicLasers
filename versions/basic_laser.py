import math

from res.params import default_laser_params, epsilon, gamma


class single_node_laser:

    def __init__(self, s0, d, params=None):
        self.s = s0  # initial state
        self.d = d  # laser pump current (lasing threshold)

        if params is None:
            self.params = default_laser_params
        else:
            self.params = params

        self.k = self.params["k"]  # laser parameters
        self.A = self.params["A"]
        self.a = self.params["a"]

    def gx(self) -> float:
        return self.A * math.log(1 + (self.a * self.s[0]))

    def x_dot(self) -> float:
        return self.s[0] * (self.s[1] - 1)

    def y_dot(self) -> float:
        xy = self.s[0] * self.s[1]
        return gamma * (self.d - self.s[1] + self.k * (self.s[2] + self.gx()) - xy)

    def w_dot(self) -> float:
        return -epsilon * (self.s[2] + self.gx())

    def set(self, s):
        if s is not None:
            self.s = s

    def get_state(self, s=None):
        if s is not None:
            return s
        return [self.s[0], self.s[1], self.s[2]]

    def apply(self, s=None, t=None) -> list[float]:
        self.set(s)
        return [self.x_dot(), self.y_dot(), self.w_dot()]

