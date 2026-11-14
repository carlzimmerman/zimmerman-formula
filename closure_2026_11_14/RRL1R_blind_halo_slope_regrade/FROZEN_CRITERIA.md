# RRL1R FROZEN CRITERIA: blind re-grade of RRL1 (stellar-halo density slope from RR Lyrae; RAW1 redone with it)

2026-11-14. TEST lane, blind re-grade. Adopts nothing, relabels nothing, registers nothing.
Written and committed (with `WHAT_I_SAW_AT_START.md` only) before any script of this lane and before any
number was computed from the RR Lyrae tables.

What I had seen of the data at freeze time: the two MANIFEST.txt files and the DESI BHB MANIFEST; the header,
units and column-description lines of both RR Lyrae tables; two data rows of the PS1 table (the third command
reprinted the second row) and three data rows of the DES table. Nothing else. I have read RAW1's
`RESULT.md`, `raw1.py`, `raw1_model.py` and the first 310 lines of MWT1's `mwt1.py` (whitelisted prior
context). I have not opened anything of RRL1 beyond the specification handed to me (its sections 0 to 8).

## 1. Adopted

Sections 0 to 8 of RRL1's frozen criteria (the specification `RRL1R_brief_spec.md` handed to this lane) are
adopted as written: question, inputs and provisional numbers, geometry and frame, sample cuts, density model and
fit, the second step, label words and their order, the brackets, the known answers, the twins and the mutations.
Where this file says more, it fills a gap the specification leaves open; where it differs, the difference is
listed in section 3 with its reason. Two footings (canonical a0 = 9.36e-11 m/s^2, alt 1.13e-10) are graded
separately and never pooled.

## 2. Choices the specification leaves open (fixed now)

Data reading
- Both tables parsed by my own reader (tab-separated, lines starting with `#` skipped, then the column-name,
  unit and dash lines). sha256 of each input is checked against the MANIFEST value before use; the script stops
  on a mismatch. PS1 rows with a non-finite RA, Dec, S3ab, DM or E(B-V) are dropped from the star list (counted
  and reported); all rows with finite RA/Dec count for coverage.
- PS1 junk values: the DM column's declared range starts at -206.3 and E(B-V) reaches 99.8. No extra cut is
  added: a star enters the fit only if its r falls in the range, and the reddening mask uses the cell median,
  which a few sentinels do not move. Stars with absurd DM simply never enter the fit.

Grid and normalisation
- Cell (i, j): RA in [2i, 2i+2) deg, sin(dec) in [-1 + 2j/90, -1 + 2(j+1)/90). Cell centre at RA 2i+1,
  sin(dec) at the middle of its band. A star belongs to the cell its RA and sin(dec) fall in.
- Sub-directions: RA at 2i+0.5 and 2i+1.5 deg, sin(dec) at the first and third quarter points of the band;
  each carries solid angle (4 pi / 16200) / 4.
- Distance nodes: per sub-direction, 120 nodes uniform in ln d from d(r = r_lo) to d(r = r_hi) along that
  direction (the d range covers exactly the spherical r range in that direction; the r range check per node is
  then satisfied by construction), trapezoid weights in ln d. Node weight w = C(d) d^3 dlnd dOmega.
- Speed-up, verified: the node weights are summed into 4,000 bins uniform in ln r_q, each bin carrying its
  weighted mean ln r_q; Z = sum_k W_k n(r_q,k). Accepted only if Z from the bins agrees with Z from all nodes to
  1e-5 (relative) at (single 3.0), (single 5.0), (broken 3.0 / 5.0 / 35) and (single 4.5, q = 0.7); checked in
  the run (check K0n). If it fails, the full node sum is used.
- Galactic l, b of cell centres and of the BHB stars by astropy; Sgr B by RAW1's `sgr_lat_lon` (executed from
  RAW1's source by AST, read-only); Galactocentric x, y, z by RAW1's `frame_affine` (R0 8.122, z_sun 20.8 pc);
  r_q uses that frame's z.

Clustering rule
- Applied to all PS1 rows with S3ab above the cut in use and finite DM (all distances). Neighbours: angular
  separation < 0.5 deg (KD-tree on unit vectors, chord) and |Delta DM| < 0.25; a star is a clump star if it has
  >= 4 such neighbours other than itself. Cells with centre within 1.5 deg of any clump star are masked.
  Reported clump centres: clump stars grouped by friends-of-friends with a 1.5 deg linking length; each group's
  mean RA/Dec, median DM, star count. In the score-cut brackets the rule is re-run with that bracket's cut (the
  rule says "among the RRab passing the score cut").
