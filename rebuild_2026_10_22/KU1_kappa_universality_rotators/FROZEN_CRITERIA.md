# KU1_kappa_universality_rotators — FROZEN CRITERIA (before any script or number)

Question: is κ the same for fast and slow rotators? If κ is a constant of nature, galaxies of the same stellar mass and
velocity dispersion must sit on the same law whatever their rotational support. A class-dependent offset would make "κ = 1/2" a
population average, and a derivation would be aimed at the wrong target.

Owner's yes, 2026-11-03, after reading arXiv 2610.40789 (Waldrop, Psaltis, Özel, Güver: λ_R from integrated Hα). That paper's
network isn't needed here: the catalogue below has λ_Re measured directly from the MaNGA IFU, which is better than a network
estimate of it. κ = 1/2 FITTED. Footings 9.3603e-11 and 1.1312e-10, never pooled. Not theory closed. Nothing here says the data
favour the framework. **No download**: data on disk from LAM1.

**Not blind:** VS1 found slow rotators +0.12 dex above fast at fixed mass (n 4 slow / 12 fast, all slow ones centrals; NOT
SEPARATED). LAM1 stage 0: 6063 DynPop galaxies with Qual >= 1, 514 slow among the 5811 with SDSS fibres. No residual from this
catalogue has been computed by me.

## Data
`_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits` (MaNGA DynPop, Zhu et al. 2023). HDU 1: Lambda_Re, Eps_MGE,
Sigma_Re, nsa_elpetro_mass, nsa_sersic_mass, z, Qual. HDUs 2-11: ten JAM mass models, each with log_Mt_rhalf (total mass within
the 3D half-light sphere) and rhalf_arcsec.

## Sample
Qual >= 1; nsa_elpetro_mass > 0; z > 0.005; finite Lambda_Re, Eps_MGE, Sigma_Re > 0; log_Mt_rhalf finite in at least 8 of the
10 models. Slow rotator (Cappellari 2016): Lambda_Re < 0.08 + Eps_MGE / 4 and Eps_MGE < 0.4. Fast: all others.

## Accelerations at r_half
r_half = rhalf_arcsec (median over models) × D_A, D_A from z with the same low-z Hubble law for every galaxy (the comparison is
relative: both classes scale identically, so H0 cancels to first order; the absolute level is beside only).
g_obs = G M_t(r_half) / r_half^2, M_t the median over the ten models. g_bar = G (0.5 M*) / r_half^2, M* = NSA elpetro mass
converted from h = 1 to the same H0. Gas ignored (gas-poor at r_half for most; stated).
Residual against the board law (simple nu) at each footing: r_i = ln g_obs - ln(nu(g_bar / a0) g_bar).

## Statistic
Matched cells: 0.2 dex in log M*, 0.1 dex in log Sigma_Re (σ matching is the frozen guard against an IMF that varies with σ).
In each cell with at least 2 slow and 2 fast: D_cell = median r(slow) - median r(fast), weight min(n_slow, n_fast).
**D** = weighted mean over cells. Also printed: the implied shift in ln a0, D / (d ln g_model / d ln a0) at the matched sample's
median y.

## Errors
sigma_stat: bootstrap over galaxies (2000, seed fixed), cells rebuilt each time. Systematics, added in quadrature:
(a) JAM model: standard deviation of D over the ten models used one at a time; (b) stellar mass: |D(sersic mass) - D(elpetro)|.
**Unpriced and stated:** a class-dependent IMF at fixed σ; aperture effects in NSA masses.

## Labels, per footing
- **NO POWER** if sigma_D > 0.06 (half of VS1's 0.12): the test can't see a VS1-sized offset; no other label.
- Otherwise **UNIVERSAL** if |D| <= 2 sigma_D; **DIFFERS** if |D| > 3 sigma_D; **NOT SEPARATED** in between.
- A DIFFERS result is read as "κ or mass-to-light differs by class"; this lane can't tell which. UNIVERSAL supports one κ
  across rotational support at r_half accelerations only.
- Beside, not graded: D with central/satellite ignored as here (DynPop has no group flag); the absolute median residual per class.

## Checks
- C1: at least 100 slow and 1000 fast in the sample, and at least 20 matched cells.
- C2: the residual function reproduces the board law: r = 0 to 1e-12 when g_obs is replaced by the law's prediction.
- C3 injection: add +0.12 dex (ln 0.276) to every slow rotator's g_obs; D rises by 0.276 +- 0.02.
- MUTATE (`--mutate`): class labels shuffled within each matched cell (seed fixed); |D| <= 2 sigma_D required, outputs to
  `*_MUTATE.*`, exit 1.
Exit 0 only if C1-C3 pass.

## Limits stated in advance
r_half accelerations are mostly well above a0 (boost small), so the implied a0 shift is a large multiple of D. Sphere-enclosed
g_obs from JAM is model output, not raw data. No environment control.
