# U4L1 RESULT: the ALMA upper limit on U4_27928 read against the pre-release gas requirement

2026-11-12. Criteria `FROZEN_CRITERIA.md` (04f671aa84), amended by `AMENDMENT_A1.md` (d34c7bfe7e).
A secondary reading with no verdict weight. The governing plan (CFG806, clarification A-U6) forms no
Delta_m on a non-detection, and the release-day record (row A: nothing scored) stands. One disc
excludes no model. kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Label

- **As frozen: NO LABEL** (run 1 stopped at KA2; `u4l1_run1_stopped.out`).
- **As amended (A1): NO TENSION.** At the plan's primary conversion factor (alpha_CO 4.36), the
  framework cells are ALLOWED at the plan's primary pressure branch (case c, 302.9 km/s) and at its
  no-pressure branch (case a, 226.1 km/s), on both footings, with and without the aperture match.

The limit is not adverse at the plan's primary settings. It is tight.

## The primary cells (kernel n = 1, gas scale R_g = R_d)

Three-sigma limits: log M_gas < 10.88 (alpha_CO 4.36) and < 10.24 (alpha_CO 1.0), inside 8.27 kpc.
D = log limit minus log requirement; "matched" counts only the 84.8 per cent of an exponential gas
disc that lies inside the aperture, "as printed" compares with the total. Canonical / alt.

| case | speed [km/s] | framework requirement | D at alpha 4.36, matched (as printed) | label at 4.36 | label at 1.0 |
|---|---|---|---|---|---|
| a, no pressure term | 226.1 | 9.62 to 9.72 / 8.66 to 9.22 | +1.2 to +2.3 | ALLOWED | ALLOWED |
| c, pressure term (plan's primary) | 302.9 | 10.84 / 10.80 to 10.81 | +0.11 to +0.15 (+0.04 to +0.08) | ALLOWED | IN TENSION (-0.49 to -0.53) |
| b, a with the slow-bias correction | 314.1 | 10.90 to 10.91 / 10.87 to 10.88 | +0.04 to +0.08 (-0.03 to +0.01) | ALLOWED, three of four FRAGILE | IN TENSION (-0.56 to -0.60) |
| d, c with the slow-bias correction | 373.2 | 11.17 / 11.15 | -0.20 to -0.22 (-0.27 to -0.29) | MARGINAL | IN TENSION (-0.84 to -0.86) |

Over all three kernels and both gas scales the pattern is the same: at alpha_CO 4.36 no cell is IN
TENSION in any case; at alpha_CO 1.0 every framework cell at cases b, c and d is.

## What it says

1. **If the speed is the uncorrected 226 km/s, the limit tests nothing.** The framework needs
   under 10^9.8 Msun of gas, more than a dex below the limit.
2. **If the speed is the pressure-corrected 303 km/s, the framework needs the gas to sit just
   under the limit.** It requires 6.3 to 6.9 x 10^10 Msun; the three-sigma limit is 7.6 x 10^10.
   That is also about twice what the scaling relation gives for this galaxy (10.51, or
   3.2 x 10^10). Allowed, with 0.04 to 0.15 dex to spare.
3. **The conversion factor decides it.** The limit equals the framework's requirement at
   alpha_CO = 3.1 to 3.4 (case c) and 3.6 to 4.0 (case b). Below those values the framework would
   need gas that CO does not show: 3.6 to 5.2 x 10^10 Msun of atomic or CO-dark gas at alpha_CO 1.0.
4. **Not discriminating.** The rivals CFG571 coded (a0 proportional to H, and the RAR-equivalent)
   carry the same labels as the framework in every case at alpha_CO 4.36, and are IN TENSION with it
   at alpha_CO 1.0 (one rival cell is MARGINAL at case c). At alpha_CO 1.0 the galaxy's own
   scaling-relation gas mass is itself above the limit (MARGINAL, -0.20), so that branch says more
   about the conversion factor than about any law.
5. **A halo model is untouched:** it needs no gas to make the speed.

The earlier remark in this session that the limit "may count against the framework" is not borne
out at the plan's primary conversion. It would be at a starburst-like conversion, where it counts
against every no-halo reading equally.

## Checks

KA1: the limit recomputed in SI from 0.511 Jy km/s gives 10.880 and 10.241. KA2a (A1): the
independent routine with the sealed code's G reproduces the stored requirement to 3 x 10^-11 dex in
32 cells. KA2b (A1): with standard SI constants, 0.0015 dex where the requirement is 9.5 or more
(0.0132 in the one cell at 8.66). KA3: the requirement file's hash matches and it was first committed
2026-11-01, before the release. KA4: aperture fraction 0.8481, closed form equal to the integral.
M1 and M2 bite (`u4l1_mut.out`).

## Limits

- Conditional on the H-alpha speed being the circular speed of the gas disc. No CO kinematics exist
  for this galaxy; that is why the governing plan scores nothing.
- The limit is on CO-traced gas in a circular aperture of radius 2 R_e over +-500 km/s. Atomic gas
  is not seen.
- Cases b and d apply a population-median correction (CFG99's 28 per cent slow bias) to one galaxy.
- The 0.30 dex line between MARGINAL and IN TENSION is twice the plan's systematic floor, applied to
  a limit that is already three sigma.
- Stellar mass is held at log M* = 10.74; the plan carries a 0.2 dex systematic on it, which moves
  every requirement.

## Files

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `u4l1.py`, `u4l1.out`, `u4l1_results.json`, `u4l1_mut.out`,
`u4l1_run1_stopped.out`.
