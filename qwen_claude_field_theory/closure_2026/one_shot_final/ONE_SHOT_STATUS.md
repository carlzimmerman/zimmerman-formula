# One-shot final status

## Outcome

No complete fried-chicken theory is established. The explicit
curvature-sourced QUMOND action tested here is **DEAD**, and the broader
existence question is **OPEN**.

The strongest result is a scoped action-class no-go derived from one action:

\[
S={1\over16\pi G}\int\!\sqrt{-g}\,[R-2\Lambda
-2\lambda(\Delta_h\chi-R_{\mu\nu}n^\mu n^\nu)
+2a_0^2Q(Y)]+S_m[g,\psi],
\]

with

\[
Q(y^2)=1-(1+y)e^{-y},\qquad 2Q_Y=e^{-y},\qquad
\mu(y)=1-e^{-y}.
\]

On a regular spherical branch at finite \(y>0\), the varied \(\chi\) equation
forces

\[
\lambda_r=-a_0y e^{-y}\ne0.
\]

The transverse-traceless principal action from the same ADM action is

\[
L_{TT}^{\rm principal}={1-2\lambda\over2}\dot h_{TT}^2
-{1\over2}(\nabla h_{TT})^2,
\qquad c_T^2={1\over1-2\lambda}.
\]

Exact luminality relative to the minimally coupled physical metric requires
\(\lambda=0\) pointwise and hence \(\lambda_r=0\). This contradicts the exact
MOND branch. The theorem does not depend on an assumed PPN value, a guessed
constraint rank, or the interpretation of a clock mode.

## What the same action does and does not establish

| Requirement | Derived result |
|---|---|
| Exact exponential MOND | Passes in the varied weak-static spherical branch; deep MOND and BTFR follow. |
| Newtonian recovery | \(\mu\to1\); the weak branch gives \(G_{\rm measured}=G_{\rm bare}\). |
| Matter conservation | Minimal, separately diffeomorphism-invariant \(S_m[g,\psi]\) gives \(\nabla_\mu T^{\mu\nu}=0\) on the matter equations. This is an analytic Ward consequence, not a numerical certification. |
| Linear no slip | The complete trace-free metric variation gives \(k^2(\Phi-\Psi)=0\) for \(k\ne0\), hence \(\gamma=1\). |
| Nonlinear no slip / \(\beta\) | Unresolved. The second-order equation sources a genuine second-order slip and must be solved with the other metric equations. |
| Preferred-frame PPN | A fixed foliation has a nonzero boosted diagnostic, but no complete \(\alpha_1,\alpha_2,\alpha_3\) extraction is claimed. |
| Tensor sector | Positive kinetic energy requires \(1-2\lambda>0\); exact MOND conflicts with exact \(c_T=1\). |
| Scalar/vector sector | On the special flat luminal finite-\(k\) branch the generated Dirac chain leaves one non-clock scalar with \(L_{\rm red}=6\dot\zeta^2-2k^2\zeta^2\); transverse vectors leave no pole. This is a branch result, not a generic nonlinear count. |
| FLRW | The multiplier equation permits coasting \(a=At+B\), including \(H\ne0\), but excludes acceleration on that branch. Full cosmological viability is not established. |
| \(y=0\) | The raw auxiliary pair retains its finite-\(k\) bracket, while the eliminated MOND response loses rank. No nonlinear zero-field evolution prescription is supplied. |
| \(a_0\)-\(\Lambda\) | External input, not derived. |

## Fable 5.1 comparison

The live generalized-AeST proposal does not satisfy the unchanged target:

- its own text reports two tensor, two vector, and one aether-scalar mode
  before the separate \(\phi\) clock, so the proposal's self-reported
  gravitational count is five rather than two;
- the literal displayed \(-2K(Q)\) DBI term gives negative vacuum energy and
  negative quadratic kinetic curvature at \(Q=Q_0\); and
- the sign of its written \(+c_2(\nabla\!\cdot A)^2\) term is inconsistent
  with the Foster-Jacobson \(c_2\) convention used by its printed scalar-speed
  formula.

Its proposed replacement of gate 2 by “all modes counted and healthy” is a
different target and is not accepted here. The clock-current proposal is also
dead for the strict target: minimally coupled baryons see the metric source
\(\rho_b+n\); ratio locking \(n\propto\rho_b\) preserves linear source scaling
instead of the deep-MOND square-root scaling.

The broader Fable claim that all local two-DOF architectures are exhausted is
not accepted as a theorem. The case split is informative, but it is not a
complete classification of all local covariant actions and constraint
algebras. Our result remains deliberately scoped.

## Correction to the nonlocal claim

The earlier flagship statement that nonlocal MOND universally requires an
independent dark field, and that a retarded denominator by itself establishes
`alpha_3=0` with no extra mode, is withdrawn. The fail-capable replacement
audit derives three sharper statements:

1. the exact local exponential-AQUAL action carries enclosed baryonic mass in
   its exterior solution as the integration constant
   \(r^2\mu(\Phi'/a_0)\Phi'=GM_b\), so enclosed-mass dependence alone does not
   force another field;
2. a strictly retarded triangular response cannot be the inverse Hessian of an
   ordinary one-copy action; and
3. the standard local multiplier representation has Hessian
   \(\begin{pmatrix}0&1\\1&0\end{pmatrix}\), no primary or secondary
   constraints, two configuration modes, and one negative kinetic direction
   in both the homogeneous and inhomogeneous sectors.

This kills that standard causal localization, not every possible in-in or
non-rational nonlocal construction. A full boosted 1PN metric solve is still
required before assigning `alpha_1`, `alpha_2`, or `alpha_3`.

## Latest published cluster-paper audit

The paper's original 27 checks reproduce its static polytrope and numerical
cluster-yield results. A new conservative audit narrows two phrases:

- \(\gamma=2\) is the controlled small-field limit, accurate at about
  \(10^{-5}\) for the stated cluster depth, rather than an exact finite-field
  EOS; and
- positivity fixes the first-zero radius and profile shape but leaves the
  central density and total captured mass free. The numerical attractor holds
  mass fixed and uses explicit artificial viscosity.

The defensible result is therefore **conditional pinning**: given captured mass
and a specified dissipative/shock prescription, the tested radial phases relax
near the corresponding positive polytrope. Conservative action-derived mass
selection remains open.

## High download/view record

The likely bimetric record is physically interesting because it contains a
derived MOND map and a proposed Boulware-Deser constraint mechanism. It is not
the strict finish: its advertised best gravitational count is \(7=2+5\), and
continuum closure, lensing, and full PPN remain open. The public API reported
one unique download and zero unique views on 2026-09-01. That sample is too
small to support an interest claim; a direct file, DOI, API, or bot fetch can
increment downloads without a landing-page view.

## Reproducible entry point

Run every command listed in `ONE_SHOT_COMMANDS.md`. A zero process status means
the stated derivation reproduced; it never changes a failed theory gate into a
physics pass.
