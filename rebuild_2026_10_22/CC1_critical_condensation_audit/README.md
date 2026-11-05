# CC1_critical_condensation_audit

**Question.** An outside specification ("PAPER65 critical condensation") proposes that a cold dark energy halo condenses only where η Σ_coll(M) ≥ Σ_a0, the a₀ law applies below, and the threshold is parameter-free. It supplies Lean certificates, a Python harness and a kSZ stop rule. Criteria: `FROZEN_CRITERIA.md` (0df57bfd91, committed alone before the stack ran). Not blind: the spec's arithmetic and the record's tables were read first.

## Verdict

- **Part A, BRACKET FAILS.** The crossing lands in (10¹², 10¹³) only for a constant η. With the record's own mass-dependent η, 10¹² is already super-critical on canonical in every row except c_f 4.
- **Not new: this is CSM1's selector.** CSM1 already compared the unfloored collapse column with its own floor, using the same equation. At L 3.75 the crossover is 11.22, and lensing fails (+415). The refit that puts T at 12.3 fails canonical groups (Z +2.62).
- **Part B: the spec's Tier 2 has the wrong sign** in the ordinary cases.
- **Part C: EXTENDED GAS BELOW NEED** at all three R, but on the cached upper part of the corrected bin only. **The extent lock fires:** A(1) + 1.96e < 1 too, so this stack does not show that k = 1 is free of tension.

## Part A: the threshold on the record's tables (`cc1_parts.py`)

Constant η reproduces the spec's numbers. log M_crit, canonical / alt:

| η | canonical | alt |
|---|---|---|
| 10.82 | 12.66 | 13.00 |
| 12.10 | 12.46 | 12.80 |
| 14.30 | 12.16 | 12.50 |

The alt margin at c_f 4 is 0.13 % (10.82 × 11.95 = 129.30 against 129.13).

Mass-dependent η (ARGON_BRIEF_2026-10-30 table 3a). Crossing, canonical / alt, and η Σ_coll at 10¹² against Σ_a0 = 106.85 / 129.13:

| Table | η Σ_coll(10¹²) | Crossing (canonical / alt) |
|---|---|---|
| X73 c_f 4 | 74.0 | 12.66 / 13.00 |
| X77 | 142.5 | 11.50 / 11.83 |
| CE1 converged | 177.4 | 11.13 / 11.45 |
| SH1 R 0.685 | 121.5 | 11.78 / 12.27 |
| CL5 stipulated | 145.0 | 11.47 / 11.80 |

The spec's η 14.3 and 12.1 are those tables' 10¹³ values, applied at 10¹². Taken at their own 10¹² values, the same tables put the Milky Way, the L★ analogs and KiDS bins 3–4 on the halo branch. That is CSM1's +415 lensing failure.

The spec counts the following as passes. The record has them as failures:
- **Milky Way.** HO2 already graded the Milky Way on the law branch: the box is INFEASIBLE (0/175 cells), and McMillan gives K_z z +12.0 / +14.1.
- **LS1 at 200–250.** ΔV −12.5 is still short there. At 150–200 the law gives Υ 0.44 and fails, and at 250–400 it gives −40.0.
- **Alt.** Alt fails SPARC on the law itself (X78, Υ 0.44).

## Part B: Tier 2 (×264/194)

The estimator is −Σw T u / Σw u². If v_rec = α v_true + noise, the true correction to A is (α_m/α_d)(σ_d/σ_m)². A Monte Carlo with 2 × 10⁶ draws matches the closed form to 1e-3:

| Case | Correction to A |
|---|---|
| Same α, less noise (r_data ≈ 1) | ×0.557 |
| Pure rescale (r_data 0.756) | ×0.735 |

The spec's ×1.361 holds only if r_data ≈ 0.41, against the mock's 0.756. GH8 does not measure that. Rescaling by rms alone lowers A; it does not raise it.

## Part C: the type-corrected stack (`cc1_stack.py`)

The corrected mass is lm + 0.14 for passive lenses and lm + 0.31 for star-forming ones, in the bin [10.5, 11.0]. The cached CAPs start at CIGALE 10.6, so the cut keeps passive lenses at 10.60–10.86 and star-forming ones at 10.60–10.69. That gives N 157,826 (123,641 passive, 34,185 star-forming). The model is GH9's build() at D = −0.14 / −0.31 by type.

A ± e (95 % limit), R fm. R cut and R ctx agree within 0.03:

| Tier | A(1) | A(1.8) | A(3) |
|---|---|---|---|
| T1 raw | 0.02 ± 0.41 (0.82) | −0.04 ± 0.27 (0.49) | 0.14 ± 0.26 (0.65) |
| T2 ×264/194 (sign wrong, Part B) | 0.03 ± 0.56 (1.12) | −0.06 ± 0.37 (0.66) | 0.19 ± 0.36 (0.89) |
| T3 ÷ control 0.58 | 0.03 ± 0.71 (1.41) | −0.07 ± 0.47 (0.84) | 0.24 ± 0.46 (1.13) |

- **Class:** EXTENDED GAS BELOW NEED at fm, cut and ctx.
- **Extent lock:** T1 A(1) + 1.96e = 0.79–0.84 < 1 at every R. The shortfall is in the normalisation, as in GH9, not in the extent.
- **Checks:** K1, GH9 D1 A(1.8) 0.2372 reproduced; K2, v flip exact. Peak RSS was 0.70 GB.

## Lean and the harness

- **Lean.** The supplied file fails on Lean 4.34.0-rc2: `decide` gets stuck on `Rat`. With `decide +kernel` (`cc1_certs_kernel.lean`) it compiles. The certificates are rational comparisons of hand-copied numbers, which the brief's rule bars from use as physics certification. They certify nothing here.
- **Python harness.** It does not parse: the `p_exp` line is indented 5 spaces. Its scoreboard is hard-coded text, and the `if 1.82 >= 1.8` branch is always taken. Its numbers are recomputed in Parts A–C instead.

## CAP self-subtraction

The power-law factor 2 − 2^0.855 = 0.191 is correct. GH10_smooth_gas_taper tests the "3×" template bias with the real beam and lenses. That lane is the reference for it, not this one.

κ = ½ FITTED; c_f EXTERNAL; core shape empirical. Cold dark energy is a gravitating field component, never a particle. Footings are not pooled. Not theory closed. Nothing here says the data favour the framework.
