# Nonlinear heat estimate obtained; startup bootstrap remains open

**The requested common interval is not established.** This phase closes
specific nonlinear heat commutators and the heat-dependent time-weight
derivative for an actual first energy, under its explicit provisional
prefix envelope. The coupled density-gradient, local/collar and pointwise
bootstrap estimates needed for the full seeding theorem remain open.
The law and all physical coefficients are unchanged.

## Actual nonlinear first-energy estimate

On a material prefix starting from exact activation, assume
2<x=-theta<=8 throughout its history. Set

\[
 z=\log\rho,\quad f=S-S_d,\quad q=\psi-\psi_d,\quad
 \psi=KW^{3/2},\quad \nu=\tfrac12\rho Wh(1+K/(K+.01)).
\]

Here S is the full actual stress, and the homogeneous functions S_d,psi_d
are references, not replacements for the vacuum-boundary solution. With
the explicit material cutoff phi=chi^2 covering the central quarter,

\[
 E_\phi=\frac12\sum_i\frac{V_i\phi_i f_i^2}{\nu_i}
      +\frac12\sum_i\frac{dm\,\phi_i q_i^2}{W_i^{1/2}}.
\]

For 0<s<=1e-6, the exact finite-edge law gives

\[
 \boxed{E_\phi'\le-\tfrac18D_\phi(f)-\tfrac1{16}H_\phi(q)
 +4.2\,10^{21}s^6D_\phi(z)
 +9K_\chi(f)+5.2\,10^5s^4K_\chi(q)+\mathcal R_\phi.}
\]

D is the mechanical graph gradient square and H the actual heat gradient
square. K_chi is explicit cutoff work, bounded by
17000 times the corresponding volume-weighted square on the collar.
The remaining local work R_phi is given exactly in (H34)-(H35) of
[heat_absorption.md](heat_absorption.md).

This controls the actual nonlinear heat coefficient differences without
assuming a spatial compression-gradient bound. It also includes the
otherwise dangerous nu_K H weight derivative: its shared-flux coefficient
is alpha f-beta f^2/2. The other weight derivatives are nonpositive on the
stated branch. Neither a heat-divergence norm nor a heat Jacobian is assumed.
The constants, cutoff and absorption time are uniform in N, but the prefix
envelope itself is still a hypothesis. The time 1e-6 is not a proved common
bootstrap interval.

## Why this does not yet close the theorem

[viscous_energy.md](viscous_energy.md) gives an exact nonlinear estimate
propagating s^3 D(log rho) from dissipation of the **old** stress
q_old=kappa(x-2). The first energy above instead dissipates the **total**
stress. Substituting one dissipation for the other leaves a mechanical
gradient of K from pressure and memory. That gradient can exist where
the heat gate is closed.

Adding a plain D(K) or D(psi) energy does not automatically repair the
gap: the note constructs exact admissible states where their heat work
is positive. These are counterexamples to proposed dissipativity steps,
not to the specified cold-collapse trajectory. The heat-only TV(K)
contraction is valid, but supplies no missing mechanical square norm.

The [coupled-gradient route](coupled_gradient.md) tests whether a more
general state-dependent gradient energy can supply this control. Its
scope and any obstruction must be kept separate from a counterexample
to startup itself. Independent review of the phase is in
[INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md).

## Boundary and geometry progress

[bootstrap.md](bootstrap.md) replaces a global absolute-compression
assumption for the scalar boundary barrier by an upper density cap on
the inner three quarters. Exact energy then controls the required
geometry. Positive cut stress needs no amplitude bound. The cap and
the cut condition have not been established for the actual common interval.

[adverse_trace.md](adverse_trace.md) gives a further exact bound for
negative cut stress. Under only x<=U on a cell from activation,

\[
 \int_0^T s^{-p}S_-(s)\,ds
 \le\frac{6U^3e^{2UT}}{3-p}T^{3-p},\qquad0\le p<3,
\]

and integral_0^T S_-/nu_d <=U^3 exp(2UT)T/4. This needs no lower
compression bound or upper K bound. It gives time-integrated boundary
control, not the pointwise boundary-transfer estimate needed to finish.

No common T, (UC), or unconditional all-time floor follows from the
current conjunction. Exact energy conservation and quiet-gate inactivity
remain unchanged. [STATUS.md](STATUS.md) states the missing implication;
[PROVENANCE.md](PROVENANCE.md) records sources, checks and review scopes.
