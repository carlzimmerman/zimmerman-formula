# L23 — independent verification of "the Coma UDG kill FIRED at 19.4σ"

Script: `fable_independent_2026/L23_udg_verify.py` · output: `L23_udg_verify.out` · 23 checks, 0 FAIL.

## The claim on the record

The 2026-09-03 57-item sweep logged as liability (9):

> "the Coma UDG kill FIRED — 11 galaxies +1.195 ± 0.062 dex = **19.4σ** above the EFE prediction,
> all same sign, offset tracks the external field"

It is carried verbatim into `THE_ACTION_2026-09-05.md` §6.5 as a standing liability. Source:
`hunt_2026/h9_h11_pressure_supported.py`, ITEM 9. Never checked by a second pass until now.

## Verdict in one line

**The number stands. The sigma does not.** The offset is reproduced, survives a corrected
external-field treatment, and is carried on its own by the single best-measured ultra-diffuse
galaxy in existence — but "19.4σ" is a statistics-only error bar on eleven galaxies that share one
mass-to-light scale, one estimator and one cluster model. With the coherent systematics priced,
the same data give **4.9σ (canonical) / 4.7σ (alt)**, and **2.7σ** on the first-infall hypothesis
that the field's own MOND simulations endorse. The record should read *a ~5σ liability with a
factor-14 amplitude*, not a 19.4σ kill.

## What was compared with what

Eleven Coma UDGs from Freundlich, Famaey, Oria, Bílek, Müller & Ibata 2022, A&A 658, A26
(arXiv:2109.04487), Tables 1–2 — nine with MMT/Binospec dispersions and SSP mass-to-light ratios
from Chilingarian et al. 2019 (ApJ 884, 79), plus DF44 and DFX1 from van Dokkum et al. 2016/2017/2019.
I rebuilt `g_bar` and `g_obs` from the raw `(L, M/L, R_e, σ_eff)` rather than from h9's pipeline and
recovered the published columns to 0.016 dex, which also identifies the convention:

- `r_1/2 = 4R_e/3`, `g_obs = 3σ_eff²/r_1/2` (Wolf et al. 2010), `g_bar = G(M_*/2)/r_1/2²`.
- Internal accelerations `g_bar/a₀ = 0.004–0.014` — 1.5 dex below the lowest SPARC point.
- Kernel: ν_RAR with the saturated Δ (`THE_ACTION` §3). Both footings, 9.3619e-11 / 1.1279e-10.
  The saturation branch is inert here (everything sits far below s = 2.540).

## The external field — the expected crux, and it was not the crux

h9 made **two real errors**, and they point in opposite directions and nearly cancel.

1. **The NFW is not self-consistent.** M200 = 1.3e15 M☉ at z = 0.023 implies R200 = 2292 kpc; h9
   used 2900 kpc. At fixed M200 and c that dilutes the profile, so h9's external field was *too
   weak* and its deficit *too small*. (g_ext at 1.13 Mpc: 0.665 a₀ used vs 0.840 a₀ correct.)
2. **The ν argument is one closure inversion short.** In the field equation ν acts on the
   *Newtonian* field of the real matter; the programme's own registered convention is x = y·ν(y)
   (`prep_2026/gaia_dr4_prep/aqual_efe_full_solve_2026.py` provenance block, 1.8996 → 1.28903,
   reproduced here to 2.3e-4). h9 fed ν the *observed* acceleration from Coma's weak-lensing mass.
   That **overstates** the suppression by +0.140 dex per galaxy.
3. On the third axis h9 was *generous*: it used the bare ν, the largest eigenvalue. An isotropic
   dispersion measures the sphere average ν(1+L/3) (`hunt_2026/f01_efe_sphere_average.py`,
   reproduced here independently to 5e-9), which is 0.059 dex *lower* — i.e. the correct treatment
   makes the deficit worse.

Net effect, running every combination of three Coma mass models (h9's NFW, the self-consistent NFW,
and Freundlich's own X-ray β-model, kT = 8.6 keV / r_c = 276 kpc / β = 0.71, which my implementation
validates against their published 5.6e14 M☉ Newtonian-equivalent asymptote) × two 3-D position
choices × the two ν conventions × the two couplings:

| | isolated | EFE-on |
|---|---|---|
| h9 as recorded (canonical) | +0.396 | **+1.196** (19.4σ stat) |
| corrected, β-model, Einasto 3-D, canonical | +0.396 | **+1.159** |
| corrected, alt footing | +0.358 | **+1.112** |
| full arm spread, canonical | — | +1.089 to +1.264 |

**The external field is not the escape.** Nor is the 3-D position: at 9 Mpc — four virial radii,
the turnaround scale, the most generous geometry a Coma member can have — the EFE still costs
+0.635 dex against an isolated floor of +0.396.

## Where the 19.4σ actually comes from, and why it fails

`0.062 dex = 1/√Σw` — an inverse-variance error on the mean of eleven galaxies, using only the
per-object σ and luminosity errors, as if the eleven were statistically independent. They are not.
Every systematic that matters is **common to all eleven** and therefore does not average down:

