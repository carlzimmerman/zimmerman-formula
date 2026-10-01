# FGF028 independent response-construction audit

**Primary verdict: computationally verified only in a stated range.** The candidate implements the declared finite response construction consistently with the inherited model. Code review covers its fifteen pressure hats and all fifteen annuli; one independently integrated outer pressure column verifies the end-to-end numerical response to near machine precision. This is scoped finite-response evidence, not an authenticated full instrument calibration or an observed pressure-gradient measurement.

Auditor `/root/metric_intake`, 2026-09-30. Scope authorized exclusively under `campaign_fresh_gravity_astra/stage_13/response_audit/`. The inherited FGF019 projector was read, never imported at top level. The new FGF028 source, declared model and outputs were inspected after availability. A checklist and quadrature order/tolerance were saved before executing the independent check. Root separately owns the full exact-information/sensitivity computation; its small proof/code/record received the limited review below without another run.

## Response model and construction review

The source is the inherited ZW1215 center (184.42191 degrees, 3.6557217 degrees), target radius 1252 kpc, z=0.0766 and added fiducial flat-distance conversion H0=70, Omega_m=.315, Omega_Lambda=.685. The resulting DA=299.1293131965726 Mpc and theta_target=0.004185480809689986 rad match the old geometry. The radius is spherical angular separation divided by this fixed angular scale, not a flat radial approximation. The pressure model has fifteen free linear hat amplitudes, final p(5)=0 and zero pressure beyond x=5. Its physical interpretation remains electron pressure; total thermal pressure and force require additional conversion/data.

The segment projector evaluates 2 integral p(sqrt(t²+l²))dl through the primitives sqrt(s²−t²) and [s sqrt(s²−t²)+t² asinh(sqrt(s²−t²)/t)]/2. The lower radial limit is max(a,t), and a segment contributes only when t<b. The t=0 code gives the proper s²/2 second primitive without division by zero. Adjacent rising/falling segments correctly construct each pressure hat; the first hat has only its falling segment, and the last free hat at x=4 falls to zero at x=5. Factor two and support endpoints are retained.

Projection uses actual map-pixel WCS positions on the same 512-square patch, origin [42413,7743]. Map/mask shapes agree; the candidate compares their center and corner WCS. Our check independently reprojects four corners and center through both WCS objects and finds zero pixel discrepancy. The source-support boundary x=5 lies inside the patch: its minimum edge radius is approximately 8.830269576 target radii.

The beam operator uses longitude pixel angle times cos(center declination) and latitude pixel angle, both in radians. The frequency axes use their respective spacings, ell=2pi sqrt(fx²+fy²), the cached transfer interpolation and declared zero above ell=17000. It zero-pads the 512 image to 1024, convolves through a real FFT, then takes the centered 512 crop. The cache has transfer1 at ell0. This is consistent with the stated tangent-plane finite convolution; it is not an exact spherical instrument response. In particular, fixed padding with a sharply cut transfer is a declared finite periodic approximation; source containment alone does not bound long beam tails or padding error. No such error bound is claimed here.

The three added bins are exactly [2,3), [3,4), [4,5). Every bin selects finite map and finite positive-mask pixels, then uses mask/sum(mask). The map values themselves are used only for valid-pixel selection in this run, not to fit a pressure profile. The identical weights average each convolved basis. Empty/fully masked bins cause a saved failure, rather than a silent zero row. This is the inherited pixel-weighted annular mean, not an asserted solid-angle integral with fractional boundary pixels.

A post-convolution additive map background has response column one because each bin weight sums to one. This offset fact is distinct from how a zero-padded constant source would convolve. The candidate assumes the offset is fixed and subtracted; no actual background calibration has been supplied.

## Changed-implementation control

The candidate recomputes all fifteen pressure columns on the old twelve annuli and compares them with the pinned old matrix. Its saved record reports **bitwise equality**, zero absolute and relative difference. It then combines the original pinned twelve rows with the new outer rows rather than silently replacing the old operator. This controls implementation changes but shares the inherited physical approximation and much of its projection arithmetic; agreement alone would not constitute an independent physical validation.

## One independent discriminating computation

The reviewer executed exactly one bounded end-to-end check, `check_response.py`, for pressure basis index14 at x=4. It derives that hat directly as p(r)=r−3 on [3,4] and 5−r on [4,5], integrates each positive line-of-sight segment with 32-point Gauss–Legendre quadrature and doubles it. It does not call the candidate's or parent's Abel primitive. Angular radii use an independent atan2 of spherical cross-product magnitude and dot product. The declared beam/padding model is then applied with NumPy FFT and independently reconstructed normalized pixel weights.

The predeclared response tolerance was absolute1e−10 plus relative2e−9 times each reference entry. No refinement was needed. Maximum absolute discrepancies were:

- first twelve inherited responses: **1.3322676295501878e−15**;
- three new responses: **8.881784197001252e−16**.

All fifteen independently reconstructed normalized weight arrays have exactly the same hashes as the candidate arrays. The new annuli respectively contain 13036,18240,23474 valid pixels, all with mask1; their raw mask sums equal these counts and normalized sums equal one to the declared numerical tolerance. Thus the added bins are nonempty in this cache and share the expected weighting. Pixel count and unmasked coverage do not measure the number of independent noise samples.

This checks one pressure basis column across the entire measurement set. It does not independently recompute all fifteen columns, authenticate external beam calibration, prove continuum convergence or vary source support/grid/beam assumptions. No additional independent computation was executed because this discriminating check passed.

## Bounded record and provenance

The saved `run_001/manifest.json` records the actual command, Python3.13.9, NumPy1.26.4, SciPy1.14.1 and Astropy7.2.0 declarations, input hashes, limits, status and output hashes. It pins the actual cached map/mask/beam, inherited model/geometry, candidate source/response/geometry and checklist/check code. The run completed with exit0 under a 120-second wall bound, 110-second per-process CPU bound and cooperative one-library-thread environment; no memory cap is claimed. Manifest validation returned `valid evidence record; mathematical interpretation requires review`.

The exact hashes in `audit_result.json` include the run's validated input pins, saved output and the additional proof/code records reviewed. No old top-level script was imported and no other research scope was written. Scientific source ancestry and a passing hash check are distinguished from calibration authentication.

## Limited proof/code review of root's target and offset audit

The separately pinned `stage_13/target_audit/DERIVATION.md`, `check.py` and result/manifest were inspected without rerunning their computation. The exact rational full-transpose solve U^T r=L^T is a valid alternative to block elimination; the direct rU=L assertion certifies target reconstruction in the stored fixed-offset matrix. All seven declared nonempty subsets of the three added rows are tested before/after appending L, and the code constructs strict two-sided feasible null witnesses for the nonidentifying subsets. Root's recorded result says all singles and pairs fail and all three identify the target. This limited review accepts the finite algebraic implication, not a physical response or uncertainty model on that basis alone.

The deterministic componentwise error bound |delta g|<=epsilon sum|r_i| is exact for the stated box and is attained by delta y_i=epsilon sign(r_i). Recorded l1 gain is 50.26948356094382 in raw Compton-y bin units for the dp/dx target. This is not a measured noise level or probability statement. The common additive-offset sensitivity is sum r_i=−0.028902247822995483. Candidate and root use different declared synthetic epsilon examples (1e−8 and 1e−9 respectively); this is not disagreement about the shared amplification coefficient.

The relaxed-offset negative control is algebraically correct: with v=−U^-1 ones, the direction (delta p,delta b)=(v,1)t preserves all fifteen modeled bins, while L v=−sum r_i is nonzero. The script halves the minimum positive nodal-difference margin per absolute directional change and verifies both signs preserve positive decreasing profiles and all bin values. This is an exact conditional counterexample to removing the fixed-background premise. It does not infer an actual offset, contradict fixed-offset identification or fit observed data. No additional execution of the root algebra was performed by this reviewer.

The formula for response error r y−Lp=r Delta U p+r e is also correct, assuming y=(U+Delta U)p+e and nominal rU=L. A physical bound requires calibrated Delta U, allowable p and noise information; none is invented here.

## Accepted scope and remaining physical gap

| Obligation | Outcome |
|---|---|
| Finite basis, support and Abel source conventions | Code inspection passed |
| Angular scale, WCS and spherical radius | Inspected and independently checked for this patch |
| FFT frequency units, transfer, padding and crop | Consistent with declared finite approximation |
| New annulus coverage and normalized weights | Independently matched all15 weight hashes; new rings nonempty |
| Old twelve rows under changed execution | Candidate records bitwise reproduction |
| Independent end-to-end response | One outer column agrees to about1e−15 |
| Target/offset algebra | Limited source/proof review passed; root owns execution |
| Actual calibration/covariance/observed gradient | Not established |

All rows come from the same cached map; they are not independent instruments or automatically independent observations. The finite beam approximation, fiducial distance, fixed outer support, additive background assumption, masks and bin compression define the accepted response model. Noise/covariance, shared-map/systematic errors, distance/calibration uncertainty and alternative support remain missing physical inputs. The exact finite rank and deterministic amplification cannot replace them.

No observed pressure profile or gradient, total-pressure conversion, density determination, MOND force or mass discrepancy is accepted. Any later source bridge must preserve both registered a0 normalizations, separate constant-vacuum and H(z) histories, and distinct Q/RAR/registered M laws. This result supports a reproducible finite response construction and exposes the background-calibration requirement; it does not close the empirical gravity test or the physical theory.
