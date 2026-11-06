# What generates the barrier and sustains the radiation bath?

## Outcome

An explicit heavy-field interaction generates a two-phase barrier without
putting its height directly into the effective potential. The resulting height
and wall properties depend on that interaction's masses and couplings; they
are not selected by the absolute dark-energy density.

Coupling conversion to radiation losses exposes an independent constraint:
a finite closed vacuum reservoir has no steady positive radiation output.
Temperature feedback can regulate conversion transiently, but does not erase
reservoir depletion. Replenishment permits steady output only by supplying a
new energy flux whose normalization is not fixed here. Thus no whole-halo
stability or MOND1/2 has been established.

Base694ea3f1cc; contract0d93a34136. This is a candidate phase-sector extension,
not a unique consequence of the river analogy or an adopted particle theory.
The existing material capture, cooling, and boundary requirements still apply.

## 1. Generate a barrier from an interaction

In natural units, take canonical real fields phi and a heavy field S, with

    V=V0+a phi^2/2+lambda_v phi^4/4
      +(M^2+h phi^2)S^2/2+g_phi S phi^2/2.

M^2,h,lambda_v are positive. g_phi is a phase-sector coupling; it is not
silently identified with the mediator's particle-production coupling or the
chi-a scattering coupling from earlier calculations. The potential is bounded
at large fields for these signs. At fixed phi the exact minimum over S is

    S*(phi)=-g_phi phi^2/[2(M^2+h phi^2)],
    W(phi)=V0+a phi^2/2+lambda_v phi^4/4
               -g_phi^2 phi^4/[8(M^2+h phi^2)].

This establishes a microscopic origin for a reduced quartic term and a
stabilizing higher-order dependence. It is an exact potential minimization;
dropping S dynamics is valid only when its response is sufficiently fast.

### Exact coexistence, without relying on a truncated expansion

Let delta=g_phi-sqrt(2lambda_v)M>0. There are equal-energy phases at phi=0
and phi^2=x_c when

    x_c=M delta/[h sqrt(2lambda_v)],
    a_c=delta^2/(4h).

Writing x=phi^2, the exact potential at this point factorizes:

    W(x)-V0=lambda_v h x(x-x_c)^2/[4(M^2+h x)].

It is nonnegative, zero at the two phases, and positive between them. The
barrier's x coordinate is the unique positive root between0 and x_c of

    2h x^2+3M^2 x-M^2 x_c=0,
    x_bar=[-3M^2+sqrt(9M^4+8hM^2 x_c)]/(4h).

Thus the barrier is explicitly fixed once M,h,g_phi,lambda_v are specified.
The outside offset V0 has canceled. Varying these couplings changes the barrier
while preserving equal phase energies. Small positive phase splitting can
also be held fixed by adjusting a near a_c; near coexistence the minimum's
energy derivative with respect to a is x_c/2. Vacuum levels therefore do not
uniquely determine the barrier even in this explicit microscopic construction.

### Effective expansion and wall limitations

For h phi^2/M^2 much less than1,

    W=V0+a phi^2/2-b phi^4/4+d phi^6/6+O(phi^8),
    b=g_phi^2/(2M^2)-lambda_v,
    d=3g_phi^2 h/(4M^4).

For b,d>0 the truncated potential has coexistence

    a_c,6=3b^2/(16d),  x_c,6=3b/(4d),
    barrier height=b^3/(96d^2).

These approximate coexistence values must not replace the exact ones outside
the expansion regime. Integrating out a canonical S also changes the kinetic
term along its valley:

    Z_phi=1+[dS*/dphi]^2,
    dS*/dphi=-g_phi M^2 phi/(M^2+h phi^2)^2.

A canonical one-field wall formula additionally needs this derivative
correction small, or must include it. In the controlled canonical sextic
limit, the degenerate wall tension is

    Sigma approximately sqrt(d/3) x_c,6^2/4.

More generally the adiabatic-valley approximation involves
integral sqrt[2(W-V0) Z_phi] dphi. A truly heavy-field wall can require solving
the two-field profile. No uncomputed wall tension or bounce prefactor is
presented as an exact prediction of the full coupled theory.

## 2. Thermal feedback can regulate a rate temporarily

As a conditional thermal illustration, suppose a free-energy mass term acquires

    a(T)=a_base+kappa_T T^2,

with kappa_T>0. This coefficient would need calculation from the bath-field
couplings and state; it is not selected here. Coexistence occurs at
T_c^2=(a_c-a_base)/kappa_T if the right-hand side is positive. Near coexistence,
the false-minus-true free-energy difference is approximately

    Delta f(T)=(kappa_T x_c/2)(T_c^2-T^2).

This is a FREE-ENERGY difference, not automatically the latent energy. Its
corresponding internal-energy difference is

    Delta e=Delta f-T d(Delta f)/dT
           =(kappa_T x_c/2)(T_c^2+T^2).

Confusing these would incorrectly count the bath's energy budget. A full
finite-temperature model must include both phases' heat capacities and energy
exchange, not simply substitute Delta f into a vacuum energy reservoir.

For illustration, a thermal thin-wall bounce has exponent

    B_T=S3/T=16 pi Sigma^3/[3T Delta f(T)^2].

Keeping Sigma approximately fixed near coexistence,

    d ln B_T/dT=-1/T+4T/(T_c^2-T^2).

It is positive for T_c/sqrt(5)<T<T_c, so the exponential nucleation rate tends
to decrease as the bath heats near coexistence. Prefactor derivatives and
thermal wall corrections must also be checked in an actual model. This is a
possible thermostat sign, not a calculated bath history or universal rate.
It also does not determine the microscopic conversion of wall energy into
the soft radiation needed by the halo boundary.

