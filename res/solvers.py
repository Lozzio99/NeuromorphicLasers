# y(t0) = y0 = s = laser.s
# y'(t) = f(t, y(t)) = laser.apply(s)
from res import params

import numpy as np
from numpy import multiply, add, sqrt


def euler(laser, h):
    s = laser.s
    return add(s, multiply(h, laser.apply(s)))


def midpoint(laser, h):
    h2 = h / 2
    s = laser.s
    s2 = add(s, multiply(h2, laser.apply(s)))
    return add(s, multiply(h, laser.apply(s2)))


def improved_euler(laser, h):
    s = laser.s
    fs = laser.apply(s)
    s_ = add(s, multiply(h, fs))
    fs_ = laser.apply(s_)
    return add(s, multiply(h / 2, add(fs, fs_)))


def rk4(laser, h):
    s = laser.s
    k1 = multiply(h, laser.apply(s))
    k2 = multiply(h, laser.apply(add(s, multiply(0.5, k1))))
    k3 = multiply(h, laser.apply(add(s, multiply(0.5, k2))))
    k4 = multiply(h, laser.apply(add(s, multiply(0.5, k3))))
    k5 = add(multiply(1 / 6, k1), multiply(1 / 6, k4))
    k6 = add(multiply(1 / 3, k2), multiply(1 / 3, k3))
    return add(s, add(k5, k6))


def euler_mayurama(laser, h):
    noise = multiply(sqrt(h), laser.noise())
    return add(improved_euler(laser, h), noise)


def solve(ts, laser, method):
    t0 = params.t0
    sz = len(ts)
    traj = np.empty(shape=(sz, len(laser.s)))
    traj[0, :] = laser.s
    i = 1
    while i < sz:
        if i % 5e4 == 0:
            print(f"Iteration {i}/{sz}")
        t1 = ts[i]
        h = t1 - t0
        y1 = method(laser, h)
        traj[i, :] = laser.get_state(y1)
        laser.set(y1)
        t0 = t1
        i += 1

    return traj


def solve_t(t0, tf, dt, laser, method):
    ts = np.arange(t0, tf, dt)
    return ts, solve(ts, laser, method)
