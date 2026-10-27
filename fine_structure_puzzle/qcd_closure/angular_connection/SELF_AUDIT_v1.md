# Self-audit AC-005-001

Normalized claim: for the actual static BPS gauge Hessian in each total
J>=6 sector, the regular DN map and actual relative mixed wall satisfy
the inequalities in Sections 4-8 of RAW_DERIVATION_v1.md, in the stated
Z=J/R+Q boundary normalization. The determinant connection is normalized
by Y(2)=Y_0(2)=I. It is not a physical infinite-angular determinant claim.

Primary verdict: **proved as written** for this normalized claim, by the
hand argument and the operator conventions checked below. This verdict
is an author self-review, not an independent audit. The larger physical
goal remains incomplete.

## Dependency graph and obligation matrix

| Implication or leaf | Evidence | Status |
|---|---|---|
| Cartesian A,Phi,D,H -> (2.1)-(2.3) | Direct covariant angular derivative; curvature quaternion matrices | passed |
| Angular expression has actual sign and field content | All 120 frozen J1 Cartesian component residuals vanish after BPS substitution | passed; exact finite crosscheck |
| Profile c<=b | Identity (3.1), Taylor lower bound and differentiated tanh inequality | passed |
| Curvature lower/upper eigenvalues | Explicit active 2 tensor 3 matrix characteristic polynomial and 2-by-2 blocks | passed |
| Grand-spin constraints -> L^2,G^2 extrema | Actual coupling J=L+T+S, T=1,S=0 or 1 | passed |
| Coercivity -> no regular Dirichlet zero and Hermitian P | Integration of the ODE and zero origin Wronskian | passed |
| Variational lower/upper P estimates | Completed square and explicit neutral/charged trial functions | passed |
| Charge-sensitive P lower bound | Half form split and mass >=1/2 on [2,R] | passed |
| Q commutes with the actual P_N | Pointwise internal/spatial normal projections; ranks derived from harmonics | passed |
| Actual 9D+3R map and neutral Schur | Triangular wall map, positive three-normal block, variational Schur minimization | passed |
| Full profile error E_J | Exact operator subtraction; norm bound retaining K and h corrections | passed |
| Riccati transport | W'=E-PW-WP_0, two factors with contraction (s/R)^(J-1) | passed |
| Uniform J~sqrt(R) regime | Explicit split integral (7.4)-(7.5) | passed |
| Connection constant and determinant error | Nonnegative-integral interchange, trace bound dim E_J=12, normal determinant bound | passed |
| J=2 or improved constants at small J | Not used in the main large-J theorem | out of scope |
| Frobenius connection singular values | Not implied by determinant or DN bounds | not addressed |
| Infinite-J UV-subtracted product / physical matching | Requires additional common-regulator information | not addressed |

## Adversarial checks

The large-J proof uses angular bounds on L and G before applying the
curvature estimate. It does not commute noncommuting matrices or identify
the spatial-vector and isospin-vector indices. The explicit J1 projection
uses the frozen Cartesian tensor basis only as a check of the derived
angular operator, not as its definition.

The profile inequality b>=c is global, not an asymptotic assumption.
The lower potential coefficient factors as
(1-K)[2(J-1)-5(1+K)] after subtraction of (J-1)(J-2), so J=6 is included
without a strict-positivity assumption at K=1. The positive radial
centrifugal coefficient still excludes a nonzero Dirichlet zero.

The charged lower bound loses half of the angular coefficient explicitly;
no invalid addition of two separately minimized full kinetic forms is
made. The upper comparison keeps Q, giving the required small neutral
scale rather than a spurious neutral mass.

The wall estimate uses the actual normal Robin shift +1/R and the
commutation [P_N,Q]=0. The full P_J need not commute with charge or normal
projection. Only the normal block is SPD after Dirichlet values are fixed;
the entire mixed map is triangular, not asserted to be SPD.

The Riccati comparison uses the regular Coulomb DN map, which stays
positive, rather than a pure growing solution through possible zeros.
Both P and P_0 have lower bound (J-1)/r, so the two-sided contraction
exponent is 2J-2. Matrix multiplication order is retained in
P W+W P_0 and the right propagator is the transpose/adjoint propagator.

For the constant 38, the initial difference is bounded by the maximum
of the two positive DN norms, not by a claimed estimate for arbitrary
connection entries. The normalized Y matrices have positive determinant
for R>=2. The limiting normal determinant ratio is one because the
fixed-J bound (7.3) is O_J(R^(-2J+2)), and its relative error is bounded
by R epsilon/J. The integrated error (8.2) is obtained before any angular
sum. The loose bound (7.4), taken alone as R varies at fixed J, is not
integrated, because its middle term is constant in R.

The claimed finite expanding band result stops at J<=Lambda R. No
summability at infinite J is inferred from a uniform pointwise estimate.
No physical finite part of the divergent fixed-J inverse coefficients
has been defined.

## Sources, execution, and limits

All load-bearing new leaves are internal proofs. The far centrifugal
decomposition is inherited from the frozen higher-angular derivation;
that input derives it from Pauli/monopole algebra. No external index or
boundary determinant theorem is applied in this proof. The finite
manifest is `runs/exact-001/manifest.json`, run status completed, with
146 checks passed; validator confirms its before/after input hashes.

Final mathematical proofreading self-review covered RAW_DERIVATION_v1.md,
REPORT.md, this audit and ROUTE_v1.md: operator signs, charge labels,
matrix dimensions, square-root boundary scales, Schur shifts, quantifiers,
integration limits, and fixed versus uniform angular claims. Routine
edits: none. Mathematical-token changes: none. Unresolved typographical
issues: none. This receipt is not independent correctness review.
