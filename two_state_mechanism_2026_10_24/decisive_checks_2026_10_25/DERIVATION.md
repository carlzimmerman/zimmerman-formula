# Three decisive checks on the actual mechanism

Research checkpoint: prior published archive commit
5c9cde2c9a528444ea7d5aea7621896e532d183e; working HEAD at start
b37983a0f7d5edbbad84e7f57b35ff8312ece9ac. Predecessor source preserved.

Target: one charge/energy-conserving microscopic theory deriving the acceleration
law, preparing its state and selecting disk tethering with dwarf/cluster free
mass, using common microscopic constants. Passing any check below is not that
target. Three routes: finite-temperature critical response; response/mass-budget
compatibility; and a thermal-state/relaxation ordering screen. No new simulation
is used to replace a missing microscopic derivation.

## A. Finite temperature destroys the exact ground-state critical law

Retain the actual predecessor four-level atom, not a substitute two-level atom:
its energies at field E are d*s +/- d*sqrt(s²+E²), and two dark levels 2*d*s.
Let r=sqrt(s²+E²), Tbar=k_B*T/d. Its partition function is
Z=2*exp(-s/Tbar)*[cosh(r/Tbar)+exp(-s/Tbar)].
The dipole response is
P_s=n(s)*d*E/r * sinh(r/Tbar)/[cosh(r/Tbar)+exp(-s/Tbar)].

Normalize s_max=d=1 and n(s)*d=chi*s on0<s<1. With tau=kBT/(d*s_max),
P/(chi*E)=integral_0^1 s/r F(r,s,tau) ds,
F=tanh(r/tau)/[1+2*exp(-(r+s)/tau)/(1+exp(-2r/tau))].
At tau0 this is sqrt(1+E²)-|E|, the predecessor critical response.
The exact thermal zero-field susceptibility is
chi_T/chi = 1-(2*tau/3)*log[4/(1+3*exp(-2/tau))].

For any fixed tau>0 the finite internal Hilbert space has an analytic partition
function around E=0, uniformly over the compact s interval. Its denominator is
positive there; apparent r singularities cancel. Inversion symmetry makes P odd.
Thus P=chi_T E+O(E³), with no E|E| term near zero. Thermal averaging makes the
infrared response analytic even though the zero-temperature gap distribution
extends to zero. Infinite interacting thermodynamic critical states are outside
this proof. Internal T need not equal orbital/virial temperature.

There are TWO distinct failures, and they must not be conflated:
1. With q/m fixed by the original zero-temperature chi, the source is
   S=g-[4*pi*G/beta]*D = [chi*g-beta*P]/(1+chi).
   Therefore S/g tends to (chi-chi_T)/(1+chi)>0: the deepest law becomes linear.
2. Even if charge matching were illegally retuned to chi_T in each environment,
   the cancelled leading remainder would be cubic, not quadratic.

Use f=chi/(1+chi), g_star=f*a0, x=g/a0, E/s_max=x/f. The fixed-parameter source is
S/a0=f*x*(1-P/(chi*E)). The static test solves this at fixed source. It measures
thermal deviation from the same candidate's zero-temperature curve, not an
observational RAR likelihood and not an exactly fitting cold law.

A temperature-dependent optical spectrum or a different interacting phase can
escape these assumptions, but must be derived. It cannot claim the ground-state
curve while omitting the thermal density matrix.

## B. Response speed, gravitating mass and the light-countercharge loophole

For the predecessor canonical charged-constituent critical spectrum, the dipole
sum rule gives Omega_max²<=12*pi*G*rho_M/(epsilon*f), where rho_M is all the
bound medium's gravitating rest mass. The field-relevant modes at x have a
representative dressed frequency Omega_rel~sqrt(2)*Omega_max*x/f. This is a
representative adiabatic-mode diagnostic, not a bound on every conceivable
collective response or a relaxation rate.

If local mean densities are identified with spherical enclosed averages,
t_dyn²=3/(4*pi*G*rho_total), then
(Omega_rel*t_dyn)² <=18*x²/(epsilon*f³)*(rho_M/rho_total).
This identification is an explicit geometry/uniformity approximation.

