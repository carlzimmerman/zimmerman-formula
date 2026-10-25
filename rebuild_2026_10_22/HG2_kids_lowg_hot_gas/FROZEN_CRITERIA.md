# HG2_kids_lowg_hot_gas — FROZEN CRITERIA (committed alone, before any script or number)

Written 2026-10-25. This retries HG1 (`../HG1_hot_gas_selector`, frozen 25bb540d4d, result 65d1d50bd9: UNDERPOWERED) with a
reference that reaches the groups' accelerations. HG1 failed on coverage: the groups' half-mass g_bar has median 10^−13.0
m/s² (5–95%: −13.7 to −11.9), and SPARC disc segments stop near 10^−12, so 182 of 190 groups had no reference.

**Question.** At matched velocity dispersion, do galaxy groups with a detected hot X-ray atmosphere (eRASS1) show more
acceleration excess than groups without one, once their hot gas is counted as baryons? The excess is measured against the
KiDS-1000 lensing RAR of isolated late-type (blue) galaxies, which reaches 10^−14.9.

**Why this reference.** On the record the blue isolated lenses sit on the law in the groups' g_bar range (CFG829:
A = 1.016 ± 0.086 for 10^−13.3 ≤ g_bar < 10^−11.9). That reading is FRAGILE (CFG840: A 0.90–1.31 across window and lens-M★
variants). This lane does **not** use the law or A. It uses the blue-lens data points themselves as an empirical cold-gas
reference curve. So the result does not depend on CFG829's fragility, and the reference level largely cancels in D (§3),
which is a difference between the two group arms.

Nothing here says the data favour the framework or ΛCDM. κ = ½ is FITTED. The graded statistic uses no a₀, no
interpolation function and no fitted cold component, so it is **footing-independent**: one result, not two. This is
stated here so the "both footings" rule is not silently skipped. a₀ enters only check K1 (a reproduction of CFG829's
canonical number, to prove the loader), never the class. Not "theory closed".

## 1. Data (all on disk before this file; nothing downloaded)

| id | source | path | used for |
|---|---|---|---|
| D1–D3 | KT2017 groups and galaxies, and eRASS1, exactly as in HG1 §1 | as HG1 | groups, X flag, hot gas |
| D4 | Brouwer+2021 KiDS-1000 isolated lensing RAR, colour bin 1 (u−r < 2.5) ESD + full covariance | `real_research/data/lensing_rar/brouwer2021_rar/Fig-8_RAR-KiDS-isolated_Colorbin_1.txt`, `..._Colorbins_covmatrix.txt` (sha256 prefixes 377ced17a8896b6a, 85573dde45dce3d7) | the reference |
| D5 | the same, all isolated lenses, no colour cut | `Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt` + covmatrix | reported variant only |

D4/D5 are gitignored public data (as in CFG829). They are converted exactly as CFG829 does: g_obs = 4 G ESD_t / bias × pc,
covariance / bias column, G = 4.52e-30 pc²/(M☉ s²), pc = 3.086e16 m.

Pre-flight facts read before this file (no Δ was computed or seen): D4 has 15 points from g_bar 10^−14.86 to 10^−11.41,
spaced 0.245 dex, per-point S/N 2.7–6.8. HG1's built groups span g_bar 10^−14.1 to 10^−10.8. The X-BRIGHT groups span
10^−12.54 to 10^−11.47. Eleven X-BRIGHT groups fall in log σ bins that also hold X-FAINT groups.

## 2. Construction (fixed now)

- **Groups.** HG1's `build()` is imported read-only and used unchanged, with HG1's primary settings: Nm ≥ 5, H0 = 67.70,
  Υ_K = 0.6, X-FAINT gas = 0, the 0.5 Mpc / 1500 km/s eRASS1 match, the eRASS1 footprint, the β-model hot gas,
  g_bar = G M_b(<r)/r², g_obs = 3σ²/r at r = (4/3) R_h. Every construction line of HG1 §2 except its SPARC reference applies.
- **Reference (model-free).** log g_ref(g_bar) is linear interpolation of log g_obs against log g_bar between the two
  adjacent D4 points that bracket the group's g_bar. A group whose g_bar lies outside [10^−14.86, 10^−11.41] is
  UNSUPPORTED and dropped (count reported). No extrapolation, no smoothing, no law.
- **Δ_i = log10 g_obs,i − log10 g_ref(g_bar,i).**

## 3. The statistic (identical to HG1 §3)

- Stratify by log σ in 0.1 dex bins (edges at multiples of 0.1). In each bin with ≥ 1 X-BRIGHT and ≥ 1 X-FAINT group, take
  median Δ(bright) − median Δ(faint). D = the mean of the bin differences, weighted by min(n_bright, n_faint).
- **Uncertainty.** 2000 bootstrap draws, seed 20261025. Each draw resamples groups with replacement within each arm, and
  redraws the D4 reference g_obs from a multivariate Gaussian with the D4 covariance. Any drawn reference value ≤ 0 is set
  to 1% of its central value (counted and reported). 95% percentile interval.
