from numpy import mean
from scipy.signal import find_peaks

from res.params import dt


def analyse_peaks(ts, solution):
    peaks, properties = find_peaks(solution[:, 0],
                                   height=2,
                                   width=(None, None),
                                   prominence=2)
    print(peaks, properties)
    # plt.plot(ts[peaks], solution[:, 0][peaks], "x")
    # plt.vlines(x=ts[peaks], ymin=solution[:, 0][peaks] - properties["prominences"], ymax=solution[:, 0][peaks])


def analyse_solution(ts, solution):
    # assuming initial condition close to off fixed point (x = 0)
    # state 0 - before first spike / non spiking
    # state 1 - after any spike / non spiking
    # state 2 - during any spike / spiking
    state = 0
    threshold = 0.01

    tp = []
    ta = []
    te = []

    start_spike_t = 0
    end_prev_spike_t = 0
    transition_count = 0
    step = int(500 / dt)

    for i, t in enumerate(ts):
        x = solution[i, 0]
        if state == 2:                          # during spiking state
            if x < threshold:                   # wait for end of laser relaxation osc.
                transition_count += 1
                if transition_count > step:
                    te.append(ts[i-step] - start_spike_t)  # record excursion time
                    if len(ta) > 0:  # if this isn't the first recorded spiking end
                        # record pulse duration : last recorded activation time + last recorded excursion time
                        tp.append(ta[len(ta) - 1] + te[len(te) - 1])

                    end_prev_spike_t = t  # update this as the last recorded spike
                    state = 1                   # go to state : after any spike / non spiking
                    transition_count = 0
            else:                               # if it's fake spike end
                transition_count = 0
        else:                                   # non spiking state 0 or 1
            if x > threshold:                   # reaching spike
                transition_count += 1
                if transition_count > step:
                    start_spike_t = ts[i-step]  # get the initial spike time
                    if state == 1:              # if non-first spike
                        ta.append(start_spike_t - end_prev_spike_t)  # record activation time

                    state = 2  # now spiking
                    transition_count = 0

            else:                               # if it's fake spike start
                transition_count = 0

    print(f'Excursion time  : {mean(te) if len(te) > 0 else 0}')
    print(f'Activation time : {mean(ta) if len(ta) > 0 else 0}')
    print(f' Pulse duration  : {mean(tp) if len(tp) > 0 else 0}')

    print(f'Activation times : \n{ta}')
    print(f'Excursion  times : \n{te}')
    print(f'Pulse durations  : \n{tp}')
    return tp, ta, te


def print_solution(ts, solution):
    for i in range(len(solution)):
        print(f"t: {ts[i]}", f"s: {solution[i]}")
