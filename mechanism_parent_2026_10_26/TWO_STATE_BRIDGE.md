# Source bridge to conversion; full dynamical matching remains open

The parent derivation assumed a conserved pure-component current to make its
local stability claim precise. The compression/conversion source itself extends
without a fitted rate. Introduce two effective currents J_T,J_F and phases
theta_T,theta_F in a constrained fluid action, with a conversion energy
V(n_T,n_F,theta_T-theta_F,carrier). Phase variation gives

    nabla.J_T = -V_delta = Gamma,
    nabla.J_F = +V_delta = -Gamma.

Total medium charge is conserved; Gamma must come from this specified energy,
not an independent reaction prescription. A complete V and carrier kinetic
action compatible with the existing complex-amplitude benchmark are still
required. This equation alone does not provide them.

Use the same tracking potential M^2(s-lambda n_T)^2/2 and interaction
h s J_T.partial chi, optionally retaining g1 J_T.partial chi. The exact scalar
source is

    S = g1 Gamma + h[s Gamma+J_T.partial s].

At leading low-frequency order s=lambda n_T, and with
J_T=n_T u_T and theta_u=nabla.u_T,

    J_T.partial n_T = n_T Gamma-n_T^2 theta_u,
    S = g1 Gamma + g2[2 n_T Gamma-n_T^2 theta_u].

This is precisely the compression/conversion combination in the prior CC
action, with consistent density units. The discarded kinetic companion also
contributes to the exact effective scalar equation through
nabla_mu[alpha (J_T.partial chi) J_T^mu]; it cannot be dropped in an evolution.
The parent version retains it through s dynamics.

The fluid n_T may represent a coarse-grained field charge rather than particles.
Its hydrodynamic closure, EOS and validity through n_T=0 must be derived. Phase
variables are singular at zero component amplitude; the existing regular
complex fields are needed for a genuine all-F birth calculation. Consequently
the positive pure-T homogeneous Hessian is not a proof of full two-state health.

Necessary matching conditions before a new galaxy run:
1. Derive the current and density normalization from the existing regular field
   action, retaining its quantum-gradient and finite-carrier terms.
2. Include every scalar, density, carrier and conversion derivative of the new
   parent, with a single total-energy/shift-charge ledger.
3. Recompute the static branch including finite-M density-gradient forces.
4. Test local cones across the occupied density/flow range, not one rest state.
5. Determine h,lambda,M from a stated microscopic or framework input. Writing
   g2=h lambda exposes parameters; it does not predict their values or kappa.

The vacuum-like dark-energy component has w approximately -rho and cannot be
silently identified with the positive-enthalpy fluid assumed in DERIVATION.md.
This bridge concerns the mobile cold component; how it exchanges with vacuum
energy remains an additional dynamical obligation.
