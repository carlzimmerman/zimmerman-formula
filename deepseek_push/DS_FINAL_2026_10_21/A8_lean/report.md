# A8 — Lean 4 + Mathlib certificates for the algebraic core

Lane: `deepseek_push/DS_FINAL_2026_10_21/A8_lean/`
Toolchain: Lean `v4.34.0-rc2`, Mathlib `v4.34.0-rc2`, existing built project
`fable_independent_2026/lean_2026` (reused, 8.1 GB `.lake`, nothing rebuilt, no
existing `.lean` file touched). Build: `cd <project> && lake env lean <lane>/<file>.lean`.

## Claim

The algebraic core of this push is certified, in Lean 4 with Mathlib, as **40
theorems with no `sorry`**, each with axiom footprint exactly
`[propext, Classical.choice, Quot.sound]` (machine-checked from the compiler
output, see `a8_lean_checks.out` K1–K2). Specifically: (C1) the kappa–Z identity
`(a0/(cH))^2 = kappa^2·3/(8pi)` from the two defining equations, with `kappa = 1/2`
giving `3/(32pi)` and, on the positive branch, `a0/(cH) = 1/(2 sqrt(8pi/3)) = 1/Z`;
(C2) the two closed forms are the *same real number* (`1/(2 sqrt(8pi/3)) =
sqrt(3/(32pi))`, `2 sqrt(32pi/3) = 2(2 sqrt(8pi/3)) = 2Z`) — identities in `pi`, not
numerical coincidences; (C3) each closed form satisfies its own law, the canonical
closed form is *the* positive root, and `g_q < g_c` **strictly for all `gN, a0 > 0`**;
(C4) `dg/dgN > 0` for both laws at every acceleration, with explicit derivative
formulas, plus strict monotonicity in `gN` and in `a0`; (C5) `mu = gN/g = x/(1+x)`
satisfies `0 < mu < 1` with `mu -> 0` at `x -> 0` and `mu -> 1` at `x -> atTop`.

Two corrections to the task statement, both proven rather than asserted:

1. **The ordering needs no extra hypothesis, and it is strict.** `g_q <= g_c` is
   true but weak: `g_q < g_c` holds for every `gN > 0`, `a0 > 0`, with the exact gap
   `g_c - g_q = a0 gN^2/(g_c(g_c + g_q))`. Equality is *never* attained; it is
   approached only asymptotically (both normalised laws tend to 1 in the deep limit,
   and the gap tends to 0 as `a0 -> 0+`). The reversed and the equality claims are
   in `A8_C3_MUTATE.lean` and **fail to compile**.
2. **"One twelfth of the horizon" is not an identity.** `1/12 < 1/(2Z) < 1/11` is
   proven (`Z = 5.788810036`), so `1/(2Z) = 0.086373537` is 3.65% *above* `1/12`; and
   `a0/(cH) = 1/Z = 0.172747075 = 2.073/12`. The exact statement is `1/Z`.

## Derivation

Symbols: `c` speed of light, `G` Newton's constant, `rho` the vacuum energy density,
`H` the expansion rate, `a0` the vacuum-tied acceleration scale, `kappa > 0` its
normalisation, `gN` the baryonic acceleration, `g` the total (observed)
acceleration, `Z := 2 sqrt(8 pi/3)`.

1. Vacuum-tied scale (definition, premise): `a0 = kappa c sqrt(G rho)`.
2. Flat, Lambda-only Friedmann equation (premise): `H^2 = 8 pi G rho/3`.
3. Squaring (1) gives `a0^2 = kappa^2 c^2 G rho` — `A8.a0_sq`.
4. Dividing (3) by `c^2 H^2` and inserting (2):
   `(a0/(cH))^2 = kappa^2 G rho / H^2 = kappa^2 · 3/(8 pi)` — `A8.kappa_Z_identity`
   (hypotheses `kappa, c, G, rho, H > 0`).
5. `kappa = 1/2`: `(a0/(cH))^2 = 3/(32 pi)` — `A8.kappa_half_sq`.
6. On the positive branch (`a0/(cH) > 0`, the physical one):
   `a0/(cH) = 1/(2 sqrt(8 pi/3)) = 1/Z` — `A8.a0_over_cH_eq_inv_two_sqrt`. The square
   in (5) alone gives `+-1/Z`; the sign hypothesis is stated, not hidden.
7. Closed-form identities: `1/(2 sqrt(8pi/3)) = sqrt(3/(32pi))`
   (`A8.inv_two_sqrt_eq_sqrt_ratio`) and `2 sqrt(32 pi/3) = 2 (2 sqrt(8 pi/3)) = 2Z`
   (`A8.two_sqrt_32pi_3`). Both are exact in `pi`.
8. `1/12 < 1/(2Z) < 1/11` (`A8.inv_twoZ_bracket`), using only `3 < pi < 3.14159265358979323847`;
   hence `1/(2Z) != 1/12` (`A8.inv_twoZ_ne_twelfth`).
