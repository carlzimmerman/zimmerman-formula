# On-shell de Sitter scalar audit and the PQ repair

This calculation advances from frozen derivative blocks to an actual solution of the common action. The inactive, vacuum-only CA4-GNC-P branch has a positive scalar kinetic coefficient at every nonzero wave number, but negative infrared spatial stiffness. An added projected quadratic vacuum potential removes that defect in an explicit parameter window. The repaired result is a linear scalar statement on this de Sitter background, not global nonlinear health of the theory.

The original calculation and its evidence are preserved in frw_check.py and frw_run_001/. The action deformation is checked separately in pq_check.py and pq_run_001/. Sources are frozen under frw_snapshots/. These formulas use the centered trace clock term of FINAL_ACTION.md and the perspective carrier of PERSPECTIVE_VARIANT.md, not the older uncentered clock or exponential carrier.

## 1. Background and independent ADM expansion

Set bare cosmological constant to zero, carrier excitations to zero, and retain its positive vacuum floor \(V_0\). The homogeneous solution is

\[
a(t)=e^{Ht},\quad H>0,\quad V_0=3M^2H^2,\quad
U=Z=0,\quad z=P_hZ=0,\quad t_c=1+z=1.
\]

The gate argument is \(-\theta<0\), so its primitive and derivatives vanish near this background. Write

\[
h_{ij}=a^2e^{-2\psi}\delta_{ij},\qquad N=e^\varphi,\qquad
N^i=a^{-2}\partial_i\beta,\qquad x=q^2=k^2/a^2>0.
\]

The homogeneous mode is excluded from every division by \(x\). Centered quantities and the global constraint need a separate homogeneous analysis.

For a plane wave, put \(B=a^{-2}\beta_{xx}\) at first order and \(C=a^{-2}\beta_x\psi_x\) at second order. With \(T=H-\dot\psi+C\), the exact invariant for this ansatz is

\[
K_{ij}K^{ij}-K^2=e^{-2\varphi}(-6T^2+4TB).
\]

The kinetic density divided by \(a^3\) is \(e^{-\varphi-3\psi}(-6T^2+4TB)\). The background vacuum term, in units \(M^2/2\), is \(-6H^2e^{\varphi-3\psi}\). Their quadratic sum differs from

\[
-6(\dot\psi+H\varphi)^2-4B(\dot\psi+H\varphi)
\]

by

\[
-12H(C+\psi B)-36H\psi\dot\psi-54H^2\psi^2.
\]

The first pair integrates to zero spatially. The remaining pair is a time boundary with the \(a^3\) measure: integration of \(-36Ha^3\psi\dot\psi\) gives \(+54H^2a^3\psi^2\). No de Sitter mass term was discarded by substituting a flat-space formula.

The exact conformal intrinsic curvature is

\[
R^{(3)}=a^{-2}e^{2\psi}(4\Delta\psi-2|\nabla\psi|^2).
\]

Its integrated quadratic density is \(2x\psi^2-4x\varphi\psi\). The centered trace has background zero and, for a nonzero mode,

\[
\delta Q_K=-3(\dot\psi+H\varphi)+x\beta.
\]

Second-order changes of the mean cannot enter its square at quadratic order. With \(v=\dot\psi+H\varphi\), the shift block is

\[
-6v^2+4x\beta v-c_2(3v-x\beta)^2.
\]

Its stationary solution \(x\beta=(3+2/c_2)v\) leaves \(Kv^2\), where

\[
K=\frac{2(2+3c_2)}{c_2}>0\qquad(c_2>0).
\]

## 2. Projection and the original P branch

The carrier vacuum term is \(-N\sqrt h\,V_0/(1+z)\), with \(z=Z-\langle Z\rangle_h\). Relative to a pure cosmological constant, its integrated quadratic correction is

\[
a^3 V_0(\varphi Z-Z^2).
\]

Indeed \(\int\sqrt h\,z=0\) identically. Expanding \(\int N\sqrt h\,z\) gives only \(\varphi Z\) at quadratic order. The apparent \(\psi Z\) term cancels against the second variation of the projection. The symbolic check also differentiates an exact two-cell projected expression to verify this cancellation.

Let \(c_N=1-\alpha/2\) and

\[
r(x)=r_0e^{-\xi^2x/2},\quad r_0=\ell/4,\qquad
\alpha_e(x)=2-(2-\alpha)(1-r)^2.
\]

