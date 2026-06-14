# What is actually going on in cluster cores? The dissenting / non-standard physical readings (2026-06-14)

*Step back from "MOND vs LCDM" and ask what is PHYSICALLY happening. Literature 2024-2026 + the real eRASS1
FITS (9,830 clusters) + python, through the framework's distinctive density-a0 / a0<->Lambda lens. Open inquiry,
both ways. No manufactured cure, no high-priest dismissal. Quarantine held (a0/Z never asserted derived).*

---

## The one-paragraph answer

The cluster "2x deficit" is NOT one thing. The latest data resolves it into **two physically distinct pieces**:
**(A) a genuine, uniform, central residual** that survives in the most relaxed, gas-complete clusters — it is a
**CORE phenomenon** (~400 kpc, missing-to-gas density ratio ~10, "dark-mass-follows-gas"), remarkably uniform
cluster-to-cluster (eRASS1 intrinsic scatter only ~0.04 dex / 10%); and **(B) a disequilibrium inflation** on top
of it — mergers (A644, A2319) need ~0.5-0.9 dex MORE "missing mass" than relaxed clusters, which the X-COP team
attribute explicitly to **non-equilibrium dynamics, NOT actual missing mass**. The honest synthesis: the "2x" is
**real piece (A) + a heterogeneous systematic skirt (B)**. Piece (B) means the raw stacked number over-states the
true residual; piece (A) means a real residual remains even after you strip every systematic. The framework's
density-a0 has a DISTINCTIVE thing to say about (A) — the residual's CORE-concentration + follows-gas shape is
exactly what a density-dependent a0 would predict — but the banked nulls (no derived smoothing scale lands in the
core window) still stand, so it is a CONSTRAINT the framework must match, not yet a confirmation.

---

## (1) Non-equilibrium / merging — how much of the deficit is disequilibrium? **REAL and LARGE for mergers.**

Kelleher & Lelli 2024 (A&A 688 A78, arXiv:2405.08557; "Galaxy clusters in Milgromian dynamics") fit the MOND missing-mass on 5 X-COP clusters:
- **Relaxed** (A1795, A2029, A2142): log M_mm = 14.17, 14.31, 14.36 M_sun.
- **Merging** (A644, A2319): log M_mm = **14.78, 15.05** — i.e. **0.5-0.9 dex (3-9x) MORE** missing mass.
- Their words: the merger ratio "increases up to ~5 but **may indicate out-of-equilibrium dynamics rather than
  actual missing mass**"; mergers "may not be appropriate to test a dynamical theory such as MOND."
- The fitted external-field strength is 0.001-0.002 a0 for relaxed clusters (matches large-scale structure) but
  **0.1-0.3 a0** for mergers — a fitting artifact of disequilibrium, not a real field.

**eRASS1 context (real data):** ~30-35% of eROSITA clusters are dynamically RELAXED by the BCG-X-ray offset
(Kluge+2024, Zhang+2025 A&A 698 A171) — i.e. the MAJORITY (~65-70%) show merger/disturbance signatures. A stacked
"2x" over 9,830 clusters is therefore a population average over a relaxed core + a disturbed majority whose
hydrostatic/HSE-derived masses are merger-boosted. **Verdict: a real, measured fraction of the raw deficit is
disequilibrium inflation — it makes the population number bigger than the equilibrium residual.**

## (2) The relaxed subset — is the deficit smaller there? **YES, smaller, but NOT gone.**

In the relaxed X-COP clusters the missing-to-baryon ratio peaks at **1-5 at 200-300 kpc** and declines to
**0.4-1.1 by ~1-3 Mpc** — "total missing mass smaller than or comparable to the ICM mass." With the MOND external
field effect + a sensible 10-40% hydrostatic bias, the relaxed residual shrinks substantially **but never reaches
zero at any radius**. So the relaxed subset confirms: stripping disequilibrium lowers the number (toward ~1x the
ICM, not 2x M_dyn), **but a real central residual survives**.

## (3) Gas clumping / multiphase gas — **a real X-ray bias, but it goes the WRONG way and lives in the OUTSKIRTS.**