9. Canonical law: `gN = g^2/(g + a0)`, solved: `g_c = (gN/2)(1 + sqrt(1 + 4 a0/gN))
   = gN/2 + sqrt(gN^2/4 + a0 gN)` (`A8.gCanon_form`). Then `g_c^2 = gN(g_c + a0)`
   (`A8.gCanon_root`) and any `g > 0` with that equation equals `g_c`
   (`A8.gCanon_root_unique`) — so `g_c` is *the* positive root.
10. `n = 2` law: `g^2 - gN^2 = a0 gN`, solved: `g_q = sqrt(gN^2 + a0 gN)`, and
    `g_q^2 = gN^2 + a0 gN` (`A8.gQuad_root`). Both laws exceed Newton
    (`A8.gCanon_gt_gN`, `A8.gQuad_gt_gN`).
11. Ordering: subtracting the two root equations gives
    `g_c^2 - g_q^2 = gN(g_c - gN)` (`A8.gCanon_sq_sub_gQuad_sq`); with `g_c > gN > 0`
    this is positive, so `g_q < g_c` (`A8.gQuad_lt_gCanon`) — unconditionally on
    `gN, a0 > 0`. Exact gap: `g_c - g_q = a0 gN^2/(g_c(g_c + g_q))`
    (`A8.gCanon_sub_gQuad_eq`), with `g_c - g_q <= gN` and `<= a0`
    (`A8.gCanon_sub_gQuad_le_gN`, `..._le_a0`).
12. Equality only in the limit: `g_c/sqrt(a0 gN) -> 1` and `g_q/sqrt(a0 gN) -> 1`
    as `gN/a0 -> 0+` (`A8.gCanon_normalised_tendsto`, `A8.gQuad_normalised_tendsto`),
    and `g_c - g_q -> 0` as `a0 -> 0+` at fixed `gN` (`A8.gap_tendsto_a0_zero`).
    Both are `Filter.Tendsto` statements at `nhdsWithin 0 (Set.Ioi 0)` and `atTop`.
13. Monotonicity: `d/dgN sqrt(gN^2 + a0 gN) = (2 gN + a0)/(2 sqrt(gN^2 + a0 gN))`
    (`A8.deriv_gQuad`) and `d/dgN g_c = 1/2 + (gN/2 + a0)/(2 sqrt(gN^2/4 + a0 gN))`
    (`A8.deriv_gCanon`); both `> 0` at every `gN > 0` (`A8.deriv_gQuad_pos`,
    `A8.deriv_gCanon_pos`), with strict monotonicity on `gN > 0`
    (`A8.gQuad_strictMonoOn`, `A8.gCanon_strictMonoOn`), strictly positive difference
    quotients on every interval (`A8.gQuad_slope_pos`, `A8.gCanon_slope_pos`), and
    strict increase in `a0` (`A8.gQuad_strictMonoOn_a0`, `A8.gCanon_strictMonoOn_a0`).
14. Capacity: on the canonical law `gN/g = g/(g + a0) = x/(1+x)` with `x = g/a0`
    (`A8.mu_eq_of_canonical`), so the boost is exactly `g/gN = 1 + a0/g`
    (`A8.boost_eq_one_add`); `0 < mu x < 1` (`A8.mu_pos`, `A8.mu_lt_one`),
    `mu -> 0` at `x -> 0` (`A8.mu_tendsto_zero`), `mu -> 1` at `x -> atTop`
    (`A8.mu_tendsto_one`).

## Status

**DERIVED** (algebra), with the premises listed above. `kappa = 1/2` is **FITTED**
(BRIEF section 1/4) and is only propagated, never derived, here. No new fitted
constant appears. The deliverables contain no numerical input into any proof: every
theorem is an implication, and the only `pi` input is `Real.pi`'s own definition plus
the bounds `3 < pi < 3.14159265358979323847` used for the 1/12 bracket.

An honesty note on (9)-(12): the ordering is a consequence of the two
root equations alone, so it certifies "these two *interpolations* are ordered", not
"the data prefer one". Nothing here distinguishes the laws empirically.

## Checks

`python3 a8_lean_checks.py` → `A8 COMPLETE: 8/8 checks PASS.` (exit 0); the exact
stdout is `a8_lean_checks.out`. Per-file compiler output is in `A8_*.out`.

| id | what it checks | measured |
|----|----------------|----------|
| K1 | all four certificate files compile with no error and no `sorryAx` | 4/4 clean |
| K2 | every theorem's `#print axioms` is exactly `[propext, Classical.choice, Quot.sound]` | 40/40 |
| K3 | no `sorry` token in the four sources (comment-stripped) | 4/4 |
| K4 | `A8_C3_MUTATE.lean` is rejected (`error`, `EXIT=1`, `linarith failed`) | rejected |
| K5 | `11 < 2Z < 12` and `1/12 < 1/(2Z) < 1/11`, with `1/(2Z)` 3.648% above `1/12` | `2Z = 11.577620` |
| K6 | `a0/(c H_Lambda)` from BRIEF constants equals `1/Z` to machine precision (with `H0` instead it is `0.1428`, so the check has teeth) | rel. diff 0.0 |
| K7 | ordering witness `gN = a0 = 1`: `g_q = 1.414214 < g_c = 1.618034`, gap `0.203820 <= min(gN,a0)` | pass |
| K8 | deep limit: `|g/sqrt(a0 gN) - 1|` at `gN/a0 = 1e-8, 1e-10` | `5.0e-5` (canon), `5.0e-9` (n=2) |

