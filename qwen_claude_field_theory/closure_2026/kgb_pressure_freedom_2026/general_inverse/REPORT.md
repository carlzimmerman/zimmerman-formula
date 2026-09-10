# General-pressure static inverse

Requested base: `de9cc54`; execution HEAD initially
`a696e9ca72a4d6273eccfed32ce73f6319f84858`. Only new files in this directory
were edited. The parent aggregate records final hashes and provenance.

The same action is retained:
\(F(X)R+3F_X^2(\nabla X)^2/(2F)+P(X)-G(X)\Box\phi\), with physical
minimal matter, an explicit clock \(\phi=q t+\psi(r)\), and one global
constant \(a_0\) as units. No particles or new action terms are introduced.
All equation checks here concern exterior vacuum and the regular invertible
EF map; no CMB, observational, full-Hamiltonian or mode-count claim is made.

## Arbitrary metric input and actual 3 by 3 inverse

Let \(g=A'/(2A),z=X',f=F_X,j=F_{XX},U=p^2/B,p=\psi',Q=2X+U\).
Input \((r,B,B',g,g')\), not an imposed radial pressure. `metric_invariants`
computes

\[
\rho=\frac{1-B^{-1}}{r^2}+\frac{B'}{B^2r},\quad
p_r=\frac{B^{-1}-1}{r^2}+\frac{2g}{Br},\quad
p_t=\frac{g'+g^2-gB'/(2B)+(g-B'/(2B))/r}{B}.
\]

The derivative of the displayed \(p_r\) gives \(p_r'\); it requires no
\(B''\). The geometric identity
\(p_r'+g(\rho+p_r)-2(p_t-p_r)/r=0\) is verified symbolically.
Set \(a=g+2/r,b=B'/(2B),K=3f^2/(2F)\),
\(K_X=3fj/F-3f^3/(2F^2)\). The radial equation is

\[
P=2Fp_r+N/B,\quad N=2fza+Kz^2,\quad P_z=(2fa+2Kz)/B.
\]

Its true explicit radial derivative is

\[
R_0=2fzp_r+2Fp_r'+
\frac{2jz^2a+K_Xz^3+2fz(g'-2/r^2)}B-\frac{NB'}{B^2}.
\]

Define

\[
\begin{split}
C_J&=2(U/r-Xg)/p,\\
A_\chi&=f(\rho-p_r-2p_t)-K_Xz^2/B-2K(g-b+2/r)z/B,\\
L&=2F\rho+P-2f(2/r-b)z/B+(K-2j)z^2/B.
\end{split}
\]

The total current, density equation, and constitutive preservation give

\[
\begin{pmatrix}
P_z&-z&0\\ -2K/B&1&-C_J\\ 2f/B&0&2Xz/p
\end{pmatrix}
\begin{pmatrix}z'\\P_X\\G_X\end{pmatrix}
=\begin{pmatrix}-R_0\\-A_\chi\\L\end{pmatrix}.
\]

The determinant is **computed from this matrix**, then simplified to
\(4fzQ/(Bpr)\); the numerical solve also computes its own determinant.
The physical angular equation follows after these rows and the actual
geometric identities are substituted. It is checked, not imposed as an
extra adjustable equation. In particular the Ricci term is
\(\rho-p_r-2p_t\), and using the old \(\rho-2p_t\) fails the current
regression test when pressure is nonzero.

## Normalized chart available for joint reconstruction

`normalized(geometry,X,U,w,F)` uses \(w=fz,W=w'\),
\(\kappa=P_X/f,\Gamma=G_X/f\). It solves

\[
\begin{pmatrix}
P_w&-w&0\\-3/(FB)&1&-C_J\\2/B&0&2Xw/p
\end{pmatrix}
\begin{pmatrix}W\\\kappa\\\Gamma\end{pmatrix}
=\begin{pmatrix}
-(P_{r,\mathrm{explicit}}+wP_F)\\
-(\rho-p_r-2p_t)-3w^2/(2F^2B)+3(g-b+2/r)w/(FB)\\
2F\rho+P-2(2/r-b)w/B+3w^2/(2FB)
\end{pmatrix}.
\]

Here derivatives of \(P=2Fp_r+[2wa+3w^2/(2F)]/B\) hold \(w,F\)
fixed in the explicit radial derivative. Neither \(f\) nor \(j\)
appears. The normalized and physical solves agree at nonzero pressure,
including \(W=fz'+jz^2\). Symbolically changing \(j\) changes only
\(z'\) by \(-z^2\delta j/f\), with \(P_X,G_X\) unchanged.

Both charts require \(F,X,U,r,B>0\) and \(fz=w\ne0\). EF evaluation
additionally requires \(2(F-Xf)\ne0\) and \(1+rfz/(2F)>0\).
Either sign of the field Jacobian is allowed. This does not license using
an EF minimally coupled matter model inside sources.

## Executed control and scope

`geometry(eps,y,eta)` supplies
\(r=\epsilon/\sqrt{y(1-e^{-y})}\),
\(B_0=(1-2ry)^{-1}\), \(B=B_0[1+\eta(ry)^2]\), \(g=yB\).
It satisfies exactly \(B-(1+2rg)=\eta(ry)^2\) and
\(p_r=-\eta y^2/B\). A common finite \(\eta\) changes the metric only
at second order in \(\epsilon\) at fixed \(y\), so leading weak-field
no-slip is retained without enforcing exact zero radial pressure. This is
a metric control, not a new universal solution or a pressure fit.

Seven tests cover symbolic derivation/determinant/angular consistency,
geometric derivatives, original zero-pressure closed-inverse recovery,
nonzero-pressure original EF stress/current, a deliberately wrong Ricci
term, normalized equivalence, and second-order scaling. The bounded runner
also evaluates six 65-digit controls: \(\epsilon=10^{-6},2\,10^{-6}\),
\(y=.1\), common choices \(\eta=-2,0,3\),
\(F=.525,f=.05,j=-3000,X=.5,U=.25Xrg,z=-1.5g\).

The original general EF dictionary and original coupled KGB stress/principal
are evaluated independently; transformed Einstein tensor, current and
\(dP/dr=P_Xz\) are checked. Curvatures are **real total derivatives**
of the solved first jets along \((y,X,U,z)\), with a specified local
quadratic \(F\), not independently assigned health controls. Their
evaluation needs next metric derivatives, supplied by differentiating the
chosen smooth geometry. The generic first-jet solver itself does not
assume that metric family.

Run from repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_pressure_freedom_2026/general_inverse/run_checks.py --result-file qwen_claude_field_theory/closure_2026/kgb_pressure_freedom_2026/general_inverse/results.json
```

`results.json` records all checks and actual local scalar matrix coefficients.
They are six independent local controls, **not** one common-action two-mass
seed, radial continuation, cosmology or complete gravity certificate. No
PPN value, rank or healthy verdict is assigned. Initial TDD failures caught
a duplicate dictionary key and an incomplete symbolic angular substitution;
the final run tests the corrected implementation.
