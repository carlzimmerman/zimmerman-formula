# X11_cross_shear_diagnosis: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Inputs and classes:
`ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², reported side by side, never
pooled. No dark-matter particle. No new fitted constant. Never "theory closed". Never "the data favour the framework".

## 0. Question

X7 (`X7_cluster_core_significance/`, criteria 40ae8ff09f, result b1a2ffcb6b) finds the eRASS1 × KiDS-1000 core excess at
Z_MID = 4.5–5.5 on statistical errors (STAT) and 2.4–2.9 (MARGINAL) when the cross-shear MID offset (+0.19 to +0.24 in A
units; rotated-source shape noise 0.084–0.096; p 0.010–0.015) is treated as an isotropic calibrated systematic (CAL). Its
source is unidentified; PSF leakage explains ≤ 0.003.

**Is the cross-shear offset an instrumental or astrophysical systematic that should also bias the tangential signal (so the
excess stays MARGINAL), or is it consistent with a statistical fluctuation / pure B-mode (so the STAT Z stands)?**

**Seen before freezing (disclosed).** BRIEF; X7 README, FROZEN_CRITERIA, ASSUMPTION_LEDGER, all four scripts (full), their
`.out` files and the key layout and graded numbers of `x7_analysis_results.json` (A_x, σ_n,×, p_×, rand_x, the cross
profile's per-bin significance −3.05 / +0.38 / −1.75 / +0.22 / +1.81 / +1.43 / +1.00 / +0.74 at h 0.672, Z_STAT, Z_CAL,
the PSF regression tables); X2 README and the statistics / model sections of `x2_cluster_outskirts.py`; F1 README. The KiDS
FITS column list (it has MAG_AUTO, bias_corrected_scalelength_pixels, PSF_Q11/Q22/Q12, neighbour_distance,
contamination_radius, model_SNratio). **No number of this lane exists**: no split, null or E-mode statistic below has been
computed by anyone.

## 1. Step 0: reproduce X7 on a rebuilt cache

- **Cache.** Rebuilt from the raw KiDS FITS on disk by X7's `x7_extract.py` into session scratch (`<scratch>/x11cache/`),
  not the repo.
- **X7's code, run read-only.** `x11_step0.py <x7 script> <args>` reads X7's committed source text, checks its sha256 against
  the committed blob, applies only declared output-path substitutions (X7 output names `x7_*` → `x11_s0_x7_*` in this lane's
  dir; X7's per-cluster npz → scratch), and executes it. Order: extract, PSF regression, measure, analysis (each X7's own
  checks must pass). The extractor's E1 is given X7's earlier scratch cache as its comparison cache if present.
- **S0 checks (`x11_s0_check.py`):**
  - S0-1: the 7 shared cache columns (ra, dec, e1, e2, w, zb, cell) have the sha256 X7 committed (`x7_extract_results.json`).
  - S0-2: every array of the step-0 per-cluster npz equals X7's committed `x7_measure_percluster.npz` (max |Δ| = 0).
  - S0-3: the step-0 analysis JSON equals X7's committed JSON on: `all.<C*|boost|cell>.MID|OUTER.{A, A_x, s_n_x, p_x,
    resid_x, s_x_exc, rand_x, Z_rand_x, Z_STAT, Z_CAL, s_STAT, s_CAL}` (4 cells), `V1`, `Z_MID_CAL`, `cross_profile.*.chi2`,
    to ≤ 1e-9 absolute.
  - S0-4: all X7 checks in the four step-0 runs PASS.
  - `--mutate`: the step-0 Dx sign is flipped before S0-2 (S0-2 must FAIL).
- If S0 fails, nothing downstream is graded (UNDECIDED, the missing input named).

## 2. New inputs (extra columns, class edges; catalogue only, no shear)

`x11_extract_extra.py <cache> [--mutate]`: re-reads the KiDS FITS with X7's filter and order (finite RA, DEC, e1, e2;
weight > 0; Z_B ≤ 1.2; stable sort by the 0.2° sky cell) and writes into the scratch cache: `mag` = MAG_AUTO, `size` =
bias_corrected_scalelength_pixels, `psfT` = PSF_Q11 + PSF_Q22, `nbr` = neighbour_distance (float32).
Validity: mag finite and 10 < mag < 35; size finite and > 0; psfT finite and > 0; nbr finite. An invalid value puts the
source in no class of that variable (it stays in ALL); counts are reported.

**Class edges** (computed here from the catalogue alone, written to the results JSON before any shear statistic):
- mag, size, psfT: lensfit-weight (w) quantiles at 0.25 / 0.5 / 0.75 over the valid cache rows (halves at 0.5;
  quartiles at all three).
- psfE = √(PSF_e1² + PSF_e2²): w-quartiles.
- nbr: w-median (halves; a value equal to the edge goes to the upper class).
- Tile seeing (tile groups): per tile (THELI_NAME) the w-weighted mean psfT of its valid sources; tiles sorted by that mean
  and cut where the cumulative source weight crosses 1/3 and 2/3 → 3 tile classes.
- Δz_ls edge: the median of Z_B − z_l over (cluster, source) pairs, each pair weighted w·Σ_crit⁻² (h 0.672, F1's
  distances), sources from the cache's w-weighted Z_B histogram (0.01 bins) with Z_B > z_l + 0.2, each of the 326 clusters
  (z from X7's committed npz) given equal total weight.
- Count slope (for §6 only): unweighted MAG_AUTO counts of the valid cache rows in 0.1-mag bins; s = least-squares slope of
  log10(dN/dm) over [m_25, m_60] (unweighted percentiles), brackets [m_10, m_50] and [m_40, m_75]; α = 2.5 s.

Checks: X1 the re-extracted e1 column, after the reorder, is byte-identical to the cache's `e1.npy` and the kept count
equals the cache's; X2 every edge is finite and strictly increasing, and each class of every split holds ≥ 10 % of the
valid weight; X3 peak RSS < 1 GB. `--mutate`: the reorder is skipped (X1 must FAIL).

## 3. The split measurement (`x11_measure.py <cache> <scratch out> [--mutate]`)

X7's measurement loop (F1's 326 clusters, F1's random positions, seed 20261022 and acceptance; X7's estimator, Σ_crit,
bins, m = −0.01), with every per-bin sum also accumulated per **source class**. Per call (cluster or random), per h ∈
{0.672, 0.686}, per channel (tangential, cross), per class, per radial bin: Σ ww·val, Σ ww, Σ ww²·val², count, Σ isc.

**Source-level variables (classes):**
| id | variable | classes |
|---|---|---|
| ALL | all sources | 1 |
| tomo | KiDS-1000 Z_B bin (0.1,0.3], (0.3,0.5], (0.5,0.7], (0.7,0.9], (0.9,1.2] | 5 |
| mag2 / mag4 | MAG_AUTO halves / quartiles | 2 / 4 |
| size2 / size4 | scalelength halves / quartiles | 2 / 4 |
| psfT4 | PSF size (Q11 + Q22) quartiles | 4 |
| psfE4 | PSF ellipticity modulus quartiles | 4 |
| psfx2 | sign of the PSF ellipticity's cross projection about the call centre (record convention; ≥ 0 → class 1) | 2 |
| psft2 | sign of the PSF ellipticity's tangential projection about the call centre | 2 |
| nbr2 | neighbour_distance halves (blending proxy) | 2 |
| dzls2 | lens–source separation Z_B − z_l halves (the "pair separation in the source plane", read as line-of-sight separation behind the cluster) | 2 |
| tile3 | tile-seeing group | 3 |

Per cluster and class: D_k = (cluster sum / its den_k) − mean over the cluster's randoms (each normalised by its own
den_k), as F1/X7 (an empty class-bin gives 0, X7's nan_to_num); E_k from the cluster call alone; W_k = 1/E_k²
(0 if empty); B_k,j = Σ_i den_ijk / Σ_i den_r,ijk (the class's own boost).

**Rotated realisations:** R = 200, X7's splitmix64 hash of (row index in the cell-sorted cache, r) (a source keeps its
rotation in every aperture and equals X7's draw), cross channel, MID bins (3–5) only, per class; per cluster
D^(r)_k = cluster/den_k − mean_rand(random/den_k).

**Per-cluster geometry (cluster call, h 0.672, MID sources, ww weights):** f_main = weight fraction on the dominant tile
(tile straddle); m2 = |Σ ww e^{2iφ}| / Σ ww (azimuthal coverage anisotropy).

**90° null (identity):** for every cluster call the stack is also computed with every source position rotated by 90° about
the cluster (ellipticities held in the sky frame). Algebraically this flips both channels exactly (2φ → 2φ + π), so it is
recorded as a check of the code and of that statement, not as independent evidence.

**Extended random points (`x11_randoms.py <cache> <scratch out> [--mutate]`):** 20 new random positions per cluster
(numpy default_rng(20261025), X7/F1's rule: uniform angle, 1–3° away, the cluster's z, accepted if the h 0.70 in-bin count
exceeds 0.5 × the cluster's; up to 60 tries), ALL class: raw tangential and cross sums per bin, counts, and R = 200 rotated
cross realisations (MID bins). Its first part re-measures F1's own randoms for the first 3 clusters with this code path.

## 4. Statistics (per cell = footing × h; C\* model; boost convention unless stated)

- **Cross offset of a class / cluster subset:** a_k = Σ_i Σ_{j∈MID} W_ijk B_jk Dx_ijk / Σ_i Σ_j W_ijk P_ij, P = X2's C\*
  model (X2's functions exec'd read-only, as X7), the all-source model for every source class (the cross channel uses P as
  normalisation only). Raw A_× (no leakage subtraction; X7's all-source cross leakage +0.003 is common to all classes and
  reported). The ALL row equals X7's A_× exactly.
- **Rotated-noise error:** σ_k = std over the 200 realisations; per-class two-sided p_k = fraction |a_k^(r)| ≥ |a_k|;
  class covariance C_rot from the joint realisations, inverse × Hartlap (R − K − 2)/(R − 1).
- **Bootstrap covariance (qualifier):** paired cluster bootstrap, 2000 draws, numpy default_rng([20261024, 900 + variable
  index]), ratio of sums per class.
- **Cluster-level splits** use X7's per-cluster arrays and X7's 200 rotations (step-0 extras), selection = the subset:
  patch (N: 100° < RA < 260°, else S); z halves (z ≤ median → 0); mass terciles (catalogue MGAS500, X7/X2's edges);
  straddle (f_main halves at the median of the 326); aniso (m2 halves at the median); off_deg halves (median).
- **Radial split within MID:** the three MID bins (0.46–0.67, 0.67–0.97, 0.97–1.42 Mpc) as 3 classes.

## 5. Consistency and correlation tests (graded on the cross offset)

For each variable v with classes a = (a_1..a_K):
- χ²_const = GLS of a constant (C_rot), dof K − 1, p_const.
- Δχ²_v = χ²_const − χ²_lin, lin = constant + slope × ordinal class index (K ≥ 3); for K = 2, Δχ²_v = χ²_const.
- **Candidate in a cell** if Δχ²_v ≥ 9 or p_const < 0.0027. Variables graded: tomo, mag2, mag4, size2, size4, psfT4, psfE4,
  psfx2, psft2, nbr2, dzls2, tile3, radial3, patch, z2, mass3, straddle2, aniso2, off2 (19).
- **Robust** if the same variable is also a candidate with C_boot.
- **Empirical look-elsewhere rate (reported):** the whole candidate rule applied to each of the 200 rotated realisations as
  data (C_rot unchanged); the fraction of realisations with ≥ 1 candidate.

**Nulls (graded):**
- N1 random points: the raw cross stack around F1's randoms (X7's `rand_x`) and around the extended set, in A units with
  the clusters' W, B, P, rotation errors. Pass if |Z| < 3 for both.
- N2 90° identity: max |stack(rotated positions) + stack| ≤ 1e-9 × max |stack| over all clusters, both channels, ALL class.
- N3 excess variance: per cluster x_i = Σ_j W_ij B_j Dx_ij / Σ_j W_ij B_j (MID), σ_i from its 200 rotations;
  χ²_cl = Σ_i x_i²/σ_i² against the same statistic over the 200 realisations; pass if p_var ≥ 0.0027.

Reported, not graded: the cluster offset with the extended randoms subtracted instead of F1's (cluster raw − extended mean),
with its rotation p; per-class p_k; the bootstrap and jackknife versions of every split.

## 6. E-mode systematics that could share the cause (reported sub-verdicts; never change the main class)

- **E1 source-density deficit:** per bin, Q_j = Σ_i n_ij(cluster) / Σ_i n̄_ij(F1 randoms) (unweighted counts of selected
  sources, h 0.672), MID = bins 3–5 pooled; cluster-bootstrap σ; also per mag2 and nbr2 class, and X7's weighted boost B.
- **E2 magnification:** δ_mag = 2(α − 1) κ̄_MID, κ_ij = Σ_model,ij × (mean Σ_crit⁻¹ of the bin's sources), Σ_model from
  X2's C\* (Σ = KAP·m2/m3), scaled by A_MID,STAT of the cell (bracket: unscaled law); α central and the two brackets of §2.
  Sub-verdict: CONSISTENT WITH MAGNIFICATION if Q_MID − 1 lies within the predicted bracket ± 2σ; EXCESS DEFICIT
  (obscuration / blending, f_obs reported) if below; EXCESS COUNTS (member contamination) if above.
- **E3 tangential splits:** a_t,k with each class's own W, B and the C\* P, paired-bootstrap covariance; the §5 tests on
  every variable. Sub-verdict: E-MODE SOURCE/CLUSTER DEPENDENCE FOUND (variables named) if Δχ² ≥ 9 or p_const < 0.0027 in
  all 4 cells; otherwise NONE. For nbr2 the far-neighbour half's Z_MID,STAT is reported as the blending-clean value.
- **E4 deficit counterpart:** if the deficit is obscuration or magnification (no shape bias), the boost B < 1 should not
  be applied; Z_MID under the clipped boost (B = 1, STAT and CAL) is reported as its tangential counterpart.

## 7. Frozen verdict classes (cross offset; graded at C\*, boost, 4 cells)

Preconditions: S0-1..S0-4 and this lane's checks pass; otherwise UNDECIDED (missing input named).
- **SYSTEMATIC IDENTIFIED:** ≥ 1 variable is a robust candidate in all 4 cells. The variable is named. Z_MID re-derived on
  the **clean subset** = that variable's classes with |a_k/σ_k| < 2 (if none, the class with the smallest |a_k|):
  A_MID,STAT (σ = max(bootstrap, jackknife)) and A_MID,CAL (σ² = σ_STAT² + s_×,clean² with s_×,clean² =
  max(0, a_clean² − σ_clean²); leakage and R−R terms as X7's all-source values) — graded Z_MID = CAL on the clean subset,
  class by X7's rule (REAL ≥ 3 in all 4 cells; NOT SIGNIFICANT < 2 in any; else MARGINAL). The tangential counterpart
  A_MID(all) − A_MID(clean) ± paired bootstrap is reported.
- **CONSISTENT WITH A FLUCTUATION:** no variable is a candidate in any cell (C_rot) and N1, N2, N3 pass. Graded Z_MID =
  Z_STAT (X7's: max(bootstrap, jackknife)), class by X7's rule, stated with the cross offset's p_× (rotations) beside it.
- **UNDECIDED:** otherwise (a candidate in some cells only or not robust, or a failed null). Z_MID STAT and CAL both
  reported; X7's MARGINAL is not changed.

## 8. Checks (each script prints `K# PASS|FAIL value threshold`, ends `... COMPLETE: n/m checks PASS.`, exit 0 iff all pass)