Clumping (Nagai-Lau, Eckert+) biases X-ray gas density HIGH (C~1.3 at R200, ~5 at 2R200), concentrated at
**r > R200**. Two consequences for this problem: (i) it INFLATES the inferred baryon (gas) mass, which would
*lower* eta, a ~10-15% reducer at most (banked); (ii) it is an OUTSKIRT effect, so it does nothing to the CORE
residual that the lensing data isolate at ~400 kpc. Multiphase/cold gas in the core is the opposite: it is
exactly the candidate for the residual ITSELF (see below). **Verdict: clumping is a modest outskirt reducer, not
the core story.**

## (4) Central-vs-outskirt structure — **the deficit is a CORE phenomenon. This is the headline.**

Two independent 2024-2025 analyses agree the MOND residual is **centrally concentrated, NOT global**:
- **X-ray (X-COP, Kelleher & Lelli 2024):** "missing matter MORE centrally concentrated than the ICM," inner core + outer
  r^-4 decline (finite total mass), scale radius ~250-400 kpc.
- **Lensing (Famaey, Pizzuti & Saltas 2025, PhRvD 111 123042, arXiv:2410.02612, CLASH strong+weak lensing):**
  inner **constant-density core**, outer slope steeper than -3.5, within ~1 Mpc. Best-fit is a
  **"dark-mass-follows-gas" profile with an exponential cutoff ~400 kpc**; missing-to-hot-gas density ratio
  **~10, remarkably uniform** across the 11 most massive clusters. Their leading interpretation: MOND's residual
  is **additional baryonic mass in the center — cold, dense H2 gas clouds in a multiphase ICM** (collisionless
  like DM per lensing, follows the gas).

**This re-frames everything: eRASS1 reads eta AT R500 = 0.77 Mpc median (range 0.52-1.14 Mpc) — squarely inside
the ~400 kpc-1 Mpc core where the residual lives.** The eRASS1 "2x" is essentially a measurement of the CORE
phenomenon at one aperture, integrated over the cored excess. The deficit is NOT a global halo-scale missing mass;
it is a central excess that the lensing data say tracks the gas.

## (5) Cluster-to-cluster scatter — is eta~2 a universal law or a heterogeneous mix? **BOTH, at different scales.**

Real-data result (eRASS1, framework interp g_pred = sqrt(g_bar^2 + g_bar*a0), a0 = 9.36e-11):
- eta distribution: 5th=2.00, 50th=2.33, 95th=4.43; total log-scatter **0.109 dex**.
- Median measurement scatter (from M500 errors) = **0.102 dex** => **intrinsic scatter only ~0.04 dex (~10%)**.
- **80% of clusters within +/-0.1 dex of the median; NO eRASS1 cluster has eta < 1.5.**

So at FIXED aperture R500, on WL-calibrated masses, eta is **remarkably UNIFORM** — a near-universal ~2, not a
heterogeneous bag. The heterogeneity the lensing/X-COP papers see is (a) the relaxed-vs-merging split (item 1,
~3-9x in mergers) and (b) low-mass clusters showing "larger, more scattered" missing-to-gas ratios with
disequilibrium features. **Reconciliation:** the CORE residual (A) is uniform; the disequilibrium skirt (B) is
heterogeneous and concentrated in low-mass / disturbed systems. The eRASS1 uniformity is the signature of (A)
dominating a fixed-aperture WL-mass stack; the X-COP/lensing heterogeneity is (B) showing up when you resolve the
radial profile and include disturbed systems.

## The non-tautology check (so I don't over-read the data)

