# L24 — cluster lensing versus cluster dynamics

`L24_lensing_vs_dynamics.py` / `L24_lensing_vs_dynamics.out`. **5 FAIL of 13. All six controls PASS.**

Every cluster verdict this directory reached — L2 (no kernel), L5 (no fixed-strength long-range
force), L6 (no screened force), L7 (the residual *is* the cosmic dark-to-baryon share), L18 (the
hydrostatic bias makes it worse) — rests on one mass probe: X-ray gas in hydrostatic equilibrium.
This lane brings in the second probe, with orthogonal systematics.

---

## What the repository already had (surveyed, not duplicated)

| where | what it established |
|---|---|
| `prep_2026/mi_lensing_final/` | the **modified-inertia** arm's lensing no-go, at **galaxy** scale: the assembled single-metric MI stress tensor under-lenses, F(y) = g_lens/(ν g_bar) < 1/ν < 1 everywhere; Brouwer 2021's KiDS-1000 lensing RAR gives Δχ² = +722/+754 (both footings, conservative rail). Model-free core: **g_lens ≤ g_bar for any baryonic source**. |
| `prep_2026/kids_rar/` | KiDS-1000 lensing as a third road to a₀ — a *consistency*, explicitly not a free fit. |
| `prep_2026/rar_origin_2026/dark_charge_kids_lensing_gate_2026.py`, AeST boundary-constant closure | galaxy–galaxy lensing gates (KiDS Δχ² ≥ +106 at every m²). |
| `hunt_2026/h67_hff_cores.py` | **asked** for η(r) = M_lens/M_framework in four Hubble Frontier Fields cluster cores and reported honestly that it was **not runnable** — the on-disk tables are member photometry with no convergence map and no lens-model profile. |

**Cluster lensing masses had never entered a framework test in this repository.** They do now.
This lane does *not* redo L18's hydrostatic-bias systematic; it **measures** that bias empirically
for this exact sample, which is a complementary thing.

## The data

* **Dynamics + baryons:** the twelve X-COP clusters, on-disk public profiles
  (`real_research/data/xcop/`; Eckert et al. 2019 A&A 621 A40, Ettori et al. 2019 A&A 621 A39) —
  gas mass, stellar mass, and the forward hydrostatic mass `M_FORW` with errors.
* **Lensing, primary:** Herbonnet et al. 2020, MNRAS 497, 4684 (CCCP+MENeaCS, arXiv:1912.04414),
  Tables 2 and 3. **Five** of the twelve X-COP clusters are in that 100-cluster sample —
  A85, A1795, A2029, A2142, ZwCl1215 — checked name by name against the full published list; the
  other seven have no entry (Eckert et al. 2022 A&A 662 A123 records the same for A644 and A2319).
  NFW fit to the reduced shear over 0.5–2 h₇₀⁻¹ Mpc with the Dutton & Macciò (2014) c–M relation.
* **Lensing, independent teams:** the LC² compilation (Sereno 2015, MNRAS 450, 3665; VizieR
  J/MNRAS/450/3665, table `lc2all` V2.0, matched by coordinate within 2′), which tabulates
  **spherical masses inside fixed physical radii 1.0 and 1.5 Mpc** — Cypriano et al. 2004 (A85,
  A2029), Umetsu et al. 2009 and Okabe & Umetsu 2008 (A2142), Kubo et al. 2009 (ZwCl1215).
* All five lensing clusters have **measured** (not imputed) stellar profiles, so the lensing
  subsample's baryon budget carries no stellar-imputation systematic.

## The framework's lensing sector

The carried arm is modified **gravity** with γ_PPN = 1 (`THE_ACTION_2026-09-05.md` §4), so light and
gas fall in the same potential. Its predicted convergence is κ = Σ_eff/Σ_crit with Σ_eff the
projection of ρ_eff = (1/4πG)∇·g_fw, g_fw = g_bar + a₀Δ(g_bar/a₀), ν_RAR saturated (§3).
**It therefore predicts M_lens(<r) = M_dyn(<r) identically**, so S_lens/S_dyn = M_WL/M_HSE
*per cluster*, exactly — M_fw cancels. (In the summary table the two population means are 1.2278 and
1.1536 rather than equal, because S_lens and S_dyn are inverse-variance weighted with different
weights; the per-cluster identity is exact and is what the difference test in C8 uses.) The framework
has *no freedom* to make the two differ.

