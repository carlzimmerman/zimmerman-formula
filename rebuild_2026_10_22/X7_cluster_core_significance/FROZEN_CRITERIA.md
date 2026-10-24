# X7_cluster_core_significance: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Map: `X0_explanation_map/MAP.md`
§1.A (item 3), §3 (first bullet), §4 (X2 row). Inputs and classes: `ASSUMPTION_LEDGER.md`.
κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², reported side by side, never pooled. No dark-matter
particle. No new fitted constant as a cure. Never "theory closed". Never "the data favour the framework".

## 0. Question

F1 finds the raw KiDS-1000 shear stacked on 326 eRASS1 clusters at A_MID = 1.68–1.85 (canonical) / 1.54–1.70 (alt) times the
law on baryons, Z ≈ +5 to +6 on jackknife errors. X2 propagated the cross-shear MID offset (+0.19 to +0.24 in A units,
1.7–2.1σ) and the random-minus-random offset in quadrature as a systematic. That roughly doubles σ_MID and drops Z_MID to
2.2–2.7 at its corrected baseline C\*. X2 calls this conservative: the cross-shear stack is mostly shape noise. X2 also finds
the lightest Mgas500 tercile without a core excess (MID 1.02–1.13) and OUTER rising with mass (0.46–0.54 / 0.72–0.80 /
1.25–1.40).

(i) Is the core excess significant once the additive shear systematics are **calibrated** on the KiDS data on disk,
rather than inflated? (ii) Does A_MID (and A_OUTER) depend on cluster mass?

**Seen before freezing (disclosed).** BRIEF, MAP §1.A/§3/§4; F1 README, criteria, ledger, `f1_cluster_cores.py` (full) and
`f1_extract.py`; X2 README, criteria, ledger, `x2_replay.py` (full), `x2_cluster_outskirts.py` (full), its `.out`
(C0, C\*, (e) offsets, terciles) and the key layout of its results JSON; X2's npz key names and shapes; CFG687 and CFG688
READMEs and LEDGER rows; CFG922/CFG949/CFG967 LEDGER rows. The KiDS FITS column list (it has PSF_e1, PSF_e2, THELI_NAME,
THELI_INT) and the eRASS1 FITS column list (it has M500). **No number of this lane exists.**

## 1. Data, statistic, cells, baseline

- **Data.** F1's per-cluster KiDS measurement of the 326 clusters (F1's estimator, F1's random positions and seed, F1's
  acceptance), REPLAYED here from my own KiDS column cache (`x7_extract.py`, same filter and order as F1's
  `f1_extract.py`), extended to return the leakage templates (§2a) and the rotated-source realisations (§2c). The replay must
  equal X2's committed `x2_replay_percluster.npz` (check M1).
