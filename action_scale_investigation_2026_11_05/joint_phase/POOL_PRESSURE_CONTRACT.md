# Pool speed selection by pressure confinement and marginal collapse

User request: determine the pool speed from baryonic mass and dark-energy
density without inserting1/2. Base:50b4fe4e74. Changed construction: finite
pressure-confined isothermal equilibrium and its first mass maximum at
fixed sound speed and external pressure. This is not a rerun of the retired
cluster/dwarf turnaround-retention fits in V3S_FINAL_VERDICT_2026-10-24.md.

Use SI symbols for interpretation. Newtonian equilibrium has P=c_s^2 rho,
mass M_p of the pool, and independently specified P_ext>0. The regular
isothermal equation is (x^2 psi')'=x^2 exp(-psi). For a boundary x_b define

    mu(x_b)=x_b^2 psi'(x_b) exp[-psi(x_b)/2]/sqrt(4pi),
    M_p=mu c_s^4/(G^(3/2) sqrt(P_ext)).

Calculate the first mass maximum using the derivative of mu, not an
inserted critical radius or coefficient. Check the resulting density
contrast and edge circular speed. Distinguish the ideal asymptotic flat
speed from the finite sphere's edge speed. The mass in these equations
is M_p; do not silently identify it with baryonic M_b.

Compute the local interface stress condition for a pool in the SAME
vacuum on both sides and for different vacuum phases. Negative vacuum
pressure is not a positive external gas pressure. Retain a possible wall
tension and vacuum-energy difference explicitly; do not equate the phase
difference with the cosmological vacuum density by fiat.

Independent check: derive the similarity scaling of a cold isothermal
pool subject only to M_b, G and rho_DE and a turnaround condition. This
tests whether cosmic acceleration alone selects the required mass power;
no cluster/dwarf data or previously rejected parameter scans are used.

Execution: exact symbolic derivative identities plus two independent
float64 ODE integrations, tolerances1e-9 and1e-11, first critical root in
0.01<x<12 found from a sign change. Start at x=1e-5 with regular series
through x^6. Require root and dimensionless mass agreement below1e-6
relative and the critical edge-acceleration identity below1e-7 relative.
Store the dimensionless profile and boundary speed variation; no empirical
inputs, coefficient scans or target-based boundary conditions.60 seconds,
one thread. Negative control drops the derivative of the surface-density
factor from d mu/dx; the symbolic derivative identity must fail.

Scope: the first mass extremum is a marginal equilibrium criterion, not
a proved cosmological attractor. A finite sphere is not automatically a
stable galaxy with an extended flat curve. Neither its mass inventory nor
the confining pressure is fixed until separately derived.
