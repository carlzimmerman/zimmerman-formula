# XR29: the Milky Way's outer rotation curve in the derivation chain's law

**Question.** Does the chain's static law (FP7's AQUAL-type root: two-field AQUAL with the P2 primitive, heat filter xi, H_Y band-pass L)
reproduce the Gaia-era Milky Way rotation curves out to 25-27 kpc, including the decline that Jiao+2023 call Keplerian and that
Coquery & Blanchard 2025 (A&A 703, A88) use to argue MOND needs a0 < 0.53e-10 m/s^2?

**Short answer.** Yes for the decline, with a price. The law reproduces the outer points (R >= 19 kpc) of all four curves, and none of
them falls below the law's floor for the lowest census baryons. To match the inner normalisation, though, it needs a stellar mass of
7.3-8.2e10 Msun. That is 4-5 sigma above the McMillan 2017 and Cautun 2020 structural censuses, and 1.1-1.5 sigma above Licquia &
Newman 2015 on the alt footing. The real misfit is the mid-disc shape (8-19 kpc), not the outer decline. At the fitted mass the law's
curve falls from about 8 kpc onward (-2.2 to -2.9 km/s/kpc), while Eilers and Zhou fall at -1.7. Nothing here says the theory is
closed.

Script: `XR29_mw_outer_curve.py` (run from the repository root; `MUTATE=1` first). Main run: 16/17 checks pass, 0 load-bearing failures,
615 s, rc = 0. MUTATE: T1 fails, rc = 1.

## The law and the inputs

- Law: Phi = Phi_N + chi, div[mu_s(|grad phi|/a0) grad phi] = 4 pi G S rho, mu_s = x/(1-2x). It is solved with FP7's own dual
  (flux) Kacanov solver, exec'd read-only from FP7's source, axisymmetric (R, z). The spherical law is P2 exactly.
- Footings (FP0): canonical 9.3603e-11, alt 1.1312e-10 m/s^2. kappa = 1/2 is fitted (Z = kappa = 5.7888). No new constant is added.
- Baryons (stellar part scaled by f_*; gas fixed):
  - McM17: McMillan 2017, the record's model, verified against the record's functions to 1.3e-15.
  - McM17r: the record's refit cell (1.30, 0.90).
  - Cau20: Cautun+2020 contracted-halo fit, with and without its CGM (6.4e10 inside 218 kpc).
  - Cau20N: Cautun's NFW-halo column.
  - B2: de Salas+2019 B2, as used by Ou+2024, Jiao+2023 and Coquery & Blanchard.
- Data:
  - E19: Eilers+2019, Table 1 (committed file).
  - O24: Ou+2024, Table 1 (committed file).
  - Z23: Zhou+2023, Table 4. Transcribed from the arXiv PDF.
  - J23: Jiao+2023, Table 3. Transcribed from the arXiv PDF and checked against the HTML.
  - B22: Bird+2022, M(<52) and M(<73 kpc) (committed file).
  - Systematics are the authors' own budgets. Details:
    - E19 and O24: envelopes read by eye from their Figs. 4 and 5.
    - Z23: 1-3%, from the text and Fig. 12.
    - J23: the tabulated sigma already includes systematics.
    - A correlated variant (normalisation plus the published slope systematic) is given for E19 and Z23.

## Results (McM17 shape; chi^2 with the published stat (+) sys budget)

| curve | N | chi^2 at census (can / alt) | fitted M_* [1e10] (can / alt) | chi^2 at fit (can / alt) | outer R>=19 at fit (can / alt) | decline-only R>=13, f_* free (can / alt) |
|---|---|---|---|---|---|---|
| E19 | 38 | 670 / 444 | 7.75 / 7.31 | 20.6 / 9.3 | 1.4/10, 2.1/10 | 3.2/21, 3.5/21 |
| O24 | 37 | 791 / 524 | 8.19 / 7.65 | 27.5 / 18.3 | 3.2/11, 7.0/11 | 9.2/22, 12.5/22 |
| Z23 | 34 | 4630 / 3186 | 8.21 / 7.73 | 160 / 68 | 4.3/6, 0.6/6 | 4.4/17, 4.0/17 |
| J23 | 18 | 603 / 358 | 8.02 / 7.37 | 30.5 / 27.2 | 4.7/8, 9.9/8 | 12.6/13, 19.7/13 |

- **At the census baryons** (McM17 M_* = 5.45e10 plus 1.19e10 gas), the predicted v_c in km/s is:

  | R [kpc] | 5 | 8.2 | 10 | 15 | 20 | 25 | 30 | 50 | 100 |
  |---|---|---|---|---|---|---|---|---|---|
  | canonical | 201 | 203 | 199 | 189 | 183 | 180 | 178 | 173 | 170 |
  | alt | 204 | 207 | 204 | 195 | 190 | 187 | 185 | 181 | 179 |

  Every shape and footing is 19-40 km/s low at 5-12 kpc (H1).
