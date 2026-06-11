# agentCC — THE a* HUNT: no flattening in the deepest existing kinematic data (best a* = 0 at both footings, both shapes, both environment halves), but SPARC's deepest points only reach a*_95 ≈ 1.0–1.3×10⁻¹¹ m/s² (0.08–0.11 a₀) — WEAKER than the indirect band line a* < 0.05 a₀, which stays the binding kinematic constraint. Below SPARC's floor the published deviations are UPWARD (UFDs — the wrong sign for the floor) or ENVIRONMENT-KEYED (Crater II; Chae's 13σ env correlation). Verdict: DATA-INSUFFICIENT below x ≈ 0.05 — the prediction's window 0 < a* < 4.7×10⁻¹² is open and untested, and the decisive test is named.

*agentCC, 2026-06-11. Task (the campaign's NEW prediction vs existing data): agentV's no-kernel corollary —
ANY realization of the linear field-bath class flattens μ to const + O(a²) below some a* > 0 (the deep-MOND
√ law cannot be exact; agentV §2.2/§7 verdict (1), watchlist item (ii)) — against the deepest kinematics now
in hand. The band constraint (agentBB registry item v): a* must hide below x = a/a₀ ≈ 0.05, i.e.
**a* < 0.05 a₀ = 4.68×10⁻¹² m/s² (fw) / 6.0×10⁻¹² (canon)**, else the full-band SPARC fit already kills it.
Inputs: the LOCKED SPARC conventions of `mi_f4_sparc_shape_test.py` (unweighted dex RMS primary, weighted
secondary, Υ_bul = 1.4Υ_d, per-shape best-Υ, both a₀ footings), `data/sparc_data/*_rotmod.dat` (175 galaxies),
the repo 2M++ environment table `data/sparc_a0_environment_table.csv` (the same Carrick+2015 field Chae+2021
keyed e_N to), and literature pins fetched 2026-06-11 (Lelli+2017 arXiv:1610.08981; Chae+2020 arXiv:2009.11525;
Chae+2021 arXiv:2109.04745; MUSE-Faint/EDGE arXiv:2510.06905 A&A 2025; Mancera Piña+ arXiv:2404.06537;
arXiv:2408.05269). Artifacts: `agentCC_astar_hunt.py` → `agentCC_astar_hunt.out` (all numbers below
machine-generated there; regression gate reproduces the locked baseline EXACTLY before any new scoring:
fw 0.1950 @ Υ=0.52, canon 0.1977 @ Υ=0.46 — PASS both). Pre-registered readings: FLATTENING-FAVORED /
EFE-NOT-FLOOR / BOUND / DATA-INSUFFICIENT. Raw numbers first; verdict at the end, both ways, full weight.
Bug log, recorded not hidden: (i) run v1's coarse M3 grid printed dlnL = +20.17 at the canonical footing —
a real maximum, but the fine-grid rerun + the pre-built offset control diagnosed it as the a₀-NORMALIZATION
direction, not a floor (§3b below; the gain is offset-degenerate to within 0.06 lnL); kept and quarantined,
exactly the artifact class the working rule exists for. (ii) The 95% bounds are grid-quantized (factor
10^0.1): quoted as last-allowed/first-excluded brackets. (iii) The dense-half y<0.01 median was printed for
< 3 points in v1; guarded to n/a.*

## 0. The two models and the confound, pinned

Both the predicted floor and the standard EFE pull g_obs BELOW the deep-MOND line — partially degenerate:

- **The floor (the prediction under test).** μ freezes at x* = a*/a₀: below the transition y_t (where
  ν(y_t)y_t = x*), the boost freezes, g_pred = ν(y_t)·g_bar — slope-1 quasi-Newtonian below **g_obs = a***.
  Keyed to ACCELERATION, environment-blind, universal. (Implemented as the MI μ-floor mapped through the
  locked ν baseline; in the deep regime y_t ≈ x*², so a floor at 0.05 a₀ bites only below y ≈ 0.0025.)
- **The EFE (the confound).** QUMOND radial form (repo convention, `sparc_efe_test.py`):
  g_pred = ν((g_bar+g_ext)/a₀)(g_bar+g_ext) − ν(e_N)g_ext — slope-1 below g_bar ≈ g_ext = e_N a₀. Keyed to
  ENVIRONMENT (Chae+2021: fitted e_N median ≈ 0.053; UNDERDENSE median 0.016₋₀.₀₂₇₊₀.₀₁₅ — consistent with
  zero — vs OVERDENSE 0.103₋₀.₀₀₈₊₀.₀₃₀, a ~13σ contrast keyed to the 2M++/NSA large-scale field).
- **The discriminator:** the floor's downturn sits at a universal g_obs = a* in EVERY environment; the EFE's
  tracks g_ext. Split the deep sample by external density and compare. A second discriminator, free of
  charge: unmodeled real EFE is also downward — it cannot CANCEL a floor, so a no-downturn result bounds the
  floor conservatively.

## 1. SPARC's deepest points (task item 1)

Deep sample y = g_bar/a₀ < 0.1 at the locked Υ (membership fixed once per footing, all models score the
same points):

| footing | N pts | gals | min y | min g_obs [m/s²] | pts y<0.01 | pts y<0.005 |
|---|---|---|---|---|---|---|
| fw 9.36e-11 | 1179 | 125 | 2.50e-3 | 8.02e-13 (0.009 a₀) | 9 | 1 |
| canon 1.2e-10 | 1454 | 141 | 1.32e-3 | 8.02e-13 (0.007 a₀) | 23 | 5 |

The deepest galaxies: DDO064, UGCA444, UGC07577, NGC3109, D564-8, NGC3741, UGC06667, UGC05750, KK98-251.
**The raw shape (binned median residual vs the locked ν law, fw):** +0.43 (y<0.005, 1 pt), +0.12 (0.005–0.01),
+0.07 (0.01–0.02), −0.02 (0.02–0.04), −0.01 (0.04–0.07), +0.00 (0.07–0.1). The deepest bins sit ON or ABOVE
the law — **no downward dive anywhere**. (Canon shows a near-uniform −0.05 dex offset across the whole deep
band — y-INDEPENDENT, i.e. normalization, not flattening; §3b.) Three individual galaxies do sit low
(UGC05750 −0.98 dex, KK98-251 −0.66, UGC07577 −0.45 vs √) — but KK98-251's environment is mean-density
(2M++ 1+δ = 1.006), the other two lack table entries, and single-galaxy inclination/distance systematics
own this regime; the medians carry the verdict.

## 2. The two-branch fit (task: pure MOND vs MOND-with-floor, full weight both ways)

Profile likelihood (per-point σ_dex = (2/ln10)·eV/V, intrinsic scatter profiled; σ_int ≈ 0.165 dex both
footings), unweighted dex RMS primary:

| model (deep sample) | fw RMS / dlnL | canon RMS / dlnL | best parameter |
|---|---|---|---|
| M0 pure MOND (locked ν_McGaugh) | 0.2295 / — | 0.2269 / — | — |
| M1 + floor a* | 0.2295 / +0.00 | 0.2269 / +0.00 | **a* = 0 at BOTH footings** |
| M2 + global EFE e_N | 0.2295 / +0.00 | 0.2269 / +0.00 | e_N = 0 (global; see §4 caveat) |
| M3 floor + EFE (fine joint) | 0.2295 / +0.00 | 0.2219 / +20.35 | canon: a*=1.0e-11, e_N=0.0016 — ARTIFACT, §3b |

- **No flattening preferred, anywhere:** best a* = 0 at both footings (AIC +2 for the extra parameter), in
  both environment halves (§4), under the shape-only nuisance treatment (§3c), and under the framework's own
  ν = √(1+1/y) baseline at its own locked Υ (§3d: best a* = 0, identical bound). 87% (fw) / 76% (canon) of
  1000 galaxy-level bootstrap resamples put the best a* exactly at 0.
- **The lower bound the data impose (95%, one-sided, Δχ²=2.71):** the profile crossing sits between the
  last-allowed and first-excluded grid points: **a* ∈ (1.00, 1.26)×10⁻¹¹ excluded upward — i.e.
  a* ≲ 1.1×10⁻¹¹ m/s² ≈ 0.11 a₀ (fw) / ≈ 0.09 a₀ (canon)**. Two-sided (Δχ²=3.84) lands on the same grid
  bracket. Galaxy bootstrap (clustering-aware): median bound 7.9×10⁻¹² (0.085 a₀ fw / 0.066 canon),
  [16,84]% within one grid step.
- **The headline comparison:** the direct deep-point bound (≈ 0.08–0.11 a₀) is a factor ~2 WEAKER than the
  indirect band line a* < 0.05 a₀ that agentBB's full-band fit already imposes. **SPARC's deepest points add
  no constraining power below the band constraint.** The reason is arithmetic: a floor at 0.05 a₀ bites only
  below y ≈ 0.0025 — and SPARC has exactly 1 (fw) / 1 (canon) point there, with σ_int ≈ 0.165 dex.

### 3b. The normalization artifact, caught and quarantined (working rule)

The canon-footing M3 gain (+20.35 lnL) is reproduced to within 0.06 lnL by a PURE DEX-OFFSET control
g_pred = ν(y)g_bar·10^c with c = −0.030 (+20.29): the floor+EFE combination at (a* = 1.0e-11, e_N = 0.0016)
degenerates into a constant linear subtraction ν(y_t)·g_ext across the band — a y-independent shift, not a
flattening. The canon deep band sits uniformly −0.0514 dex below the law (fw: −0.0287, offset gain a
negligible +0.38) — the known a₀-normalization direction: under the locked unweighted metric the deep band
is better centered on the framework footing than the canonical one (raw fact, stated raw; consistent with
the banked result that the unweighted-RAR-preferred a₀ sits within ~0.3% of the framework value). The
shape-only refit (§3c: free offset nuisance per model) kills the artifact and returns best a* = 0 with the
same bound at both footings. *Deficit-claim symmetry: the same control confirms the fw footing's deep band
carries no hidden offset rescue either.*

## 4. The EFE confound and the environment split (task's explicit warning)

- Global-e_N fit: best e_N = 0 at both footings (canon dense half: e_N = 0.0010 at +1.42 lnL — noise). This
  echoes the repo's own `sparc_efe_test.py` global null and does NOT contradict Chae's >4σ detection, which
  is per-galaxy rotation-curve SHAPE with environment correlation — a finer statistic than the pooled RAR.
- 2M++ median split of the deep sample (env data for 861/1179 fw pts): **ISOLATED half best a* = 0
  (a*₉₅ ≈ 1.0×10⁻¹¹), DENSE half best a* = 0–1×10⁻¹¹ at dlnL ≤ +0.05 (a*₉₅ ≈ 1.0–1.3×10⁻¹¹)** — no downturn
  in either half, no environment-keyed contrast at pooled-RAR sensitivity.
- **Where the floor-sensitive points live:** the y < 0.01 points concentrate in the ISOLATED half (fw 3 vs 2,
  canon 12 vs 5, of those with env data) — the EFE confound is WEAKEST exactly where a floor would bite
  first. Good news for the future test; too few points today.
- **The published downturn evidence is environment-shaped, not floor-shaped:** Chae+2021's fitted downturns
  correlate with the external 2M++/NSA field at ~13σ (underdense median e_N = 0.016, consistent with zero;
  overdense 0.103). An acceleration-keyed universal floor produces NO environment correlation — so the one
  existing deep-RAR downturn detection points AWAY from the floor reading. (Not quantitatively binding on a*
  beyond §2 — Chae's e_N priors and the e_N ↔ y_t ≈ x*² mapping are model-dependent — but directionally
  against. The isolated-subsample consistency-with-zero is the floor-relevant row.)

## 5. The published ultra-deep points below SPARC's floor (task item 2)

Pinned 2026-06-11 (machine placements in `.out` [6]; convention g_obs = 3σ²/r_½, r_½ = (4/3)R_e, both
footings):

- **Classical dSphs (Lelli+2017, arXiv:1610.08981): ON the law.** g_bar ~ 10⁻¹²–10⁻¹¹; the high-quality
  classical dSphs "follow the same relation as LTGs within the errors" — the √ law holds to g_bar ≈ 10⁻¹².
- **Ultrafaints (the famous flattening hint): the WRONG SIGN for the floor.** Lelli+2017 eq. 14: the UFDs
  trace a possible flattening at **ĝ_obs = (9.2 ± 0.2)×10⁻¹² m/s²** — a g_obs-CONSTANT plateau ABOVE the √
  extrapolation (slope→0), explicitly flagged by the authors as "may be real or an intrinsic limitation of
  the current data" (tides, binaries, contaminants, few-star dispersions). The predicted floor is the
  OPPOSITE deformation: slope→1, BELOW the √ line. The UFD hint, even if real, is not the floor.
- **MUSE-Faint/EDGE 2025 (arXiv:2510.06905): UPWARD, again.** 12 dwarfs (8 classical + Eridanus II, Grus 1,
  Leo T, Antlia B), g_bar down to ~10⁻¹⁴: systematically **+0.3 to +0.5 dex ABOVE** the RAR extrapolation,
  growing toward lower mass; the paper itself notes "galaxies in the EFE regime should scatter below the
  RAR, while the opposite is what we see." Whatever is happening at g_bar < 10⁻¹² (their headline: the RAR
  stops being predictive), it is not a downward acceleration-keyed floor — though upward dispersion-inflating
  systematics could in principle MASK one, so this is sign-evidence, not a clean bound. Fornax is their one
  on/below-RAR object (our placement: −0.08 dex fw).
