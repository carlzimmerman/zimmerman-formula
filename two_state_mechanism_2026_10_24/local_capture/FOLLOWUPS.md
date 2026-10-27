# Targeted v4 checks

Use profile 1 (100 million solar masses, scale 1 kpc), beta4, flat .25,
seed11 for all controls. This is a numerical/physical sensitivity sample,
not a parameter change assigned to that object's type in the population scan.

- Halve event interval to .01 initial dynamical time, tighten Hamiltonian
  energy budget tenfold and double field quadrature. Since trajectories are
  stochastic, a single pair does not estimate a weak convergence order.
- Halve both numerical softenings to .1b and double field quadrature.
- Disable baryonic cooling while retaining reversible conversion.
- Extend rotating and unordered histories to eight initial dynamical times.

Record every outcome. Do not treat a phase fraction that changes by one packet
as significant. These controls probe numerical/event sensitivity, cooling
dependence and accumulation over a longer window, not a cosmological lifetime.
