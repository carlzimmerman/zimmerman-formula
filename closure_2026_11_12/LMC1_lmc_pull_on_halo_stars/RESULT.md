# LMC1 RESULT: the LMC's pull on the DESI DR1 BHB halo stars, in the framework's own Milky Way

> **LEAD'S STATUS NOTE (2026-11-12, after verification).** AS FROZEN THIS LANE EARNS **NO LABEL** on either
> footing: the frozen rule stops the script before any label when a known-answer check fails, and the
> precision check K7 failed in runs 3 and 4; mutation M1 also failed to bite. The words below are the reading
> under Amendment A3, which was written after the q values had been seen and is not blind. What the runs do
> support, and what they do not, is in "Lead's verification and reading" near the end.

2026-11-12. TEST lane. Adopts nothing. Criteria `FROZEN_CRITERIA.md` (sha256 04cba553..., frozen
2026-11-13T00:20:54Z UTC), written before any LMC run and before any star was read in this lane. Three
amendments, each written before the run it governs: A1 (bracket low end 1.6e10, after run 1 stopped at the
bracket check), A2 (K4 reference value corrected, after run 2 stopped at K4; set after the computed value was
seen), A3 (K7 precision failed in run 3; recorded instead of stopping, plus an adverse-noise robustness test;
**not blind**: run 3 had printed the q values). Graded run: run 4 (`lmc1.out`).

## Labels (central M_eff 2.5e10; bracket 1.6e10 / 4e10)

| footing | label | bracket | q noise (A3.2) |
|---|---|---|---|
| census canonical | **LMC NEGLIGIBLE** | robust (1.6e10: NEGLIGIBLE, 4e10: NEGLIGIBLE) | **FRAGILE (q NOISE)**: +2 err_q gives MAKES IT WORSE, -2 err_q gives PART OF IT |
| census alt | **LMC NEGLIGIBLE** | robust | **FRAGILE (q NOISE)**: same |

Graded with two failed checks: **K7 failed** (q errors 0.5 to 2.2 per cent against the frozen 0.5 per cent) and
**mutation M1 failed to bite** (see Checks). Read plainly: the framework's LMC changes the line-of-sight
dispersion in every bin by less than the model's own noise of 0.5 to 2 per cent. It does not explain the hot bin
and does not change RAW1's verdicts. The model cannot resolve an effect below about 1 per cent per bin.

## Numbers

q = sigma(with LMC) / sigma(without), model particles in RAW1's bins inside each bin's footprint
(nside-4 pixels holding a real star: 69, 63, 50, 45 of 192), 150,000 tracers, 2 Gyr twins:

| | 20-30 | 30-40 | 40-55 | 55-80 |
|---|---|---|---|---|
| canonical 1.6e10 | 1.0039 +/- 0.0049 | 0.9930 +/- 0.0088 | 1.0101 +/- 0.0136 | 0.9725 +/- 0.0165 |
| canonical 2.5e10 | 1.0005 +/- 0.0054 | 0.9960 +/- 0.0089 | 1.0156 +/- 0.0162 | 1.0057 +/- 0.0224 |
| canonical 4e10 | 1.0061 +/- 0.0062 | 1.0074 +/- 0.0109 | 1.0332 +/- 0.0178 | 0.9700 +/- 0.0261 |
| alt 2.5e10 | 0.9988 +/- 0.0046 | 0.9918 +/- 0.0095 | 1.0026 +/- 0.0151 | 1.0047 +/- 0.0202 |
| canonical 2.5e10, 3 Gyr (reported) | 1.0040 | 0.9868 | 1.0275 | 0.9907 |
| M1 1.5e11 canonical (BORROWED, context) | 0.9876 | 0.9991 | 1.0206 | 1.0064 |

Every central q is within 1.0 sigma of 1. The model's per-star velocity change at 55-80 kpc is about 9 km/s
(3-D median), mostly orbit-phase scatter; the coherent part (template, below) is 2 to 8 km/s rms.

