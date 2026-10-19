# Focused proof, computation and source self-review

Primary verdict: **conditional on a named input** for physical QCD
reconstruction: the matched UV endpoint and the complete all-scale
canonical derivative data. The normalized integral theorem is proved under
its stated endpoint and regularity hypotheses. The elementary Dirac
numerical controls are computationally verified only in the declared range.
This is author self-review; independent fresh review is requested separately.

## Claim card and dependencies

Theorem object: a real/complex f in C^n(0,infinity), continuous at zero,
with `s^k f^(k)(s)->0` as s->0 for 1<=k<n. Its nth derivative defines
the improper integral h_n in main equation (2). On finite positive
intervals integration by parts gives equation (4); the supplied endpoint
conditions pass to the improper lower limit. Under asymptotic (5), the
large endpoint gives equation (6). No physical positivity is used.

Dependency graph:

* Canonical photon path + full current normalization -> equation (2).
  Convention inherited and pinned; QCD data not supplied.
* Elementary derivative/Beta primitive -> equation (3). Internal proof,
  symbolic identity checked for executed n=1,3.
* n integrations by parts + lower endpoint assumptions -> equation (4).
  Internal proof, finite-L independent integral check at every declared L.
* Single-log asymptotic and derivative remainder -> equation (6).
  Internal harmonic boundary evaluation; conditional class, not all QCD.
* Dirac numerator and fixed MSbar subtraction -> equation (7).
  Internal extension of inherited denominator calculation; includes the
  inherited evanescent finite term. Not independently re-renormalized
  through a third regulator in this package.
* Dominated/integrable logarithmic parameter limit -> equation (8).
  Endpoint x=1 creates the displayed O(log(s)/s) remainder, not a constant.
* Source equations (56)-(57),(64) -> QCD scalar/gluon insertion obligation.
  Exact source checked; no numerical proton matrix elements claimed.
* Trace/Feynman-Hellmann relations -> one constraint on multiple matrix
  elements. Algebraic rank test; does not construct a distinct QCD model.

## Obligation matrix

| Obligation | Status | Evidence and limit |
|---|---|---|
| Signs and n! normalization | passed | Differentiate [s/(s+t)]^n; n=1 and n=3 independent current/FP integrals |
| Lower endpoint | conditional | Charged square-root branch is integrable; general theorem states endpoint conditions explicitly |
| UV convergence of derivative at fixed s | passed for control; conditional for QCD | Dirac g~a/t; QCD needs the complete matched current-product OPE |
| UV subtraction and finite threshold | passed for control | Finite/infinite integrals and independent rational density difference |
| Harmonic H_(n-1) term | passed | Log derivatives give a/k in the endpoint Taylor sum; omitting it is numerically nonzero |
| Physical all-orders single-log asymptotic | out of scope | Main derivation expressly substitutes RG-improved finite endpoint for QCD |
| Full scalar/gluon QCD matching | not addressed numerically | Source confirms required operators, not their state data |
| Full proton/vacuum Ward closure | incomplete | One trace constraint does not determine charge-weighted or conditioned response |
| All-scale information vs soft projection | passed as stated | Compact-band fixture has same soft log and leading UV endpoint but delta f(0)=c |
| Numerical exhaustive scope | passed | Two precisions, two derivative orders, five s values and four L values; all Q included by infinite-domain quadrature |
| Independent source-first review | not addressed here | Coordinator-owned fresh review pending |

The numerical outcome is conditional on mpmath quadrature and floating
precision, without certified error intervals. The largest checked
discrepancy over both precisions is about 4.31e-42 against the declared
1e-28 absolute-scaled tolerance. Passing this control is not a QCD result.

## Checks and proofreading

`validate_manifest.py run_001/manifest.json --root PROJECT` reported a valid
v2 completed evidence record. Runtime 3.702786 s, 81 checks, before/after
input hashes equal; no RLIMIT_AS. Caps: 240 s wall, 220 s CPU, 1 MiB log,
one numerical thread. No failures occurred in this run; stdout/stderr are
retained. The pre-execution record pins derivation, source admission,
inputs, implementation and contract before the target execution.

Proofreading coverage: all new equations and prose in this package.
Routine edits: none to frozen inputs. Mathematical-token changes: none.
The post-run contact/band companion is an explicit analytical addition,
not relabeled as an executed run input. The remaining physical endpoint,
all-scale QCD tensor and curved-vacuum inputs are clearly distinguished.
