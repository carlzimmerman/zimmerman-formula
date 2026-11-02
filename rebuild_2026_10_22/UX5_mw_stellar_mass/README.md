# UX5_mw_stellar_mass: both failures stand. K_z FAILURE SURVIVES on the real field equations, on both footings. The Upsilon gap at 60-150 km/s is NOT CARRIED, though the level miss against GSWLC is narrow; the step in shape is what no offset touches

Criteria: `FROZEN_CRITERIA.md` (331d49b71d), committed alone first. **Not blind**; it lists what I'd read. `ux5_core.py`, `ux5_checks.py`, `ux5_grid.py`, `ux5_read.py`, `ux5_ups.py`; post-result, no label: `ux5_post.py`, `ux5_post_k.py`. kappa = 1/2 FITTED. Footings never pooled. Reinstates nothing; the cold sector stays retired. Nothing here says the data favour the framework. Not theory closed. No line moved.

**The brief's premise needed correcting.** LW1's Milky Way form A was never one-zone: it is already a 2D AQUAL solve with thin and thick discs, bulge, HI and H2. DiskMass is the one-zone part. What was new here is a real QUMOND solve, varied vertical structure, and grid convergence.

## 1. Vertical force
Form Q solves lap Phi = div[nu grad Phi_N] on the same grid. Class on UR3's gate, unchanged:

| Box | form A, canonical / alt | form Q, canonical / alt | form R, in-prior cells, canonical / alt |
|---|---|---|---|
| B175, X5's cells | INFEASIBLE / INFEASIBLE | INFEASIBLE / INFEASIBLE | 1 / 6 |
| BV, 4725, heights and thick share varied | INFEASIBLE / INFEASIBLE | INFEASIBLE / INFEASIBLE | 15 / 134 |
| BV2, 2025, thick R_d 2.0 | INFEASIBLE / INFEASIBLE | INFEASIBLE / INFEASIBLE | 72 / 196 |

**Label for forms A and Q: K_z FAILURE SURVIVES**, both footings.

- **The two field equations agree.** K(R0) Q/A differs by at most 0.13 %, v_c by 0.06 %. The choice AQUAL or QUMOND doesn't matter here. I expected a few per cent.
- **Lowest K(R0) with v_c in its line, against the line's top of 70.8:**

| | B175 | BV | BV2 |
|---|---|---|---|
| form A, all cells, canonical / alt | 76.7 / 76.9 | 73.8 / 74.3 | 71.6 / 74.4 |
| form A, in priors, canonical / alt | 83.5 / 83.5 | 82.7 / 80.9 | 75.9 / 76.2 |

  Form Q is within 0.1 of these. Structure helps by up to 8 units in priors, and a thick disc of length 2.0 does nearly all of it. It never reaches the line.
- **Form R isn't an approximation to either equation.** At the same baryons its K(R0) is 9-28 % below form A canonical, 11-30 % alt, median 21 %, 23 %. Its pass comes from that difference, and it has no field equation behind it.
- **Form R's pass still fails the K_z scale length everywhere in priors.** h 3.29-3.41 on BV (2.72 +- 0.15), strict count in priors 0 in every box and footing. It's still unmoved as a test of a0: a0 x 1.5 keeps it FEASIBLE IN PRIORS, 6 and 6 cells on B175.

**How hard the fail was tried:** doubling the grid moves K by at most 0.10. a0 x 1.5 worsens A and Q. Kuzmin's exact disc field is recovered to 0.09 %.

**Where it's weakest, post-result, no class change.** The fail leans on Bovy and Rix's summaries, which were fitted inside Newtonian potential families. On alt, BV2, in priors, 9 form A cells (8 form Q) pass v_c, chi2_Kz and Ou; K(R0) 77.7 is all that stops them (+5.1 sigma), plus h 3.6, which isn't in the gate. The same data's chi2 line lets K near 76 through, because of its 5 % pad. Older K_z values, from memory, PROVISIONAL, about 71 +- 6 and 74 +- 6, wouldn't exclude 76. On canonical no in-prior cell passes all three non-K lines in any box.

**No single form clears both weighings still:** Q inherits A's position, so MW fails, and DiskMass form A at r 1.477 has no label (LW1). OD1's c isn't changed by this.

## 2. Upsilon at 60-150 km/s
**Label: NOT CARRIED, both footings.** Law U_tot canonical 0.620, 0.650, alt 0.530, 0.590; GSWLC 0.277, 0.304; Taylor 0.231, 0.231. Reproduced from UL1 per galaxy, |d| 0.

