# LMC1 FROZEN CRITERIA: the LMC's pull on the DESI DR1 BHB halo stars

2026-11-12. TEST lane. Adopts nothing. Written before any LMC simulation was run and before any star of the
catalogue was read in this lane. Never edited after the stamp (`FREEZE_STAMP.txt`); changes go in dated
amendments written before the run they govern.

## 1. Question

How much of RAW1's hot 30-40 kpc bin (sigma_los 106.74 km/s against 97.24 and 92.62 in the neighbours; excess
E0 = 11.81 km/s, z = 2.25), and of RAW1's observed / predicted ratios in all four bins, is the Large Magellanic
Cloud's doing? Model the LMC's pull on the Milky Way's centre and on halo tracers in the framework's own
Milky Way field, and re-measure the dispersions with that pull removed.

## 2. Known beforehand, and hand expectations (disclosed)

- Known: RAW1's numbers (counts 865 / 264 / 241 / 125; sigma_los 97.24, 106.74, 92.62, 95.30 km/s; ratios in
  RAW1 `RESULT.md`); HOT1's post hoc: a marginal dipole in the 30-40 bin (43 km/s toward l 56, b +39,
  p 0.048), dipoles 24 and 26 km/s in the 20-30 and 40-55 bins; removing each bin's own dipole takes the excess
  from 11.8 to 10.1 km/s (z 1.95). RAW1's 55-80 bin mean is -21.6 km/s. These were seen in the session context
  before this file was written. The positions of the stars have not been looked at in this lane.
- Published (PROVISIONAL look-ups): reflex ("travel") velocity of the disc relative to the outer halo
  (40-120 kpc) 32 +/- 4 km/s toward (l, b) = (56 +/- 9, -34 +10/-9) deg (Petersen & Penarrubia 2021, Nature
  Astronomy 5, 251; arXiv 2011.10581 abstract, fetched 2026-11-12); Erkal et al. 2021 also detect the
  sloshing (amplitude as recorded in the repository's hunt_2026/h81 notes, about 40 +/- 8 km/s; PROVISIONAL,
  not re-checked).
- Lead's hand expectation: a pure dipole of amplitude A adds about A^2 / 3 to the line-of-sight variance, so
  lifting 95 km/s by 11.8 km/s needs A near 85 km/s, far above any published reflex; the framework's LMC is
  several times lighter than the standard model's. Expected word: LMC NEGLIGIBLE.
- This lane's own hand expectation: the MW centre's acceleration toward an M_eff = 2.5e10 LMC at 50 kpc is
  about G M / D^2 = 43 (km/s)^2 / kpc, i.e. about 44 km/s per Gyr, acting strongly only for the last few
  hundred Myr near pericentre, so a reflex of order 10 km/s at 50-80 kpc and less inside (inner tracers move
  with the centre). The variance change is then a few tens of (km/s)^2 at most, a shift of q of a few
  tenths of a per cent at 55-80 and less inside. Expected: LMC NEGLIGIBLE on both footings, robust across
  the bracket; M1 (1.5e11) several times larger in dipole but still far short of 11.8 km/s in the 30-40 bin.
- Design study (disclosed; purely synthetic, before the freeze; `lmc1_design.py`, outputs
  `lmc1_design_N150k_aout5.5_beta0.6.out`, `lmc1_design_N150k_aout5.5_beta0.45.out`): MW field alone (census
  canonical), no LMC run, no star. Fixed N = 150,000, dt = 2 Myr, relaxation 5 Gyr. Relaxed tracers: alpha
  (20-80) 4.98, beta 0.61 / 0.68 / 0.72 / 0.77 by bin (initial beta 0.6), endpoint dispersion changes over
  the last 2 Gyr +0.7, +1.9, +1.8, -1.3 per cent (noise dominated; hence the trend estimator in K3), and a
  stand-in ratio error of 0.12 to 0.36 per cent for one third of the sky under a synthetic 30 km/s offset.

