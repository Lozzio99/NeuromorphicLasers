# y(t0) = y0 = s = laser.s
# y'(t) = f(t, y(t)) = laser.apply(s)
import numpy as np
from numpy import multiply, add

from res import params


def euler(laser, t, h):
    s = laser.s
    return add(s, multiply(h, laser.apply(s)))


def midpoint(laser, t, h):
    h2 = h / 2
    s = laser.s
    s2 = add(s, multiply(h2, laser.apply(s)))
    return add(s, multiply(h, laser.apply(s2)))


def improved_euler(laser, t, h):
    s = laser.s
    fs = laser.apply(s)
    s_ = add(s, multiply(h, fs))
    fs_ = laser.apply(s_)
    return add(s, multiply(h / 2, add(fs, fs_)))


def rk4(laser, t, h):
    s = laser.s
    k1 = multiply(h, laser.apply(s))
    k2 = multiply(h, laser.apply(add(s, multiply(0.5, k1))))
    k3 = multiply(h, laser.apply(add(s, multiply(0.5, k2))))
    k4 = multiply(h, laser.apply(add(s, multiply(0.5, k3))))
    k5 = add(multiply(1 / 6, k1), multiply(1 / 6, k4))
    k6 = add(multiply(1 / 3, k2), multiply(1 / 3, k3))
    return add(s, add(k5, k6))


def euler_mayurama(laser, t, h):
    noise = laser.noise()
    s = laser.s
    fs = laser.apply(s, t)
    s_ = add(add(s, multiply(h, fs)), noise)
    fs_ = laser.apply(s_, t)
    return add(add(s, multiply(h / 2, add(fs, fs_))), noise)


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
        y1 = method(laser, t0, h)
        traj[i, :] = laser.get_state(y1)
        laser.set(y1)
        t0 = t1
        i += 1

    return traj


def solve_population(ts, population, method):
    t0 = params.t0
    sz = len(ts)
    traj = np.empty(shape=(sz, population.n_iris, 3))
    traj[0, :, :] = population.get_state(population.s)
    i = 1
    while i < sz:
        if i % 5e4 == 0:
            print(f"Iteration {i}/{sz}")
        t1 = ts[i]
        h = t1 - t0
        y1 = method(population, t0, h)
        traj[i, :, :] = population.get_state(y1)

        population.set(y1)

        t0 = t1
        i += 1

    return traj


def solve_population_until_spike(t0, tf, dt, laser, method, spike_thresh):
    ts = np.arange(t0, tf, dt)
    t = t0
    sz = len(ts)
    i = 1
    while t < tf:
        if i % 1e5 == 0:
            print(f"Iteration {i}/{sz}")

        y1 = method(laser, t, dt)

        if laser.X(y1) > spike_thresh:
            return t, 1

        else:
            laser.set(y1)
            t += dt
            i += 1

    return t, 0


def solve_until_individual_spikes(t0, tf, dt, laser, method, spike_thresh):
    ts = np.arange(t0, tf, dt)
    t = t0
    sz = len(ts)
    i = 1

    individual_times = np.full(laser.n_iris, tf)
    individual_responses = np.full(laser.n_iris, 0)

    while t < tf:
        if i % 1e5 == 0:
            print(f"Iteration {i}/{sz}")

        y1 = method(laser, t, dt)

        for ls in range(laser.n_iris):
            if abs(y1[ls, 0]) ** 2 > spike_thresh[ls]:
                individual_times[ls] = t
                individual_responses[ls] = 1

        if all(individual_responses):
            return individual_times, individual_responses
        else:
            laser.set(y1)
            t += dt
            i += 1

    return individual_times, individual_responses


def solve_coupled_until_spike(t0, tf, dt, laser, n1, method, spike_thresh):
    ts = np.arange(t0, tf, dt)
    t = t0
    t1 = 0
    sz = len(ts)
    i = 1
    p1_spiking = False

    while t < tf:
        if i % 1e5 == 0:
            print(f"Iteration {i}/{sz}")

        y1 = method(laser, t, dt)
        if not p1_spiking:
            if laser.p1.X(y1[:n1]) > spike_thresh:
                t1 = t
                p1_spiking = True

        if p1_spiking:
            if laser.p2.X(y1[n1:]) > spike_thresh:
                return t - t1, 1

        laser.set(y1)
        t += dt
        i += 1

    return t-t1 if p1_spiking else t, 0


def solve_t(t0, tf, dt, laser, method):
    ts = np.arange(t0, tf, dt)
    return ts, solve(ts, laser, method)
