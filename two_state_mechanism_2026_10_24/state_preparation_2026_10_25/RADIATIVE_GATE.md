# Can independent microscopic dipoles cool the prepared medium?

This is a conditional rate bound, not a calculation of collective-band cooling.
It applies only if each mode is an independent local opposite-charge pair with
dipole matrix element d=q*ell, masses m and epsilon*m, and the SAME vacuum
Maxwell charge that gives the predecessor's screened tether cancellation:

    q^2/(4*pi)=G*(1+chi)*m^2.

Rationalized Maxwell units absorb the SI epsilon_0 into q and d. For an isolated
transition of frequency omega, weak coupling to vacuum transverse radiation,
and an electric dipole whose extent is small compared with c/omega,

    Gamma_vac=omega^3*d^2/(3*pi*hbar*c^3).

Primary source for the conventional SI formula (with epsilon_0 restored):
Richard Fitzpatrick, Spontaneous Emission, Eq.1131,
https://farside.ph.utexas.edu/teaching/qmech/lectures/node119.html .
The source supplies the single-transition vacuum rate, not an astrophysical or
collective-medium theorem.

For a declared dipole-regime cap omega*ell/c<=zeta, substitute d=q*ell:

    Gamma_vac/omega=(4/3)*(1+chi)*(G*m^2/(hbar*c))*(omega*ell/c)^2,
    Gamma_vac <= (4/3)*(1+chi)*G*m^2*zeta^3/(hbar*ell),
    t_rad >= 3*hbar*ell/[4*(1+chi)*G*m^2*zeta^3].

Use zeta=.1, with .03 as a stricter validity check. These are declared bounds on
the dipole approximation, not fitted physical constants. The spatial extent
of a real emitter could exceed its transition length ell, making these
optimistic limits still more optimistic. No claim is made for larger k*ell,
multipoles, strong-coupling radiation or a non-vacuum photon density of states.

The predecessor's UNINTERACTING critical-curve local-pair inventory gives

    rho_M*ell=(1+epsilon)*f^2*a0/(8*pi*G), f=chi/(1+chi).

Assigning the entire available dark reservoir
rho_available=3*eta*M_b/(4*pi*b^3), eta=5.364, to rho_M yields ell_min. For any
ell>=ell_min, the same rate upper bound is smaller. To get even one spontaneous
transition in t_available, a necessary condition is therefore

    m >= sqrt(3*hbar*ell_min/[4*(1+chi)*G*zeta^3*t_available]).

Numerical table uses a0=9.3603e-11 m/s^2, chi=11.220184543019636, epsilon=.1,
t_available=10 Gyr and the four earlier inventory profiles. These profile labels
are output labels, not branches of a physical rule. Bounds also evaluated at
epsilon=1e-8 to check the small-countermass limit.

This does not use the oscillator-strength ceiling on omega, which can strengthen
the restriction. It generously treats one transition as sufficient cooling and
assumes the emitted photon escapes without reabsorption. The much slower
low-frequency modes can only worsen independent radiative relaxation.

It cannot be transferred to collective states by identifying a Bloch mode with
one pair. Coherent many-emitter enhancement, collective currents, strong optical
response, collisional transfer to an independently escaping species, nonlocal
matrix elements or a different charge-to-mass relation require new analysis.
An actual collective emission mechanism must account for its coherence volume,
photon escape, energy and countercharge mass; multiplying this rate by a guessed
particle number would not establish it. The interaction-renormalized static fit
in DERIVATION.md is not inserted into this independent-pair inventory formula.

Interpretation: the formula fixes a candidate forward decay rate from the same
charge and dipole, instead of introducing an adjustable cooling coefficient.
It screens a proposed preparation mechanism. It does not prove that all quantum
media fail to cool, or derive disk/dwarf/cluster separation.
