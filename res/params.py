# timescale variables
import random

gamma = 0.004
epsilon = 0.0001

# time variables
t0 = 0
tf = 1e5
dt = 0.1

# laser parameters
k = 0.7
A = 1 / k
a = 2
h = 4
sigma = 1 / (-510 ** 2)

p = 0.01
t_range = [0, 1000]
c = 0.5

# method = 'sum'
method = 'mean_sum'  # coupling method


def default_laser_params():
    return {
        "k": k,
        "A": A,
        "a": a,
        "h": h,
        "s": sigma,
        "p": p,
        "t": t_range,
        "c": c,
        "d": 0.995,
        "e0": 0,
        "y0": 0.995,
        "w0": 0
    }


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Critical manifold, epsilon = 0, 2 branches

# OFF Branch
# NON LASING fixed point: [x=0, y=1, w=0]
# Stable for d<1
# Attracting for w<(1-d)/k
#
d_off = 1 - 1e-6
stable_off_initial_condition = {
    "d": d_off,
    "x0": 0,
    "y0": 0,
    "w0": 0
}

noise_off_initial_condition = {
    "d": d_off,
    "e0": 1e-6,
    "y0": d_off,
    "w0": random.uniform(0, (1 - d_off) / k),
}

pulse_off_initial_condition = {
    "d": 0.995,
    "e0": 0,
    "y0": 0.995,
    "w0": 0,
}

#
#
#
#
#
#
#
#
#
#
# ALTERNATE BRANCH
# Unstable for 1 < d < 1.5136
#
d_alternate = 1.3
unstable_initial_condition = {
    "d": d_alternate,
    "x0": 1e-6,
    "y0": 0,
    "w0": (1 - d_alternate) / k
}
noise_alternate_initial_condition = {
    "d": d_alternate,
    "e0": 1e-6,
    "y0": 0,
    "w0": (1 - d_alternate) / k,
}

#
#
# ON Branch
# LASING fixed point : [x=d-1, y=1, w= -A ln(1+a(d-1))
# Emerges at: [x=0, w=(1-d)/k]
# Stable for d > 1.5136
# Attracting for x>kA-(1/a)
#
d_on = 1.6
stable_on_initial_condition = {
    "d": d_on,
    "x0": d_on - 1,
    "y0": 1,
    "w0": (1 - d_on) / k
}

noise_on_initial_condition = {
    "d": d_on,
    "e0": d_on - 1,
    "y0": 1,
    "w0": (1 - d_on) / k
}

# pulse params
