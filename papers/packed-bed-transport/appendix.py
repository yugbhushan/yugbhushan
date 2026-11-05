"""Transcription of Appendix A, printed page 25, of the supplied term paper.

Authors: Parikshit, Shrish Kumar, Yug Bhushan.
Only whitespace/line wraps are normalized. The printed plotting code is omitted.
The radial expression is reproduced for traceability; it can yield negative
porosity and must not be used as a validated physical input.
"""
import numpy as np
import matplotlib.pyplot as plt

# Parameters for Analysis
rho = 1000
mu = 0.001
dp = 0.005
eps_inf = 0.4
L = 1.0

# Superficial velocity range for Ergun Analysis
v0 = np.linspace(0.001, 0.2, 100)


def compute_ergun(v, epsilon, diameter):
    term1 = 150 * mu * v * (1 - epsilon)**2 / (diameter**2 * epsilon**3)
    term2 = 1.75 * rho * v**2 * (1 - epsilon) / (diameter * epsilon**3)
    return (term1 + term2) * L


# Generate Data for Porosity Sensitivity
p_035 = compute_ergun(v0, 0.35, dp)
p_040 = compute_ergun(v0, 0.40, dp)
p_045 = compute_ergun(v0, 0.45, dp)

# Radial Porosity Model (Benenati-Brosilow), as printed
y_dp = np.linspace(0, 5, 500)
A, B = 0.7, 2.0
eps_radial = eps_inf + (1 - eps_inf) * np.exp(-A * y_dp) * np.cos(B * np.pi * y_dp)

# Plotting scripts omitted for brevity ... (Include full plotting code here)
