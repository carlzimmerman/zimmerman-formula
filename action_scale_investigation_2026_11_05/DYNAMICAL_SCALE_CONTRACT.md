# Dynamical promotion: attraction versus freezing

Freeze before computation. This extends DERIVATION.md's auxiliary-scale
test to a canonical dynamical scalar chi. It is a structural audit, not
a new numerical coefficient candidate or a campaign reopen.

Add -g^{mu nu} partial_mu chi partial_nu chi/2 to the single-clock candidate.
Take V(phi)=V0>0 and a(chi,phi,X)=a_ref(phi,X) exp(chi/f), f>0,
a_ref>0. The source-clock phi, metric, polarization and stiffness definitions
remain fixed when varying chi. No new chi potential or chi-dependent
stiffness is included. The exponential is a convenient strictly monotone
positive chart, not a prediction for a scale. Constant shifts are not a
symmetry of the full polarized action.

1. Derive the exact homogeneous P=0 solution with both scalar kinetic
energies in Friedmann. Let A be the FRW scale factor, Q_phi=A^3 phi_dot,
Q_chi=A^3 chi_dot, C=Q_phi^2+Q_chi^2>0, Q_phi nonzero so the clock is
timelike at every finite A. Verify that chi_infinity-chi_initial is
sqrt(2/3) M Q_chi/sqrt(C) asinh(sqrt(C/(2V0))/A_initial^3).
Show explicitly that chi_initial is a freely retained offset. Do not infer
that the limiting X_phi=0 configuration has a defined normalized clock.
2. At fixed p in0<p<a derive W_chi and its sign using the actual W kernel.
Use the scalar Euler-Lagrange equation on an arbitrary static positive-lapse
domain to derive its weighted boundary-flux identity. Determine whether a
regular time-independent chi can coexist with nonzero polarization and
zero total boundary flux. Boundary fluxes, horizon singularities, extra
potentials and nonmonotone scale functions are explicit exclusions.
3. Explain why a new potential can balance the force but does not derive
its extremum or response coefficient without independent physical input.

Exact symbolic checks: kernel derivative, chain rule, positive derivative
of the sign function, FRW Friedmann reduction, late-time integral primitive,
constant momentum, and sensitivity to the initial offset. Mutation drops
the initial offset in the purported late-time solution and must fail the
initial-value derivative check and its operational-scale sensitivity check.
No numerical fixtures are needed for these
elementary exact identities. Self-review, no full-health or universal no-go.
