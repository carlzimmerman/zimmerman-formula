# C6P_cassini_high_precision: v3s's Solar-System gate is a clean PASS on both footings. C6's failed check C2 clears at 30, 50 and 80 digits and under an analytic rewrite, and the two methods agree to 3e-20

**Owner 11-04:** "Yes, rerun C6", under the 11-04 lift. **This test adopts nothing. The 10-24 v3s verdict stands unless the
owner changes it**: v3s passes as a galaxy-scale law and fails as gravity plus cosmology (clusters, growth/CMB, radiation
era, hosted dwarfs, MW disc). Those failures are outside this gate and stay open. **Not blind**: C6's numbers and AX1's
grades were seen first. κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not theory
closed. Nothing here says the data favour the framework. No file under `covariant_push_2026_10_22/` was edited; C6's code
is imported read-only.

- Criteria: `FROZEN_CRITERIA.md`, committed alone first (3da94262c4).
- Script: `c6p_cassini_hp.py`.
- Outputs: `c6p_cassini_hp.{json,out}`, the rerun `*_RERUN.*` (byte-identical, SHA-256 in Checks) and the twin `*_MUTATE.*`.
- Compute: 20 min, one thread, 0.49 GB peak RSS, no downloads.

## Labels (frozen rule): canonical **PASS**, alt **PASS**. Checks 9/9

| footing | G2a Cassini Q2 (24 cells) | G2b planets (worst) | G2c γ − 1 |
|---|---|---|---|
| canonical | 1.96e-36 to 1.86e-34 s⁻²; ≥ 4.85e7 inside Hees 9.0e-27, ≥ 2.80e7 inside Park 5.2e-27 | Mars 0.173 of bound at 24 pc (Saturn 0.035, Earth 0.028); 0.012 at 90 pc | γ = 1 (record X15/A22); proxy \|γ − 1\| ≤ 9.9e-12 at 24 pc, band [−2.5e-5, 6.7e-5] |
| alt | 1.76e-36 to 1.58e-34 s⁻²; ≥ 5.70e7 (Hees), ≥ 3.30e7 (Park) | same: the hedgehog GM/L★² does not depend on a0 | same |

- **Q2 per L★, max over E0–E3, divided by the Hees line:** canonical 2.06e-8 at 24 pc, 2.28e-9 at 50 pc and 3.91e-10 at
  90 pc; alt 1.75e-8, 1.94e-9 and 3.33e-10.
- **Planets:** the hedgehog GM/L★² and C6's Route F monopole agree to four digits in every cell.
- **Wide binary** (1.5 M☉ at 20 kAU; reported, not graded, as in C6): γ_v − 1 = 8.1e-6 at 24 pc, 1.9e-6 at 50 pc and
  5.8e-7 at 90 pc.
- **The γ proxy is a bound, not a PPN derivation.** It is 2(r/L★)² at r = 11 AU, the hedgehog potential (GM/L★²)r over
  GM/r. Its pass rests with the structural γ = 1 carried from X15.
- **The exact footings move Q2 by under 0.6 % from C6's** (C6 ran at 9.36e-11 and 1.13e-10). Method B at 50 digits
  reproduces C6's 24 recorded R1 cells to 7.5e-10, which is C6's own quadrature error.

## What cancelled, and how it was removed

- **The failed check.** C6's C2 had one failing sub-item: the isolated (x_e = 0) ratio of its general 2×2 kernel
  `chi_gen` at r_F = 0 over r_F = 1. In float64 it came out 3.77e-11 against the < 1e-12 line. Check H3 reproduces that
  value exactly (rel 0) and locates the error.
  - Almost all of it sits in the **r_F = 0 general kernel at large κ**: 3.77e-11 at κ = 794, c = −0.6.
  - The r_F = 1 kernel errs by 5.4e-12.
- **The mechanism.** With J = I and β = κ²/2 − 1:
  - A_xx = 1 + βs², A_zz = 1 + βc², A_xz = βsc;
  - det = (1 + βs²)(1 + βc²) − β²s²c² = 1 + β = κ²/2.
  - So the β²s²c² ≈ κ⁴/16 terms cancel, and det is formed from numbers ~κ²/8 larger than itself. At κ ≈ 800 that loses
    about 5 digits of float64.
