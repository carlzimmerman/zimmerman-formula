# A26 — the fork settled on dwarfs: **LAW-FIRST**

Lane A26, `DS_FINAL_2026_10_21`. Script `a26_checks.py`, output `a26.out`, numbers `a26_results.json`,
per-system table `a26_rar.csv`, mutation `MUTATE.md`. Verdict line: **`A26 COMPLETE: 11/11 checks PASS.`**

## Claim

The 92-dwarf Local Volume Database sample decides FINAL_THEORY sec 5b in favour of **law-first**, and
decides it in the *opposite direction* to the medium-first reading. Below `M_crit = 3.87e5 Msun` the
systems are not Newtonian: the median kernel-free boost is `g_obs/g_bar = 140` where medium-first
requires `1`; the median offset from the law is `+0.651 +- 0.090` dex (Wolf estimator) or `+0.173` dex
with `g_obs = sigma^2/r`, i.e. never the `-1.49` dex deficit medium-first demands; the step in the
residual across `M_crit` at fixed `g_bar` is **`c = +0.453 +- 0.099` dex where medium-first requires
`-1.622` dex — a 21-sigma rejection**. Not one of the 45 sub-threshold systems lies within 0.5 dex of
its Newtonian prediction (0/45), while 14/45 lie within 0.5 dex of the law. The known `+0.44` dex
satellite-dwarf excess cannot rescue medium-first: it has the wrong sign, and even the largest measured
binary/tidal correction on disk (0.59 dex) leaves 1.55 dex of the 2.15 dex gap standing. The `M_crit`
threshold *is* present in the data — as a **positive** step, i.e. ultra-faints are further *above* the
law, not below it — so the excess and the threshold are the same boundary, but the fork does not depend
on disentangling them.

## Derivation

Units SI; `G = 6.67430e-11`, `Msun = 1.989e30`, `pc = 3.0856775814913673e16`, `a0 = 9.36e-11 m/s^2`
(canonical footing), `L* = 24 pc` (A20 window edge), `kappa = 1/2`. All from BRIEF sec 4 / A22; nothing
is fitted here.

1. **The theory's threshold (A22 eq. 9 and following).** Inside `lambda` the P sector is a hedgehog of
   constant magnitude,

   `u = K|P| = GM/(2 lambda^2) = 2.42e-16 m/s^2 = 2.59e-6 a0`,   `lambda = sqrt(gamma/K) = L*/sqrt2 = 17.0 pc`  (1)

   and the crossover `r_MOND = sqrt(GM/a0) > L*` gives

   `M_crit = a0 L*^2 / G = 3.8669e5 Msun`.   (2)

   *Law-first*: `g_N = g^2/(g+a0)` at every scale, so `M < M_crit` is still MOND.
   *Medium-first*: the crossover is physical, so `M < M_crit` is Newtonian.

2. **Observables per dwarf.** With `r_h` the projected half-light radius and `M_star` the LVD stellar
   mass (`Upsilon_V = 2`),

   `r12 = (4/3) r_h`,   `g_bar = G (M_star/2) / r12^2`,   `g_obs = 3 sigma_los^2 / r12`   (3)

   — the deprojected 3D half-light radius, half the stars enclosed, and the Wolf dynamical-mass
   estimator. The `3` is a normalisation convention: the variant `g_obs = sigma^2/r12` is carried
   through every robustness check and only shifts `Delta` by `-log10 3 = -0.477` dex.

3. **Residual from the law.** With `y = g_bar/a0` and `nu(y) = (1/2)(1 + sqrt(1 + 4/y))` (the canonical
   law inverted),

   `Delta = log10 g_obs - log10[ g_bar nu(y) ]`.   (4)

   Law-first predicts `Delta = 0`. Medium-first predicts, for `M_star < M_crit`, `g_obs = g_bar`, i.e.

   `Delta = Delta_N = -log10 nu(y)`   (5)

   which at the sample's median sub-threshold `g_bar = 1.0e-13 m/s^2` is `Delta_N = -1.490` dex.

4. **The threshold step.** Regress

   `Delta = a + b (log10 g_bar + 12) + c * 1[M_star < M_crit] + eps`,   (6)

   so `c` is the residual step at *fixed acceleration*. Medium-first requires
   `c = median(Delta_N | below) - median(Delta | above) = -1.490 - 0.132 = -1.622` dex. This is the
   decisive statistic: it is immune to any global calibration error in `sigma` or `Upsilon` (a constant
   offset is absorbed by `a`).

