# X13_source_size_test: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Inputs and classes:
`ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², reported side by side, never
pooled. No dark-matter particle. No new fitted constant. Never "theory closed". Never "the data favour the framework".

## 0. Question

X11 (`X11_cross_shear_diagnosis/`, criteria 9a105431c9, result c1cd5455a5) found that the eRASS1 × KiDS-1000 MID
(0.46–1.42 Mpc) tangential excess depends on source size (lensfit `bias_corrected_scalelength_pixels`) in all 4 cells:
small half A_MID 1.10–1.24, large half 1.86–2.11 (Δχ² 15.9–17.4); quartiles 0.81–0.91 / 1.34–1.49 / 1.29–1.49 /
2.04–2.44. Class boosts, count deficit and boost convention do not explain it. **Is the size dependence a source-side
measurement / calibration effect, or a cluster-specific signal?**

**Seen before freezing (disclosed).** BRIEF; X11 README, criteria, ledger, all scripts and the size numbers and keys of its
committed JSON (`tangential_Z_per_class`, `E3`, the size edges 1.4136 / 1.9020 / 2.5378 px); X7 README and scripts; F2
and P2 READMEs and the measurement parts of their scripts; the KiDS FITS column list; the layout of `lr_lenses.npz`
(181,477 lenses, z 0.10–0.50) and `cfg96_stack.npz` (50 patches); the SOM n(z) file format (5 bins, 0.05 steps, blind C).
**A back-of-envelope estimate, made from X11's published quartile pattern and edges only, motivated test (f):** if the
lensfit scalelength is a semi-major-axis length, a cut on it selects on the shear itself (a sheared source's major axis
grows by g∥), and with the log-normal width implied by X11's quartile edges and |e| ≈ 0.25–0.3 the expected half ratio is
of order 1.4–1.7. (f)'s graded prediction is computed from catalogue sums (§5f), not from this estimate. **No number of
this lane exists.**

## 1. Step 0: reproduce X11's size-half numbers with X11's code on a rebuilt cache

- **Cache** (session scratch, not the repo) rebuilt from the raw KiDS FITS by X7's `x7_extract.py`, then X7's
  `x7_psf_regression.py`, then X11's `x11_extract_extra.py`.
- **Runner `x13_step0.py`** executes X7's and X11's committed scripts read-only: it re-executes itself with
  `MallocMediumZone=0` first (so no script re-executes itself under its own path), reads the source text, checks its sha256
  against the committed blob (X7 at b1a2ffcb6b as recorded by X11; X11 at c1cd5455a5), applies only declared path
  substitutions (each must occur the declared number of times), and executes it. Substitutions: the lane dir `HERE` → this
  lane; output names `x7_*` → `x13_s0_x7_*` and `x11_*` → `x13_s0_x11_*` (this lane); X7's per-cluster npz → scratch;
  X11's `import x11_common` and its sha256 path → X11's dir (read-only, `sys.dont_write_bytecode`); X11's reads of its own
  lane products → the renamed step-0 products. Order: X7 extract, X7 regress, X7 measure, X11 extract_extra, X11 measure,
  X11 randoms (part 1, part 2), X11 analysis.
- **S0 checks (`x13_s0_check.py`):**
  - S0-1: the 7 shared cache columns (ra, dec, e1, e2, w, zb, cell) have X7's committed sha256.
  - S0-2: every array of the step-0 `x7_measure_percluster.npz` equals X7's committed npz (max |Δ| = 0).
  - S0-3: the step-0 X11 analysis JSON equals X11's committed JSON (c1cd5455a5) to ≤ 1e-9 absolute on:
    `tangential_Z_per_class` (16 keys × A, s_boot, s_jk, s_STAT, Z_STAT), `E3.<cell>|size2` and `|size4` (a, sig,
    boot.dchi2, boot.p_const), `E3_clip` for the same keys, `all_MID` (4 cells, all numbers), `Z_MID`; and `verdict`,
    `E3_sub` equal as strings.
  - S0-4: all checks of the step-0 runs PASS, except X7 extract E1, which is N/A (no F1 cache exists in this session; S0-1
    is the replacement).
  - `--mutate`: the size2 class labels are swapped (0 ↔ 1) in the S0-3 comparison (S0-3 must FAIL).
- If S0 fails, nothing downstream is graded (UNDECIDED, the missing input named).

## 2. New catalogue columns and frozen class edges (`x13_extract.py <cache> [--mutate]`; catalogue only, no shear)

Re-reads the KiDS FITS with X7's filter and order (finite RA, DEC, e1, e2; weight > 0; Z_B ≤ 1.2; stable sort by the 0.2°
cell) and writes to the scratch cache: `psfD` = PSF_Q11·PSF_Q22 − PSF_Q12² (r_psf ≡ psfD^¼), `snr` = model_SNratio,
`frad` = FLUX_RADIUS (float32). From the cache: |e| = √(e1² + e2²); circularised size **r_ab = size·√((1 − |e|)/(1 + |e|))**.
Validity: size finite > 0 (X11's rule); psfD finite > 0; snr finite > 0; frad finite > 0; |e| < 1. Invalid → no class of
that variable.

Edges (exact lensfit-weight quantiles, X11's `wquant` algorithm, valid rows):
- `psf2|q`: the w-median of psfD inside each of X11's size quartiles q (4 edges).
- `snr2|q`: the w-median of snr inside each size quartile (4 edges).
- `circ4`: w-quartiles of r_ab; `circ2` = its median.
- `frad2`: w-median of frad.
- Bands: `band` = |ln size − ln E| < 0.05 for E = each of X11's three size4 edges (3 classes; the middle one is the size2
  edge); `cband` = |ln r_ab − ln E_circ2| < 0.05 (1 class).

Checks: X1 the re-extracted e1, after the reorder, is byte-identical to the cache's e1.npy and the counts agree; X2 every edge
finite, each within-quartile half holds 40–60 % of its quartile's weight, each circ/frad class ≥ 10 % of the valid weight;
X3 peak RSS < 1 GB. `--mutate`: the reorder is skipped (X1 must FAIL).

## 3. Cluster measurement (`x13_measure.py <cache> <step-0 scratch> <work> [--mutate]`)

X11's `x11_common.py` copied with provenance (sha256 recorded) as `x13_common.py`, with X11's VARS replaced by the classes
below and 7 extra per-class sums. Everything else is X11's/X7's: F1's 326 clusters, F1's random positions (seed 20261022,
acceptance), X7's estimator, Σ_crit, bins, m = −0.01, R = 200 rotated cross realisations (MID, X7's draws).

| id | classes | use |
|---|---|---|
| ALL | 1 | reproduction |
| size2 / size4 | 2 / 4 (X11's edges) | reference effect, (a), (b), (f) |
| tomo×size2 | 10 | (d) |
| size4×psf2 | 8 (PSF-size halves inside each size quartile) | (c) resolution |
| size4×snr2 | 8 (SNR halves inside each size quartile) | (c) SNR |
| circ2 / circ4 | 2 / 4 | (f) shear-invariant size |
| frad2 | 2 | (f) reported |
| band | 3 | (f) selection response of size2/size4 |
| cband | 1 | (f) alternative-convention response of circ2 |

Extra per-class, per-bin sums over the cluster call's selected sources (both h): Σ w, Σ w·Z_B, Σ w·s_B (s_B = Σ_crit⁻¹ from
Z_B), Σ ww·ln size, Σ ww·ln r_psf, Σ ww·ln snr, Σ ww·|e| (ww = w·s_B², X7's weight).

Checks: M1 the ALL class reproduces the step-0 X7 npz (D, Dx, E, den, den_r; ≤ 1e-9 × max|D|, relative ≤ 1e-9);
M2 the size2 and size4 classes reproduce the step-0 `x11_measure_classes.npz` (D, Dx, E, den, den_r, Rt; same tolerances);
M3 every partitioning variable (all but band, cband) satisfies Σ_classes den + invalid den = ALL den (relative ≤ 1e-12);
M4 peak RSS < 1 GB. `--mutate`: first 20 clusters, e2 flipped (M1 must FAIL).

## 4. Galaxy-lens measurement for (e) (`x13_galaxy.py <cache> <work> [--mutate]`)

- **Lenses:** F2's lens catalogue `real_research/data/lensing_rar/lr_lenses.npz`, all 181,477 (z 0.10–0.50), with F2's 50
  jackknife patches (`cfg96_stack.npz` `patch`).
- **Estimator:** P2's `measure()` (`P2_spec_isolated_lensing/p2_spec_isolated_lensing.py`, "native" convention: Z_B >
  z_l + 0.2, ww = w·Σ_crit⁻², flat Ω_m 0.3085, h 0.679), copied with provenance and extended with per-class sums, run on
  this lane's cache (whose 7 columns equal F1's reader cache, S0-1). P2's 15 bins (0.03–3 Mpc); bins 0–11 (to 1.19 Mpc)
  are measured. **Graded range "in": bins 0–7 (0.03–0.35 Mpc)**; O1 (bins 8–11) reported.
- **Source classes:** ALL; size2 (X11's edge); circ2; band at the size2 edge (for the predicted response). Sums per class,
  bin and patch: WG, WX, WW, W2, NN and Σ ww·|e|.
- **Random points:** one per lens, numpy default_rng(20261026): uniform angle, 1–3° away (F1's placement), the lens's z;
  kept if its "in"-range ALL source count exceeds 0.5 × its lens's (F1's acceptance), otherwise dropped (no retry); each
  random carries its lens's patch.
- Sources are loaded per 0.2° declination row with its two neighbours (θ_max ≤ 0.19° for every lens); lenses in pass 1,
  randoms in pass 2. If a run would exceed 30 min it is split into parts by row ranges (implementation, same sums).
- Checks: G1 P2's K0b on the first 2,000 lenses of the catalogue, P2's "record" (CFG110) convention vs
  `cfg110_perlens.npz` (WW ratio in [0.90, 1.000001], median ΔΣ ratio in [0.95, 1.05], P2's thresholds); G2 classes
  partition (size2 halves + invalid = ALL; circ2 likewise; relative ≤ 1e-12); G3 peak RSS < 1 GB. `--mutate`: cross shear
  in place of tangential (G1 must FAIL).

## 5. Statistics (per cell = footing × h, C\* model, X7's boost convention; class amplitude as X11's `src_split`)

**Reference.** A_k = Σ_i Σ_{j∈band} W_ijk B_jk D_ijk / Σ_i Σ_j W_ijk P_ij (W = 1/E_k², B = class boost, P = X2's C\* model).
Δ_obs = A_L − A_S and ρ_cl = A_L/A_S for the size2 halves in MID. Paired cluster bootstrap: 2000 draws,
default_rng([20261024, 1300 + test index]), ratio of sums; σ_STAT = max(bootstrap, X2's 30-patch jackknife). Class means
of a source variable v: v̄_k = Σ W B P v_ijk / Σ W B P with v_ijk = Σ ww v / Σ ww. Fractions: f = Δ_pred / Δ_obs, with the
same bootstrap draws; σ_f = half the 16–84 % range. A fraction is **DETERMINED** if σ_f ≤ 0.40 (no wider than the 0.30–0.70
gap).

**(a) Bands.** The size2 split in INNER (bins 0–2, 0.15–0.46 Mpc) and OUTER (bins 6–7, 1.42–3.0 Mpc; the record's OUTER,
used for the brief's "1–3 Mpc"). Per band: A_S, A_L, ρ, Δ with bootstrap σ; and ρ_band − ρ_MID (paired bootstrap).
Reported sub-verdict per band: SAME AS MID if |ρ_band − ρ_MID| < 2σ and |ρ_band − 1| ≥ 2σ; NONE if |ρ_band − 1| < 2σ and
|ρ_band − ρ_MID| ≥ 2σ; NOT DECISIVE otherwise.

**(b) Random points.** The tangential stack of F1's random points per size2 class in A units (cluster W, B, P; X7's
`rand_t` form) in MID, with σ from the 200 rotated random-mean cross realisations of the class (`rotRx`); also L − S. Null
PASSES if |Z| < 3 for S, L and L − S in all 4 cells. INNER/OUTER random stacks with bootstrap σ reported.

**(c) Resolution and SNR at fixed size.** GLS over the 8 classes (bootstrap covariance, Hartlap):
- resolution: A_c = a + β_s x_c + β_p p_c (x = ln size, p = ln r_psf; classes size4×psf2). A dependence on resolution
  (any function of size/r_psf) gives β_p = −β_s; on size alone β_p = 0. **f_res = (−β_p)·[(x̄_L − x̄_S) − (p̄_L − p̄_S)] / Δ_obs.**
- SNR: A_c = a + β_s x_c + β_n n_c (n = ln snr; classes size4×snr2). **f_snr = β_n (n̄_L − n̄_S) / Δ_obs.**
- Reported: the within-quartile V-half differences and the fitted coefficients.

**(d) Redshift calibration.**
- Reported: per tomographic bin and size half, the w-weighted mean Z_B and mean s_B (catalogue-wide and in the cluster
  MID apertures at h 0.672), and each bin's share of the class weight.
- **H_SOM** (KiDS-1000 calibrates n(z) per tomographic bin, not per size): every source of bin t has the bin's SOM n_t(z)
  as its true redshift distribution. With U_ijkt = Σ w s_B and V_ijkt = Σ w s_B² (class k, bin t), and
  s̄_T,t(z_l, h) = Σ_z n_t(z) s(z_l, z) / Σ_z n_t(z) (F1's distances, z at the file's bin centres, s = 0 for z ≤ z_l), the
  estimator's factor is b_ijk = Σ_t s̄_T,t U_ijkt / Σ_t V_ijkt and b_k = Σ W B P b_ijk / Σ W B P.
  **f_d = A_ALL (b_L − b_S)/b_ALL / Δ_obs** (A_ALL = X7's all-source A_MID; b_ALL from both halves pooled). The naive ratio
  of mean s_B between halves is reported. The SOM n(z) is for the full bin; bins cut by Z_B > z_l + 0.2 are an
  approximation (the cut-bin weight share is reported).

**(e) Independent lens sample.** Per class: ΔΣ_kj = WG/WW (lenses) − WG/WW (randoms), stacked sums; boost
B_kj = (Σ_lens WW_kj/N_lens)/(Σ_rand WW_kj/N_rand); **A_k = Σ_j WW_kj T_j B_kj ΔΣ_kj / Σ_j WW_kj T_j², T_j = 1/R_j** (shape
only; it cancels in the ratio when the halves share a profile shape). ρ_gal = A_L/A_S over "in", σ from the paired
delete-one jackknife over the 50 patches. No model enters, so ρ_gal is footing-independent and is compared with each cell's
ρ_cl, σ_diff² = σ_gal² + σ_cl² (independent lens samples). Classes per cell:
- **E-MATCH**: |ρ_gal − ρ_cl| < 2σ_diff and (ρ_gal − 1)/σ_gal ≥ 2 (a size effect in galaxies, consistent with clusters);
- **E-NULL**: |ρ_gal − 1| < 2σ_gal and |ρ_gal − ρ_cl| ≥ 2σ_diff;
- **E-AMBIGUOUS**: consistent with both; **E-OTHER**: consistent with neither.
(e)'s class is the one common to all 4 cells, else MIXED. Reported: O1 and in+O1 ratios, clipped boost, circ2 ratio, the
predicted selection ratio for galaxy sources.

**(f) Shear-induced size selection (source-side, split-induced).** Assumption (ledger B11): the lensfit scalelength is the
semi-major-axis length and e = (a − b)/(a + b). Then a shear g changes ln size by g∥ = g·cos 2(θ_e − θ_t) to first order,
and a cut on size selects on the shear. For a size class between edges E_lo < size < E_hi, the selection response is
R_k = ½ [D(E_lo) − D(E_hi)] / Σ_k ww per cluster-bin (D(E) = Σ_band(E) ww|e| / 0.1; an open edge contributes 0), class
effective R_k = Σ W B P R_ijk / Σ W B P, and A_k = A₀(1 + R_k), A₀ ≈ A_ALL. **f_sel = A_ALL (R_L − R_S) / Δ_obs** (size2).
r_ab is invariant to first order under shear, so the prediction for circ2/circ4 is R = 0 (ratio 1). **Gate:** f_sel counts
only if the circ2 ratio is consistent with 1 (|ρ_circ − 1| < 2σ, all 4 cells); otherwise f_sel is treated as 0. Reported:
the size4 predictions vs measurement; the alternative convention (scalelength already circularised: size2 response 0,
circ2 response −½ D_c/Σ ww per half sign, from `cband`); frad2.

## 6. Frozen decision (preconditions: S0 and every check of this lane pass; otherwise UNDECIDED with the input named)

A mechanism m ∈ {res, snr, d, sel} **accounts for ≥ 70 %** if f_m is DETERMINED and ≥ 0.70 in all 4 cells (sel: gate
passed); **< 30 %** if DETERMINED and < 0.30 in all 4 cells (sel with a failed gate counts as < 30 %).
- **SOURCE-SIDE SYSTEMATIC** if (e) = E-MATCH, and/or some mechanism accounts for ≥ 70 %. The mechanism(s) are named.
- **CLUSTER-SPECIFIC** if (e) = E-NULL and every mechanism accounts for < 30 %.
- **UNDECIDED** otherwise.
(a) and (b) are reported sub-verdicts and never change the class.

## 7. Correction under SOURCE-SIDE SYSTEMATIC (frozen method; both footings, both h)

The correcting mechanism is the qualifying one with the largest minimum-over-cells f; if none qualifies (E-MATCH only),
the galaxy calibration. Per size2 class k with per-cluster sums num_k, den_k (X11's `src_split`):
- sel: c_k = 1 + R_k; d: c_k = b_k; galaxy: c_k = A_gal,k / A_gal,ALL; **A_corr = Σ_k num_k / c_k / Σ_k den_k**.
- res / snr: **A_corr = Σ_k [num_k − b_V (V̄_k − V̄_pool) den_k] / Σ_k den_k**, b_V the fitted coefficient (−β_p or β_n),
  V̄_pool the pooled mean of both halves.
σ_corr = max(paired bootstrap with c_k, R_k, b_k recomputed per draw, 30-patch jackknife); for the galaxy calibration the
galaxy jackknife variance is added in quadrature (linear propagation). **Z_MID,corr = (A_corr − 1)/σ_corr**, class by X7's
rule (REAL if ≥ 3 in all 4 cells; NOT SIGNIFICANT if < 2 in any; else MARGINAL), stated beside X11's Z_STAT. All other
mechanisms' corrected A are reported, not graded. Under the other verdicts no correction is applied and X11's Z_STAT with
its size caveat stands.

## 7b. Analysis checks (`x13_analysis.py <step-0 scratch> <work> <cache> [--mutate]`)

K1 the size2 and size4 tangential A of this lane's measurement equal X11's committed `E3` values, and the size2 s_boot with
X11's draws equals `tangential_Z_per_class` (≤ 1e-9, 4 cells); K2 selection-response injection: 2·10⁶ synthetic sources
(log-normal size, |e| from a Rayleigh-like draw, isotropic angles, tangential g = 0.02 applied as ε' = (ε + g)/(1 + g ε)
and ln a' = ln a + Δ ln a from the exact transform), split at the median: measured (⟨e_t⟩_k/g − 1) equals the §5f
formula within 3 Monte-Carlo σ for both halves, and the circularised split's response is within 3σ of 0; K3 GLS injection:
exact synthetic class amplitudes A = a + β_s x + β_v y recover f_res and f_snr to ≤ 1e-9; K4 peak RSS < 1 GB.
`--mutate`: the cross shear replaces the tangential in every class amplitude (K1 must FAIL).

## 8. Runs

`OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, ≤ 30 min each (split into parts if needed: an implementation amendment),
never while `compute_queue/heavyq.py status` shows low free memory; `compute_queue/` and other lanes untouched (X7, X11,
F2, P2, X2, F1 files read only). Caches and large npz in session scratch; `.out` and `_results.json` (main and MUTATE)
committed.

## 9. Stop rule

Splits, edges, bands, thresholds, draws, the decision rule and the correction method are fixed above. No post-hoc split, no
new edge, no knob scan, no new physics. A pattern outside §5 is reported as an observation, never graded.

## AMENDMENTS (append-only; each labelled PRE-RESULT or POST-RESULT)