The metric variation of the heat operator acting on this constant background field vanishes. The inactive \(U\) constraint of the compensated action gives \(Z=r\varphi\). Substitution in the spatial block gives \(\alpha_e x\varphi^2\). The full quadratic scalar block is

\[
L^{(2)}=\frac{M^2a^3}{2}
\left[K(\dot\psi+H\varphi)^2+2x\psi^2-4x\varphi\psi+D\varphi^2\right],
\quad D=\alpha_e x+6H^2r(1-r).
\]

For \(0<\alpha<2,\ 0<\ell<4\), \(D>0\) at every finite \(x>0\). Put \(F=KH^2+D\). Eliminating the lapse gives

\[
\varphi=\frac{2x\psi-KH\dot\psi}{F},\quad
A=\frac{KD}{F},\quad B=\frac{4KHx}{F},\quad
C=2x-\frac{4x^2}{F},
\]

where the remaining density is \(a^3(A\dot\psi^2+B\dot\psi\psi+C\psi^2)\). The mixed term must be integrated with both the expansion measure and evolving physical wave number:

\[
\dot x=-2Hx,\quad \dot r=H\xi^2xr,\qquad
C_* = C-\frac{3HB+\dot B}{2}
=\frac{2xD}{F}-\frac{4x^2}{F}
-\frac{4KH^2x^2D_x}{F^2}.
\]

Here \(D_x\) includes \(r_x=-\xi^2r/2\). With \(D_0=6H^2r_0(1-r_0)>0\),

\[
A\longrightarrow\frac{KD_0}{KH^2+D_0}>0,\qquad
\frac{C_*}{Ax}\longrightarrow\frac2K>0.
\]

Positive spatial stiffness is \(-C_*\) in this convention, so the original branch has an infrared negative stiffness. In the ultraviolet it approaches the positive normalized-host speed \(2(2-\alpha)/(K\alpha)\). The limits \(q\to0\) and \(\ell\to0\) are not interchangeable.

This sign does not by itself prove unbounded future growth: a fixed comoving mode redshifts. For \(0<\ell\le2\), direct differentiation gives \(\dot D+2HD\ge0\), hence friction \(3H+\dot A/A\ge H\). Also \(|C_*/A|\le Mx(t)\) for a finite mode-dependent \(M\) on the future interval. Section 5 proves the resulting boundedness, preserving the sign defect without overstating it.

## 3. PQ adds one potential and fixes its coefficient by infrared health

The new action ingredient is

\[
\Delta L=-\sqrt{-g}\,V_0\zeta z^2,\qquad
\zeta=\frac{1-r_0}{r_0}=\frac4\ell-1>0.
\]

It lies outside the carrier factor \(1/(1+z)\). It leaves this background and the \(U\) equation unchanged and adds a positive quadratic term to the canonical auxiliary energy. It changes the lapse coefficient by \(-6H^2\zeta r^2\). Thus

\[
D_{\rm PQ}=\alpha_e x+6H^2r_0S(1-S)=x\,d(x),\quad
S=e^{-u},\quad u=\xi^2x/2,
\]

\[
d=\alpha_e+\eta g(u),\qquad \eta=3H^2\xi^2r_0,\qquad
g(u)=\frac{e^{-u}-e^{-2u}}u=\int_1^2e^{-vu}\,dv.
\]

The identity defines \(g(0)=1\) continuously and gives \(0<g\le1,\ g'<0\). Also \(\alpha_e'<0\), so \(d_x<0\) for \(\xi>0\).

The coefficient is constrained if every nonzero physical wave number must have positive kinetic and spatial stiffness in this family. Before tuning,

\[
D(0)=6H^2r_0[1-(1+\zeta)r_0].
\]

If it is positive, the infrared negative stiffness persists. If it lies strictly between \(-KH^2\) and zero, \(A=KD/(KH^2+D)\) is negative near zero. If it is below \(-KH^2\), continuity to the positive ultraviolet denominator forces a denominator zero. At the equality endpoint, either a nearby ghost or a denominator zero remains. Therefore nonsingular all-\(q\) positivity requires \(D(0)=0\), giving the tuning above. This is a conditional inverse relation from linear background health; it does not derive \(V_0\), \(\ell\), or their microscopic origin.

## 4. An analytic all-\(q\) positive window

Assume

\[
0<\alpha\le1,\quad 0<\ell\le1,\quad c_2>0,\quad H>0,\quad
\xi>0,\quad 0<\eta=3H^2\xi^2r_0\le\frac1{10}.
\]

Then \(0<r\le r_0\le1/4\), and

