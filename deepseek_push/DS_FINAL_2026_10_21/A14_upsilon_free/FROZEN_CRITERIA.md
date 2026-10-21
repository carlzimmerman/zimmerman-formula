# A14 — FROZEN CRITERIA

Written before the production fit was run. Everything in this file is fixed; the
fit in `a14_checks.py` may not change any of it. Where a choice was arbitrary it is
labelled as such and a declared robustness variant is given, so the reader can see
how much the answer depends on it.

Order of operations, disclosed honestly: a **census** (counts only, no fits) was run
first to learn whether an Upsilon-free subset exists at all at thresholds 0.6–0.95.
The threshold was then fixed at 0.80 from the physics in §2 below — not from that
census — and all fits were run afterwards. The census is reported as a declared
robustness scan in the report, not as tuning: the primary is 0.80 and it does not move.

---

## 1. Data

Only files already on disk. No network.

| what | file |
|---|---|
| rotation curves + baryonic components | `real_research/data/sparc_data/*_rotmod.dat` (175 files) |
| D, e_D, f_D, inclination, R_disk, quality flag Q | `real_research/data/SPARC_Lelli2016c.mrt` (Lelli, McGaugh & Schombert 2016, Table 1) |

Column meaning in `*_rotmod.dat` (SPARC convention, **verified in-script**, K0):
`Rad[kpc] Vobs errV Vgas Vdisk Vbul SBdisk SBbul`. `Vobs` is the deprojected
circular speed in km/s (Doppler — distance-independent). `Vgas` includes the
1.33 helium correction and is the *total* gas contribution. `Vdisk` and `Vbul` are
the stellar templates for **M/L = 1** at 3.6 μm, so the physical contribution is
`Upsilon * Vdisk^2`. This is the convention used by every SPARC RAR paper and by
this repo (`fable_independent_2026/L232_sparc_parameter_free.py:42`); it is
re-verified from the photometry in K0 rather than assumed.

**Mass model used for the gas-fraction test** (the only place a stellar M/L enters,
and it enters the *selection*, not the fit):

    Vbar^2 = Vgas^2 + 0.5*Vdisk^2 + 0.7*Vbul^2          (Chabrier, SPARC standard)

## 2. Selection — the Upsilon-free subset

A galaxy is in the primary sample iff **all** of:

- **S1 (gas dominance).** For every point in the fitted range,
  `f_gas = Vgas^2 / (Vgas^2 + 0.5 Vdisk^2 + 0.7 Vbul^2) > 0.80`.
- **S2 (fitted range).** `R > 2 R_disk`, `R > 0`, `Vobs > 0`, `errV > 0`,
  `errV/Vobs < 0.10`, `Vgas > 0`. The 2 R_disk cut is the standard "outside the
  bulge/beam-dominated core" cut; R_disk is Table 1's 3.6 μm disk scale length.
- **S3 (depth).** `min(g_bar) < a0_can = 9.3603e-11` over the fitted range, i.e. the
  curve actually reaches the deep branch. `g_bar = Vbar^2/R` with R in metres.
- **S4 (size).** At least 3 points in the fitted range.
- **S5 (quality).** SPARC quality flag `Q <= 2` (excludes the poor curves).

The threshold 0.80 is **arbitrary but principled**: the residual sensitivity of the
fitted a0 to the stellar M/L is `dln a0/dln Upsilon = -(1 - f_gas)` in the deep
limit (§4). At f_gas = 0.80 the IMF bracket (Chabrier -> Salpeter, +0.24 dex in
Upsilon) can still move a0 by ~12%, which is the honest size of what "Upsilon-free"
buys. It is not zero, and it is not claimed to be zero.

Declared robustness variants (reported, never substituted for the primary):
`f_gas > 0.70, 0.75, 0.85, 0.90`; `Q <= 1`; `f_D = 1` only (Hubble-flow distances);
`f_D = 2` only (2–5% distances); `f_gas` evaluated at Upsilon_d = 0.87 (Salpeter).

## 3. The two laws (BRIEF §1), both fitted

    L1 canonical :  g = (g_N/2) (1 + sqrt(1 + 4 a0/g_N))
    L2 quadratic :  g = sqrt(g_N^2 + a0 g_N)          (n = 2 "a0-line")

One free parameter, `a0`. No Upsilon, no per-galaxy nuisance parameter, no halo,
no intrinsic-scatter parameter. `g_N = g_bar`.

## 4. The distance scaling — derived here, before fitting

A distance rescaling `D -> f D` at fixed **angular** position sends

