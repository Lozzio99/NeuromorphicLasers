from res import params
from res.solvers import time_sequence, solve_population, euler_mayurama
from versions.masked_population import masked_array
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

pio.renderers.default = "browser"

params.tf = 5e3
params.t_range = [0, 500]

d1 = 0.35
d2 = 0.95

mask = [0, 1]
n_pulses = 2
laser = masked_array([d1, d2], mask)

ts = time_sequence(params.t0, params.tf, params.dt)
p_range = np.arange(0, 1.1, 0.001)

# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for pulse_strength in p_range:
    print(pulse_strength)

    x1_sum = np.zeros((len(ts)))
    x2_sum = np.zeros((len(ts)))

    for _ in range(n_pulses):
        laser.state0()
        params.p = pulse_strength
        traj = solve_population(ts, laser, euler_mayurama)
        x1_sum = np.add(x1_sum, traj[:, 0, 0])
        x2_sum = np.add(x2_sum, traj[:, 1, 0])

    trace1 = go.Scatter(visible=False, line=dict(color="blue", width=2),
                        name=rf"$\delta_1={d1}$", x=ts, y=np.divide(x1_sum, n_pulses))
    trace2 = go.Scatter(visible=False, line=dict(color="red", width=2),
                        name=rf"$\delta_2={d2}$", x=ts, y=np.divide(x2_sum, n_pulses))

    fig.add_traces([trace1, trace2])

# Make 10th trace visible
fig.data[0].visible = True
fig.data[1].visible = True

# Create and add slider
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
    active=100,
    currentvalue={"prefix": "pulse strength ", "suffix": ""},
    pad={"t": 10},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)


fig.show()