- **At the E19-fitted mass** (canonical, M_* 7.75e10), the prediction is:

  | R [kpc] | 5 | 8.2 | 10 | 15 | 20 | 25 | 30 | 50 | 73 | 100 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | v_c [km/s] | 234 | 232 | 226 | 210 | 201 | 196 | 192 | 187 | 185 | 184 |

  The full predicted-versus-measured tables are in the .out (section C).
- **Shape dependence.**
  - Z23's whole curve fits only with Cautun-shaped (more extended) discs on the alt footing: chi^2 = 28.8/33 and 26.1/33.
  - McM17 misses Z23 on both footings (p < 1e-3).
  - J23's whole curve is marginal on every shape: best p = 0.09.
  - The misfit sits at 8-19 kpc. The model is up to 1.7 sigma high at 5-9 kpc and up to 2.9 sigma low at 12-19 kpc.
- **The decline.**
  - At the fitted mass the outer points are reproduced for every curve (best p_outer 0.84-0.999).
  - With statistical errors only: E19 p 0.65 / 0.23, O24 p 0.012 / 0.000, Z23 p 0.000 / 0.69.
  - The floor (M_* = 3.0e10) lies below every outer point: margins +0.9 to +6.9 sigma on the best shape, +0.2 to +4.2 on the worst.
  - The outer power-law index is -0.09 to -0.14 for the model. The data give -0.19 (Z23) to -0.40 (J23) from this lane's fits,
    and the published values are -0.47 (J23) and -0.56 (O24). The model is shallower by 0.3-2.0 sigma: +2.3 / +2.5 sigma against
    J23's published value.
  - Newton on baryons (the MUTATE) gives -0.53 and fails the outer points: chi^2_outer 36-373.
