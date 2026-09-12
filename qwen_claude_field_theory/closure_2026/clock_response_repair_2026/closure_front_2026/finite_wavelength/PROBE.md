# Conserved source: the equations to integrate next

This is a **symbolic forced linear system**, not a completed galaxy solution.
The source-free full-wavelength calculation already existed in
`../../cubic_finite_wavelength/`; it is not counted as new work. The independent
`adm/` calculation now checks it in unitary-chi gauge, keeping all background
residuals before using the on-shell equations. `probe.py` adds a source and
varies/eliminates the resulting constraints without selecting a MOND law.

The probe is a formal zero-background-density perturbation
\(\delta\rho=\rho_*a^{-3}\cos(kx)\), with zero pressure and momentum. Its
background conservation equation \(\dot{\delta\rho}+3H\delta\rho=0\) holds
exactly. The sign-changing density is a linear-response probe, **not** a
positive-density isolated galaxy or a nonzero baryonic background. Adding
real background baryons requires solving their background equations too.

Minimal worldline coupling gives the source term
\(-a^3\rho n/2\) after averaging the real cosine mode. Use the common
normalization \(L=2\langle\mathcal L\rangle/a^3\); its source is then
\(-\rho n\). This is not a direct scalar coupling. Define

\[
r=k^2/a^2,\quad \Theta=M^2H+\gamma q^3,\quad
\Sigma=q^2P_X+2q^4P_{XX}-3M^2H^2-12\gamma Hq^3,
\]
\[
W=W(0,t),\quad C=W-2q^2W_Y,\quad
D=P_\tau-V_\tau-2q^2P_{X\tau},\quad
E=P_{\tau\tau}-V_{\tau\tau}-3HW_\tau.
\]

Here D and E are called C and D respectively in the ADM report; the explicit
map prevents conflating the gradient block C with a clock-time derivative.
The varied shift and clock equations give

\[
n=\frac{M^2\dot\zeta+W\sigma/2}{\Theta},\qquad
\sigma=\frac{J\dot\zeta+Rr\zeta-f}{\mathcal D},
\]
\[
J=\frac{M^2(\Sigma W+D\Theta)}{\Theta^2},\quad
R=\frac{M^2W}{\Theta},\quad f=\frac{\rho W}{2\Theta},\quad
\mathcal D=Cr-E-\frac{DW}{\Theta}-\frac{\Sigma W^2}{2\Theta^2}.
\]

The fully reduced normalized density, retaining time-dependent coefficients,
is

\[
L_{\rm eff}=\frac{K_0}{2}\dot\zeta^2
+\frac{2M^4r}{\Theta}\zeta\dot\zeta+M^2r\zeta^2
-\frac{\rho M^2}{\Theta}\dot\zeta
+\frac{(J\dot\zeta+Rr\zeta-f)^2}{2\mathcal D},\quad
K_0=6M^2+\frac{2\Sigma M^4}{\Theta^2}.
\]

Here \(M^4=(M^2)^2\); the Python symbol `M2` is the Einstein coefficient.
Differentiating this density defines A, B, C_eff, F, S, without inserting
expected values:

\[
L_{\rm eff}=A\dot\zeta^2/2+B\zeta\dot\zeta+C_{\rm eff}\zeta^2/2
+F\dot\zeta+S\zeta+\text{source-only term}.
\]
\[
p=a^3(A\dot\zeta+B\zeta+F),\quad
\dot\zeta=(p/a^3-B\zeta-F)/A,\quad
\dot p=a^3(B\dot\zeta+C_{\rm eff}\zeta+S).
\]

These equations retain coefficient time derivatives through the canonical
momentum, without approximating them by constants. All divisions require
\(k\ne0\), \(q\ne0\), \(\Theta\ne0\), \(\mathcal D\ne0\), and \(A\ne0\).
The actual homogeneous mode and singular constraint branches remain separate.

Finally vary the lapse to recover the longitudinal shift. For
\(u=a^2B_{\rm shift}=-(\Delta B_{\rm shift})/r\), the two physical Newtonian-
gauge potentials are independently

\[
\Phi=n+\dot u,\qquad \Psi=-\zeta-Hu.
\]

Their time-gauge invariance is checked algebraically. Their equality, full
PPN parameters and numerical force response are **not** assigned or evaluated
in this checkpoint. The next computation is integration of this forced
system with source-compatible lapse/shift/clock initial data, followed by
separate reconstruction of both potentials. Abruptly switching the dust
probe on would violate conservation without an injection mechanism; use a
finite-initial-time conserved-source problem, not a Heaviside switch.

Eighteen exact checks and the independent source-sign/zero-source unit test
passed. The unit test initially failed its missing-implementation assertion
before the source reduction was written. Independent proof review checked
the averaging factor, coefficient map, all forcing signs and potential gauge
transformations. These checks do not integrate the response or certify nature.
