# AZ32 — solar spectrum and a sourced tensor diagnostic

Tier 1 lane 2. Freeze before new outputs. Prior V3X and CT14 H3 outputs were
read; this is an explicit reproduction and extension, not blind validation.
Kappa = 1/2 FITTED; not theory closed. Both a0 footings remain separate:
9.3603e-11 and 1.1312e-10 m/s^2. L_star = 24 pc is FITTED.

## Spectrum

Rebuild V3X's radial lower/upper bracket operators from freshly solved C6
backgrounds, with the same domain, inner Neumann and outer Dirichlet conditions.
Use 12,16 cells/decade for known answers; 24,32,48 for the graded ladder;
l=0..4, reporting l=1..4 explicitly. Use the CT14 H3 float64 symmetric
Cholesky reduction read-only, independently checked against V3X's recorded
40-digit lowest three roots at 12/16 (relative error <=1e-8). A fresh 30-digit
V3X solve at 24 cells/decade, l=4, lower bracket on each footing must agree
within 1e-8. Background residual <1e-9.

Require A positive definite, V positive definite, V >= gamma within relative
1e-12 roundoff, and every computed omega^2 positive. Lowest three roots on
32/48 must change <0.05 relative (original V3X discretisation tolerance).
Report 24/32 too. This is convergence of the radial bracket discretisation,
not proof of convergence of an unrestricted 3D background or its nonlinear
evolution. Background grid remains the inherited 30/48; AZ31 separately
checks a background observable, not every background derivative.

MUTATE: reverse the sign of the stiffness in V, on the same background and
same grids. Require the actual positivity test to fail on both footings.
Report mutant eigenvalues and ladder changes; no passing physical model is
inferred from this deliberately wrong-sign operator.

## Tensor line: source and scope fixed before calculation

Primary source: LIGO/Virgo/Fermi/INTEGRAL, arXiv:1710.05834v2,
https://arxiv.org/abs/1710.05834v2, abstract, verified 2026-11-05 UTC.
It reports -3e-15 < (v_g-c)/c < 7e-16 from GW170817/GRB170817A.
This is a propagation-speed bound, NOT a tolerance on omega^2/k^2 at
arbitrary Solar-System wavelengths. No primary source for the old 1e-10
finite-root threshold has been established; do not reuse it as an
observational tensor gate or erase its historical failure.

Recompute the V3W restricted TT quadratic expansion, including background
P and its gradients, and its frozen background mass scan at 100 Hz.
Verify zero additional quadratic derivative coefficients and the GR limit.
At 100 Hz bound both signs using max|m^2|/(2k^2); demand the symmetric
envelope lies inside the source's asymmetric interval. Check the small-mass
approximation error via the exact group-speed formula at high precision.
Known answer: m^2=0 gives v_g/c=1 exactly. MUTATE additionally adds a
dimensionless tensor gradient coefficient 1e-8 and must violate the same
speed bound. This coefficient is a control, not a fit.

The isolated TT subspace does not prove that the full constrained mixed
metric/polarization system has the same eigenmodes. Report this tensor result
as a restricted diagnostic; full tensor closure remains UNDECIDED unless
the mixing is independently controlled. A local 100 Hz scan is not a
line-of-sight cosmological propagation calculation.

## Labels and execution

Separate labels: radial-spectrum PASS only if all numerical checks pass;
FAIL for a verified negative eigenvalue, UNDECIDED for failed convergence;
restricted tensor diagnostic PASS/FAIL; overall W4c remains scoped by the
missing full-mode implication above. No label is inherited from old prose.
Single thread, sub-1GB; checkpoint each spectrum atomically, source hashes
and software recorded; resume checks hashes. Separate main/mutate outputs.
No historical files edited. Commit rerunnable script, JSON, logs and README.
