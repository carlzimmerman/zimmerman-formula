# Preserved failed numerical audit

`manifest.json` records status `failed`: the final cross-precision comparison
divided the 4D coupling derivative by its exact zero at the self-dual coupling
alpha_M=1/2. A residual 4.56e-121 at 120 decimal digits became exactly zero at
150 digits, making the erroneous relative-error comparison fail.

This was an implementation/audit-normalization failure, not a counterexample
to the physics. All within-precision derivative comparisons had passed using
the noncancelled stress scale. Minimal reproduction at r=1/2 gives rho=2.71944410718409,
d rho/d log alpha_M=4.56228986626569e-121 (120 digits), zero (150 digits).
The theta modular identity proves that derivative zero analytically.

The pre-fix script is preserved as `check_maxwell_at_failure.py`; its SHA-256
equals the original script hash in this run's manifest. The original manifest
refers to the then-current main script path; after correction that live path
changes, so `--root` intentionally reports that old live input stale. Do not
interpret this failed run as completed evidence. `run_002` uses the corrected
comparison and adds explicit self-duality controls.
