# Independent audit: UGC08286 finite disk inversion

Normalized claim: on the explicitly declared finite annular source bases and
17 observed target radii, solve additive nonnegative-mass feasibility and
the least stellar M/L ceiling compatible with the frozen simple law and
quoted velocity-error boxes.

**Primary verdict: computationally verified only in a stated range.** The
finite model and the nominal one-error-box numerical results pass the
independent controls below. A physical exclusion of all stellar gradients
does not follow. No intrinsic radial stellar M/L bounds or full intrinsic
light profile have been recovered. The external observation/calibration
statements were read in the authenticated packet records; their primary
source authentication was not independently repeated in this numerical audit.

## Exact mathematical dependencies

1. Input convention: inward acceleration is positive. The Newtonian gas
   contribution is `Vgas*abs(Vgas)`, in (km/s)^2. The first three entries are
   -14.8225, -1.9044, -0.3969. Exterior positive gas may pull outward; there is
   no negative gas mass. The supplied gas template includes helium already.
2. Let `b` be Newtonian baryonic V^2 and `a=a0*R*kpc_m/1e6`. The fixed simple
   law gives `W=(b+sqrt(b^2+4*a*b))/2`. For nonnegative W its inverse is
   `F(W)=W^2/(W+a)`. Its derivative `W*(W+2*a)/(W+a)^2` is nonnegative.
   Therefore transforming each observed squared-speed interval through F is
   exactly equivalent to the stellar-only interval constraints. The code
   places stellar mass inside the simple law; the separate extra-mass
   comparison adds Newtonian force outside the frozen baseline, as declared.
3. For a unit-surface-density uniform disk, the original Newtonian force is
   `G*R*a*integral_0^(2*pi) cos(phi)/sqrt(R^2+a^2-2*R*a*cos(phi)+z^2) dphi`.
   This follows from the boundary integral of the planar Newtonian potential.
   Its complete-elliptic-integral evaluation is the production boundary
   formula. Subtracting two disk boundaries and dividing by annular area
   yields signed V^2 per source mass. An annulus can have negative columns
   at interior targets despite its nonnegative density.
4. Exponential height averaging uses `u=abs(z)/h` with normalized positive
   weight `exp(-u)/(1-exp(-24))`, truncated at u=24. The substitution `u=t^2`
   correctly supplies Jacobian 2t and regularizes the integrable edge log.
   This is the specified truncated density; agreement of quadrature orders
   does not prove an enclosure for an untruncated physical galaxy.
5. The luminosity in bin j is `2*pi*1e6*integral R*I(R) dR`, in Lsun. The
   factor 1e6 converts kpc^2 to pc^2. Multiplying the signed kernel by this
   bin luminosity gives B. This is exact for the finite model whose surface
   light density has been replaced by its annular average. It approximates
   the declared continuous interpolant; it is not an exact arbitrary radial
   `Upsilon(R)*I(R)` calculation at a finite bin width.
6. Stellar min-ceiling variables satisfy `0<=U_j<=u`. The linear inequalities
   are `B*U<=hi`, `-B*U<=-lo`, `U-u<=0`. Minimizing u is therefore the correct
   finite least necessary ceiling, with no hidden gradient penalty. The
   implemented [0,Ucap] family enlarges the calibration boxes with nonzero
   lower bounds. Its failure can exclude such a box only under the stated
   total-light/clean-old-star, extinction, support and projection assumptions.
7. For `min c*x` with `A*x<=b`, `x>=0`, valid inequality multipliers obey
   `y<=0` and `A^T*y<=c`; then `b*y` is a lower bound. The saved sign checks,
   primal residuals and dual objectives use these directions correctly.
   They are floating numerical certificates, not exact-arithmetic proofs.
8. Independently, for any vector z and feasible `0<=U<=u`,
   `u >= [z_positive*lo + z_negative*hi] / sum(max(B^T*z,0))`, if the
   denominator is positive. This is the support-function inequality for a
   box, independent of HiGHS optimality status. Applying it to the saved
   multipliers reproduces every reported ceiling within 1.99e-12. No
   rigorous rounding or quadrature enclosure is claimed.
9. Homologous distance changes rescale R,h,source edges by lambda and L by
   lambda^2. Hence B and gas V^2 scale by lambda while baryonic acceleration
   is invariant. The inverse-law radius must change by the same lambda;
   the code does this. It does not reapply the empirical h~Rd^0.633 rule.

## Obligation matrix

| Obligation | Status | Evidence / limit |
|---|---|---|
| Units, signs, simple-law inversion and interval equivalence | Passed | Direct derivation; actual-interval round trips |
| Uniform-disk boundary identity | Passed numerically | Four original Newtonian angular/radial integrals, max relative difference 2.92e-13 |
| Annular light integrals | Passed | Independent adaptive radial integration matches all six luminosities |
| Vertical quadrature in nominal stellar controls | Passed numerically | Adaptive versus order192 for all six models, both footings, all17, one-error boxes |
| All saved successful LP constraints and multipliers | Passed to reported residuals | 84 additive and 432 stellar witnesses rebuilt |
| Main unsuccessful additive cases | Passed as numerical statuses | All 24 independently recomputed as status2 |
| Physical intrinsic light deprojection and radial M/L bounds | Conditional / unresolved | 17 corrected SB samples only; 65-point profile is projected |
| Calibration bridge to total SPARC light | Conditional | Calibration is dust-corrected old stars; IMF/extinction/projection correspondence not established |
| Full observational covariance and all-radius dynamics | Not addressed | Error boxes and odd/even samples are finite controls |
| Coupled nonlinear field, density uniqueness, detection or lifetime | Out of scope | None follows from these LPs |

