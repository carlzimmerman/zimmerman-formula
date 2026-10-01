# FGF-022: fixing the offset leaves a finite pressure ambiguity

With the exact synthetic bins and **offset fixed to zero**, the sharp closed
monotone pressure-family gradient interval is
**[-3.755809477804311e-6, -3.627360614306535e-6]**. Its width is
**3.485789560538283%** of the baseline gradient magnitude. Fixing this nuisance
alone therefore does not identify the finite gradient. These are dp/dx values
in the inherited normalized pressure coordinates, not gravitational forces.

Six selected offset bounds are certified below. Beta is a synthetic design
variable in Compton-y units, not authenticated calibration or uncertainty.

| beta | Minimum gradient | Maximum gradient | Width / baseline |
|---|---:|---:|---:|
| 0 | -3.7558094778e-6 | -3.6273606143e-6 | 3.48579% |
| 1e-6 | -3.7654545425e-6 | -3.6056760878e-6 | 4.33600% |
| 2.8093879085e-6 | -3.7829062059e-6 | -3.5664403678e-6 | 5.87436% |
| 5.6187758170e-6 | -3.8100029341e-6 | -3.5284484255e-6 | 7.64070% |
| 1.8298237703e-5 | -3.8100029341e-6 | -3.4496370858e-6 | 9.77945% |
| 3.6596475406e-5 | -3.8100029341e-6 | -3.4028341047e-6 | 11.04957% |

The unrestricted minimum and maximum are unique for this fixed rational
model. Their dual certificates each have four strictly negative inequality
multipliers. Any other optimum must set those same four pressure increments
to zero; exact elimination of those rows plus the twelve observation rows
recovers one vertex. Consequently **5.618775817022595e-6** and
**3.659647540638036e-5** are necessary and sufficient beta thresholds for
recovering the corresponding unrestricted gradient extrema. Exact rational
thresholds, including their slightly different decimal displays, are saved.

All twelve selected extrema have exact feasible primal vertices and exact
dual multipliers with zero objective gaps, stationarity residuals and
complementarity residuals. Verification uses Fraction elimination after the
floating LP chooses an active set. Direct pressure-coordinate H p=d checks
also pass. The source code explicitly reuses the pinned FGF-021 certificate
helpers; this is not an independent second implementation. Root review is
required. Wrong-cost dual controls fail as expected; baseline feasibility,
nested intervals and unrestricted recovery pass. No failed attempt occurred.

Across all beta>=0, feasible-set nesting proves the minimum is nonincreasing
and the maximum nondecreasing. Convex mixing proves the minimum is convex and
the maximum concave. This does **not** enumerate every breakpoint or certify
an interpolated table as the complete curve. Strictly positive/decreasing
profiles approach the extrema by mixing with the strict feasible baseline.

The surviving ambiguity is in the finite pressure coefficients. Calling it
outer-pressure freedom is a coordinate description conditional on the prior
invertible first-twelve-column block: outer-node choices then determine inner
coefficients. It is not a claim that changes physically reside only outside
the target aperture, nor a null direction of every original map pixel.

No actual-map gradient acceptance, noise model, covariance, instrumental
offset estimate, continuum gradient bound, force calculation or metric/photon
coupling is inferred. Both a0 normalizations, distinct vacuum/H histories and
Q/RAR/registered-M branches remain intact for any later density/composition
MOND bridge. The full gravity theory remains open.

The next discriminating input is a calibrated observable constraining the
remaining pressure freedom: additional outer annular SZ measurements with
their response and a justified support/background treatment, or an externally
calibrated map offset plus outer-pressure constraints. Outer annuli contain
projected pressure and cannot be assumed to measure pure background. Fixing
the offset perfectly is insufficient by itself, as this result demonstrates.
