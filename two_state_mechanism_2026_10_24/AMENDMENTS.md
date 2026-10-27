# Execution disclosures

The first static run revealed a factor-1000 error converting m/s^2 to
(km/s)^2/kpc. An independent SI length benchmark reproduced the error before
the fix. `model_v0_unit_error.py` and `run_static/` retain this rejected run;
its dimensional numerical results are invalid. The original dimensionless
dynamics does not use that conversion, but is rerun with the corrected source
for a consistent provenance record. Original manifests refer to the old hash
of model.py and are historical, not current validated evidence.

Before corrected execution, the chemical test radius is restricted to
min(original test radius, 0.8 reservoir radius). A chemical test beyond a
truncated T halo cannot convert existing T. Both radii and whether the finite
reservoir can supply the original test-radius law are reported. This narrows
TS3 to those explicit local points; it is not a full-halo phase-selection test.
TS1 free-mass limits are conditional on enough T being present to equilibrate.

The first dimensionless retention run failed the predeclared energy tolerance
in one coarse run (0.00841 > 0.005); the two bound-fraction resolution differences
were below 0.01. Timesteps are halved for the corrected run, retaining the
original output. No physical parameter or pass threshold is changed.

Continuation TS3b tests a concrete reversible rate closure on *frozen total
profiles*: Gamma_TF/Gamma_FT=exp((mean_mu(q)-epsilon)/theta). It has a common
nonnegative bath specific energy theta, not the observed baryon temperature.
The rate normalization remains unspecified. Desired q_dwarf<=0.1 and
q_disk>=0.95 are declared diagnostic thresholds, not fitted observational
limits. Compute the necessary epsilon interval analytically from endpoint
chemical potentials, then test representative stationary fractions. This
does not solve simultaneous mechanical and chemical equilibrium.