5. **Hypothesis comparison.** `H_law: Delta = a + eps`; `H_med: Delta = a + Delta_N 1[below] + eps`,
   with the amplitude of the medium-first term fixed at 1 (that *is* the prediction) and one free offset
   in each model, Gaussian scatter `s` by maximum likelihood. Then
   `Delta(-2 lnL) = 2N ln(s_med/s_law)`, positive favouring law-first.

## Numbers

**Samples on disk (task 1).** Every compilation with the three required columns:

| sample | file | rows | usable | log M*/Msun | role |
|---|---|---|---|---|---|
| LVD MW (Pace 2024) | `real_research/data/dsph/lvd_dwarf_mw.csv` | 68 | 45 | 2.67–9.46 | **primary** |
| LVD M31 | `lvd_dwarf_m31.csv` | 43 | 34 | 4.63–8.86 | **primary** |
| LVD LG field | `lvd_dwarf_local_field.csv` | 64 | 13 | 5.43–8.51 | **primary** |
| LVD beyond LG | `lvd_dwarf_local_field_distant.csv` | 736 | 7 | 6.07–7.57 | cross-check (all are satellites) |
| McConnachie 2012 | `mcconnachie2012_dsph.csv` | 46 | 46 | 2.83–8.83 | independent σ, r_h |
| Collins 2013 (M31) | `collins2013_m31_dsph.tsv` | 18 | 14 | 4.75–6.47 | independent M31 |
| Geha 2026 Paper II | `CFG257_ufd_kinematics_scoping/geha2026_paperII_tableA1.csv` | 67 | 55 | 2.75–7.63 | independent σ, no r_h |
| Arroyo-Polonio 2026 | `CFG257.../arroyo_polonio2026_tableA1.csv` | 12 | 12 | — | binary-corrected σ |
| Walker 2023 | `real_research/data/walker2023/` (CFG51 reduction) | 38 | 2 | — | multi-epoch σ |
| McQuinn 2022 | `faint_rotators_mcquinn2022/apjac9285t1_mrt.txt` | 25 | 0 | 6.57–8.45 | rotators: no σ, not used |

`N = 92`, of which **45 below `M_crit`** and 47 above; `log g_bar` spans `-14.17` to `-8.56`. The
median `r_MOND = sqrt(GM/a0)` is **4.4 pc below** and **71.9 pc above** `L* = 24 pc`, and exactly 45/92
systems have `r_MOND < L*` — the sample straddles the criterion, it is not all on one side.

**The RAR split (tasks 2 and 3).**

| | N | median log g_bar | median Delta | median log(g_obs/g_bar) |
|---|---|---|---|---|
| `M_star < M_crit` | 45 | −12.99 | **+0.651 ± 0.090** | **+2.147 ± 0.078 (140×)** |
| `M_star >= M_crit` | 47 | −12.12 | +0.132 ± 0.053 | +1.171 ± 0.089 (14.8×) |

- bootstrap errors, 4000 resamples; `Delta = +0.173` dex below `M_crit` with `g_obs = sigma^2/r`.
- Mann-Whitney `p(Delta) = 2.7e-08`, Kolmogorov-Smirnov `p(Delta) = 1.4e-08`,
  Mann-Whitney `p(log g_obs/g_bar) = 1.0e-11`.
- medium-first's prediction for the sub-threshold group is `-1.490` dex; measured `+0.651`, so
  **gap `+2.147 ± 0.084` dex** and **0/45** systems within 0.5 dex of Newtonian vs **14/45** within
  0.5 dex of the law. The most negative sub-threshold residual is `-0.438` dex (Crater II); `0/45`
  show a deficit of even 0.5 dex.
- **step at fixed `g_bar`: `c = +0.453 ± 0.099` dex** (`a = +0.140`, `b = -0.086`), where medium-first
  requires `-1.622` dex: **21.0 sigma**. Model comparison `Delta(-2 lnL) = +158.0` for law-first
  (`s_law = 0.472` dex vs `s_med = 1.114` dex).
- matched acceleration bin `log g_bar in [-14.2, -12.5]`: 42 below (`Delta = +0.654`) vs 9 above
  (`+0.237`), difference `+0.417` dex — the threshold appears as a *positive* offset, not the `-1.5`
  of medium-first.

**The RAR itself** (`a26_rar.csv` has all 92 points):