| quantity | scaling | reason |
|---|---|---|
| `r` | `-> f r` | geometry |
| `V_obs` | `-> V_obs` | Doppler, distance-free |
| `V_gas` | `-> f^(1/2) V_gas` | `M_gas ∝ D^2` from the HI flux, `V^2 = GM/r ∝ f^2/f` |
| `V_disk, V_bul` | `-> f^(1/2) V_*` | surface brightness is distance-free, `M_* = Upsilon L`, `L ∝ D^2`, `R_d ∝ D` |
| `g_bar` | **invariant** | `V_bar^2/r ∝ f/f` |
| `g_obs` | `-> g_obs/f` | `V_obs^2/r` |

So a distance error is a **pure vertical shift** of the RAR, and in the deep limit
`g_obs = sqrt(a0 g_bar)` gives

    a0  ->  a0 / f^2        (exact in the deep limit; O(sqrt(g_bar/a0)) corrections otherwise)

This is *not* the `a0 ∝ 1/f` of a "freeze V_bar and move only r" bookkeeping, which
implicitly rescales the baryonic mass as `M ∝ D` instead of `D^2`. The exponent is
tested against the data themselves in K5 (per-galaxy a0 scatter vs the published
`e_D`), so the statement is not merely asserted.

Consequences: a 5% distance error is a 10% error in a0 and in kappa; the H0
zero point 73 -> 67.4 (7.42% in D) is a **14.8%** error in a0, coherent over the
whole sample, and no sample size removes it.

## 5. Likelihood

    chi^2(a0) = sum_i [ (Vobs_i - Vmodel_i)^2 / sigma_i^2 ]
    Vmodel_i  = sqrt( g_model(g_bar_i; a0) * r_i )      [m/s -> km/s]
    sigma_i^2 = errV_i^2 + (0.05 Vobs_i)^2              <-- the 5% error floor

(floor declared per the task; it is applied to every point, in both laws, in every
variant). One parameter, so the 1-sigma interval is `Delta chi^2 = 1`.

**Statistical error, declared:** the 73 points are *not* 73 independent measurements
— they are 12 galaxies, each carrying a coherent distance error and a coherent
intrinsic offset. The primary statistical error is therefore a **block bootstrap
resampling galaxies** (fixed seed, 400 draws), not the per-point `Delta chi^2 = 1`
interval. The latter is reported too, scaled by `sqrt(chi^2_red)`, to show how much
it understates the truth.

**Systematic budget, declared in advance** (all coherent, added in quadrature as the
nominal and linearly as the worst case):

| term | how it is computed |
|---|---|
| distance zero point | `2 * ln(73/67.4)` = 14.8%, coherent |
| residual stellar M/L | measured slope `dln a0/dln Upsilon` x the Chabrier->Salpeter bracket 0.24 dex |
| law choice | half the L1-L2 difference in a0 |
| helium correction | 1.33 -> 1.36 in M_gas, `a0 ∝ V_bar^-2` |
| sample scatter | the block-bootstrap value itself |

Deliberately **excluded** from the budget and named in the report: pressure
support / asymmetric drift (order +10% in a0 for these V ~ 50 km/s dwarfs, always
in the direction that raises a0), and beam smearing (raises with distance, so it is
degenerate with the f_D = 1 / f_D = 2 split).

## 6. kappa

    kappa = a0 / (c sqrt(G rho_DE))

with `rho_DE` on **two** conventions, both computed in-script:

- **CMB-normalised**: `rho_DE = 3 (Omega_L h^2) H100^2 / (8 pi G)`, Planck 2018
  `Omega_m = 0.3153, h = 0.6736` -> `Omega_L h^2 = 0.3109`. This is the density the
  CMB actually measures; it is independent of the local H0.
- **local**: `rho_DE = 3 Omega_L H0^2/(8 pi G)` with `H0 = 73.0`, `Omega_L = 0.685`.

The two differ by `sqrt(rho_local/rho_CMB) = (73/67.4) sqrt(0.685/0.6853) = 1.0831`
in kappa, exactly.

## 7. Predictions registered before the fit (falsifiable)

- **P1.** The Upsilon-free sample is small: fewer than 20 galaxies of 175.
- **P2.** Because the sample is dwarfs and the scatter is galaxy-level, the
  statistical error on a0 will be >= 10%, i.e. >= 10% on kappa — larger than the
  5% target and larger than the 0.076/0.465 = 16% error on the record's number.
- **P3.** The two rho_DE conventions plus the two footings will not be internally
  consistent at 5%; the convention spread alone exceeds the target.
- **P4.** 5% kappa is not reachable by adding galaxies of the SPARC type, because
  the coherent distance zero point (14.8%) is a floor.

These are the things that could have come out the other way. They did not, and §
"What this does not do" in `report.md` says what would overturn them.

## 8. What is NOT allowed

- No changing the threshold to raise N.
- No dropping galaxies to lower the error bar.
- No fitting Upsilon, a distance scale, or an intrinsic scatter as free parameters.
- No quoting `a0` alone without the law and the density convention attached.
