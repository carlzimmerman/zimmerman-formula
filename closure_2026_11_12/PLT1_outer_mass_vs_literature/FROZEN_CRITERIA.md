# PLT1 FROZEN CRITERIA: the framework's enclosed mass at 100 kpc and beyond against the literature compilation of DESI DR2 Results III

Committed alone, 2026-11-12, before any script and before any value in the `fig13/` literature
files was read. Nothing below is re-tuned after the run. TEST lane. Adopts nothing. Relabels no
other lane and does not change the status of FALSIFIER_MATRIX row 32. kappa = 1/2 FITTED; not theory
closed.

## Question

Inside 80 kpc the release cannot separate the framework's two readings (NMB1, origin 9d17287e7e).
Beyond 100 kpc they differ by a factor of two to three: with the Local Group field the line
saturates near 5.3 x 10^11 Msun, with no field it keeps rising in proportion to radius. The paper's
Figure 13 compiles published enclosed masses out to those radii, in two classes: field halo stars,
and other tracers (satellites, globular clusters, streams). Which reading, on which footing, agrees
with each class?

## What was known when this was frozen

Known: the structure of the two files (columns; 22 and 29 rows; counts by tracer and radius band
printed in DR2REV's `figdata_inventory.out`: beyond 100 kpc four halo-star rows and four
satellite or globular-cluster rows, plus an unknown number at exactly 100 kpc). The paper's
sentence that distant halo-star results show "a hint of a ceiling" near 8 x 10^11 which the
satellite and globular-cluster results do not show, and that its NFW extrapolation lies above the
most distant halo-star points and is consistent with the higher satellite estimates. General
knowledge of this literature: halo-star and stream masses inside 100 kpc of roughly 5.5 to
7.5 x 10^11, and satellite-based virial masses of roughly 1.0 to 1.5 x 10^12.

Not known: any value, radius, label or error in the two literature files.

Hand expectation, stated before freezing: the field reading (about 5.1 x 10^11 at 100 kpc, 5.3
beyond 150 kpc) should pass or sit low against the halo stars and fail low against the satellite
class. The no-field reading (about 7.0 / 7.7 x 10^11 at 100 kpc, 1.4 / 1.5 x 10^12 at 200 kpc,
canonical / alt) should pass the satellite class and sit high against the most distant halo stars.
A split between the classes is the expected outcome. These are expectations, not results.

## Instrument

File: Zenodo 10.5281/zenodo.23712180, `desi-dr2-mw-mass-figdata.zip`,
md5 `5b0cc3aa9947286eb9348e947d01182d`.

- **Class H:** `fig13/literature-halo-stars.csv` (mass column `Menc_Msun`).
- **Class S:** `fig13/literature-other-tracers.csv` (mass column `value_Msun`).
- **Selection:** every row with `r_kpc` >= 100. No row is removed for any other reason, except a
  row without a usable error (mass <= 0, lower error <= 0 or >= the mass, upper error <= 0), which
  is listed and excluded.
- **Row error, in dex:** sigma_lo = log10(M / (M - err_lo)), sigma_hi = log10((M + err_hi) / M).
- **Systematic floor:** 20 per cent, s = log10(1.2) = 0.0792 dex, added in quadrature to every
  row. Reason, fixed in advance: the paper states that equilibrium mass estimates in this range can
  be biased by up to 20 per cent by the LMC and finds mock-calibrated systematics of that order,
  larger than the errors methods report.
- **Pull of a row:** z = (log10 M_line(r) - log10 M) / sqrt(sigma_side^2 + s^2), with sigma_side =
  sigma_lo when the line is below the row and sigma_hi when above. Negative z: line below the row.

## The framework's line

Baryons: McMillan 2017 (thin, thick, HI, H2 discs and the bulge, as ported in DW1), spherical
enclosed mass M_sph(<r), total 6.681 x 10^10 Msun, amplitude A = 1. Kernel
nu(y) = 1 / (1 - exp(-sqrt(y))). No fitted parameter. Footings: canonical a0 = 9.36e-11, alt
a0 = 1.13e-10 m/s^2.

- **E1, the field reading** (G239's QUMOND angle average; G241 identifies it with the
  modified-inertia reading): uniform external field e_N = 0.01273 in units of a0,
  M = (M_sph / g_b) (1/2) integral over mu in [-1, 1] of
  nu(sqrt(g_b^2 + e_N^2 + 2 g_b e_N mu)) (g_b + e_N mu), g_b = G M_sph / (r^2 a0).
