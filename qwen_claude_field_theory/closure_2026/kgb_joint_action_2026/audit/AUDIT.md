# Independent local principal and preservation audit

Audited 2026-09-10 against base commit
`de6b2c1a948c043a3a3c7130f88051db66c6bc46`. Legacy code is preserved. This
directory contains the audit, six reproducible Python checks, four conditional
Lean theorems, contracts, and bounded-run provenance. None of these artifacts
certifies a universal MOND theory or a complete stable solution.

**Verdict: correct only after stated restrictions.** The coupled scalar
principal expression, derivative identities, and analytical cone optimization
pass. A positive interval rejected by the numerical width threshold is
unresolved, not empty. Positive time kinetic coefficient and a Lorentzian
subluminal cone do not imply bounded energy relative to static time.

## Claim and source bridge

The audited action is `sqrt(-g)[m R/2 + P(X) - G(X) box(phi)]`, with signature
`(-+++)`, `X=-dphi^2/2`, and a timelike stationary spherical scalar
`phi=q t+psi(r)` on the zero-radial-current branch. Here `p=psi'(r)`.
The files audited were the legacy `jet_window.py`, `jet_steering.py`,
`regular_clock.py`, and parent `ticking_kgb_inverse_2026/kgb_inverse.py`.

Primary source checked: Deffayet, Pujolas, Sawicki and Vikman,
*Imperfect Dark Energy from Kinetic Gravity Braiding*,
[arXiv:1008.0048v2](https://arxiv.org/html/1008.0048v2), 24 September 2010,
[JCAP 10 (2010) 026](https://doi.org/10.1088/1475-7516/2010/10/026).
The exact version's sections 2.1--2.3, especially equations 13 and 16--18,
were checked on 2026-09-10. Its `(+---), K+G box(phi)` convention translates
to the convention above. No source copy was retained. This was an exact
formula check, not a novelty search.

The independent reconstruction from equations 16--18 matches all 16 entries
of the code's principal matrix symbolically. In particular, the code keeps
the `G_X^2/m` contributions from eliminating Ricci with the Einstein equations.
The sign reproduces positive canonical time kinetic coefficient for `P=X`.
The gravitational kinetic sign additionally requires `m>0`; the elimination
requires `m!=0`. The source's characteristic argument assumes ordinary matter
stress without second derivatives of the scalar or metric. This is a local
high-frequency principal calculation, not a canonical constraint analysis.

The dependency chain is: action and conventions -> covariant stress/scalar
equation -> Einstein elimination -> principal matrix -> zero-current slope
identity -> local cone interval. The separate Lean preservation algebra does
not prove any of these physical arrows.

## Derivative identities and regular crossing

In the orthonormal frame set `w=p/sqrt(B)`, `chi=X'/sqrt(B)`,
`v^2-w^2=2X`. Stationarity gives `X_hat0=0`. Zero current implies

```
P_X = G_X (box(phi) + chi/w),
E = rho+P = 2X G_X chi/w.
```

Independent differentiation of the reconstructed effective metric then gives

```
dC/dP_XX = (E/P_X) diag(1,0,beta,beta),
beta = w^2/(2X),
I = C00-C22/beta.
```

Substituting `G_X=p L` directly gives `dC/dL_X=(E/L) diag(1,0,beta,beta)`
without division by `P_X` or `Z`. The symbolic test checks both slopes and
the substitution at `box(phi)+chi/w=0`. A separate exact crossing control
uses `B=r=p=L=1, X=3/2, g=2/3, H11=3`: then `Z=P_X=0`, `E=-17`,
`beta=1/3`, and the slope is `diag(-17,0,-17/3,-17/3)`; radial pressure
and energy flux vanish. This is an algebraic control, not a global solution.

Require a regular metric, `A,B,X,r>0`, `p!=0`, and finite action derivatives.
The old chart also requires `P_X!=0` and a nonsingular current denominator.
The regular inverse still requires `L!=0`, `X'!=0`, and `T+Z!=0`.
Nonzero `E` is needed to steer an arbitrary local time coefficient, although
the zero-slope identity can still hold at `E=0`. Integration and agreement of
the same `P(X),G(X)` across different masses are additional obligations.

## Two exact counterexamples to broader interpretations

The analytical stationary-point quadratic used by `jet_steering.window` is
correct for its stated cone problem. However, with

```
I=1, cross=0, radial=-1+10^-11, beta=1,
```

the exact interval is `1-10^-11 < K < 1`. Its midpoint has positive time
coefficient, negative spatial coefficients, and every characteristic speed
strictly below one. The legacy function returns `exists=False` only because
the positive width is below its relative `1e-10` threshold. The audit records
this result as `numerically_unresolved`; the preserved legacy text saying
"empty strict causal window" is not a valid nonexistence conclusion.

For the independent matrix example

```
I=11/10, cross=1/2, radial=1/10, beta=1, K=1,
C22=C33=-1/10,
```

the legacy window accepts. The radial discriminant is `3/20`; the exact
maximum characteristic speed is `1/2+sqrt(15)/10 < 1`. Nevertheless, the
quadratic scalar Hamiltonian for static time has radial gradient coefficient
`-C11/2=-1/20`. Setting the time and transverse derivatives to zero leaves
`H=-(radial derivative)^2/20`, which is unbounded below. This is a static-time
energy counterexample, **not a claim of a wrong-sign time kinetic ghost**.
Requiring `C11<0` alongside `C00>0,C22<0` establishes the stronger local
energy-sign condition for this scalar quadratic form.

The previously reported repaired jet survives that stronger condition.
At `epsilon=10^-6,y=20,u=0,z=0.5,P=0,P_X=1`, the selected
`P_XX=3232288.890528025` gives, with 60-digit reevaluation,

```
C00 = 15033306.36333942826567
C11 = -0.24407592012491445752
C22 = -15.02857327822006540888
C01 = 2373.93480835516807541863
radial discriminant = 9304834.55747209111330
relative stress error = 9.44065419047549e-55
```

This is one local point. Arbitrary precision is not a rigorous interval
error bound, nor does it certify an ODE trajectory or global stability.

## Formal preservation algebra and reproduction

`SharedPreservationFormal.lean` proves over the reals: if `a+p*b=0` and
`b!=0`, then `p=-a/b`; such `p` is unique; if `b=0,a!=0` there is no solution;
if `a=b=0` every `p` satisfies the equation. In this file **p is an abstract
control, not psi'(r)**. Establishing the physical mapping to these symbols
and preservation equation remains outside the theorem. All four checked
theorems print only `propext`, `Classical.choice`, and `Quot.sound` as axioms;
there is no `sorryAx`.

From the repository root, reproduce the six Python checks with:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/audit/test_independent_audit.py
```

Using the existing Lean environment, reproduce the four formal checks with:

```sh
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean "$PWD/qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/audit/SharedPreservationFormal.lean"
```

Both commands passed, and their bounded recorded reruns passed. Full argv,
base revision, dirty state, before/after input hashes, runtime, and output
hashes are in `run_python_001/manifest.json` and `run_lean_001/manifest.json`.
Their stdout/stderr preserve the actual results. Each run had a 60-second
wall timeout and 1 MiB combined log cap. The Python run requested one numerical
library thread, a cooperative restriction rather than a hard CPU limit.
No memory or CPU-time limit was imposed. Both manifests validate with input
freshness checking against the repository root.

Environment: Python child 3.9.6, SymPy 1.14.0, NumPy 1.26.2, SciPy 1.11.4,
mpmath 1.3.0; provenance runner Python 3.11.13. Lean 4.34.0-rc2,
Lake 5.0.0-src+6a10ac8, Mathlib revision
`85e3a25e006c35636f0e53b0e9296caca2685bc0`. No randomness is used.

Audit methods: proof audit, computation audit, exact-version literature
check, and mathematical self-proofreading of these new artifacts.
