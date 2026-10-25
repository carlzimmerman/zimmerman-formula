# HG1_hot_gas_selector — FROZEN CRITERIA (committed alone, before any script or number)

Written 2026-10-25. The owner asked: "Compare X-ray-bright and X-ray-faint groups and ellipticals at matched mass and
sigma, model-free against SPARC like ChatGPT's lane. Check data availability before anything else."

**Question.** At matched velocity dispersion, do groups with a detected hot X-ray atmosphere show a larger acceleration
excess over the matched SPARC disc relation than groups without one, after their hot gas is counted as baryons?

**Why this is open.** Excess is seen in clusters (model-free +0.416 dex vs SPARC, `reviews/matched_clumping_2026_10_24`),
groups (f22: +0.20 to +0.23 dex) and red/spheroidal lenses (~1.6×). Disc galaxies and blue lenses sit on the law. Every
excess class carries a hot atmosphere. The hot-gas variable has never been tested where it varies independently of
system class: in X19 (V7a/V7b) it was nonzero only for clusters, and groups were N/A. The elliptical arm was swung in
cm05–cm07 (SLUGGS/Alabi × O'Sullivan+01 L_X): the L_X signal vanished without the 9 group/cluster centrals
(ρ +0.06), so it was environment. **This lane does not rerun ellipticals**; that result stands and is cited.

Nothing here says the data favour the framework or ΛCDM. κ = ½ is FITTED. The comparison uses no a₀, no interpolation
function and no fitted cold component, so it is **footing-independent** (one result, not two; stated so the
"both footings" rule is not silently skipped). Not "theory closed".

## 1. Data (all on disk before this file; nothing downloaded)

| id | source | path | used for |
|---|---|---|---|
| D1 | Kourkchi & Tully 2017 groups (J/ApJ/843/16 table2: PGC1, Nm, sigmaV, logMK, logMd) | `real_research/data/kt2017_groups.tsv` | σ_LOS, member count |
| D2 | KT2017 galaxies (PGC, RA, Dec, group HRV, Ks mag, PGC1) | `real_research/data/kt2017_galaxies.tsv` | members, centre, radius, L_K |
| D3 | eRASS1 cluster/group catalogue as used by CFG687 (col 1 RA, 2 Dec, 3 z, 5 Mgas500 [1e11 M☉], 8 R500 [kpc]) | `../_external_data/cfg687_inputs/erass1_main.tsv` | X-ray detection flag, hot-gas mass |
| D4 | SPARC Lelli+2016 rotation models, as read by the matched-clumping lane | the matched-clumping lane's `SPARC_Lelli2016c.mrt` source | the disc reference |

`logMK` and `logMd` (D1) are NOT used: logMK is a luminosity-to-halo-mass conversion and logMd a model dynamical mass.

## 2. Construction (fixed now)

- **Sample.** D1 groups with Nm ≥ 5 (primary) and Nm ≥ 10 (variant), sigmaV > 0, and at least 5 members in D2 with
  Ks mag and the group HRV. Distance d = HRV / H0, H0 = 67.70 km/s/Mpc (CFG689 native); variant 73.0. Groups with
  HRV < 600 km/s are dropped (peculiar velocities dominate).
- **Footprint.** eRASS1 covers Galactic longitude 179.94° ≤ l ≤ 359.94°. Only groups whose PGC1 galaxy lies in that
  range and at |b| ≥ 10° are graded. l, b come from the standard J2000 → Galactic rotation (IAU 1958 pole RA 192.85948°,
  Dec 27.12825°, l_NCP 122.93192°), coded and checked (K2).
- **X-ray flag.** X-BRIGHT if an eRASS1 entry lies within projected 0.5 Mpc of the PGC1 galaxy at the group distance
  and |c z_eRASS − HRV| ≤ 1500 km/s. Otherwise X-FAINT. If two match, the nearest in projection is used.
- **Radius.** Luminosity-weighted centroid of the members; R_h = median projected member distance from it;
  r = (4/3) R_h (Wolf-style deprojection, the record's convention).
- **Stars.** L_K from Ks with M_K,☉ = 3.28 and no extinction correction; M★ = Υ_K L_K, Υ_K = 0.6 (variants 0.5, 0.8).
  M★(<r) = 0.5 M★,tot.
- **Hot gas (X-BRIGHT only).** β-model (r_c = 0.15 R500, β = 2/3, the F1/CFG687 convention) normalised to eRASS1
  Mgas500 at R500, evaluated at r. X-FAINT primary gas = 0; variant: gas = 0.1 M★,tot (a generous undetected atmosphere).
  No cold gas (no HI in D2) in either arm, the same for both, disclosed.
- **Accelerations.** g_bar = G M_b(<r) / r² (distance-independent by construction: M ∝ d², r ∝ d). g_obs = 3 σ² / r
  (∝ 1/d; the shift is common to both arms).
- **Disc reference (model-free).** Exactly the matched-clumping rule: at each target's g_bar, interpolate log g_obs within
  adjacent accepted SPARC radial segments, max separation 0.30 dex; one median per SPARC galaxy over multiple crossings;
  reference = median over galaxies; need ≥ 8 galaxies, else the group is UNSUPPORTED and dropped (count reported).
  Δ_i = log10 g_obs,i − reference(g_bar,i).

## 3. The statistic

- Stratify by log σ in bins 0.1 dex wide (fixed edges at multiples of 0.1). In each bin with ≥ 1 X-BRIGHT and ≥ 1
  X-FAINT group, take median Δ(bright) − median Δ(faint). D = the mean of the bin differences, weighted by
  min(n_bright, n_faint).
- Uncertainty: 2000 bootstrap draws, resampling groups within each arm and bin and the SPARC reference galaxies globally;
  95% percentile interval. Seed 20261025.
- Reported only: unstratified medians per arm; Δ versus log σ per arm; D with Nm ≥ 10.

## 4. Classes (decided on the primary; variants reported)

| class | rule |
|---|---|
| UNDERPOWERED | fewer than 6 X-BRIGHT or 6 X-FAINT groups in shared σ bins, or the pre-flight power (§5) < 50% |
| HOT TRACKS | D ≥ +0.15 dex and the 95% interval excludes 0 |
| HOT DOES NOT TRACK | the 95% upper bound on D < +0.10 dex |
| UNDECIDED | anything else |

A HOT TRACKS result is a correlation, not a mechanism. It would not establish that hot gas sources cold energy. A HOT
DOES NOT TRACK result closes the hot-atmosphere selector at group scale.

## 5. Checks (each must pass, or the run stops and says so)

- **K1** The SPARC reference reimplementation reproduces the matched-clumping X-COP cluster median Δ = +0.416 dex to
  ±0.005, from that lane's committed inputs.
- **K2** The Galactic transform: the North Galactic Pole and the Galactic Centre (RA 266.405, Dec −28.936) map to b = 90°
  and (l, b) ≈ (0, 0) to 0.01°.
- **K3** g_bar is unchanged (to 1e-12 relative) when every distance is scaled by 1.1.
- **Pre-flight power (computed before Δ is examined):** with the real arm sizes and bins, plant D = +0.20 dex on
  Gaussian Δ of scatter 0.25 dex (f22's measured group scatter) and report the fraction of 500 draws classed
  HOT TRACKS.
- **MUTATE=1:** (a) shuffle the X flag within σ bins: the class must not be HOT TRACKS in ≥ 90% of 200 shuffles;
  (b) add +0.30 dex to every X-BRIGHT Δ: the class must be HOT TRACKS. A MUTATE run exits 1 if its controls behave as
  required (so the plain run exits 0, the MUTATE run exits 1).

## 6. Disclosed limits (fixed now, not discovered later)

- eRASS1 non-detection is not proof of no hot gas. Very extended nearby groups can be missed or split, and the catalogue
  is a cluster selection. X-FAINT means "not in this catalogue".
- σ from KT2017 differs from other group catalogues by up to 0.4 dex in boost (f22); only KT2017 σ is used, so that
  bias is common to both arms but not removed.
- Matching on σ does not match formation history, environment or morphology mix.
- Arm sizes are small: about 21 eRASS1 entries lie inside the KT2017 volume (z < 0.0117), before footprint and
  matching. UNDERPOWERED is a likely outcome and is a result, not a failure.
- Post-hoc motivation: the hypothesis was formed after seeing the class pattern (clusters, groups, red lenses vs discs).
  This is not a blind test.

Run: `python3 hg1_hot_gas_selector.py` and `MUTATE=1 python3 hg1_hot_gas_selector.py`; outputs `hg1_*.out`, `hg1_*.json`,
`hg1_*_MUTATE.*` written separately.
