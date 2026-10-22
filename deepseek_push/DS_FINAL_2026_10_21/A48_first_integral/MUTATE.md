# A48 — MUTATIONS

Five mutations, each of which must break at least one declared check. The base run is
`A48 COMPLETE: 25/25 checks PASS.` (exit 0, 12.5 s). Each mutation is a single, named, physically
meaningful change; the mutated run exits 1.

```
python3 a48_checks.py                     # A48 COMPLETE: 25/25 checks PASS.   exit 0
python3 a48_checks.py --mutate total      # 19/25                              exit 1
python3 a48_checks.py --mutate baryon     # 17/25                              exit 1
python3 a48_checks.py --mutate a0factor   # 22/25                              exit 1
python3 a48_checks.py --mutate exact      # 24/25                              exit 1
python3 a48_checks.py --mutate nocount    # 24/25                              exit 1
```

## 1. `--mutate total` — make total matter the *baryonic* branch

Swaps the two branches: branch B gets `g_N = 6.3643 G M_b/r^2` and branch T gets
`g_N = G M_b/r^2`. This is the mutation that matters, because it is the reading under audit —
if the code cannot tell "total matter" from "baryons only", the χ² table is not wired to the physics.

```
B3  FAIL  Delta chi2 (T-B), a0=9.3603e-11: +0.0  (0 sigma formal)      > 1000
B4  FAIL  Delta chi2 (T-B), a0=1.132e-10: +0.0  (0 sigma formal)       > 1000
B5  FAIL  T worse on both footings by 0.0 / 0.0                        both > 0
B8  FAIL  branch T: a0* = 8.080e-11, chi2* = 7114.3 ; Delta chi2* = +0.0   > 1000
B10 FAIL  galaxies where T beats B at fixed a0: 0 of 171               <= 20
A48 COMPLETE: 19/25 checks PASS.
```

The mutation does not just fail a bookkeeping check — it *inverts the verdict*. The branch that
wins the fit becomes the one with the cold sector in the source, which is the statement that the
2.523× excess is preferred by SPARC. It is not: the fit quality moves by 10⁴ in χ².

## 2. `--mutate baryon` — make the baryonic branch carry total matter

The mirror image: both branches use `6.3643 M_b`. This is the mutation that simulates the
*opposite* error to the one A40 made — reading the record's evidence as if every fit had already
used total matter.

```
B2  FAIL  branch B at a0=9.3603e-11: chi2 = 81835.81  (chi2/dof 25.54)   7259.38 +- 0.5
B7  FAIL  branch B: a0* = 2.6499e-12, chi2* = 17471.1                     a0* in (0.5,1.3)e-10
A48 COMPLETE: 17/25 checks PASS.
```

B2 is the anchor to the record: it is the only check that ties this lane's pipeline to a published
number (A7's 7259.38). Under the mutation the same pipeline returns 81 835.8, so the anchor is
doing real work — it fixes the *normalisation* of the source, not only its shape.

## 3. `--mutate a0factor` — use the brief's 2.523 instead of 6.3643

Uses `fac_a0 = 2.523` when computing the a0 that branch T would require. This is the arithmetic
error actually present in the lane brief ("a0 must be 2.523× smaller"), and the mutation shows it
is detectable: `a0` enters the deep-MOND amplitude as `sqrt(a0 g_N)`, so a source factor `1+M_c/M_b`
demands an `a0` factor `(1+M_c/M_b) = 6.3643`, not its square root.

```
C2  FAIL  branch T requires a0 = 4.4867e-11 (record) / 3.7100e-11 (canonical)  1.7787e-11 / 1.4707e-11
C3  FAIL  kappa: total matter 0.2398 / 0.1983                          < 0.12
C4  FAIL  Lambda at branch T's canonical a0 = 1.7130e-53 = Lambda_obs/6.36      < 0.03 Lambda_obs
A48 COMPLETE: 22/25 checks PASS.
```

The wrong factor understates the damage by 2.52×: it makes the counterfactual look like a 6.4×
Λ problem instead of a 40.5× one.

## 4. `--mutate exact` — assert that section 5's identity holds at all orders

Flips A5 from "the identity does not close beyond O(ε)" to "it must close". A33 §5 says the first
integral is "*exact* and not an expansion"; A5 tests that claim by solving the (L) and (P) equations
for `ρ` and `P″` and evaluating the residual of `(r²(g−u))′ − Kρr²` at a point where both equations
hold. The residual is 22 % of the terms.

```
A5  FAIL  all-orders residual / term = 0.221                           > 0.02
A48 COMPLETE: 24/25 checks PASS.
```

This is a *wording* defect, not a numerical one: at O(ε) the identity is exact (A2, A3) and every
galactic use is at O(ε). But §5's derivation invokes only (L) and (P); beyond leading order the
`f`-equation — which §5 does not use — would be needed. "Exact, not an expansion" is not supported
by the derivation offered.

## 5. `--mutate nocount` — remove the double count from the printed lapse source

Sets the difference between the printed source `ρ_b + ρ_c + ς(ρ_c−ρ̄_c)` and A33 §1's own partition
`ρ_b + (1−ς)ρ_c + ς(ρ_c−ρ̄_c)` to zero. This is the mutation that tests whether the audit's central
algebraic claim is actually computed.

```
A6  FAIL  S_printed - S_partition = 0                                  varsigma rho_c
A48 COMPLETE: 24/25 checks PASS.
```

The difference is `ςρ_c`: the charge's share of the cold density sits in `ρ_c` *and* in `d`. Only
`ς = 1` removes it, and at `ς = 1` the first integral's `M_src` is `M_b`, not `M_b + M_c`.

## What is *not* mutated, and why

- **The SPARC data and the error model.** External, frozen by A7's `FROZEN_CRITERIA.md`; the whole
  point of B1/B2 is that this lane reproduces A7's sample and total exactly. Mutating data to make a
  check fail would prove nothing.
- **`a₀`'s two footings.** They are a declared sensitivity (C1–C4, B2/B4), not a mutation: both
  footings give the same sign and the same order of magnitude for every Δχ². A mutation must break a
  check, and a factor-1.2 change in `a₀` does not.
- **The `M_c/M_b = 5.3643` value.** It is `Ω_c/Ω_b` from the CMB (A9/A11/A18), not a knob. Using a
  *larger* cold fraction (the catchment ratio `N = 5.364/f_ret`, up to 53.6) would make branch T
  worse by a further factor in mass, so 5.3643 is the most favourable case for the branch under
  audit; the exclusion is therefore conservative.
