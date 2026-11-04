"""Through-thickness transient heat conduction in half a brake rotor."""
import numpy as np
import pandas as pd
from scipy.linalg import solve_banded
from common import options, plt, save_plot

# Illustrative constant properties: density (kg/m³), heat capacity (J/kg/K),
# conductivity (W/m/K). These are engineering scenarios, not measured grades.
MATERIALS = {"Cast iron": (7200, 500, 52), "SiC composite": (2500, 800, 35)}
AMBIENT = 293.15
SIGMA = 5.670374419e-8


def simulate(material, elements=30, dt=0.1, duration=30.0, peak_flux=600_000.0):
    density, capacity, conductivity = material
    dx = 0.01/elements
    nodes = elements+1
    # Linear finite elements, lumped capacity, per square metre of face area.
    weights = np.ones(nodes); weights[[0, -1]] = 0.5
    mass = density*capacity*dx*weights
    off = -conductivity/dx
    diag = 2*conductivity/dx*weights
    temp = np.full(nodes, AMBIENT)
    history = [(0.0, AMBIENT-273.15, AMBIENT-273.15, 0.0, 0.0, 0.0)]
    incident = loss = 0.0
    for step in range(1, round(duration/dt)+1):
        time = dt*step
        # Integrate the triangular four-second heat pulse over each time step.
        def cumulative_heat(t):
            t = min(t, 4.)
            return peak_flux*(t-t*t/8.)
        flux = (cumulative_heat(time)-cumulative_heat(time-dt))/dt
        rhs = mass/dt*temp
        rhs[-1] += flux
        trial = temp.copy()
        for _ in range(12):
            surface = trial[-1]
            cooling = 35*(surface-AMBIENT) + 0.8*SIGMA*(surface**4-AMBIENT**4)
            residual = (mass/dt+diag)*trial-rhs
            residual[1:] += off*trial[:-1]
            residual[:-1] += off*trial[1:]
            residual[-1] += cooling
            bands = np.zeros((3, nodes))
            bands[0, 1:] = off; bands[2, :-1] = off
            bands[1] = mass/dt+diag
            bands[1, -1] += 35 + 4*0.8*SIGMA*surface**3
            change = solve_banded((1, 1), bands, -residual)
            trial += change
            if np.max(abs(change)) < 1e-9:
                break
        else:
            raise RuntimeError("Surface heat balance failed to converge.")
        temp = trial
        incident += flux*dt
        loss += dt*(35*(temp[-1]-AMBIENT)+0.8*SIGMA*(temp[-1]**4-AMBIENT**4))
        history.append((time,temp[-1]-273.15,temp[0]-273.15,incident,loss,mass @ (temp-AMBIENT)))
    return pd.DataFrame(history, columns=["time_s","surface_C","midplane_C","input_J_m2","loss_J_m2","stored_J_m2"])


def main():
    args = options("brake")
    fig, ax = plt.subplots(figsize=(7, 4))
    histories, metrics = [], []
    for name, material in MATERIALS.items():
        coarse = simulate(material)
        fine = simulate(material, elements=60, dt=0.05)
        coarse["material"] = name
        histories.append(coarse)
        peak = coarse.surface_C.max()
        balance = (coarse.input_J_m2-coarse.loss_J_m2-coarse.stored_J_m2).abs().max()
        metrics.append(dict(material=name, peak_surface_C=peak, refined_peak_C=fine.surface_C.max(),
                            peak_change_C=abs(peak-fine.surface_C.max()), max_energy_residual_J_m2=balance))
        ax.plot(coarse.time_s, coarse.surface_C, label=name)
    pd.concat(histories).to_csv(args.out/"temperatures.csv", index=False)
    pd.DataFrame(metrics).to_csv(args.out/"metrics.csv", index=False)
    ax.axvline(4, color="gray", ls="--", label="Brake release")
    ax.set(xlabel="Time (s)", ylabel="Surface temperature (°C)", title="Illustrative 1D rotor model")
    ax.legend()
    save_plot(fig, args.out)


if __name__ == "__main__":
    main()