- **The downward objects, both confounded:** (a) **Crater II** — our placement g_bar = 1.1×10⁻¹⁴,
  g_obs = 5.0×10⁻¹³, −0.31 dex below √ (fw) — but g_ext ≈ 0.14 a₀ ≫ g_int: EFE-dominated, and the
  suppression was PRE-predicted by McGaugh from the EFE before measurement (2.1 vs 2.7±0.3 km/s) —
  environment-keyed by construction. (b) **AGC 114905** (the single floor-shaped object in the literature):
  isolated (e_N ~ 0.01), gas-rich UDG, −0.90 dex below √ at the measured i = 32° (Mancera Piña+2022/24,
  arXiv:2404.06537 maintains the tension) — an isolated downward ultra-deep point is exactly the floor
  fingerprint — BUT the deviation is inclination-hostage: i ≈ 15° (consistent with the optical image;
  arXiv:2408.05269, A&A 2024) lifts g_obs ×4.2 to −0.27 dex, inside ordinary scatter. Contested; not
  evidence; THE object class to watch.
- **Quarantined:** weak-lensing RAR extensions (Mistele+2024: the √ law to g_bar ~ 10⁻¹³) probe the LENSING
  channel — in this framework that sector carries the Ψ-slip partner (agentW) and is NOT a kinematic a*
  probe. Wide binaries probe x ~ 1, not the deep regime.

