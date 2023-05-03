from math import log
from pathlib import Path
from typing import Callable, Any

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter
from numpy import where

from res.params import A, a, k, tf, t0

global show_xw
global show_xyw
global frames

globals().__setitem__('show_xw', True)
globals().__setitem__('show_xyw', True)
globals().__setitem__('frames', 100)


def plot_solution(ts, solution, fixed_point, title=None, file_name=None, phase_space=False, makegif=False):
    if makegif:
        if show_xyw:
            plot_dynamic_xyw_t(ts, solution, fixed_point, title, file_name)
        if show_xw:
            plot_dynamic_x_w(ts, solution, fixed_point, title, phase_space, file_name)
    else:
        if show_xyw:
            plot_static_xyw_t(ts, solution, fixed_point, title)
        if show_xw:
            plot_static_x_w(solution, fixed_point, title, phase_space)


def plot_static_xyw_t(ts, solution, fixed_point, title=None, share_axes=True):
    x1 = ts[0]
    x2 = ts[len(ts) - 1]

    plt.figure()

    if share_axes:
        plt.plot(ts, solution[:, 0], 'r')
        plt.plot(ts, solution[:, 1], 'g')
        plt.plot(ts, solution[:, 2], 'b')

        plt.xlabel("t")
    else:
        plt.subplot(1, 3, 1), plt.plot(ts, solution[:, 0], 'r'), plt.ylabel("x(t)"), plt.xlabel("t")
        plt.subplot(1, 3, 2), plt.plot(ts, solution[:, 1], 'g'), plt.ylabel("y(t)"), plt.xlabel("t")
        plt.subplot(1, 3, 3), plt.plot(ts, solution[:, 2], 'b'), plt.ylabel("w(t)"), plt.xlabel("t")

    plt.hlines(fixed_point[0], x1, x2, 'r', '--')
    plt.hlines(fixed_point[1], x1, x2, 'g', ':')
    plt.hlines(fixed_point[2], x1, x2, 'b', ':')

    plt.legend(["x(t)", "y(t)", "w(t)"])
    plt.tight_layout()

    if title is not None:
        plt.suptitle(title)

    plt.show()


def plot_static_x_w(solution, fixed_point, title=None, phase_space=False):
    if len(solution[0, :]) > 2:
        plt.figure()
        plt.plot(solution[:, 0], solution[:, 2], 'k')

        plt.xlabel("x"), plt.ylabel("w")
        if phase_space:
            plot_manifold(fixed_point, min(solution[:, 2]), max(solution[:, 2]))
        if title is not None:
            plt.suptitle(title)
        plt.show()


def plot_dynamic_xyw_t(ts, solution, fixed_point, title=None, file_name=None):
    x1 = ts[0]
    x2 = ts[len(ts) - 1]
    t_span = round((x2 - x1) / frames)

    fig = plt.figure()

    plt.xlim(x1, x2)
    plt.ylim(min(min(solution[:, 0]), min(solution[:, 1]), min(solution[:, 2])) - 0.5,
             max(max(solution[:, 0]), max(solution[:, 1]), max(solution[:, 2])) + 0.5)

    plt.hlines(fixed_point[0], x1, x2, 'r', 'dotted')
    plt.hlines(fixed_point[1], x1, x2, 'g', 'dotted')
    plt.hlines(fixed_point[2], x1, x2, 'b', 'dotted')

    if title is not None:
        plt.suptitle(title)

    plt.ylabel("value"), plt.xlabel("t")
    plt.legend(["x(t)", "y(t)", "w(t)"])
    plt.tight_layout()

    l1, = plt.plot([], [], 'r')
    l2, = plt.plot([], [], 'g')
    l3, = plt.plot([], [], 'b')

    writer, output_file = make_gif_writer(f"{file_name}_xyw_t")

    with writer.saving(fig, output_file, frames):
        t = t0
        for i in range(0, frames - 1):
            if i % 20 == 0:
                print(f"frame {i} / {frames}")
            ftf = min(t + t_span, tf)
            ft0 = max(0, ftf - (t_span * 40))
            ida = int(where(ts == ft0)[0][0])
            idz = int(where(ts == ftf)[0][0])
            l1.set_data(ts[ida:idz], solution[ida:idz, 0])
            l2.set_data(ts[ida:idz], solution[ida:idz, 1])
            l3.set_data(ts[ida:idz], solution[ida:idz, 2])
            writer.grab_frame()
            t = ftf

    print(f"Gif file {output_file.absolute()} successfully created.")

    l1.set_data(ts, solution[:, 0])
    l2.set_data(ts, solution[:, 1])
    l3.set_data(ts, solution[:, 2])
    plt.show()