## 3. Couple conversion, depletion and escape in one energy budget

Let F be the fraction of a fixed finite volume still in the convertible phase,
U the radiation energy density, D the approximately fixed available latent
energy per initially unconverted volume, eta the fraction entering that bath
(0<eta<=1), and tau_esc a finite positive escape time. Let R(F,U)>=0 denote
any conversion rate consistent with the microscopic model. Then a minimal
closed-reservoir balance is

    F_dot=-R(F,U),
    U_dot=eta D R(F,U)-U/tau_esc.

It obeys the exact identity

    d[U+eta D F]/dt=-U/tau_esc.

Including the untracked non-radiative conversion products gives the related
full-energy accounting

    d[U+D F]/dt=-U/tau_esc-(1-eta)D R.

These identities do not depend on the functional form of the rate or on its
feedback sign. At a joint stationary state, F_dot=0 requires R=0, and then
U_dot=0 requires U=0. Therefore a positive steady escaping bath is impossible
in this closed finite-reservoir model. Its time-integrated escaping energy
per volume satisfies

    integral_0^infinity U/tau_esc dt <= U(0)+eta D F(0).

This does not rule out a long-lived quasi-steady state with a sufficiently
large reservoir. It provides the budget that such a claim must demonstrate.
An equilibrium calculated while freezing F by hand is not an equilibrium of
the full system.

### Why a negative feedback sign is not enough

If the conversion rate decreases as U rises, the U equation at an artificially
held-fixed F can have a restoring thermal mode. In that restricted calculation
its derivative is eta D R_U-1/tau_esc<0 when R_U<0. But F continues to decrease,
so the regulated bath level moves or eventually disappears. A controller can
regulate expenditure; it cannot create an energy supply. The same conclusion
holds if latent energy and heat capacities vary with state, provided the full
energy is accounted for and no external source is added.

Cooling the material halo transfers its kinetic energy into radiation. It is
not free vacuum replenishment. For a genuinely stationary whole halo, material,
gravity, wall and phase energies must also remain stationary. Gravitational
contraction may provide finite power during evolution, but is not a stationary
energy source. The total balance remains

    dE_total/dt=P_external-L_escaping.

A constant cosmological vacuum has stress -V0 g^{mu nu} and no local transfer
source. Simply calling it a flowing medium does not give an advective energy
flux: a pure constant vacuum stress is Lorentz invariant. Gradients, moving
walls or additional material components can carry energy, but their dynamics
are separate physical inputs.

## 4. What would sustained supply require?

Add an explicit replenishment rate S_in of convertible material/phase volume:

    F_dot=S_in-R,
    U_dot=eta D R-U/tau_esc.

At a stationary state,

    R*=S_in,  U*=eta D tau_esc S_in,
    escaping power per volume=eta D S_in.

Now steady supply is possible in principle, but the normalization is fixed by
the external source S_in. The barrier determines whether conversion can keep
up, not a unique value of the supplied energy flux. Maintaining F physically
requires a process that imports higher-energy phase, regenerates it, or draws
on another reservoir. Regeneration costs energy; it cannot be counted as a
net gain from a closed cycle. No such influx or regeneration law has been
derived from baryonic mass and dark-energy density.

This directly affects the cooling requirement found previously. A maintained
soft bath and fixed boundary pressure can select local temperature and density,
but those external quantities must be supplied. The present barrier mechanism
does not set the bath's spectrum, source geometry or pressure, and it does not
prove capture, fluid closure or whole-halo stability.

## 5. The normalization remains open

The conditional transport relation is still

    v_flat^4=2G zeta L_a/c.

Obtaining a0=c sqrt(G rho_DE)/2 would require

    L_a/Mb=c^2 sqrt(G rho_DE)/(4zeta).

The heavy-field barrier does not establish this relation. In a supplied steady
bath, L_a is controlled by source power and spectral transfer; in a closed
reservoir it changes with depletion. V0 remains an independent offset in the
local phase potential. Setting a barrier or supply rate to fit the luminosity
would put the normalization in by hand. No1/2 is claimed from the ordinary
symmetry factors or equilibrium coefficients in these calculations.

## Evidence and scope

barrier_supply_checked.py passes18 exact checks covering heavy-field
elimination, coexistence/barrier structure, the controlled expansion, thermal
free versus latent energy, and reservoir/replenishment identities. The sign-
reversed depletion control fails the radiative-energy identity as intended.

The first run, barrier_supply.py, failed one verification because U and R were
strictly-positive SymPy symbols, excluding the zero state the test expected
the solver to return. A minimal reproduction confirmed that nonnegative
symbols admit that state. The corrected implementation changes that domain;
the original script, failed run and corrected evidence are all preserved.
This was a verification-domain bug, not a physical counterexample. All
manifests are validated, including both intentionally and unintentionally
failed records. Interpretation is self-reviewed, not independently audited.

Primary-source context: [Dimensional reduction of the Standard Model coupled
to a new singlet scalar field](https://arxiv.org/abs/1609.06230) studies
integrating out a heavy scalar in a different theory. Its abstract was checked
only for context. The explicit potential and identities here are derived
directly, with no claim that electroweak results validate a galactic model.

Disposition: barrier origin is constructed conditionally from a particle
interaction; thermal rate regulation is possible conditionally. A closed finite
vacuum reservoir cannot sustain nonzero stationary luminosity. A replenished
reservoir remains an open physical route, requiring a derived source and full
halo/phase/radiation evolution. Neither global halo stability nor the requested
coefficient has been achieved. No claim excludes every evolving or externally
powered pool theory.