- For DES the rule runs on the DES stars kept by the ACc/Sys cuts.

Fits
- Single law: bounded minimisation over a in [0, 10] (xatol 1e-7) and the profile interval Delta ln L = 0.5;
  the Hessian error (central second difference, h = 0.01) is the one used for draws and comparisons; both
  reported.
- Broken law: rb grid 25.0, 27.5, ..., 75.0 (21 points; DES 25 to 95, 29 points), Nelder-Mead in (a_in, a_out)
  from (a_single, a_single) at each grid point, then a 3-parameter Nelder-Mead from the best grid point
  (xatol 1e-6, fatol 1e-8). rb is bounded by returning +inf outside its range; slopes are free (no bound) in the
  fit. 2 Delta ln L = 2 (min nll single - min nll broken), floored at 0 for reporting.
- Hessian of the broken law: central differences with steps (0.02, 0.02, 1.0 kpc); the rb step is wide because
  ln L has a kink in rb at every star's radius. If the Hessian is not positive definite, the steps are doubled
  once; if still not, the rb error is taken from the profile over the rb grid (half-width of Delta nll <= 0.5,
  with the slopes' 2x2 Hessian at fixed rb), and this is reported.
- Mock stars (null, K1, K2, T1, DES null): drawn from the binned normalisation (bin k with probability
  proportional to W_k n(r_k), then uniform in ln r inside the bin); q = 1, so r = r_q. Mock size = the data's N
  of that sample. 99th percentile by numpy's default (linear) interpolation over the 100 values.

Profile draws and the second step
- 200 draws per fitted profile from the Gaussian of the inverse Hessian (single: a only), rb clipped to its
  range, slopes clipped to >= 0.
- My own Jeans integral: sigma_r^2(r) = [n(r) r^(2 beta)]^-1 int_r^(2e4 kpc) n(s) s^(2 beta) g(s) ds, evaluated
  in ln s on a 6,000-point log grid from 1 kpc to 2e4 kpc with the break radius inserted as a node, cumulative
  trapezoid from the outer end, ln sigma_r^2 interpolated in ln r at each star. g(s) from RAW1's
  `raw1_model.g_model` (imported read-only). The profile is the fitted law extrapolated with its outermost
  slope (and innermost slope inward).
- RAW1's sample (1,495 stars), bins, velocities, errors, beta and per-bin beta ranges come from RAW1's
  `load`, `build` and `measure` executed read-only (AST, as MWT1 did); `fit_f` is RAW1's. Per bin and case:
  f, s_stat from `fit_f` with P = sigma_r^2(r) (1 - beta sin^2 eta); s_beta = 0.5 |f(beta_hi) - f(beta_lo)|
  over RAW1's per-bin range, with the new profile; s_slope = standard deviation (ddof 0) of f over the 200 draws
  (beta nominal); sigma_f = sqrt(s_stat^2 + s_slope^2 + s_beta^2). Words: PASS if |f - 1| <= 2 sigma_f, HOT
  above, COLD below.
- NO POWER rule: for each draw, the 30-40 word uses that draw's f and s_stat with the nominal profile's s_beta;
  NO POWER if the HOT fraction is in [0.16, 0.84] inclusive.
- RAW1's own words per bin (the reference for rules 2 to 4) are read from `raw1_results.json` (its nominal f and
  sigma_f, graded by RAW1's rule), not typed in.
- Label rules 1 to 4 are applied to H and N as well and reported with their words, not graded.
- FRAGILE: a bracket whose label HEAD word (NO POWER / MEASURED SLOPE MAKES A PASSING BIN FAIL / FAIL REMOVED BY
  THE MEASURED SLOPE / FAIL SURVIVES THE MEASURED SLOPE) differs from the nominal one. Changes only in the
  bracketed bin list are reported but do not set FRAGILE.

Brackets (section 7) are PS1-side only: RAW1's BHB sample keeps its own Sgr band, distances and beta. Each
bracket redoes the PS1 fit of the nominal model choice (both models are fitted and 2 Delta ln L reported, for
information), the 200 draws and the full second step with its labels. The distance-scale brackets multiply the
RR Lyrae distances by 0.95 / 1.05 and evaluate C at the table magnitude DM_table + 0.6. q = 0.7 is used in the
fit; the Jeans step stays spherical with the fitted slopes and rb. T is the nominal one for every PS1 bracket.

DES cross-check: model chosen by DES's own T (100 DES null mocks); the second step with that profile and its
200 draws; f and sigma_f reported per case, not graded. Both laws' parameters reported.

BHB-vs-RR Lyrae check (section 5): the cells holding at least one of RAW1's 1,495 stars, intersected with the
nominal PS1 footprint; r range [20, 45); single fit; |a - 5.289| <= 2 sqrt(sigma_a^2 + 0.169^2) is
"consistent". Reported, does not gate.

Known answers, order of running
- K0n (normalisation compression, above), K3 (RAW1's six cases reproduced with my Jeans at RAW1's alpha and
  s_alpha, f and sigma_f to 5e-4 against `raw1_results.json`), K3a (my Jeans against the analytic flat-curve
  answer V^2 / (a - 2 beta) for a single law, and the exact broken-law flat-curve answer, to 1e-3), K4 (SI:
  g(30 kpc) for FW census canonical; M = g r^2 / G with my own constants against `raw1_model.M_of_g`, to 1e-9)
  run first, before any RR Lyrae number.
- K1 and K2 need T and the data's N. Order: nominal PS1 cuts and single and broken fits (no label, no second
  step), the 100 null mocks and T, then K1 and K2. Only after all K pass: second step, brackets, DES, twins,
  mutations, labels.