`python3 a8_lean_checks.py --mutate` (asserts the false `1/12` identity) → **K5 FAIL**,
`7/8`, exit 1: `a8_lean_checks_MUTATE.out`. That is the check's teeth.

Numbers (all in `a8_results.json → numbers`, all computed from exact formulas):
`Z = 5.788810036`, `2Z = 11.577620073`, `1/Z = 0.172747075`, `1/(2Z) = 0.086373537`,
`3/(32pi) = 0.029841552`, `H_Lambda = c sqrt(Lambda/3) = 1.806234e-18 1/s`,
`a0 = kappa c sqrt(G rho_Lambda) = 9.354173e-11 m/s^2` (BRIEF quotes `9.36e-11`, 6.2e-4
relative), `a0/(c H_Lambda) = 0.172747075 = 1/Z`.

Two numerical facts worth stating and *not* over-reading:

* The identity of C1 holds with `H_Lambda = c sqrt(Lambda/3) = 1.806234e-18 1/s`
  (55.8 km/s/Mpc), **not** with the measured `H0 = 67.4 km/s/Mpc`: with `H0` the ratio
  is `0.142847`, not `1/Z`. The Lean theorem is agnostic (it takes any `H > 0`
  satisfying the Lambda-only Friedmann equation); the number `0.172747` is the
  `H_Lambda` number.
* The approach to the deep limit is *not* linear in `gN/a0`: numerically
  `g_c/sqrt(a0 gN) - 1 ≈ sqrt(gN/a0)/2` while `g_q/sqrt(a0 gN) - 1 ≈ (gN/a0)/2`.
  The canonical law converges more slowly; the `Tendsto` theorems certify convergence,
  **not** these rates.

## What this does not do

* No numerical value of `G`, `H`, `rho` or `a0` is certified: no theorem mentions one.
  The only decimal literal anywhere in the lane is the `pi` bound
  `3.14159265358979323847` in `inv_twoZ_bracket`. `G`, `Lambda`, `H0`, `a0_can` appear
  only in the checks script, as labelled BRIEF inputs.
* No physics premise beyond the stated equations: `a0 = kappa c sqrt(G rho)`,
  `H^2 = 8 pi G rho/3`, and the two law definitions. In particular it does **not**
  certify that the vacuum-tied scale or the Friedmann equation are the right physics.
* `kappa = 1/2` is not derived; nothing here derives the integer `n = 1/kappa = 2`.
* It does not certify that `a0/(cH)` is "one twelfth of the horizon" — the opposite is
  proven (`1/12 < 1/(2Z) < 1/11`).
* It does not certify that the canonical law is the physically correct one, nor that
  the `n = 2` law is excluded; no galaxy, rotation-curve, RAR or fit statement.
* C4 is monotonicity of the algebraic map `gN -> g`; it is **not** a dynamical
  (perturbation) stability statement about any field equation.
* The "capacity `a0` vs `a0/2`" reading is not certified — only `mu = gN/g = x/(1+x)`,
  its bounds and its two limits. The integral `int (1 - mu) dg` is not computed here.
* The `n = 2` law's `mu` is not analysed (it is a different function of `x`).
* No statement about the strong-field turn-off `nu_fix`, the `a0/2` Solar-System tail,
  or `Lambda/a0^2 ≈ (pi/4) y_t`.

## Next

1. If the "twelfth" is to be claimed, the thing to derive is `n = 1/kappa = 2`
   (BRIEF section 1), not `8 pi/3`; the Lean lane can host that as a separate
   certificate once a candidate derivation exists.
2. The "capacity `a0` vs `a0/2`" reading is not a statement about `mu` at all: for the
   canonical law `1 - mu = a0/(g + a0)`, so `int_0^inf (1 - mu) dg` diverges
   logarithmically and no finite "capacity" follows from `mu`. Any capacity claim needs
   a different, explicitly stated functional (a sum rule for the interpolation), which
   must be written down before it can be certified.
3. The gap rate (`~sqrt(gN/a0)/2` vs `~(gN/a0)/2`) is numerically clear; certifying the
   asymptotic constants needs `IsEquivalent`/`Asymptotics` lemmas and is a small,
   well-scoped follow-up.

## Files

`A8_C1_C2_kappa_Z.lean` (9 theorems), `A8_C3_law_ordering.lean` (14),
`A8_C4_monotonicity.lean` (11), `A8_C5_capacity.lean` (6), each with a `.out` build log;
`A8_C3_MUTATE.lean` + `A8_C3_MUTATE.out` (must fail); `a8_lean_checks.py` +
`a8_lean_checks.out` + `a8_lean_checks_MUTATE.out`; `a8_results.json`;
`make_results.py`; `MUTATE.md`; this report.