def plot_manifold(fixed_point, y_min, y_max):
    delta = fixed_point[3]
    w = (1 - delta) / k
    plt.vlines(x=0, ymin=y_min, ymax=w, colors='r', linestyles='--')  # unstable off
    plt.vlines(x=0, ymin=w, ymax=y_max, colors='b')  # stable off
    # x_b = k * A - (1 / a)
    x_b = fixed_point[0]
    x_unstable = np.linspace(0, x_b, 100)
    x_stable = np.linspace(x_b, x_b * 2.5, 100)
    gx: Callable[[float], float] = lambda x: A * log(1 + (a * x))
    wx: Callable[[Any], list[float | Any]] = lambda x: [((xi - delta + 1) / k) - gx(xi) for xi in x]
    plt.plot(x_unstable, wx(x_unstable), 'r--')
    plt.plot(x_stable, wx(x_stable), 'b')

    plt.plot([0], [w], marker="o", markersize=5, markeredgecolor="red", markerfacecolor="white")
    plt.plot([x_b], wx([x_b]), marker="o", markersize=5, markeredgecolor="blue", markerfacecolor='black')


def plot_dynamic_x_w(ts, solution, fixed_point, title=None, phase_space=True, file_name=None):
    fig, ax = plt.subplots()

    x1 = ts[0]
    x2 = ts[len(ts) - 1]
    t_span = round((x2 - x1) / frames)

    y1 = min(solution[:, 2])
    y2 = max(solution[:, 2])
    plt.xlim(min(solution[:, 0]) - 0.5, max(solution[:, 0]) + 0.5)
    plt.ylim(y1 - 0.1, y2 + 0.1)

    if title is not None:
        plt.suptitle(title)

    plt.ylabel("w(t)"), plt.xlabel("x(t)")
    plt.legend(["x(t)", "w(t)"])
    plt.tight_layout()

    if phase_space:
        plot_manifold(fixed_point, y1, y2)

    l, = plt.plot([], [], 'k')
    l2 = plt.text(0.5, 0.5, 't = 0',
                  horizontalalignment='center', verticalalignment='top', transform=ax.transAxes)

    writer, output_file = make_gif_writer(f"{file_name}_x_w")

    with writer.saving(fig, output_file, frames):
        t = t0
        for i in range(0, frames - 1):
            if i % 20 == 0:
                print(f"frame {i} / {frames}")
            ftf = min(t + t_span, tf)
            ft0 = max(0, ftf - (t_span * 40))
            ida = int(where(ts == ft0)[0][0])
            idz = int(where(ts == ftf)[0][0])
            l2.set_text(f't = {ts[idz]}')
            l.set_data(solution[ida:idz, 0], solution[ida:idz, 2])
            writer.grab_frame()
            t = ftf

    print(f"Gif file {output_file.absolute()} successfully created.")

    l2.set_text(f't = {tf}')
    l.set_data(solution[:, 0], solution[:, 2])
    plt.show()


def make_gif_writer(filename):
    writer = PillowWriter(fps=15)
    output_file = Path(f"../gifs/{filename}.gif")
    output_file.parent.mkdir(exist_ok=True, parents=True)

    print(f"Creating gif file in: {output_file.absolute()}")
    return writer, output_file