| systematic | 1σ (dex) |
|---|---|
| stellar M/L and IMF (**explicitly not propagated** by the source paper) | 0.148 |
| aperture + orbital anisotropy on σ_eff | 0.120 |
| Coma mass model + 3-D position (equilibrium arms) | 0.088 |
| velocity-dispersion instrumental systematic (9 of 11) | 0.052 |
| σ → acceleration estimator (Wolf point vs Milgrom-1994 virial) | 0.047 |
| a₀ footing | 0.047 |
| distance to Coma (±5%) | 0.021 |
| **quadrature sum** | **0.227** |
| statistical, as quoted | 0.062 |

Two further statistical points, one each way:

- **Against the escape:** χ²/dof = 1.53 about the weighted mean — the scatter *is* consistent with
  the quoted errors, so there is no variance-inflation argument. The statistical part of h9's error
  bar is sound; it is the absence of a systematic floor that is wrong.
- **Against h9:** its diagnostic "the offset tracks the external field, so it is the EFE and not
  scatter" is **half tautological** — the EFE term is by construction a decreasing function of
  x_ext with slope −L = +0.33 of the +0.68 measured. The non-circular version (the *isolated*
  offset regressed on x_ext) gives +0.41 at permutation p = 0.42. **That claim should be withdrawn
  as evidence**; it does not touch the offset itself.

## Systematics that were tested and do *not* rescue it

- **Mass-to-light ratio.** In the EFE-dominated regime the prediction is strictly linear in M/L, so
  closing the gap needs **every** M/L multiplied by 14.4×, taking Chilingarian's spectroscopically
  measured 0.37–1.48 to 5.3–21.4. No stellar population reaches that.
- **The σ → acceleration estimator.** The Wolf point estimate and the exact deep-MOND virial
  relation σ⁴ = (4/81)GMa₀ (Milgrom 1994) agree to +0.045 ± 0.003 dex. Not an escape.
- **The dispersions.** Chilingarian's nine are at R ≈ 4800 (σ_inst ≈ 26.5 km/s) with S/N 4–5/pixel,
  and a 5% error in σ_inst costs 0.02–0.11 dex per object. But **DF44 alone** — 33.3 hr of
  Keck/KCWI, σ = 33 ± 3 km/s, no resolution issue — carries **+0.938 ± 0.139 dex on its own**.
  Reported the other way too: the nine MMT objects do sit +0.29 ± 0.14 dex (2.2σ) above the two
  Keck ones, a flag on the Binospec dispersions worth recording but not enough to move the verdict.
- **Tides.** Closed by the literature, not by me: Nagesh, Freundlich, Famaey, Bílek, Candlish,
  Ibata & Müller 2024, A&A 690, A149 (arXiv:2407.03413) simulated exactly these objects in MOND
  with Phantom of Ramses and found that for UDGs *in equilibrium* "tides are not sufficient to
  increase their velocity dispersions to values as high as the observed ones."

## The one escape the literature leaves open

Nagesh+2024's surviving MOND option is that these are **out-of-equilibrium objects on first radial
infall**, whose dispersions reflect the far weaker field near turnaround rather than the field at
their instantaneous position. Priced here: at 9 Mpc the offset falls to +0.635 dex = **2.7σ**.
That is a hypothesis about the sample, not a repair of the theory, and it is strained for the
objects at 188–540 kpc projected — but it is a real, published, simulated escape and must be
carried.

## Controls

- **SPARC control.** Same kernel, same footings, same log-residual machinery: median residual
  −0.022 dex on 29 dwarfs with V_flat < 80 km/s and +0.022 dex on all 147 galaxies. The pipeline is
  not a machine that rejects everything.
- **Round-trip control.** A mock sample built to *be* the EFE prediction returns 1.8e-15 dex.
- **Reproduction control.** h9's headline recovered from an independent rebuild:
  +1.1961 ± 0.0616 = 19.4σ canonical, +1.1679 alt, isolated +0.3965 — against h9's +1.195 ± 0.062,
  +1.166, +0.396. Every later difference is therefore attributable to a *named* assumption.

## The recomputed significance

| arm | offset (dex) | σ |
|---|---|---|
| h9 as recorded (statistics only) | +1.196 | 19.4 |
| corrected EFE, equilibrium, canonical | +1.159 | **4.9** |
| corrected EFE, equilibrium, alt | +1.112 | 4.7 |
| corrected EFE, first infall at 9 Mpc | +0.635 | 2.7 |
| the EFE term alone (isolated offset as a common nuisance) | +0.763 | 6.0 |

**Dominant systematic: the stellar mass-to-light ratio and IMF, 0.148 dex** — the one the source
paper states it did not propagate. Physically the equilibrium arm is a factor 14.4 in acceleration
and 3.8 in velocity dispersion; the first-infall arm 4.3 and 2.1.

## What the record should say

Replace "the Coma UDG kill FIRED at 19.4σ" with:

> **Coma UDGs (11, Freundlich+2022): the framework's EFE prediction sits +1.16 dex (canonical) /
> +1.11 dex (alt) below the observed accelerations — a factor 14 in acceleration, 3.8 in σ, all
> eleven the same sign, carried on its own by DF44. Statistical 0.062 dex, coherent systematic
> floor 0.227 dex ⇒ 4.9σ / 4.7σ, falling to 2.7σ if the sample is on first infall (Nagesh+2024).
> h9's "offset tracks the external field" diagnostic is withdrawn as half-tautological. Two errors
> in h9's EFE treatment (non-self-consistent R200; ν fed the observed rather than the Newtonian
> field) nearly cancel and do not change the conclusion.**

It remains the framework's largest single-system liability. It is not a 19.4σ falsification.
