# Cassini: the fixed portfolio and two adaptive choices

All 18 original power-length choices pass the inherited Cassini quadrupole
cut on both frozen acceleration footings. The two separately authorized
adaptive choices also pass. These are **40 individual Solar results** from
the complete A/B variation; no all-parameter acceptance theorem is inferred.

The tables give abs(Q2)/(5.2e-27 s^-2). Every signed quadrupole is negative.

| Power p | Length (kpc) | Canonical | Alternate |
|---:|---:|---:|---:|
| 1.25 | 1.5 | 5.301830e-5 | 6.271374e-5 |
| 1.25 | 2 | 3.976372e-5 | 4.703531e-5 |
| 1.25 | 2.5 | 3.181098e-5 | 3.762824e-5 |
| 1.25 | 3 | 2.650915e-5 | 3.135687e-5 |
| 1.25 | 3.5 | 2.272213e-5 | 2.687732e-5 |
| 1.25 | 4 | 1.988186e-5 | 2.351765e-5 |
| 1.5 | 1.5 | 4.266999e-5 | 5.173353e-5 |
| 1.5 | 2 | 3.200250e-5 | 3.880014e-5 |
| 1.5 | 2.5 | 2.560200e-5 | 3.104012e-5 |
| 1.5 | 3 | 2.133500e-5 | 2.586676e-5 |
| 1.5 | 3.5 | 1.828714e-5 | 2.217151e-5 |
| 1.5 | 4 | 1.600125e-5 | 1.940007e-5 |
| 1.75 | 1.5 | 3.670738e-5 | 4.529941e-5 |
| 1.75 | 2 | 2.753053e-5 | 3.397456e-5 |
| 1.75 | 2.5 | 2.202443e-5 | 2.717965e-5 |
| 1.75 | 3 | 1.835369e-5 | 2.264970e-5 |
| 1.75 | 3.5 | 1.573173e-5 | 1.941403e-5 |
| 1.75 | 4 | 1.376527e-5 | 1.698728e-5 |

The following two choices were explicitly requested **after** initial MW
results, and are recorded separately as adaptive rather than part of the
original portfolio:

| Power p | Length (kpc) | Canonical | Alternate |
|---:|---:|---:|---:|
| 1.125 | 3 | 3.077669e-5 | 3.581393e-5 |
| 1.25 | 2.75 | 2.891907e-5 | 3.420750e-5 |

For the latter choice, Q2=-1.50379172e-31 s^-2 canonical and
-1.77878976e-31 s^-2 alternate. Passing this Solar amplitude cut is separate
from the parent's MW and dwarf grades; none of those grades is supplied by
this lane.

## Full law, contacts, and noninteger regularity

The implemented law is

```
P=xR(z), z=x+s^p, s=lambda^2 H:H,
A=(R-1+xR')g,
B=beta xR' H, beta=p lambda^2 s^(p-1),
S_ph=div A-double_div B.
```

The function Q=zR is the unchanged simple-response primitive with Q(0)=0.
The ordinary Newtonian Solar field and constant external field are unfiltered.
The full B term dominates the nonzero Solar quadrupoles and is retained,
together with beta' and beta'' in the differential-density calculation.
DERIVATION.md records these derivatives, both finite-core contacts, and
the geometric Green expressions. Scaled R derivatives avoid unnecessary
overflow without a high-field floor.

The point field is interpreted as a shrinking regular Gaussian source.
For fixed p>1, eta>0, and lambda>0, both contacts vanish as
sigma^(9p-3)/lambda^(3p). Uniform small-core estimates and integrable
exterior tails establish this Gaussian STF limit, also covering the adaptive
p=9/8. This does not square a distributional Hessian or establish the same
limit for every regulator.

At H=0 with g!=0, the action is C^2 for every tested power, while B is
C^1. B is not generally C^2 for p<=1.5, including 9/8, so a classical
pointwise double divergence across H=0 need not exist. The variational
source may require a weak interpretation. This limitation is stated in the
derivation; the finite Solar radial Hessian norm never vanishes and needs
no numerical floor. The joint zero-field point retains MOND nonanalyticity.
Improved static uniform-field behavior does not prove dynamical health.

The analytic owner independently checked the derivative identities,
regularity qualifications, and Gaussian-limit powers in
`../analytic/SOLAR_DERIVATION_REVIEW.md`, with source hashes.

## Completed checks and reproducibility

`run_001/` completed in 29.49 seconds with all predeclared controls passing:

- Each of the 36 original physical rows received base 8000x160 and fine
  16000x320 radial/angular quadrature with expanded domain. Maximum relative
  refinement shift was 1.173e-9; maximum Green/density discrepancy was
  2.503e-9 relative.
- The full scalar coefficients were checked against the shared tensor API
  on 24 states per power. Maximum relative discrepancy was 3.84e-16.
- Shared zero-length controls reproduced QUMOND and the finite Gaussian
  origin correction. Newtonian and zero-external-field controls returned
  exactly zero for each power.
- At 1.5 kpc, every power and footing was checked with Gaussian widths
  .5,.1,.01,.001,5e-7 rM. Maximum point-limit discrepancy was 2.20e-10
  relative. Half/quarter changes of the resolved broad-core inner radius
  shifted q by at most 4.47e-16, with analytic contacts retained.
- The general implementation also reproduced the already validated p=1
  and p=2 endpoint models at 3 kpc: relative differences 2.66e-11 and zero,
  respectively. This is an implementation check, not a transferred grade.

`adaptive_001/` completed in 5.47 seconds. Both new choices received fresh
API, base/fine, and density checks. The new p=9/8 additionally received
Gaussian-core, core-cutoff, Newtonian, and zero-external-field checks on both
footings. The unchanged zero-length controls were explicitly inherited from
the original successful run. Separate API checks at H=0 reproduced the
ordinary response with B=0, and the joint zero-field value was zero for all
four powers; this verifies values, not additional differentiability.

Both manifests completed and validate against unchanged input hashes.
Contracts preceded each run and preserve the exact argv, resource caps,
software versions, output hashes, and one-thread setting. No randomness is
used. The original portfolio and every KT37/KT38 artifact remain unchanged.
The results are conditional on empirical quadrature accuracy, not certified
interval integration.

The diagnostic uses the original constant external field, with zero external
Newtonian Hessian. Actual Galactic gradients, ephemeris modeling, relativistic
completion, and other observations remain separate. Final mathematical
self-proofreading covered this new text and formulas without changing any
previous source artifact.
