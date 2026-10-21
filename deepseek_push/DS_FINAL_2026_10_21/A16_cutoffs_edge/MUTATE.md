# A16 — mutations

Two mutations, both run with `--mutate <name>`. Each changes **one premise** and must break exactly
the check that tests that premise. Both exit 1 by design; the unmutated run is `21/21 checks PASS`,
exit 0. Captured runs: `a16_MUTATE_gamma.out`, `a16_MUTATE_units.out`.

    python3 a16_checks.py --mutate gamma    ->  K2 FAIL   (exit 1)
    python3 a16_checks.py --mutate units    ->  K8 FAIL   (exit 1)

## M1 — `--mutate gamma`: replace the `Gamma = 2` polytrope by `Gamma = 5/3`

The whole chain rests on one fact: `c_s^2 = 2 pi G L*^2 rho_c` is **linear** in density, so
`k_J = sqrt(2)/L*` is density-free (§1, K2). The mutation replaces the equation of state by
`e = A rho^Gamma` with `Gamma = 5/3`, which keeps `c_s^2 = dp/drho` a well-defined quantity (K1
still passes — it is a control, not the test) but makes the Jeans wavenumber density-dependent:

    Gamma = 2:    d ln k_J / d ln rho = 0        <- k_J = sqrt(2)/L*, one length
    Gamma = 5/3:  d ln k_J / d ln rho = 1/6      <- k_J ∝ rho^{1/6}, NOT one length

Captured (`a16_MUTATE_gamma.out`):

    MUTANT Gamma=5/3: c_s^2 = 10*A*rho**(2/3)/9
    K1   PASS residual 0   [threshold exactly 0]  MUTANT: species differ
      dispersion: omega^2/(4 pi G rho) = 5*A*k**2/(18*pi*G*rho**(1/3)) - 1
      MUTANT Gamma=5/3: d ln k_J / d ln rho = 1/6
    K2   FAIL dlnkJ/dlnrho = 0.166667   [threshold 0 for Gamma=2 (1/6 for Gamma=5/3)]  MUTANT: Gamma=5/3 breaks it
    ...
    A16 COMPLETE: 20/21 checks PASS.
    exit code 1

Teeth: K2 measures `0.166667 = 1/6` against a declared threshold of `0`. It is the check that
licenses the claim "one `L*` is one length", and the mutation shows a one-third-power change in the
polytrope index is detected. K3–K21 are unaffected because they are evaluated at `Gamma = 2` by
construction; only the EOS premise moves.

## M2 — `--mutate units`: reproduce A11 §14's `c_s` slip

A11 §14 computes `c_s^2 = 2 pi G L*^2 rho_c = 0.5191` in SI, which is **m^2/s^2**, and reports it as
`0.5191 c^2`, concluding `c_s = 0.72 c`. The mutation reproduces that arithmetic exactly — it
reports the m/s value as if it were in units of `c`:

    c_s/c  =  sqrt(0.519081) = 0.720473     instead of     0.720473 / c = 2.4032e-9

Captured (`a16_MUTATE_units.out`):

    K8   FAIL c_s/c = 7.2047e-01   [threshold < 1e-6]  MUTANT: unit slip reproduces A11's 0.72
    ...
    A16 COMPLETE: 20/21 checks PASS.
    exit code 1

Teeth: K8 compares `c_s/c` against `1e-6`. The mutant lands on `7.2047e-01`, which is A11's `0.72`
to three digits — the mutation *is* the published error, and it is caught by 6 decades. This is the
check that decides whether the pressure must be switched off inside halos at all; §6 of the report
and Tasks 3–4 depend on it.

## What is not mutated, and why

- The SPARC edge (K12–K17) is a data check with no free premise to mutate; its sensitivity is
  quantified instead, in-lane, by the `Upsilon_d = 0.7` run (`N > 9.829`) and by the `M_b` inflation
  scan (`1.33x` clears the `N = 8.296` violation). A mutation of the census table would only show
  that a different table gives a different `N`, which is already A11's finding.
- `K6` is a reproduction of an external computation (AG6D's growth ODE). Its control is the 1 %
  agreement with `k_1/2 = 0.980`; there is no premise to flip that would not simply re-derive the
  same ODE.
