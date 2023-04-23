import numpy as np
from numpy import multiply, sqrt, sort
from numpy.random import normal

from res import params
from res.params import gamma


class laser_array:
    def __init__(self, deltas, args):
        self.deltas = sort(deltas)  # array deltas
        self.n_iris = len(deltas)  # num of laser nodes
        self.A = args["A"]  # A logarithmic
        self.alpha = args["a"]  # alpha logarithmic
        self.pulse = args["p"]  # pulse strength
        self.t_range = args["t"]  # time range pulse
        self.k = args["k"]  # laser parameters
        self.h = args["h"]  # noise factor
        self.sigma = args["s"]  # sigma noise

        self.noise = lambda: [multiply(self.sigma, [normal(0, sqrt(params.dt)), 0, 0]) for _ in range(self.n_iris)]
        self.P = lambda t: self.pulse if self.t_range[0] <= t < self.t_range[1] else 0
        self.s0 = np.empty(shape=(self.n_iris, 3))

        for j in range(self.n_iris):
            self.s0[j] = [args['e0'], self.deltas[j], args['w0']]

        self.s = self.s0
        self.x = self.X(self.s)

    def X(self, s):
        intensity_sum = 0
        for i in range(self.n_iris):
            intensity_sum += abs(s[i, 0]) ** 2

        if params.method == 'mean_sum':
            return intensity_sum / self.n_iris
        if params.method == 'sum':
            return intensity_sum
        pass

    def gx(self, s, t):
        self.x = self.X(s)
        return self.A * np.log(1 + (self.alpha * (self.x + self.P(t))))

    def apply(self, s, t):
        # assert (len(set(s[:, 2])) == 1) & (len(s) == self.n_iris)
        gx = self.gx(s, t)
        w_dot = -params.epsilon * (s[0, 2] + gx)
        s_dot = np.empty(shape=(self.n_iris, 3), dtype=complex)
        for i in range(self.n_iris):
            e, y, w = s[i]
            x = abs(e) ** 2
            xy = x * y
            s_dot[i] = [
                0.5 * complex(1, self.h) * e * (y - 1),
                gamma * (self.deltas[i] - y + self.k * (w + gx) - xy),
                w_dot
            ]
        return s_dot

    def get_state(self, s) -> list[list[float]]:
        return [[abs(s[i, 0]) ** 2, s[i, 1].real, s[i, 2].real] for i in range(self.n_iris)]

    def set(self, s):
        # self.x = self.X(s)
        self.s = s