For a target simple spherical law S/a0=x²/(1+x), let t=10^delta, and allow extra
positive medium mass to raise g from x*a0 to t*x*a0 at fixed baryons. The maximum
additional enclosed medium fraction of total gravitating mass at that upper
edge is
F_M,max=[t²*x²/(1+t*x)-x²/(1+x)]/(t*x).
It is O(x) at small x (not O(x²)). Consequently the representative response
condition Omega_rel*t_dyn>=A requires
epsilon <=18*x²*F_M,max/(A²*f³), scaling as x³.
This budget assumes no cancellations, positive added medium mass and the stated
simple-law equilibrium; a free-mass component only uses more of the budget.
Using this exact simple-law budget with the approximate fitted critical medium
is a diagnostic comparison, not a proof that both hold exactly together.

The plasma comparison needs care. If n_C=alpha*n_T locally, the optimistically
screened carrier frequency is omega_p²=4*pi*G*rho_T*(1+alpha/epsilon).
Combining with Omega_rel gives
(Omega_rel/omega_p)²<=6*x²*(rho_M/rho_T)/[f³*(epsilon+alpha)].
For alpha1, taking epsilon->0 does not help; for alpha0 it CAN help. A nearly
countercharge-free tether region is not a locally neutral plasma. Claiming that
this cancellation is a universal no-go would be incorrect. Confinement, pressure,
nonadiabatic preparation and nonlocal response remain genuine loopholes.

The cutoff relation d*s_max=hbar*Omega_max/2 also converts the thermal tolerance
from route A to a physical temperature ceiling:
T <= tau_tolerance*hbar/(2*k_B)*sqrt(12*pi*G*rho_M/(epsilon*f)).
Use the entire available dark reservoir for rho_M as an optimistic upper bound;
this does NOT justify neglecting its gravity in the RAR. None of these formulae
derives epsilon, the density state or a cooling mechanism to attain this T.

## C. State-selection ordering without morphology labels

For common particle masses, an ideal Bose equilibrium condensation/degeneracy
indicator scales as rho/sigma³, since n*lambda_thermal³ is proportional to
rho/(m^4*sigma³). With the shared inventory rho=3*eta*Mb/(4*pi*b³) and
sigma²=G*(1+eta)*Mb/(6*b), this indicator scales as
Mb^(-1/2)*b^(-3/2). In the four historical inputs the smallest dwarfs are
MORE degenerate than the large disk. A common monotone threshold cannot condense
the large disk while keeping those dwarfs normal under these state assumptions.
Rotation is not itself an internal temperature or a relative collision speed.

For comparison only, a classical Rutherford relaxation estimate gives
Gamma~n*sigma_transport*v~G²*m*rho*logLambda/v³ at fixed mass ratio and force
matching, so the same ordering appears when a common Coulomb logarithm is used.
Multiplying this by a high-occupation Bose factor produces the schematic
rho²/v^6 ordering. We do NOT use this heuristic multiplication to predict an
absolute condensation time, and do NOT equate gravitational cooling with
collisional Bose condensation. Their regimes and processes differ.

A short-range collision rate proportional to rho*v would have a different
ordering and can favor the dense disk input. That route is not excluded: it
requires a separately justified interaction/cross section and an acceleration-
producing state. A new freely fitted contact coupling would not be a derivation
from the existing matched Coulomb theory. Likewise nonvirial assembly histories
could change state ordering; they have not been derived here.

Context: superfluid dark-matter models propose galaxy/cluster phase differences,
https://arxiv.org/abs/1507.01019 . This is a distinct model with its own effective
interactions; we do not import its phenomenology as a proof of repulsive tethering.
Gravitational kinetic condensation is studied in
https://arxiv.org/abs/1804.05857 ; only our explicitly stated scaling screen is
computed, not that paper's full kinetic solution.

## Claim discipline

Route A is an analytic result for the specified four-level thermal spectrum.
Route B is a necessary consistency screen within named sum-rule, geometry and
adiabatic assumptions, not a universal exclusion. Route C is a conditional
ordering theorem for the stated one-zone state prescription, not real-galaxy
classification. The original microscopic theory remains missing. No spontaneous
state selection, exact a0, dark-matter abundance or observational fit is derived.
