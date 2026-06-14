# Lensing modality — latest 2023-2026 data + the concrete measurement design (Opus 4.8, 2026-06-14)

Framework a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = **9.355e-11** (eta-worst footing). Density-law superset
a0 = (c/2) sqrt(G rho_total) => the distinctive **a0_local > a0_field**. Quarantine: a0/Z never asserted derived.
Both-ways rule applied: every "confirms" verified as hard as every "kills".

## 1. LATEST DATA (2023-2026)

**Strong lensing — JWST Bullet, the headline result.** Rihtarsic et al. 2026 (arXiv:2503.21870, ApJL) JWST strong+weak
model; Famaey 2026 (arXiv:2605.10022) MONDian re-analysis. The residual missing mass in MOND is **eta ~ 8-9 within 300
kpc of the main-cluster galaxies** (observed baryon+residual+phantom / baryon ~7.5-9), modeled by two Plummer spheres at
(40,55) and (820,220) kpc — i.e. **galaxy-centred, collisionless, total residual 3.4e14 Msun ~ the cluster baryonic
mass**, NOT neutrinos. This is the cleanest lensing statement that the residual is CENTRAL and collisionless-baryon-order.
Joint JWST+DECam (arXiv:2512.03150) separately reclassifies the Bullet as a minor merger (merging does not worsen it).

**Strong+weak Euclid — Abell 2390 (ERO, arXiv:2507.08545).** Combined SL+WL, z=0.228, constrains 30 kpc < r < 2000 kpc
(beyond R200). M200 = (1.48+-0.29)e15 Msun, R200 = 2.05+-0.13 Mpc, NFW c=6.5, r_s=230 kpc; consistent with X-ray HSE
(relaxed cluster). Demonstrates Euclid resolves the profile over >1 dex in radius at 0.13" resolution.

**Cluster lensing-RAR a0 — Tian et al. 2024 (A&A 684 A180, arXiv:2402.12016).** 64 CLASH clusters (WL+SL+X-ray);
cluster acceleration scale **g‡ = (2.0+-0.1)e-9 m/s^2 = ~10x the galactic 1.2e-10 = 21x the framework a0_F**, intrinsic
scatter only **~0.06 dex (15%)** — as tight as the galaxy RAR. 2026 A&A (aa58664-25, kinematic): isolated/noncentral
galaxies follow the standard RAR; **central galaxies of clusters/groups show enhanced accelerations**, onset radius
**shrinks with increasing group mass**; interpreted as residual cold invisible mass, not an a0 shift.

**WL-vs-HSE/kinematic mass ratio — the cross-method lever.** Li+2024 / eROSITA: WL masses run **~110% (2.1x) higher**
than hydrostatic at fixed radius (M500_HSE ~ M500_WL/2.1). Joint eROSITA (A&A aa51266-24, 2024; 22 eROSITA + 10
HIFLUGCS, 68-3820 kpc): **dynamical/kinematic mass up to +40% above HSE at the low-mass end**, ratio DECLINING toward
large radii. The MOND discrepancy is **~0.5 dex (3x) at small/intermediate radii narrowing to ~0.3 dex (2x) at R500** —
an independent (non-lensing) confirmation of the central-largest, outward-shrinking eta(r).

**Euclid WL pipeline & forecast.** XLII / Sereno+2024 (arXiv:2404.08036): unified COMB-CL catalogue-level reanalysis
across **five surveys (CFHTLenS, DES SV1, HSC-SSP S16a, KiDS DR4, RCSLenS)**, validated on PSZ2 + redMaPPer. LXV /
2025 (A&A aa52122-24): WL mass biased low **-14.6+-1.7% (ideal) / -15.5+-2.4% (realistic)**, shear profile fit in
**8 log bins over [0.4, 4.0] Mpc**; only ~3.7% of clusters have individual (S/N)_WL>3 — so the eta(r) shape is a
**STACKING** measurement, not per-cluster. Euclid will yield **~60,000 clusters (z=0.2-2), ~50,000 WL-quality**;
~10% mass precision on the most massive systems. Rubin/LSST (first light 2025, survey from 2026) adds depth over half
the sky; DESC redMaPPer mass-richness already validated on DC2.

**Weak-lensing morphology-RAR (banked, KiDS).** Brouwer+2021 KiDS-1000 lensing RAR extends 2 dex below galaxy
outskirts. Banked re-analysis (`real_research/reviews/lensing_rar/lr_battery_results.md`): the early/late (u-r) split
on Brouwer's released ESD profiles is **8.8sigma (chi2=119.9/15), 15/15 bins early-above-late, +0.261 dex**, hardened
to 8.6-9.2sigma with measured per-class concentrations. This is **a0-INDEPENDENT** (type-dependence at fixed g_bar)
and is the framework's strongest STANDING lensing EXPOSURE.

## 2. HOW TO MEASURE — the concrete tests

**TEST A — Stacked lensing eta(r) shape (Euclid/Rubin), the central-boost test.** Lensing bypasses HSE bias entirely
(Sigma(R) -> Delta-Sigma -> g_obs(r) needs NO equilibrium). Stack N clusters in fixed M500/z bins, measure the shear
in the 8 Euclid bins over [0.4,4.0] Mpc, form eta(r)=g_obs(r)/sqrt(g_bar(r) a0) at a0=9.355e-11.
- Precision (computed): per-radial-bin g_obs fractional error ~3.3%/sqrt(N_stack/100); N_stack=1000 -> ~1.1%/bin,
  10000 -> ~0.3%/bin. The measurement is **systematics-limited, not statistics-limited** (intrinsic scatter, miscentring,
  projection, photo-z dominate). Euclid's -15% WL bias is the leading systematic and must be marginalized.
