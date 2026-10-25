# X29_late_power_shear — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** The cold-sector spec (7af76cfeed, §4) has the cold component heated after z ≈ 2. That suppresses
small-scale matter power late: X22 found T²(z = 0, k = 1 h/Mpc) = 0.80–0.97, ungraded. On X26's allowed sheet
(c9112e3126, scenario B), what does that suppression do to **raw** KiDS-1000 and DES Y3 cosmic shear (ξ±)? The comparison
is the record's own same-pipeline control run, scored by the record's native scorer.

Standing rules:
- κ = ½ FITTED. Footings canonical / alt, never pooled.
- RAW shear data against framework-native predictions. No HMcode, BAHAMAS, ΛCDM S₈ number or ΛCDM yardstick enters the
  verdict.
- Cold energy is field mass, never a particle.
- Not "theory closed". Nothing here may say the data favour the framework. CFG909's lesson is carried forward: a lower χ²
  from lower amplitude is not a preference for the model's shape.

## 1. Inputs (read-only)

- **Control run S:** `_external_data/cfg654_work/NCS0/cfg654cmb_cfg650_na_S0_canonical_N1024_L100_ns1024_lean.json`
  (CFG654 native_cmb inputs; dust-only S0 control, 1024³, L 100 Mpc/h). Its snapshots at z = 1, 0.755, 0.5, 0.256, 0
  carry P(k) and P_grav(k) on 512 k values.
- **Scorer:** `campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native.py` `load_lib("native_cmb")` + `score()`,
  executed read-only. This is the scorer used for NC1x / NC2x.
  - Δχ² = χ²(F) − χ²(S0) per survey, on the published kept set with support ≥ 0.9.
  - Robust variants are reported as the scorer prints them: widen2, noIA, held, DESI, LOC.
- **Allowed sheet:** X26 `x26_pass_masks.npz`, the AND of scenario B's constraints (`GRADED_B` in `x26_cold_sector_map.py`),
  per footing, over (c_*, r, q, p).
- **Cosmic sound speed (X26's law, copied):**
  - c_s,cos(a) = C₀ a^(p_eff − ½), with p_eff = p − r/2 − 3q/2;
  - log C₀ = log c_* + r log(σ_cos1/100) + (q/2) log(ρ_b0/10⁻³);
  - σ_cos1 and ρ_b0 as in X26.
- **Growth:** X22's linear two-fluid ODE (copied verbatim from X26 `grow`), giving T²(k, z) = [δ_m(c_s) / δ_m(0)]² at
  each snapshot z.

## 2. The framework arm F

F = S with every snapshot's P and P_grav multiplied by T²(k, z_snap) at each allowed point. T² is computed on 48
log-spaced k from the box minimum to its maximum and interpolated in log k. The two arms differ only by T². The
z > 1 continuation, the IA treatment and the background are the scorer's own, applied identically to both.

**ASSUMPTION A (disclosed, not tested):** the linear T² multiplies the nonlinear P. Late heating's nonlinear response
(a hot component in collapsed halos) is not modelled. For a suppression this is conservative in direction only: halo
retention at c_s ≈ σ would restore part of the power in clusters.

The S0 run is footing-blind (dust control). The footing enters through the allowed set and through the scorer's foot
label.

## 3. Verdict (per footing; the class needs both footings to agree), on KiDS-1000 Δχ²

| class | condition |
|---|---|
| **SHEET EXCLUDED** | every allowed point has Δχ²_KiDS ≥ 9 |
| **SHEET CUT** | some allowed points have Δχ²_KiDS ≥ 9, others < 9; the surviving fraction is reported |
| **SHEET CONSISTENT** | every allowed point has Δχ²_KiDS < 9 |

- If every point also has Δχ² ≤ −4, the label gains **[LOWER χ², AMPLITUDE CAVEAT]**. In words: the suppression lowers
  χ² against a projection whose amplitude CFG909 found too high, and that is not a shape preference.
- DES Y3 is reported with the same numbers. It follows CFG909's NOT-DIAGNOSTIC precedent unless its own control passes.
- Reported: the minimum, median and maximum Δχ² over the sheet; T²(k = 0.3, 1, 3; z = 0, 0.5) and σ₈ ratio range; and
  the robust variants at the min and max points.

## 4. Checks (all must pass; `--mutate` must fail K0)

- **K0:** with T² ≡ 1, F = S and Δχ² = 0 exactly (1e-10) for both surveys. The X26 allowed counts are reproduced
  (45 canonical / 37 alt grid points).
- **K1:** at c_s ≡ 0, the ODE gives T² ≡ 1 (1e-10). T² is non-increasing in C₀ at fixed p_eff (X22's C3), at three k.
- **K2:** the scorer's numbers on the stored NC1x vs NCS0 pair equal CFG654's committed `cfg654_native_results_NC1x.json`
  dchi2 to 1e-6 (as CFG909 K1), if that file exists. Otherwise this is reported as not available.
- **K3:** peak RSS < 6 GB (the scorer's lookup tables), one thread, preemptible on SIGTERM (it exits cleanly; runtime is
  minutes).
- **MUTATE:** T² is applied as 1/T² (power raised, not lowered); K0's count check passes, but **K4** must fail.
- **K4:** at every allowed point σ₈(F)/σ₈(S) ≤ 1.
