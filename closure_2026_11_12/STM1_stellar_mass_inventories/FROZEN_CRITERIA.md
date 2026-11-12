# STM1 FROZEN CRITERIA: MWI1's stellar-mass inventories redone from the full texts

Written 2026-11-12, before any number bearing on the answer was extracted in this lane. TEST lane.
Adopts nothing. Relabels no other lane. All published numbers will be web look-ups and are
PROVISIONAL. kappa = 1/2 FITTED; not theory closed.

## Question

MWI1 (closure_2026_11_12/MWI1_inner_baryons) compared the Milky Way stellar mass the framework's
rotation-curve fit needs (7.05 to 7.41 x 10^10 Msun canonical, 6.36 to 6.73 alt; lower ends used)
with five inventories taken from abstracts only, on mixed conventions, with one bulge borrowed
across papers and one erratum unread. Do MWI1's classes survive when each inventory is read from its
full text, put on one convention, and when the cold gas takes its published range?

## Disclosed before freezing

- MWI1's inputs and z values (LN15 6.08 +- 1.14; McM17 5.43 +- 0.57; C20 5.04 + 0.43; I25 disc
  5.27 (+0.2, -1.5) plus LN15 bulge 0.91; L25 2.607 +- 0.363) and its labels are known.
- From general memory, not yet checked: Licquia and Newman 2015 use a Kroupa IMF and a disc scale
  length near 2.7 kpc; Bovy and Rix 2013 give a dynamical disc mass near 4.6 x 10^10 and scale
  length near 2.15 kpc; Bland-Hawthorn and Gerhard 2016 give a total stellar mass near 5 x 10^10;
  Portail et al. 2017 give a bulge-plus-bar mass near 1.8 to 1.9 x 10^10 in the bar region;
  Madau and Dickinson 2014 give Chabrier = 0.61 and Kroupa = 0.66 times Salpeter mass. None of these
  is used until read from the source.

## The need (unchanged from MWI1)

Required stellar mass = A x 6.681 - M_cold - 0.15 (x 10^10 Msun), A lower end 1.256 (canonical) or
1.152 (alt), upper end 1.310 / 1.208 reported. M_cold = 1.191 in the MWI1 reading; the low and high
ends of the published cold-gas range (below) in the gas readings. The required total baryons
A x 6.681 are held fixed, so cold gas moves the stellar need one for one.

## Which number from each paper (fixed now, not by outcome)

General rule H (headline): the paper's own headline total Milky Way stellar mass, as stated in its
abstract or, if the abstract has none, in its summary/conclusions or main results table; the
central value as given. The error used is the total upward error: if statistical and systematic
upward errors are both given, their quadrature sum; if only one is given, that one; asymmetric
errors use the upward side.

Per paper:
- LN15 Licquia and Newman 2015 (arXiv:1407.1078): headline total stellar mass and its error.
- McM17 McMillan 2017 (arXiv:1608.00971): headline total stellar mass and error (the best-fit
  model's; as stated).
- C20 Cautun et al. 2020 (arXiv:1911.04557): headline total stellar mass and its upward error
  (for their fiducial model, as stated in the abstract or conclusions).
- BHG16 Bland-Hawthorn and Gerhard 2016 (arXiv:1602.07702): the total stellar mass in their
  summary table of best values (or text), with its error.
- L25 Lian et al. 2025 (arXiv:2508.13665): headline total stellar mass and error AS CORRECTED BY
  THE ERRATUM if the erratum changes it; otherwise the original. Both are reported.
- I25 Imig et al. 2025 (arXiv:2507.17629): if the paper gives a whole-Galaxy total stellar mass,
  use that; otherwise composite = the paper's headline disc mass + the bulge/bar stellar mass of
  Portail et al. 2017 (below), upward errors in quadrature. (MWI1 borrowed LN15's bulge; that is
  replaced by Portail for every composite row.)
- BR13 Bovy and Rix 2013 (arXiv:1309.0809): composite = their headline disc stellar mass + Portail
  2017 bulge/bar stellar mass, errors in quadrature.
- P17 Portail et al. 2017: supplies the bulge/bar component only, not graded alone. Number used:
  the paper's headline stellar mass of the bulge plus bar (their abstract's stellar mass number;
  if it gives the bar-region stellar mass and the total bar+bulge separately, the larger region
  that the paper calls the total bulge plus bar stellar mass), with its upward error.
