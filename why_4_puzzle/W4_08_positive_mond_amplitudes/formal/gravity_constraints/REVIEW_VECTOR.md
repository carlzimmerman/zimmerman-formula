# Independent analytic audit: physical force and finite-wave-number clock mode

2026-10-20. Reviewer: vector_completion_audit. Scope frozen by
`FROZEN_CRITERIA.md`, commit `201229b5f`, continuation base `f1565bc90`.
This review independently differentiates and reduces the displayed bosonic
action. No executable mathematical calculation, compilation, scan or
source-code edit was used to establish the algebra below. The initial
inputs were the root's force dictionary and gap_selection_physics's raw
Bianchi/finite-k packet. The final saved-report cross-review and exact
artifact hashes appear in section 6.

**Verdict.** The force dictionary, counterfactual PPN inequality, homogeneous
Bianchi reduction and exact frozen finite-k instability pass in their stated
domains. The weak-gravity extension is a conditional small-coupling continuity
argument, rather than an explicitly solved finite-coupling ADM constraint
system. It needs regular constraint reduction and an action-validity window;
it does not establish a healthy completion, a global background or a selected
normalization.

## 1. Model, physical frame and force dictionary

The chosen covariant representative is

\[
 S=\int\sqrt{-g}\left[\frac{M_{\rm Pl}^2}{2}R
 -\frac M2(\nabla_\mu u_\nu)(\nabla^\mu u^\nu)
 +\lambda_u(u^2+1)+L_{\rm rational}\right]
 +S_m[e^{2q\phi}g,\psi].
\]

Here \(M>0\) has mass dimension two, the vacuum conformal factor is fixed
to one, and \(q\phi\) is dimensionless. With a scalar of mass dimension
one, \(q\) has mass dimension minus one. This is an added bosonic action,
not a derived nonlinear supergravity completion. In the usual aether
notation its only nonzero coefficient is \(c_1=M/M_{\rm Pl}^2\).

For an aligned, approximately static clock, the aether term contributes
\(+M(\nabla\ln N)^2/2\) to the static lapse action. The linear static
constraint and the homogeneous isotropic lapse constraint respectively give

\[
 G_t=\frac1{8\pi(M_{\rm Pl}^2-M/2)},\qquad
 G_{\rm cos}=\frac1{8\pi(M_{\rm Pl}^2+M/2)}.
\]

Explicitly, for \(N=1+n\) and \(h_{ij}=e^{2\zeta}\delta_{ij}\),
the static quadratic density is
\(M_{\rm Pl}^2[(\nabla\zeta)^2-2n\Delta\zeta]
+M(\nabla n)^2/2-\rho n\). With vanishing harmonic boundary pieces,
the spatial equation gives \(\zeta=-n\), and the lapse equation gives
\((2M_{\rm Pl}^2-M)\Delta n=\rho\). This also fixes the potential sign
and the Einstein-frame equality used below.

The tensor/shear kinetic coefficient is \(M_{\rm Pl}^2-M\), imposing
the stronger condition \(M<M_{\rm Pl}^2\) used below. At the retained
linear static order the Einstein-frame metric potentials agree.

For the rational branch, \(E(h)=V_0+C_2h^2+o(h^2)\) in the UV, with
\(C_2=25g/48\), and \(E(h)=V_0+C_3|h|^3+o(|h|^3)\) in the IR,
with \(C_3=10\sqrt{5g\tau}/9\) and \(V_0=g^2/(12\tau)\).
For a weak, nonrelativistic compact source, the scalar Gauss law in
\(n\geq2\) spatial dimensions is

\[
 \Omega_{n-1}r^{n-1} E_h(h)=q\,m(<r),
\]

with the sign of the radial derivative retained if \(q<0\). In three
space dimensions this gives

\[
 G_s=\frac{q^2}{8\pi C_2},\quad G_{\rm UV}=G_t+G_s,\quad
 a_s=\frac{2|q|C_2}{3C_3},\quad
 a_{\rm IR}=\frac{G_s}{G_{\rm UV}}a_s.
\]