- **Statistic (X2's).** A_band = Σ_i Σ_j W_ij D_ij B_j / Σ_i Σ_j W_ij P_ij, W = 1/E², B = F1's data boost (graded
  convention, as F1's frozen PRIMARY and X2); MID = bins 3–5 (0.46–1.42 Mpc), OUTER = bins 6–7 (1.42–3 Mpc), INNER reported
  only. Z_band = (A_band − 1)/σ_band. The clipped-boost convention (B = 1, F1 A1) is reported for every graded row.
- **Cells.** 2 footings × 2 native h (0.672, 0.686) = 4 cells, reported side by side, never pooled.
- **Graded model: X2's C\* model** = F1 PRIMARY (spherical AQUAL μ = x/(1+x), native h, eRASS1 gas rescaled q^{5/2}, β-model,
  f\* = 0.20, catalogue miscentring) + (a1) CFG814 r⁻³ gas beyond 2.2 R500 + (c1) Chae+21 noclu external field (F2's solver,
  F2 transplant) + (d) reduced shear. Computed with X2's own functions exec'd read-only from its source text (sha256
  recorded). **C0 (F1 PRIMARY model)** is reported beside it with every error treatment.

## 2. Calibrating the additive systematics (step 1)

**(a) PSF leakage / additive bias regression.** Per source, e_k = c_k + α_k e_PSF,k + noise (k = 1, 2), w-weighted least
squares, with heteroscedastic (sandwich) errors.
- **LK-P (primary):** one (α_k, c_k) per group g = KiDS patch (N: 100° < RA < 260°; S: otherwise) × KiDS-1000 tomographic Z_B bin
  ((0.1, 0.3], (0.3, 0.5], (0.5, 0.7], (0.7, 0.9], (0.9, 1.2]); 10 groups × 2 components. Sources with Z_B ≤ 0.1 are not
  fitted (they never enter the stack: Z_B > z_l + 0.2 ≥ 0.25) and get their patch's first bin's coefficients.
- **LK-T (bracket, reported):** one (α_k, c_k) per KiDS tile (THELI_NAME). Tiles with < 1000 fitted sources take LK-P's
  coefficients.
- Sources with non-finite PSF_e1/PSF_e2 are left out of the fit and get a zero leakage field (count reported).
- **Leakage template:** F1's estimator applied to the model field e_sys = c + α e_PSF in place of (e1, e2) (same weights,
  Σ_crit, bins, cluster − mean random, × B), tangential (D_leak) and cross (D_leak,×). Band offsets A_leak = Σ W D_leak B /
  Σ W P, A_leak,× likewise. σ_leak = linear propagation of LK-P's coefficient covariance through the per-group templates
  (each (group, coefficient) template computed separately; the stack is linear in the coefficients).
- Reported also: the global (all-source) α_k, c_k; the raw tangential/cross PSF pattern around clusters (α = 1, c = 0).

**(b) Random-point stacks.** F1's own random positions (5–6 per cluster, 1–3° away, the cluster's z, same source selection).
Reported: the mean raw random-point stack (tangential and cross) in A units with jackknife and rotated-noise errors (what
F1 subtracts), and X2's random-minus-random D_RR = mean(randoms 1–3) − mean(randoms 4–n) → A_RR.

**(c) Rotated-source realisations.** R = 200 realisations. In realisation r each source's ellipticity is rotated by
θ_{s,r} = π u_{s,r}, u uniform in [0, 1) from a counter-based hash (splitmix64) of (the source's row index in the
cell-sorted cache, r), so a source has the same rotation in every aperture (cluster or random) it enters. The tangential,
cross and R−R stacks are recomputed with F1's estimator, weights, randoms and boost. **σ_n** (per band, per selection, per
cell and convention) = the standard deviation of the band statistic over the 200 realisations. Reported: σ_n,× against the
jackknife σ of the observed cross stack, the two-sided p_× = fraction of realisations with |A_×^(r)| ≥ |A_× − A_leak,×|, and
the cross-shear profile χ² (bins 0–7) against the rotation covariance (Hartlap (R − 8 − 2)/(R − 1)).

## 3. Three error treatments (step 2), per band, per selection S, per cell

- **σ_boot:** cluster bootstrap, 2000 draws (numpy default_rng seed 20261024), clusters of S resampled with replacement, A
  recomputed as the ratio of sums. **σ_jk:** X2's 30 equal-count RA patches restricted to S.
- **STAT:** A as measured; σ_STAT = max(σ_boot, σ_jk). (σ_boot and σ_jk are each reported.)
- **CAL (graded):** A_CAL = A − A_leak (LK-P); σ_CAL² = σ_STAT² + σ_leak² + s_×² + s_RR², where
  s_×² = max(0, (A_× − A_leak,×)² − σ_n,×²) (the cross-shear offset left after the leakage model, in excess of its pure
  shape-noise expectation) and s_RR² = max(0, A_RR² − σ_n,RR²). An unexplained cross-shear excess is treated as an additive
  systematic of unknown sign whose tangential projection has the same variance (isotropic systematic); its measured
  amplitude, not the raw offset, enters.
