# AMENDMENT A1 to OUT-3 (SCALE-FREE BOUNDARY): the counter-theorem, corrected

**Status: post hoc with respect to `PREREGISTER.md`, ante hoc with respect to every number and to the
Lean certification. Nothing else changes: no threshold, no gate, no arm, no label rule.**

---

## What was wrong

`PREREGISTER.md` §3 item 8 stated:

> `fold_lambda_blind` — if instead the fold *rescaled* so that `u_f` were λ-invariant, all three arms
> would collapse to a flat direction (weights equal).

That is wrong for arm A. I wrote the weight of `N_f(F1)` as `−2 + d ln X/d ln u`, which holds only at
fixed `R_f`. When the fold responds, `R_f` contributes through two places: through `u_f` (which
carries `R_f²`) **and** through the `R_f³` in `ρ_c = 3 X M_b/(4π R_f³)`. I omitted the second.

## The corrected general weights

Let `s ≡ d ln X / d ln u` and `ρ ≡ d ln R_f / d ln a₀`. Then, holding `M_b, ρ_Λ, G, c` fixed:

```
w_F1 = -2 + s*(1 + 2ρ) - 3ρ      w_V1 = -2
w_F2 = -1 + s*(1 + 2ρ)           w_V2 = -1
w_F3 =      s*(1 + 2ρ)           w_V3 =  0
```

(`d ln u/d ln λ = 1 + 2ρ` at fixed `M_b`; the `−3ρ` is the `R_f³` I dropped.)

**Flat-direction conditions** (the arm is a flat direction when `w_F = w_V`):

| arm | condition on ρ | in the deep-field limit `s = 1/2` |
|---|---|---|
| **A** energy density | `s*(1+2ρ) = 3ρ` | `ρ = +1/4` |
| **B** column | `s*(1+2ρ) = 0` | `ρ = -1/2` |
| **C** share | `s*(1+2ρ) = 0` | `ρ = -1/2` |

So the corrected statement is: **arms B and C are flat directions iff `ρ = −1/2` (exactly, at every `u`,
since `s ≠ 0`) — my original claim holds for them — but arm A needs `ρ = +1/4`, not `ρ = −1/2`.**

Certified in `OUT3.lean` as `weight_gap_A/B/C`, `flat_BC_rho`, `flat_BC_only`, `flat_A_deep_iff`,
`dlnX_dlnu_pos`. The MUTATE twin makes `flat_BC_rho` assert `ρ = +1/2` and fails to compile
(`compile_MUTATE.txt`, error at line 280).

## Why the amendment does not move anything

- The **measured** value is `ρ = d ln R_f/d ln a₀ = 2.9e-3 dex/dex` (FINAL-18, log M_b 10.45, z = 0),
  i.e. `ρ ≈ 0`. Gate G2 as written asks only whether the gap `|w_F − w_V| ≥ 0.1`. At `ρ = 0` the gaps are
  `s` for all three arms (`0.503 … 0.517`), comfortably ≥ 0.1. The gate's verdict is unchanged.
- The roots `κ_A, κ_B, κ_C` are computed at the actual `R_f` and do not involve `ρ` at all. Every number
  in `out3.out` is unchanged.
- The **conclusion is unchanged and if anything sharpened**: the take is a real constraint, not a flat
  direction — and it is so for a *structural* reason that survives in all three slots, because the fold
  simply does not respond to `a₀` (`ρ ≈ 0`, whereas flatness needs `ρ = ±1/4` or `−1/2`).

## One consequence worth recording

The framework's symmetry statement (FRAMEWORK.md §2: "`G_λ` is an exact symmetry of the formation
equations and `κ` is the only quantity charged under it") and FINAL-16's "flat direction" are statements
about the *equations at fixed geometry*. The boundary condition is a statement about the *geometry at
fixed equations*. Those are different objects, and only the second is κ-charged in a way that can pin κ.
**This is the cleanest form of the OUT-3 negative: the condition is genuinely constraining (G2 PASS) and
genuinely wrong (G3/G4/G5 FAIL).** A flat direction would have been the more comfortable failure.
