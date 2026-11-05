# Curvature-only Gaussian filter: Solar scale test

The new response loses the inherited Cassini cut once the curvature filter
reaches roughly half a parsec. The bracketed numerical crossings are
**0.54706835 pc canonical** and **0.52375287 pc alternate**, with p=9/8,
ell=3kpc, original Solar mass, original uniform external field, original a0
footings and ceiling all fixed. These are numerical crossings, not a theorem
that every smaller width passes or every larger width fails.

This test changes only H to T_a H in the KT39 energy and returns T_a* on B
after variation. It leaves g unfiltered. It is distinct from filtering the
baryonic source or filtering H:H after taking the norm. The equations and
the adjoint Green reduction are in `DERIVATION.md`.

The ratio is abs(Q2)/(5.2e-27 s^-2). All listed total signed quadrupoles are
negative; the B contribution can change sign at larger widths.

| Gaussian width a (pc) | Canonical ratio | Alternate ratio |
|---:|---:|---:|
| 0 | 0.000030777 | 0.000035814 |
| 0.1 | 0.000257016 | 0.000319013 |
| 0.2 | 0.00749800 | 0.00936062 |
| 0.3 | 0.0565222 | 0.0702242 |
| 0.4 | 0.230716 | 0.284471 |
| 0.5 | 0.663292 | 0.809995 |
| 0.6 | 1.50259 | 1.81497 |
| 0.7 | 2.81934 | 3.36605 |
| 0.8 | 4.46757 | 5.27129 |
| 0.9 | 6.05181 | 7.06305 |
| 1 | 7.18433 | 8.31386 |
| 1.5 | 8.00093 | 9.18281 |
| 2 | 7.90521 | 9.08167 |
| 3 | 7.88285 | 9.05829 |
| 5 | 7.88124 | 9.05662 |
| 10 | 7.88119 | 9.05656 |
| 30 | 7.88119 | 9.05656 |
| 100 | 7.88119 | 9.05656 |
| 300 | 7.88119 | 9.05656 |
| 1000 | 7.88119 | 9.05656 |

The finite scan is visibly nonmonotone: the ratio peaks near the sampled
1.5pc point, then approaches the ordinary unfiltered-gradient QUMOND value.
There is no sampled high-width reentry, but no interval-certified exclusion
of every unsampled width is claimed. Joint MW/dwarf interpretation belongs
to the phase's other lanes; Solar data alone do not supply their grades.

## Mechanism and source convention

For a Gaussian-filtered Solar Hessian,

\[
H_a(0)=\frac{\sqrt{2/\pi}}3\frac{GM}{a^3}I,
\qquad s(0)=\frac{2\ell^2(GM)^2}{3\pi a_0^2a^6}.
\]

Thus increasing a removes the very curvature contrast that supplied Solar
screening. At1pc the unsmoothed-gradient A term already dominates the
quadrupole. At100pc it has essentially returned to the original QUMOND
external-field value, while the B quadrupole is negligible. The ultraviolet
symbol can become bounded without preserving the Solar suppression.

The reported quantity is the regular exterior l=2 point-Sun coefficient
under the repository's inherited Q2 convention. The raw g is singular at
the point source and generates an isotropic high-field cusp. Its quadrupolar
particular potential is of higher order than r^2 and does not contaminate
the regular l=2 coefficient. The full isotropic r cusp has no central
Hessian and has a directional STF Hessian away from the origin, despite
having no l=2 potential component. Thus q is the STF Hessian of the regular
l=2 potential only, never the full singular point-source potential. The
isotropic radial anomaly remains a separate planet/ephemeris obligation;
passing the retained Q2 amplitude cut would not clear it. A central Hessian
taken *inside* a finite
Gaussian Sun can have a different, nonuniform source-radius limit; that
quantity is not substituted for Cassini.

The exact finite-radius A multipole at9.58AU was separately computed for
point and finite Gaussian sources at filter widths0.1,1 and100pc. Source
widths5e-6 and5e-7 rM give at most7.0e-15 change in dimensionless q_A.
The finite-radius coefficient differs from the regular exterior q_A by at
most1.28e-7 of the Cassini ceiling in these controls. This resolves the
specific source-center ambiguity in the dominant A term. The B observable
is already a pairing against a smooth Gaussian-filtered STF Green kernel;
no unfiltered origin contact is silently discarded.

These remain constant-external-field diagnostics with zero external
Newtonian Hessian. They are not a full Galactic-background Solar solution,
an ephemeris likelihood, a Sun-interior prediction or a relativistic theory.

## Numerical and variational checks

`run_002` completed in21.77s with43/43 checks. `verify_001` completed
in56.61s with38/38 checks. Both use one numerical-library thread. All20
widths on both footings received base/fine radial/angular checks:4000x128
and8000x256, expanding r/rM from[1e-8,1e6] to[1e-10,1e7]. The maximum
change in ceiling ratio was2.953e-8, well below the predeclared2e-4 gate.
The a=0 branch reproduces KT39, and exact Newtonian and zero-external-field
controls vanish.

Independent checks target omitted-adjoint and observable-kernel mistakes:

- On a periodic13^3 smooth source, the full action derivative is
  0.04493246348288343; the weak force pairing is
  0.044932463482883434. The smallest finite energy-difference error is
  4.26e-11. Omitting the return filter instead gives0.0056380963006974994.
- Cartesian second differences of the filtered STF Green test reproduce
  the analytic B tensor contraction at12 states with maximum absolute
  discrepancy2.18e-9.
- Adaptive radial integration at each bracketed crossing gives ratios
  1.0000000049 and0.9999999986. Its reported absolute q error estimates are
  1.66e-8 and1.51e-8; these are numerical estimates, not rigorous interval
  bounds. The retained acceptance test is agreement within2e-4 of the
  ceiling, not a claim that every requested internal adaptive tolerance was
  attained.
- The exterior finite-source multipole checks above avoid reusing KT39's
  inapplicable central-contact argument.

The first `run_001` failed at JSON serialization of a numpy.bool_ after
printing its finite grid. It also emitted floating-point status warnings
from BLAS angular matrix products. That source, contract and failed run
are retained. `calculate_v2.py` converts the scalar boolean explicitly and
uses the identical weighted angular sum through elementwise reduction;
the successful run has clean stderr. No physical input or tolerance was
changed. Only successful, hashed outputs support the table.

Both successful manifests were validated with the computation-audit
validator against current input and output hashes. Actual software was
Python3.13.9, NumPy1.26.4 and SciPy1.14.1. Manifests contain exact argv,
resource limits, dependency hashes and completion status. The contracts
precede their runs; the additional width/crossing calculation was explicitly
authorized after the first grid and is not represented as a blind initial
portfolio. No randomness is used.

Commands are preserved as argv in `run_002/manifest.json` and
`verify_001/manifest.json`; choose fresh output directories for reproduction.
The calculation scripts accept `--output PATH`. No old KT39 source or
result was modified, and no commit or external publication was made.

The derivation received a local mathematical proofreading pass for notation,
units and display consistency. Independent physical review is recorded by
the coordinating audit, rather than inferred from these numerical checks.
