# Editable COMSOL brake study

This newly authored Java source constructs a three-dimensional annular half-rotor, meshes it, runs a transient heat-transfer study for each material and saves the resulting models in the working directory. It requires a licensed COMSOL installation with Heat Transfer in Solids and a compatible Java compiler. The builder targets COMSOL 6.x and has not been compiled or solved in the portfolio build environment.

From a writable directory containing the Java file, use the COMSOL launcher on Linux or macOS.

```sh
comsol compile DiscBrakeStudy.java
comsol batch -inputfile DiscBrakeStudy.class
```

On Windows use the installation's COMSOL Compile and COMSOL Batch launchers. The expected files after a successful solve are `disc-brake-iron.mph` and `disc-brake-sic.mph`. The source creates fresh illustrative models. The original academic MPH file and its exact settings were unavailable.

## Model definition and checks

The bore and outside radii are 55 and 145 mm. The simulated thickness is 10 mm with symmetry at the rotor midplane. A radial heat flux proportional to radius approximates uniform pad pressure and sliding speed proportional to radius, averaged over angle. Peak flux is 600 kW/m² at the arithmetic mean radius. Heat input decays linearly over four seconds. Convection and radiation act on the rubbing face throughout a 30-second study. The radial edges are insulated.

Compare peak face temperatures and the radial temperature gradient between materials. The 1D Python companion uses spatially uniform flux. To compare it directly with COMSOL, remove the radial multiplier from the Java flux expression before compiling. Refine the mesh and decrease the maximum solver time step independently until peak temperature stabilises. The output time list specifies report times, not a guaranteed internal solver step.

[COMSOL compile instructions](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_running.38.09.html) · [Batch execution](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_running.38.08.html)
