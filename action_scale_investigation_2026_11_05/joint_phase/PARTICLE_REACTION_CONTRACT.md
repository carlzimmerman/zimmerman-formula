# Actual reaction and energy-accounting test

Base65954af232. Target unchanged: realize the proposed global abundance feedback
from a particle interaction, preserve rotation scaling, derive coefficient1/2.
Only this investigation directory may be modified.

Illustrative canonical real fields: stable Z2-odd chi of mass m; mediator S of
mass M>2m; light radiation a. Interactions -g S chi^2/2-lambda chi^2 a^2/4,
plus a baryonic portal -y S Nbar N and positive stabilizing quartics. Derive
S->chi chi decay and nonrelativistic chi chi->a a annihilation with identical
final-state factors. The portal permits stellar emission but its luminosity
is NOT computed or assumed proportional to baryon mass by the Lagrangian.

Use steady radial ballistic mediator propagation, constant speed and decay
length l. Derive particle injection, balance with two-body annihilation, radial
profile, and rotation scaling. Track rest-mass and kinetic energy, capture and
angular/threshold constraints. Do not relabel a density profile as the global
feedback equation from the preceding toy attractor.

Finite checks: exact symbolic rate factors, continuity, source/loss equilibrium,
energy balance and profile scaling. Local fixed-volume example n_dot=J-K n^2,
cv n T_dot=J(e_in-cv T)-Lambda n^2 T with constants J=2,K=0.5,cv=1,
e_in=3,Lambda=0, no extra phenomenological cooling or heating. Annihilation
removes the sampled particles and their mean kinetic energy; daughters escape. Fixed before execution. Initial
(n,T)=(0.2,0.5),(2,0.5),(0.5,2),(3,4), DOP853 t0..40 rtol1e-10 atol1e-12,
max_step0.1. Require positive solutions and convergence to independently derived
equilibrium within1e-7. Negative control omits kinetic dilution -cv T J;
the conservation identity must fail.60 seconds,one thread.

Nonclaims: no stellar emissivity calculation, data fit, full halo transport,
threshold abundance prediction, selected dark-energy offset or boundary.
Local kinetic stability does not imply correct global gravity or rotation curves.
