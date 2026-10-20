# CFG880 — FROZEN CRITERIA: is the cold clump's velocity dispersion σ_x UNIVERSAL, or does it vary from dwarf to dwarf?

Frozen before any script (owner block 880–889). κ = ½ fitted; ν_e; the two a0 footings are never pooled; not theory closed.

## Why
CFG877's finite cold clump (one bound cold-energy clump per faint dwarf, σ_x = V_x/√2 ≈ 7.53 km/s, M_cl = 81σ_x⁴/(4 G a0))
fits every dwarf sample within ~2σ with ONE σ_x. CFG878 showed the clump mass is set by σ_x alone and that a fixed-physics
origin (neutral primordial gas at the hydrogen-cooling floor, 7.36–8.22 km/s) contains it (post-hoc). A fixed-physics origin
needs σ_x to be the SAME in every dwarf. CFG872 (different clump form, H-LINK) found per-dwarf clump masses scattered by
0.52 dex. This lane measures the intrinsic dwarf-to-dwarf scatter s_int of ln σ_x directly, under CFG877's clump.

## Sample (LVD csvs only; nothing downloaded)
`real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv`: every dwarf with a measured `vlos_sigma` (no `vlos_sigma_ul`),
r_h (`rhalf_sph_physical`, else `rhalf_physical`) and M_V; excluded rotating / gas-rich set: LMC, SMC, WLM, NGC 6822, IC 1613,
Leo A, Sagittarius dIrr, Pegasus dIrr, M 32. Expected N = 83 (counted before freezing; no prediction computed). Errors: LVD
`vlos_sigma_em` / `vlos_sigma_ep` (all 83 have both).

## Model (per dwarf i; every number fixed beforehand)
- r12 = (4/3) r_h. g_bar = G (Υ_V L_V/2 + M_gas,in)/r12², Υ_V = 2 (primary), gas inside r12 from CFG874's `gas_in()` (Wang+16
  exponential HI disc ×1.33, extended root; copied unchanged). σ_law² = g_bar ν_e(g_bar/a0) r12/3 (Wolf).
- Clump (CFG877's shape): M_x(<r; σ_x) = min[2σ_x² r³/(G (r² + r_c²)), 81σ_x⁴/(4 G a0)], r_c = 104 pc fixed.
- σ_pred,i(σ_x)² = σ_law,i² + G M_x(<r12; σ_x)/(3 r12).

## Hierarchical likelihood
- ln σ_x,i = ln σ̄ + δ_i, δ_i ~ N(0, s_int²).
- σ_obs,i | σ_pred,i: split normal with constant normalisation √(2/π)/(e_m + e_p), width e_p when σ_obs < σ_pred, else e_m.
- δ_i marginalised numerically: per-dwarf likelihood tabulated on a uniform grid in u = ln σ_x (step 0.0025, σ_x from 1e-3 to
  3e3 km/s, edge-padded: below = law-only plateau, above ≈ 0), convolved with the normalised discrete Gaussian kernel of width
  s_int (FFT). s_int grid: 0, 0.005–0.30 (step 0.005), 0.32–1.00 (0.02), 1.05–2.00 (0.05); ln σ̄ on the u grid (σ̄ 1–50 km/s).
- Maximum likelihood over (σ̄, s_int). Profile-likelihood intervals (Wilks, one parameter, no boundary correction —
  conservative for an upper limit at s_int = 0): 68% Δ(−2 ln L) ≤ 1.00, 95% ≤ 3.84, crossings linearly interpolated.
  An upper limit reaching the grid edge is reported as "> 2.0".
- Reported: ŝ_int, σ̂̄, their 68/95% intervals; σ̄ of the universal fit (s_int = 0) with its 68/95% interval; the scatter
  test Λ = 2[ln L(ŝ) − ln L(s_int = 0)], p = ½ P(χ²₁ > Λ); per-dwarf individual σ_x MLE and 95% range (upper limit if it
  runs to σ_x → 0), and the dwarfs whose individual 95% range excludes the universal σ̄.

## Classes (primary: canonical; the alternative footing must give the same class, else UNDECIDED)
- **UNIVERSAL:** 95% upper limit on s_int ≤ 0.15 (σ_x the same to ≤ 15% in every dwarf).
- **NOT UNIVERSAL:** 95% lower limit on s_int > 0.15.
- **UNDECIDED:** anything else.
Qualifiers appended to the class (pre-registered):
- if variant V3 (law-over-predicted dwarfs removed) gives a different canonical class → "(rests on the law-over-predicted
  dwarfs: <names>)";
