# Independent mathematical and code audit

15 October 2026. Primary verdict: **conditional on the explicitly recorded
finite-band template, source/data footing, and numerical convergence; the
reported bounded conclusions are supported**. I found no material projection,
distributed-source derivative, covariance-profiling or exclusion error that
reverses RESULT.md. This was a read-only reconstruction, not a fit rerun.
Only this audit file was written. It is independent same-team review, not
external verification or a calibrated observational validation.

Audited exact SHA-256 revisions:

| File | SHA-256 |
|---|---|
| model.py | `f86a1ce3331d13f894abc5c4daacbe4b2046e57d7fcd7a8bb1072fee8c5affa9` |
| extended_model.py | `b89abd18c202f070faf4d2e82a57deea826573bd48bc5e586ba32bdaf3d27d52` |
| fit.py | `8a2383af87b76b944964e3ae5af5f16f2b4a87c9c7e92e93cd5b829c7eced7e5` |
| DERIVATION.md | `7b0467c982573b7840b1b4a51308dcc5b29ad30f61c94fe3be3ce6c73db442fc` |
| POST_DATA_CRITERIA.md | `c7f9eae1df31351cb1e23a0d3078f61fb2a1fbbd45b913af3514685e55a03ab5` |
| RESULT.md | `3cb4029c5a28a7d676d352cd7e978aac505eb7efe5c8c95b7a0526ac0c714283` |
| native_all_verified_001/result.json | `b46ab142c8a01aff7d93a90cf136d1afc263d9e2c0df2a9271395d6582881d97` |
| extended_profile_001/result.json | `86fdef806b96dcd33b6899d643d8d3e77dfc8664cfc51eb7b3d3e253ae6f10ea` |

**Continuous finite profile and projection: passed.** Differentiating
`m_ex(s)=(sqrt(1+4s^2)-1)/2` gives the implemented density. For any spherical
enclosed mass m, the omitted cylindrical caps are
`integral_x^e m'(s)sqrt(1-x^2/s^2)ds`. Substituting `s=x cosh u` gives
both the finite point-source cap integrand in model.py and the general
distributed-source cap integrand in extended_model.py. The corresponding
LOS surface density is `(2pi)^-1 integral m'(x cosh u)/(x cosh u)du`.
These independently reconstruct the factors of two and pi in both codes.
The incomplete-elliptic surface term and infinite elliptic expression use
SciPy's parameter convention consistently. At and beyond the point-source
edge, the excess surface density is zero and the complete ESD is exactly
`(1+5.364N)/(pi x^2)`. Its interior limit agrees, so changing mass/retention
does not select a nearest-N profile. Sharp-edge derivatives need not be
smooth; the report appropriately claims tested optimization convergence.

**Distributed source: passed at its stated spherical-algebra scope.** With
`b=s^3/(s^2+u^2)^(3/2)`, differentiating
`[sqrt(b^2+4s^2b)-b]/2` gives the exact implemented dmex. It is positive
for `s>0`: its derivative at fixed b is positive, while its partial
derivative in b is nonnegative because
`(b+2s^2)^2-(b^2+4s^2b)=4s^4`. Thus positivity has an analytic reason
beyond the sampled derivative control. The cap is solved from the actual
new enclosed excess mass, and its physical edge is reused for environmental
exclusion. The Plummer baryon ESD is also changed. This is a reciprocal
change to the specified spherical acceleration algebra; it is not a common
varied action or a self-consistent energy/formation solution. Both the
reusable module and the inline four-size implementation agree on these
formulas. The extended fitter is used only for the declared all-radius
native-unit diagnostics; its override does not implement arbitrary primary
subselections or alternative conventions.

**Environmental transform and exclusion: passed within the finite controls.**
Combining the cylindrical mass and surface-density kernels before LOS
integration gives the stated outer weight
`-2[R/(sqrt(R^2+t^2)+t)]^2`; it retains the inner cylinder. Setting the
density to zero for `r<e` produces exactly the implemented inner lower
limit and outer `arccosh(e/R)` lower limit. The signed xi mass is retained;
the preliminary clipped assignment is overwritten by the correct signed
expression. The DST-I factor of two is compensated by its `4pi^2` divisor.
Physical/comoving radius and surface-density conversions are consistent
between the direct Hankel and real-space paths. Each trial mass recomputes
retention, rM, its edge and the interpolated exclusion template in both B
and D. The four data files have identical radius arrays, so sharing the
15-row environmental table is valid for these inputs. The quoted best-fit
edges lie well within the interpolation interval. This does not authenticate
matter auto-power as an isolation-selected galaxy–matter cross-power.

**Full-covariance profiling and reporting: passed.** For `C=LL^T`, the code
applies `L^-1` to the data, one-halo prediction and all four design columns,
then jointly profiles nonnegative biases by NNLS. Its squared residual is
therefore `r^T C^-1 r`, including cross-bin covariance. The supplied
covariance has all 3600 entries, and its boost correction matches the two
data factors in the file headers. Primary fits select the covariance
submatrix before whitening. Signed block contributions partition the full
precision quadratic; conditional increments are separately computed by
subtracting the remaining-data quadratic and are not called additive.
The nominal degrees of freedom and boundary/post-data caveats are explicit.
Four starts plus another local algorithm establish the stated convergence
gate, not a global optimum theorem. The stored independent optimizer runs
for the checked fits report success.

**Control provenance and conclusion: supported.** I validated the existing
Mathbox manifests for controls_002, refinement_001,
native_all_verified_001, extended_profile_001 and summary_verified_001
against their current inputs/outputs. The authoritative baseline fit uses
the refined cache and the passing supplementary refinement receipt.
The initial algebraic normalization entry is correctly distinguished from
the subsequently executed density mutation; it has not been retroactively
called an earlier runtime control. No optimizer, simulation or projection
fit was rerun for this audit.

The inspected outputs reproduce the report's native all-radius
`chi2_B=161.841092`, `chi2_D=165.358204`, difference `3.517112` and nominal
`p_D=9.7824e-14`. Hence the predeclared relative gate passes and the
absolute gate fails. Four-size Plummer gives `75.734180/48` and nominal
`p=.00651557`; common size gives `83.776292/51` and `p=.00259431`.
Neither reaches the fixed `.01` convention. Those larger families are
explicit post-data profile diagnostics, not a matched relative comparison
to point-source B or empirical closure. Nonnegative-bias boundaries and
selection prevent treating these nominal p values as calibrated sampling
probabilities. No ownership-consistent observed cross-power, external
baryon-size constraints, microscopic production, galaxy formation or common
Einstein/current action has been established by these fits. RESULT.md keeps
those distinctions and does not claim physical-theory closure.
