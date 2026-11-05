"""Illustrative 1-D half-slab FEA; not the original COMSOL simulation."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

SIGMA = 5.670374419e-8
PARAMS = dict(m_vehicle=1500., v0=25., decel=8.,
    front_fraction=0.70, rotors=2, heat_fraction=0.90,
    ro=0.14, ri=0.07, thickness=0.013,
    rho=7200., cp=500., conductivity=50.,
    h=50., emissivity=0.8, ambient=300.)

def load(p, t):
    speed = max(p["v0"]-p["decel"]*t, 0.)
    power = (p["heat_fraction"]*p["front_fraction"]/p["rotors"]
             *p["m_vehicle"]*p["decel"]*speed)
    area = np.pi*(p["ro"]**2-p["ri"]**2)
    return power/(2*area)  # Equal heat on both full annular faces.

def solve(p, elements=40, dt=0.025, end=60.):
    half = p["thickness"]/2
    dx = half/elements
    nodes = elements+1
    M = np.zeros((nodes, nodes)); K = np.zeros_like(M)
    for e in range(elements):
        ix = np.ix_([e, e+1], [e, e+1])
        M[ix] += p["rho"]*p["cp"]*dx/6*np.array([[2,1],[1,2]])
        K[ix] += p["conductivity"]/dx*np.array([[1,-1],[-1,1]])
    # Midplane is insulated by symmetry; outer node has heat input/loss.
    T = np.full(nodes, p["ambient"])
    times = np.unique(np.r_[np.arange(0, end, dt),
                           p["v0"]/p["decel"], end])
    times = times[(times >= 0) & (times <= end)]
    base = p["ambient"]
    history = [[0., base, base, 0., 0., 0.]]
    heat_in = heat_out = 0.
    weights = M @ np.ones(nodes)
    for t0, t1 in zip(times[:-1], times[1:]):
        step = t1-t0
        q = load(p, (t0+t1)/2)
        old = T.copy(); trial = old.copy()
        A = M/step+K
        for _ in range(20):
            surface = trial[-1]
            loss = (p["h"]*(surface-base)
                    +p["emissivity"]*SIGMA*(surface**4-base**4))
            residual = M @ ((trial-old)/step)+K @ trial
            residual[-1] += loss-q
            J = A.copy()
            J[-1,-1] += p["h"]+4*p["emissivity"]*SIGMA*surface**3
            update = np.linalg.solve(J, -residual)
            trial += update
            if np.max(np.abs(update)) < 1e-9:
                break
        else:
            raise RuntimeError("Newton iteration did not converge")
        T = trial
        loss = (p["h"]*(T[-1]-base)
                +p["emissivity"]*SIGMA*(T[-1]**4-base**4))
        heat_in += q*step; heat_out += loss*step
        stored = float(weights @ (T-base))
        mean = float(weights @ T / weights.sum())
        history.append([t1,T[-1],mean,heat_in,heat_out,stored])
    return pd.DataFrame(history, columns=["time_s","surface_K","mean_K",
                 "input_J_m2","loss_J_m2","stored_J_m2"])

def main():
    out = Path("verification_outputs"); out.mkdir(exist_ok=True)
    rows = []; final = None
    for sweep, n, step in [("mesh",10,0.025),("mesh",20,0.025),
                            ("mesh",40,0.025),("time",40,0.10),
                            ("time",40,0.05),("time",40,0.025)]:
        data = solve(PARAMS, n, step)
        error = data.input_J_m2-data.loss_J_m2-data.stored_J_m2
        rows.append(dict(sweep=sweep, elements=n, dt=step,
            peak_surface_K=data.surface_K.max(),
            peak_mean_K=data.mean_K.max(),
            relative_energy_residual=abs(error).max()/data.input_J_m2.max()))
        final = data
    summary = pd.DataFrame(rows)
    summary.to_csv(out / "refinement.csv",index=False)
    final.to_csv(out / "history.csv",index=False)
    fig, ax = plt.subplots(1,2,figsize=(9,3.2))
    ax[0].plot(final.time_s, final.surface_K-273.15,label="Heated surface")
    ax[0].plot(final.time_s, final.mean_K-273.15,label="Volume mean")
    ax[0].set(xlabel="Time (s)",ylabel="Temperature (degrees C)")
    ax[0].legend(frameon=False,fontsize=8)
    for col, name in [("input_J_m2","Input"),("loss_J_m2","Loss"),
                       ("stored_J_m2","Stored")]:
        ax[1].plot(final.time_s,final[col]/1e6,label=name)
    ax[1].set(xlabel="Time (s)",ylabel="Energy per face area (MJ/m2)")
    ax[1].legend(frameon=False,fontsize=8)
    for a in ax:
        a.spines[["top","right"]].set_visible(False)
        a.grid(alpha=0.15)
    fig.tight_layout();fig.savefig(out / "verification.pdf",bbox_inches="tight")
    plt.close(fig)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