Excess of 30-40 over its neighbours (all three bins corrected the same way):
E0 = 11.81 km/s, z0 = 2.25 before. After: canonical E1 = 12.98 (E1/E0 1.10), z1 2.40; alt 12.75 (1.08), 2.34.
Bracket: canonical 13.21 / 12.80, alt 11.72 / 12.54. Adverse 2 err_q: 9.1 to 16.8 (canonical), 8.8 to 16.6 (alt).
3 Gyr variant: 14.67 (reported, MAKES IT WORSE under the rule; inside the q noise).
rc footings (reported): rc canonical E1 10.87, rc alt 11.37, both NEGLIGIBLE. Their no-LMC tracers drift
2.1 to 2.3 per cent in the outer bins, so they would not pass K3. Tracer variant (initial beta 0.45): E1 11.56,
NEGLIGIBLE.
Second estimator (model's mean LMC velocity subtracted star by star, RAW1's estimator refit): sigma 97.32,
106.41, 92.86, 95.37 (canonical); E1' = 11.32 (z 2.16), alt 11.43 (2.18). Both NEGLIGIBLE.

RAW1 ratios / q (NOT A RE-GRADE; RAW1's predicted dispersion is not recomputed), central M_eff:

| case | before | after | RAW1's rule would say |
|---|---|---|---|
| census canonical | 1.095, 1.205, 1.052, 1.090 | 1.094, 1.210, 1.036, 1.084 | FAILS HOT (20-30, 30-40), unchanged |
| census alt | 1.052, 1.155, 1.007, 1.043 | 1.053, 1.165, 1.005, 1.038 | FAILS HOT (30-40), unchanged |
| rc canonical | 1.028, 1.135, 0.992, 1.030 | 1.025, 1.128, 1.001, 1.004 | FAILS HOT (30-40), unchanged |
| rc alt | 1.012, 1.114, 0.972, 1.007 | 1.013, 1.108, 0.968, 0.993 | FAILS HOT (30-40), at the edge (1.108 vs 1 + 2 x 0.054) |

Effective-mass bracket (K6, all inside after A1): (i) LMC rotation curve 1.70e10 inside 8.7 kpc; flat curve to
the equal-field radius 13.0 / 11.9 kpc gives 2.54e10 / 2.33e10 (Jacobi variant 3.49e10 / 3.35e10); (ii) kernel
on 3.2e9 of LMC baryons at the Milky Way's field at 49.1 kpc (nu 5.45 / 5.94) gives 1.74e10 / 1.90e10, or
1.64e10 / 1.78e10 at 3.0e9; (iii) momentum with baryonic inertia (3.2e9 / 6.67e10 = 0.048) gives 1.74e10 /
1.89e10. The framework's own routes cluster at 1.6e10 to 1.9e10, the low end of the bracket. This is an
effective-mass bracket. The framework's nonlinear two-body field is not computed.
The LMC's past orbit with no friction: pericentre 47.4 kpc about 46 Myr ago, 234 kpc 2 Gyr ago (canonical
central). It is first passage in practice.

Reported, no label:
- Dipoles (km/s, toward l, b). Real stars: 24.0 (342, +2), 43.2 (56, +39), 26.3 (127, +30), 44.1 (179, +22).
  Model with the LMC, canonical central, full sky: 1.7, 2.4, 3.8, 13.2 (80, +46). In the footprint the model's
  dipoles (5 to 16) are close to the no-LMC twin's (3 to 12), which is pure sampling noise. The real stars'
  dipoles are 2 to 18 times the model's full-sky LMC dipole and point elsewhere.
  Model full-sky 50-80 kpc dipole 11.7 (canonical) / 9.2 (alt) km/s. M1: 20.9 / 13.0. Published reflex
  (PROVISIONAL): 32 +/- 4 km/s toward (56, -34) (Petersen and Penarrubia 2021, 40-120 kpc). The framework's
  LMC gives about a third of it, and the borrowed heavy LMC in this Milky Way about two thirds. Context only.