The displayed signed formula \(a_s=2qC_2/(3C_3)\) therefore assumes
\(q>0\), which can be chosen by orienting \(\phi\). The leading deep-IR
scalar force obeys \(g_s^2=G_s a_s m/r^2\). Tensor gravity is subleading
in that asymptotic deep-IR force, while it contributes to the UV Newton
coupling. A single-mediator amplitude dictionary cannot replace this sum.

Write the Einstein-frame potentials as \(\Phi_E=\Psi_E=-G_tm/r\).
Then the conformal physical potentials are

\[
 \widetilde\Phi=\Phi_E+q\phi=-\frac{(G_t+G_s)m}{r},\qquad
 \widetilde\Psi=\Psi_E-q\phi=-\frac{(G_t-G_s)m}{r}.
\]

Consequently \(\gamma_{\rm UV}=(G_t-G_s)/(G_t+G_s)=1-2f\), where
\(f=G_s/G_{\rm UV}\). This is a local unscreened UV potential ratio:
it assumes universal conformal coupling, weak physical potentials, a
nonrelativistic source and an approximately aligned clock, with scalar
self-gravity beyond the retained order and source distances small compared
with the curvature radius. The source mass uses the physical frame at
unit background conformal factor. It is not a global PPN expansion
through the nonlinear MOND exterior. Screening, source sensitivities,
preferred-frame motion and other matter couplings require separate work.

## 2. Density footing and exact PPN counterfactual

The actual potential density and a Friedmann-inferred density differ.
For this vacuum, \(H^2=8\pi G_{\rm cos}V_0/3\). If the density is
instead inferred using \(G_{\rm UV}\), it is
\(\rho_{\rm inf}=(G_{\rm cos}/G_{\rm UV})V_0\). The fixed branch
coefficients give \(a_s^2/(G_sV_0)=125\pi/128\) for \(q\ne0\);
the resulting force ratios extend continuously to \(q=0\). Hence

\[
 \frac{a_{\rm IR}^2}{G_{\rm UV}V_0}
 =\frac{125\pi}{128}f^3,
 \qquad
 \xi_{\rm inf}=\frac{a_{\rm IR}^2}{G_{\rm UV}\rho_{\rm inf}}
 =\frac{125\pi}{128}
 \frac{f^3(1+r)}{(1-r)(1-f)},\quad
 r=\frac{M}{2M_{\rm Pl}^2}.
\]

In the tensor-positive range \(0\leq r<1/2\), \(0\leq f<1\), impose
\(\xi_{\rm inf}=1/4\) only as a downstream counterfactual. It requires

\[
 125\pi(1+r)f^3=32(1-r)(1-f).
\]

If \(f\leq1/4\), using only \(\pi<4\) and \(r<1/2\) yields

\[
 125\pi(1+r)f^3
 <125\cdot4\cdot\frac32\cdot\frac1{64}
 =\frac{375}{32}<12,
 \qquad
 32(1-r)(1-f)>32\cdot\frac12\cdot\frac34=12.
\]

This is a strict contradiction, including the endpoints \(f=0,1/4\).
Thus \(f>1/4\) and \(\gamma_{\rm UV}<1/2\) under the same unscreened
source assumptions. No measured PPN value or target coefficient determines
\(q\) upstream. The statement is a second-observable diagnostic, not a
selection equation.

## 3. Consistent homogeneous background

For
\(ds^2=-dt^2+a_\perp^2(dx^2+dy^2)+a_\parallel^2dz^2\),
\(\phi=pz\), \(u=\partial_t\), \(h=p/a_\parallel\), and the regular
finite-gradient auxiliary root, the scalar current is homogeneous and
spatial, so its divergence vanishes. The spatial clock equations vanish
by the homogeneous reflection symmetries; the temporal equation fixes
the unit multiplier. Reduced lapse variation is legitimate after imposing
the unit norm and retaining the lapse until variation.

After the standard Einstein-Hilbert temporal boundary subtraction, the
homogeneous kinetic density is

\[
 -M_{\rm Pl}^2(H_\perp^2+2H_\perp H_\parallel)
 -\frac M2(2H_\perp^2+H_\parallel^2)-E(h).
\]

The lapse constraint and rational-matter stresses are

