# Countercharge action checkpoint

User requested explicit charge-conserving action, fewer free parameters, energy
conservation and disk/dwarf/cluster separation without switches. Added only this
directory; all predecessor sources and manifests unchanged.

Derived inventory F neutral, T(+q,m), C(-q,epsilon*m). RAR weak-field normalization
fixes q/m=sqrt(4piG), alpha_G=Gm²/(hbar*c), field scaleD0=a0/sqrt(4piG). Electric
Hamiltonian h=D0²w(D/D0); Legendre ell=D0E-D0²log(1+E/D0). New 3D equation has
curlE=0 and divD=rho; old curlD=0 not retained. field.py solves periodic spectral
variational electrostatics for smooth sources. No galaxy dynamics or conversion
rates were fabricated. Opposite charges explicit; like-charge fixture alone has
uniform compensating background, not physical carrier model.

run_action completed/valid:8field solves N17,25,33, Gauss3.62e-8, force derivative
1.86e-8, grid25->33 neutral-pair energy1.96e-7 andforce1.80e-6. Like repel/opposite
attract.18nonlinear two-carrier mode integrations; both inertias included,
maxcoarseenergy7.64e-7, maxfineenergy9.67e-9, finalDchange2.48e-6. Oscillatory
not damped.4unit tests pass.1037RARgridpoints;68physical plasma scaling points;
1717micropoints,1135Coulomb-applicable. No physical population result claimed.

First-principles restrictions: coldT balance e=g gives aC=-(1+1/epsilon)g;
countercharge needs pressure/transport/etc. Under common virial proxy lambdaD/b
andomegaP*tdyn independentofMb,b, so no type selection. RAR atx=.1,epsilon=.1,
tolerance.05dex allows innerNC/NT<.01968484. Netneutral localrho cancels field.

Chargeflux capforcescore>=sqrt(Gm/a0). Controlled CoulombF boundstate aB>=10core
gives analytic continuous massbound; B/Tmax declines with epsilon, maximum at
epsilon1e-4. run_bound completed/valid evaluates this: maxB/T coolestfamily
1.32634e-26. Not an ionization-rate or cosmological-abundance conclusion. Extra
corephysics could change result and is not derived. Minimal single-invariant
Lorentz L(S) extension yields characteristicv²/c²=1+E/D0; fails subluminality.
Not a no-go for every medium/derivative/multifield/preferred-frame completion.

No activejobs. New sources uncommitted. Next route requires controlled collective
or alternative fieldcompletion, explicit conversion/corephysics and evolving
countercharges, not another arbitrary capturegap or frozen negativebackground.
