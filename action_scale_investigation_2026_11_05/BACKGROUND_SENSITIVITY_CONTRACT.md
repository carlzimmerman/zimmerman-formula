# Independent background sensitivity test

Frozen before execution. Retain all four diagnostic shells and the same
equations, boundaries, and physical parameters. Recompute the BVP from the
analytic seed with 400/800 initial nodes and tolerances 1e-9/1e-10; retain
2001 profile points instead of 201. This changes the background resolution
independently of the radial perturbation mesh. Maximum BVP nodes remains
10000. Existing sampled-domain and boundary gates remain unchanged.

Run the identical radial Hessian assembly on 320/640 cells for all four
new backgrounds. Require positive lowest five reported modes, backward
errors <=1e-8, scaled constraint condition <1e14, and <=2% change in the
lowest three modes across the new perturbation ladder. Compare each new
640-cell lowest-three spectrum with the corresponding old 640-cell result;
require <=0.5% change. The 0.5% gate is a separate background-sensitivity
gate, stricter than the existing 2% mesh gate. Retain failures without
retuning. Existing known-Laplacian and reversed-sign controls remain.

These are finite-box floating-point diagnostics with fixed endpoint B,p
perturbations. Passing cannot establish continuum positivity, physical
galaxy/cosmology matching, angular health, or the acceleration coefficient.
No claim of an independent implementation: independence here is only of
the newly solved background and its resolution. Preserve original scripts
and results. Use one numerical thread; no downloads.
