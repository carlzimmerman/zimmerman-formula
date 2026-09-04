# HPI-Delta full static-spherical action audit

Status: **DEAD under isolated static classical regular-center requirements**.

This audit answers the narrow loophole left by the earlier weak-static HPI-Delta
calculation: retaining and varying the radial shift and elliptic multiplier does
not regularize a smooth positive-density center on the isolated, momentum-free
branch. The result is derived from the same nonlinear ADM action rather than by
inserting the AQUAL equation phenomenologically.

## 1. Claim card and scope

The action is

\[
S=\frac{M_{\rm Pl}^2}{2}\int dt\,d^3x\,N\sqrt h
\left[
\bar K_{ij}\bar K^{ij}-\bar K^2+{}^{(3)}R-2\Lambda
-\frac{2}{\ell_0^2}F_{\exp}(y)
\right]+S_m[g,\psi],
\]

\[
\bar K_{ij}=K_{ij}-\frac{D^2\lambda}{2N}h_{ij},\qquad
y=\ell_0\sqrt{h^{ij}D_i\ln N D_j\ln N},
\]

\[
F_{\exp}(y)=2[(1+y)e^{-y}-1].
\]

The proved statement assumes:

- unitary clock gauge with timelike clock gradient;
- a spherically symmetric, isolated, asymptotically static branch;
- no radial matter momentum;
- no point charge for the multiplier equation;
- a regular center and finite auxiliary action;
- continuous central density and pressure, with
  \(p_r(0)=p_t(0)=p_c\).

The result does **not** establish a full nonlinear Dirac theorem, boosted PPN
parameters, global stability, a nonspherical external-field theorem, or the
absence of a cosmological constant-mean-curvature branch. No global novelty
claim is made.

All relativistic equations below use \(c=1\). Section 7 restores ordinary units
for the central acceleration law.

## 2. Reduction before gauge fixing

The minimal unitary-clock ADM ansatz is

\[
ds^2=-N(t,r)^2dt^2+A(t,r)^2[dr+\beta(t,r)dt]^2
+R(t,r)^2d\Omega^2,
\qquad \lambda=\lambda(t,r).
\]

The time-dependent extrinsic-curvature eigenvalues are

