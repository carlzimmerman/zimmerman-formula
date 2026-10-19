# Confinement from outward crossing speeds

19 October 2026. Claim ZAR-C1. The model and nonlinear stability theorem are those of [checkpoint 05](../nonlinear_radial_2026_10_19/README.md). Here L is squared specific angular momentum, ell <= L <= Lambda, and v is radial velocity. No force, equilibrium or boundary wall is added.

## The exterior force bounds supplied by nonlinear stability

Let R_F be the equilibrium outer radius and let T and U be the actual conserved tethered and free masses of the perturbed solution. Suppose the previous theorem has been used to ensure

\[
\sup_{t\ge0}X(f(t)-F)<\epsilon.
\]

Because F vanishes outside R_F, at every time the total perturbed mass beyond R_F is at most epsilon. At every r >= R_F put tau = T-M_t(t,r), upsilon = U-M_f(t,r). Then tau, upsilon >= 0 and tau+upsilon <= epsilon. Write c = G^2/a_0. The exact forces imply the following bounds, using actual total masses rather than silently replacing them by equilibrium masses:

\[
-\frac{A_i^s}{r^2}+\frac{B_i^s}{r^4}
\le a_i(t,r)\le
-\frac{A_i^w}{r^2}+\frac{B_i^w}{r^4},
\]

\[
\begin{array}{c|cc|cc}
i&A_i^w&B_i^w&A_i^s&B_i^s\\ \hline
f&G[M_b+(T+U-\epsilon)_+]&0&G(M_b+T+U)&0\\
t&G[M_b+(U-\epsilon)_+]&cT^2&G(M_b+U)&c(T-\epsilon)_+^2.
\end{array}
\]

The superscripts w and s mean weaker and stronger inward force. In particular A_i^s >= A_i^w > 0 and 0 <= B_i^s <= B_i^w. For the tethered force, the exact difference from its vacuum expression is G upsilon/r^2 - c tau(2T-tau)/r^4. This proves both bounds and retains the different roles of the two species.

Define the static comparison effective potentials

\[
W_i^w(r,L)=\frac{L}{2r^2}-\frac{A_i^w}{r}
+\frac{B_i^w}{3r^3},\qquad
W_i^s(r,L)=\frac{L}{2r^2}-\frac{A_i^s}{r}
+\frac{B_i^s}{3r^3}.
\]

Choose a fixed sphere r=b containing the initial support and satisfying

\[
b\ge R_F,\qquad
b>\max_i\frac{\Lambda+
\sqrt{\Lambda^2+4A_i^wB_i^w}}{2A_i^w}.
\tag{1}
\]

Both comparison potentials increase strictly toward zero on r >= b, uniformly over the allowed L. More importantly, the actual radial acceleration obeys

\[
\ddot r\le\frac{L}{r^3}-\frac{A_i^w}{r^2}
+\frac{B_i^w}{r^4}<0\qquad(r\ge b).
\tag{2}
\]

An exterior excursion therefore has one outward leg, followed by return if it turns. An outward leg cannot restart entirely outside b. This is why every excursion can be tested at its outward crossing of the same sphere. Let such a crossing have time t_b, angular momentum L and outward speed u>0. Define its two launch energies

\[
q_i^w=\frac{u^2}{2}+W_i^w(b,L),\qquad
q_i^s=\frac{u^2}{2}+W_i^s(b,L).
\]

Every occupied characteristic and every repeated outward crossing is included. A condition on the initial crossing alone is insufficient.

## A sufficient condition for one fixed outer radius

Fix R>b. If all outward crossings of b satisfy

\[
\boxed{\frac{u^2}{2}+W_i^w(b,L)\le W_i^w(R,L),}
\tag{3}
\]

then the full spatial support stays inside R for all time. The equivalent speed threshold is

\[
u^2\le
2A_i^w\left(\frac1b-\frac1R\right)
-L\left(\frac1{b^2}-\frac1{R^2}\right)
-\frac{2B_i^w}{3}\left(\frac1{b^3}-\frac1{R^3}\right).
\tag{4}
\]

The right side is positive by (1). To prove the claim, on each outgoing exterior leg compute

\[
\frac d{dt}\left(\frac{v^2}{2}+W_i^w(r,L)\right)
=v\left[a_i(t,r)+\frac{A_i^w}{r^2}
-\frac{B_i^w}{r^4}\right]\le0.
\tag{5}
\]