## 3. Inherited ingredients and their class

| ingredient | value | class |
|---|---|---|
| DESI DR1 BHB stars (velocities, distances, positions) | MWS_BHB.fits, sha256 5669c821...5246 | raw measurement |
| RAW1 sample cuts S1-S6 and solar frame (R0 8.122, z_sun 20.8 pc, v_sun (12.9, 245.6, 7.78)) | copied from raw1.py | raw measurement (GRAVITY, Sgr A* proper motion) |
| MW baryon census (McMillan 2017 discs + bulge), stellar mass 5.49e10; rc stellar masses 7.08e10 / 6.42e10 | raw1_model.py | raw-derived compilation (as in RAW1) |
| kernel nu(y) = 1 / (1 - exp(-sqrt(y))), a0 9.36e-11 / 1.13e-10, g = nu(g_b / a0) g_b, no external field | raw1_model.py | framework's own |
| LMC centre (RA, Dec) = (78.76, -69.19) deg | van der Marel & Kallivayalil 2014 / Kallivayalil 2013 | raw (PROVISIONAL, from memory) |
| LMC distance 49.59 +/- 0.54 kpc | Pietrzynski et al. 2019 | raw |
| LMC proper motion mu_W = -1.910 +/- 0.020, mu_N = 0.229 +/- 0.047 mas/yr | Kallivayalil et al. 2013 (abstract fetched) | raw |
| LMC line-of-sight velocity 262.2 +/- 3.4 km/s | van der Marel et al. 2002 | raw (PROVISIONAL, from memory) |
| published Galactocentric LMC: speed 321 +/- 24 km/s (fetched), v_rad +64 +/- 7, v_tan 314 +/- 24, r_GC about 50.1 | Kallivayalil 2013 | raw-derived (check K4 only) |
| LMC rotation curve 91.7 +/- 18.8 km/s at 8.7 kpc, flat | van der Marel & Kallivayalil 2014 (secondary sources, web) | raw (PROVISIONAL) |
| LMC baryons: stars 2.7e9 + gas about 5e8 (x 1.33 helium) = 3.2e9 | repository hunt_2026/h37 notes | raw-derived (PROVISIONAL) |
| rigid-body treatment, linear superposition of the LMC's pull on the framework's field, Plummer body | standard practice | BORROWED (Newtonian / standard-model method); the framework has no two-body field equation |
| Plummer softening 5 kpc (puts 1.63e10 inside 8.7 kpc for 2.5e10) | this lane's choice | choice |
| Jacobi tidal radius r_t = D V_LMC / (sqrt(2) V_MW) for two flat curves | Newtonian tidal theory | BORROWED (route i upper end, variant only) |
| Gaussian Jeans initial conditions, leapfrog | standard numerical method | borrowed method (no physics content) |
| M1 LMC mass 1.5e11 | standard-model literature | BORROWED, CONTEXT ONLY, no label |
| published reflex 32 +/- 4 km/s, (56, -34) | Petersen & Penarrubia 2021 (their analysis assumes a standard halo model) | context only |

No standard-model halo and no standard-MOND interpolation or external-field prescription enters any label.

## 4. Model

- Milky Way: the framework's spherical field g(r) = nu(g_b / a0) g_b from the census, tabulated on a log grid
  0.5 to 2e4 kpc (inside 0.5 kpc a harmonic core g(0.5) r / 0.5). Static in its own frame. Labelled cases:
  census canonical, census alt. Reported: rotation-curve stellar mass canonical and alt (central mass only).
- The LMC is a rigid Plummer body of mass M_eff (softening 5 kpc) at d(t) relative to the MW centre.
  Bracket M_eff = 1.7e10, 2.5e10 (central), 4e10 Msun. This is an EFFECTIVE-MASS BRACKET, NOT A FIELD
  SOLUTION; the nonlinear two-body field of the framework is not computed.