\[
 M_{\rm Pl}^2(H_\perp^2+2H_\perp H_\parallel)
 +\frac M2(2H_\perp^2+H_\parallel^2)=E,
\quad \rho=E,\quad p_\perp=-E,\quad
 p_\parallel=-E+h^2E_X.
\]

They satisfy matter conservation because \(\dot h=-H_\parallel h\)
and \(\dot E=E_Xh\dot h\). With
\(a_\perp=e^{\alpha+\beta}\), \(a_\parallel=e^{\alpha-2\beta}\),
the kinetic coefficients are exactly

\[
 -3(M_{\rm Pl}^2+M/2)\dot\alpha^2
 +3(M_{\rm Pl}^2-M)\dot\beta^2.
\]

At initially zero shear,
\(H_{\rm bg}^2=E/[3(M_{\rm Pl}^2+M/2)]\). Smooth local homogeneous
ODE evolution is available away from a degenerate auxiliary root and
\(M=M_{\rm Pl}^2\). This supplies a local background, not a global
cosmology or a static halo.

## 4. Exact frozen nonzero-k instability

Let the local scalar gradient be \(H\hat z\), and define
\(a=E_X>0\), \(j=L_J>0\), \(K=a+j\),
\(b=E_X+2XE_{XX}>0\). Here \(H\) is the scalar gradient, not
\(H_{\rm bg}\). For a clock tilt \(v\) along that gradient, the
even scalar sector at wave vector \(k\hat z\) is

\[
 L_2=\frac K2\dot\varphi^2-\frac b2(\partial_z\varphi)^2
 -jHv\dot\varphi+\frac M2\dot v^2
 -\frac M2(\partial_zv)^2+\frac{jH^2}{2}v^2.
\]

The mixed-term sign depends on the tilt orientation and does not affect
the determinant. Auxiliary response is included in \(b\); there is no
linear auxiliary source in the homogeneous tilt/time sector. The odd
\(\chi\) sector decouples. For \(w=\omega^2\), direct variation gives

\[
 (Kw-bk^2)[M(w-k^2)+jH^2]-j^2H^2w=0.
\]

Its leading coefficient is \(KM>0\) and its constant term is
\(bM k^2(k^2-m_b^2)\), with \(m_b^2=jH^2/M\). Every
\(0<k^2<m_b^2\) therefore has two real roots of opposite sign. This
is an actual finite-wave-number growing mode of the frozen scalar/clock
system, not an inference from an auxiliary Hessian sign.

At the exact branch point \(x=11/112\), \(F/f_0=3/4\), the independently
checked constants are

\[
 \frac E{V_0}=\frac{283}{252},\quad
 \frac ag=\frac{22}{27},\quad \frac jg=\frac5{54},\quad
 \frac Kg=\frac{49}{54},\quad \theta=\frac aK=\frac{44}{49},
\]
\[
 m_b^2=\frac{55}{1698}\frac EM,\qquad
 m_t^2=\theta m_b^2=\frac{1210}{41601}\frac EM.
\]

Set \(\kappa=k^2/m_b^2\), \(s=w/m_b^2\), and
\(B=b/K>0\). The polynomial is

\[
 p(s)=s^2+[\theta-(1+B)\kappa]s+B\kappa(\kappa-1).
\]

At \(\kappa=1/4\),

\[
 p(-\theta/4)=
 \frac{\theta(1-3\theta)+B(\theta-3)}{16}<0.
\]

Since \(p(0)<0\) and the negative root lies to the left of any negative
argument with negative polynomial value, \(w_-<-m_t^2/4\). Thus
\(k=m_b/2\) has growth rate \(\gamma>m_t/2\). No inverse at \(k=0\)
is used.

## 5. Conditional weak-gravity continuation and remaining work

Take \(\epsilon=M/M_{\rm Pl}^2\to0\) at fixed \(M,g,\tau,h\) at
the regular branch point. Then \(m_b\) and the frozen growth rate stay
finite, whereas \(L_{\rm bg}^{-1}/m_b=O(\sqrt\epsilon)\). In particular,

\[
 \frac{E}{M_{\rm Pl}^2m_b^2}=\frac{1698}{55}\epsilon.
\]