## Decisive finite results

The main-run matrices and results were independently read and rebuilt:

- 108 additive cases, 84 solver-feasible. Successful witnesses have maximum
  primal violation 3.96e-11 (km/s)^2, dual violation 2.05e-14, absolute
  primal/dual gap 1.43e-14 in the billion-solar-mass objective units. Saved
  predicted vectors reproduce exactly. The other 24 statuses were
  independently reproduced as infeasible for their finite matrices.
- All 432 stellar min-ceiling cases succeed. Maximum primal violation is
  1.89e-10 (km/s)^2. Maximum dual violation is 6.28e-8 in two exact-central-
  value CF4 diagnostic cases; support-function bounds still agree with
  their ceilings to 2.14e-14. Across all cases the largest support-bound gap
  is 1.99e-12. This is numerical evidence with the stated tolerance.
- In the primary additive geometry, the minimum one-error-box mass is
  1.810171818834884e9 Msun. Independent adaptive-height quadrature gives
  1.810171818834860e9 Msun. This conditional minimum is not a parameter-free
  mass prediction.
- For the six nominal all17 one-error-box stellar models, switching from
  order192 to adaptive height quadrature changes the minimum ceiling by at
  most 4.93e-9. The largest unit-disk speed change is 2.70e-8 km/s. Thus the
  quadrature discrepancy is negligible relative to the conditional ceiling
  comparison with 0.95093592 in these controls.
- Loglinear and linear light have total luminosities 1.260841500e9 and
  1.272724911e9 Lsun. Their finest tested reconstruction differs from the
  published unit-disk template by at most 1.3791 and 1.3991 km/s, RMS 0.4945
  and 0.4864 km/s; maximum relative errors are 5.83% and 5.75%. The coarsest
  errors reach 11.05% and 9.53%. These are approximate conditional geometry
  reconstructions, not exact template/deprojection recovery.
- For the main fixed source matrix there is a strictly positive normalized
  force-null ray over 18 bins. Its smallest mass fraction is 0.00162004;
  fractions sum to 1. The target-force residual per 1e9 Msun is 7.68e-13
  (km/s)^2 with the stored matrix and 2.34e-11 with adaptive quadrature.
  This explains the unbounded maximum-mass LP numerically. On 518 dense
  radii the same source gives -372.676 to +3679.909 (km/s)^2 per 1e9 Msun.
  The maximum occurs at the support edge 8.07 kpc and the minimum near
  8.02164 kpc. It is not a continuum force-free distribution or a physical
  unbounded-mass conclusion. The terminal bin is only 0.0342132 kpc wide
  versus median 0.472693 kpc.

## Post-run sensitivity code and result review

`../sensitivity.py` and its completed output were reviewed algebraically and
read, without an additional independent reproduction in this audit. Its
minimum-total-stellar objective `L*U/1e9` and the homogeneous distance
translation `10^8.75*(6.5/8.59)^2 = 3.21988518e8 Msun` are correct. A
comparison treating that finite-footprint nominal SED mass as a full-support
upper budget remains conditional on aperture correspondence, missing light,
population modeling, dust, IMF, mass convention and absent global error.

The equal-width source control demonstrates material basis dependence. The
same 18-bin 8.07-kpc support has no reported positive null ray and a finite
canonical one-error-box range 1.85492419e9 to 2.67809310e9 Msun. A coarse
18-bin 16.14-kpc support instead needs minimum 6.93328996e12 Msun canonical
or 9.80293137e12 alternative, with severe inward/outward cancellation; its
saved residuals are approximately 1e-9 (km/s)^2. These results do not support
a globally stable inferred source mass. Both 9-bin 8.07-kpc one-error-box
footings return status4 for minimum and maximum: **solver-indeterminate,
not infeasible**. No claim should collapse that status into an exclusion.

## Corrections and strongest safe interpretation

The main field named `quadrature_delta_v2_bound` is a 96-versus192 discrepancy,
not a proved quadrature bound. The independent adaptive checks substantially
strengthen the numerical interpretation for the primary cases but do not
change that mathematical distinction. `baseline.py` explicitly reproduces
legacy dchi2, coherent offset and grid-selected constant M/L; it does not
itself recompute the cited legacy pull +3.70.

The strongest safe interpretation is finite positive-source feasibility and
finite necessary stellar ceilings under the listed geometry, interpolation,
support, interval and population-bridge conditions. The calculated failure
of a chosen ceiling does not replace missing intrinsic stellar constraints.
Improving the intrinsic photometric/deprojection and population information
is more decisive than tightening the already negligible nominal quadrature
discrepancy. Boundary/source-basis changes must remain separate controls.

## Reproduction and provenance

Fresh independent reviewer; raw target, source code and records were supplied
without an author verdict. All audit writes are confined to this directory.
Both independent runs use the computation-audit runner, one numerical thread,
supported CPU/wall/output caps, and nominal memory well below 1 GB. macOS
address-space and affinity caps were not requested or claimed enforced.

- `run001/manifest.json`: completed; independent original-force, radial-light,
  adaptive-height and nominal LP controls. Validated against current inputs.
- `run002/manifest.json`: completed; full saved-constraint/multiplier audit
  and explicit sampled-force null ray. Validated against current inputs.
- `../inversion_run/manifest.json`: completed and independently validated.
- Exact commands, input/output hashes and observed versions are in the run
  manifests; source/proof/run hashes are collected in `PROVENANCE.json`.
  Recorded Git revisions differ between shared-workspace runs; individual
  before/after input hashes, which validate unchanged, identify the actual
  artifacts audited. This reviewer made no Git mutations or manual Git-state
  inspection; the required runners recorded their own repository metadata.