\[
0<\alpha_e\le\frac{23}{16},\qquad
0<d\le\frac{23}{16}+\frac1{10}=\frac{123}{80}<2.
\]

Use \(ue^{-u}\le1/2\), following for example from \(e^u\ge1+u+u^2/2\ge2u\) for \(u\ge0\). The exact derivatives obey

\[
2u\alpha_{e,u}=-4(2-\alpha)ur(1-r)\ge-4r_0,
\]

\[
2u\eta g_u=2\eta(-S+2S^2-g)\ge-4\eta.
\]

Consequently

\[
2+d+2u d_u\ge2-4r_0-4\eta\ge\frac35>0.
\]

Writing \(F=KH^2+xd\), the exact mixed-term integration now gives

\[
A=\frac{Kxd}{F}>0,\qquad
C_*=-\frac{2x^2}{F^2}
\left[KH^2(2+d+2xd_x)+xd(2-d)\right]<0
\quad(x>0).
\]

Both terms in brackets are positive. This proves the sign for all positive wave numbers from inequalities, not a finite scan. The separate PQ computation reproduces the exact identities and rational margins; PQBridge20260926.lean certifies the conditional rational/sign bridges.

In the infrared,

\[
d_0=2-(2-\alpha)(1-r_0)^2+\eta>0,\quad
A\sim\frac{d_0x}{H^2},\quad
\Omega^2=-C_*/A\sim\frac{2(d_0+2)}{Kd_0}x.
\]

Positivity is not uniform down to \(q=0\): the kinetic coefficient vanishes there. The ultraviolet speed again tends to \(2(2-\alpha)/(K\alpha)>0\). Neither limit certifies uniform nonlinear coercivity or strong-coupling control.

## 5. Future mode evolution

The reduced equation is

\[
\ddot\psi+b(t)\dot\psi+\Omega^2(t)\psi=0,\qquad
b=3H+\dot A/A.
\]

For PQ,

\[
b=H\left[3-\frac{2KH^2}{F}
\left(1+\frac{x d_x}{d}\right)\right]\ge H,
\]

because \(d_x<0\) and \(F>KH^2\). For a fixed initial \(x_0>0\), \(\Omega^2/x\) extends continuously to \(x=0\) and has finite absolute bound \(M\) on \(0\le x\le x_0\). Since \(x(t)=x_0e^{-2H(t-t_0)}\),

\[
\int_{t_0}^{\infty}|\Omega^2(t)|dt\le\frac{Mx_0}{2H}.
\]

Variation of constants for \(\dot\psi\), using the \(b\ge H\) kernel bound, gives

\[
|\psi(t)|\le|\psi_0|+|\dot\psi_0|/H+
\frac1H\int_{t_0}^t|\Omega^2(s)|\,|\psi(s)|ds.
\]

Gronwall yields

\[
\sup_{t\ge t_0}|\psi(t)|\le
(|\psi_0|+|\dot\psi_0|/H)
\exp\!\left(\frac{Mx_0}{2H^2}\right)<\infty.
\]

The same kernel bound gives \(\int|\dot\psi|dt<\infty\); each fixed mode has a finite future limit. With \(\Omega^2=-C_*/A\), the same argument applies to the untuned P branch for \(0<\ell\le2\), despite its negative infrared stiffness.

This is a per-mode linear future result. The bound depends on the initial wave number. No uniform Sobolev sum, past-eternal regularity, nonlinear estimate, or global clock/lapse theorem has been established.

## 6. Evidence and the remaining boundary

The original de Sitter run checks 19 exact identities: the ADM background cancellations, projected vacuum term, shift/lapse stationarity, evolving-\(q\) mixed-term integration, and original infrared/ultraviolet limits. The separate PQ run checks the new coefficient, tuning, derivative identities, and limits. The integral and inequalities above supply the analytic all-\(q\) argument; command success alone is not that argument.

PQBridge20260926.lean proves the effective-coefficient interval, rational \(d\) bound, derivative margin, kinetic positivity, integrated-gradient negativity, and tuning equivalence under explicit hypotheses. It does not formalize the ADM variation, exponential estimates, or differential-equation argument. Its accepted compile/axiom record is separate from the older fourteen-lemma certificate.

Remaining full-theory obligations include the homogeneous constraint, excited-matter backgrounds, transition-gate and spatial-metric mixing, uniform small-\(q\) control, nonlinear evolution, and continuation of a positive clock/lapse. The positive vacuum floor and tuned projected potential are explicit new action inputs, not a derived dark-energy magnitude or inherited successes of the earlier action.
