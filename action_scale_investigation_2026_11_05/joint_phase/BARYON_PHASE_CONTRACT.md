# Baryonic loading and vacuum-phase pressure contract

Base checkpoint: c28bc49408 pool-pressure result; working HEAD at start
44192e0129077db4ff99afe95dae38c5d49c58dd. Only this investigation directory
is writable for this task. Target remains a0=c sqrt(G rho_DE)/2 without
using the target to choose a coupling, state, or boundary condition.

Route A: include a resolved Plummer baryonic mass profile and pool self-gravity
in isothermal hydrostatics. Test whether the same baryon mass, dispersion and
surface pressure permit distinct pool inventories. Dimensionless equations:
m'=x^2 d, (ln d)'=-(m+B x^3/(1+x^2)^(3/2))/x^2, B=1.
Take central d=0.01,0.03,0.1 and surface d=0.001, fixed before execution.
Use DOP853 rtol 1e-9 and 1e-11, atol=rtol/100, initial x=1e-5,
outer cap 300, max step .2. Require each surface event and mass/radius
agreement below 1e-6 relative. These are illustrative dimensionless fixtures,
not an empirical or coefficient scan. Derive continuity and chemical-potential
normalization analytically. Distinct masses refute uniqueness for these
specified equilibrium inputs, not every possible cosmological attractor.

Route B: explicit scalar phases V=Vout+lambda(phi^2-v^2)^2/4+DeltaV q(phi/v),
q(z)=(2+3z-z^3)/4. Add baryon energy epsilon rho_b c^2 q.
Derive phase minima, energy difference, local stability, and thin-wall pressure
from energy variation. Keep DeltaV, epsilon, tension, and Vout independent.
Check a uniform bubble extremum's second derivative; do not identify a
nucleation maximum with a stable pool. The scalar model is illustrative,
not an adopted action. Derive the extra force from baryonic coupling too.

Route C: test whether conserved particle inventory or a conserved baryon-linked
charge can close Mp(Mb). Show what new charge/mass/chemical-potential inputs
would be needed. Do not substitute a ratio chosen to reproduce 1/2.

Exact symbolic checks plus the six ODE solves, 60 seconds and one thread.
Negative control reverses the vacuum pressure sign in the wall variation;
the derivative identity must fail. No observed galaxy data, coefficient
search, complete stability spectrum, or relativistic galaxy fit claimed.
