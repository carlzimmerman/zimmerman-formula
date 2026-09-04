# Arbitrary-slip extension of the exact-MOND center obstruction

Date: 2026-09-04

Verdict: **NO-GO under the stated center assumptions.**  The base repository
already contained the no-slip \(C^2\) center obstruction and a longer
exact-exponential inner-orbit series.  The new content here is the direct
four-dimensional arbitrary-slip Kretschmann calculation, its positive-square
noncancellation theorem, and the general source/kernel matching threshold
\(m\ge n\).  This is not a complete no-go for every relativistic MOND
architecture.

## 1. Assumptions and claim

Consider a smooth spherical source with

\[
 \rho(r)=\rho_0+O(r^2),\qquad \rho_0>0,
\]

and suppose the requested quasistatic law remains valid into its force-free
center:

\[
 {1\over r^2}{d\over dr}\left[r^2\mu(g/a_0)g\right]
 =4\pi G\rho(r).
\]

More generally, write the integrated source as

\[
 \mu(g/a_0)g=br+o(r),\qquad b>0,
\]

and let

\[
 \mu(y)=\kappa y^n+o(y^n),\qquad \kappa>0,\quad n>0.
\]

Assume the measured nonrelativistic acceleration is the lapse potential of a
single physical metric,

\[
 ds^2=-\left(1+{2\Phi\over c^2}\right)c^2dt^2
      +\left(1-{2\Psi\over c^2}\right)d\boldsymbol{x}^2+\cdots.
\]

Then no classical \(C^2\) metric exists at that center.  In fact, the
Kretschmann invariant diverges even if gravitational slip is allowed.  The
requested \(\Phi=\Psi\) branch is a particularly simple specialization, not
an assumption needed for the obstruction.

## 2. Universal center scaling

Balancing the integrated equation gives

\[
 s={1\over n+1},\qquad
 C=\left({b a_0^n\over\kappa}\right)^{1/(n+1)},
\]

\[
 \boxed{g(r)=C r^s+o(r^s)},\qquad
 \boxed{\Phi(r)-\Phi(0)={C\over s+1}r^{s+1}+o(r^{s+1})}.
\]

