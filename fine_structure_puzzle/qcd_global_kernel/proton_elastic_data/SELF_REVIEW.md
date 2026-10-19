# Author self-review

2026-10-19. Independent review is not implied.

- Authenticated version v2, 27 August 2019, exact source archive, Table VI TeX and PDF page26. The numerical points are source entries, not digitization of figure bands.
- Excluded the Q=0 row with unavailable magnetic form factor. No extrapolated magnetic moment or fitted radius is inserted.
- Used the source's common mass scale consistently with Q² units and disclosed its empirical nucleon-mass calibration. This does not establish a fixed-MSbar QCD+QED mass path.
- Distinguished dynamical heavy flavors from heavy-current insertions. Only the source's included light-current sector is claimed.
- Imported published point extraction and current normalization, including its source fits, while excluding Q² ansatz fits from this calculation.
- Checked every point's complete Born value against dispersive elastic plus Born subtraction. Neither the subtraction nor non-pole Dirac term is dropped.
- Compared segment and nodal trapezoid implementations and their constant/linear invariants. This checks the finite functional, not a bound on between-point curvature or continuum error.
- Computed the worst admissible covariance ceiling only for the linearized error at fixed printed masses/momenta. Missing covariance is not replaced by independence; nonlinear mean/variance and total physical error remain unknown.
- Source central values and all executed inputs are frozen. No number is calibrated to alpha or a cosmic target. The older proton_kernel package remains untouched.

Outcome: **implementation and finite assertion verified in the stated source-data range**, conditional on the published lattice extraction and explicit scale/current conventions. Full physical proton response and global vacuum ratio remain unresolved.
