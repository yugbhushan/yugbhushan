# Packed-bed momentum transport

[Download the standalone source ZIP](packed-bed-transport.zip) · [Open the editable notebook](packed_bed.ipynb)

Extract the ZIP, install dependencies from requirements.txt, and run the script from the extracted directory.

```sh
python -m pip install -r requirements.txt
python packed_bed.py
```

To use the notebook, open it in Jupyter with the same Python environment and run all cells. If needed, install JupyterLab separately.

## Engineering question

How do particle shape and wall channeling affect pressure drop and flow distribution in a packed bed?

## Modelling approach

| Component | Approach |
| :--- | :--- |
| Governing model | Ergun equation, connected to a shell momentum balance |
| Particle shape | Sphericity-based extension for non-spherical particles |
| Implementation | Python pressure-drop model |
| Wall effects | Benenati–Brosilow correlation |

## Original project work

1. Derived the pressure-drop relation from a shell momentum balance.
2. Extended the model to account for particle sphericity.
3. Compared crushed catalyst particles with spherical beads.
4. Modelled wall channeling and proposed packed-bed design guidelines.

## Reported comparison

Crushed catalyst at a sphericity of **0.65** produced approximately **190% higher pressure drop per unit length** than spherical beads under the studied conditions.

This percentage describes the specific model comparison; it is not a general result for every bed geometry or flow regime.

## Engineering relevance

The analysis brings particle geometry and near-wall flow into the assessment of packed-bed resistance and design.

## Reproducible implementation

### Run the pressure-drop study


```sh
python packed_bed.py
```

The uniform-bed example evaluates the positive pressure-loss gradient $G=A U+B U^2$, where $U$ is superficial velocity. With void fraction $\varepsilon$, volume-equivalent diameter $d$, and sphericity $\phi$, the solver uses

$$ A=\frac{150\mu(1-\varepsilon)^2}{(\phi d)^2\varepsilon^3}, \qquad B=\frac{1.75\rho(1-\varepsilon)}{\phi d\varepsilon^3}. $$

The linear term represents viscous resistance and the quadratic term represents inertial resistance. The force balance gives the pressure-loss structure. The numerical coefficients are empirical Ergun coefficients.

| Example input | Value |
| --- | --- |
| Diameter and bulk void fraction | 3 mm and 0.40 |
| Fluid density and viscosity | 1.2 kg/m³ and 0.000018 Pa·s |
| Superficial velocity | 0–0.5 m/s |
| Shape comparison | Sphericities 1.0 and 0.65 |

At 0.2 m/s, changing only the shape factor increases pressure drop by **100.44%**. With the other inputs held fixed, the pressure ratio lies between $1/\phi$ and $1/\phi^2$. For $\phi=0.65$, even the viscous limit is about a 137% increase. The historical 190% increase therefore needs additional original inputs, such as a difference in void fraction or equivalent diameter, or a different model or comparison definition.

### Wall sensitivity

A second calculation divides a 30 mm radius bed into 100 annuli. Voidage rises towards the wall according to the illustrative profile $0.4+0.18\exp[-(R-r)/d]$. For a candidate common gradient, the solver finds each annulus's local velocity and uses its area as a weight. A scalar root solve chooses the gradient that recovers the specified mean velocity. The example yields **419.73 Pa/m** at 0.2 m/s. Higher local voidage permits more flow near the wall.


The original project used the Benenati–Brosilow correlation. The executable wall example is a separate sensitivity study with an explicitly chosen voidage profile. Direct comparison to the original requires its radial correlation parameters and particle and fluid properties.
