# CFG69 — a ΛCDM comparator through the identical pipelines: is each failure of B specific to B?

Script: `CFG69_lcdm_comparator.py` (about 15 s). Outputs: `.out`, `_results.json`, and the MUTATE pair. Written by a delegated agent (the question and the model declared first) and re-run here. The main run passes 9 of 9. **The declared MUTATE control failed and is kept** (below). **This is a comparator, not a model comparison and not a fit. Nothing here says the data favour ΛCDM or the framework.**

## The frozen question

For each population where candidate B (the bare law L or the sum rule S) fails or is marginal, is the failure SPECIFIC to B, or SHARED by a standard ΛCDM halo run through the identical data, estimator, σ treatment and floors? SHARED if the ΛCDM offset has the same sign and |z| > 2; SPECIFIC-TO-B if ΛCDM is within 2σ; ΛCDM-WORSE if it has the opposite sign at more than 2σ.

**The ΛCDM model (declared once, no per-population tuning):** stars inside a standard NFW halo, halo mass from the Moster+2013 relation (clamped at 10⁹ M☉ below M_* ≈ 1.6 × 10⁴, as CFG42), Duffy+2008 full 200c concentration (CFG65's A2 row), added mass (1 − f_b) M_NFW, no phantom (ν = 1), **no adiabatic contraction (declared, untested)** and no SHMR scatter. ΛCDM has no a₀, so it is identical on both footings.

## Result (offset in dex, σ in brackets; L and S canonical | alt)

| population | L (bare law) | S (sum) | ΛCDM | class (L / S) |
|---|---|---|---|---|
| SLUGGS, JAM-calibrated, 16 (CFG55) | +0.097 (4.0) \| +0.088 (3.6) | +0.046 (2.6) | +0.001 (0.0) | SPECIFIC / SPECIFIC |
| SLUGGS, own masses, 19 (CFG38) | +0.080 (3.3) \| +0.065 (2.7) | +0.007 | −0.048 (−2.4) | **ΛCDM-WORSE** / ok |
| MW ultra-faint KM, 31 + 9 (CFG42) | +0.325 (3.8) \| +0.304 (3.5) | −0.059 (−0.4) | +0.080 (0.6) | SPECIFIC / ok |
| CFG46 eight, f free | +0.206 (1.3) | −0.151 (−1.2) | +0.016 (0.1) | SPECIFIC / SPECIFIC |
| Boötes I cleaned (CFG51) | +0.219 (2.5) | −0.205 (−0.8) | −0.078 (−0.5) | SPECIFIC / ok |
| Tucana II cleaned (CFG51) | +0.465 (3.6) | −0.165 (−0.9) | −0.041 (−0.2) | SPECIFIC / ok |
| Boötes I total mixture / cold only (CFG66) | +0.222 (2.3) / −0.072 (−0.4) | −0.203 / −0.497 (−1.5) | −0.075 / −0.369 (−1.6) | SPECIFIC / ok; ok / SPECIFIC |
| Tucana II gradient-removed (CFG66) | +0.464 (3.6) | −0.165 (−0.9) | −0.041 (−0.2) | SPECIFIC / ok |
| MW classical (CFG42) | +0.027 (0.3) | −0.118 (−1.8) | −0.029 (−0.4) | ok / SPECIFIC |
| M31 Collins (CFG42) | +0.064 (0.8) | −0.024 (−0.2) | +0.058 (0.6) | ok / ok |
| **M31 LVD (CFG42)** | +0.044 (0.6) | −0.107 (−2.7) | −0.062 (−1.3) | ok / SPECIFIC |
| **LV field dwarfs, 13 (CFG58)** | −0.044 (−0.6) | −0.105 (−3.5) \| −0.093 (−2.7) | −0.020 (−0.5) | ok / SPECIFIC |

Over the 16 rows × {L, S}: **15 SPECIFIC-TO-B, 2 ΛCDM-WORSE, 15 B-ok, 0 SHARED.** Where L fails, ΛCDM does not share the failure at > 2σ; where S over-predicts (MW classical, M31 LVD, LV field dwarfs), ΛCDM has the same sign but stays within 2σ.

## Why this is weaker than it looks

- **The ultra-faint gate is not discriminating for ΛCDM, and the declared MUTATE control FAILED (kept).** With every halo mass × 100 the ΛCDM ultra-faint KM median is −0.149 (−1.25σ) and the gate still passes. A diagnostic added after that failure (R3, disclosed, reported only): the gate fails at × 0.01 and × 10³ and passes from × 0.1 to × 100, because the inner NFW mass scales only weakly with the halo mass (Lean-certified: effective slope about 0.18). So "ΛCDM passes the ultra-faint gate" is nearly automatic in this machinery; the collapse-mass floor dominates its error (0.12 dex; the KM median runs +0.204 at 10⁸ to −0.037 at 10¹⁰).
- **The concentration relation matters.** With the Dutton–Maccio concentration instead of Duffy 200c, ΛCDM's M31 LVD is −2.2σ and the LV field dwarfs −2.6σ, the same sign as S's failures, so those two become SHARED for S. SLUGGS with its own masses goes to −4.1σ. Scaling all halo masses by 3 or 1/3 moves the JAM row to ∓2.5σ.
- **The JAM row is built in.** ΛCDM's 0.0σ on the JAM-calibrated SLUGGS is largely by construction (the calibration forces the mass inside r_1/2); the own-mass rows are the unabsorbed test, and there ΛCDM is −2.4σ (ΛCDM-worse).
- No adiabatic contraction and no SHMR scatter (both untested); the SLUGGS sample is 16 of 19; CFG51's own control C1 fails in its committed run; the satellite estimator (σ² = gr/3 with half the baryons enclosed) is applied unchanged to an NFW cusp; CFG66's dispersions were read from its JSON.

## Controls

Pass: C1 (ΛCDM through CFG38's SLUGGS machinery reproduces its post-hoc ΛCDM value per galaxy: mean −0.0365 ± 0.0172, −2.12σ); C2 (124 comparisons of L and S against the committed lane numbers, worst 1.7 × 10⁻¹⁶); C3 (the generic NFW equals the analytic enclosed mass); C4 (M_h → 0 gives the closed-form Newtonian prediction); C6 (the JAM calibration residual 4 × 10⁻¹³). **C5 (the declared MUTATE, halo × 100 flips the ΛCDM ultra-faint gate) FAILED; kept.**

## Standing

**In this machinery none of B's failures is shared by a standard halo, but the comparator is generous to ΛCDM (a floating collapse-mass floor, a built-in JAM calibration, a non-discriminating ultra-faint gate) and sensitive to the concentration relation, so this is not evidence for or against either model.** It says B's failures are not artefacts of the estimators. Nothing here says the theory is closed.