## 6. VERDICT (pre-registered readings adjudicated; both ways, full weight)

> **NO-FLATTENING-DETECTED + DATA-INSUFFICIENT below x ≈ 0.05.** (1) SPARC's deepest points show no floor:
> best a* = 0 at both footings, both baseline shapes, both environment halves, shape-only and absolute,
> 87%/76% of galaxy bootstraps. The bound they impose — **a* ≲ 1.0–1.3×10⁻¹¹ m/s² ≈ 0.08–0.11 a₀ (95%)** —
> is WEAKER than the indirect band line **a* < 0.05 a₀ = 4.7×10⁻¹² (fw)** that the full-band fit already
> enforces (agentBB): the binding kinematic constraint on a* remains the band-hiding requirement, and
> existing kinematic data CANNOT test the prediction inside its allowed window 0 < a* < 0.05 a₀.
> (2) Below SPARC's floor, nothing published shows the floor's signature (downward, acceleration-keyed,
> environment-blind): classical dSphs sit ON the √ law to 10⁻¹²; the UFD/MUSE-Faint deviations are UPWARD
> (wrong sign); the downward objects are environment-keyed (Crater II, EFE-pre-predicted) or
> inclination-contested (AGC 114905); and the one published deep-downturn detection (Chae) correlates with
> environment at ~13σ — EFE-shaped, not floor-shaped. (3) The prediction is alive, unfalsified, and
> currently untestable with data in hand below 4.7×10⁻¹².

