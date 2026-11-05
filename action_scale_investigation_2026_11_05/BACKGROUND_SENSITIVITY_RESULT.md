# Radial box results survive independent background refinement

All four cases pass the frozen BACKGROUND_SENSITIVITY_CONTRACT.md gates.
This resolves the particular concern that the previous low modes might
be artifacts of the 201-point background representation. It does not
resolve the other limitations of SPECTRUM_RESULT.md.

The new BVP solves use independent analytic seeds, initial meshes of
400/800 points, tolerances 1e-9/1e-10 and 2001 saved profile points. All
converge, with final finer meshes between4590 and6295 nodes. The maximum
scaled difference between the two new solutions is9.18e-12. No parameters
or boundary conditions were changed and no values were fitted.

| b | Lstar | Relative change of lowest3 at640 cells, old/new background | New320/640 relative change of lowest3 | Lowest omega squared at640 |
|---|---|---|---|---|
|0.1|1|6.66e-8|0.00878948|1.75155e-8|
|0.1|3|1.52e-7|0.0102446|3.67636e-8|
|0.3|1|9.37e-7|0.00714490|1.16449e-8|
|0.3|3|1.22e-7|0.0145155|2.63213e-8|

All reported lowest five modes are positive on both new perturbation
meshes. The background sensitivity is below1e-6 in relative units, much
smaller than the remaining perturbation-mesh error. Constraint and
eigenvalue backward-error gates pass, as do the known-Laplacian and
reversed-sign controls. The scaled constraint condition numbers remain
about3.2e10 to3.5e10; this is not an interval-certified spectral bound.

The test reuses the same Hessian assembly and static equations; it is
independent background refinement, not independent implementation review.
The endpoint perturbations remain fixed B,p in a finite artificial box.
There is no inference here about angular modes, nonlinear stability,
cosmological matching, or selection of b. Self-review only.

Evidence: evidence/shell_dense and evidence/spectrum_dense, with executed
inputs and outputs hashed in their manifests. The launch rejected before
execution when input pins were initially omitted; the recorded run includes
all executed project inputs. No scientific result was discarded.