Because \(0<s<1\), the tangential Hessian eigenvalue
\(\Phi'/r\sim Cr^{s-1}\) diverges.  Thus a classical \(C^2\) physical metric
is already excluded without differentiating the little-\(o\) remainder.

More strongly, the componentwise tensor contraction with independent radial
Hessian eigenvalues gives the derivative-free lower bound

\[
 \boxed{
 R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
 \ge {8\over c^4}\left({\Phi'\over r}\right)^2
 \sim {8C^2\over c^4}r^{2s-2}.
 }
\]

The code obtains this by minimizing the derived curvature quadratic form over
\(\Phi''\), \(\Psi''\), and \(\Psi'/r\) at fixed \(\Phi'/r\); its Hessian is
positive definite.  Gravitational slip therefore cannot cancel the divergence
even when derivatives of the asymptotic remainder oscillate.

For the sharper coefficients below, add the regular-variation hypotheses
\(r\Phi''/\Phi'\to s\) and \(r\Psi''/\Psi'\to s\).  Write

\[
 \Phi'=C_\Phi r^s+o(r^s),\qquad
 \Psi'=C_\Psi r^s+o(r^s).
\]

Direct construction and contraction of the linearized four-dimensional
Riemann tensor then gives

\[
 \boxed{
 R={2(s+2)(2C_\Psi-C_\Phi)\over c^2}\,r^{s-1}+\cdots
 }
\]

and

\[
 \boxed{
 R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
 ={4r^{2s-2}\over c^4}
 \left[C_\Phi^2(s^2+2)
 +C_\Psi^2(2s^2+4s+6)\right]+\cdots .
 }
\]

The Ricci scalar can be tuned away at this order by
\(C_\Psi=C_\Phi/2\).  The Kretschmann coefficient is a sum of positive
squares and cannot be tuned away for real nonzero \(C_\Phi\).  If \(\Psi\)
is more regular, set \(C_\Psi=0\) and the first positive term remains.  If it
is more singular, the spatial contribution makes the metric at least as bad.
Connection-squared terms are subleading because first derivatives vanish as
\(r^s\), whereas second derivatives diverge as \(r^{s-1}\).

This establishes the following local alternative:

\[
 \boxed{
 \text{positive smooth center}+\mu(0)=0+\text{metric MOND acceleration}
 \ \Longrightarrow\ \text{curvature singularity}.
 }
\]

There is also a sharp necessary regularity-matching rule.  If the effective
spherical source vanishes as \(\rho_{\rm eff}\sim r^m\), then value
asymptotics alone give

\[
 g\sim r^{(m+1)/(n+1)},\qquad
 R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
 \ge {\rm const}\,r^{2(m-n)/(n+1)}.
\]

Therefore a necessary leading-order condition for finite curvature is

\[
 \boxed{m\ge n.}
\]

For ordinary MOND, \(n=1\): a constant positive core (\(m=0\)) gives at
least a \(1/r\) Kretschmann divergence, while an effective source that vanishes
at least linearly reaches the marginal necessary threshold.  The condition is
not sufficient for regularity; radial derivatives can still fail.  It gives
proposed regularizations a precise gate rather than the vague instruction to
smooth the zero-field point.

## 3. Exact exponential result

For \(\mu(y)=1-e^{-y}\), \(n=\kappa=1\).  With the exact target source,

\[
 b={4\pi G\rho_0\over3},\qquad
 C=\sqrt{{4\pi G a_0\rho_0\over3}}.
\]

The symbolic series inversion derives

\[
 \boxed{
 g(r)=\sqrt{a_0b}\,r^{1/2}
 +{b\over4}r
 +{7b^{3/2}\over96\sqrt{a_0}}r^{3/2}
 +O(r^2).
 }
\]

On the requested no-slip branch \(C_\Phi=C_\Psi=C\),

\[
 \boxed{R={5C\over c^2\sqrt r}+O(1)},
\]

\[
 \boxed{
 R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
 ={43C^2\over c^4r}+O(r^{-1/2})
 ={172\pi G a_0\rho_0\over3c^4r}+O(r^{-1/2}).
 }
\]

The same tensor builder returns \(R=0\) and the standard leading
Schwarzschild coefficient \(48G^2M^2/(c^4r^6)\) when supplied the weak
Schwarzschild potentials.  With physical Hubble parameter \(H\), the weak
isotropic de Sitter control returns \(R=12H^2/c^2\) and \(K=24H^4/c^4\)
(equivalently \(12H_{\rm geo}^2,24H_{\rm geo}^4\) for \(H_{\rm geo}=H/c\)).

## 4. Reproduced kernel-specific inner Kepler series

For a circular tracer, \(v_c^2=rg\).  Squaring the independently derived
Puiseux series reproduces the first terms of the longer series already in
`exact_mond_regular_center_no_go_2026`:

\[
 \boxed{
 {v_c^4\over r^3}
 =a_0b+{b\sqrt{a_0b}\over2}\sqrt r
 +{5b^2\over24}r+O(r^{3/2}).
 }
\]

For a constant-density baryonic core,

\[
 \boxed{
 \lim_{r\to0}{v_c^4\over r^3}={4\pi G a_0\rho_0\over3}.
 }
\]

This series is a regression control, not a new repository-level law.  Its
limiting square-root behavior is also part of the known central-MOND-spike
phenomenology.  It does not rescue a relativistic action: if \(\Phi\) is a
metric potential all the way to \(r=0\), the same prediction carries the
curvature obstruction above.

## 5. Meaning for the nonlocal/elliptic phantom-density route

An elliptic or retarded auxiliary architecture does **not** evade this result
merely by having no propagating scalar.  If its varied equations reproduce the
exact local MOND equation at an isolated positive-density center and ordinary
matter measures \(g=|\nabla\Phi|\) from one metric, the local output still has
the nonanalytic lapse and divergent tidal curvature.

A surviving action must therefore demonstrate at least one explicit escape:

1. modify or screen the MOND equation in a neighborhood of every force-free
   positive-density center;
2. give \(\mu\) a nonzero zero-field floor;
3. ensure the effective central source vanishes sufficiently rapidly;
4. use an external-field/nonlocal branch that prevents the total field from
   reaching zero, with boundary dependence derived from the action;
5. abandon metric motion for baryons; or
6. accept a singular/distributional center.

Options 1--4 must be reconciled with the request for the exact MOND law and a
controlled \(y=0\) limit.  Option 5 abandons the preferred one-metric/Ward
architecture.  Option 6 is not a healthy classical completion.

## 6. Computational contract and result

The symbolic computation tests the local series, source/kernel matching law,
and leading curvature over the exact rational/symbolic domain using SymPy
1.14.0.  Physical acceleration coefficients are converted to dimensionless
metric potentials by explicit factors of \(c^{-2}\).  It constructs the
linearized Riemann tensor component by component and contracts it; the values
5, 43, 48, 12, and 24 are test expectations, not assignments in the tensor
builder.

The independent numerical audit does not import the symbolic module.  At 80
decimal digits it solves

\[
 y(1-e^{-y})=x
\]

at ten logarithmically spaced points \(10^{-12}\le x\le10^{-3}\).  The
three-term root has measured relative-error slope 1.5000049962 and the scaled
error approaches 1/48; the maximum equation residual was
\(8.24\times10^{-84}\).

The bounded numerical run verifies the Puiseux approximation on that range;
it is not the proof of the asymptotic theorem.  The symbolic balance and
tensor contraction supply that argument under the stated assumptions.

## 7. Reproduction

```bash
python3 -m unittest -v \
  qwen_claude_field_theory/closure_2026/slipless_exact_mond_center_nogo_2026/test_slipless_exact_mond_center_nogo_2026.py

python3 \
  qwen_claude_field_theory/closure_2026/slipless_exact_mond_center_nogo_2026/slipless_exact_mond_center_nogo_2026.py \
  --output qwen_claude_field_theory/closure_2026/slipless_exact_mond_center_nogo_2026/calculation_results.json

python3 \
  qwen_claude_field_theory/closure_2026/slipless_exact_mond_center_nogo_2026/independent_numeric_audit.py \
  --json \
  --output qwen_claude_field_theory/closure_2026/slipless_exact_mond_center_nogo_2026/independent_numeric_results.json
```

Final observed status for all three commands: **0**.
The standalone symbolic program is a result renderer whose exit status is
computed from six live symbolic predicates; the unit suite, not the printed
classification string, is the adversarial certificate.

The first test-first run, before the derivation module existed, exited 1 with
one intentional failure.  Separate red runs also caught the ambiguous power
labels, missing general-\(n\) theorem, missing arbitrary-slip theorem, and
missing independent numerical audit before each implementation was added.
After review, further red runs caught the missing explicit \(c\) scaling, the
uncontrolled differentiation of a little-\(o\) remainder, the lack of a stored
numeric artifact, and an unconditional renderer exit before those defects were
repaired.
