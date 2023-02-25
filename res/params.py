# timescale variables
import random
from math import log

gamma = 1e-3
epsilon = 1e-4

# time variables
t0 = 0
tf = 5e4
dt = 0.1

# laser parameters
k = 0.7
A = 1/k
a = 2

# noise parameters
h = 4
sigma = 5e-3


default_laser_params = {
    "k": k,
    "A": A,
    "a": a,
    "h": h
}


# Critical manifold, epsilon = 0, 2 branches

# OFF Branch
# NON LASING fixed point: [x=0, y=1, w=0]
# Stable for d<1
# Attracting for w<(1-d)/k
#
d_off = 0.995
stable_off_initial_condition = {
    "d": d_off,
    "x0": 1e-6,
    "y0": d_off,
    "w0": random.uniform(0, (1-d_off)/k)
}

noise_off_initial_condition = {
    "d": d_off,
    "e0": 0,
    "y0": d_off,
    "w0": random.uniform(0, (1-d_off)/k),
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
    "w0": (1-d_alternate)/k
}
noise_alternate_initial_condition = {
    "d": d_alternate,
    "e0": 1e-6,
    "y0": 0,
    "w0": (1-d_alternate)/k,
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
    "x0": d_on-1,
    "y0": 1,
    "w0": (1-d_on)/k
}

noise_on_initial_condition = {
    "d": d_on,
    "e0": d_on-1,
    "y0": 1,
    "w0": (1-d_on)/k
}



