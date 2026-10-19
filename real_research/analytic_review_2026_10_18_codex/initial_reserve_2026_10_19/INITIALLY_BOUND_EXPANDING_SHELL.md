# A smooth initially bound radial population with unbounded outer support

19 October 2026. Claim ZAR-P2. This construction is a self-consistent radial solution of the actual two-population model, rather than a prescribed pumping field. It refutes confinement from an unquantified initial negative particle-energy gap alone in the broad angular interval specified below. Its gap shrinks with the added mass, its initial support extends outside the old halo, and it is not a canonical rearrangement of the original equilibrium. These restrictions are essential.

## Initial parameters and the smooth outer population

Let F_t,F_f be the exact warm equilibrium with outer radius R_F and masses T_F,U_F. Set

\[
A_c=G(M_b+T_F+U_F),\qquad
A_{\max}=A_c+G\delta_0,
\]

where delta_0>0 is fixed. Choose a fixed allowed angular interval containing the equilibrium supports and an additional subinterval [L_0,L_1] satisfying

\[
L_1>L_0>2A_{\max}R_F.
\tag{13}
\]

This is a genuine extra range assumption. It need not hold for an arbitrarily narrow previously fixed interval. Choose alpha>0, kappa_minus,kappa_plus such that

\[
\frac12<\kappa_-<\kappa_+<\frac1{1+\alpha},
\tag{14}
\]

and choose a fixed R>max(R_F,L_1/A_c). For each 0<delta<=delta_0 append a free population g_delta of mass delta with compact smooth support in

\[
R<r<(1+\alpha)R,\quad L_0<L<L_1,
\quad \kappa_-\frac{G\delta}{R}
<e_c(r,v,L)<\kappa_+\frac{G\delta}{R},
\tag{15}
\]

\[
e_c=\frac{v^2}{2}+\frac{L}{2r^2}-\frac{A_c}{r}.
\]

Both radial velocity branches can be populated equally, so g_delta is even in v and initially has zero radial current with positive centered radial dispersion. The radicand for v is strictly positive on this band because R>L_1/A_c.

For an explicit smooth choice, take nonnegative nonzero C-infinity bump functions q,zeta,eta supported respectively inside (1,1+alpha), (L_0,L_1), (kappa_minus,kappa_plus), and normalize

\[
g_{\delta,0}(r,v,L)=c_\delta
q(r/R)\zeta(L)
\eta\left(\frac{R e_c(r,v,L)}{G\delta}\right)
\tag{16}
\]

to mass delta in dGamma=4 pi^2 dr dv dL. This is even in v. Changing from v to e_c on either branch has Jacobian 1/|v|. Since |v| is bounded above and below by positive constants times R^(-1/2), the unnormalized phase integral is comparable to delta sqrt(R), with constants independent of delta. Thus c_delta is comparable to R^(-1/2) and the distribution heights can be kept within a prescribed bound by enlarging the fixed R if needed. Each distribution is smooth; no derivative bound uniform as delta tends to zero is asserted.

Set f_t,0=F_t and f_f,0=F_f+g_delta,0. The supports of F and g are initially spatially separated, all masses and kinetic moments are finite, and the initial X distance is O(delta).

## Every initial individual particle energy is negative

Let psi_g be the Newtonian self potential of g, zero at infinity. For every point in its initial support, the spherical kernel gives

\[
-\frac{G\delta}{R}\le\psi_g(0,r)
\le-\frac{G\delta}{(1+\alpha)R}.
\tag{17}
\]

The tail's actual free-particle energy is E_g=e_c+psi_g. By (14)-(17),

\[
\boxed{E_g(0)\le
-\left[\frac1{1+\alpha}-\kappa_+\right]
\frac{G\delta}{R}<0.}
\tag{18}
\]

The original core particles also have strictly negative actual initial energies: the external free shell adds a negative spatially constant gravitational potential inside R_F. Thus for each fixed delta the entire initial halo has a common strictly negative energy upper bound. That bound is not fixed uniformly as delta tends to zero.

## The outer population never enters the core

The following comparison uses only the total mass bound, and therefore does not assume spatial separation at later times. For any free characteristic,

\[
a_f(t,r)\ge-A_{\max}/r^2.
\]

For a tail particle put e_A=v^2/2+L/(2r^2)-A_max/r. Initially,

\[
e_A=e_c-G\delta_0/r<0
\]

by (14)-(15). On an inward leg,