\[
\kappa_r=\frac1N\left(\frac{\dot A}{A}-\beta'
-\beta\frac{A'}A\right),\qquad
\kappa_t=\frac1N\left(\frac{\dot R}{R}-\beta\frac{R'}R\right).
\]

The program varies all five invariant fields in the static specialization:

\[
\kappa_r=-\frac{\beta'+\beta A'/A}{N},\qquad
\kappa_t=-\frac{\beta R'}{NR}.
\]

Define

\[
q=D^2\lambda
=\frac1{AR^2}\left(\frac{R^2}{A}\lambda'\right)',
\qquad
\bar\kappa_a=\kappa_a-\frac{q}{2N}.
\]

The exact spatial curvature and reduced kinetic scalar are

\[
{}^{(3)}R=\frac2{R^2}\left[
1-\frac{R'^2}{A^2}-\frac{2RR''}{A^2}
+\frac{2RR'A'}{A^3}
\right],
\]

\[
\bar K_{ij}\bar K^{ij}-\bar K^2
=-4\bar\kappa_r\bar\kappa_t-2\bar\kappa_t^2.
\]

Thus, apart from the positive angular and Planck-mass factor, the static radial
integrand is

\[
{\cal L}_g=NAR^2\left[
-4\bar\kappa_r\bar\kappa_t-2\bar\kappa_t^2
+{}^{(3)}R-2\Lambda-\frac2{\ell_0^2}F_{\exp}(y)
\right].
\]

Neither \(R=r\), \(\beta=0\), \(q=0\), nor no slip is inserted before
variation. The displayed time-dependent convention anchors the signs, but the
program does not independently vary the full time-dependent spherical action.
It evaluates the attractive one-sided radial branch \(N'>0\); the covariant
definition of \(y\) contains \(|N'|\).

## 3. The shift and multiplier do not furnish an isolated regular branch

The higher-derivative Euler operator applied to the displayed action gives

\[
\boxed{
E_\lambda=2\left(\frac{R^2}{A}\bar K'\right)'=0
},\qquad
\bar K=\bar\kappa_r+2\bar\kappa_t,
\]

and, for zero radial matter momentum,

\[
\boxed{
E_\beta=4AR\left[
R'(\bar\kappa_r-\bar\kappa_t)-R\bar\kappa_t'
\right]=0
}.
\]

The script compares these factored expressions with direct Euler variation;
both residuals vanish identically.

The multiplier equation first integrates to

\[
\frac{R^2}{A}\bar K'=C_\lambda.
\]

The flux through a vanishing sphere is \(4\pi C_\lambda\). A nonzero value is a
delta-function source absent from the action, so a distributionally source-free
center has \(C_\lambda=0\) and \(\bar K=K_0\). The momentum equation then gives

\[
\bar\kappa_t=\frac{K_0}{3}+\frac{C_s}{R^3},\qquad
\bar\kappa_r=\frac{K_0}{3}-\frac{2C_s}{R^3}.
\]

The \(C_s\) mode makes the radial auxiliary action density scale as \(r^{-4}\)
and is not finite at the center. Isolated asymptotically static data set
\(K_0=0\). Therefore \(\bar K_{ij}=0\).

The remaining equality \(\kappa_r=\kappa_t\) integrates to

\[
\beta=C_\beta\frac{R}{A}.
\]

Asymptotic \(\beta\to0\), \(R\to\infty\), and \(A\to1\) require
\(C_\beta=0\). It follows that \(\beta=0\), \(q=0\), and a regular solution of
\(q=0\) has constant \(\lambda\). Hence the auxiliary-flat static branch is a
consequence of both variations and the stated boundary conditions; it is not a
preselected ansatz.

The surviving \(K_0\ne0\) possibility is a non-isolated CMC branch and is not
excluded here.

## 4. Exact metric equations

On the derived isolated branch, the curvature term can be integrated by parts.
The program verifies the discarded expression is exactly a radial total
derivative. The first-order integrand is

\[
{\cal L}_{g,0}=2NA+\frac{2NR'^2}{A}+\frac{4N'RR'}A
-2\Lambda NAR^2-\frac{2NAR^2}{\ell_0^2}F(y).
\]

Restricting to this branch before displaying the metric equations loses no
metric equation: the program first varies the complete barred-kinetic radial
integrand with respect to (N,A,R), and only then substitutes
\(\beta=0\) and constant \(\lambda\). All three kinetic Euler derivatives
vanish identically there. This is also immediate from the fact that the
barred-kinetic scalar and its first derivative vanish at
\(\bar K_{ij}=0\), but the executable checks the full reduced expressions.

Let

\[
H(y)=F(y)-yF'(y),\qquad F'(y)=-2ye^{-y}.
\]

Independent variation of \(N,A,R\) gives

\[
{}^{(3)}R-2\Lambda-\frac{2H}{\ell_0^2}
+\frac{2}{\ell_0AR^2}(R^2F')'=16\pi G\rho,
\]

\[
1-\frac{R'^2}{A^2}-\frac{2RR'N'}{A^2N}
-\Lambda R^2-\frac{R^2H}{\ell_0^2}
=-8\pi Gp_rR^2,
\]

and

\[
4\frac{N'R'}A
-\frac{d}{dr}\left(\frac{4NR'}A+\frac{4N'R}A\right)
-4NAR\left(\Lambda+\frac{F}{\ell_0^2}\right)
=-32\pi GNARp_t.
\]

Every displayed geometric left side is independently compared with an Euler
derivative of the reduced action.

The exact radial-diffeomorphism identity is

\[
N'E_N+R'E_R+\lambda'E_\lambda+A'E_A+\beta'E_\beta
-(AE_A)'+(\beta E_\beta)'=0.
\]

The code verifies the metric and full barred-kinetic pieces separately. This is
the required control for imposing areal gauge only after variation.

## 5. Full-action regular-center obstruction

Set \(R=r\) only now, and let \(u=\ln N\). A classical \(C^2\) center has

\[
u'=u_1r+o(r),\qquad A=1+a_2r^2+o(r^2).
\]

The exact radial and lapse equations respectively require

\[
2(a_2-u_1)-\Lambda=-8\pi Gp_c,
\]

\[
12(a_2-u_1)-2\Lambda=16\pi G\rho_0.
\]

Eliminating \(a_2-u_1\) gives

\[
\boxed{4\pi G(\rho_0+3p_c)=\Lambda}.
\]

This is incompatible with an ordinary positive-density baryonic center when
the cosmological term is negligible. It is an action-level result and does not
assume the weak AQUAL equation as an independent premise.

## 6. The actual Puiseux branch and invariant singularity

On the attractive branch the exact equations instead select

\[
u'=c\sqrt r+dr+\cdots,
\qquad
A=1+cr^{3/2}+a_2r^2+\cdots.
\]

The two independently varied metric equations give

\[
a_2-d=\frac{\Lambda-8\pi Gp_c}{2},
\]

\[
\boxed{
c^2=\frac{4\pi G(\rho_0+3p_c)-\Lambda}{3\ell_0}
}.
\]

The constant central lapse \(N_0\) cancels because the constitutive invariant
contains \(N'/N\). Its asymptotic normalization cannot change the local result.

The curvature engine constructs Christoffel symbols and the Riemann tensor from
the four-dimensional metric. It does not enter the desired coefficients as
inputs. It obtains

\[
\boxed{
{}^{(4)}R\sim\frac{5c}{\sqrt r}
},\qquad
\boxed{
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
\sim\frac{43c^2}{r}
}.
\]

The scalar divergence is therefore not a coordinate artifact. The same engine
returns \(R=0\), \({\cal K}=48M^2/r^6\) for Schwarzschild and
\(R=12H^2\), \({\cal K}=24H^4\) for static de Sitter.

## 7. Central acceleration relation

Restoring ordinary units, writing \(\rho_m\) for mass density, and denoting the
speed of light by \(c_{\rm light}\) to distinguish it from the Puiseux
coefficient gives

\[
\boxed{
\lim_{r\to0}\frac{g^2}{r}
=\frac{4\pi Ga_0}{3}
\left(\rho_m+\frac{3p_c}{c_{\rm light}^2}\right)
-\frac{a_0c_{\rm light}^2\Lambda}{3}
}.
\]

For nonrelativistic matter and negligible \(\Lambda\), this reduces to the
previously derived central MOND relation. The pressure and cosmological terms
are the relativistic action-level completion, not a new viable theory: the same
coefficient produces the invariant curvature singularity above.

## 8. Live negative controls

The executable includes mutations capable of changing the result:

1. Setting \(F=0\) restores the regular GR center,
   \[
   a_2=\frac{4\pi G\rho_0}{3}+\frac{\Lambda}{6},\qquad
   u_1=\frac{4\pi G(\rho_0+3p_c)}3-\frac{\Lambda}{3}.
   \]
2. Replacing \(F\) by \(F+\epsilon y^2\), which makes
   \(\mu(0)=\epsilon>0\), gives a finite Taylor coefficient. It regularizes the
   center only by changing the demanded exact law.
3. Replacing \(D^2\lambda\) by coordinate \(\lambda''\) produces a nonzero
   radial-Noether defect.
4. Replacing the load-bearing \(-3b^2/2\) term by \(-b^2\) fails the trace-
   momentum constraint derivative.
5. Setting the shift to zero before variation makes its Euler equation vanish
   identically and therefore cannot establish the isolated branch.
6. A nonzero harmonic multiplier flux is detected as an unprovided central
   charge, and the \(R^{-3}\) traceless mode is detected as non-finite action.

## 9. Interpretation

This computation removes the specific objection that the earlier regular-center
no-go might have resulted from setting the HPI-Delta radial shift or multiplier
to zero too early. Both variables are now retained, varied, and eliminated only
by their own equations plus explicit isolated-boundary assumptions.

The strongest safe classification is therefore:

> **HPI-Delta is dead as an isolated static exact-exponential MOND theory with a
> classical regular positive-density center.**

It remains logically possible to change the law at zero field, accept a
nonclassical weak metric, add a central multiplier charge, use a nonspherical
external field, or construct a cosmological CMC embedding. Each option leaves
at least one stated target assumption or requires a new calculation.

## 10. Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_hpi_delta_full_spherical_2026.py
PYTHONDONTWRITEBYTECODE=1 python3 hpi_delta_full_spherical_2026.py
```

The center calculation uses the exact Taylor jet of \(F_{\exp}\) required for
the displayed coefficients. All load-bearing algebra is exact SymPy arithmetic;
there is no random sampling or floating tolerance.
