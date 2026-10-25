# A scoped reciprocal coupling without counting cold mass twice

This is a NEW nonrelativistic two-potential candidate, not v3/v3s, not a derived covariant completion, and not a four-dwarf solution. Its selective coupling is a postulate. It exhibits what an explicit action can do; it does not establish that nature uses it.

Let rho_c=|psi|^2. With live baryonic kinetic Lagrangian L_b, introduce a Newtonian potential Phi and a baryon-sourced extra potential Xi:

    L = L_b + (i eta/2)(psi* psi_t - psi psi*_t)
        - eta^2 |grad psi|^2/2 - (rho_b+rho_c) Phi - rho_b Xi
        - |grad Phi|^2/(8 pi G) - a0^2 F(z)/(8 pi G),
    z=|grad Xi|^2/a0^2, u=sqrt(z), 0<=u<1,
    F(z)=-u^2-2u-2 ln(1-u).

Variations give

    lap Phi=4 pi G(rho_b+rho_c),
    div[ u/(1-u) grad Xi ]=4 pi G rho_b,
    i eta psi_t=-eta^2 lap psi/2 + Phi psi.

Baryons feel -grad(Phi+Xi); the cold field feels -grad Phi. The cold field is therefore neutral under Xi by hypothesis, not a universal single-metric matter sector. Newtonian baryon/cold interactions are reciprocal through the common Phi; the extra Xi interactions are between baryons. Cold inventory enters Phi once. It is not an extra Xi charge and must not also be added a second time as an independent Newtonian correction after solving Phi. For appropriate fixed boundaries this is a variational Newtonian system; the Xi field/source terms and baryonic work belong in its full energy ledger.

In spherical symmetry without cold mass, y=g_N,b/a0 = u^2/(1-u). Total baryonic acceleration is x=g_b/a0=y+u=u/(1-u), hence

    x^2/(1+x)=y.

Thus the same rational spherical baryon-only law is recovered. With cold mass,

    g_b = g_law(rho_b) + g_N,c,

in spherical symmetry. This split is derived here from a stated non-universal action, rather than assumed as a force addition. It does not match an unchanged cold-sourced AQUAL equation, and it does not inherit the old disk/SPARC fits in nonspherical geometry. For u>0, F'(z)=u/(1-u)>0 and the static radial coefficient F'+u dF'/du=u(2-u)/(1-u)^2>0; degeneracy at u=0 remains. No relativistic time-dependent health or equivalence-principle test is established. The MOND-like isolated logarithmic potential also needs explicit outer boundary/cosmological matching; do not infer finite isolated energy at infinity from this static action.

The envelope simulations in this directory are the rho_b=0, Xi=0 limit of this candidate, so their failed storage/retention tests remain applicable to that limit. They are not runs with a baryonic potential or live stars. In particular:

* Poisson counts cold mass once, but that mass STILL boosts stellar gravity. No bookkeeping trick suppresses the real central cold mass in Fornax/Leo I.
* Universal eta and homologous profiles still fail the older four-dwarf ordering test in homology_result.json.
* eta, the cold inventory and the selective Xi charge are not derived from Lambda. A new potential and non-universal coupling are substantive changes.
* Preserving the old law in spheres is not preserving all its tests or explaining a0. A covariant parent, cosmological history, composition tests, stellar heating and nonhomologous assembly remain open.

One physically distinct possible source of nonhomology is time-dependent baryonic structure. In the cold wave equation an externally prescribed Phi_b supplies work

    dE_c/dt |_external = integral rho_c partial_t Phi_b d^3x.

Rapid gas removal and slower return can redistribute collisionless energy; this is demonstrated for particle halos by Pontzen & Governato (2012), https://arxiv.org/abs/1106.0499. Transferring that result to this coherent field requires computing its own response and stellar heating. It is a candidate continuation, not a simulation result here, and gas histories/energy budgets must be constrained before trying it. Tuning four arbitrary potential pulses would not predict the dwarfs.