- Template scale s (v = mu + s T): canonical -0.82 [-2.21, +0.56], +4.39 [+2.22, +6.55], -0.22 [-1.31, +0.87],
  +0.35 [-0.87, +1.57], combined +0.25 +/- 0.67. Alt combined +1.01 +/- 0.67. The 30-40 bin prefers about 4.4
  in both footings, the same bin as HOT1's dipole. Power: formally 6 - 1 > 2 sigma_s, and the central template
  beats the M1 template by Delta(-2 ln L) = 23.7 / 25.6. **This is not claimed**: the template is built from
  noisy shell fits (its rms of 2 to 8 km/s is comparable to the twins' sampling noise), so the stars' power to
  tell a 2.5e10 LMC from a 1.5e11 one is not established by this lane.

## Checks

Passed: K6 bracket (after A1); K1 integrator (circular orbit at 30 kpc dE/E 3.9e-10, radius 4.1e-5;
eccentric orbit 4.4e-5; LMC-track integrator 1.7e-8); K4 LMC today (r_GC 49.08 kpc against 49.7 [A2], each
component within 0.18 kpc of the scaled K13 position; speed 320.1 (321 +/- 24), v_rad 68.2 (64 +/- 7), v_tan
312.7 (314 +/- 24)); K5 sample (counts 865 / 264 / 241 / 125; dispersions 97.244, 106.739, 92.617, 95.301; E0
11.809, z0 2.247); K3 stationarity on both labelled footings (trend drift +0.1 to +1.7 per cent, alpha 4.98 /
4.96, beta 0.61 to 0.77); K2 zero-mass twin bitwise equal to the no-LMC run; M2 bites (z component of the
50-80 kpc dipole +7.99 -> -4.21).

**Failed:**
- K6 in run 1 (route ii at 3.0e9 below the frozen floor; A1).
- K4 in run 2 (frozen reference 50.1 kpc was a heliocentric distance; A2, set after seeing 49.08).
- **K7 in runs 3 and 4**: q errors 0.0054, 0.0089, 0.0162, 0.0224 (canonical) and 0.0046, 0.0095, 0.0151, 0.0202
  (alt) against 0.005. The design study's paired-noise estimate was wrong: the LMC changes bin and footprint
  membership, so the twins are nearly independent samples. Meeting 0.5 per cent needs about 3 million tracers.
- **M1 did not bite**: the 50-80 kpc full-sky dipole is 1.78 (canonical) and 1.42 (alt) times the central
  case's, against the frozen >= 3. Two causes may combine: the dipoles carry about 3 km/s of sampling noise, and
  the heavy LMC's own orbit differs (r 141 kpc 2 Gyr ago, against 234). The mutation therefore does not show
  that the machinery responds in proportion to mass. The size of the framework LMC's effect rests on the
  central numbers alone.

Reproducibility: every random step is seeded (tracers 11, bootstrap 21; design seeds 11, 12, 13) and output
files carry no times. A byte-for-byte re-run was **not done** (compute budget; run 4 took about 6.5 minutes).
The q values for the labelled footings agree to all printed digits between runs 3 and 4, which is a partial
reproducibility check.

## Lead's verification and reading (2026-11-12, after the result; not graded; no label changes)

Verification: `FROZEN_CRITERIA.md` and `lmc1_core.py` match the hashes in `FREEZE_STAMP.txt`, as do the three
amendments; the lead read the model module (the relative orbit, the star's acceleration as Milky Way field
plus LMC pull minus the centre's acceleration, and the observation are coded as stated); the lead re-ran
`lmc1.py` (402 s, one thread) and `lmc1.out`, `lmc1_results.json` and `lmc1_mut.out` came back equal byte
for byte. That closes the "re-run not done" item above. `lmc1_lead_check.py` / `.out` hold the numbers below
(they read `lmc1_results.json`; no simulation).

1. **As frozen: NO LABEL.** K7 failed and A3 changed a stop into a recorded failure after the outcome was
   visible. A1 and A2 corrected reference values before any tracer run and are sound, though A2 is not blind.
2. **What the runs support.** The model's noise alone puts E1 at 12.98 +/- 1.23 km/s (canonical) and
   12.75 +/- 1.26 (alt). LMC EXPLAINS THE BIN is 6.2 / 5.8 model-noise sigma away and LMC PART OF IT 2.9 / 2.6;
   LMC MAKES IT WORSE is 1.0 / 1.1 sigma away, so the runs cannot separate NEGLIGIBLE from MAKES IT WORSE. In
   the 30-40 bin itself the LMC's change of the dispersion lies between -1.4 and +2.4 km/s (canonical,
   two sigma), against an excess of 11.8.
3. **A ceiling that needs no model.** A pure dipole of amplitude A adds A^2 / 3 to a bin's variance. Taking the
   whole published reflex (32 km/s, PROVISIONAL, measured beyond 40 kpc) out of all three bins lowers each by
   1.6 to 1.9 km/s and leaves the excess at 12.0. A dipole would have to be 85 km/s to carry the excess.
4. **The model is not validated against the measured reflex.** Its dipole has the published vertical sign
   (northern stars receding), and M2 and the zero-mass twin behave. But its apex lies about 100 degrees from
   the published one at every mass (toward the LMC's present position, not an earlier point on its path), and
   the amplitude grows far more slowly than the mass (ratio 1.78 / 1.42 for a mass ratio of 6). With the
   borrowed heavy LMC it gives 21 / 13 km/s against the published 32 +/- 4. Points 2 and the dipoles above are
   therefore the statements of a crude rigid model; point 3 does not depend on it.
5. **Not graded here, and open:** the framework's LMC is light (routes ii and iii give 1.6 to 1.9e10; the
   bracket tops out at 4e10) and gives 9 to 14 km/s of reflex in this model, where the published measurement
   is 32 +/- 4. This lane cannot grade that (point 4). It is a candidate test of the framework, not a result.

RAW1's labels are not changed by this lane.

## Limits

An effective-mass bracket in place of a two-body field solution. Rigid bodies, no deformation of either galaxy,
no dynamical friction, no SMC. A spherical, static Milky Way. One past orbit. The tracers are a model (Gaussian
Jeans start relaxed 5 Gyr, alpha about 5.0, beta 0.61 to 0.77), not the real halo (RAW1: beta 0.44 at 40-55).
The model's noise floor is 0.5 to 2 per cent in q, which is larger than the frozen precision. The template is first order in
direction per 2.5 kpc shell and noisy. The footprint uses Galactocentric axes (0.15 deg from Galactic). Only 264 stars
in the test bin. Published LMC inputs are PROVISIONAL where marked in the criteria (centre, line-of-sight
velocity, rotation curve, baryon mass, K13 position). The Plummer softening (5 kpc) is a choice. Total compute
used is about 12 minutes (design about 1.2 min, runs 1-4, and two post hoc noise diagnostics of about
1.5 min in the scratch area). That is over the 10-minute guide.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt` (criteria, model module and amendment hashes), `AMENDMENT_A1.md`,
`AMENDMENT_A2.md`, `AMENDMENT_A3.md`, `lmc1_core.py` (field, tracers, integrator, observation; copies from
raw1_model.py and hot1.py), `lmc1_design.py` with `lmc1_design_N150k_aout5.5_beta0.6.out` and
`lmc1_design_N150k_aout5.5_beta0.45.out` (pre-freeze synthetic design study; the script writes
`lmc1_design.out`, renamed by hand), `lmc1.py`, `lmc1.out` (graded run 4), `lmc1_results.json`, `lmc1_mut.out`,
`lmc1_run1_K6_FAIL.out`, `lmc1_run2_K4_FAIL.out`, `lmc1_run3_K7_FAIL.out`; the lead's `lmc1_lead_check.py`,
`lmc1_lead_check.out`.
Data: https://data.desi.lbl.gov/public/dr1/vac/dr1/mws-bhb/v1.0/MWS_BHB.fits, sha256
5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246, 8,591,040 bytes, not in the repository.
Run: `nice -n 10 python3 -I -B lmc1.py <MWS_BHB.fits>` (about 6.5 minutes, one thread).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
