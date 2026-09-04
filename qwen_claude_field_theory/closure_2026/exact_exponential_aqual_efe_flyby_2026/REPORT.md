# Exponential-AQUAL external-field flyby and scattering laws

Date: 2026-09-04

Verdict: **PASS_NONRELATIVISTIC_EFD_SCATTERING_CALCULATION; NOT a
relativistic completion.**  The generic three-dimensional result below is an
exact evaluation of the straight-line (first-Born) integral, not the exact
curved scattering map.  The equatorial result is exact for arbitrary
eccentricity and deflection angle within the linear external-field-dominated
(EFD) potential.  None of these statements supplies the missing covariant
action, PPN, constraint, or stability gates.

The defensible novelty statement is deliberately narrow: the full vector
impulse tensor, its azimuth bounds, and its small-angle cross-section are a
repository-new formal observable corollary of the known AQUAL EFD Green
function.  No global priority claim is made.  The static force-axis
`sqrt(q)` ratio and the existence of the EFD potential predate this bundle;
the exact equatorial conics reduce to the ordinary Kepler problem and are
also not claimed as new mathematics.

## 1. Action, variation, and EFD point potential

Start from the nonrelativistic AQUAL action

\[
 S_{\rm AQUAL}=-\int dt\,d^3x\left[
 {a_0^2\over8\pi G}{\cal G}\!\left({|\nabla\Phi|\over a_0}\right)
 +\rho\Phi\right],
\]

with the exact primitive

