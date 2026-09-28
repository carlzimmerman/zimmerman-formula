# FGF-012 independent raw-catalog audit

**Outcome: supports_scoped_claim.** The nominal-aperture, fixed-distance,
uniform-density-shape conditional calculation is reproduced from the raw local
FITS/TSV inputs. This is an Astra audit by `/root/catalogue_audit`, not a DeepSeek
run, a detector likelihood, theoretical closure, or a novelty claim. Promotion
requires a separate orchestrator review pinning `result.json`.

## What was independently established

All **45** source paths pinned by the task and the original run manifest match
their expected SHA256 hashes. This authenticates byte identity to the supplied
premises, not upstream catalog calibration or scientific semantics. The
source check includes the large map, mask, beam and four compressed FITS
catalogs, even where only headers/schema or mask pixels enter this audit.

Haversine matching implemented independently of the original SkyCoord call
selects exactly two eRASS objects under the registered <=5 arcmin and
|delta z|<=0.01 gate. All seven nearest neighbors, including every rejection,
are preserved in `numeric_001/matches.json`. Each matched object has exactly
one eRASS row satisfying the full gate.

| X-COP name | eRASS zero-based row | Identity | Separation, arcmin | X-COP/eRASS redshift |
|---|---:|---|---:|---|
| A644 | 7035 | em01_126099_020_ML00003_010_c010 | 0.3173147440323242 | 0.0704 / 0.0704 |
| ZW1215 | 9149 | em01_185087_020_ML00003_003_c010 | 0.20437371504819948 | 0.0766 / 0.0773 |

The five rejected eRASS nearest neighbors are 256.5–4237.7 arcmin away. PSZ2
has six accepted matches; ZW1215 remains unmatched. Maximum separation
roundoff difference from the original result is 2.2737367544323206e-13 arcmin.

Mass parsing uses the actual FITS units, converts each R/R500 radius with its
own FITS R500 header, and independently evaluates piecewise power-law
interpolation. It does not import the worker's load/rad/col/interp/xc_bounds
helpers. Both apertures lie within every required raw profile's support.
`masses_and_apertures.json` pins the individual supports, bracketing row
indices and physical radii, metadata and all four mass boxes.

| Quantity | A644 | ZW1215 |
|---|---:|---:|
| eRASS nominal aperture, kpc | 1331 | 1252 |
| eRASS gas mass, solar masses | 6.7184e13 | 6.2832e13 |
| X-COP gas mass there, solar masses | 8.30168432458238e13 | 7.446107952124134e13 |
| Enclosed gas ratio | 0.8092815550822541 | 0.8438233826851257 |
| Ratio bounds in registered box | 0.7730586–0.8421361 | 0.8245000–0.8641157 |
| Maximum p_required over all branches/boxes | **0.6839299192843087** | **0.44303907891275407** |
| Maximum closing emissivity ratio over favorable corners | 0.6057063459733419 | 0.3455667268614069 |

The force calculation independently implements Q and R and the pressure/source
transformation derived in `DERIVATION.md`. M uses the pinned registered
implementation, as required; this run does **not** independently validate that
kernel's numerical table. Both a0 values and distinct vacuum/H histories are
present for all three kernels: 24 branch/object cases, 16 box corners each,
and 48 gas-boost roots. Bisection is independent of the worker's Brent root
solver. Largest compared value difference is 2.3092638912203256e-14; maximum
root forward residual is 4.440892098500626e-16. Every corner extremum agrees
with the independently derived monotone direction, and every ceiling is below
one. Interpolating endpoint masses instead of separately interpolating central
mass and error shifts the upper pressure ceiling by at most 0.010396%; this
specific interpolation sensitivity does not remove the conditional discrepancy.

At fixed pressure, no uniform gas normalization **inside these mass boxes**
closes the force. Correlation inside a subset of the rectangular box cannot
raise its ceiling, but neither joint coverage nor unknown systematic bounds
has been established. This deterministic statement has no confidence level.

## Aperture and measurement gaps remain load-bearing

The test compares the same **nominal numerical kpc radius**, not authenticated
common angular apertures/cosmology. Equal radius units do not supply the
conversion history or a common center. A644's gas/hydro FITS R500 is 1250 kpc;
the auxiliary JSON lists 1230 kpc, and the eRASS aperture is 1331 kpc. The
calculation correctly uses the FITS value for its own R/R500 profile, rather
than silently replacing it with another mass-model radius. The analogous
ZW1215 FITS value is 1358 kpc, compared with eRASS 1252 kpc.

