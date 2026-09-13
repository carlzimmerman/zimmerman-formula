# Local single-⁠`F(Y)` elliptic-sector audit

Date: 2026-09-12  
Status: **conditional obstruction, not a universal no-go**

This bundle audits the restricted preferred-foliation action

\[
 S_F=\int dt\,d^3x\;N\sqrt h\,F(Y),\qquad
 Y=h^{ij}D_i\chi D_j\chi .
\]

The calculation holds the foliation fixed on the static branch (zero shift),
retains the Einstein-Hilbert weak-field curvature equations, and assumes that
there is no independent anisotropic stress which cancels the Hilbert stress of
`F(Y)`.  These restrictions matter: varying a dynamical clock, adding a
second field, a multiplier, nonlocal boundary data, or a stress-canceling
operator is outside this certificate.

## Action variation

Allowing an external/source term `J chi` only to display the required source
structure gives

\[
 S_F+S_J=\int N\sqrt h\,[F(Y)+J\chi].
\]

Since

\[
 \delta Y=2D^i\chi\,D_i\delta\chi,
\]

integration by parts gives the Euler-Lagrange equation

\[
 \boxed{
 {1\over N\sqrt h}\partial_i\!\left(2N\sqrt h\,F_YD^i\chi\right)=J
 }.
\]

The bare `F(Y)` sector has `J=0`; therefore it cannot produce a baryonic
right-hand side by itself.  A mixing or source term is already an additional
architectural ingredient.  If the carrier is identified with the physical
potential, \(\chi=\Phi\), the desired flux normalization requires

\[
 2F_Y(Y)=\mu(\sqrt Y/a_0).
\]

For the requested exponential law this is

\[
 F_Y={1-e^{-y}\over2},\qquad y={\sqrt Y\over a_0},
 \qquad F_{YY}={e^{-y}\over4a_0^2y}\quad(y>0).
\]

## Hilbert stress and the slip source

Varying the inverse spatial metric while holding the foliation fixed gives

\[
 \delta_h S_F=N\sqrt h\left(F_Y\chi_i\chi_j-rac12Fh_{ij}\right)
 \delta h^{ij}.
\]

With \(T_{ij}=-2(N\sqrt h)^{-1}\delta S/\delta h^{ij}\),

\[
 T^i{}_j=F\,\delta^i{}_j-2F_YD^i\chi D_j\chi,
 \qquad
 p_F=F-{2\over3}F_YY,
\]

and the traceless part is

\[
 \boxed{
 \Pi^i{}_j=-2F_Y\left(D^i\chi D_j\chi-rac13\delta^i{}_jY\right).
 }
\]

At any point with \(Y=q^2>0\), choose an orthonormal frame aligned with the
gradient.  Then

\[
 \Pi^i{}_j=
 \operatorname{diag}\left(-{4\over3}F_Yq^2,
          {2\over3}F_Yq^2,{2\over3}F_Yq^2\right),
 \qquad
 \Pi^1{}_1-\Pi^2{}_2=-2F_Yq^2.
\]

This is not removable by the isotropic `F` term.  For a strictly elliptic
MOND flux, \(F_Y\ne0\); hence this traceless stress is nonzero at every
nonzero-gradient point.

## Independent weak-field potentials

Write \(\varphi=\Phi/c^2\), \(\psi=\Psi/c^2\), and

\[
 ds^2=-(1+2\varphi)c^2dt^2+(1-2\psi)\delta_{ij}dx^idx^j.
\]

Direct static linearized curvature gives (in `c=1` normalization)

\[
 G^{(1)}_{00}=2\nabla^2\psi,
\]

\[
 G^{(1)}_{ij}=D_iD_j(\psi-\varphi)
             +\delta_{ij}\nabla^2(\varphi-\psi),
\]

\[
 (G^{(1)}_{ij})^{\rm TF}
 =\left(D_iD_j-\frac13\delta_{ij}\nabla^2\right)(\psi-\varphi).
\]

Thus the 00 and spatial-trace equations determine the two potentials
independently,

\[
 \nabla^2\Psi=4\pi G\rho_{\rm tot},\qquad
 \nabla^2(\Phi-\Psi)=12\pi Gp_{\rm tot}
\]

