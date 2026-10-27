# Reaction closure: what is derived and what remains unknown

## A newly resolved physical cycle

Atomic capture X+C -> A+gamma and molecular photobreakup
T_b+gamma -> A+X combine to T_b+C -> 2A. This photon-mediated channel is
already present in the dynamic solver; it needs no new four-body collision
coefficient. At the shared photon energy
 .5+E_atomic = D_b+E_breakup,
it releases .5-D_b into matter kinetic energy. The reverse cycle exists when
a molecular-capture photon has enough energy to ionize an atom. This is not
instantaneous, local direct dissociative recombination: photons have finite
residence, absorption competition and escape in the implemented closure.

The same explicit radiation can repeatedly ionize and re-form atoms, leaving
positive carriers available for molecular capture. Hence the previous
irreversible kinetic bound of4.42% does NOT apply. Indeed some radiative-only
runs exceed it, though none meets the requested separation screen.

## Why detailed balance is not an absolute rate calculation

For direct T_b+C <-> 2A, define a forward coefficient d_b(T) for destruction and
an inverse coefficient i_b(T), with inverse event rate i_b n_A². Equilibrium
requires i_b/d_b=K_A/K_b. For every positive function lambda_b(T), replacing
(d_b,i_b) by (lambda_b d_b,lambda_b i_b) preserves:
- net charge and both constituent counts;
- the energy defect fixed by the molecular spectrum;
- the entire equilibrium manifold and detailed balance.
It changes the finite-time evolution. Therefore these constraints do not fix
that remaining kinetic function. This is an identifiability statement about
the present reduced data, not a claim that the complete Coulomb Hamiltonian
cannot determine scattering amplitudes.

Likewise, impact breakup and its three-body inverse have a fixed ratio but
require a continuum collision matrix element. A photon dipole transition of
one electron is not the two-electron scattering S-matrix. Borrowing ordinary
hydrogen rates at mass ratio1836 and assigning them to each mass-ratio100 state
would be an additional approximation, not a first-principles derivation.

## Rapid-collision limit and a uniform constraint

The fast solver takes these direct collisions infinitely fast on the retained
X,C,A,T_b species. This enforces the Saha relations while radiation remains
explicit and evolves. It is a limit test, not a fitted finite relaxation rate.
Fast chemical relaxation initially converts the fully ionized gas at its SAME
energy and constituent counts to the equilibrium manifold; subsequent matter
energy is an independent state, exchanging energy with photon groups.

Set q=N/K_A and r=N/K_T, where K_T=(mu_AX T/(2pi))^1.5/Z_T and
Z_T=sum_b g_b exp(D_b/T). Equilibrium x satisfies the monotone cubic
 q r x³ + q(1+r)x² + x - 1=0.
Then a=(1-x)/(1+2rx), t=rx(1-x)/(1+2rx), c=x+t,
and t_b=t g_b exp(D_b/T)/Z_T. These relations avoid inaccurate subtraction
of nearly equal ionized fractions when the neutral abundance is very small.

Eliminating densities gives t(x+t)=a²/(K_T/K_A). Since x>=0 and a<=1-2t,
 t <= 1/[2+sqrt(K_T/K_A)].
All23 D_b<.5 and sum_b g_b=147, so
 K_T/K_A >= (mu_AX/mu_A)^1.5/147.
For the retained BO convention mu_A=1 and mu_AX=100*101/201, this gives
 molecular mass fraction <= .559546302
at every density and temperature on this manifold. It eliminates density,
age, alpha and absolute collision normalization from the80% target in the
rapid-collision limit. No such global bound has been proved for intermediate
collision rates with trapped photons. The two tested limits need not bracket
every intermediate trajectory.

## Still missing

No finite state-resolved direct dissociative-recombination, collisional
ionization, molecular collisional breakup or three-body coefficient has been
derived here. Neutral X2C2 molecules, negative XC2 ions, excited atomic levels,
their reactions and radiative cooling remain unmodeled in both limits.
Their energies and couplings require additional two-electron calculations.
The retained thermal gas and sphere closure are not full chemical, kinetic,
spatial or gravitational simulations. Charged molecular mass is not proof of
a tethered orbital population or preservation of the galaxy acceleration law.
