# CFG433 FROZEN CRITERIA — the T13 phantom dispersion vs Milky Way satellites (spherical Jeans, beta from 3D motions)

Frozen 2026-10-07, before any number below was computed. The data table has been parsed by eye
only for its column layout (it was opened to find the columns); no statistic has been computed.

## Question

T13 (deepseek_push/openai_math_cross_analysis_2026-10/t13_phantom_sound_speed/) derives that the
settled deep-MOND phantom is a singular isothermal sphere with sigma_ph^2 = V^2/2, V^4 = G M_b a0:
the halo's dynamics are set by the baryons alone. Its registered falsifier #2 says MW satellites
"probe 110-125 km/s vs 132.8/139.2" (T13 used M_b = 1e11 Msun, which is not the record's MW value).
The naive comparison ignores anisotropy and the tracer profile. Here: does a proper spherical Jeans
analysis of the MW satellite population, with anisotropy measured from their own 3D motions and
tracer density from the satellites themselves, recover the circular speed the kernel predicts from
MW baryons alone? No fitting of the law, no free constant.

## Data (fixed)

Fritz et al. 2018, A&A 619, A103 (arXiv:1805.00908), Table 2: d_GC, V_rad +- err, V_tan (+err/-err)
for 39 objects (Galactocentric frame of the paper: R0 = 8.2 kpc, solar velocity (11, 248, 7.3) km/s).
Fetched from the arXiv source (CDS has no catalogue); see ../_external_data/cfg433_work/FETCH_LOG.md.
The tangential error is taken as e_t = (err_plus + err_minus)/2.

## Prediction (fixed, no fit)

V_pred(r)^2 = r * g_N(r) * nu(g_N/a0), nu(y) = 1/(1 - exp(-sqrt(y))), g_N = G M_b / r^2 (point mass;
at r >= 30 kpc the disc + bulge is enclosed to < 1 %).
- M_b PRIMARY = 6.0e10 Msun (the record's MW baryon mass: FG001 / CFG42 / CFG286 MW_MB).
- M_b variant = 7.3e10 Msun (the record's census-high value, CFG286 MW_MB_CENSUS_HI).
- Reported for reference only: T13's 1.0e11.
- Both footings, never pooled: a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2.
- Compared at the median Galactocentric radius of the selected sample; the range of V_pred over
  the sample's radii is reported.
- T13's sigma_ph = V/sqrt2 is the isotropic dispersion of r^-2 tracers; the decisive quantity is V_c,
  and the isotropic-equivalent sigma = V_c,obs/sqrt2 is reported alongside.

## Estimator (fixed)

Spherical Jeans equation for a tracer n ~ r^-gamma with constant second moments in a scale-free
flat (logarithmic) potential (alpha = 0 member of the Watkins, Evans & An 2010 3D tracer estimator):

    V_c^2 = <v_t^2> + (gamma - 2) <v_r^2>  ==  (gamma - 2 beta) <v_r^2>,   beta = 1 - <v_t^2>/(2 <v_r^2>)

- <v_r^2> = mean(V_rad^2 - e_r^2), <v_t^2> = mean(V_tan^2 - e_t^2) (unweighted, error-deconvolved
  second moments; streaming motion included, as the Jeans equation requires second moments).
- gamma: maximum-likelihood power-law index of the satellites' own radial distribution, truncated
  to the selected radial window [r_lo, r_hi] (all selected objects, before the quality cut).
- beta is not free: it is measured from the same 3D motions.
- Uncertainty sigma_stat: bootstrap over satellites (10000 resamples, seed 433), gamma re-estimated
  in each resample; sigma_stat = half the 16-84 % width of V_c,obs.

## Sample (fixed)

PRIMARY: 30 <= d_GC <= 300 kpc (drops Sgr, Hyi I, Tuc III, Seg 1 inside; Eri II, Phx I beyond) AND
quality cut e_t <= 50 km/s (without it, objects with e_t ~ 200-500 km/s make v_t^2 - e_t^2 pure noise).

Declared variants (the systematic envelope; each re-run with its own gamma and bootstrap):
- V1 no quality cut (30-300 kpc, all)
- V2 quality cut e_t <= 100 km/s
- V3 exclude LMC-candidate satellites {CarII, CarIII, HorI, HyiI, RetII, TucII}
- V4 exclude Leo I (possibly unbound)
- V5 inner half (30-100 kpc)  ; V6 outer (100-300 kpc)
- V7 gamma fixed = 2.0 ; V8 gamma fixed = 3.0 (bracket for satellite-census incompleteness)
- V9 M_b = 7.3e10 (prediction variant; same V_c,obs as primary)

## Decision rule (per footing; primary sample, primary M_b)

D = (V_c,obs - V_pred(r_med)) / sigma_stat.
- PASS:      |D| <= 2
- TENSION:   2 < |D| <= 3, or |D| > 3 but at least one of V1-V9 has |D| <= 2
- FAIL:      |D| > 3 AND every variant V1-V9 has |D| > 2 with the same sign
- NON-DIAGNOSTIC: if the MUTATE power checks (below) do not flip, whatever D is.
Direction is part of the verdict: D > 0 (more dynamical mass than baryons-alone phantom) fails the
"phantom alone sets the halo" statement of T13 but leaves room for the cold fluid of B (CFG344:
dark mass that clumps like CDM); D < 0 is a fail that cold mass cannot repair (cold mass only adds).

## Controls (all must pass for the verdict to stand)

- C1 table parse: 39 rows; |V_3D^2 - (V_rad^2 + V_tan^2)| <= (2 * combined error) for >= 37 of 39.
- C2 mock recovery: 300 mocks at the primary sample's size, radii drawn from the fitted power law
  within the window, velocities Gaussian with the Jeans solution of the EXACT kernel potential
  (M_b primary, canonical footing) for beta = beta_obs (primary), each object's real errors added.
  The estimator's mean recovered V_c must lie within 3 % of the mean true V_c over the radii, and
  the bootstrap sigma_stat must cover the truth in 50-85 % of mocks at 1 sigma.
- C3 predicted curve sanity: V_pred(r) varies by < 10 % across 30-300 kpc (the flat-potential
  estimator is appropriate); V_pred(deep limit) -> (G M_b a0)^(1/4) within the kernel's next order.

## MUTATE (deliberately broken; written to a separate output, *_MUTATE.out)

- M1 planted mock: the C2 mock with the true potential's V_c multiplied by 1.35 must return FAIL
  (D > 3) in >= 80 % of 100 mocks, and the unmodified mock must return PASS in >= 80 %.
- M2 real data, all velocities and errors scaled x1.35, and separately x(1/1.35): at least one of
  the two must give a verdict category different from the main run in each footing; if neither
  flips, the test is NON-DIAGNOSTIC.
- M3 anisotropy-blind (the naive comparison the brief warns against): beta forced to 0 by using
  V_c^2 = gamma * <v_3D^2>/3. Reported as the naive number; it must differ from the primary V_c,obs
  by more than 1 sigma_stat if anisotropy matters (informational; not a verdict input).

## What this is NOT

Not a test of the mass law v^4 = G M a0 on galaxies (that is SPARC), not a cold-fluid measurement,
not a fit of a0 or kappa (kappa = 1/2 stays FITTED). A satellite population is a sparse,
incompleteness-biased tracer; the gamma bracket (V7/V8) is the declared handle on that.