- if the class is NOT UNIVERSAL and variant V5 (10% systematic floor) is not NOT UNIVERSAL → "(not robust to a 10% systematic)".
**Reading rule (pre-registered):** s_int absorbs ALL scatter not in the quoted σ errors (Υ_V spread, distance / r_h errors,
anisotropy and the Wolf estimator, binaries, tides, external field). So UNIVERSAL is a strong statement (an upper limit on
everything), while NOT UNIVERSAL means "scatter beyond the quoted errors which, if it were all the clump's, exceeds 15% in σ_x";
it does not by itself prove the clump varies.

## Hydrogen-cooling comparison (POST-HOC label; CFG878 candidate (i))
Does the 95% interval of σ̂̄ (hierarchical) and of the universal-fit σ̄ overlap [7.36, 8.22] km/s? Reported as OVERLAPS /
BELOW / ABOVE; not graded. Also reported, not graded: whether the 95% upper limit on s_int is ≤ 0.055 (the bracket's half-width).

## Variants (reported, both footings; only V3 and V5 feed the qualifiers above)
- V1 Υ_SFH from CFG827 rows where available (else 2).
- V2 M_V ≤ −6 only (fewer binary-inflated ultra-faints; expected N = 53).
- V3 law-over-predicted dwarfs removed: z_law = (σ_obs − σ_law)/e_p ≤ −2 at the primary inputs (tidal / external-field cases).
- V4 binary-corrected σ (Arroyo-Polonio+2026 flat-prior-f column, ±1σ) where available in
  `real_research/data/arroyopolonio2026_ufd_binary_corrected.tsv` (as used by CFG859).
- V5 a 10% systematic floor: e → √(e² + (0.1 σ_obs)²) on both sides.
- V6 law-linked core: r_c = 104 pc × (σ_x/σ_ref)², σ_ref = V_x/√2 of the footing.

## Power pre-flight (reported, not graded)
16 synthetic null data sets per footing (seeds 8800–8815): σ_x = σ_ref = V_x/√2 (CFG870, 10.6547 / 10.5870 km/s) in every dwarf,
σ_obs = σ_pred + split-normal noise with the observed e_m / e_p (negative side e_p, positive side e_m; floor 0.1 km/s), primary
inputs, full fit. Reported: median and 84th percentile of the 95% upper limit on s_int, and the fraction ≤ 0.15 (the chance of
reaching UNIVERSAL if σ_x were exactly universal). If the median exceeds 0.15, UNIVERSAL is declared out of reach with present
errors; the class rule is unchanged.

## Controls
- **K1 (code identity):** with s_int = 0 and σ̄ = V_x/√2 (CFG870 value per footing; 7.534 canonical), the script's σ_pred function,
  fed CFG877's own inputs (CFG824 σ / CFG827 Υ_SFH / no gas for MW classical and M31+field; LVD σ / Υ 2.20 / no gas for the UFDs;
  LVD σ / Υ 2 / gas for CFG876's large and small sets), must reproduce all five CFG877 group means E (cfg877_results.json, both
  footings) to |diff| < 1e-9.
- **K2 (integrator):** for s_int = 0.3 and σ̄ = σ_ref, the FFT-marginalised per-dwarf ln L must match a direct fine quadrature
  (trapezoid over ±10 s_int, 40001 nodes) to < 1e-3 for every dwarf in the primary sample.
- **MUTATE** (`CFG880_MUTATE=scatter|null`, outputs `cfg880_MUTATE_<mode>.out` / `cfg880_results_MUTATE_<mode>.json`): synthetic
  σ_obs as in the pre-flight, seed 880, primary sample and inputs. `scatter`: σ_x,i = σ_ref e^{0.4 z_i} (s_int = 0.4) → the primary
  rule must return NOT UNIVERSAL on both footings. `null`: s_int = 0 → must NOT return NOT UNIVERSAL. Otherwise CONTROL FAILED
  (reported as such; the test then lacks the power it claims).

## Disclosures (known before freezing)
- Not blind: all 83 dispersions were used in earlier lanes; σ_x ≈ 7.53 km/s was calibrated (CFG870) on a subset of this sample, so
  σ̄ is not an independent measurement. The finite-clump form itself was chosen post-hoc (CFG877).
- No external field, tides or binary modelling except in the variants named. r_c fixed (V6 lets it scale).
- Only light single-core compute (OMP_NUM_THREADS=1, nice 10), alongside the running 1024³ job, as allowed by the owner.
