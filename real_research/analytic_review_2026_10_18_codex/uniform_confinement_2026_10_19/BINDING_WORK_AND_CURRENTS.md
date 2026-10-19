# Binding reserves and radial current work

19 October 2026. Claims ZAR-C2 and ZAR-C3. Use the exact model, angular gap, classical evolution and notation of [checkpoint 05](../nonlinear_radial_2026_10_19/NONLINEAR_FLOW.md). Let T,U denote the perturbed conserved masses, c=G^2/a_0, and rho>0 the time-uniform inner radius from that theorem. All potentials are zero at infinity.

## The exact energy transfer

Define shell currents j_i=C_Gamma int v f_i dv dL, with C_Gamma=4 pi^2. Integrating the transport equation gives partial_t M_i=-j_i. Therefore

\[
\Phi_f(t,r)=-\frac{GM_b}{r}
-G\int_r^\infty\frac{M_t(t,s)+M_f(t,s)}{s^2}\,ds,
\]

\[
\Phi_t(t,r)=-\frac{GM_b}{r}
-G\int_r^\infty\frac{M_f(t,s)}{s^2}\,ds
+c\int_r^\infty\frac{M_t(t,s)^2}{s^4}\,ds.
\]

Differentiation is justified on each finite time interval by smoothness and finite-time compact support. The exact work rates are

\[
w_f(t,r):=\partial_t\Phi_f
=G\int_r^\infty\frac{j_t+j_f}{s^2}\,ds,
\tag{11}
\]

\[
w_t(t,r):=\partial_t\Phi_t
=G\int_r^\infty\frac{j_f}{s^2}\,ds
-2c\int_r^\infty\frac{M_tj_t}{s^4}\,ds.
\tag{12}
\]

The tethered term has a minus sign: outward tethered current reduces its repulsive potential. Taking absolute values before combining these terms would discard a real cancellation.

For an initially occupied label z and its characteristic r_i(t;z), put

\[
E_i(t,z)=\frac{v_i(t;z)^2}{2}
+\frac{L(z)}{2r_i(t;z)^2}+\Phi_i(t,r_i(t;z)),
\quad
\mathcal W_i(t,z)=\int_0^t w_i(s,r_i(s;z))\,ds.
\]

The characteristic equation gives exactly

\[
E_i(t,z)=E_i(0,z)+\mathcal W_i(t,z).
\tag{13}
\]

Suppose beta_i(z)=-E_i(0,z)>0 on the initial support. The condition

\[
\mathcal W_i(t,z)\le\beta_i(z)-\eta_i
\quad\hbox{for every }z,t,\qquad\eta_i>0,
\tag{14}
\]

is necessary and sufficient for retaining that uniform actual-energy gap E_i<=-eta_i. It is sufficient for spatial confinement, because

\[
\Phi_f(t,r)\ge-\frac{A_f}{r},\quad A_f=G(M_b+T+U),
\qquad
\Phi_t(t,r)\ge-\frac{A_t}{r},\quad A_t=G(M_b+U),
\]

and the other particle-energy terms are nonnegative. Thus

\[
\boxed{r_i(t;z)\le A_i/\eta_i\quad\hbox{for every }z,t.}
\tag{15}
\]

No converse from spatial confinement to (14) is established here. The certificate imposes a negative actual-energy gap throughout the core, whereas the exterior launch theorem only tests outgoing passages. The exact identity (13) establishes the criterion but does not prove that the work stays small.

## A sufficient budget expressed only through the currents

Suppose initially E_i(0,z)<=-eta_i0 uniformly, eta_i0>eta_i>0. A directly checkable sufficient hypothesis is

\[
\mathcal B_i(t)=\sup_{r\ge\rho}[w_i(t,r)]_+,
\qquad
\int_0^\infty\mathcal B_i(t)dt
\le\eta_{i0}-\eta_i.
\tag{16}
\]

Then (14) and (15) follow. This allows arbitrary negative work, and forms the species and spatial cancellations in (11)-(12) before taking a positive part. It is stronger than the signed pathwise budget (14), since it discards temporal cancellation and lets the maximizing radius vary arbitrarily.

Still stronger but simpler sufficient bounds follow from

\[
\mathcal B_f(t)\le
G\int_\rho^\infty\frac{(j_t+j_f)_+}{s^2}\,ds,
\]

\[
\mathcal B_t(t)\le
G\int_\rho^\infty\frac{(j_f)_+}{s^2}\,ds
+2c\int_\rho^\infty\frac{M_t(j_t)_-}{s^4}\,ds,
\tag{17}
\]

where x_- = max(-x,0). An even warm distribution has zero current and positive pressure, so these conditions do not impose a cold halo.

## A finite boundary uses only relative potential work

A chosen enclosing radius B can admit a weaker certificate than a global negative-energy gap. Assume the initial support lies strictly inside B and define

\[
m_i(z)=\frac{L(z)}{2B^2}+\Phi_i(0,B)-E_i(0,z),
\quad m_{i,*}=\inf_z m_i(z)>0.
\tag{18}
\]

This is a separate support margin, not a consequence of small integrated density error. For a fixed compact initial support with negative energy gap, a sufficiently large B gives (18), since Phi_i(0,B) and L/(2B^2) tend uniformly to zero.

Let

\[
D_i^B(t,z)=\frac{L(z)}{2B^2}+\Phi_i(t,B)-E_i(t,z).
\]

For r<=B, the exact relative work rates are

\[
q_f^B(t,r)=w_f(t,r)-w_f(t,B)
=G\int_r^B\frac{j_t+j_f}{s^2}\,ds,
\]

