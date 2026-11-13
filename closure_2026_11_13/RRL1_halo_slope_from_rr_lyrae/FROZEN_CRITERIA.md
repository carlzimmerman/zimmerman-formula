# RRL1 FROZEN CRITERIA: the stellar halo's density slope from RR Lyrae, and RAW1's test redone with it

2026-11-13. TEST lane. Adopts nothing, relabels nothing (RAW1, MWT1, MWT2 keep their labels), registers nothing.
Written and committed alone, before any script of this lane and before any number was computed from the RR Lyrae
tables. What had been seen of the data at freeze time: the two tables' header, units and column-description lines,
their MANIFEST.txt files and three data rows of each (printed with the headers). Nothing else.

## 0. The question

RAW1 (`closure_2026_11_12/RAW1_halo_stars_direct/`) read FAILS HOT at 30-40 kpc for the framework's Milky Way line
on DESI DR1 blue horizontal branch (BHB) stars. MWT1 (`closure_2026_11_13/MWT1_hot_bin_assumptions/RESULT.md`)
showed that the fail depends on the tracer density slope, which the BHB sample cannot settle (single 5.29; own
two-slope at break 30: outer 4.33 +/- 0.48, p about 0.04). MWT2 found an ungraded cold lump of about 31 stars in
that bin. RRL1 measures the stellar halo's number-density slope from 20 to 80 kpc independently, from RR Lyrae
(RRab) stars with good distances, and redoes RAW1's statistic in every bin with the measured slope.

## 1. Inputs (untracked, never added to git, read as untrusted data with `python3 -I`, paths as arguments)

- PS1: `_external_data/ps1_rrlyrae_sesar2017_J_AJ_153_204/table5_subset.tsv` (Sesar et al. 2017, AJ 153, 204;
  239,044 rows; sha256 ab4b837f...f813, checked by the script).
- DES: `_external_data/des_y6_rrlyrae_stringer2021_J_ApJ_911_109/table1.tsv` (Stringer et al. 2021, ApJ 911, 109;
  6,971 rows; sha256 94e3eb68...8303, checked).
- DESI BHB: `MWS_BHB.fits` (sha256 5669c821...5246), read only through RAW1's loader as MWT1 did.

Numbers read from the papers on 2026-11-13 through web pages (ar5iv HTML of arXiv 1611.08596 and 2011.13930;
each read twice; PROVISIONAL):

| number | value | source | reads agree |
|---|---|---|---|
| PS1 RRab score cut | score_3,ab > 0.8 ("91% pure and 77% complete at ~80 kpc"; "97% pure and 92% complete within ~40 kpc") | Sesar+17 sec. V.1, Fig. 9 | yes |
| PS1 selection function | logistic in flux-averaged r_F: S = L / (1 + exp(k (r_F - x0))), decreasing to faint mags, L = 0.91, k = 4.1, x0 = 20.57 mag (50% point); "approximately constant at ~90% for r_F <~ 20" | Sesar+17 sec. V.2, eq. 7 | yes (the HTML rendering of the sign in the exponent was garbled; the text says it drops to zero at faint r_F, so the decreasing sign is used) |
| PS1 measured where | high latitude |b| > 20 deg (Stripe 82 for purity, Draco for completeness) | Sesar+17 sec. V.2 | yes |
| PS1 distances | precise to 3 per cent | Sesar+17 abstract | one read |
| DES completeness | "> 70% complete at ~150 kpc" (abstract); detection efficiency "> 95% out to 150 kpc" (Fig. 11 caption); ">= 50% for mu <= 22" | Stringer+21 | one read each; the function's form and parameters are NOT given |
| DES halo fit | elliptical broken power law, q fixed 0.7, binned Poisson likelihood, 9 < r_e < 100 kpc: break 32.1 +1.1/-0.9 kpc, inner 2.54 +/- 0.09, outer 5.42 +0.13/-0.14 (full sample); Oo-I subset: 31.3, 2.32, 5.59 | Stringer+21 Table 2, App. C | yes |
| DES masks | LMC 27.1 deg, SMC 12.6 deg, Fornax 2.0 deg, Sculptor 1.0 deg; no Sgr or cluster mask mentioned | Stringer+21 Table 8 | yes |

