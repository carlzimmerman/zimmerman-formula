# Quantum events and field-action bookkeeping

For species/cell a use occupation f_a, number measure w_a, statistic eta_a=+1
for bosons and−1 for fermions, and availability A_a=1+eta_a f_a. For a
projected reaction r let nu_ar be its signed fractional stoichiometry, with
parent coefficient−1 and daughter interpolation weights each summing to1.
An energy-linear daughter map obeys sum_a nu_ar E_a=0 at the background x.

Geometric interpolation of f and A gives forward and reverse products F_r,R_r
such that

    log(F_r/R_r) = sum_a nu_ar log(A_a/f_a).

The quantum collision flux is J_r=k_r(F_r−R_r), k_r>=0, and
w_a df_a/dtau=sum_r nu_ar J_r. It follows algebraically that collision energy
and every linear stoichiometric invariant are conserved. For interior
occupations, the comoving quantum entropy satisfies

    dS/dtau = sum_r k_r(F_r−R_r) log(F_r/R_r) >=0.

FD/BE populations with common T have log(f/A)=−(E−mu)/T; detailed balance
therefore follows from the same energy identity and sum nu mu=0. Positivity
and the fermion upper bound are a property of the realized time integrator,
not an inference from this entropy identity alone. Fractional geometric
projection near zero occupations need not have the continuum's regularity;
momentum/time refinement remains necessary.

At a fixed background with only F->C+lambda and its inverse, both N_F+N_C
and N_F+sum N_lambda are conserved. If the reversed mass ordering is also
visited, C->F+lambda introduces a different emission reaction and removes
the latter invariant. Orbit-driven repeated emission draws energy from the
field and particle distributions; it is not free particle multiplication.

For a common coupled field action and all populations, let U=V+sum w_a f_a E_a
(with physical measures including a_FRW^-3) and normalized scalar action
J=(1/(2pi)) integral p_x dx. Its averaged collision contribution is

    Jdot_coll = Torbit/(2pi) sum_a w_a
                    [<E_a C_a>−<E_a><C_a>].

If all daughter populations are retained and every phase's collision operator
conserves energy, sum_a w_a E_a C_a=0 pointwise. The first averaged term then
vanishes after summing species, but the second generally does not. Expansion
adds−3HJ. This supplies an independent integration check: tracking the full
particle energy cannot be replaced by a photon ledger, and even an
energy-conserving collision network can change collective oscillation action.

These identities validate the declared finite quantum projection. They do
not prove that phase averaging is justified for every soft mode or that the
projected finite operator is the complete microscopic quantum collision action.