- **CONS (X2's (e), reproduced):** A as measured; σ_CONS² = σ_jk² + A_×² + A_RR².

## 4. Mass trend (step 3)

- **Proxy:** catalogue MGAS500 (unrescaled), the record's proxy (CFG687 T2; X2 terciles). eRASS1 M500 (ΛCDM-processed)
  binning is reported, never graded.
- **Binning (noise-only rule, frozen):** quintiles of the 326 (np.quantile at 0.2, 0.4, 0.6, 0.8; np.digitize) are graded
  if every quintile's σ_STAT,MID at C\* is ≤ 0.40 in all 4 cells; otherwise X2's terciles (np.quantile at 1/3, 2/3) are
  graded. The rule looks at errors only. The other binning is reported.
- **Per-bin CAL systematic:** the leakage A_leak,b and σ_leak,b from the bin's own clusters. The cross and R−R excess is the
  all-cluster amplitude carried as a **coherent** additive ΔΣ offset: v_b = s_×,ALL κ_b, u_b = s_RR,ALL κ_b, with
  κ_b = (Σ_{b} W B / Σ_{b} W P) / (Σ_{ALL} W B / Σ_{ALL} W P) per band. CAL covariance across bins =
  diag(σ_STAT,b² + σ_leak,b²) + v vᵀ + u uᵀ. STAT covariance = diag(σ_STAT,b²). CONS covariance = diag(σ_jk,b² + A_×,b² +
  A_RR,b²) (X2's per-tercile rule). Reported (not graded): CAL with each bin's own s_×,b, s_RR,b (diagonal).
- **Shapes (no fitted physics; linear GLS on the binned A vector):** (S0) constant a; (S1) linear a + b·x, x = log10(MGAS500 /
  median MGAS500 of the 326); (S2) step a_lo (MGAS500 < M_T), a_hi (≥ M_T) with M_T = X2's T1|T2 boundary (np.quantile at 1/3
  of the 326). The model's binned prediction is the statistic's own weighted mean over the bin's clusters,
  A_b = Σ_{i∈b} w_i a(M_i) / Σ_{i∈b} w_i with w_i = Σ_{j∈band} W_ij P_ij (C\* model, per cell).
  Δχ²_S1 = χ²_S0 − χ²_S1, Δχ²_S2 = χ²_S0 − χ²_S2; BIC = χ² + k ln(n_bins). Preferred shape = lowest BIC (a tie goes to the
  simpler shape).

## 5. Frozen verdict classes (graded at C\*, CAL, boost convention)

**V1 core excess:** Z_MID,CAL per cell.
- **REAL:** Z_MID,CAL ≥ 3 in all 4 cells (both footings, both h ends).
- **NOT SIGNIFICANT:** Z_MID,CAL < 2 in at least one cell (either footing).
- **MARGINAL:** otherwise.
- Reported beside it, never changing the class: the same rule under STAT and under CONS; the clipped boost; C0; the LK-T
  bracket (A_leak from LK-T instead of LK-P). Qualifier **LEAKAGE-MODEL-DEPENDENT** if |A_leak,LK-T − A_leak,LK-P| > σ_STAT,MID / 2 in
  any cell.

**V2 mass trend of A_MID** and **V3 mass trend of A_OUTER** (each graded; CAL covariance; graded binning):
- **PRESENT (shape):** max(Δχ²_S1, Δχ²_S2) ≥ 9 in all 4 cells; the shape named is the preferred one (SPLIT shape reported if
  cells differ).
- **ABSENT:** max(Δχ²_S1, Δχ²_S2) < 4 in all 4 cells.
- **UNDECIDED:** otherwise.
- **Lightest bin:** CONSISTENT WITH A = 1 if |Z_1,CAL| < 2 in all 4 cells; INCONSISTENT if ≥ 2 in all 4; SPLIT otherwise.

Reported, never graded: Z_OUT under the three treatments; the STAT and CONS trend fits; the M500 binning; terciles if
quintiles are graded (and vice versa); the calibration numbers of §2.

## 6. Checks (each script prints `K# PASS|FAIL value threshold`, ends `... COMPLETE: n/m checks PASS.`, exit 0 iff all pass)

`x7_extract.py <out dir> [<F1 KiDS cache dir>]`:
- E1: kept rows and order equal F1's cache: ra, dec, e1, e2, w, zb, cell byte-identical (when F1's cache dir is given).
- E2: THELI_NAME ↔ tile id is one-to-one; the count of non-finite PSF_e among kept rows is reported.
- E3: peak RSS < 1 GB.