Reaching r>R would make the left energy at least W_i^w(r,L)>W_i^w(R,L), contradicting (3) and (5). Equality at R can only occur with zero radial speed; (2) turns the trajectory inward. Initially everything is inside b, and all other portions of the characteristics remain inside b or return along the same exterior interval. Thus the assertion concerns all times and every particle, rather than an escaped-mass tolerance.

A convenient equivalent form of the sufficient comparison condition is a common negative launch gap: for some eta_i>0,

\[
\boxed{q_i^w\le-\eta_i\quad\hbox{at every outward crossing}.}
\tag{6}
\]

It implies

\[
R_{\rm supp}(t)\le
\max\left\{b,\frac{A_f^w}{\eta_f},
\frac{A_t^w}{\eta_t}\right\}\qquad(t\ge0),
\tag{7}
\]

because W_i^w(r,L) >= -A_i^w/r. Conversely (3) gives a uniform negative q_i^w gap: W_i^w(R,L)<0 continuously on the compact L interval. Hence (3) for some finite R and (6) for some common eta_i are equivalent as comparison certificates. The condition permits arbitrary interior energy exchange and indefinitely repeated bound oscillations.

If the initially occupied region extends beyond a previously chosen b, increase b to contain it. Alternatively apply the same energy cap at the actual initial r to every initially exterior outward particle and include the entire initial support radius in the final bound. Initially exterior inward or zero-speed particles cannot develop a new outward leg while remaining outside b, by (2).

## A necessary threshold and the size of the uncertainty

If the actual solution stays inside R, every outward crossing necessarily satisfies

\[
\boxed{\frac{u^2}{2}+W_i^s(b,L)\le W_i^s(R,L).}
\tag{8}
\]

Indeed the strong comparison energy has nonnegative derivative on outgoing legs. A trajectory confined to [b,R] must turn in finite time, since (2) is uniformly strictly negative on that compact interval. At its turning radius r_a <= R,

\[
q_i^s\le W_i^s(r_a,L)\le W_i^s(R,L).
\]

Thus (3) is sufficient, (8) is necessary. For the autonomous comparison force itself, weak and strong coefficients coincide, so the launch threshold is necessary and sufficient. In the exact self-consistent halo the thresholds differ by a controlled amount. With Delta W = W(R,L)-W(b,L),

\[
\Delta W_i^s-\Delta W_i^w
=(A_i^s-A_i^w)\left(\frac1b-\frac1R\right)
+\frac{B_i^w-B_i^s}{3}
\left(\frac1{b^3}-\frac1{R^3}\right)\ge0.
\tag{9}
\]

Here A_i^s-A_i^w <= G epsilon, and B_t^w-B_t^s <= 2cT epsilon. The gap between the necessary and sufficient squared-speed caps is twice (9), hence at most

\[
2G\epsilon\left(\frac1b-\frac1R\right)
+\frac{4cT\epsilon}{3}
\left(\frac1{b^3}-\frac1{R^3}\right).
\tag{10}
\]

The free species has only the first term. This quantifies precisely what the existing bulk-mass estimate leaves undetermined about the outermost particles.

Strict negativity at each crossing without one common gap excludes a single infinite outgoing leg under the weak comparison, but permits a family of increasingly distant turning radii. It does not prove a uniform halo boundary. In the Kepler comparison case, q_n increasing to zero from below gives apocenters tending to infinity, while q >= 0 gives escape. These are statements about the comparison dynamics, not a claimed self-consistent construction of such a sequence.

## Meaning of the condition

This is a sharp condition within the stated exterior force comparison class. It only tests outgoing launches instead of imposing a negative actual-energy bound at every interior point and time. No direct implication between numerical gaps for the actual and comparison potentials is asserted without aligning their reserves. It requires neither a stationary field nor finite total absolute current over all time. It is a dynamical condition, not a result that the initial small-X neighborhood propagates by itself. The necessary and sufficient thresholds coincide only when the force envelopes coincide. No globally weakest initial-data condition for the coupled system is asserted.

[The work and current estimates](BINDING_WORK_AND_CURRENTS.md) give independent sufficient certificates. [The scope statement](WARMTH_AND_SCOPE.md) combines confinement with the existing nonlinear stability, law and dispersion control.