- **E0, the no-field reading:** M = nu(g_b) M_sph.

Four graded cases: E1 canonical, E1 alt, E0 canonical, E0 alt, quoted in that order.

## Gate

The rows share tracers and data and no covariance exists, so no chi-square is formed. For each
class with at least three usable rows, the median pull z_med is graded: it says whether at least
half of the published measurements individually exclude the line at two sigma.

- **PASSES** if |z_med| <= 2.
- **FAILS LOW** if z_med < -2; **FAILS HIGH** if z_med > +2; "(beyond 3)" is added if
  |z_med| > 3.
- **NO POWER** for a class with fewer than three usable rows, or in which a mutation below does not
  bite.
- **FRAGILE** is appended to a class label if any of these pre-named variants gives a different
  label: rows with r >= 150 kpc only (evaluated only if that leaves at least three rows; otherwise
  skipped and said so); symmetric errors (the mean of the two sides for every row); a 10 per cent
  floor; a 30 per cent floor; dropping any single row.
- **Case label:** "H: ... / S: ...". Headline of a case: **PASSES** if both classes pass;
  **FAILS LOW** or **FAILS HIGH** if both fail the same way; **SPLIT** if the classes differ and at
  least one fails; if one class has no power the headline is the other class's label with the
  class named.
- **NO VERDICT** if a known-answer check below fails (the script stops before any graded number).

Reported, not graded: every row with its pull; the count of rows beyond two sigma; published errors
with no floor; the paper's own NFW extrapolation (`fig13/extrapolated-nfw-menc.csv`) through the
same gate; the set of field strengths e_N in [0, 0.05] for which both classes pass, per footing,
against the record's 0.01273 and the rotation curve's [0, 0.008]; the baryon amplitude A that would
centre each class under E1; the matched-field value of today's correction lane (4.94 / 4.95 x 10^11
at 200 kpc) against the rows at r >= 150 kpc; and row 32's kill as first registered (a measured
M(<200 kpc) >= 1.0 x 10^12), evaluated on the rows at r >= 150 kpc both on central values and at
two published sigma. That last item is a report; row 32's status belongs to its own record.

## Known-answer checks (all before any graded number)

| id | check | pass condition |
|---|---|---|
| KA1 | the file is the one named above | md5 equal |
| KA2 | units and reading of `fig13`: `desi-dr2-joint-menc.csv` against Table 4's All column | 13 values, each within 0.011 x 10^11 Msun |
| KA3 | the baryon model as ported | total within 0.1 per cent of 6.681 x 10^10; M_sph/M_b = 0.9777 at 30 kpc and 0.9972 at 80 kpc, each within 0.0005 |
| KA4 | the line reproduces the record | E0 at 80 kpc 5.691 / 6.219; E1 at 80, 150, 200, 300 kpc 4.977, 5.252, 5.264, 5.270 (canonical) and 5.109, 5.257, 5.266, 5.270 (alt), x 10^11, each within 0.5 per cent; E1 at 2000 kpc within 0.5 per cent of the closed form [nu(e) + e nu'(e)/3] M_b |
| KA5 | the statistic on synthetic rows | rows placed exactly on the line give z = 0 and PASSES; rows placed three total sigma above the line give z = -3 and FAILS LOW; five rows with pulls -4, -1, 0, 1, 4 give z_med = 0 |

## Mutations (each must bite in each class)

| id | mutation | must give |
|---|---|---|
| M1 | E1 with e_N = 0.05 (a plateau near 2.8 x 10^11), both footings | FAILS LOW |
| M2 | E0 with a0 multiplied by 16 (the flat speed doubled), both footings | FAILS HIGH |

Mutation runs write `plt1_mut.out`, never the graded output.

## What a label will and will not mean

The rows are published Newtonian enclosed masses. Several assume a halo form and are extrapolated
beyond their tracers; the compilation does not say which. The field reading's angle average is
exact only for tracers spread isotropically about the field direction, which the satellites are
not. A FAIL is against the published numbers with a 20 per cent floor and the McMillan census at
A = 1. A PASS is not a confirmation. A SPLIT that the paper's own NFW shares says the two classes
disagree with each other at these radii, whatever the model.
