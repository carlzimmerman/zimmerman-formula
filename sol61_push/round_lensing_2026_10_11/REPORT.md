# Round-profile lensing: a physical constraint on the reservoir

2026-10-11. This is a necessary-condition calculation, not a candidate-B fit.
The global theory goal remains open; kappa=1/2 remains fitted.

## Question and data

Can positive circular projected profiles at three observed BCG centres, or
six observed galaxy centres, reproduce the 135 gold image positions?
The raw catalogues come from the [authors' public lensing release](https://niriss.github.io/lensing.html)
for [Rihtarsic et al.](https://arxiv.org/html/2601.22245v2).
Only observed coordinates and source redshifts enter the fit. No published
halo mass, fitted radial profile or mass map enters it. Source file hashes and
individual download URLs are in sources/provenance.json. The gold catalogue
agrees with the independently obtained CDS rows. Six member IDs, 1/3/4/5/9/10,
were fixed before fitting. Gas and other members are not separate components.

The finite circular-profile representation is exact at the sampled radii:
nonnegative increments of enclosed projected mass correspond to positive
annuli between consecutive radii. See PROJECTION_PROOF.md. This freedom is a
relaxation for bounds, not an extra freedom proposed for the theory.

## Completed projected-density calculation

The original run passed 32/32 checks. Both three- and six-centre models achieve
zero minimum source-contrast residual, within floating-point precision, in
each of the two separately labelled backgrounds. The minimum-mass follow-up
uses a residual allowance of 1e-7 arcsec solely to break numerical ties.

| Background | Centres | Angular mass coefficient at this allowance |
|---|---:|---:|
| Native PM flat geometry | 3 | 13767.748706 |
| Native PM flat geometry | 6 | 5413.333125 |
| Author reference, context only | 3 | 13549.630261 |
| Author reference, context only | 6 | 5347.231502 |

Units are arcsec squared in the deflection coefficient, not solar masses.
The projected-density run checks minimax duality and feasibility of the
minimum-mass solution; it does not independently certify the latter's dual.
These distance scenarios are NOT the two a0 footings, and neither kernel nor
a0 was imposed. The 172 scalar source contrasts are algebraic constraints,
not 172 independent statistical measurements. Their infinity norm depends on
the declared Helmert basis. Image-plane error bars cannot be applied to it.

## Why three-dimensional positivity matters

A spherical shell outside an aperture projects some mass into that aperture.
For every positive spherical three-dimensional profile and Ri<Rj,

`M2D(Ri) >= [1-sqrt(1-(Ri/Rj)^2)] M2D(Rj)`.

The coefficient is sharp. The proof is in PROJECTION_PROOF.md. All these pair
bounds are necessary; their sufficiency for a positive deprojection has not
been proved. Thus even passing them does not establish a physical halo.

The first full-row solve exhausted its frozen 60 CPU-second cap. Its manifest
and empty logs are preserved in spherical_run; no optimum was obtained.
The separately frozen CUT_CRITERIA.md changes execution to constraint
generation, checking every omitted row and lifting dual multipliers by zero.
The continuation completed with **86/86 checks**, including shell controls,
deliberately invalid projected annuli, an omitted-cut mutation, the direct
small-LP comparison, all-row primal feasibility, dual signs/columns/gaps, and
both solver tolerances in every cell. Its hashed manifest validates. The
original projected run and the resource-limited run also have valid provenance
records; provenance validation does not turn the resource failure into a pass.

| Background | Centres | Minimum contrast residual (arcsec) | Angular mass at minimum + 1e-7 |
|---|---:|---:|---:|
| Native PM flat geometry | 3 | 0.1692960718 | 10942.539865 |
| Native PM flat geometry | 6 | 0.0526688329 | 19489.946991 |
| Author reference, context only | 3 | 0.1670724210 | 10800.784363 |
| Author reference, context only | 6 | 0.0502069400 | 19456.768095 |

These are the 1e-10 solver-tolerance results. At that tolerance the largest
minimax primal violation is 3.05e-9 and absolute primal/dual gap is 5.86e-15.
Mass-objective dual gaps satisfy the separately frozen relative tolerance.
The mass columns in the two tables use DIFFERENT allowed residuals and must
not be interpreted as an increase/decrease in the physical mass requirement.

The finding is narrow but useful: even necessary spherical positivity removes
the exact-fit freedom of these selected circular-centre configurations. At
exact positions their unrestricted positive projected profiles can interpolate
the data, whereas the strengthened cones cannot. This is not an observational
exclusion, a proof about every cluster geometry, or a cold-energy identification.
Full outputs and numerical certificates are in cuts_run. Every shape row is
checked, including rows omitted from the optimizer's active constraint set.

## Connection to Claude's new CFG629 result

CFG629 reports that adding an unsettled reservoir changes the main-cluster
aperture fraction from about 0.33/0.36 to 0.84 on its two footings. That number
uses a placeholder NFW c=4 profile and provisional recalled lensing masses;
it is not a derived reservoir prediction. Its isolated small-subcluster supply
is only 0.71 of the provisional aperture mass. Interpreting this as a necessary
increase in that subcluster's own mass requires separating projected mass from
the main cluster and other structures. The raw multi-centre calculation here
is useful precisely because it need not assign an aperture to one host first.

Consequently, the older shortfall cannot by itself establish that the law
fails. Nor does reinstating an assumed reservoir profile establish success.
Do not use these relaxed fits to calibrate a new free concentration parameter.

## Next discriminating calculation

Use measured baryon components to compute the repaired-kernel settled term,
then subtract its predicted deflection in the SAME raw-image operator. The
remaining target must be supplied by a nonnegative unsettled component with
an explicitly accounted shared mass budget. Before choosing a radial template,
ask whether any physically permitted reservoir can meet that residual target.
Apply the two fixed a0 footings separately. An LP lower bound can diagnose
incompatibility of a declared reservoir class; feasibility alone cannot derive
its dynamics, its carrier, catchment ownership, or settling rate.

An observational verdict additionally requires the image-position likelihood,
astrometric covariance and full component accounting; exact point matching
does not test extra images, magnifications or time delays. Existing sealed
predictions and Claude's lane are unchanged.
