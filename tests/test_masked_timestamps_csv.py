import csv
import os
from pathlib import Path

import numpy as np
import glob

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

from plotly.subplots import make_subplots

from res import params
from res.solvers import time_sequence, solve_population, euler_mayurama
from versions.masked_population import masked_array

pio.renderers.default = "browser"

p_range = np.arange(0., 1.001, 0.025)
d1 = 0.35
d2 = 0.95

masks = [
    [0, 1],
    [0.5, 0.5],
    [1, 0]
]

n_pulses = 2
params.tf = 2e3
params.t_range = [0, 500]
folder = f"..\\imgs\\timestamps\\[{d1},{d2}]"

d1s = rf"$\delta_1:{d1}$"
d2s = rf"$\delta_2:{d2}$"


def show():
    fig = go.Figure()

    for f in os.listdir(folder):
        df = pd.read_csv(folder + "\\" + f)
        ts = df["t"]
        trace1 = go.Scatter(visible=False, line=dict(color="blue", width=2),
                            name=rf"$\delta_1:{d1}$", x=ts, y=df["x1"])
        trace2 = go.Scatter(visible=False, line=dict(color="red", width=2),
                            name=rf"$\delta_2:{d2}$", x=ts, y=df["x2"])
        fig.add_traces([trace1, trace2])

    fig.data[0].visible = True
    fig.data[1].visible = True

    steps = []
    for i in range(len(p_range)):
        pulse_strength = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"Pulse strength: {p_range[i]}"}],
            label=p_range[i]
        )
        pulse_strength["args"][0]["visible"][i * 2] = True
        pulse_strength["args"][0]["visible"][i * 2 + 1] = True

        steps.append(pulse_strength)

    sliders = [dict(
        active=1,
        currentvalue={"prefix": "pulse strength ", "suffix": ""},
        pad={"t": 10},
        steps=steps
    )]

    fig.update_layout(sliders=sliders)
    fig.show()


def write():
    ts = time_sequence(params.t0, params.tf, params.dt)

    for mask in masks:
        print(f"mask {mask}")
        laser = masked_array([d1, d2], mask)

        for pulse_strength in p_range:
            print(pulse_strength)

            x1_sum = np.zeros((len(ts)))
            y1_sum = np.zeros((len(ts)))
            x2_sum = np.zeros((len(ts)))
            y2_sum = np.zeros((len(ts)))
            w_sum = np.zeros((len(ts)))

            for _ in range(n_pulses):
                laser.state0()
                params.p = pulse_strength
                traj = solve_population(ts, laser, euler_mayurama)
                x1_sum = np.add(x1_sum, traj[:, 0, 0])
                x2_sum = np.add(x2_sum, traj[:, 1, 0])
                y1_sum = np.add(y1_sum, traj[:, 0, 1])
                y2_sum = np.add(y2_sum, traj[:, 1, 1])
                w_sum = np.add(w_sum, traj[:, 0, 2])

            x1 = x1_sum / n_pulses
            x2 = x2_sum / n_pulses
            y1 = y1_sum / n_pulses
            y2 = y2_sum / n_pulses
            w = w_sum / n_pulses

            timestamp = []
            for i in range(len(ts)):
                timestamp.append({
                    "t": ts[i],
                    "x1": x1[i],
                    "x2": x2[i],
                    "y1": y1[i],
                    "y2": y2[i],
                    "w": w[i],
                })

            pcsv = Path(folder + f"/mask{mask}/p_{pulse_strength:.3f}.csv")
            pcsv.parent.mkdir(exist_ok=True, parents=True)
            try:
                with open(pcsv, 'w', newline='', encoding='utf-8') as csvfile:
                    print(f"writing file {csvfile}...")
                    writer = csv.DictWriter(csvfile, fieldnames=['t', 'x1', 'x2', 'y1', 'y2', 'w'])
                    writer.writeheader()
                    writer.writerows(timestamp)

            except IOError:
                print("I/O error")


# show()
write()