- `x11_measure.py`: M1 the ALL class reproduces the step-0 npz D, Dx, E, den, den_r (≤ 1e-9 × max|D|; relative ≤ 1e-9);
  M2 the ALL class rotations reproduce the step-0 extras cross rotations in MID (≤ 1e-6 × max, float32 storage);
  M3 classes partition: for every call, variable and bin, Σ_classes den + den(invalid) = den_ALL (relative ≤ 1e-12);
  M4 the 90° identity (N2); M5 rotated stacks centre on zero (|mean| ≤ 4 std/√R per h and class, MID); M6 RSS < 1 GB.
  `--mutate`: first 20 clusters, e2 sign flipped (M1 must FAIL).
- `x11_randoms.py`: R1 F1's randoms of the first 3 clusters re-measured with this code reproduce X7's Rmean / Rmeanx
  (≤ 1e-9 × max); R2 extended random rotations centre on zero (as M5); R3 RSS < 1 GB. `--mutate`: e2 flipped (R1 must FAIL).
- `x11_analysis.py`: K1 the ALL source class equals X7's A_× (4 cells, ≤ 1e-9) and the cluster-split machinery on all
  clusters equals X7's `s_n_x`, `p_x` (≤ 1e-9); K2 injection: a constant added to every class gives Δχ² = 0 and χ²_const
  unchanged (≤ 1e-9); 10 σ added to one class makes it a candidate; K3 the extended random stack's ALL class with F1's
  random positions reproduces X7's rand_x for the 3 re-measured clusters (via R1); K4 RSS < 1 GB. `--mutate`: the tangential
  data replace the cross in the split machinery (K1 must FAIL).

Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, ≤ 30 min each (a split into parts is an implementation amendment), never
while `compute_queue/heavyq.py status` shows low free memory; compute_queue/ and other lanes untouched; caches, rotation
products and large npz in session scratch; `.out` and `_results.json` (main and MUTATE) committed.

## 9. Stop rule

Splits, edges, thresholds, R, draw counts and the decision rule are fixed above. No post-hoc split, no new edge, no knob
scan, no new physics. A pattern seen in the numbers that is not one of §3–§6 is reported as an observation, never graded.

## AMENDMENTS (append-only; each labelled PRE-RESULT or POST-RESULT)
