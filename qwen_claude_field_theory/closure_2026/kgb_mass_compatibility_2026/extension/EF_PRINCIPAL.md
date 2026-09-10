# Affine conformal Einstein-frame principal dictionary

2026-09-10. Base `9a088d45c9c3349de154446aeee4500a84f31c9a`.
This is an independently checked dictionary and one mapped solution control.
It does not certify the newly constructed physical-frame inverse.

Set \(C=2F/m=1+\sigma X\), \(\chi=X/C\). Here \(X\) and physical action
derivatives carry the conventions of `REPORT.md`; a subscript \(\chi\) denotes
an Einstein-frame derivative. Since \(d\chi/dX=C^{-2}\), direct differentiation
gives

\[
 \widetilde P=\frac P{C^2},\qquad
 \widetilde P_\chi=P_X-\frac{2\sigma P}C,\qquad
 \widetilde P_{\chi\chi}=C^2P_{XX}-2\sigma C P_X+2\sigma^2P,
\]
\[
 \widetilde G_\chi=CG_X,\qquad
 \widetilde G_{\chi\chi}=C^3G_{XX}+\sigma C^2G_X.
\]

These formulas include the integration-by-parts contribution from transforming
the cubic scalar term. They are not obtained by treating \(G/C\) alone as the
new braiding function. The conformal family and its primary references remain
as verified in `SOURCES.md`; no new external theorem is introduced here.

## Background and derivatives