\[
\frac d{dt}e_A=v(a_f+A_{\max}/r^2)\le0.
\tag{19}
\]

Any later inward leg begins at an outer turning point a. There ddot r<=0, while ddot r>=L/a^3-A_max/a^2, so a>=L/A_max. Hence e_A(a)<=-A_max/(2a)<0. Consequently e_A<0 on every inward leg and

\[
\boxed{r>\frac{L}{2A_{\max}}\ge
b_0:=\frac{L_0}{2A_{\max}}>R_F.}
\tag{20}
\]

Outward legs start at radii already above b_0 and increase. This proves the barrier for all time. It applies equally to the two even velocity branches.

One can construct the full solution without a bootstrap: solve the ordinary radial self-gravitating free tail in the fixed central potential -A_c/r. The global classical characteristic theorem applies to that one-population equation with positive central mass and angular gap. The same barrier (20) keeps it outside R_F. Then set f_t(t)=F_t and f_f(t)=F_f+g_delta(t). Inside the core the tail's enclosed mass is zero, so both actual accelerations are exactly the old core accelerations. Outside it the original core contributes exactly -A_c/r to free-particle potential. The combined distribution therefore solves the full coupled system exactly. The core's potential can acquire a time-dependent spatial constant; its force and stationary phase distribution remain unchanged.

## Positive collective energy forces the support to expand

The conserved Hamiltonian of the isolated tail is

\[
H_g=K_g+W_c+W_g
=\int e_c g\,d\Gamma+\frac12\int\psi_g g\,d\Gamma,
\]

\[
K_g=\frac12\int(v^2+L/r^2)g\,d\Gamma,
\quad W_c=-A_c\int r^{-1}g\,d\Gamma,
\quad W_g=\frac12\int\psi_g g\,d\Gamma.
\]

Equations (15) and (17) give

\[
\boxed{H_g\ge(\kappa_--\tfrac12)
G\delta^2/R>0.}
\tag{21}
\]

There is no contradiction with (18). Individual energies include the full self potential, whereas the collective Hamiltonian counts it with a factor one half. The self-consistent field is time dependent and individual energies are not conserved.

Let I_g(t)=int r^2 g dGamma. Every finite-time solution is compact, so integration by parts is justified. Since the external point potential and Newtonian self potential both have degree -1 under spatial dilation,

\[
I_g''=4K_g+2(W_c+W_g)=2K_g+2H_g\ge2H_g.
\tag{22}
\]

This can also be checked directly: I_g''=2 int[v^2+L/r^2+r a_f]g, with int r a_c g=W_c and int r a_g g=W_g. The initially even g has I_g'(0)=0. Hence

\[
I_g(t)\ge I_g(0)+H_g t^2,
\qquad
\boxed{R_{g,\rm supp}(t)\ge
\sqrt{H_g/\delta}\,t.}
\tag{23}
\]

The whole halo therefore has no finite time-independent outer support radius. The theorem establishes unbounded support and a linear lower growth bound; it does not identify a fixed positive-mass set whose every trajectory tends to infinity.

## Stability and the inner law nevertheless remain exact or controlled

The tail stays beyond b_0. Its negative potential energies have uniform lower bounds

\[
W_c\ge-A_c\delta/b_0,\qquad
W_g\ge-G\delta^2/(2b_0).
\]

Energy conservation therefore gives

\[
K_g(t)\le H_g+A_c\delta/b_0+G\delta^2/(2b_0),
\]

\[
\boxed{\sup_{t\ge0}X(f(t)-F)
=\sup_{t\ge0}(\delta+2K_g(t))
\le\delta+2H_g+2A_c\delta/b_0+G\delta^2/b_0
=O(\delta).}
\tag{24}
\]

The old core densities, exact law annulus and centered radial dispersion are unchanged at every time, not merely close. The added tail is an ordinary bounded smooth radial distribution with nonzero initial radial dispersion. The expanding example is thus compatible with nonlinear bulk stability and a warm exact-law core.

The conclusion is restricted to a fixed interval broad enough for (13), mass-changing perturbations with an initially exterior shell, and an initial energy gap that can shrink with delta. It does not refute confinement in a sufficiently small neighborhood with a separately prescribed negative gap independent of perturbation size, with unchanged initial support, with exact original Casimirs, or with a narrow angular interval excluding (13). Those sharper strict-radial subclasses remain open. It does refute the general inference from smoothness, small X, initial evenness, zero initial current and an unspecified strictly negative initial particle-energy cap to all-time outer confinement.