- Timeline: Euclid Q1 (2025, 63 deg^2) -> first stacks now; DR1 (2026) thousands of clusters; DR2/DR3 (2027-2030) the
  full 50k. Rubin Y1 (2026-27) -> Y10 (2035) doubles the sky and the source density.

**TEST B — WL-vs-X-ray mass-ratio profile, the bias-free eta normalization.** The cross-method ratio M_WL/M_HSE(r)
directly removes the HSE bias the whole cluster-MOND deficit hinges on. eROSITA already gives M_dyn/M_HSE declining
outward; Euclid WL on the SAME eROSITA clusters (eRASS1, N=12247) pins whether eta(R500) is ~1.0 (HSE-driven) or ~2.1
(real). On the framework's own dS-Unruh interpolation the eRASS1 WL-calibrated **eta(R500) median = 2.33** (computed
here, N=9830) — the high end of the cross-method bracket [1.0, 2.15], because eRASS1 M500 are themselves WL-calibrated.

**TEST C — Environment-split lensing-RAR, the a0_local > a0_field test.** Density-a0 predicts cluster-MEMBER galaxies
(high local rho) sit ABOVE matched FIELD galaxies (low rho) on the RAR at fixed g_bar. Galaxy-galaxy lensing of
cluster-members vs an isolated field control, both at fixed stellar mass AND morphology, isolates the DENSITY axis the
8.8sigma morphology split confounds. Euclid/Rubin GGL S/N is ample (millions of lens-source pairs); the design
challenge is the matched control, not statistics.

## 3. WHAT IS DISTINCTIVE — and what confirms vs kills (both ways)

**The framework's central-density-a0 prediction is the OPPOSITE sign of the observed eta(r).** Density-a0 boosts a0
MOST where rho is highest = the CENTER -> g_pred largest at center -> **eta SMALLEST at center**. But every method
(eRASS1, Eckert eROSITA 0.5->0.3 dex, Famaey Bullet eta~8-9 within 300 kpc, the 2026 A&A onset radius) shows eta
LARGEST at center, shrinking outward. **Read at the LOCAL density the framework's distinctive density-a0 predicts the
WRONG sign for the eta(r) shape** — a clean potential falsifier.

The ONLY reading that survives is the **Mpc-smoothed** a0: at the R500-mean density (500 rho_crit = 730 rho_DE)
density-a0 gives **27x a0_F vs Tian's observed 21x** (a0_cluster=2e-9) — right ballpark, ~1.3x overshoot, and naturally
~universal (fixed overdensity -> Tian's 0.06-dex tightness). BUT this Mpc-smoothing is the **untuned, NOT-derived ell**
the banked work flagged (derived horizon ell is Gpc); and read at the BCG-core local density it gives 60-380x, far over
Tian's 21x, breaking the galaxy RAR. So the cluster-a0 magnitude match is suggestive but NOT banked — it rides the
untuned-Mpc-ell problem and inverts the radial shape.

**The 8.8sigma morphology split is NOT a clean a0_local>a0_field confirmation (verified both ways).** To make early
sit +0.261 dex above late via a0 needs d log a0 = 0.52 dex (3.3x) -> d log rho_total = 1.04 dex (11x) between early/late
environments — far above the morphology-density few-x contrast. AND the framework's OWN field test
(`A0_COSMICWEB_ENVIRONMENT_2026-06`) measured d log a0/d log(1+delta) = **+0.05+-0.04** (1.2sigma from 0, 6.8-10.5sigma
from the predicted +0.5): the density-a0 lever that would "explain" the split is EXCLUDED on the field RAR. So the split
stays a STANDING EXPOSURE to the type-blind universal-RAR reading, not a density-a0 win. The genuine a0_local test is
TEST C (controlled density at fixed morphology), not the morphology split.

**Confirm vs kill (lensing channel, both ways):**
- CONFIRMS distinctive density-a0: cluster-member galaxies sit ABOVE matched field at fixed g_bar+morphology with
  slope d log a0/d log(1+delta) -> +0.5 (TEST C); AND the cluster-a0 tracks the Mpc-mean density (~universal 2e-9).
- KILLS distinctive density-a0: TEST C returns slope ~0 (consistent with the +0.05+-0.04 field null) -> no density
  boost -> the cluster-a0 magnitude match was coincidence and the framework is the type-blind universal RAR (already
  8.8sigma-exposed). KILLS the central-boost shape outright: stacked lensing eta(r) (TEST A) confirms eta LARGEST at
  center / shrinking outward at high precision while the framework local-density reading predicts the OPPOSITE — the
  Mpc-smoothed escape is the only survivor and it is not framework-derived.
- The standard-MOND shared part (a phantom-halo lensing boost of order sqrt(g_bar a0)) the framework reproduces within
  Brouwer's ~0.1-0.2 dex scatter, sitting ~0.054 dex low in deep-MOND at 9.355e-11 (a soft pass, not a win). That is
  NOT distinctive; the distinctive content is the eta(r) SHAPE and a0_local, both addressed above.

NET: lensing is the cleanest channel to test the framework because it bypasses HSE bias, and Euclid/Rubin will deliver
the resolved eta(r) and the environment-split GGL within 2026-2030. The framework's distinctive central-boost
prediction is, on the local-density reading, the WRONG SIGN vs all current data; only the Mpc-smoothed (untuned-ell,
not-derived) reading survives and even that overshoots the radial shape. Both-ways: no manufactured cure (the central
match inverts the shape), no high-priest dismissal (the cluster-a0 MAGNITUDE genuinely lands in Tian's ballpark and the
test is concretely measurable).