---

## The three shortfalls

At each cluster's X-ray R500, five clusters, inverse-variance weighted, **both a₀ footings**:

| quantity | canonical (9.3619e-11) | alt (1.1279e-10) |
|---|---|---|
| **framework vs measured DYNAMICS** S_dyn = M_HSE/M_fw | **1.618 ± 0.022** (28.0σ from 1) | **1.493 ± 0.020** (24.2σ) |
| **framework vs measured LENSING** S_lens = M_WL/M_fw | **1.987 ± 0.246** (4.0σ from 1) | **1.834 ± 0.227** (3.7σ) |
| **measured LENSING vs measured DYNAMICS** M_WL/M_HSE | **1.154 ± 0.147** | **1.154 ± 0.147** (a₀ cancels) |

Independent weak-lensing teams at fixed 1.0 and 1.5 Mpc give S_lens = **1.623 ± 0.080** /
**1.499 ± 0.074** against a mean S_dyn of 1.876 / 1.732 there — the same picture, 1.4σ from the
Herbonnet-based numbers (C9 PASS).

The empirical hydrostatic bias for this sample is **1 − b = M_HSE/M_WL = 0.867 ± 0.111** (stacked
0.892; 0.733 if Herbonnet's aperture-deprojected masses are used instead). That lands on X-COP's own
gas-fraction calibration 0.85 ± 0.05 (Eckert+2019) and on Eckert+2022's "< 10 % out to R500", and is
consistent with CCCP 0.78 ± 0.09 (Hoekstra+2015). This is the first time the bias has been measured
directly for these clusters in this repository, rather than imported from the literature as L18 does.

## The pattern, and what it means

**The two shortfalls are the same.** S_lens − S_dyn = +0.369 ± 0.238 (1.55σ) canonical,
+0.341 ± 0.220 (1.55σ) alt. **C8 FAILS**, and the FAIL is the finding: there is no lensing-sector
signature. Three consequences, all structural:

1. **The cluster residual is not an artefact of hydrostatic equilibrium.** It is present at the same
   size in a probe whose systematics (shear calibration, photometric redshifts, projection) share
   nothing with X-ray temperature gradients. L2, L5, L6, L7 do not rest on the HSE assumption.
2. **No choice of lensing sector can repair it.** A slip changes lensing and leaves dynamics alone,
   and the shortfall is already present in dynamics. This closes a door that was, in principle, open:
   before this lane, one could have hoped a lensing sector would be where the cluster problem was
   solved. It is not, and it cannot be.
3. **The modified-inertia arm is worse here too, independently of Brouwer 2021.** Its model-free
   bound g_lens ≤ g_bar means M_lens ≤ M_bar at these radii; for this sample M_WL/M_bar = **6.6×**,
   against the 1.8–2.0× the modified-gravity arm carries. Cluster lensing excludes the MI arm on its
   own.

## The one place lensing adds something the dynamics could not: shape

ΔΣ(R) = Σ̄(<R) − Σ(R) is what a shear survey actually measures, and it is blind to a uniform sheet.
The framework's phantom is a nearly-flat sheet at these radii, so it produces far less shear than its
enclosed mass suggests:

| | canonical | alt |
|---|---|---|
| d ln ΔΣ / d ln R, framework | −0.26 to −0.38 | −0.26 to −0.37 |
| d ln ΔΣ / d ln R, measured | −0.76 to −0.98 | same |
| slope difference | **+0.531 ± 0.058 (9.1σ)** | **+0.536 ± 0.058 (9.2σ)** |
| deficit in the raw observable, ΔΣ_measured/ΔΣ_framework | **2.68×** | **2.48×** |
| M500 an observer would report for the framework's signal, ÷ its true M(<R500) | **0.429** | **0.443** |
| shape-corrected lensing shortfall | 4.63× | 4.14× |

So the enclosed-mass comparison (≈2×) **understates** the disagreement: in the observable a survey
measures, the framework is short by ≈2.5×, and an observer running Herbonnet's own pipeline on the
framework's predicted signal would report about 43 % of the framework's own M(<R500).

**This is not a pipeline artefact — that is what control C10 is for.** Projecting the *measured*
X-ray hydrostatic mass profile through exactly the same machinery reproduces the *measured*
weak-lensing ΔΣ to a median of **1.11** (scatter 0.40) over 0.5–2 Mpc. The shape mismatch is a
property of the framework's own predicted ρ_eff.

## The PASS/FAIL lines

```
[PASS] C1  [control] projection machinery vs analytic NFW convergence and shear   (max |Sigma error| 1.30e-06, max |DeltaSigma error| 1.09e-06, density-route 2.47e-07)
[PASS] C2  [control] vs analytic singular isothermal sphere (rho ~ r^-2)          (max |Sigma error| 3.41e-13)
[PASS] C3  [control] NFW + Dutton-Maccio reproduces Herbonnet's own M500 from their M200, and the as-observed refitter recovers an injected NFW mass   (max deviation 3.3%)
[PASS] C4  [control] independent read of the X-COP FITS vs the committed audit    (max |diff| 0.00e+00, 124 rows)
[PASS] C5  [control] measured lensing/dynamical ratio in the published bias range (1-b = 0.867 +/- 0.111, both footings)
[FAIL] C6  [test] framework matches the measured LENSING mass                     (S_lens = 1.99 +/- 0.25, 4.0 sigma / 1.83 +/- 0.23, 3.7 sigma)
[FAIL] C7  [test] framework matches the measured DYNAMICAL mass                   (S_dyn = 1.62 +/- 0.02, 28.0 sigma / 1.49 +/- 0.02, 24.2 sigma)
[FAIL] C8  [THE TEST] the two shortfalls differ at > 3 sigma                      (1.55 sigma both footings -- they agree)
[PASS] C9  [indep] independent weak-lensing teams give the same shortfall         (1.4 sigma both footings)
[PASS] C10 [control] projecting the measured dynamical profile reproduces the measured lensing DeltaSigma   (median 1.11)
[FAIL] C11 [shape] framework's lensing profile shape consistent with measured     (+0.531 +/- 0.058, 9.1 sigma; DeltaSigma deficit 2.68x / 2.48x)
[FAIL] C12 [as-obs] NFW-refit shape systematic under 15%                          (as-observed/true = 0.429 / 0.443)
[PASS] C13 [syst] insensitive to truncation and outer baryon slope                (0.3% / 0.1%; no extrapolation inside 1500 kpc)
```

## Where this sits in the published literature

Stated so the result is not mistaken for a discovery. That the MOND cluster residual survives in
*lensing* is known: Natarajan & Zhao 2008 (MNRAS 389, 250) showed MOND plus classical neutrinos
cannot supply cluster lensing; Angus, Famaey & Buote 2008 (MNRAS 387, 1470) found unexplained mass on
the group scale; and **Famaey, Pizzuti & Saltas 2024** (arXiv:2410.02612) characterised the residual
MOND missing mass directly from CLASH strong- and weak-lensing profiles, finding it "in line with
results obtained in the literature from the hydrostatic equilibrium of hot gas". What is new here is
only that the test is run on **this framework's own carried kernel**, on **this repository's own
cluster sample and baryon budget**, on **both footings**, with the two shortfalls measured side by
side at the same radii — and that it closes the lensing-sector escape explicitly.

One flag, not settled here: Famaey+2024's lensing-derived residual is **cored** inside ~1 Mpc,
while this repository's own X-ray inversion (g04a) reports ρ ~ r^−1.53 and *not* cored. Different
radial ranges and different kernels; worth a lane of its own.

## Limits, stated

* **Five clusters.** Seven of the twelve X-COP clusters have no published weak-lensing mass at all.
* **Per-cluster weak-lensing errors are 20–60 %**, so the lensing-versus-dynamics comparison
  constrains a lensing-sector difference only at the ~15 % level. **A slip smaller than that is
  untested, not excluded.**
* Per-cluster M_WL/M_HSE ranges from 0.58 (ZwCl1215) to 1.79 (A1795) — the *mean* is what carries
  the result, not any individual cluster.
* This measures nothing about dark matter and touches nothing at galaxy scale, where baryons plus
  the kernel work at 0.108 dex and a cosmic-share halo would overshoot badly.
* The framework's ΔΣ assumes spherical symmetry, the measured baryon distribution, and no external
  field contribution.
