# NC3 frozen criteria: do cluster-member and group-central early types carry a residue over the law that field early types do not? (FRAMEWORK_CANDIDATE_2 R5 / K4)

Frozen and committed alone, before any NC3 script or residual number. Kappa = 1/2 FITTED; not theory closed. Adopts
nothing. TEST lane (born-clumped cold dark energy; no particle). Footings graded separately, never pooled: canonical a0
9.3603e-11, alt 1.1312e-10. One thread, < 1 GB, no download. Lane id: no NC3 in `ls` or `git log` (NC1 in the record is
CFG489's unrelated "NC1 chassis"; the candidate's NC1/NC2 are the sibling lanes).

## Known before this freeze (not blind)

- The match counts only: MaNGA DynPop (QX22's file) x Tully 2015 2MASS groups (T15 table5, on disk from CFG393) within
  10 arcsec and |cz - HV| < 300 km/s: 1545 galaxies matched (u - r >= 2.5 red: 179, of which 81 sit in nests with Mlum
  >= 1e14 and 77 are singletons). No residual of any matched galaxy was looked at.
- The record's environment readings: CFG330/331 (four SLUGGS centrals +0.22 vs others +0.06, outer GC bins); QX24 T2 and
  EV1 W2 (seven X-ray ellipticals, NGC 720 isolated at +0.51); QX22 (MaNGA red galaxies on the law at fixed M* x sigma);
  KX1 (KiDS isolated lenses on the law after kSZ gas); QX33 (CLASH s).

## Primary sample (graded): MaNGA DynPop early types tagged by T15

- MaNGA DynPop JAM v2 (`_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits`) with QX22's quality cuts
  verbatim (Qual >= 1, finite NSA elpetro and Sersic masses, z > 0.005, finite lambda_Re and eps, sigma > 0, >= 8 finite
  JAM models), the best-chi2 JAM model's log_Mt_rhalf and rhalf, H0 70, QX22's accel(): g_obs = G M_t(<r_h) / r_h^2,
  g_bar = G (0.5 M*) / r_h^2 with M* = NSA elpetro mass. Residual r = ln g_obs - ln(nu(g_bar/a0) g_bar), nu the law's.
- Early type: T15 MType <= -1 (E and S0, de Vaucouleurs code). Reported: u - r >= 2.5 (QX22's red) instead.
- Match: nearest T15 galaxy within 10 arcsec and |c z - HV| < 300 km/s.

## Environment tagging rule (T15 nests; Mlum in 1e12 Msun as tabulated)

- **IN** (formed inside a clump, R5): cluster members, i.e. nest Mlum >= 100 (1e14 Msun) and Nmb >= 5 (centrals included),
  plus group centrals, i.e. PGC == PGC1 in a nest with 10 <= Mlum < 100 and Nmb >= 3.
- **FIELD**: Nmb == 1 (no other 2MRS K < 11.75 galaxy in its nest).
- Reported, not graded: group satellites (non-central members of 10 <= Mlum < 100 nests), and FIELD restricted to
  cz < 6000 km/s (where 2MRS sees fainter companions, so "single" is cleaner).

## Statistic (both footings)

D = cell-matched median residual difference IN - FIELD, in dex (ln / ln 10), on KU2/QX22's M* x sigma cells (0.2 dex in
M*, 0.1 dex in sigma): D = sum_c w_c [median(r_IN,c) - median(r_FIELD,c)] / sum_c w_c, w_c = min(n_IN, n_FIELD), cells
with >= 2 of each. Matching on sigma is the IMF control: the IMF trend (Posacki+2015, used by ST1) is a function of sigma,
so IN and FIELD in one cell share it. Reported: the Posacki correction applied per galaxy instead, with M*-only cells.
CI: 2000 bootstrap resamples of galaxies (seed 20261107), 2.5-97.5 %. sigma_D also carries QX22's model term (second-best
JAM) and mass term (Sersic M*), in quadrature with the bootstrap sigma; the CI used for the lines is D +- 1.96 sigma_D.

## The stripping budget (stated before any number)

R5 says members formed in a component-rich region, so they carry a halo or had it stripped. Tides remove a member's mass
outside r_t = r_p (m / (3 M_host(<r_p)))^(1/3). Budget: r_p from 0.1 to 0.5 Mpc for cluster members (cluster
centrals and group centrals are not stripped: they sit at their nest's centre, r_t undefined, budget 0). m = 10 x M* (a halo
carrying R ~ 5.6 x baryons, generous), M_host(<r_p) = Mlum x (r_p / 1 Mpc) (isothermal, generous to stripping). The budget
computes r_t / r_half per IN galaxy at both ends of r_p. If r_t >= 2 r_half for a galaxy, stripping cannot remove the
component inside r_half there; the residual at r_half is then stripping-proof. The fraction of IN galaxies that are
stripping-proof at the r_p = 0.1 Mpc end is reported and used in the K4 reading.

## Lines (per footing)

- **NO POWER**: half-width of the 95 % CI > 0.10 dex, or fewer than 5 matched cells.
- **R5 SIGNAL**: D > 0 and the 95 % CI excludes 0 and D >= +0.05 dex.
- **NO DIFFERENCE**: the 95 % CI lies inside [-0.05, +0.05] dex.
- **UNRESOLVED**: anything else.
- **K4 reading**: NO DIFFERENCE on both footings AND >= 50 % of the IN galaxies stripping-proof at r_half (r_p 0.1 Mpc end)
  -> K4 FIRES (the born-clumped picture's member prediction fails at r_half unless the component was never inside r_half,
  which is stated as the surviving reading). R5 SIGNAL on both -> R5 SUPPORTED at galaxy scale. Otherwise K4 not decided.

## Controls

- KA1: my reimplementation of QX22's sample reproduces QX22's T1 D (red, low-lambda minus high-lambda) to 1e-6 per footing.
- MUTATE M1 (separate output): environment tags shuffled within cells (seed 20261108), 200 shuffles. The mean D must be
  within +-0.01 dex of 0 and the first shuffle's CI must contain 0, on both footings. Otherwise the label is NO VERDICT.
- MUTATE M2 (power, separate output): +0.10 dex added to every IN residual. It must read R5 SIGNAL on both footings,
  otherwise the label is NO POWER.

## Two added reads (reported, with their pre-stated expectation)

- **KiDS isolated lenses, the field-by-construction control:** read KX1's M2 (the law against the isolated-lens data with
  the joint budget). Expectation under the candidate: nothing, i.e. z_law <= 2 in >= 3 of 4 bins on both footings.
- **CLASH lensing-only s (QX33):** an early-collapsed clump puts its mass more concentrated than the hot gas, so s <= 0
  past the BCG (r > 50 kpc reading). Read QX33's s HIGH / LOW on both footings and say whether they sit at or below 0.
  QX33 had no power on evolution; this read is about the sign of s, not its change.

## Further reported reads (small samples, no grade)

- SLUGGS (CFG330 K0 per-galaxy outer offsets, nu_mono) tagged by T15 using the SLUGGS RA/Dec on disk: IN vs FIELD medians.
- The seven X-ray ellipticals (QX24 T2 raw offsets; positions from QX24) tagged by T15: IN vs FIELD.