- LMC orbit: today's position and velocity from section 3 converted with astropy to RAW1's Galactocentric frame;
  integrated backward 3 Gyr (2 Gyr runs use the last 2 Gyr of it) with d'' = -g(|d|) d_hat - a_MW, where the
  MW centre's acceleration a_MW = G M_eff d / (|d|^2 + eps^2)^(3/2). Leapfrog, step 0.1 Myr, stored every 2 Myr.
  No dynamical friction (flagged), no SMC, no deformation of either body.
- Tracers (test particles, MW-centred frame): acceleration = -g(r) r_hat + LMC pull - a_MW.
- Tracer population: N = 150,000, seed 11; density n proportional to r^-2 inside 20 kpc and r^-5.5 outside,
  2 to 400 kpc; constant beta 0.6; Gaussian velocities with the Jeans sigma_r of that density in that
  footing's field. Relaxed in the MW field alone from t = -5 Gyr with dt = 2 Myr; states kept at -3 and -2 Gyr.
- Twins: from the relaxed state at -2 Gyr (variant: -3 Gyr), one run with the LMC and one without (the
  relaxation run itself, continued). Every difference is the LMC's.
- Observation: Galactocentric r of each particle, unit vector n from the Sun (Sun at RAW1's Galactocentric
  position from astropy), v_gsr = v . n relative to the MW centre; |v_gsr| <= 400 km/s (RAW1's clip); RAW1's
  four bins. Footprint per bin: the HEALPix nside-4 RING pixels (in Galactocentric-axis longitude and latitude
  as seen from the Sun; the 0.15 deg tilt from Galactic axes is ignored) that contain at least one real star
  of that bin. Pixel routine copied from hot1.py.

## 5. Estimators

- Primary: q_bin = std(v_gsr with LMC) / std(v_gsr without), model particles in bin and footprint; error from
  300 Poisson bootstrap weightings of the particles (seed 21), the same weights applied to both twins.
  Corrected dispersion of the real stars sigma_c = sigma_obs / q; its half-width h_c = h_obs / q (+) sigma_c
  err_q / q in quadrature, h_obs = half the 68 per cent interval of RAW1's estimator.
- E = sigma_c(30-40) - (sigma_c(20-30) + sigma_c(40-55)) / 2; z = E / sqrt(h2^2 + (h1^2 + h3^2) / 4).
  E0, z0 from the uncorrected stars (must be 11.81, 2.25); E1, z1 after.
- Second (reported): the model's mean LMC-induced velocity field. In radial shells 2.5 kpc wide (centres 18.75
  to 81.25 kpc), fit the 3-D velocities of all particles (full sky) as v = a + B r_hat (12 parameters) in each
  twin; Delta(r, r_hat) = fit_with - fit_without, linear in r between shell centres. Template at each real star
  T_i = Delta . n_i. Subtract T_i from v_gsr and refit RAW1's estimator (fit_disp, copied); E1', z1'.
- RAW1 ratios: f / q and s_f / q for the four cases and bins (rc cases use their own q), graded with RAW1's
  rule (|f - 1| <= 2 s in every bin, else FAILS HOT / COLD); stated as NOT A RE-GRADE (RAW1's predicted
  dispersion is not recomputed).
- Reported, no label: dipole v_gsr = m + d . n (least squares, as in hot1_posthoc.py) of the model "with" twin
  per bin, in footprint and full sky, and of the real stars per bin; amplitude and (l, b).
  Template scale factor per bin: v_i = mu + s T_i with variance sigma^2 + e_i^2, s by profile likelihood
  (68 per cent interval); combined over bins by inverse variance. Power statement: the stars can tell the
  framework's LMC from one six times heavier only if |6 - 1| > 2 sigma_s (combined) and the M1 template's
  likelihood differs from the central one's by Delta(-2 ln L) > 4; both are reported.

## 6. Labels (per labelled footing, at the central M_eff; FRAGILE if 1.7e10 or 4e10 gives a different word)