- **Two diagnoses on record were off.** C6's AMENDMENT 1 called the failure (κ²/2 + 1) − 1 at κ = 0.01, and this lane's
  frozen diagnosis followed it. Both had the location wrong; the failure is the κ⁴ cancellation at large κ. The C6 README
  is left as recorded. This is the correction.
- **Method A (high precision).** The literal C6 and D7d formulas were run in mpmath at 30, 50 and 80 digits. All four
  C2 sub-items come out at 3.6e-26, 5.2e-46 and 4.1e-76.
- **Method B (analytic rewrite, no subtraction).** Every term is non-negative:
  - r_F = 0: χ = (1 + xs²)/[x(1 + x + c²) + q(1 + xs²)];
  - r_F = 1: χ = (q + 1 + x + bs²)/[(q + x)(q + 1 + x) + b(q + x + c²)], with b = x(1 + x).
  - In float64, all four C2 sub-items come out at ≤ 2.7e-15.
  - The κ-integral is also closed: I2 = −(5π/√2)∫₋₁¹ P₂ √(x(1 + x + c²)/(1 + x(1 − c²))) dc (sympy, H1).
- **The two methods agree.** Method A's nested quadrature of the literal r_F = 0 kernel agrees with Method B to 3.1e-20
  (8 fields × 3 precisions).
- **The cancellation never reached Q2.** C6's Route F integrals already used the closed form m/(1 − m + κ²m/2), which
  has no large-κ cancellation. The cancellation lived only in the C2 validation comparison. C6's Q2 numbers stand to
  7.5e-10.

## Checks (9/9 PASS; exit 0)

| check | result |
|---|---|
| H1 | sympy: B equals the general kernel at r_F = 0 and r_F = 1; the 1/m − 1 factorisation; κ²χ − 2; the κ integral. All residuals 0 |
| H2 | C2 rerun, C6's line < 1e-12 unchanged. Method A 3.6e-26 / 5.2e-46 / 4.1e-76 (30/50/80 digits); Method B float64 2.7e-15 |
| H3 | C6's float 3.7665e-11 reproduced (rel 0); float error vs 80 digits 3.8e-11 (r_F = 0, κ = 794) and 5.4e-12 (r_F = 1) |
| H4 | C6 float where nothing cancels: C2's other three items exact (Δ = 0); 24 R1 Q2 exact; R2 planet ratios exact; Method B 50 digits vs C6 R1 7.5e-10 |
| H5 | plain QUMOND law Q2 vs D7c `L` (PAPER58's QUMOND number), 8 cells: 3.84e-6 (≤ 1e-2) |
| H6 | Method A = Method B: 3.1e-20 (≤ 1e-14) |
| H7 | ladder: B 30/50 vs 80 digits 2.2e-31 (≤ 1e-25); A 1.5e-25 (≤ 1e-14); C2 max falls 1e-26 → 1e-46 → 1e-76 |
| H8 | E0 field g_e recomputed at C6's a0 = D7b (rel 0) |
| H9 | AX1 V1: hedgehog Mars 0.1728 at 24 pc (rel 9e-4 to 0.173) |

- **MUTATE twin (ν ≡ 1):** A_law ≡ 0 and J = I. H4 and H5 fail, and every screened Q2 is exactly 0. Exit 1. The twin
  skips the Method A ladder, which the mutation does not touch.
- **Byte-identical rerun:** `c6p_cassini_hp.json` and `c6p_cassini_hp_RERUN.json` share SHA-256 b6c21df3…87e9f, and the `.out` files share 820a5404…b0d.

## Carried, not rerun

- **C6's other checks.** C1 and C3–C8 are carried from C6 as it recorded them. This includes C6's own note that its check
  C6 passed on an unconverged Λ = 0.01 r_M solve (weak). That solve sits below the physical window L★ ≫ r_M and does
  not enter this gate.
- **Scope.** The result is O(ε), static, in a uniform Galactic field, with no ephemeris refit.
- **v3s's place.** With this, v3s is the only AX1 class with a clean PASS on the Solar-System gate on both footings.
  Nothing else changes: G5 (a0 by hand) and the 10-24 cosmology and cluster failures stand.
