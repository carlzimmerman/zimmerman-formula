# Independent extent-control review

**Verdict: computationally verified only in the declared finite range.**
The target is the 408 cases in `../extent.py`: 17 observed-radius support
cuts, three prescribed heights, two annular resolutions, two inherited
acceleration footings, and one/two quoted-error boxes. The published stellar
baseline remains fixed at M/L 0.5. This supplement leaves `AUDIT.md` and
`PROVENANCE.json` unchanged.

## Certificate signs and independent checks

The stated sufficient exclusion certificate is correct. If `M*x<=b`,
`x>=0`, `u>=0` and `M^T*u>=0`, then `0<=u^T*M*x<=u^T*b`; hence a negative
`u^T*b` is impossible. Normalization to sum(u)=1 is optional.

Reconstructed all 102 matrices and all 408 constraint systems. All 190
saved successful cases independently solve successfully, reproduce the
minimum masses exactly in binary64, and have primal residuals at most
2.64e-11 (km/s)^2. This uses the same SciPy/HiGHS library with independently
assembled constraints, not an independent optimization library.

The raw author statuses are 190 optimal, 198 infeasible and 20 status4.
The 198 saved negative certificates and 20 separately computed dual
certificates were checked using exact `Fraction` arithmetic on the
reconstructed binary64 coefficients. Only 30 raw certificates have exact
nonnegative column signs; small negative roundoff entries cannot certify
an unbounded nonnegative-variable domain by themselves.

For every one of the 218 certificates, a tiny exact correction resolves
this issue. Set `v=max(u,0)`. The upper-inequality row at the largest target
radius is strictly positive in every column of these finite matrices.
Add `t` times that row's coordinate vector to v, where t is at least the
largest exact column deficit divided by the corresponding positive row
entry. The code adds a factor 1.000001 when t is positive. All corrected
column signs and negative objectives are then verified exactly. Dividing
the corrected vector by its positive sum gives a normalized certificate.

All 218 corrected certificates pass. The largest added weight is
1.69226e-13. The smallest remaining absolute negative objective is
1.405256883213339 (km/s)^2. The source primal status4 values remain
unchanged; their 20 separate exact negative certificates establish
exclusion for these finite matrices. No unresolved smaller tested cuts
remain in the summaries below.

## First feasible support cuts among the 17 tested values

| Footing / error box | First feasible cut, kpc |
|---|---|
| Canonical, one quoted error | 6.15 for quarter-beam bins; 5.67 for eighth-beam bins; all three heights |
| Canonical, two quoted errors | 4.25 for all six height/resolution controls |
| Alternative, one quoted error | 5.67 for all six controls |
| Alternative, two quoted errors | 3.30 for five controls; 2.84 for twice-height/eighth-beam control |

Every smaller **tested cut in its own declared finite basis** is excluded
by the exact finite-matrix certificates. In particular, all 18 canonical
two-error cases at 2.84, 3.30 and 3.78 kpc are excluded, with corrected
negative objectives from -336.403 to -30.7742 (km/s)^2. The first numerical
positive witnesses at 4.25 kpc reproduce for all six controls.

These are tested support-cut results, not a continuum lower bound on a
physical remnant radius. Equal-width bases change with support cut and
need not be nested. Certificates are exact for the pinned binary64
matrices saved in `extent_run001/matrices.npz`; the continuous Newtonian
quadrature, untested cuts, other source geometries and between-target
forces have not received an exact enclosure. Positive finite witnesses
remain nonunique. The population/deprojection bridge for stellar
calibration remains missing, and no lifetime follows.

## Run and provenance

`extent_run001/manifest.json` completed and validated against current
inputs; the author `../extent_run/manifest.json` also validated. This was
a bounded, deterministic one-thread run with CPU/wall/output caps and
nominal memory below 1 GB; unsupported memory/affinity enforcement was
not requested. Exact commands, versions and result hashes are in the
manifest. `EXTENT_PROVENANCE.json` pins the raw source, outputs, independent
code, matrices, report and preserved earlier audit files.