Evaluated in this order:
- LMC EXPLAINS THE BIN: z1 < 1.0.
- LMC PART OF IT: E1 <= 0.8 E0 and z1 >= 1.0.
- LMC NEGLIGIBLE: 0.8 E0 < E1 < 1.2 E0.
- LMC MAKES IT WORSE: E1 >= 1.2 E0.
The 3 Gyr variant, the rc cases and the tracer variant (initial beta 0.45, canonical, central) are reported
beside the label and do not change it.

## 7. Known-answer checks (the script stops before any label if one fails)

- K1 integrator, static census-canonical field, dt 2 Myr, 5 Gyr: circular orbit at 30 kpc: max |dE / E| < 1e-4
  and max |r / 30 - 1| < 1e-3; eccentric orbit (start 60 kpc, tangential speed 0.4 v_c): max |dE / E| < 1e-4.
  LMC-track integrator (0.1 Myr) with M = 0 over 3 Gyr: max |dE / E| < 1e-4.
- K2 a twin with M_eff = 0 on the LMC code path gives exactly the no-LMC state (bitwise equal arrays), canonical.
- K3 stationarity without the LMC (each labelled footing; also the reported footings, reported only): nine
  snapshots every 250 Myr over the final 2 Gyr; per bin (full sky) the least-squares linear trend times 2 Gyr,
  divided by the mean dispersion, |drift| < 0.02; density slope alpha (20-80, ML power law) at t = 0 in
  [4.5, 5.5]; beta at t = 0 in [0.5, 0.85] for 20-30 and 30-40 and in [0.35, 0.85] for 40-55 and 55-80.
- K4 LMC today: |r_GC - 50.1| <= 1.0 kpc; |v - 321| <= 24; |v_rad - 64| <= 7; |v_tan - 314| <= 24 km/s.
- K5 sample: real stars reproduce RAW1's counts (865 / 264 / 241 / 125) exactly and dispersions within
  0.05 km/s; E0 = 11.81 +/- 0.01 and z0 = 2.25 +/- 0.01.
- K6 bracket (before any simulation): (i) V^2 r / G at 91.7 km/s, 8.7 kpc; upper end: flat curve continued
  to where the LMC's own field V^2 / r equals the MW's framework field at the LMC's distance (variant: Jacobi
  radius, reported); (ii) nu(g_b,MW(r_LMC) / a0) x 3.2e9 (variant 3.0e9), each footing; (iii)
  (3.2e9 / M_b,MW,total) x g_MW(r_LMC) r_LMC^2 / G, each footing. Every number must lie in
  [1.7e10 x 0.99, 4e10 x 1.01]; if any does not, stop and write an amendment.
- K7 q error: err_q < 0.005 in every bin, every labelled footing, central mass.

## 8. Mutations (separate output `lmc1_mut.out`)

- M1 (the only borrowed number): M_eff = 1.5e11 (own orbit), census canonical and alt. Bites if the full-sky
  dipole amplitude of the model's 50-80 kpc particles (with twin) is >= 3 times the central case's. Report q,
  sigma_c, E, z and RAW1 ratios / q per bin as CONTEXT, flagged BORROWED, no label; the published reflex beside.
- M2: LMC position and velocity mirrored through the Galactic plane (z, v_z -> -z, -v_z), canonical, central.
  Bites if the z component of the full-sky 50-80 kpc model dipole changes sign relative to the central run.

## 9. Seeds, compute, reproducibility

Tracers seed 11 (variant seed 11 with beta 0.45), bootstrap seed 21. One thread, nice 10, about 6 minutes.
No timestamps or run times in output files. The data path is a command-line argument and is never written.

## 10. Limits to state

Effective-mass bracket in place of a two-body field solution; rigid bodies, no deformation, no dynamical
friction, no SMC; spherical static Milky Way; one past orbit; the tracer population is a model, not the real
halo (its beta and slope are near, not equal to, RAW1's); the template is first order in direction per shell;
264 stars in the test bin.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
