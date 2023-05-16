from numpy import sort, sqrt, multiply, empty, log, concatenate
from numpy.random import normal

from res import params

default_laser_params = params.default_laser_params_OFF()


class laser_array:

    def __init__(self, deltas):
        self.deltas = sort(deltas)  # array deltas
        self.n_iris = len(deltas)
        self.noise = lambda: [multiply(params.sigma, [normal(0, sqrt(params.dt)), 0, 0]) for _ in range(self.n_iris)]
        self.P = lambda t: params.p if params.t_range[0] <= t < params.t_range[1] else 0

        self.s0 = empty(shape=(self.n_iris, 3))
        for j in range(self.n_iris):
            self.s0[j] = [default_laser_params['e0'], self.deltas[j], default_laser_params['w0']]

        self.s = self.s0
        self.x = self.X(self.s)

    def X(self, s):
        intensity_sum = 0

        for i in range(self.n_iris):
            intensity_sum += abs(s[i, 0]) ** 2

        if params.method == 'mean_sum':
            return intensity_sum / self.n_iris
        elif params.method == 'sum':
            return intensity_sum
        pass

    def gx(self, s, t):
        self.x = self.X(s)
        return params.A * log(1 + (params.a * (self.x + self.P(t))))

    def apply(self, s, t):
        # assert (len(set(s[:, 2])) == 1) & (len(s) == self.n_iris)
        gx = self.gx(s, t)
        w_dot = -params.epsilon * (s[0, 2] + gx)
        s_dot = empty(shape=(self.n_iris, 3), dtype=complex)
        for i in range(self.n_iris):
            e, y, w = s[i]
            x = abs(e) ** 2
            xy = x * y
            s_dot[i] = [
                0.5 * complex(1, params.h) * e * (y - 1),
                params.gamma * (self.deltas[i] - y + params.k * (w + gx) - xy),
                w_dot
            ]
        return s_dot

    def get_state(self, s) -> list[list[float]]:
        return [[abs(s[i, 0]) ** 2, s[i, 1].real, s[i, 2].real] for i in range(self.n_iris)]

    def set(self, s):
        self.s = s

    def state0(self):
        self.s = self.s0
        return self.s


class coupled_arrays:

    def __init__(self, d1, d2):
        self.p1 = laser_array(d1)
        self.p2 = laser_array(d2)
        self.n_iris = self.p1.n_iris + self.p2.n_iris
        self.s0 = concatenate((self.p1.s, self.p2.s), axis=0)
        self.s = self.s0
        self.get_state = lambda s: [[abs(s[i, 0]) ** 2, s[i, 1].real, s[i, 2].real] for i in range(self.n_iris)]
        self.p2.gx = lambda s, t: params.A*log(1+(params.a*((1-params.c)*self.p2.X(s)+(params.c*self.p1.x))))
        self.noise = lambda: concatenate((self.p1.noise(), self.p2.noise()), axis=0)

    def state0(self):
        self.s = self.s0
        self.p1.state0()
        self.p2.state0()
        return self

    def set(self, s):
        self.s = s

    def apply(self, s, t):
        return concatenate(
            (self.p1.apply(s[:self.p1.n_iris], t),
             self.p2.apply(s[self.p1.n_iris:(self.p1.n_iris + self.p2.n_iris)], t)),
            axis=0)

