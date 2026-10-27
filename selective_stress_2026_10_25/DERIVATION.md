# Selective stress and conversion pumping

These are new constitutive hypotheses and bounded component tests. The original
galaxy-formation objective is not inferred from them.

## Species-selective stress

Let rho=rhoT+rhoF, theta=arcsin(sqrt(rhoT/rho)), and alpha=pi*x/2 for the
independent vacuum carrier. Preserve the previous response, gravity, carrier,
volume and binding terms, but replace coherent-spinor material gradients by

    Egrad = integral [kT |grad sqrt(rhoT)|^2
                     + kF |grad sqrt(rhoF)|^2]/2 dV.

Each k is nonnegative. The cold incoherent T hypothesis is kT=0; kF is the
previous common physical coefficient, scaled as rM^-3 in dimensionless units.
This is a two-fluid constitutive model; it is not obtained by dropping a
required term from a canonical coherent spinor. Its microscopic conversion
and entropy law remain unspecified.

Alignment has an exact nonsingular amplitude representation:

    Ealign = J integral (sqrt(rhoT) cos(alpha)
                         -sqrt(rhoF) sin(alpha))^2 dV.

This identity motivates separate density amplitudes for numerical solving.
Write Phi=delta Egravity/delta rho, Psi=delta Eresponse/delta rhoT, including
the response dependence of the carrier barrier and gradient coefficient.
For positive species densities the chemical potentials are

    muT = Phi + Psi - epsilon
          + J[cos(alpha)^2-sqrt(rhoF/rhoT) sin(alpha)cos(alpha)]
          - kT Delta sqrt(rhoT)/(2 sqrt(rhoT)),
    muF = Phi + (5/2)K rhoF^(2/3)
          + J[sin(alpha)^2-sqrt(rhoT/rhoF) sin(alpha)cos(alpha)]
          - kF Delta sqrt(rhoF)/(2 sqrt(rhoF)).

Forces per unit mass are -grad(mu_i). Endpoint statements require direct
variations, not substituting zero into these divided expressions. Carrier
variation preserves the old response force Xi_x, volume force B qx', vacuum
gradient force -ell_v^2 Delta x, and alignment force

    -pi J [sqrt(rhoT)cos(alpha)-sqrt(rhoF)sin(alpha)]
           [sqrt(rhoT)sin(alpha)+sqrt(rhoF)cos(alpha)].

On a pure aligned T interval x=1 and kT=0, alignment energy is J rhoF and muT
has no material-gradient force. Thus the PC-28 *pure-T stiffness* obstruction
does not apply. This does not prove that the transition is filled, that F is
absent in the core, or that the finite-radius equilibrium follows the law.
F quantum stress alone may leave an unconstrained T depletion mode.

## Autonomous conversion pump

The previous radiation test supplied an initial modulus oscillation. To test
that missing implication, consider an explicit reduced Hamiltonian after the
fast modulus tracks a conversion coordinate q:

    S(q)=1+sin^2(pi q/2), V(q)=cos^2(pi q/2)/4,
    H=P^2/2+V(q)+p^2/(2S(q)^2)+S(q)^2 k^2 chi^2/2.

q=0 is the unstable unconverted state and q=1 a converted minimum. q is a
periodic order coordinate; its fraction sin^2(pi q/2) remains in [0,1]. The
angular mode chi has positive inertia and a massless dispersion prior to
finite-mode truncation. Equations are

    qdot=P,
    Pdot=-V'(q)+S'(q)[p^2/S^3-S k^2 chi^2],
    chidot=p/S^2,
    pdot=-S^2 k^2 chi-gamma p,
    Qdot=gamma p^2/S^2.

Direct differentiation gives Hdot=-Qdot, hence H+Q is conserved and escape
is passive. A seed q=1e-4, chi=1e-6, P=p=0 contains essentially all initial
energy in the conversion potential. It contains no initial radial oscillator
energy. This tests actual transfer from a conversion potential into radiation,
not gravitational collapse or the galaxy boundary.

The rates remain a substantive physical constraint. For a 100 Myr conversion
time and 56 kpc source, light escape is of order 500 conversion frequencies;
the earlier favorable gamma=.005 regime is not that free-space hierarchy.
Both regimes are tested. A single leaking Fourier mode is not an authenticated
outgoing continuum; its success cannot determine the physical escape rate.

## Gradient relaxation versus physical conversion

For chemical potentials from any stated energy functional, fluxes
Ji=-Mi rhoi grad(mu_i) and conversion Gamma=L(muF-muT), with nonnegative
mobilities and L, give

    rhodotT=-div(JT)+Gamma, rhodotF=-div(JF)-Gamma,
    Edot=-integral [sum_i Mi rhoi |grad(mu_i)|^2
                   +L(muF-muT)^2] dV,

under vanishing boundary work. Thus mass is conserved and energy decreases.
Positivity needs a compatible conversion mobility/endpoint law, for example
L proportional to rhoT*rhoF with a nonzero seed. Adding an escaped-energy
ledger equal to -Edot conserves total bookkeeping energy, but does not derive
a radiation channel or its rate. Changing positive mobilities cannot repair
an existing force imbalance at an equilibrium. This excludes relabeling the
old numerical optimizer as a physical galaxy-formation calculation.
