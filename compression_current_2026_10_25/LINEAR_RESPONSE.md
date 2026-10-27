# What the compression coupling adds, and what remains unclosed

This is an internal derivation for the proposed CC action, not an external
result or a derivation of the operator from the Zimmerman formula.

In ACTION.md the first `div` is a spacetime divergence: its time component is
q(rho)=g1 rho+g2 rho² and its spatial component is (g1+g2 rho) j_T.
It is not the spatial divergence alone.

Consider a locally uniform pure-T state of density rho0 with conversion off.
Write the physical velocity potential as sigma theta and absorb the constant
background spatial connection (g1+g2 rho0) chi into that potential. To quadratic
order the remaining one-form couples density perturbation d to chi_t with
G=g2 rho0. Eliminating the longitudinal material phase at a nonzero spatial
wavenumber k gives

    L2=I_k d_t²/2 - I_k Omega_k² d²/2 + G d chi_t
       +chi_t²/2 - c² k² chi²/2,
    I_k=1/(rho0 k²).

Omega_k denotes the uncoupled density mode, including whatever local response
is valid. With only a barotropic local energy and the Schrödinger gradient,
Omega_k²=c_T² k²+kappa k^4/4. The nonlocal gravitational/response energy is not
being replaced by this local expression in the simulations.

The coupled equations and exact dispersion relation are

    I_k(d_tt+Omega_k² d)=G chi_t,
    chi_tt+c² k² chi=-G d_t,
    omega^4-[Omega_k²+c²k²+g2² rho0³ k²]omega²
              +Omega_k² c²k²=0.

For Omega_k²>0 both squared frequencies are positive. For Omega_k << c k,

    omega_-² ~= Omega_k²/(1+eta_local),
    omega_+² ~= c² k² (1+eta_local),
    eta_local=g2² rho0³/c².

Thus stronger coupling both adds a fast branch and slows the material branch.
This positive energy coupling is not a friction term. Irreversible cooling
requires excitation of modes that actually propagate out, as opposed to the
reversible near field. The old slow-source bound therefore remains relevant.

There is also a completion issue: in this nonrelativistic truncation the
upper linear branch exceeds the bare scalar speed c for nonzero coupling.
That is not a theorem ruling out every completion of the hypothesis, but the
present action cannot be claimed to establish a causal relativistic model.
At large eta_local, treating the scalar as having an unchanged light cone is
particularly unjustified.

A relativistic kinetic completion would need to treat the material temporal
and spatial covariant derivatives together. The temporal counterpart of the
transformed spatial square has the structure

    kappa/(2c²) |phi_T,t + i(g2/sigma)
                         [rho chi_t+2chi rho_t]phi_T|².

At uniform background its chi_t² contribution is eta_local/2, alongside the
spatial coefficient c²(1+eta_local)/2. Keeping these terms consistently may
repair the principal cone, but this expression alone is NOT a complete
relativistic action: its cross terms, material time dynamics, Noether charge,
background and conversion sector all require derivation. It must not be
inserted as an ad hoc scalar inertia while claiming a completed model.

Three unresolved inputs are now separated: (1) origin and magnitude of g2,
(2) a consistent kinetic completion in the regime where eta_local matters,
and (3) demonstrated nonlinear population of escaping modes at a rate that
forms the galaxy. Static agreement fixes none of these three inputs.
