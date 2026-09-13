# Exact exponential-kernel local trilemma

The exact primitive in the framework satisfies

```text
G'(y)/(2y) = 1-exp(-y),
G(y) = 2 y^3/3 - y^4/4 + y^5/15 - ... .
```

On a regular isotropic FLRW background `Ybar=0`, a perturbative spatial
gradient has `Y=epsilon^2 q`.  The MOND energy therefore begins at order
`epsilon^3`, and the linearized flux divided by `epsilon` tends exactly to
zero.  The exact exponential kernel supplies no quadratic MOND principal
symbol around the homogeneous state.

The three local repairs are mutually costly:

1. A local quadratic `cY` term shifts the constitutive law to
   `mu_eff(0)=c`; exact `mu(0)=0` forces `c=0`.
2. A nonzero background spatial gradient can produce a quadratic response, but
   a vector invariant under the 90-degree spatial rotation is exactly zero, so
   it is incompatible with isotropic FLRW.
3. A derivative-only local auxiliary multiplier has `P(0)=0`, giving
   `Lambda=-R/P` and an inverse-Laplacian IR pole for generic trace-free source.
   A finite local regulator produces `d=F R/P^2`; exact no-slip with nonzero
   source forces `F=0`, restoring the pole.

This is a conditional structural trilemma for local single-metric actions with
regular isotropic FLRW and the exact exponential constitutive law.  It is not a
universal no-go theorem for arbitrary nonlocal, multi-metric, or explicitly
anisotropic constructions.  It does show why the current routes keep cycling:
the kernel itself is nonlinear at the cosmological zero-field point, while the
usual repairs spend one of the required gates.

## Reproduction

```bash
python3 exponential_kernel_trilemma.py
python3 -m unittest discover -s . -p 'test_*.py'
python3 run_exponential_kernel_lean.py
```

The Python and unittest commands exit `0` when all symbolic identities and
limits are reproduced.  The Lean runner exits `0` for the exact algebraic
lemmas.  Neither executable is a universal proof beyond the stated scope.