- K1 "recovered within 2 sigma": |a_fit - 4.5| <= 2 sigma_Hessian; "no break": 2 Delta ln L <= T.
- K2: 2 Delta ln L > T, |a_in - 3| <= 2 sigma, |a_out - 5| <= 2 sigma, and |rb - 35| <= max(2 sigma_rb, 5).

Twins and mutations as section 8. T2's star set: PS1 rows with S3ab > 0.8 and finite DM in kept cells, all DM;
the DMs are permuted among them, r recomputed, the 20 to 80 range applied, both laws refitted.
M1 passes if (a) 2 Delta ln L > T, (b) rb within [32.5, 47.5] kpc ("near 40", fixed now), and (c) a_out(M1) >
a_out(nominal broken fit). M2 passes if f(n = r^-3.5) < f(nominal profile) in every bin of all six cases.

Seeds (numpy default_rng): null mocks 141101; K1 141102; K2 141103; T1 141104; T2 141105; M1 141106;
nominal profile draws 141107; bracket draws 141200 + bracket index; DES null mocks 141108; DES draws 141109.

Compute: one process, `nice -n 19`, BLAS threads 1, mock-loop results appended to a checkpoint file in the
output folder (resumable). The graded run writes to the lane folder; the identity run writes to a copy folder
and every output is compared byte for byte.

## 3. Where I differ from, or read narrowly, the specification

- Per-direction ln d range (section 2 above) instead of one global d range masked per node: same integral, no
  edge-node error. Reason: accuracy; the specification's wording ("wide enough to cover ... with the r range
  applied per node") is satisfied.
- The 4,000-bin compression of the normalisation (verified by K0n, fallback to the full sum).
- s_beta in the NO POWER rule is the nominal profile's, not recomputed per draw (per-draw recomputation would
  triple the cost and s_beta depends on the profile only weakly). Reported.
- None of these changes a frozen threshold or label rule.

## 4. My hand estimate (written before any RR Lyrae number)

- Single slope over 20 to 80 kpc (q = 1): about 4.3 (range 3.8 to 4.8), Hessian error about 0.05 to 0.1.
- A break is likely detected (literature halos break at about 20 to 35 kpc), with rb about 25 to 35, a_in about
  2.5 to 3.5, a_out about 4.5 to 5.2. Probability I give to "break detected": 0.65.
- Second step: a profile shallower than 5.289 at 30 to 55 kpc raises the predicted dispersion by roughly
  (5.29 - 1.32) / (a - 1.32); for a about 4.4 to 4.8 at those radii, f drops by 6 to 12 per cent. Then the 30-40
  bin moves toward PASS for every case, and the rc cases risk COLD at 40-55 (RAW1 0.99 / 0.97 there, sigma
  about 0.05).
- Labels I expect, least confident first: census canonical: FAIL REMOVED BY THE MEASURED SLOPE (0.45) or FAIL
  SURVIVES (0.35); census alt: FAIL REMOVED (0.5); rc canonical: FAIL REMOVED (0.45) or MEASURED SLOPE MAKES A
  PASSING BIN FAIL [40-55, COLD] (0.35); rc alt: MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55, COLD] (0.45).
  NO POWER unlikely for all (0.1) because the PS1 sample is large. FRAGILE likely (q = 0.7 and the other model
  move the slope by more than its error).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