`x7_psf_regression.py <cache> [--mutate]`:
- G1: injection linearity: refitting with e_k + 0.05 e_PSF,k returns α_k + 0.05, and with e_k + 0.003 returns c_k + 0.003,
  to ≤ 1e-6 absolute in every LK-P group.
- G2: the accumulator fit equals a direct `np.linalg.lstsq` weighted fit on all rows of one LK-P group (KiDS-N, bin 3) to ≤ 1e-8
  relative in α and c.
- G3: peak RSS < 1 GB.
- `--mutate`: the accumulators drop the weights (G2 must FAIL).

`x7_measure.py <cache> <scratch out dir> [--mutate]`:
- M1: N = 326, names equal, and D, E, den, den_r, Dx, DRR, m3to8 for h070/h0672/h0686 equal X2's committed npz to ≤ 1e-9 ×
  max|D| (den/den_r/m relative ≤ 1e-9).
- M2: the template code path fed with the field (e1, e2) itself reproduces D and Dx (≤ 1e-9 × max|D|) for every cluster.
- M3: rotation identities on the first 3 clusters: θ ≡ 0 reproduces D and Dx; θ ≡ π/4 gives D_t = −D_x (≤ 1e-9 × max|D|).
- M4: the hash is deterministic (same (s, r) → same u) and uniform (KS p > 1e-3 on 1e6 draws).
- M5: rotated stacks centre on zero: for each h and channel, |mean_r(ΣWD^(r)_MID)| ≤ 4 × std_r/√R.
- M6: peak RSS < 1 GB.
- `--mutate`: first 20 clusters only, e2 sign flipped (M1 must FAIL).

`x7_analysis.py <scratch out dir> [--mutate]`:
- K0: X2 reproduction from X2's committed npz with X2's functions: C0 and C\* A, s_jk, s_tot, A_x, A_RR (MID, OUTER, 4 cells,
  boost and clip) equal X2's results JSON to ≤ 1e-4; C0 equals F1's PRIMARY rows (A_MID, σ_MID, A_OUTER; F1 JSON) to ≤ 1e-4;
  X2's tercile A_MID/A_OUTER at C0 and C\* to ≤ 1e-4.
- K1: the analysed data (my replay) equal X2's npz (D, Dx, DRR) to ≤ 1e-9 × max|D|.
- K2: bootstrap: σ_boot = 0 (≤ 1e-12) when every cluster has D = 2P; for synthetic i.i.d. per-cluster ratios with known σ,
  σ_boot within 10 % of σ/√n (n = 326, 2000 draws).
- K3: GLS shapes: a synthetic A vector built exactly from S1 and from S2 with the real weights is fitted with χ² ≤ 1e-10 and
  parameters to ≤ 1e-8.
- K4: σ_leak propagation equals a finite-difference recomputation (one coefficient moved by ε) to ≤ 1e-6 relative.
- K5: peak RSS < 1 GB.
- `--mutate`: the cross shear replaces the tangential data (K0 must FAIL) and the shape fits use unweighted bin means for
  the model (K3 must FAIL).

Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, ≤ 30 min each (split into parts with the RNG state carried over if
needed; that split is an implementation amendment), none while `compute_queue/heavyq.py status` shows low free memory;
compute_queue/ and other lanes untouched. Caches and the rotation products live in session scratch; `.out`,
`_results.json` and a compact per-cluster npz are committed.

## 7. Stop rule

No knob scans. No new physics fitted: the only fitted numbers are the survey's own leakage coefficients (α, c) and the
shape-model amplitudes of §4, none of which enter the law. No post-hoc bin choices: binning, step location, pivot, R, draw
counts and thresholds are fixed above. If M1 or K0 fail, nothing downstream is graded (UNDECIDED, missing input named).

## AMENDMENTS (append-only; each labelled PRE-RESULT or POST-RESULT)