- Spearman(fgas, eta) = -0.60 is **mechanical** (more gas -> more g_bar -> lower eta; partial corr | g_bar = -0.86
  confirms it's the deep-MOND tautology), NOT a disequilibrium signal. Do not cite it as physics.
- The real, non-tautological eRASS1 result is **eta is FLAT-to-slightly-rising vs mass** (2.30 at group scale ->
  2.42 at M500>7e14), even as gas climbs toward cosmic. The deficit does NOT shrink where the baryon budget is
  most complete — confirming the banked finding that it is not a missing-baryon artifact at R500.

---

## The FRAMEWORK-DISTINCTIVE angle (a0<->Lambda, density-a0) — LIVE as a constraint, banked-null as a cure

The single most framework-relevant new fact is the lensing **"dark-mass-follows-gas, core-concentrated, ratio ~10"**
shape. Standard universal-constant MOND has NO reason for the residual to track the gas or concentrate in the core.
The framework's DISTINCTIVE density-a0 law, a0 = (c/2)sqrt(G rho), DOES: a density-dependent a0 boosts the MOND
enhancement **most where rho is highest = the core**, producing a centrally-concentrated, gas-tracking extra
gravity — qualitatively the observed signature.

But the quantitative banked nulls stand (re-verified this session):
- **Local/clumpy rho** (cool-core n_e~1e-2 cm^-3 -> rho ~5e3 rho_DE): a0 boost ~70x. DEAD — would also erase galaxy
  MOND (disk rho ~1e6x cosmic) and over-close clusters.
- **Mean density within R500** (500 rho_crit): a0 boost ~28x -> over-closes (eta<1). Banked.
- **No DERIVED smoothing scale** (1/mu=1 Mpc breaks SPARC; r_DE and c/H give no differential boost) lands in the
  core-residual window that would need a0_cluster ~ 2-4x a0_field.

**So:** the lensing core-concentration + follows-gas result is a **genuine, specific, falsifiable target the density-a0
must match** (it is exactly the right SHAPE), and it is the framework's distinctive lens on "what is going on" — but
producing it requires a smoothing scale that no framework-derived length supplies. It is a LIVE constraint and a
banked-null cure, simultaneously. This is the honest standing.

There is one more distinctive reading worth flagging both ways: the lensing team's OWN leading interpretation of
the residual is **baryonic** (cold H2 in a multiphase core), not a new field. If that is right, the cluster
"deficit" is a baryon-census problem in the core (undetected cold gas tracking the hot gas), which would be a
shared MOND/framework resolution with NO new component and NO a0<->Lambda cost — but it is unconfirmed (cold-gas
masses of ~10x the hot gas in cluster cores are not independently detected).

---

## Bottom line (both ways)

**It is NOT a coherent single missing-mass.** The latest data say the "2x" decomposes into:
1. **A real, uniform, CENTRAL residual** (~400 kpc core, follows the gas, ratio ~10 to gas, intrinsic eRASS1
   scatter ~10%) that survives in relaxed gas-complete clusters and at R500. This is the irreducible piece.
2. **A heterogeneous disequilibrium skirt** (mergers need 3-9x more "missing mass," explicitly attributed to
   non-equilibrium not real mass; ~65-70% of eRASS1 clusters are disturbed) that INFLATES the raw stacked number.
3. **Outskirt systematics** (clumping ~10-15%, hydrostatic bias 10-40%, incomplete gas budget beyond R500) that
   shave the wings but not the core.

The "robust 2x" over-simplifies by stacking (1)+(2)+(3). The honest equilibrium core residual is the ~1.6-2.0
banked floor — real, MOND-shared, central, gas-tracking. **The framework-distinctive payoff: the residual's
shape (core-concentrated, follows-gas) is exactly what density-a0 predicts and standard MOND does not — a real
qualitative match — but no derived smoothing scale delivers the magnitude. LIVE as a constraint/target, banked-null
as a cure.** The lensing team's own baryonic (cold-H2) reading would close it with no new physics if confirmed.

## Sources
- Kelleher & Lelli 2024, A&A 688 A78 (arXiv:2405.08557) — X-COP MOND missing mass, relaxed vs merging,
  non-equilibrium, EFE + 10-40% hydrostatic bias, core-concentrated r^-4 profile.
- Famaey, Pizzuti & Saltas 2025, PhRvD 111 123042 (arXiv:2410.02612) — CLASH lensing: inner core, ~400 kpc cutoff,
  missing-to-gas ratio ~10 uniform, dark-mass-follows-gas, cold-H2 interpretation.
- Zhang, Zonoozi & Kroupa 2026, PRD (arXiv:2602.06082) — 46 z<0.1 clusters; baryons (stars+remnants+ICM) = 88% of
  MOND dynamical mass with IGIMF top-heavy remnants, residual ~12%.
- Kluge+2024 / Zhang+2025 A&A 698 A171 (arXiv:2503.21066) — eROSITA dynamical-state classification, ~30-35% relaxed.
- Eckert+2019 (X-COP), Popesso+2024 (arXiv:2411.16555), Siegel+2025 (arXiv:2509.10455) — gas budget / clumping /
  expulsion beyond R500.
- eRASS1 catalog: Bulbul+2024 A&A 685 A106; real FITS on disk (N=9830).