- **Framework-favorable reading, full weight:** the new structural prediction survives its first
  confrontation intact — nothing in the deepest existing kinematics contradicts a floor anywhere in the
  allowed window, and the two raw shape facts cut the framework's way: the deep band is better centered on
  the fw footing (offset c = −0.005 vs −0.030 canon, §3b), and the floor-sensitive deepest points live in
  isolated environments where the EFE cannot mimic or mask the future signal.
- **Framework-unfavorable, same weight:** "survives" here means UNTESTED, not supported — the window is open
  because the data run out, and the bound this memo adds (0.08–0.11 a₀) is the WEAKEST link in the a* chain
  (the band line stays binding). Worse for near-term testability: the floor must hide below y ≈ 0.0025 in
  g_bar, where SPARC has ONE point — closing the window needs a new data class, not a reanalysis. And the
  one literature object with the right fingerprint (AGC 114905) currently resolves AGAINST the deviation
  being real.
- **THE DECISIVE NEXT TEST (named, as tasked):** *isolated ultra-deep rotators* — resolved HI rotation
  curves of gas-rich dwarfs/UDGs with e_N ≲ 0.005 (2M++ underdense, no host within ~1 Mpc) reaching
  g_obs = (0.01–0.05) a₀ with inclination pinned (i ≳ 40° or kinematic inclination): the floor predicts a
  universal downturn at g_obs = a* IDENTICAL in all of them; the EFE predicts NONE in isolation (Chae's
  isolated median is already consistent with zero). One clean isolated galaxy with a coherent outer downturn
  at fixed g_obs — replicated at the same g_obs in a second environment — separates the two. Concrete
  routes: (i) AGC 114905-class MeerKAT/VLA UDGs with settled inclinations (arXiv:2404.06537 vs 2408.05269 is
  the live fight); (ii) FAST/Apertif isolated dwarf HI samples; (iii) BIG-SPARC (the repo's staged
  environmental-fork pipeline, `project_bigsparc_environmental_fork` — not public as of 2026-06) multiplies
  the y < 0.01 count by ~an order of magnitude and carries the environment axis natively. Pre-registered
  discriminator: fit per-galaxy downturn scale g_down; floor ⇒ g_down clusters at one universal value
  uncorrelated with e_N,env; EFE ⇒ g_down ∝ e_N,env (Chae's 13σ slope re-emerges).
- **What would have shown the flattening** (pre-stated, did not occur): the deepest bins diving coherently
  NEGATIVE vs the locked ν law at a common g_obs in BOTH environment halves, with dlnL > 2 surviving the
  offset control.
- **Untouched:** agentV's theorem and agentBB's closure (this memo tests the prediction, not the
  derivation); the effective law's SPARC standing (the regression gate reproduced it exactly); the lensing
  channel (quarantined to agentW's sector); Chae's per-galaxy EFE detection (our global-e_N null is the
  expected wash-out, not a refutation).
- **Registry handoff:** (i) watchlist (agentV item ii / agentBB item v) can be updated: the deep-RAR
  flattening floor a* is now BOUNDED DIRECTLY at 0.08–0.11 a₀ by SPARC kinematics (this memo), with the band
  line 0.05 a₀ still binding and the open window 0 < a* < 4.7×10⁻¹² requiring the named isolated-rotator
  test; (ii) new watch triggers: the AGC 114905 inclination fight (arXiv:2404.06537 vs 2408.05269 — a
  confirmed low-inclination resolution removes the only floor-shaped object; a confirmed i ≈ 32° makes it
  the first candidate DETECTION at a* ~ 2×10⁻¹², inside the window), BIG-SPARC public release, any
  isolated-dwarf deep-HI RAR release; (iii) the canon-footing −0.05 dex deep-band offset is banked as a
  normalization artifact with its control (§3b) — do not re-report it as either an EFE detection or a floor.

## 7. Anchors
- In-repo: `agentV_kernel_inversion.md` (§2.2 the no-kernel flattening corollary; §7 watchlist item ii),
  `agentBB_legal_mixture.md` (registry item v: a* must sit below x ≈ 0.05; the band line),
  `mi_f4_sparc_shape_test.{py,out}` (locked conventions + the reproduced baseline), `sparc_efe_test.py`
  (the QUMOND radial EFE form + the global-fit null), `data/sparc_a0_environment_table.csv` +
  `project_sparc_a0_vs_cosmicweb.py` (the 2M++/2MRS environment axes), `project15_dsph_efe_thermometers.py`
  (Crater II EFE arithmetic), `project_bigsparc_environmental_fork` (the staged deep-sample pipeline).
- Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152 (arXiv:1610.08981) — dSph RAR extension; eq. 14
  flattening hint ĝ = (9.2±0.2)×10⁻¹² (UPWARD; caveated by the authors).
- Chae, Lelli, Desmond, McGaugh, Schombert, Li 2020, ApJ 904, 51 (arXiv:2009.11525) — the EFE detection;
  Chae et al. 2021, ApJ 921, 104 (arXiv:2109.04745) — e_N median 0.053; underdense 0.016 vs overdense 0.103
  (~13σ), keyed to 2M++/NSA; Carrick+2015 (the 2M++ field, also this repo's environment table source).
- MUSE-Faint/EDGE: arXiv:2510.06905, A&A 2025 — 12 dwarfs to g_bar ~ 10⁻¹⁴ sit +0.3–0.5 dex ABOVE; EFE
  direction explicitly rejected by the authors.
- Mancera Piña et al. (arXiv:2404.06537, A&A 2024) — AGC 114905 tension maintained at i = 32°;
  Lelli (arXiv:2408.05269, A&A Letters 2024) — AGC 114905 + AGC 242019 consistent with Milgromian dynamics
  at i ≈ 15° once inclination/distance uncertainties are realistic.
- McGaugh 2016 (Crater II σ = 2.1 km/s EFE pre-prediction); Caldwell et al. 2017 (σ = 2.7±0.3 km/s).
- Mistele et al. 2024 (weak-lensing RAR to g_bar ~ 10⁻¹³ — quarantined to the lensing/Ψ-slip channel).
