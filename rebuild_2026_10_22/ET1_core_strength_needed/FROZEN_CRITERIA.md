# ET1_core_strength_needed: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** ARGON_BRIEF_2026-10-30 Q1: the full SPARC line needs η(10¹²) ≤ 21.2 while the L★ analogs want about 26. Route E's rule is S = ρ₀r₀ = max(Σ_a0, η Σ_coll(M)). Instead of
grading a chosen η, measure the S each galaxy asks for at a fixed Υ, and read the rule's shape from the data: plateau, rise with mass, and where the tension sits. Standing: κ = ½ FITTED; footings never
pooled; not theory closed. Nothing here says the data favour the framework.

**Seen before freezing.** LS1's table of median Υ and ΔV by V_flat; CE1 and X73 η values; LS1's per-analog Υ. No per-galaxy S has been computed. X23's criteria use a needed-core idea for a different statistic, so this is not a re-run.

**Sample.** `SPARC_Lelli2016c.mrt` and X74's `GALS` through LS1's base exec, Q ≤ 2, Inc ≥ 30°. V_flat bins 20–60, 60–100, 100–150, 150–200, 200–250, 250–400 km/s (LS1's bins). Galaxies without V_flat are left out and counted.

**Measurement.** M200 from background A_c2b_refit's EM1 relation, as in LS1. Halo: LS1's `solve_r0` and `B` with s set directly. For each galaxy, S_need minimises `fit_one`'s weighted mse of log g on a grid of 121 log-spaced S from 10 to 3000 M☉/pc² at
fixed Υ_disk (bulge 1.4 Υ as in EM1). Primary Υ 0.50; Υ 0.40 and 0.60 reported. S_need is footing-free, because the footing only enters the prediction. A galaxy at either grid end is counted as censored and kept at that end, so medians stay valid. Galaxies whose S is saturated in `solve_r0` are counted.

**Predictions compared (per footing).** At each bin's median lg M200: floor Σ_a0 (106.85 canonical, 129.13 alt); P1 = max(Σ_a0, 10.82 Σ_coll); P2 = max(Σ_a0, η_conv Σ_coll) with η_conv interpolated in lg M through 25.94 / 17.67 / 16.91, held at 25.94 below 10¹²; both with `sigma_coll`.

**Statistic.** Median S_need per bin with a 95 % bootstrap interval (20000 resamples, seed 20261030).

**Verdicts, primary Υ 0.50.**
1. **Per model, per footing:** MATCHES if each bin's 95 % interval contains the prediction; otherwise FAILS, listing bins and sign.
2. **Plateau:** PLATEAU SUPPORTED if all bins with V_flat < 150 have intervals containing that footing's Σ_a0. PLATEAU REJECTED if at least two of those three bins exclude it on the same side. MIXED otherwise.
3. **L★ tension:** NON-MONOTONIC if the 150–200 and 200–250 intervals are disjoint and that step is larger than the prediction P2 allows, meaning lg(S_200-250/S_150-200) exceeds P2's step by more than 0.3 dex in both interval ends. SAMPLE-LEVEL if the intervals overlap. Else STEEPER THAN P2.
4. **Bulge door:** among V_flat ≥ 150, split at f_b = Σ V_bul² / Σ (V_disk² + V_bul²) over OK points: bulgeless f_b < 0.1, bulged f_b ≥ 0.1. BARYON-MODEL SIGNAL if the two groups' intervals are disjoint. NO BULGE SIGNAL otherwise. Fewer than 8 in a group: UNDECIDED.
5. **Mass trend:** Spearman ρ of lg S_need against lg M200 for V_flat ≥ 150, permutation p (20000, same seed). P2 falls with M above 10¹², so a positive ρ at p < 0.01 is OPPOSITE TO NATIVE TREND; negative at p < 0.01 is NATIVE SIGN; otherwise NO TREND.

**What each outcome means, declared now.** A NON-MONOTONIC or OPPOSITE reading with no bulge signal points to route E's mass dependence or to M200, not to the baryons. A bulge signal points to the baryon model. SAMPLE-LEVEL means the tension is not a real feature at this sample size. None of these derive a parameter, and no fitted curve from this lane enters any other lane without its own criteria.

**Checks.**
- K1: S grid value nearest route E's own S returns LS1's halo gravity to 1e-10 on three galaxies.
- K2: a synthetic galaxy whose observed g equals its own model at a planted S returns that S to within one grid step, at S 50, 200 and 800.
- K3: `fit_one` at fixed Υ agrees with a direct weighted mse computation to 1e-10.
- MUTATE (`--mutate`): M200 × 0.5, separate outputs. Exit 1 unless the 200–250 median S_need rises. Less halo mass needs a more compact, denser core to supply the same inner pull, so this tests direction.

**Limits declared now.** A single Υ for all galaxies is a choice, and stellar-population Υ scatters. M200 is taken from one relation, not fitted, so errors there alias into S. Distance and inclination errors are ignored. The core shape is chosen, not derived. Rotation curves probe only part of the halo, so S_need can be weakly constrained in galaxies that end near r₀, and the bootstrap covers sample scatter only. Single-threaded, small job.
