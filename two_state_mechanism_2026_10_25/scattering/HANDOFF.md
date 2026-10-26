# Continue from the actual missing amplitudes

Completed: two-electron finite-basis neutral singlet/triplet and anion energies;
neutral J0 nuclear spectrum at M/m100; collision scaling and finite-rate adapter;
conservation/detailed-balance/photon integration checks. See README/AUDIT.

Not completed: physical finite collision rates or new physical halo trajectories.
Do not present manufactured single-block unit loss as a rate calculation.
Do not infer a DR amplitude from FCI bound energies or Sommerfeld enhancement.

Next physical requirement: choose and converge a Coulomb-matched two-electron
continuum/R-matrix calculation, spin-resolved, with neutral valence/resonance
channels, then nuclear frame transformation at M/m100 (not ordinary-H mass).
Check open-channel unitarity, electronic and nuclear basis refinement, energy
resolution across resonances, partial-wave convergence and product branching.
Only then populate coupling.py with actual per-level rates and use the shared
four profiles. Include neutral molecule/negative-ion branches and consistent
finite-mass energies rather than claiming the retained species are closed.

Current coupling uses prior leadingBO thermochemistry for exact compatibility.
The finite-mass detailed-balance factor and atomic energy differ; DERIVATION.md
lists this correction explicitly. Applying it alone would make the old photon
and new collision equilibrium inconsistent.

Original goal (repulsive tethering, live gravity/rotation, dwarf/cluster free
mass and acceleration relation) remains unachieved. Charged molecular fraction
is not an orbital tethering observable. Keep existing limitations visible.
