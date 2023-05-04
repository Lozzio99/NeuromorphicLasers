from res import params
from versions.laser_population_fast import laser_array

default_laser_params = params.default_laser_params_OFF()


class masked_array(laser_array):

    def __init__(self, deltas, mask):
        # assert len(deltas) == len(mask)
        # assert sum(mask, axis=0) == 1
        # assert all([x <= 1 for x in mask])
        self.weights = mask
        super().__init__(deltas)
        self.P = lambda t: params.p * t / params.t_range[1] if params.t_range[0] <= t < params.t_range[1] else 0

    def X(self, s):
        intensity_sum = 0

        for i in range(self.n_iris):
            intensity_sum += (abs(s[i, 0]) ** 2) * self.weights[i]

        return intensity_sum
