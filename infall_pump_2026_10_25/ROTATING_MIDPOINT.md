# A numerical phase frame, not an added physical force

The old canonical T phase contains a large density-dependent scalar phase.
Physical alignment and currents can remain slow while this coordinate winds
rapidly. Ordinary arithmetic complex midpoints then underestimate midpoint
density by cos^2(delta phase/2), even when endpoint density is unchanged.

Freeze a real diagonal reference frequency Omega for an entire macrostep and
write a(t)=exp(-i Omega t)b(t). The EXACT transformed Hamiltonian is

 H_b(t)=H(exp(-i Omega t)b,alpha,p,chi,pi)-sigma sum Omega |b|^2.

No density, scalar or carrier force is dropped. For a substep h define

 a_mid=[exp(-i Omega h/2)a0+exp(+i Omega h/2)a1]/2,

 exp(+i Omega h/2)a1-exp(-i Omega h/2)a0
       +i h[H_a(a_mid)-sigma Omega a_mid]/sigma=0.

Every original force and source uses THIS physical midpoint. The scalar and
carrier are jointly solved as before. The reference term is real diagonal,
so the exact material norm-increment identity is unchanged. The same endpoint
density secant therefore preserves the original quartic shift-charge ledger.
Constant-frequency phase rotation is represented exactly, including its
constant density; this is not supplied mode energy.

For fixed Omega this map is self-adjoint: exchanging endpoints and h->-h
changes only the sign of the residual, and leaves a_mid unchanged. It is
second order for the SAME continuous equations. Keep the SAME Omega through
all3 symmetric composition substeps to obtain the fourth-order composition.
Choosing a new Omega at each internal substep would invalidate that argument.
The macrostep can choose Omega from its starting full Hamiltonian phase rate;
the transformed differential equation is exact for any such fixed reference.

Reference selection near vacuum is only a numerical coordinate choice. It is
never a density gate in the physical action. Mass, shift charge, full physical
energy, root residuals and fine-step comparison remain mandatory. Successful
phase removal would address a solver bottleneck, not prove galaxy formation.