The eRASS RA_XFIT/DEC_XFIT centers are separated from the X-COP centers by
0.52830 arcmin (A644) and 0.12522 arcmin (ZW1215), distinct from the catalog
matching coordinates. This audit does not establish which center/geometry
was actually used to infer each gas mass. The nominal eRASS radius endpoint
ranges are 1309–1364 and 1230–1285 kpc. Their covariance with gas mass and mass
proxy is unavailable; moving to those endpoints would require an eRASS radial
gas profile. The audit therefore does not invent an aperture-error correction.

Numerical ordering supports the registered endpoint/error conventions, but
FITS names and units do not authenticate posterior coverage, correlations,
emissivity, deprojection, selection, spectral fitting or M500-proxy dependence.
The original hydrostatic-equivalent M_FORW is an input to the conditional
thermal-force interpretation, not an independently verified direct gravity
measurement. The eRASS gas masses and temperatures are reductions, not raw
photon likelihoods. No likelihood independence follows from different files
or different instruments.

The mask control reproduces A644's center value zero despite rectangular map
coverage. A2029, A85 and ZW1215 have center value one; other three centers lie
outside the map bounds. Map and mask WCS coordinates agree at inspected
centers. No surrounding annulus coverage, beam deconvolution, foreground/noise
covariance or resolved pressure profile was recovered. The four compressed
catalog schemas contain no named direct thermal columns in the registered
schema test; this is not a statement about every possible local data product.
PSZ2 integrated Y is not a local pressure derivative. ACT+Planck and PSZ2
share Planck information; actual cross-product and X-COP dependencies remain
unreconstructed. Recomputed FGAS and YX algebraic diagnostics support treating
them as potentially dependent summaries; near-equality does not prove exact
pipeline construction.

## Adversarial control: enclosed mass alone is insufficient

For canonical vacuum R, one can keep the observed enclosed gas ratio while
holding pressure fixed and choose the following positive density multipliers:

| Object | Inner region (95% of original gas mass) | Outer region (5%) |
|---|---:|---:|
| A644 | 0.7744644516 | 1.4708065217 |
| ZW1215 | 0.7679921010 | 2.2846177352 |

The outer multiplier is gH/F at the nominal boundary. The inner multiplier
preserves the enclosed mass exactly. The resulting boundary force equality
holds with p=1. All 24 analogous registered-branch constructions have positive
inner multipliers (minimum 0.7563215230) and match the target enclosed mass and
local force to <1e-14. This falsifies an extension from these enclosed masses
to arbitrary density shapes. It does not falsify the original uniform-shape
conditional result, fit a resolved image, establish global hydrostatic balance,
or make the two-zone profile a physical explanation. A smooth transition can
replace the step with a small compensating change in inner normalization;
positivity has ample margin.

## Execution and acceptance scope

Setup was timestamped 2026-09-27T18:46:07Z. The numerical child started
2026-09-27T18:50:41.375983Z and completed successfully in 12.646181 seconds.
The runner actually imposed 120 s wall, 110 s per-process CPU and 1 MiB logs,
with cooperative one-thread library variables. No memory or affinity cap was
requested or claimed. Python 3.13.9, NumPy 1.26.4, SciPy 1.14.1 and Astropy
7.2.0 ran on macOS arm64; runner Python was 3.9.6. No random sampling occurred.
No failed numerical attempt occurred in this audit. A preparatory schema read
used subprocess timeout=120 and one-thread environment settings, but is not
used as the load-bearing evidence: the recorded audit rereads the actual data.

`numeric_001/manifest.json` records actual argv, before/after input hashes,
output hashes, Git/dirty state, bounds and completion. It validates against
current inputs and outputs. Exact reproducible argv is also saved in
`execution_argv.json`; regeneration must choose a fresh runner output directory.
`result.json` hashes all returned artifacts and provides the task contract.

Mathematical proofreading self-review covered the newly authored DERIVATION.md
and this audit only: no mathematical-token corrections or unresolved notation
issues were found. This proofreading is not an independent proof referee.

The next discriminating empirical task is to authenticate the same angular
aperture, center and distance conventions and obtain an independently reduced
local gas-density/thermal-pressure gradient with its response and shared-data
covariance for these two objects. If only integrated gas masses remain
available, retain the uniform-shape assumption explicitly and stop short of
an empirical exclusion. No theory closure or novelty is claimed.
