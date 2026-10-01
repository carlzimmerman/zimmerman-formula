# Constructive continuation: a conserved-fluid realization of the conditional EOS

This supplies a local matter action for the conditional equilibrium equation of state. It does not derive the host-dependent state, the boundary, the cold abundance or a joint observationally viable theory. Those distinctions matter: conservation can be built explicitly even though formation selection is still missing.

Use c=1 in the action and metric signature (-,+,+,+). Let J^mu be a timelike mass current, rho=sqrt(-g_mu_nu J^mu J^nu), u^mu=J^mu/rho, and s an advected material label. Consider

    S_d = integral sqrt(-g) [-epsilon(rho,s)
                            + J^mu(partial_mu theta + beta partial_mu s)] d^4x.

Varying theta gives nabla_mu J^mu=0, and varying beta gives J^mu partial_mu s=0. Varying the current gives partial_mu theta+beta partial_mu s=-epsilon_rho u_mu. Hence the on-shell Lagrangian is P=rho epsilon_rho-epsilon. Metric variation gives

    T_mu_nu = (epsilon+P) u_mu u_nu + P g_mu_nu.

Together with the matter equations, diffeomorphism invariance supplies stress conservation. Coupling this matter sector to the Einstein action and baryons is a concrete conserved-fluid construction, rather than a prescription that creates extra halo mass whenever a gate switches on. The displayed one-pair material-label representation is sufficient for the spherical irrotational equilibria under discussion; a general vortical fluid can require additional labels. The construction does not identify this matter with the framework's original complex field.

For any positive material function V(s), put Pc=a0²/(8 pi G), C(s)=Pc/V(s), q=rho/C(s), and

    y(q) = [q²+q sqrt(q²+4)]/2,
    F(y) = sqrt(1+y) + log[(sqrt(1+y)-1)/(sqrt(1+y)+1)],
    epsilon(rho,s) = rho [1 + V(s) F(y) + e0(s)].

Here V and e0 are specific energies in units c=1; restoring SI replaces the rest-energy term 1 by c². Direct differentiation gives

    rho epsilon_rho-epsilon = Pc y,
    dP/d rho at fixed s = V(s) (1+y)^(3/2)/(1+y/2) > 0.

The desired point-baryon P2 equilibrium requires the *additional relation*

    V(s_host) = sqrt(G M_b a0)/2.

The equations above conserve and advect s; they do not select that relation or reset it consistently after a merger. Imposing it separately for each host is supplied initial/formation data, not a derivation or an eliminated parameter. The freely specifiable e0(s) cancels from Newtonian pressure but changes the relativistic energy and enthalpy, so it cannot be ignored in a cosmological or perturbative audit.

For an isentropic perturbation the candidate relativistic speed would be

    c_s²/c² = (dP/d rho)/(d epsilon/d rho)

with consistent energy-density units. A positive numerator alone is insufficient: enthalpy, energy conditions and the upper causal bound also need checking on the physical domain. In particular F(y) tends to minus infinity logarithmically as rho tends to zero; no finite e0 makes this unshifted formula a healthy all-density relativistic EOS. A selected finite-density domain and a justified vacuum/boundary completion are required. No global stability or causality claim follows from this construction.

Adding a constant energy density Pe(s) changes P to Pc y-Pe while retaining the hydrostatic pressure gradient within a uniform-s host. This realizes the algebra behind the finite-edge pressure subtraction, but also adds an actual vacuum-like stress term. Its domain, interface matching and exterior value must be varied consistently. It is not a pressure gauge and does not select Pe or the edge.

The useful result is therefore exact and limited: the conditional EOS admits a conserved local matter-action realization, and this exposes rather than conceals the remaining material-state, energy-zero and boundary-selection functions. A next action-level proposal must determine those functions and their formation statistics from the permitted inputs, then pass the existing observational gates.
