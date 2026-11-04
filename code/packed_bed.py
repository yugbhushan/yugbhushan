"""Compare particle shape and illustrate wall channeling in a packed bed."""
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from common import options, plt, save_plot


def coefficients(voidage, sphericity, diameter, viscosity, density):
    """Return A, B for pressure gradient A*u + B*u² in SI units."""
    if not 0 < sphericity <= 1 or not np.all((0 < voidage) & (voidage < 1)):
        raise ValueError("Sphericity must be in (0,1] and voidage in (0,1).")
    if min(diameter, viscosity, density) <= 0:
        raise ValueError("Particle diameter and fluid properties must be positive.")
    effective_diameter = diameter*sphericity
    a = 150*viscosity*(1-voidage)**2/(effective_diameter**2*voidage**3)
    b = 1.75*density*(1-voidage)/(effective_diameter*voidage**3)
    return a, b


def main():
    args = options("packed-bed")
    velocity = np.linspace(0, 0.5, 101)
    properties = dict(diameter=0.003, viscosity=1.8e-5, density=1.2)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    table = {"superficial_velocity_ms": velocity}
    for shape in (1.0, 0.65):
        a, b = coefficients(0.4, shape, **properties)
        gradient = a*velocity + b*velocity**2
        table[f"gradient_phi_{shape}_Pa_m"] = gradient
        axes[0].plot(velocity, gradient, label=f"φ = {shape}")
    pd.DataFrame(table).to_csv(args.out/"pressure.csv", index=False)
    axes[0].set(xlabel="Superficial velocity (m/s)", ylabel="Pressure drop (Pa/m)", title="Uniform bed")
    axes[0].legend()

    # Independent annuli share one axial pressure gradient. The wall voidage
    # profile is a chosen sensitivity assumption, not a fitted correlation.
    radius = 0.03
    edges = np.linspace(0, radius, 101)
    radial = (edges[1:]+edges[:-1])/2
    weights = np.diff(edges**2)/radius**2
    eps = 0.4 + 0.18*np.exp(-(radius-radial)/properties["diameter"])
    a, b = coefficients(eps, 1.0, **properties)
    def local_velocity(gradient):
        return 2*gradient/(a+np.sqrt(a*a+4*b*gradient))
    target = 0.2
    upper = float(np.max(a*target+b*target**2))
    gradient = brentq(lambda g: weights @ local_velocity(g)-target, 0, upper)
    local = local_velocity(gradient)
    pd.DataFrame(dict(radius_m=radial, voidage=eps, velocity_ms=local,
                      area_fraction=weights)).to_csv(args.out/"wall.csv", index=False)
    axes[1].plot(radial/radius, local)
    axes[1].axhline(target, ls="--", color="gray", label="Specified mean")
    axes[1].set(xlabel="Radius / bed radius", ylabel="Local superficial velocity (m/s)", title="Wall sensitivity")
    axes[1].legend()
    save_plot(fig, args.out)
    i = np.argmin(abs(velocity-target))
    increase = 100*(table["gradient_phi_0.65_Pa_m"][i]/table["gradient_phi_1.0_Pa_m"][i]-1)
    pd.DataFrame([dict(target_velocity_ms=target, wall_gradient_Pa_m=gradient,
                       area_mean_ms=weights @ local, shape_increase_pct=increase)]).to_csv(args.out/"metrics.csv", index=False)


if __name__ == "__main__":
    main()