Let \(g=A'/(2A)\), \(p=\psi'\), and \(b=B'/B\), with primes taken with
respect to physical areal radius \(r\). Define

\[
 h=\frac{C'}C=\frac{\sigma X'}C,\quad
 D=1+\frac{rh}2,\quad \Omega=\sqrt C,\quad R=\Omega r.
\]

On the \(D>0\) orientation branch,

\[
 \widetilde A=CA,\quad \widetilde B=\frac B{D^2},\quad
 \widetilde g=\frac{g+h/2}{\Omega D},\quad
 \widetilde p=\frac p{\Omega D},\quad
 \frac d{dR}=\frac1{\Omega D}\frac d{dr}.
\]

When coordinate radial derivatives themselves are required,

\[
 h'=\frac{\sigma X''}C-h^2,\qquad D'=\frac h2+\frac{rh'}2,
\]
\[
 \frac{d\widetilde p}{dR}
 =\frac{p'-p(h/2+D'/D)}{CD^2},\qquad
 \frac1{\widetilde B}\frac{d\widetilde B}{dR}
 =\frac{b-2D'/D}{\Omega D}.
\]

All \(D'\), hence all \(X''\), terms cancel when these derivatives are
combined into the Einstein-frame scalar Hessian. In its orthonormal frame,
for \(\phi=qt+\psi\),

\[
 v_a=\left(\frac q{\sqrt{CA}},\frac p{\sqrt{CB}},0,0\right),
\]
\[
 H_{00}=-\frac{(g+h/2)p}{CB},\quad
 H_{01}=-\frac{q(g+h/2)}{C\sqrt{AB}},\quad
 H_{11}=\frac{p'-(b+h)p/2}{CB},\quad
 H_{22}=H_{33}=\frac{pD}{CBr}.
\]

The mixed sign is explicit: the previous source examples choose \(q=-1\).
An independent check uses the conformal connection identity for the Hessian;
all sixteen matrix-entry residuals vanish.

Inputs must obey the physical scalar norm and its derivative:

\[
 2X=\frac{q^2}{A}-\frac{p^2}{B},\qquad
 X'=-\frac{q^2g}{A}-\frac{pp'}B+\frac{p^2b}{2B}.
\]

The helper reports both residuals rather than silently assuming unrelated input
jets are coherent. Its direct principal evaluation does not use \(X''\).

## Executable use and interpretation

`ef_principal.py` provides:

- `action_dictionary(X,sigma,P,PX,PXX,GX,GXX)` for the five transformed action jets;
- `background_dictionary(r,A,B,g,BrB,p,pr,X,Xr,sigma,q=-1)` for the transformed
  metric, gradient and Hessian; `pr` means \(dp/dr\), not radial pressure;
- `evaluate(m,background,physical_jet)` to insert those quantities into the
  original KGB coupled scalar principal and stress expression.

Use arbitrary-precision inputs inside an `mpmath.workdps` context when high
precision is needed. The evaluator returns the matrix and stress themselves,
the clock consistency residuals, and explicitly named Einstein-frame flags.

Outside baryonic matter, the conformally transformed action has the KGB form
with constant \(m\), so its existing coupled principal expression is applicable
to an on-shell transformed background. Inside matter, the physical minimal
matter action acquires a clock-dependent coupling in the Einstein frame. Its
metric/scalar source and principal contributions must be retained; the vacuum
evaluator cannot silently be reused there. Background equations and total-current
closure must be checked separately before interpreting an arbitrary matrix as
the physical linearization of a solution.

For the source convention, \(K=C_{00}>0\), \(C_{11}<0\), and
\(C_{22}<0\) give positive scalar quadratic energy relative to the EF static
time at the level of its reduced high-frequency kinetic form. The strict-cone
flag additionally checks \(K>|C_{01}|\) and the minimum of

\[
 K+C_{22}-2|C_{01}|t+(C_{11}-C_{22})t^2,\qquad 0\le t\le1.
\]

This is a frame-labeled quadratic-energy test, not a proof of a bounded full
physical-frame Hamiltonian. The derivative-dependent metric transformation mixes
scalar and metric perturbations; transferring a full energy statement requires
the constrained quadratic action, the transformed symplectic/boundary terms,
and regular initial/boundary data. None is supplied by a kinetic-rank count.

For characteristic-cone interpretation, the required regularities include
\(C>0\), \(C-XC_X=1\ne0\), \(X>0\), and \(D\ne0\), with the explicit
\(D>0\) orientation used here. Under the regular invertible equivalence of the
constrained physical modes, the conformal metric has the same photon null cone,
so EF scalar-cone containment can be compared to that physical cone. One must
not promote unconstrained extra roots from a higher-order representation into
physical modes. Singular field maps, a folded areal coordinate, strong coupling,
or unretained matter terms invalidate this shortcut.

## Independent controls

The action and Hessian chain rules have twenty exact zero residuals. A canonical
EF scalar control reconstructs \(\widetilde P_\chi=1\),
\(\widetilde P_{\chi\chi}=0\), and the actual principal
\(\operatorname{diag}(1,-1,-1,-1)\). It has a positive quadratic energy but
is correctly not classified as strictly inside the photon cone.

A second control maps the original exact flat-force halo with
\(\widetilde A=R^{2w}\), \(\widetilde B=1+2w\), \(w=0.01\),
\(\chi=[(2+w)\widetilde A]^{-1}\), and \(\sigma=0.1\) into physical
variables, then maps it back through this helper at \(R=1\).
At 60 digits it recovers the metric and both braiding derivatives, and its
Einstein/stress residual is below \(6.33\times10^{-60}\). The principal has

\[
 C_{00}=1.9804411764705882,\quad C_{11}=-0.0295588235294118,\quad
 C_{22}=-0.000295588235294118,
\]

with zero cross coefficient up to numerical precision and strict-cone margin
1.9508823529411765. This is a known single-profile control, not a new exponential
MOND solution, universal mass law, or physical-frame no-slip construction.

Run `python3 -B` on `ef_principal.py` from repository root. Five tests pass;
`ef_run_001/` holds results and a validated manifest. The original extension
artifacts and their earlier manifest inputs were not changed. Computation-audit
guided the checks, and proofread-math self-review covered this new dictionary.
No commits, pushes, or full-theory claims were made.
