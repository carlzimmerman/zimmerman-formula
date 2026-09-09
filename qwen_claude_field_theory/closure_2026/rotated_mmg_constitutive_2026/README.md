# Rotated-MMG constitutive candidate

This is the next construction attempt after the affine-dust, G03, and
nonlocal routes.  It uses a Hamiltonian constraint to carry the exponential
constitutive law and an independent rotated slip constraint.  The scalar
constraint block is tested by actual Poisson brackets, with homogeneous and
local Fourier sectors separated.

Run the reproducible gates from this directory:

```text
python3 -B rmmg_constitutive_action.py
python3 -B -m unittest -v test_rmmg_constitutive_action.py
python3 -B spherical_prediction.py
python3 -B -m unittest -v test_spherical_prediction.py
python3 -B hda_closure_gate.py
python3 -B -m unittest -v test_hda_closure_gate.py
python3 -B sparc_exact_exponential_fit.py
python3 -B -m unittest -v test_sparc_exact_exponential_fit.py
python3 -B run_lean_core.py
```

The result is intentionally marked `OPEN`: the local constitutive/slip gate,
the exact exponential identity, and the separately counted clock witness pass;
the nonlinear hypersurface-deformation algebra, ordinary-matter Ward identity,
boosted PPN parameters, full FLRW perturbations, and the \(y\to0\) completion
still have to be derived from this same action.

The spherical script derives the first finite-acceleration correction to the
flat deep-MOND speed, \(v^2=\sqrt{G_bMa_0}+G_bM/(4r)+\cdots\), directly from
the exact exponential law.