\[
 {\cal G}(y)=y^2+2(1+y)e^{-y}-2,
 \qquad {{\cal G}'(y)\over2y}=1-e^{-y}\equiv\mu(y).
\]

Direct variation gives

\[
 {\partial {\cal L}\over\partial(\partial_i\Phi)}
 =-{1\over4\pi G}\mu(|\nabla\Phi|/a_0)\partial_i\Phi,
\]

and therefore

\[
 \nabla\!\cdot\!\left[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi\right]
 =4\pi G\rho.
\]

Linearize about a constant external field of magnitude `g_e` and unit
direction \(\mathbf e\).  Define

\[
 \eta={g_e\over a_0},\qquad
 \mu_e=1-e^{-\eta},\qquad
 L_e={\eta\over e^\eta-1},\qquad q=1+L_e.
\]

The flux Jacobian has eigenvalues \(\mu_e\) transverse to \(\mathbf e\)
and \(\mu_e q\) parallel to it.  With \(\mathbf e=\hat{\mathbf z}\),

\[
 \mu_e(\partial_x^2+\partial_y^2+q\partial_z^2)\phi=4\pi G\rho.
\]

For a point mass, introduce

\[
 C={GM\over\mu_e},\qquad
 A=qI-(q-1)\mathbf e\mathbf e^{T}.
\]

The Green solution and test-particle acceleration are

\[
 \boxed{\phi(\mathbf r)=-{C\over\sqrt{\mathbf r^T A\mathbf r}}},
 \qquad
 \boxed{\ddot{\mathbf r}=-{C A\mathbf r\over
 (\mathbf r^T A\mathbf r)^{3/2}}}.
\]

For finite \(\eta>0\), \(1<q<2\) and the EFD operator is elliptic.  At
exactly \(\eta=0\), \(\mu_e=0\): only finite one-sided ratios are retained,
not an absolute potential or an elliptic boundary-value problem.

## 2. Exact first-Born impulse tensor in three dimensions

Let the unperturbed trajectory be

\[
 \mathbf r_0(t)=\mathbf b+v_\infty t\,\mathbf n,
 \qquad |\mathbf n|=1,\qquad \mathbf n\cdot\mathbf b=0.
\]

Define the Gram data

\[
 a=\mathbf n^T A\mathbf n,\qquad
 d=\mathbf n^T A\mathbf b,\qquad
 B=A-{(A\mathbf n)(A\mathbf n)^T\over a},
 \qquad D=\mathbf b^T B\mathbf b.
\]

Because \(A\) is positive definite and \(\mathbf b\ne0\) lies in the
impact plane, \(D>0\).  Completing the square gives

\[
 \mathbf r_0^TA\mathbf r_0
 =a\left(v_\infty t+{d\over a}\right)^2+D.
\]

The shifted odd term integrates to zero and

\[
 \int_{-\infty}^{\infty}{ds\over(as^2+D)^{3/2}}
 ={2\over\sqrt a\,D}.
\]

Thus the full vector kick is

\[
 \boxed{
 \Delta\mathbf v_{\rm B}
 =-{2C\over v_\infty\sqrt a\,D}
 A\left(\mathbf b-\mathbf n{d\over a}\right)
 =-{2C\over v_\infty\sqrt a\,D}B\mathbf b .}
\]

This is coordinate free.  It includes the trajectory displacement caused by
the \(A\)-metric cross term; dropping either that displacement or the Schur
term \(d^2/a\) is wrong for generic geometry.  Since \(B\mathbf n=0\),

\[
 \boxed{\mathbf n\cdot\Delta\mathbf v_{\rm B}=0}
\]

exactly at first Born order.  Energy conservation produces only a
longitudinal change at the next order.

## 3. The exact geometry clause behind `sqrt(q)`

Let \(\theta\) be the angle between \(\mathbf n\) and \(\mathbf e\).  For
nonparallel directions, choose \(\mathbf e_\varphi\) in the impact plane
perpendicular to both and \(\mathbf e_\theta\) in their common plane; at
parallel alignment either transverse orthonormal basis gives the continuous
limit.  Then

\[
 a=\cos^2\theta+q\sin^2\theta,
 \qquad
 B\mathbf e_\varphi=q\mathbf e_\varphi,
 \qquad
 B\mathbf e_\theta={q\over a}\mathbf e_\theta.
\]

For a Euclidean impact magnitude \(b\) and azimuth

\[
 \mathbf b=b(\cos\varphi\,\mathbf e_\varphi
                  +\sin\varphi\,\mathbf e_\theta),
\]

the kick magnitude is

\[
 |\Delta\mathbf v_{\rm B}|={2C\over v_\infty b\sqrt a}
 F(a,\varphi),
\]

where

\[
 \boxed{F(a,\varphi)=
 {\sqrt{\cos^2\varphi+\sin^2\varphi/a^2}
  \over \cos^2\varphi+\sin^2\varphi/a}},
\]

and

\[
 1\le F(a,\varphi)\le {a+1\over2\sqrt a}.
\]

The upper bound is attained at \(\tan^2\varphi=a\).  Therefore the often
quoted ratio

\[
 {|\Delta\mathbf v|_{\mathbf n\parallel\mathbf e}\over
  |\Delta\mathbf v|_{\mathbf n\perp\mathbf e}}=\sqrt q
\]

is exact only when the two encounters have the same \(M,\mu_e,b,v_\infty\)
and the perpendicular encounter's impact vector lies on either principal
impact axis (\(\varphi=0\) or \(\pi/2\)).  For a generic azimuth,

\[
 \boxed{{|\Delta\mathbf v|_\parallel\over
 |\Delta\mathbf v|_\perp(\varphi)}={\sqrt q\over F(q,\varphi)}},
 \qquad
 {2q\over q+1}\le {\sqrt q\over F(q,\varphi)}\le\sqrt q.
\]

At the deep-EFD ratio limit \(q\to2\), this directional contrast spans
\(4/3\) to \(\sqrt2\), rather than being universally \(\sqrt2\).  The
largest generic-azimuth increase over a principal kick is only
\(3/(2\sqrt2)-1=6.066\%\), but it matters when stating an exact law.

The kick need not point along \(-\mathbf b\).  Its misalignment obeys

\[
 \tan\delta={|(a-1)\tan\varphi|\over a+\tan^2\varphi},
 \qquad
 \boxed{\delta\le\arcsin\!\left({a-1\over a+1}\right)}.
\]

The maximum again occurs at \(\tan^2\varphi=a\).  Globally over exponential
AQUAL, \(a\le2\), so \(\delta\le\arcsin(1/3)=19.4712206^\circ\).

## 4. Generic anisotropic Rutherford law at small angle

Let \((\vartheta_\varphi,\vartheta_\theta)\) be the two small deflection
components in the principal impact-plane basis.  The Born map is

\[
 \boldsymbol\vartheta=-\ell{B\mathbf b\over\mathbf b^TB\mathbf b},
 \qquad \ell={2C\over v_\infty^2\sqrt a}.
\]

Its actual two-by-two Jacobian is

\[
 \det{\partial\boldsymbol\vartheta\over\partial\mathbf b}
 =-{\ell^2\det B\over(\mathbf b^TB\mathbf b)^2},
\]

where \(B\) denotes the restriction to the impact plane.  Inverting the map,
using its eigenvalues \((q,q/a)\), and identifying
\(d\Omega=d\vartheta_\varphi d\vartheta_\theta+O(\vartheta^2)\) yields

\[
 \boxed{{d\sigma\over d\Omega}\simeq
 {4C^2\over v_\infty^4
 (\vartheta_\varphi^2+a\vartheta_\theta^2)^2}}.
\]

This is an anisotropic, small-angle Rutherford law.  It is not licensed for
large generic three-dimensional deflections.

## 5. Exact invariant equatorial Kepler sector

Set \(\mathbf e=\hat{\mathbf z}\).  The plane \(z=0,\dot z=0\) is an exact
invariant submanifold because the vertical force is proportional to \(z\).
On it,

\[
 \phi(R,0)=-{C\over\sqrt q\,R}=-{k_e\over R},
 \qquad \boxed{k_e={GM\over\mu_e\sqrt q}}.
\]

Consequently every orbit in that plane is an ordinary Kepler conic, exactly
within the EFD Green potential.  With specific angular momentum \(h_z\),

\[
 \boxed{R(f)={p\over1+e\cos f}},\qquad
 p={h_z^2\over k_e}.
\]

For a finite-eccentricity bound ellipse,

\[
 p=a_{\rm orb}(1-e^2),\qquad
 E=-{k_e\over2a_{\rm orb}},\qquad
 \boxed{P^2={4\pi^2a_{\rm orb}^3\over k_e}}.
\]

This extends the circular timing anchor already recorded in the neighboring
`exact_exponential_aqual_efe_kepler_2026` bundle to all equatorial bound
conics; it does not supersede that bundle's genuinely three-dimensional
finite-anisotropy analysis.

For an equatorial hyperbolic encounter with asymptotic speed \(v_\infty\)
and impact parameter \(b\),

\[
 e=\sqrt{1+{b^2v_\infty^4\over k_e^2}},
 \qquad
 \boxed{\tan{\Theta\over2}={k_e\over b v_\infty^2}}.
\]

The usual area-to-solid-angle calculation is now exact at every scattering
angle:

\[
 \boxed{{d\sigma\over d\Omega}
 ={k_e^2\over4v_\infty^4\sin^4(\Theta/2)}}.
\]

This exact special-plane result must not be conflated with the generic 3-D
Born tensor in sections 2--4.

## 6. Independent computational falsification attempts

Three independent layers can fail:

1. `test_exact_exponential_aqual_efe_flyby_2026.py` checks hand-integrated
   principal cases, a separate improper quadrature, generic transversality,
   isotropic recovery, the corrected azimuth clause, the misalignment bound,
   the small-angle law, exact equatorial conics/scattering, and invalid input.
2. `symbolic_impulse_audit.py` derives the scalar line integral, Schur
   eigensystem, azimuth extremum, misalignment extremum, Born-map Jacobian,
   anisotropic cross-section, invariant plane, Binet conic, and exact
   Rutherford formula.  It also differentiates the exponential primitive.
3. `independent_flyby_audit.py` does not import the production module.  It
   compares 96 deterministic random 3-D improper quadratures to a separately
   coded closed expression; tests four algebraic mutations; finite-differences
   24 scattering-map Jacobians; integrates 147 curved paths; halves the Born
   parameter at the worst grid point; monitors energy and axial angular
   momentum; and integrates a full equatorial hyperbola against the exact law.

In the recorded run, the random line-integral error was below
\(6.9\times10^{-16}\), the finite-difference Jacobian error was below
\(7.0\times10^{-11}\), and every deliberate mutation missed by more than
\(1.5\%\).  On the declared curved-path grid

\[
 q\in\{1.1,1.5,1.99\},\quad
 \theta,\varphi\in\{0^\circ,15^\circ,\ldots,90^\circ\},\quad
 h={C\over b v_\infty^2}=0.002,
\]

the largest relative transverse Born error was \(0.590\%\).  Halving \(h\)
halved the worst error to within \(0.2\%\) of the expected ratio, evidence
for a generic relative \(O(h)\) post-Born correction.  This finite grid is a
calibration, not a uniform theorem.  The stored JSON files contain the exact
machine outputs and solver settings.

## 7. Validity envelope and non-claims

All absolute formulas require \(\eta>0\), \(\mu_e>0\), and a source small
relative to the encounter distance.  The EFD approximation requires the
internal field to remain much smaller than \(g_e\) over the whole trajectory.
A useful order-of-magnitude condition is

\[
 b\gg\sqrt{C/g_e};
\]

in the deep external-field limit this becomes
\(b\gg\sqrt{GMa_0}/g_e\), up to order-one geometry factors.  For exact
equatorial strong scattering, this condition must be checked at periapsis,
not merely at the asymptotic impact parameter.

The generic impulse and cross-section additionally require
\(h=C/(b v_\infty^2)\ll1\).  The external field must be approximately
constant in magnitude and direction over the encounter.  The numerical EFD
examples demonstrate that the EFD and Born inequalities have a nonempty
joint regime; they do not certify a named astronomical encounter or bound
the nonlinear-AQUAL remainder.

This bundle does **not** derive or certify:

- a covariant relativistic action;
- \(N_{\rm grav}=2\), \(\Phi=\Psi\), PPN parameters, or a Dirac algebra;
- matter Ward identities, gravitational-wave propagation, FLRW, or stability;
- the nonlinear transition out of EFD;
- a universal flyby anomaly, observational detection, or global novelty;
- ellipticity or an absolute impulse at exactly \(g_e=0\).

## 8. Reproduction

From the repository root, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/exact_exponential_aqual_efe_flyby_2026.py --output qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/calculation_results.json
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/symbolic_impulse_audit.py --output qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/symbolic_impulse_results.json
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/independent_flyby_audit.py --output qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_flyby_2026/independent_flyby_results.json
```

The manifest pins the source and output bytes, the base commit, software
versions, deterministic seeds, solver tolerances, tested ranges, and explicit
non-claims.