- Extra inventories (since 2015) found by search that give a whole-Galaxy total stellar mass (or
  total baryonic mass, from which the paper's own gas is subtracted; if no gas is given, the gas of
  the reading in use) with an error: graded under rule H as extra rows. Labels are reported on the
  core set (LN15, McM17, C20, BHG16, L25, I25, BR13: n = 7) and separately on core plus extras.

## Common convention (rule C)

Target: Kroupa (2001) IMF, stellar remnants and brown dwarfs included, whole Galaxy (no radial
truncation).
- Dynamical or kinematic masses (no IMF enters): no IMF conversion.
- Photometric/population masses: Chabrier -> Kroupa multiply by 0.66/0.61; Salpeter -> Kroupa
  multiply by 0.66 (Madau and Dickinson 2014, ARA&A, arXiv:1403.0007, IMF paragraph; to be read and
  cited). Other IMFs: use a ratio stated in the paper itself if given, else not converted and flagged.
- Remnants/brown dwarfs: if a paper excludes them and states the missing fraction, add it; if not
  stated, the row is not converted and is flagged.
- Radial truncation: if a paper's total is within a finite radius and it gives an exponential disc
  scale length, extrapolate the disc to infinity with that profile; otherwise flag.
- Errors scaled by the same factor. Each conversion stated with its source.

## Cold gas range

Total Milky Way cold gas (HI + H2, including helium) from Kalberla and Kerp 2009, Nakanishi and Sofue
2016, Heyer and Dame 2015 (H2), and McMillan 2017's gas discs (1.191 as ported). Where a paper's
mass excludes helium, multiply by the helium factor the paper itself states, else 1.36 (stated as an
assumption). Low end = lowest published HI total + lowest published H2 total; high end = highest +
highest. Whole-Galaxy totals, as MWI1 (MWI1 used McMillan's total to infinity).

## Rule (unchanged from MWI1)

z = (lower end of the need - published) / published upward error. SUPPLIED if z <= 1; WITHIN 2
SIGMA if 1 < z <= 2; NOT SUPPLIED if z > 2.

Readings, each per footing: H1 (rule H, gas 1.191), C1 (rule C, gas 1.191), H-lo, H-hi, C-lo, C-hi
(gas at the low / high end of its range). Label per reading and footing: SUPPLIED BY k OF n (naming
them); plus the class of McM17 (the record's census).

## IMF statement

Report need / published for each row, and compare with the mass ratio between IMFs (Salpeter/Kroupa
= 1/0.66; Kroupa/Chabrier = 0.66/0.61, Madau and Dickinson 2014). Say whether the need corresponds
to a change of IMF within, between, or beyond these. Dynamical rows do not move with the IMF; this is
stated.

## Checks

| id | check | pass condition |
|---|---|---|
| KA1 | MWI1's table from MWI1's inputs | z = +0.85, +2.84, +4.68, +4.14, +12.24 (canonical) and +0.24, +1.62, +3.06, +0.84, +10.33 (alt), each within 0.01 |
| KA2 | the need | 7.050 / 6.356 lower ends within 0.002 at gas 1.191 |
| KA3 | IMF factors | 0.66/0.61 = 1.082 within 0.001 |
| M1 | mutation: excess amplitude (A - 1) halved | at least one row changes class on each footing in reading H1 |

## What a label will and will not mean

As MWI1: SUPPLIED says the need is inside one published error bar, not that the Galaxy has that mass.
The need is the record's fit, not recomputed.
