# The universal 3 kpc law fails the isolated dwarf discriminator

The corrected reciprocal Gaussian law at the same ell=3 kpc used by the
Milky Way witnesses gives only **4/24 canonical** and **5/24 alternate**
passing isolated dwarfs, compared with **19/24** for plain isolated QUMOND
on each footing. No baryon prescription, mass-to-light range, sample cut,
dispersion cut, or acceleration footing changed.

This is an actual calculation of the corrected source-plus-outer operator.
It is not a transferred KT15 score. It is also not the actual satellite
external-field calculation: this first discriminator is exactly spherical
and isolated. The substantial deficit makes the two-system MW/Cassini pass
an inadequate basis for promoting this particular law as generally viable.

## Decisive original objects

Predicted global line-of-sight dispersions at the largest allowed
Upsilon_V=3 are:

| Object | Observed sigma (km/s) | Frozen 2-sigma lower limit | Canonical prediction | Alternate prediction |
|---|---:|---:|---:|---:|
| Fornax | 11.7 +/- 0.9 | 9.9 | 7.2782 | 7.4014 |
| Sculptor | 9.2 +/- 1.4 | 6.4 | 3.5409 | 3.5629 |
| Leo I | 9.2 +/- 1.4 | 6.4 | 5.3968 | 5.4144 |

These are the n=2000, base-domain values. The largest selected-object shift
under n=1000 versus 2000, doubled radial domain, or the independent Gaussian
mixture construction is **0.001127 km/s**, far below the discrepancies.
No larger stellar mass is permitted by the inherited range.

Moreover, each isolated prediction increases continuously with Upsilon:
the source field scales with M, the simple response magnitude A(g) increases
with g, the outer l=1 radial vector kernel is positive, and the Newtonian
variance is linear in M. Thus the three failures at Upsilon=3 exclude every
Upsilon in the continuous interval [1,3], conditional on the numerical
accuracy stated here, rather than only the 41 sampled values.

The finite 41-point population counts are:

| Numerical radial grid | Footing | Reciprocal 3 kpc | Plain isolated | Newtonian |
|---|---|---:|---:|---:|
| 1000 | canonical | 4/24 | 19/24 | 3/24 |
| 2000 | canonical | 4/24 | 19/24 | 3/24 |
| 1000 | alternate | 5/24 | 19/24 | 3/24 |
| 2000 | alternate | 5/24 | 19/24 | 3/24 |

The continuous endpoint-overlap test, justified by the monotonicity above,
gives the same 4/24 and 5/24 counts from the saved numerical endpoints.
The common passing objects are Andromeda IX, Andromeda III, Andromeda XV,
and LGS 3; alternate also passes Andromeda II. Some have very large observed
errors. All original Milky Way satellites in this sample fail the isolated
3 kpc model.

Both isolated counts meet the old numerical threshold of at most half the
plain isolated count. This report deliberately calls that a failure of the
isolated discriminator, not KT15's primary satellite-EFE grade.

## The operator actually computed

The original Plummer profile and mass assignment are retained:

```
rho(r)=3M/(4pi a^3) [1+(r/a)^2]^(-5/2),
a=R2,  M=Upsilon_V L_V+1.33 M_HI.
```

For spherical isolated input, the QUMOND phantom potential has radial
gradient A(g_source). Its outer Gaussian is applied as a vector convolution,
or equivalently by smoothing the scalar potential before differentiation.
Convolving the radial acceleration as if it were a scalar would be a different
operator and is not used.

The l=1 kernel and its stable implementation are derived in PLAN.md. The
virial observable is evaluated with the outer kernel moved onto the radial
Plummer measurement weight. This adjoint identity saves repeated convolutions
while preserving the source-plus-outer energy construction. The physical
Newtonian contribution is unsmoothed and contributes exactly
pi G M/(32a) to sigma_los^2.

An independent construction writes the Plummer density as a positive
exponential mixture of Gaussians. Gaussian source smoothing adds variances;
the smoothed virial vector weight includes the essential factor
sigma_source^2/(sigma_source^2+ell^2). This is independent of the l=1 kernel
implementation and agrees with it on the three selected objects.

## Numerical checks and their limits

The bounded run completed in 4.75 seconds with one numerical thread and
no randomness. Every predeclared check passed:

- Maximum Gaussian source mass discrepancy: 5.192e-5 relative.
- Maximum scalar Gaussian width-identity error: 4.945e-5 relative to its peak.
- Maximum vector Gaussian fifth-power amplitude error: 4.945e-5 relative
  to its peak.
- Independent Newtonian Plummer virial integral: 5.222e-5 maximum relative
  error; the physical predictions use the exact Newtonian term.
- Independent 256-node Gaussian-mixture predictions differ from the expanded
  l=1 convolution by at most 1.548e-5 km/s for the selected objects. Orders
  128 and 256 agree much more closely.
- Plain isolated control counts reproduce KT15's 19/24 on both footings.
  Selected archived Upsilon=1,2,3 dispersions differ by at most 0.00414 km/s
  over all objects; the new calculation extends the virial domain and uses
  the actual MW solver's physical unit conversions.

For each object and Upsilon, results also record the analytic upper bound
on the omitted outer phantom virial variance:

```
delta sigma_ph^2 <= sqrt(G M a0) [1-M_Plummer(R)/M]/3.
```

For the three focus objects its largest value is 0.02160 (km/s)^2 (alternate
Fornax at Upsilon=3). Even adding that entire bound changes its sigma by
less than 0.00146 km/s. This bound concerns the outer measurement tail only;
it does not certify all source truncation, integration, or continuum errors.
Those are checked empirically through resolution, domain, and independent
representation comparisons.

Only the three focus objects receive the expanded-domain and independent
mixture checks. All 24 receive n=1000 and 2000, Gaussian mass, and Newtonian
checks. These are finite numerical results with large margins for the three
highlighted failures, not interval-certified population likelihoods.

## Evidence and what remains

`contract.json` and PLAN.md preceded execution. `run_001/results.json`
contains every sampled dispersion, mass-to-light grid, grade, convergence
check, and tail bound. `run_001/manifest.json` completed and validates against
its before/after input hashes. The raw KT15 catalog, code, archived outputs,
and frozen criteria remain unchanged.

The next actual external-field test requires the same reciprocal operator
in a non-spherical background: construct the full vector source field,
evaluate A on that field, solve its longitudinal phantom projection, apply
the same outer Gaussian, and use the appropriate tracer virial observable.
The old one-dimensional substitution in nu alone is not that calculation.
No theorem that an external field must reduce every predicted dispersion
under this nonlocal law has been established here. The isolated failures
therefore do not stand in for a proved EFE upper bound.

The broader result is nevertheless substantive: the universal length that
earned a MW/Cassini witness has a severe new dwarf liability under the
original unchanged sample and baryon assumptions. A different response law
or a demonstrated resolution of this liability is needed before claiming
broad success; no hidden mass or dwarf-specific width was introduced.

## Independent review

The sibling reviewer reconstructed the l=1 kernel, Plummer Gaussian mixture,
adjoint virial normalization, and continuous-Upsilon monotonicity. REVIEW.md
reports no critical formula or normalization defect. Its bounded
`review/run_001/` audit completed with a validated manifest, replayed 11,808
stored grade comparisons, confirmed the original sample exactly, and compared
eight kernel values with independently integrated three-dimensional angular
expressions (maximum relative difference 1.35e-13). This independently checks
the kernel and scoring, not a second complete field solution. The verdict
retains the isolated spherical and empirical numerical-error qualifications;
no external-field upper-bound theorem is asserted.