- **Decline-only fits** (the Coquery & Blanchard setup, but in the chain's AQUAL law at its fixed a0): J23 gives p = 0.48 / 0.10 (McM17)
  and 0.77 / 0.38 (B2), at M_* = 7.6-9.5e10.
- **Free-a0 diagnostic** (algebraic P2; a0 is not free in the chain):
  - Decline-only fits of J23 prefer a0 = 5.4e-11 (95%: 4.0-7.1e-11) with the McM17 shape. This reproduces Coquery & Blanchard's
    direction. On that axis the chain's a0 costs Delta chi^2 = 8.4 (canonical) / 15.1 (alt), i.e. 2.9 / 3.9 sigma. For B2 it is
    5.1 / 10.2.
  - The whole curves pull the other way: best a0 = 1.15-1.51e-10.
  - E19's and Z23's declining parts agree with the chain's a0.
  - Read together, this is a shape tension, not an a0 measurement.
- **Required mass against censuses.**
  - Whole-curve fits give M_* = 7.1-8.7e10 across all shapes and footings, or M_b = M_* + 1.0-1.2e10 gas.
  - Decline-only fits give 7.6-9.9e10.
  - The censuses: McMillan 5.43 +- 0.57, Cautun 5.04 (+0.43/-0.52), Licquia & Newman 6.08 +- 1.14, Bland-Hawthorn & Gerhard 5 +- 1
    (all 1e10).
  - The correlated-systematics variant lowers E19's need to 6.4e10 (chi^2 53/37), because a 2.5% normalisation shift is allowed.
- **LambdaCDM control** (census baryons plus an uncontracted NFW):
  - With M200 and c free, every curve fits: best chi^2/N = 0.11-0.89, M200 = 4.9-9.5e11, c = 14-23.
  - That is +1.9 to +3.8 sigma above the Dutton & Maccio 2014 c(M) relation.
  - With c fixed on c(M), chi^2 = 37-674, which fails.
  - So both frameworks need something atypical: MOND-type laws need extra stellar mass, and NFW needs a very concentrated halo.
- **Beyond 30 kpc** (Bird+2022): at the fitted masses the law gives M(<52 kpc) within 0.0 to +0.5 sigma and M(<73 kpc) at +1.3 to
  +2.2 sigma (the high end includes Cautun's CGM). The best shape is within 1.44 sigma (H8).
- **Filters and M31.**
  - xi = 0.03 pc: < 3e-10. A direct solve at xi = 100 pc gives 6e-4.
  - The H_Y band-pass (L = 1.690 Mpc): <= 6.4e-5 at 5-30 kpc and 7.6e-4 at 100 kpc. H_S (2.879 Mpc): <= 2.3e-5.
  - M31's band-passed Newtonian field survives at the Milky Way at 97.5%, and its phantom at 94.3%. Across the inner Galaxy it is
    nearly uniform, though, so its effect on v_c at 5-30 kpc on the data's azimuths is <= 2.7e-4, and <= 0.6% in g at 100 kpc.
  - The LMC (static, 3.2e9 Msun of baryons) would add up to 0.3% in v_c at 30 kpc on the Sun side. That is reported, not applied.

## Controls and MUTATE

- **K1.** The record's committed Milky Way AQUAL numbers are reproduced exactly by its own code:
  - McMillan 2017: v_c(R0) 191.9 / 196.1 / 197.6, Sigma_dyn 71.4 / 74.8 / 76.0, Newton 177.0, simple 222.7 / 96.5.
  - The refit cell: 198.6 km/s, 75.2, slope -1.14.
- **K2.** FP7's Plummer control is reproduced to 0.0 relative.
- **K3.** Pure Newton: the grid matches the independent semi-analytic curves (Hankel transform and homoeoid integral) to <= 4.8e-4 for
  all six models, and v_N(8.21) = 176.75 km/s.
- **K4.** A finer grid changes the curves by 2.3e-4, and the f_* spline differs from direct solves by 1.7e-7.
- **K5.** The MW-centred interaction field matches FP11's dg_body to 1.3e-4.
- **MUTATE** (a0 -> 0: the scalar's force vanishes and the law is Newton on baryons). T1 fails, because the R >= 15 kpc points need
  M_* = 1.53-1.63e11, about 2.8-3.0x McMillan. rc = 1.

## Pre-declared hypotheses, as they fell

The hypotheses block has sha256 `fbfaf762...` and was unchanged through every edit.

| hypothesis | result | detail |
|---|---|---|
| H1 | holds | |
| H2 | holds | canonical 7.75-8.21e10, alt 7.31-7.73e10; +4.0 to +4.9 sigma over McMillan; +1.1 to +1.5 sigma over Licquia & Newman |
| H3 | FAILS | Its first half holds. The outer-slope tension is smaller than predicted (O24 +0.9 / +1.0 sigma, not 1.5-2.5). |
| H4 | holds | |
| H5 | holds | |
| H6 | holds | |
| H7 | holds | |
| H8 | holds | |

- **Verdict** (by the pre-declared rules):
  - Decline: REPRODUCES THE DECLINE.
  - Baryon budget: CONSISTENT by the rule, which only requires being within 2 sigma of Licquia & Newman. It is in tension with the
    structural censuses, and this should be quoted alongside.

## Disclosures

- **Exploratory runs** (scratch, before the hypotheses were written):
  - timing of the record's McMillan script;
  - FP7's solver on the McM17 census baryons at three grids (one census curve seen; this informed H1);
  - a Kacanov iteration-cap test (260 / 600 / 1500 iterations agree to 1e-3 km/s);
  - FP11's M31 fields (informed H5);
  - semi-analytic Newton against the grid.
- **After the hypotheses were frozen:**
  - One out-of-tree debug run of the full script, with outputs kept in scratch.
  - Edits that followed were reporting only:
    - F1's pre-run reading had claimed a per-cent effect at xi = 100 pc; the solve gives 6e-4, and the reading is now computed from
      the numbers;
    - a predicted-versus-measured table;
    - stat-only chi^2;
    - decline-only (R >= 13 kpc) fits.
  - The first in-tree MUTATE run crashed. The Delta chi^2 = 1 interval was narrower than the fit grid's step, and it is now
    root-found. Central values were unchanged: the fit tables match the debug run apart from the intervals.
  - The final MUTATE and main runs were made with the final code, MUTATE first.
- **Approximations.** The systematic envelopes for E19, O24 and Z23 are by-eye readings and approximate. The following are not
  modelled: the bar, spiral arms, the warp, LMC disequilibrium, and NFW contraction. The scan uses FP7's 260-iteration cap (curl
  residual <= 1.1e-4).

## Files

- `real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve.py`
- `real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve.out`
- `real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve_results.json`
- `real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve_MUTATE.out`
- `real_research/cross_thread_review_2026_09_26/XR29_mw_outer_curve_results_MUTATE.json`
- `real_research/cross_thread_review_2026_09_26/XR29_README.md`

## Sources

- Eilers+2019, ApJ 871, 120.
- Zhou+2023, ApJ 946, 73 (arXiv:2212.10393).
- Jiao+2023, A&A 678, A208 (arXiv:2309.00048).
- Ou+2024, MNRAS 528, 693 (arXiv:2303.12838).
- Bird+2022, MNRAS 516, 731.
- McMillan 2017, MNRAS 465, 76.
- Cautun+2020, MNRAS 494, 4291 (arXiv:1911.04557).
- de Salas+2019, JCAP 10, 037.
- Licquia & Newman 2015, ApJ 806, 96.
- Bland-Hawthorn & Gerhard 2016, ARA&A 54, 529.
- Coquery & Blanchard 2025, A&A 703, A88 (arXiv:2407.18846).
- Koop+2024, A&A 692, A50.
- Melchiorri & Ruchika 2026 (arXiv:2608.10189).
- Dutton & Maccio 2014, MNRAS 441, 3359.
