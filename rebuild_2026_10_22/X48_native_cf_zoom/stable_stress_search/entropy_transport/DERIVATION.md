# Conservative entropy redistribution for the gated material

The material remains `e=K W(rho)`, `P=K rho^2 h`, with the exact quiet gate
and latent energy from `../DERIVATION.md`. All scales below are fixed physical
parameters, not functions of resolution. These are Newtonian transport
constructions, not a derived relativistic theory or a production X48 change.

## Heat, viscosity and the first law

Write `Kstar=P0/rho_q^2`, `P0=a0^2/(8piG)`, `chi=K/Kstar`, `w=W/rho_q`.
For entropy coordinate sigma=chi^(1/3), the thermodynamic temperature is

\[
 T=\partial_\sigma e=3K_*\sigma^2W,\qquad
 \bar T=\chi^{2/3}w,\quad \psi=\bar T^{3/2}=\chi w^{3/2}.
\]

The baseline heat law is

\[
 F=-P_0D h^2\nabla\psi=-\kappa_{\rm eff}\nabla T,
 \qquad\kappa_{\rm eff}=\frac{\rho_qD}{2}h^2\sqrt{\bar T}\ge0.
\]

The h-squared gate matches the actual face product h_i h_j. The Kirchhoff
potential is linear in K at fixed geometry, avoiding a derivative singularity
at first warming while preserving hot-to-cold transfer.

Retain the old positive compression heater q_old. Add signed bulk stress

\[
 q_d=-\zeta\theta,\quad
 \zeta=\alpha_v\tau P_0 d w h\frac{\chi}{\chi+\chi_d}\ge0,
 \quad\theta=\nabla\cdot v,\quad C=(-\theta)_+.
\]

Use the same stress in momentum and heat equation:

\[
 \rho D_tv=-\nabla(P+q_{\rm old}-\zeta\theta)-\rho\nabla\Phi,
 \qquad
 \rho W D_tK=q_{\rm old}C+\zeta\theta^2-\nabla\cdot F.
\]

Then `rho D_t e=-(P+q_old+q_d)theta-div F`. Internal plus kinetic plus
self-gravitational energy is conserved with closed boundaries. Viscosity
damps both compression and expansion and supplies its own nonnegative heat.
The memory gate cannot seed K=0 by itself; q_old or incoming heat must do so.

For T>0,

\[
 \partial_t(\rho\sigma)+\nabla\cdot
 \left(\rho\sigma v+\frac FT\right)
 =\frac{q_{\rm old}C+\zeta\theta^2}{T}
 +\kappa_{\rm eff}\frac{|\nabla T|^2}{T^2}\ge0.
\]

At zero temperature evolve K rather than dividing by T. Seeding can give an
integrable entropy-rate singularity, not a finite classical rate at t=0.

## Exact finite-volume balances and quiet interfaces

Use one shared luminosity at each interface and zero boundary luminosities:

\[
 L_{i,i+1}=P_0D\frac{4\pi r_i^2}{\Delta r_c}
 h_i h_{i+1}(\psi_i-\psi_{i+1}),\qquad
 \dot K_i|_{\rm heat}=\frac{L_{i-1,i}-L_{i,i+1}}{dm_iW_i}.
\]

The energy sum telescopes exactly. Entropy contribution of each face is
`L(1/T_right-1/T_left)>=0`. If K_i=0, only nonnegative heat inflow can enter
that cell, so the nonnegative orthant is invariant while geometry is valid.

When h_i=0, its two face luminosities and local stress/heaters are exactly
zero, for arbitrary retained memory and neighboring temperatures. This is an
insulated material component boundary. A bare vanishing continuum gate times
a singular temperature gradient would not establish that interface statement.
Gravity and adjacent active pressure can still influence shared motion; actual
forest observables require their own calculation.

The implemented shell pressure work cancels the same internal-energy work,
including q_d, and node gravitational work cancels its declared discrete
potential. Time integration is not exact; measured energy/entropy error and
time refinement remain separate from these semidiscrete identities.

## Why passive heat mixing does not prove a floor

Persistent conduction equilibrates T, not K. At fixed uniform temperature in
the dense phase, `P=B sqrt(rho)` and `K=B rho^(-3/2)`. It admits

\[
 \rho=Ar^{-4/3},\quad
 A=\left(\frac{5B}{18\pi G}\right)^{2/3},\quad
 K=\frac{18\pi G}{5}r^2\longrightarrow0.
\]

Mass, internal energy, gravitational energy and entropy are integrable at the
center. The dense solution must be continued through the gated transition to
obtain a pressure-free vacuum surface; a bare dense truncation is not one.
The thermal enthalpy is

\[
 H_T=B\left[\frac2{\sqrt{W_q}}-\frac2{\sqrt W}
 +\frac{\rho h}{W^{3/2}}\right],\quad W_q=\tfrac32\rho_q,
\]

with finite ceiling `H_infinity=2B/sqrt(W_q)`. In the dense branch, a positive
central margin delta=H_infinity-H_c gives `K_c=delta^3/B^2`; approaching the
ceiling removes the floor. Finite heat and positive entropy production alone
do not bound this margin.

Nor does an isothermal exponent 1/2 by itself prove isolated instability.
At fixed total energy, thermal entropy maximization gives
`S=Kstar^(-1/3) U^(1/3) J^(2/3)`, `J=int W^(-1/2)dm`, `U=E-Omega`.
Microcanonical shape stability has an extra constraint term and must be
checked directly. The old frozen-entropy radial theorem is not a theorem
about the conducting equations.

## Instability-gated alternative

`CONVECTIVE_ROUTE.md` defines a distinct outward hot-to-cold flux that is
exactly zero when entropy is ordered stably outward. Its physical-gradient
gate prevents the mesh spacing from becoming a hidden transport parameter.
Shared luminosities retain energy conservation and nonnegative entropy
production. It is a heat closure, not resolved material overturn.

At fixed geometry its flux is monotone in the supplying K and antitone in
the receiving K. At a global material minimum, outgoing luminosity vanishes
and incoming luminosity and local heaters are nonnegative. Thus

\[
 D_+\min_iK_i(t)\ge\min_i Q_i(t)\ge0,
\]

where Q is the sum of local heater contributions. Geometry may vary without
changing this sign argument. If all material cells receive `Q_i>=q0>0` on a
fixed seeding interval independent of resolution, a genuine floor follows:
`min K >= q0 Delta t`, and is preserved afterward.

That sufficient condition is stronger than observed finite central warming.
For a central prefix, a comparison barrier additionally requires its outer
neighbor K to remain above the barrier, or its outer face to be insulated.
Without that protection the prefix minimum may fall even as the global minimum
rises. Quiet K=0 cells, changing active components and incompletely heated
boundary layers prevent silently replacing a central result by a global one.

The outward gate cannot seed a cold center from heat deposited only outside:
two active cells with K_inner=0 and a heater only outside have L=0 forever.
The specified collapse must therefore demonstrate its own central seeding.

The ordered singular thermal cusp above is also stationary for the gated law:
K increases outward, so transport is off, and a static velocity gives no
viscous heater. Thus this law does not exclude every zero-central-entropy
equilibrium. Any successful floor claim must concern its seeded initial-value
problem and a protected region, not all mathematically admissible states.

At a neutral K gradient, perturbations can turn transport on at first order;
gate=0 at an equilibrium does not alone recover the old adiabatic operator.
A strictly stable gradient margin, full transport perturbation analysis or
direct controlled relaxation tests are needed for a stronger stability claim.