in units with the usual powers of `c` restored in \(\rho,p\).  The traceless
equation is separately

\[
 \left(D_iD_j-\frac13\delta_{ij}\nabla^2\right)(\Psi-\Phi)
 =8\pi G\,\Pi_{ij}^{\rm TF}
\]

up to the overall sign convention for `T`.  If \(\Phi=\Psi\), its left side
vanishes identically.  With ordinary dust anisotropic stress zero and no
other auxiliary counter-stress, the `F(Y)` term then requires

\[
 0=\Pi_{ij}^{\rm TF}.
\]

The aligned expression above proves this is incompatible with `Y>0` and
`F_Y != 0`.  Therefore:

\[
 \boxed{
 \text{minimal local single }F(Y)+\text{EH}+\text{no cancellation}
 \Longrightarrow \Phi=\Psi\text{ fails on a generic MOND gradient branch}.
 }
\]

This is a conditional no-go for the stated sector, not for the full research
program.  The existing York/QUMOND and multiplier lanes test related but
different carriers and cannot be merged into this result without redoing the
metric variation.

## Ellipticity and the Dirac split

Linearizing the flux gives the principal matrix

\[
 \mathcal P^{ij}=2F_Yh^{ij}+4F_{YY}D^i\chi D^j\chi .
\]

In the gradient-aligned orthonormal frame its transverse and longitudinal
eigenvalues are derived, not inserted,

\[
 \lambda_\perp=2F_Y,\qquad
 \lambda_\parallel=2F_Y+4YF_{YY}.
\]

For the exact exponential carrier,

\[
 \lambda_\perp=1-e^{-y},\qquad
 \lambda_\parallel=1+(y-1)e^{-y}.
\]

Both are positive for `y>0`, while \(\lambda_\perp\to0\) at `y=0`; the
zero-field point is therefore rank-degenerate in this sector.

Because the ADM Lagrangian has no \(\dot\chi\), the isolated scalar sector
has the primary constraint \(p_\chi=0\).  Preservation gives the elliptic
secondary constraint

\[
 C_\chi=(N\sqrt h)^{-1}\partial_i(2N\sqrt h F_YD^i\chi)-J=0.
\]

For a Fourier mode, the principal Poisson bracket is the scalar symbol

\[
 \{p_\chi(\mathbf k),C_\chi(-\mathbf k)\}
 =-\mathcal P(\mathbf k),
\]

with

\[
 \mathcal P(\mathbf k)=2F_Y|\mathbf k_\perp|^2
 +(2F_Y+4F_{YY}Y)k_\parallel^2.
\]

The computed 2-by-2 bracket block has determinant \(\mathcal P(\mathbf k)^2\).
For `k != 0` and strict ellipticity this block is invertible, so this isolated
elliptic variable is nonpropagating.  At `k=0`, \(\mathcal P=0\): the zero
mode must be treated as a global/boundary constraint and cannot be counted by
continuity from the finite-wavelength sector.  Coupling `chi` to a dynamical
metric, clock, or multiplier enlarges this Dirac matrix and is not certified
here.

## Reproduction and result

```text
python3 -B qwen_claude_field_theory/closure_2026/local_FY_slip_audit_2026/derive_local_FY_slip.py
python3 -B -m unittest -v qwen_claude_field_theory/closure_2026/local_FY_slip_audit_2026/test_local_FY_slip.py
```

Both commands were run in the shared checkout; the symbolic script reports
16/16 checks and the unit suite reports 3/3 tests.  The companion
`LocalFYSlip.lean` contains the algebraic stress, determinant, and nonzero
source lemmas.  A fresh compile in the repository-pinned Lake project exits 0;
the earlier curl/reservoir failure was an invocation/environment issue, not a
mathematical failure.  The Lean file has no `sorry` and uses only the standard
foundational axioms imported by Mathlib.

The precise next calculation is the enlarged metric-plus-clock Dirac matrix:
allow variation of the foliation normal and any source/multiplier that is meant
to cancel \(\Pi_{ij}^{\rm TF}\), then continue the brackets through tertiary
closure at `k=0` and `k != 0`.  That is the only route by which this conditional
obstruction can be escaped without simply abandoning the local `F(Y)` carrier.
