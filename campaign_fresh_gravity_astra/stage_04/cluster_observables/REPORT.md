# Cluster observable checkpoint: two independent catalog matches restrict the gas correction

Two cached eROSITA catalogue entries provide a new cross-catalog test of the
stage-three nuisance explanation. At matched nominal apertures, both give LESS
gas than X-COP. A fixed-pressure, uniform gas-normalization explanation cannot
close the force residual anywhere in the explicitly declared error box, for
any of the 24 tested branch/object combinations. This is a **conditional
deterministic incompatibility**, not a confidence statement or a full
independent instrument likelihood.

The test advances beyond stage three's freely constructed calibration roots:
the gas normalization is now constrained by a different instrument's cached
reduction at two actual matched objects. The remaining pressure correction has
a quantitative independent-measurement requirement. Independence of raw
photons does not imply independence of emissivity, geometry, plasma or
deprojection systematics; those remain explicit limitations.

## Available observations and actual matches

The bounded search inspected the seven X-COP clusters with their own stellar
profiles, the cached eRASS1 primary catalogue, PSZ2 union catalogue, ACT+Planck
Compton-y map/mask/beam, and the schemas of four cached eRASS3-related FITS
products. It does not assert an exhaustive search of every file on the disk.
No data were downloaded and no literature mechanism was imported.

Matching was registered before calculation as nearest sky position within
5 arcmin and absolute redshift difference <=0.01. All nearest candidates,
including rejected ones, are preserved in `run_002/catalogue_matches.csv`.

| Cluster | eRASS identity | Separation | eRASS nominal R500 | eRASS/X-COP gas mass |
|---|---|---:|---:|---:|
| A644 | 1eRASS J081726.1-073013 | 0.3173 arcmin | 1331 kpc | 0.809282 |
| ZW1215 | 1eRASS J121741.5+033931 | 0.2044 arcmin | 1252 kpc | 0.843823 |

The other five nearest eRASS candidates are at least 256 arcmin away and are
rejected. A644 has the same catalogue redshift, 0.0704. ZW1215 has z=0.0773
in eRASS and 0.0766 in X-COP. The X-COP redshift is retained for the registered
H-scaling calculation; this does not assert that the distance reductions agree.

The comparison assumes the quoted kpc radii use a common distance convention
and compares X-COP's enclosed masses at the eRASS nominal R500 without
extrapolation. It does NOT compare each catalogue at its own R500 or insert
eRASS M500 as a direct gravitational measurement. Cosmology and exact angular
aperture equivalence are not authenticated by the available catalogue columns.
R500 errors are not silently propagated into a new aperture for which the
eRASS gas-mass profile is unavailable. These are load-bearing restrictions.
The catalogue's R500, gas mass and model-dependent mass proxy need not have
independent inference errors. Their full pipeline dependence is not
authenticated by the inspected FITS columns. Treating the quoted gas mass as
a reliable enclosed-mass constraint within the declared box is itself an
explicit input of this conditional test.

Other products are useful but do not provide a ready independent radial
pressure constraint:

* PSZ2 matches six clusters within 2.72 arcmin. ZW1215 is unmatched; its nearest
  PSZ2 source is 120 arcmin away at a different redshift. Y5R500 is an integrated
  pipeline quantity, with units 10^-3 arcmin². Neither Y nor its SZ mass proxy
  is a resolved pressure gradient or direct lensing acceleration.
* A2029, A644, A85 and ZW1215 lie inside the rectangular ACT+Planck map bounds.
  Their center mask values are 1, **0**, 1 and 1 respectively. Thus geometric
  coverage alone would falsely classify A644 as usable. A1795, A2142 and A2319
  are outside the rectangular coverage. A usable center does not establish
  usable surrounding annuli.
* The map has a cached beam, but the inspected products do not provide the
  joint foreground/noise/cross-product covariance and independently reduced
  matched-shell pressure gradient needed here. ACT+Planck and Planck PSZ2
  cannot be treated as independent measurements simply because they are
  different files. Independence from inputs of the original hydrostatic
  reduction also requires its actual pipeline provenance/covariance.
* Four eRASS3-related schemas were read directly. They contain no columns named
  KT, MGAS500, M500, TEMPERATURE, PRESSURE or DENSITY. They supply no ready
  replacement for the two matched eRASS1 thermal measurements in this test.

## Direct coupled test