| log g_bar bin | N | N<M_crit | med log g_obs | law | Newton | med Delta |
|---|---|---|---|---|---|---|
| −14.5…−14.0 | 3 | 2 | −11.960 | −12.059 | −14.094 | +0.067 |
| −14.0…−13.5 | 6 | 5 | −11.281 | −11.873 | −13.724 | +0.542 |
| −13.5…−13.0 | 19 | 15 | −10.958 | −11.612 | −13.206 | +0.607 |
| −13.0…−12.5 | 23 | 20 | −10.742 | −11.367 | −12.726 | +0.632 |
| −12.5…−12.0 | 19 | 3 | −10.860 | −11.178 | −12.357 | +0.227 |
| −12.0…−11.5 | 10 | 0 | −10.785 | −10.911 | −11.847 | +0.162 |
| −11.5…−11.0 | 6 | 0 | −10.617 | −10.591 | −11.258 | −0.011 |
| −11.0…−10.5 | 3 | 0 | −10.751 | −10.197 | −10.590 | −0.554 |

The last two bins are dominated by rotators/irregulars (WLM, IC 1613, NGC 6822, Sgr dIrr in the first;
SMC and LMC in the second) where a single `sigma` is not the estimator of the acceleration; they are
shown for completeness, not used in the test. Every bin at `g_bar < 1e-12` — where the sub-threshold
systems live — is dispersion-dominated and clean.

**Named systems** (from `a26_rar.csv`): Segue 1 (`M* = 5.6e2`, `g_bar = 5.8e-14`, boost `10^3.01 = 1023×`,
`Delta = +1.40`) would need `sigma = 0.13 km/s` to be Newtonian and has `4.0`; Bootes I `Delta = +0.46`
(boost 110×); Willman 1 `+1.29`; Draco `+0.63`; Sculptor `+0.20`; Fornax `-0.09`; Crater II `-0.44`;
Antlia II `+0.07`.

## Status

**NUMERICAL.** Verdict **LAW-FIRST**. Deciding number: the threshold step
`c = +0.453 ± 0.099` dex at fixed `g_bar` against medium-first's required `-1.622` dex (21σ), corroborated
kernel-free by the median boost `140×` against `1×`. The `M_crit` boundary is real in the data but has
the *opposite* sign to medium-first.

## Checks (11/11 PASS; `a26.out`)

| id | what | measured | threshold |
|---|---|---|---|
| K1 | primary sample assembled | N=92, 45 below `M_crit` | N≥80, ≥40 below |
| K2 | theory identities (1),(2) | 3.8669e5 Msun (0.08%), 16.97 pc, 2.586e-6 a0 | 1%, 0.05 pc, 1% |
| K3 | reproduces the record's dwarf excess on CFG828's own 29-dwarf sample | mean `Delta = +0.438` | \|x−0.44\|≤0.06 |
| K4 | kernel-free boost below `M_crit` | `+2.147` (140×) | ≥0.70 (5×) |
| K5 | sign below `M_crit` | `+0.651 ± 0.090` (95% lo +0.473) | >0 at 95% |
| K6 | distance from Newtonian | `+2.147 ± 0.084` dex | ≥1.0 dex |
| K7 | step at `M_crit` | `c = +0.453 ± 0.099`, 21.0σ from `-1.622` | ≥5σ |
| K8 | matched `g_bar` bin | diff `+0.417` dex | >−1.0 |
| K9 | census | 14 near-law vs 0 near-Newton | ≥10 and ≤2 |
| K10 | 8 variants (σ²/r, `M_dyn`, a0 alt, MW/M31/field, `M*/2`, pressure-supported only) | all keep `Delta_below>0`, step>−0.5 | all |
| K11 | confound budget | 1.55 dex survives the largest measured correction (73%) | ≥1.0 dex |

Mutation `--mutate` injects medium-first (`g_obs := g_bar` for `M_star < M_crit`) and the script returns
**MEDIUM-FIRST, 3/11**; `--mutate2` (σ/1.45) breaks K3 as CFG828's own control does. See `MUTATE.md`.

## The confound, honestly (task 4)

