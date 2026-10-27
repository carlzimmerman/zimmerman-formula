# Two-electron dynamics and conservative rate interface

## Hamiltonian and units

Let X have charge+Q and mass M, and C have charge−Q and mass m. Assume C is a
spin1/2 fermion. In a_D=hbar/(mc alpha), E_D=mc²alpha² and t_D=hbar/E_D units,
alpha=Q²/(4pi epsilon hbar c), the isolated two-center/two-electron Hamiltonian is

 H = −sum_A nabla_A²/(2 rho) −sum_i nabla_i²/2
     +1/R +1/r12 −sum_Ai 1/r_Ai,    rho=M/m=100.

Remove center-of-mass motion; antisymmetrize electrons. The nonrelativistic
matter Hamiltonian has only rho as a dimensionless microscopic parameter.
Spin and nuclear exchange statistics are physical inputs, not tunable rates.
The computation here diagonalizes the electronic fixed-R part with full
configuration interaction in finite Gaussian bases. It is not a solution of
the full continuum/nuclear Hamiltonian.

The physical two-body coefficient has the scaling
 k_phys = (a_D³/t_D) khat(rho,T/E_D)
        = hbar²/(m² c alpha) khat.
A separate collision normalization is therefore unnecessary once the actual
scattering matrix is computed. The photon coefficients carry the additional
alpha³ factor in these atomic units. This scaling fixes units, NOT khat.

## What absolute finite rates require

An incoming channel includes T_b, projectile angular momentum and spin,
total angular momentum/parity, and flux normalization in the attractive
Coulomb field. Outgoing channels include two neutral atoms (with allowed
excitation), electron+ion rovibrational channels, neutral molecular resonances,
and any energetically open ion-pair channels. Unpolarized two-spin1/2 entrance
weights are singlet1/4 and triplet3/4; angular and molecular-state averages must
also be handled explicitly. No spin weighting has been fitted here.

For one normalized incoming partial-wave block with weight w, define
 P_b(E)=sum_d |S_db(E)|²,  0<=P_b<=1,
where d runs ONLY over specified dissociative final channels. In atomic units
 sigma_b(E)=w*pi*P_b(E)/(2 mu E),  mu=201/202 for C+T,
 khat_b(T)=w*sqrt(2pi)/(mu^(3/2) T^(3/2))
           * integral_0^infinity P_b(E) exp(−E/T) dE.
Weights and all contributing blocks must be summed for a physical rate.
P=1 gives sqrt(2pi)/(mu^(3/2)sqrt(T)) per unit-weight block, a unitarity
ceiling, not a physical recombination coefficient and not a ceiling on the
sum of arbitrarily many omitted angular momenta.

The implementation integrates tabulated P and reports an upper bound on the
missing low/high ENERGY tails assuming unitarity. It does not claim to bound
interpolation errors, missing partial waves or missing product branches.
Bound FCI eigenvalues alone do not give P. A scattering boundary, Coulomb
matching, electronic autoionization widths and nuclear channel couplings remain
necessary. Fixed-R bound states cannot be relabeled dissociative resonances.

## Why a plane-wave Born shortcut fails this applicability check

For an attractive unit charge, eta=mu/k=sqrt(mu/(2E)). A necessary weak-Coulomb
condition for a plane-wave Born treatment is eta<<1. At representative Maxwell
energy E=3T/2, all four initial environments at alpha=.2, m=10^7 eV have eta>3.9;
the colder environments are much farther from weak coupling. The exact
point-Coulomb continuum enhancement at the origin is
 2pi eta/[1−exp(−2pi eta)].
It diagnoses strong distortion; multiplying a guessed DR cross section by it
would NOT compute molecular exchange, resonances or the reaction probability.
No Born-derived physical rate is accepted from this test. This does not rule
out Coulomb-distorted Born methods with separately validated short-range physics.

## Coupling an actual rate to recycled photons

Keep the prior leading-BO network convention B_A=.5, mu_A=1,
mu_AX=100*101/201 and T_b energy −(.5+D_b). Let a and t_b be number fractions
per initial X/C pair, x=1−a−2sum(t_b), c=1−a−sum(t_b).
For direct DR T_b+C <-> A+A, the net event rate per pair per age is
 R_b=age*N*k_b(T) [t_b*c − q_b(T)*a²],
 q_b=g_b*(mu_A/mu_AX)^(3/2)*exp[−(.5−D_b)/T].
The inverse convention is event coefficient times n_A²; no additional factor
1/2 is introduced. A physical scattering calculation must use this event
convention or convert its indistinguishable-particle counting explicitly.
Detailed balance fixes q_b once k_b is known; it never fixes k_b.

Add da=2sum R, dt_b=−R_b, dK=sum(.5−D_b)R_b to the existing photon equations.
Then dx=0, dc=−sum R, d[x+sum t−c]=0. The change in
 K−.5a−sum(.5+D_b)t_b+sum omega*y_gamma+E_escaped
is identically zero. No photon is emitted or removed directly by this
nonradiative reaction. Its changed species/temperature affect the existing
photon emission, absorption, stimulated capture and escape. The photon-mediated
T+C ->2A cycle remains distinct and is not removed or counted as this rate.

The adapter has NO default coefficient. A manufactured unit-loss fixture is
used only for integration/Jacobian/conservation tests. No fixture result is
reported as a disk/dwarf/cluster prediction.

## Remaining consistency and closure requirements

The existing model's thermochemical conventions are leading BO. With fully
consistent finite masses, the translational factor for this reaction is
(m_T*m_C/m_A²)^(3/2)=(201/10201)^(3/2), rather than (201/10100)^(3/2),
and atomic binding is 100/202 rather than1/2; molecular diagonal BO/recoil
corrections must also be recomputed. The adapter preserves the existing
conventions so conservation and detailed balance can be audited against the
same network; its output is not a precision finite-mass prediction.

FCI finds additional bound neutral X2C2 and negative XC2 electronic channels.
Their existence does not give their populations or formation probabilities.
They require their own species, energy, charge and photon branches before the
full chemistry is closed. In particular, retaining negative ions changes the
free-countercharge relation. The current adapter implements only the DR branch
into two ground-state atoms. Excited products require separate branch energies.
No finite DR, impact ionization, dissociation, three-body or state-transfer rates
have yet been calculated. No new physical halo trajectories are claimed.