- **Reported only, never graded:** unstratified median Δ per arm (this is where the groups' level against blue lenses shows,
  i.e. whether the f22 group excess appears against this reference); D with Nm ≥ 10, H0 = 73, Υ_K 0.5 / 0.8, X-FAINT gas
  0.1 M★; D with the reference g_bar shifted −0.2 and +0.2 dex (CFG840's lens-M★ variants); D against D5 instead of D4.

## 4. Classes (decided on the primary; variants reported). Identical to HG1 §4.

| class | rule |
|---|---|
| UNDERPOWERED | fewer than 6 X-BRIGHT or 6 X-FAINT groups in shared σ bins, or the pre-flight power (§5) < 50% |
| HOT TRACKS | D ≥ +0.15 dex and the 95% interval excludes 0 |
| HOT DOES NOT TRACK | the 95% upper bound on D < +0.10 dex |
| UNDECIDED | anything else |

A HOT TRACKS result is a correlation, not a mechanism. It would not establish that hot gas sources cold energy. A HOT DOES
NOT TRACK result closes the hot-atmosphere selector at group scale, for this sample and this X-ray catalogue.

## 5. Checks (each must pass, or the run stops and says so)

- **K1 loader.** The D4 loader reproduces CFG829's canonical blue-lens amplitude A = 1.016 ± 0.086 (ν_e, a₀ 9.3603e-11,
  window [10^−13.3, 10^−11.9)) to ±0.001 in A and σ_A. a₀ appears only here.
- **K2 Galactic transform.** HG1's K2 (NGP → b = 90°, GC → (0, 0) within 0.1°).
- **K3 distance invariance.** HG1's K3 as amended by its A1 (match radius scaled with the distances; X flags identical;
  g_bar unchanged to 1e-6 relative).
- **K4 builder identity.** The imported builder gives HG1's sample exactly: 190 groups, 14 X-BRIGHT, 176 X-FAINT.
- **K5 interpolation.** Evaluated at each interior D4 point's own g_bar, the reference returns that point's g_obs to 1e-9
  relative.
- **Pre-flight power (computed before Δ is examined; HG1 §5 rule):** with the real arm sizes and bins of the supported
  groups, plant D = +0.20 dex on Gaussian Δ of scatter 0.25 dex (f22's group scatter), reference held fixed, and report the
  fraction of 500 draws classed HOT TRACKS (200-draw group bootstrap per draw).
- **MUTATE=1** (writes `*_MUTATE.*`, never the plain outputs): (a) shuffle the X flag within σ bins: D ≥ +0.15 must occur
  in ≤ 10% of 200 shuffles (the fraction **not** HOT-TRACKS-sized must be ≥ 0.90; HG1's rule); (b) multiply every X-BRIGHT g_obs by
  10^0.30: the class must be HOT TRACKS (500-draw bootstrap, power taken as 1). The MUTATE run exits 1 if both controls
  behave as required; the plain run exits 0.

## 6. Disclosed limits (fixed now, not discovered later)

- **Different probes.** The reference is stacked weak lensing of isolated galaxies at 30 kpc–3 Mpc (projected ESD, then
  B21's conversion); the groups use a dynamical 3σ²/r at the half-mass radius. A level offset between the two is common to
  both arms and cancels in D, but it does not cancel in the per-arm medians, which are therefore reported, not graded.
- **Reference baryons.** B21's lens g_bar is stars plus an estimated cold gas, as a point mass. The groups count stars (and
  hot gas, BRIGHT only), with no cold gas in either arm (HG1 A6). The reference curve is shallow in this range, so the shape
  effect on D is second order; the ±0.2 dex variants (§3) bound it.
- **D's dependence on the reference is only through its slope** between the two arms' g_bar. The BRIGHT arm sits at higher
  g_bar (counted hot gas raises it). A reference slope error therefore leaks into D. This is why the ±0.2 dex and D5
  variants are reported.
- Every HG1 limit carries over: eRASS1 non-detection is not proof of no hot gas (X-FAINT = "not in this catalogue"); KT2017 σ
  bias is common but not removed; σ matching does not match richness, history or morphology (BRIGHT groups are richer at
  fixed σ); small arms, so UNDERPOWERED is a possible result, not a failure.
- B21's own "hot gas" RAR variant (`Fig-4_RAR-KiDS-isolated_hotgas`) is not used: its lens hot gas is modelled, not measured.
- Post-hoc motivation: the hypothesis was formed after seeing the class pattern (clusters, groups, red lenses vs discs). HG1's
  coverage failure was seen before this file. This is not a blind test.

Run: `python3 hg2_kids_lowg_hot_gas.py` and `MUTATE=1 python3 hg2_kids_lowg_hot_gas.py`; outputs `hg2_kids_lowg_hot_gas.out/.json`
and `hg2_kids_lowg_hot_gas_MUTATE.out/.json`, written separately.