In a regular generalized harmonic reduction, the canonically normalized
metric \(h_c=M_{\rm Pl}\delta g\) has an invertible wave block at
\(\omega=i\gamma\), \(k=m_b/2\): its denominator has size
\(k^2+\gamma^2\), rather than a wave pole. With
\(v_c=\sqrt M v\), metric mixing from the clock connection and the
finite matter/background stress is \(O(\sqrt\epsilon)\) in units of
\(m_b^2\). Fixed regular branch coefficients cannot diverge in this limit.
The metric Schur correction is consequently \(O(\epsilon)\), and the
isolated simple growing root persists for sufficiently small \(\epsilon\)
provided this regular reduction is maintained.

The gauge qualification is essential. Covariance and the matter/clock
equations give homogeneous propagation of the harmonic constraints. The
fast imaginary-frequency root at real nonzero k is separated from the
residual harmonic-gauge wave block. This supports a constrained physical
continuation, with constraint-satisfying initial data; a root of an
arbitrary gauge-fixed determinant alone would not establish it. The packet
does not display every metric mixing coefficient or an exact finite-coupling
lapse/shift inverse, and should not be described as doing so.

On the slowly varying Bianchi background, a window
\(\Delta t=\epsilon^{-1/4}/m_b\) has relative background drift
\(O(\epsilon^{1/4})\), while allowing \(O(\epsilon^{-1/4})\) growth times.
This is a local adiabatic/continuity statement. Its physical use requires
\(L_{\rm bg}^{-1}\ll k,\gamma\ll\Lambda_{\rm valid}\).
The hierarchy \(M_{\rm Pl}\gg\sqrt M\gg E^{1/4}\) leaves a frequency
window below the indicated clock and scalar scales. It does not establish
that omitted operators are small on the finite-gradient background.

Unverified here are an explicit finite-coupling constraint matrix and
threshold, validity of the rational action against omitted operators,
nonlinear evolution, a global Bianchi solution, a matched sourced halo,
screening or source sensitivities, and a microscopic/supergravity/quantum
completion. No part of this review supplies an independently selected
normalization or completes the frozen end-to-end goal.

## 6. Final saved-artifact cross-review

I reread the frozen `RESULT.md` after the two requested wording corrections.
It now explicitly orients the scalar so that q>0, and correctly describes
the clock as a real vector with no imaginary-clock sector in the declared
representative. No required correction remains in the reviewed force,
PPN, Bianchi, finite-k or conditional-continuation scope. The pure-BM
finite-nonzero-k reduction also remains consistent with my earlier
independent reduction; it is distinct from the rational vector model.

The Cassini comparison is explicitly downstream and conditional on applying
the local unscreened UV coupling in the Solar System. It is not used to
select q or another coefficient. I read `SOURCES.md` for this separation of
source claims from new calculations; this review does not independently
reauthenticate every external bibliographic or equation pin.

I also read the final `GravitySelection.lean` source. Its fourteen
statements have the advertised conditional algebraic scope. In particular,
the target bounds assume a generic ordered-field P with 0<P<4 and the
displayed target equation. The band polynomial at k=m_b/2 is exactly
\((s-B/4)(s+3/4)-(5/49)s\); evaluating at
\(s=-11/49=-\theta/4\) gives
\(-913/9604-103B/784<0\) for B>=0. The source does not claim to formalize
root existence, actual pi, the ADM variations, constraint continuation or
physical source calibration. I did not independently compile the file or
reproduce the coordinator's reported run/controls.

The following SHA256 values were independently read from the saved files:

| Artifact | SHA256 |
| --- | --- |
| `RESULT.md` | `b20f279bf75f3ad4ffa192cf41c5f92409a5e9346f2e369c57d9320c3878236e` |
| `SOURCES.md` | `2ade5450142277792316742a7b801997c6443a8d54c6c106dfbfcbef3c70fe3f` |
| `GravitySelection.lean` | `fd0145d1e60ff5cc020a15700f7a6378c0d33d5e465eba2962549b6aebcaf6c4` |

Final verdict: pass for the exact stated analytic/algebraic scopes, with the
weak-gravity Schur/Ward extension conditional and the unverified physical
obligations in section 5 retained. This verdict supplies no full-gravity
health theorem, microscopic completion or normalization selection.