1. **The split is degenerate with the excess in population terms.** Spearman `rho(log M*, log g_bar) =
   +0.791`, and **100% of the sub-threshold systems lie at `g_bar < 1e-12`**, exactly where CFG828's
   `+0.44` dex excess lives (21 of its 29 dwarfs are below SPARC's floor). The `M_crit` boundary and
   "below SPARC's floor" are the same boundary in this sample; no cut on these data separates them.
2. **But the excess has the wrong sign and the wrong size to hide medium-first.** Medium-first needs the
   sub-threshold group to sit `1.49` dex *below* the law; the excess puts them `0.44–0.65` dex *above*
   it. The two differ by 2.14 dex. The largest binary correction anywhere on disk is `-0.587` dex
   (Arroyo-Polonio f=0.7 vs f=0, median `-0.216` over 12 UFDs) and the largest multi-epoch cleaning
   effect is `-0.530` dex (Tucana II, Walker 2023 via CFG51); applying the worst of them leaves
   **1.55 dex (73% of the gap)**. To make the sub-threshold dwarfs Newtonian their `sigma` would have to
   be inflated by `sqrt(140) = 11.8×` (4.0 → 0.34 km/s for a median sub-threshold system; Segue 1
   itself needs 4.0 → 0.13 km/s); the largest measured
   inflator is `10^0.587 = 3.9×` in `g_obs` (`1.97×` in `sigma`).
3. **A positive step is nonetheless a threshold — and a new problem.** The massive low-`g_bar` control
   (25 systems above `M_crit` with `g_bar < 1e-12`: Antlia II, Crater II, Bootes III, And XIX …) sits at
   `Delta = +0.227`, while the sub-threshold group at the same acceleration sits at `+0.654`. So the
   excess is *not* a pure function of acceleration: an extra `+0.42` dex turns on below `M_crit`. That is
   a fact the record should chase — if it is not binaries or tides, it is a bigger problem for the law
   than the fork was.
4. **What would separate them.** A sample of *isolated* (non-satellite) ultra-faints with
   `M_star < 3.9e5` and measured `sigma`, `r_h`. On disk there is exactly **one** (Leo T, `log M* = 5.43`)
   — the LVD field sample has only 13 systems with `sigma` and 1 below threshold — so the confound-free
   test is not available today. Field UFDs from Rubin/LSST with `sigma` would give N ~ 10–30 at
   `g_bar ~ 1e-13`, where the law-first/medium-first separation is 1.5–1.7 dex against 0.3 dex errors:
   `>20 sigma` per system. Failing that, the fork's other leg is A24's wide-binary `gamma_v` at 20 kAU
   (`1.18` vs `1.0`, Gaia DR4), which has no satellite confound at all.

## What this does not do

- It does not confirm the law *exactly* below `M_crit`: the residual there is `+0.17` (σ²/r) to `+0.65`
  dex (Wolf) on the primary sample, and `-0.149` dex in the worst admissible combination (σ²/r with the
  record's σ/1.45 suppression). The law's *exactness* below `M_crit` is therefore unresolved at the
  0.2–0.8 dex level; the fork does not depend on that, since the rival sits 1.34 dex below the worst
  case. It excludes the rival, it does not certify the law.
- It does not test the *local* reading of the threshold (crossover biting only inside `r < L*`). If that
  reading is defended, no datum at `r_h ~ 10^2` pc bears on it and the fork must be decided by A24's
  wide-binary leg or by resolved kinematics inside 24 pc — neither on disk.
- The observable is a single-`sigma`, single-aperture dynamical mass, assuming isotropy and equilibrium;
  Crater II and Antlia II are known non-equilibrium systems and move by ±0.5 dex on their own.
- It uses LVD's `Upsilon_V = 2` stellar masses, no per-galaxy M/L. A 0.3 dex M/L error moves `Delta` by
  0.15 dex in the deep regime — an order below the 2 dex separation.
- No membership/binary quality cuts beyond LVD's own; CFG28/29's stricter sample is smaller (29 dwarfs,
  only 6 below `M_crit`) and is used here only as the K3 control.

## Next

1. **Pre-register the field-UFD test**: N ≥ 5 isolated systems with `M_star < 3.9e5`, `sigma` to
   0.3 dex; law-first predicts `Delta = 0`, medium-first `Delta <= -1.4`. This is the only sample that
   removes the satellite confound, and it is a Rubin/LSST data-wait, not a theory question.
2. **Chase the `+0.45` dex positive step.** Resolve it with multi-epoch σ (Walker-style) on the 10 most
   discrepant sub-threshold systems; if it survives, it is a law-shape problem at `g_bar < 1e-12` that
   no interpolation function in the register currently covers.
3. **Do not re-open medium-first on dwarfs.** The dwarf channel is closed at 21σ in the opposite
   direction; the fork's live leg is the wide-binary `gamma_v` (A24/Gaia DR4), where the same two
   readings differ by 18%.