Not readable / not in the tables, and therefore bracketed or set from memory (PROVISIONAL, flagged as memory):
- The PS1 table has no r_F magnitude. r_F is computed as DM + M_r with M_r = +0.6 mag for RRab (memory). Check of
  consistency with the paper: this puts the completeness at 80 kpc at 0.91 / (1 + exp(4.1 (20.12 - 20.57))) = 0.79,
  near the quoted 77-80 per cent.
- PS1 purity as a function of distance is not given beyond 90-97 per cent; it is bracketed by the score cut only.
- Published PS1 halo-profile fit (Hernitschek et al. 2018, from memory, NOT re-read): single power law with index
  about 4.4 and q about 0.92 over about 20-130 kpc, no break required. Used only for comparison, never as an input.
- Literature on q: DES fixed 0.7 (read); other halo fits put q between about 0.6 and 0.95 (memory).

## 2. Geometry and frame

Galactocentric frame exactly RAW1's (`frame_affine`, R0 = 8.122 kpc, z_sun = 20.8 pc, astropy). Distance
d = 10^(DM/5 + 1) pc. Galactic l, b and Sagittarius coordinates (Lambda, B) by RAW1's `sgr_lat_lon`.
Flattened radius r_q = sqrt(x^2 + y^2 + (z/q)^2) with z along the Galactic pole. The fitting range is on the
SPHERICAL r; the density is evaluated at r_q.

Sky grid (footprint and normalisation): equal-area cells, 180 in RA (2 deg) by 90 in sin(dec) (width 2/90);
cell area 2.546 deg^2. Every cut below is applied per CELL by the cell centre, and a star is kept only if its cell
is kept, so the data and the normalisation see exactly the same footprint. The normalisation integral uses 2 x 2
sub-directions per cell and 120 nodes in ln d (trapezoid) over a d range wide enough to cover the r range in every
direction, with the r range applied per node.

## 3. Sample cuts (frozen)

