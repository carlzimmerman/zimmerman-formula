# Conservative nonlinear inertia completes the compression triad

The earlier NC2 bare-density vertex is correct for the bare pure-T static
Hamiltonian. Adding only a scalar radiation/reaction term does not make that
vertex the full CC cubic interaction. At high k the bare gradient terms
cancel. Corrections small compared with a mode frequency can dominate the
small residual vertex. The original run_triad therefore tests a specified
truncated network, not a controlled ultraviolet CC cascade.

Here derive the missing term directly, without a new coupling or static gate.
Use physical velocity potential phi after removing g1 and drop scalar chi_tt
only in its near field. The full spatial square is retained. At fixed density
rho and rate rho_t, the longitudinal phase and scalar have the quadratic
stationary Lagrangian

 L=integral [rho_t phi-2g2 rho rho_t chi
       -rho |grad phi-g2 rho grad chi|²/2-c²|grad chi|²/2]dV - U[rho].

For nonzero spatial Fourier components and rho=rho0+n its exact quadratic
elimination has effective density kinetic energy

 L2= (1+eta)/(2rho0 k²)|n_t|²-U2,
 eta=g2² rho0³/c².

This gives Omega_k=omega_bare,k/sqrt(1+eta). The derivative-current canonical
spatial square is crucial to this result. Its normal-mode density amplitude
is A=sqrt(rho0 k²/[2Omega(1+eta)]), not the bare amplitude.

Through cubic order the positive near-field added action is

 L_added= (1/(2c²))integral S(-Delta)^-1 S dV,
 S1=g2 rho0 n_t,
 S2_k=g2 sum_(p+q=k)[2-k.q/q²]n_p n_t,q.

The physical continuity equation fixes the longitudinal velocity to first
order v1,k=i k n_t,k/(rho0 k²). A transverse velocity first arises at second
order; its inner product with the first-order longitudinal velocity vanishes
in the constant-density quadratic kinetic metric, so it does not alter this
cubic action. The full nonlinear field theory, or quartic order, cannot discard
that velocity. Zero spatial modes require the retarded outgoing field; they
first contribute to the conservative density action at quartic order here.

The fluid density kinetic action has cubic term -integral n|v1|²/2. At fixed
canonical density momentum, the cubic Hamiltonian is minus the cubic kinetic
Lagrangian plus the original cubic potential. Thus the bare velocity vertex
uses B=Omega A/(rho0 k²). For a triad m=(k1,k2,-k3), signs s=(1,1,-1), k3=k1+k2,
the additional conservative Hamiltonian vertex is

 V_added=(eta A1 A2 A3/rho0² sqrt(volume))
  sum_(i,j,l permutations) s_i s_l Omega_i Omega_l
                  [2+m_i.m_l/|m_l|²]/|m_i|².

The quantum-pressure and nonlocal W tensor terms remain the earlier ones,
with the new A. No bare term may be omitted merely because eta is small.

In particular for transverse equal parents in the high-k quantum limit, the
combined vertex relative to q²/(2A sqrt(volume)) is

 V_total / [q²/(2A sqrt(volume))] -> -3eta/(1+eta)².

At fixed weak density perturbation amplitude its coupling rate scales as
eta/(1+eta)^(3/2); this is largest at eta=2. The statement is local, leading
quasi-static and cubic, not a universal optimum of full galaxy formation.
It removes the false inference that the bare short-wave cancellation alone
rules out CC transfer. It still does not supply actual infall occupations,
a microscopic g2, or a converged global formation trajectory.

Audit this formula by an independent stationary elimination of the original
quadratic phi/chi action at variable rho, followed by a mixed third derivative.
That check must include the Legendre sign at fixed density momentum. Keeping
only on-shell frequency matching is insufficient.
