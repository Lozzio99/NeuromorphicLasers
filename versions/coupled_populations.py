import numpy as np
from numpy import log

from versions.laser_population import laser_array


class coupled_arrays:

    # class for 2 populations of lasers chained within the logarithmic amplifier (w)

    def __init__(self, d1, d2, args):
        self.d1 = d1
        self.d2 = d2

        self.p1 = laser_array(d1, args)
        self.p2 = laser_array(d2, args)

        self.n_iris = self.p1.n_iris + self.p2.n_iris

        self.c = args['c']

        self.p2.gx = self.g2x

        self.s = np.concatenate((self.p1.s, self.p2.s), axis=0)

        self.get_state = lambda s: [[abs(s[i, 0]) ** 2, s[i, 1].real, s[i, 2].real] for i in range(self.n_iris)]

        self.noise = lambda: np.concatenate((self.p1.noise(), self.p2.noise()), axis=0)

    def g2x(self, s, t):
        self.p2.x = self.p2.X(s)
        return self.p2.A * log(1 + (self.p2.alpha * (self.p2.x + (self.c * self.p1.x))))

    def set(self, s):
        self.s = s

    def apply(self, s, t):
        return np.concatenate(
            (self.p1.apply(s[:self.p1.n_iris], t),
             self.p2.apply(s[self.p1.n_iris:(self.p1.n_iris + self.p2.n_iris)], t)),
            axis=0)