\[
q_t^B(t,r)=w_t(t,r)-w_t(t,B)
=G\int_r^B\frac{j_f}{s^2}\,ds
-2c\int_r^B\frac{M_tj_t}{s^4}\,ds.
\tag{19}
\]

Consequently

\[
D_i^B(t,z)=m_i(z)-
\int_0^t q_i^B(s,r_i(s;z))\,ds.
\tag{20}
\]

A useful sufficient condition for r<B for all occupied particles and all time is

\[
\boxed{\int_0^\infty
\sup_{\rho\le r\le B}[q_i^B(t,r)]_+dt<m_{i,*}.}
\tag{21}
\]

To prove it, suppose an occupied characteristic has a first hit of B. Before that hit its r stays in [rho,B], so (20)-(21) give D_i^B>0 at the hit. But at r=B, D_i^B=-v^2/2<=0, a contradiction. This proof can be applied to each characteristic separately: it does not assume beforehand that no other particle has crossed B. The relative formulas (19) remain valid even if mass exists outside B. The positive margin is uniform, and closure gives the full support bound r<=B.

Before a first exit of the entire support the boundary potential is additionally the fixed vacuum value

\[
\Phi_f(t,B)=-G(M_b+T+U)/B,
\quad
\Phi_t(t,B)=-G(M_b+U)/B+cT^2/(3B^3).
\tag{22}
\]

Relative potential work removes any spatially constant potential change from exterior matter. Formula (21) only uses the currents between rho and B. The still weaker signed version replaces the scalar positive-rate integral by the actual characteristic integral in (20), strictly below m_i(z), up to and including a possible first hit. Equivalently one may impose a strict upper limit below m_i(z) as that time is approached. Strict positivity at every earlier time without a remaining margin would not exclude equality at a tangential hit. An independent estimate of the work is needed; merely assuming a positive reserve is not a propagation argument.

## Work sampled only at outward crossings

The exact work identity can be joined to the exterior launch criterion without demanding a gap at all interior times. Use its sphere b and comparison coefficients, and set

\[
V_i^w(r)=-A_i^w/r+B_i^w/(3r^3),\qquad
\Delta_i(t,b)=V_i^w(b)-\Phi_i(t,b).
\]

Integrating the two exterior force bounds gives

\[
0\le\Delta_i(t,b)\le\Delta_{i,*}:=
\frac{A_i^s-A_i^w}{b}
+\frac{B_i^w-B_i^s}{3b^3}.
\tag{L1}
\]

At an outward crossing time t_b of a label z, cancellation of the same angular term gives the exact comparison launch energy

\[
q_i^w=E_i(0,z)+\mathcal W_i(t_b,z)+\Delta_i(t_b,b).
\tag{L2}
\]

Consequently the target-R launch certificate is exactly the work inequality

\[
E_i(0,z)+\mathcal W_i(t_b,z)+\Delta_i(t_b,b)
\le W_i^w(R,L(z))
\quad\hbox{at every outward crossing}.
\tag{L3}
\]

For example, if E_i(0,z)<=-eta_i0, it suffices to have eta_i0>eta_i+Delta_i,* and

\[
\mathcal W_i(t_b,z)\le
\eta_{i0}-\eta_i-\Delta_{i,*}
\quad\hbox{at every outward crossing}.
\tag{L4}
\]

This gives q_i^w<=-eta_i and the explicit launch-radius bound. Only the accumulated work sampled at these crossing times is constrained; an interior excursion can gain and return energy between samples. The small known exterior-potential allowance Delta_i,* accounts for the distinction between actual and comparison energies. These identities reduce the needed all-time estimate to the outgoing labels and times but do not by themselves prove that estimate.

## What the existing nonlinear estimates do and do not imply

The equilibrium has zero current. From the already proved stability norm,

\[
\sum_i\int|j_i(t,r)|dr
\le\sum_i\int|v|\,|f_i-F_i|d\Gamma
\le\tfrac12X(f(t)-F)<\epsilon/2.
\tag{23}
\]

Thus (11)-(12) yield

\[
\mathcal B_f(t)\le G\epsilon/(2\rho^2),\qquad
\mathcal B_t(t)\le
\frac{\epsilon}{2}\left(G/\rho^2+2cT/\rho^4\right).
\tag{24}
\]

They give a reserve loss at most C epsilon t, useful on any prescribed finite time interval. Here C depends on the individual data through rho and T; no uniform support-controlled neighborhood constant is asserted. They do not give a finite all-time positive-work budget. The missing estimate concerns accumulated work, not global classical existence or bulk stability.

At a fixed radius, int_0^t j_i(s,r)ds=M_i(0,r)-M_i(t,r) is already bounded. This does not control (13) at a moving particle radius. Nor does a vanishing long-time average suffice: the scalar rate 1/(1+t) has zero limiting average but divergent accumulated work. Conversely the scalar rate a cos(t) has a bounded signed primitive despite infinite positive variation. These are examples about work estimates, not constructed self-consistent halos. The signed pathwise criterion can therefore permit sustained oscillations excluded by (16).

An initial negative particle-energy gap, small initial canonical displacement, zero initial current, or small instantaneous force error is not shown here to propagate confinement. The external-field obstruction and the exact remaining self-consistent question are recorded in [ROUTES_AND_AUDIT.md](ROUTES_AND_AUDIT.md). The launch criterion in [EXTERIOR_LAUNCH_CRITERION.md](EXTERIOR_LAUNCH_CRITERION.md) tests only repeated outward passages instead of demanding a negative actual-energy gap throughout the core; numerical reserves for the two potentials require their own comparison.