| Channel | canonical | alt | Reading |
|---|---|---|---|
| Offset passing level, Taylor | +0.331 to +0.378 | +0.284 to +0.327 | beyond Salpeter's +0.24 (PROVISIONAL) |
| Offset passing level, GSWLC | none, best +0.204, abs Z max 2.12 | none, best +0.155, 2.14 | narrow miss |
| Offset, shape | never: step -3.0, chi2 14.1 | never: step -3.0, chi2 12.3 | offset can't change it |
| Differential needed, 60-150 less 150-250, GSWLC / Taylor | +0.249 / +0.149 dex | +0.227 / +0.127 | on disk the term is -0.085: wrong sign |
| L_W1/L_3.6 needed in the two bins | 2.23, 2.14 | | measured 0.89 (n 5), 0.54 (n 2): wrong way, small n |
| Uniform D shift, 60-100 / 100-150 | x 1.38, 1.30 errors / x 1.48, 2.82 | x 1.26, 0.93 / x 1.38, 2.32 | second bin over 2 errors |
| Uniform i shift | +22 deg, 7.3 errors / unreachable (0.47 at the cap) | +13, 4.3 / unreachable (0.40) | no |
| MAP, D and i free in errors, Z GSWLC | +3.24, +2.66 | +3.64, +2.52 | fails; U 60-100 rises to 0.78, 0.82 |
| Gas factor, no label | 4.45 / over 6 | 3.55 / 5.55 | far too large for H2 or helium |

- **Bin mapping can't do it.** GSWLC's largest bin anywhere is 0.505, and 1.3-1.4 % of galaxies in these two bins reach the law's value.
- **Photometry:** estimator U doesn't change with axis ratio at fixed V in these bins (0.277/0.277, 0.304/0.311), and UL1's D > 60 cut leaves them alone. So I find no dust or aperture signal here. That tests only what's on disk.
- **Distance, post-result, no label:** galaxies with TRGB, Cepheid, SN or UMa distances read U_tot 0.622 +- 0.063 canonical, 0.550 +- 0.063 alt, and star-dominated ones among them 0.600 +- 0.072, 0.510 +- 0.067. Accurate distances don't remove the gap. That's the strongest evidence against the D channel.

**Where this is weak.** The frozen line says NOT CARRIED, but the GSWLC level miss is 0.12 sigma past a 2 sigma line, and UL1's 0.04 pad is partly what sets it. A shift of +0.12 to +0.2 dex for non-parametric star formation histories (PROVISIONAL, arXiv:2006.03599, 2409.03959; read as search summaries) is about the size needed on GSWLC, with no IMF change. So a uniform SPS shift nearly covers the level on one estimator. It doesn't cover Taylor, and it doesn't cover the 100-150 to 150-200 step, which needs a differential. I found no measured differential of the right sign. Bursty low-mass histories could have that sign in principle; I didn't establish a size. UL1's K6 also showed the shape test has limited power against Taylor. The step in the law's bins is the most specific failure, and it rests on 23 and 25 galaxies.

## 3. What would decide each (judgment)
- **K_z:** K_z(R0, 1.1 kpc) to about +-3, measured without a Newtonian potential family. Direct binary-pulsar accelerations do this in principle; published errors are still about 5 times kinematic ones (PROVISIONAL, arXiv:2010.04018). At or below about 71: forms A and Q are out on these baryons. At or above about 75: Bovy and Rix's summary is wrong, and form R's in-prior cells mostly go. Between: not decided.
- **Upsilon:** star-count mass per 3.6 micron light, from resolved colour-magnitude diagrams, for about ten SPARC discs across 60-200 km/s, on one method. No gravity law enters, though the IMF below the counting limit still does. Median near 0.3 at 60-150 fails the law's level; near 0.6 removes the gap and puts the estimators in the wrong. A step down into 150-200 tests the shape.
- **DiskMass:** OD1's answer stands, two-component fits for c on DiskMass-class spectra.

## Limits
Only two field equations were tested; this doesn't exclude a different one, and none is derived. Gas held at McMillan17's. Heights and shares are from memory, PROVISIONAL. Isolated solves. The MAP uses half-sigma steps to 3 sigma, with UL1's bin membership kept fixed. Bin error treatment is UL1's. Matches for L_W1/L_3.6 are 5 and 2 galaxies. Estimators remain estimators.

## Checks
All passed: Q1 Plummer 0.18 %. Q2 Kuzmin 0.08 %, 0.09 %. Q3 all 175 cells vs LW1 1.4e-12. Q4 177.092, 61.889. Q5 max dK 0.09, 0.10. P1 |dU| 0. MUTATE: Q with nu = 1 fails Q1 (0.90) and Q2 (0.48) as required; a0 x 1.5 moves K; injected low bins pass there, doubled fail; removing the prior moves U (0.037 dex).
Rerun byte-identical for `ux5_read`, `ux5_ups`, `ux5_post`. `ux5_checks.out` is NOT byte-identical. It prints a wall-clock timing line, the likely cause, but I kept no earlier copy to diff. `cache/` isn't committed: 12 MB, rebuilt by `ux5_grid.py`, about an hour for all four runs.

## Expectation against result
Q near A, failure survives on B175: held, 65 %, and closer than I said. BV reaching priors, 25 %: didn't happen. Part 2: I said LEVEL ONLY on GSWLC near Salpeter; wrong, it misses narrowly at +0.204, and +0.24 breaks the high bins (-2.8, -2.5). Shape fail and D, i not carrying: held.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