Adopt the stage-three assumptions: spherical conventional gas inertia, fixed
distance and angular aperture, unchanged gas-profile shape with density ratio
eta, and unchanged stellar mass-to-light convention. Let p be the thermal
pressure-gradient ratio, equal to the pressure normalization ratio when its
shape is fixed. Then

    Bnew = eta Bgas + Bstar,
    gH,new = (p/eta) gH.

Write Me for eRASS gas mass, Mx for original X-COP gas mass, Ms for X-COP stellar
mass, Mh for the original hydrostatic-equivalent M_FORW, and C=G/r² with mass
units converted to SI. The uniform-normalization interpretation gives
eta=Me/Mx, hence equality to the gravity branch requires

    p_required = (Me/Mx) F(C[Me+Ms];a)/(C Mh).                (1)

This changes both the baryonic source and inferred thermal acceleration. It
does not re-use a Newtonian missing mass. The core scale remains
`a=kappa c sqrt(G rho_Lambda)`, kappa adopted. Q, exponential R and inherited
monotone M are evaluated separately at both 9.3619e-11 and 1.1279e-10 m/s²,
with constant vacuum scaling and the separate H(z) comparison branch.

For positive inputs and monotone F, (1) increases with Me and Ms and decreases
with Mx and Mh. Its maximum over a rectangular box is therefore exactly the
corner `(Me_high, Mx_low, Ms_high, Mh_low)`. All 16 corners were independently
enumerated as a finite check of this analytic result, for every branch.

The declared box uses eRASS MGAS500_L/H as endpoint masses; X-COP MGAS_LO/HI as
error magnitudes about MGAS; MSTAR_LO/HI as endpoint masses; and EM_FORW as a
symmetric error magnitude about M_FORW. Central masses and errors are separately
log-interpolated to the nominal aperture. These interpretations match the
numerical conventions of the supplied columns, but a fully authenticated
probability interpretation is unavailable. In particular MGAS_LO is NOT used
as a tiny lower endpoint mass. The box is a one-quoted-error-unit stress test,
not a joint confidence region. No Gaussian significance, priors or independence
of its axes is asserted.

| Quantity | A644 | ZW1215 |
|---|---:|---:|
| Gas-normalization range in declared box | 0.773059–0.842136 | 0.824500–0.864116 |
| Canonical vacuum R: central p_required | 0.550230 | 0.369350 |
| Canonical vacuum R: p_required box | 0.485392–0.620265 | 0.341013–0.401297 |
| Largest p_required allowed by ANY registered branch and its box | **0.683930** | **0.443039** |
| Canonical vacuum R: required temperature ratio if its shape also rescales uniformly | 0.679899 | 0.437710 |

Thus p=1 is outside every tested box. This rules out the **fixed-pressure,
uniform-density-normalization explanation within this explicitly conditional
comparison**. It does not rule out a pressure change, correlated systematic
error outside the box, different radial density shape, or mismatched distance
and aperture conventions.

The eRASS temperatures are 7.66 keV (listed endpoints 5.92–10.29) and 3.80 keV
(3.47–4.65). They are retained as catalogue measurements, but the cache lacks a
matched original temperature profile and its response/weighting. Dividing
these aperture spectral temperatures by a temperature reconstructed from
M_FORW would not supply the missing independent local thermal test. No such
comparison or temperature significance is claimed.

## Quantitative requirement for the next measurement

A genuine independently calibrated pressure-gradient ratio with a lower bound
above **0.683930 for A644** or **0.443039 for ZW1215**, at the same aperture and
within the density/geometry assumptions, would reject every registered
density-plus-pressure normalization explanation inside the stated mass box.
For a hypothetical measurement centered exactly at p=1 with a guaranteed
fractional interval `[1-delta,1+delta]`, sufficient widths would be
delta<0.316070 and delta<0.556961 respectively. These are required bound widths,
not claimed measurement errors or significance levels.

Alternatively, holding p=1 requires multiplying the eRASS gas mass itself by
an additional factor b. For canonical vacuum R, the central required b is
**1.478557 / 1.906390** (A644 / ZW1215). Even the favorable error-box corner
needs **1.368221 / 1.808739**. For fixed distance, angular shape and X-ray counts,
the emission relation `S_X proportional to n² Lambda` gives

    b = ell^-1/2,  ell = Lambda_new/Lambda_eRASS.