PS1 nominal:
- RRab: S3ab > 0.8 (paper's cut).
- Coverage: a cell is in the PS1 footprint if its centre has dec > -30 deg and the cell holds at least one row of
  the full 239,044-row table (any score).
- Galactic latitude: |b| > 20 deg (cell centre).
- Reddening: cell masked if the median E(B-V) of all table rows in it exceeds 0.25 mag.
- Sagittarius stream: cell masked if |B_Sgr| < 15 deg at the cell centre (RAW1's band width). This masks the
  orbital-plane band at all distances (leading and trailing arms).
- Magellanic Clouds and the two southern dwarfs: cells within 27.1 deg of the LMC (RA 80.89, Dec -69.76), 12.6 deg of
  the SMC (13.19, -72.83), 2.0 deg of Fornax (39.997, -34.449), 1.0 deg of Sculptor (15.039, -33.709) masked
  (radii read from Stringer+21; centres from memory, PROVISIONAL; immaterial for PS1, which stops at -30).
- Dwarf galaxies and globular clusters, frozen clustering rule (no flag in the PS1 table): among the RRab passing
  the score cut (all distances), a star is a clump star if at least 4 OTHER such stars lie within 0.5 deg of it
  with |Delta DM| < 0.25 mag. Every cell whose centre lies within 1.5 deg of a clump star is masked at all
  distances. The number of clump stars and masked cells is reported with the positions of the clump centres.
- Fitting range: 20 <= r < 80 kpc (spherical Galactocentric).
- Completeness folded into the normalisation: C(d) = 1 / (1 + exp(4.1 (DM(d) + 0.6 - 20.57))) (L cancels).

DES nominal (cross-check only):
- RRab: all 6,971 candidates (the paper's "Full" sample) except anomalous Cepheid candidates (ACc = True) and stars
  with a non-empty `Sys` (resolved stellar system) field.
- Coverage: a cell is in the DES footprint if it holds at least one row of the table, or if at least 5 of its 8
  grid neighbours hold at least one row (fills Poisson holes; the edge is uncertain by about one cell).
- Same latitude, Sgr band, Magellanic and dwarf masks and clustering rule as PS1. Reddening: cell masked if the
  median Ag exceeds 0.80 mag (about E(B-V) 0.25 with A_g / E(B-V) about 3.2, memory).
- Fitting range: 20 <= r < 100 kpc (DES's own reach; its paper fitted to 100). Completeness: flat (the paper's
  > 95 per cent to 150 kpc).

## 4. Density model and fit (frozen)

Number density n(r_q): single power law n = (r_q/40)^(-a); broken power law n = (r_q/rb)^(-a_in) for r_q < rb and
(r_q/rb)^(-a_out) beyond, continuous at rb, rb free in [25, 75] kpc ([25, 95] for DES). Unbinned likelihood in
the stars' 3D positions: ln L = sum_i ln n(r_q,i) - N ln Z, Z = sum over the grid of n(r_q) C(d) d^3 dlnd dOmega
(the d^2 C(d) Jacobian per star is parameter-free and omitted). Fits: single by bounded 1D minimisation of
-ln L over a in [0, 10] with the profile interval (Delta = 0.5); broken by a grid over rb in steps of 2.5 kpc
(Nelder-Mead in (a_in, a_out) at each), then a 3-parameter Nelder-Mead from the best grid point. Uncertainties
from the numerical Hessian of -ln L at the optimum.

Nominal q = 1 (spherical; RAW1's Jeans is spherical). q = 0.7 is a bracket (DES's fixed value; literature range
about 0.6-0.95, memory).

**Break detected** if 2 Delta ln L (broken, free rb, against single) exceeds T, where T is the 99th percentile of
2 Delta ln L over 100 parametric null mocks drawn from the best single law with the nominal PS1 footprint,
completeness and N (frozen threshold; floor 6.63, MWT1's threshold, if the bootstrap gives less). This is a
bootstrap threshold, not MWT1's chi2(1) threshold, because the break radius is free. The same T is used for every
PS1 bracket; DES gets its own T from 100 null mocks with its footprint and N.

**Profile used in the Jeans step:** the broken law if a break is detected on the nominal PS1 sample, else the
single law, with the fitted q = 1 parameters, extrapolated with its outermost slope beyond the fitting range (RAW1
integrates its tracer law to 2e4 kpc; kept). PS1 is the measurement; DES is a cross-check whose f values are
reported, not graded.

## 5. Second step: RAW1's statistic with the measured slope

Everything RAW1 graded is kept: its sample (1,495 stars), bins (20-30, 30-40, 40-55, 55-80), velocities, errors,
beta (0.6586, with RAW1's per-bin beta ranges), its estimator `fit_f`, its rule (word PASS if |f - 1| <= 2 sigma_f,
HOT above, COLD below), its models: framework line with census and rotation-curve stellar mass on both footings
(RAW1's field reading: no external field, a0 = 9.36e-11 canonical, 1.13e-10 alt, raw1_model.py values), DESI's
NFW (H) and Newton (N). Only the tracer density n(s) inside the Jeans integral changes: RAW1's single slope 5.289
is replaced by the measured RR Lyrae profile n(s) (the integral uses the measured profile at and beyond each star's
radius, which is what "the slope at each bin's radius" means in a Jeans integral). The code is RAW1's functions
executed by AST exactly as MWT1 did, and MWT1's generalised `tracer`/`sr2_grid`/`predP` (copied, with citation),
at constant beta.

sigma_f = sqrt(s_stat^2 + s_slope^2 + s_beta^2): s_stat and s_beta as RAW1 computes them (s_beta redone with the
new profile), s_slope = standard deviation of f over 200 draws of the profile parameters from the Gaussian of the
inverse Hessian (rb clipped to its range, slopes to >= 0). This replaces RAW1's s_alpha.

**The assumption this needs, in words:** the BHB stars that carry the velocities and the RR Lyrae that carry the
density follow the same radial number-density profile (same slope at the same radius). Both are old, metal-poor
horizontal-branch stars, which makes it plausible, not certain (BHB/RR ratios are known to vary with metallicity
and age, and so with radius). **Check from the data on disk:** the PS1 single-slope fit restricted to the sky cells
that hold RAW1's 1,495 BHB stars and to 20-45 kpc (the reach of RAW1's alpha window), against RAW1's
alpha = 5.289 +/- 0.169: consistent if |difference| <= 2 sqrt(sigma1^2 + sigma2^2). Reported; it does not gate a
label. It is weak in one way stated now: RAW1's alpha comes from a different likelihood (magnitude windows), so
agreement of the two numbers is necessary, not sufficient.

## 6. Labels (per case; the four framework cases carry labels; H and N are reported with their words)

RAW1's words: census canonical HOT at 20-30 and 30-40; census alt, rc canonical, rc alt HOT at 30-40 only.

In this order:
1. **NO POWER** if the 30-40 word, computed for each of the 200 profile draws with sigma = sqrt(s_stat^2 +
   s_beta^2), is HOT in a fraction of draws between 0.16 and 0.84 (the slope's 68 per cent interval spans both
   outcomes).
2. **MEASURED SLOPE MAKES A PASSING BIN FAIL [bin, word]** if any bin RAW1 graded PASS is HOT or COLD.
3. **FAIL REMOVED BY THE MEASURED SLOPE** if every bin is PASS. A HIT, not a pass of the theory; it awaits an
   independent re-grade.
4. **FAIL SURVIVES THE MEASURED SLOPE [bins still failing, word]** otherwise (a RAW1-failing bin still HOT or now
   COLD).
**FRAGILE** if any frozen bracket (section 7) gives a different label word for that case. The label is read per
footing (canonical, alt) and never pooled.

## 7. Brackets (each redoes the PS1 fit and the second step; the nominal model choice, single or broken, is kept unless the bracket is the model choice)

completeness none (C = 1) and steeper (x0 = 20.07, 50 per cent point 0.5 mag brighter); score cut 0.6 and 0.9;
latitude |b| > 30; Sgr band none, 10, 20 deg; distance scale x0.95 and x1.05 (applied to the RR Lyrae distances,
the completeness kept a function of the observed magnitude); q = 0.7; the other model (single if broken was
chosen, broken if single).

## 8. Known answers, twins, mutations

Known answers (stop before any label if one fails):
- K1: a mock with a single slope 4.5 (q = 1) drawn from the nominal PS1 footprint and completeness with the data's
  N is recovered within 2 sigma, and no break is detected.
- K2: a mock with a_in 3.0, a_out 5.0, rb 35 is detected as broken and each parameter is recovered within 2 sigma
  (rb within 2 sigma or 5 kpc).
- K3: with RAW1's single slope 5.289 (and its s_alpha), every f and sigma_f of RAW1's six cases is reproduced to
  5e-4 (MWT1's K0 test).
- K4: SI check g(30 kpc), M = g r^2 / G as MWT1's K3.
Twins (reported; a failed twin is stated, it does not stop the run):
- T1: 50 further null mocks (new seed) from the best single law: at most 3 exceed T.
- T2: shuffle DM among the PS1 stars passing the cuts (all distances in the table, sky positions kept), recompute r,
  refit: no break beyond T. EXPECTATION WRITTEN NOW: at 20-80 kpc r is close to the heliocentric distance d, so a
  break that lives in the distance distribution largely SURVIVES this shuffle; a T2 failure is therefore not by
  itself evidence that a measured break is spurious. It is run because the brief asks for it.
Mutations (separate file `*_MUTATE.out`): M1 keep a random 60 per cent of the real PS1 stars with r > 40 kpc: a
break near 40 must be detected and the outer slope must steepen. M2 replaces the measured profile by n = r^-3.5 in
the Jeans step: f must fall in every bin of every case.

## 9. Expectation and hand estimate (written before any number)

Expectation: PS1 RR Lyrae give a single slope near 4.3-4.6 at 20-80 kpc, or a shallow-then-steep law with a break
near 25-35 kpc whose outer slope is about 4.5-5.5. DES (q 0.7, read) has inner 2.5, outer 5.4 and break 32.
Hand estimate of the second step: the Jeans relation sigma_r^2 (alpha + gamma - 2 beta) = V_c^2 with beta 0.66 and
gamma about 0.3 gives a predicted dispersion ratio sqrt((5.29 - 1.32 + 0.3) / (alpha' - 1.32 + 0.3)). For
alpha' = 4.4 that is 1.12, so f at 30-40 falls from 1.205 to about 1.07 (census canonical) and from 1.155 to about
1.03 (census alt): PASS with sigma about 0.06. At 20-30 census canonical moves from 1.095 to about 0.98. If DES's
form is right (outer 5.4 beyond 32 kpc), the 30-40 bin stays close to RAW1's value and the fail survives; its
shallow inner slope would push 20-30 cooler. So the answer rests on whether PS1 sees a steep outer slope beyond
about 30 kpc. My guess before running: the fail is removed for alt and rc, borderline for census canonical, with
the DES cross-check pointing the other way.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