Canonical central closure therefore requires ell=**0.457429 / 0.275154**.
Across all branches and all favorable box corners, the largest closing
emissivity ratio is **0.605706 / 0.345567**. An independently justified lower
bound on ell above those values would reject this emissivity-only escape
under fixed pressure/distance and the stated box. No plasma or detector model
has established such a bound in this run; temperature-dependent emissivity
cannot be silently held fixed in a physical thermal correction.

The exact branchwise requirements are in `run_002/closure_requirements.csv`.
`check_pressure.py` implements interval intersection against them for a future
actual pressure-gradient measurement. It requires explicit same-aperture,
distance, uniform-density and independent-provenance declarations. Those
declarations must be audited, not trusted merely because the program accepts
the JSON. Three explicitly synthetic controls verify rejection below/above
and acceptance inside the canonical R interval; they are not observations.

## Why reconstructed thermal quantities can be circular

If a proposed pressure profile is built from the existing hydrostatic result,

    P(r)=P(R)+integral_r^R rho(s) gH(s) ds,

then differentiating returns `-P'(r)/rho(r)=gH(r)` identically. Re-inserting
that pressure into the force test adds no independent information, regardless
of the numerical precision of the integration. The unknown pressure zero
point P(R) changes temperature and integrated SZ signal while leaving the
inferred gH unchanged. A new pressure/temperature datum needs a genuinely
independent observation map and matched weighting to constrain this family.

Likewise, constructing FGAS=MGAS/M_NFW or YX=KT*MGAS and then treating the
constructed quantity as an independent constraint duplicates its inputs. The
actual catalogue central values agree closely, though not exactly, with these
algebraic relations: the two eRASS YX/product ratios differ by 0.0965% and
0.1318%, and FGAS/mass-ratio values differ by 0.666% and 0.555%. X-COP FGAS
agrees with MGAS/M_NFW to median relative differences below 0.19%, with a
maximum discrepancy 2.38% across the inspected bins. These near-identities
are consistency diagnostics, not proof of exact pipeline provenance; separate
posterior summaries and interpolation can differ. No extra independent
precision is inferred from them. SZ mass proxies and model-dependent M500
likewise are not treated as direct force or lensing measurements.

## Execution, audit and remaining implication

The authoritative result is `run_002/manifest.json` at frozen Git base
`eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`, dirty shared checkout. It records exact
input SHA-256 values before and after execution, including the catalogue,
profile, map, beam and compressed release files; all six scientific outputs
are hashed. Code resides entirely in this lane; accepted stage-three functions
are imported read-only with bytecode writes disabled. No old files or other
research lanes were edited and no commit was made.

Run 002 completed in 12.90 seconds. Python 3.13.9, NumPy 1.26.4, SciPy 1.14.1
and Astropy 7.2.0 were used with a 180 s wall limit, 150 s per-process CPU limit,
1 MiB log cap and cooperative one-thread numerical-library cap. No memory or
affinity cap and no randomness are claimed. All 48 closure roots forward-check
to <=1.83e-14; all corner extrema agree exactly. The evidence manifest validates
against current inputs and outputs. This is finite binary64 verification and
mathematical self-review, not an independent scientific referee verdict.

Run 001 failed because the WCS API returned zero-dimensional NumPy arrays
that Python round() would not accept. Explicit scalar conversion fixed this
inventory-only implementation error. That failed run is retained and is not
counted as evidence; its old code hash is superseded.

Reproduce into a fresh output directory from the repository root:

```sh
/opt/homebrew/Caskroom/miniconda/base/bin/python campaign_fresh_gravity_astra/stage_04/cluster_observables/run.py run_003
```

Execute the next genuinely measured pressure test after supplying audited JSON
in the schema documented in `check_pressure.py`:

```sh
/opt/homebrew/Caskroom/miniconda/base/bin/python campaign_fresh_gravity_astra/stage_04/cluster_observables/check_pressure.py /absolute/path/to/actual_pressure_bounds.json --out /absolute/path/to/pressure_comparison.json
```

The first unresolved implication is the common-distance/angular-aperture and
uniform-density-shape link between these two catalogue gas masses. Next is an
independently reduced thermal pressure gradient or emissivity constraint with
the actual response and shared-data covariance. The current result specifies
how strongly those quantities must change; it does not establish that either
change is physically plausible or that the general cluster discrepancy is
resolved. Three narrow follow-up task cards are in `NEXT_TASKS.md`.
