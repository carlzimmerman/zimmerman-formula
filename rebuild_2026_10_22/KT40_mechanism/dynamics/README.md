# Mechanism and dynamical scope

The Hessian response behaves locally like an anisotropic contribution to
matter compressibility. It is not automatically stabilizing or destabilizing:

    delta Phi_hat=[K(n)+N(n)k²] delta psi_hat,
    omega²=[c_s²-4piG rho0 N(n)]k²-4piG rho0 K(n).

Negative N increases short-wave restoring pressure in this fluid closure.
Positive N reduces it and gives unbounded high-k growth when pressure is
insufficient. The full action fixes both signs; the mixed derivative terms
cancel exactly. [Full derivation](DERIVATION.md)

A general analytic result limits the whole local curvature-quenching route:
if E(g0,h nn) is C², tends to a finite high-curvature limit and lies above
that limit somewhere, its second derivative is positive somewhere. That
jet has positive matter density and a pressureless growing high-k branch.
The result applies to every positive KT39 power at nonzero-H jets. It is
conditional on the local instantaneous field law and cold-fluid closure;
it does not exclude finite-pressure, collisionless, nonlocal or dynamical
field completions. [Exact theorem and scope](GENERAL_OBSTRUCTION.md)

The original MW witnesses illustrate why the matter closure matters. In an
independent audit of the root's stored fields, the isotropic barotropic
two-gas completion has stable leading high-k response in **every direction**
at the 14 restoring-force sample points on each footing. The largest
rank-one instability parameters are 0.762123 and 0.762721, below one.
At the fifteenth point, R=12 kpc,z=.3 kpc, the stored physical potential
gradient points outward; the fixed decreasing gas profiles would require
negative dP/d rho for hydrostatic balance. That is a distinct equilibrium
obstruction. The root's separate potential-difference/refinement test checks
the force sign itself. This lane does not claim actual-MW ultraviolet growth.
[Independent 90-row audit](hydro_audit_001/results.json)

Separately, the fixed-uniform-field Plummer virial sign and normalization
were independently rederived. The original 1,312 nonzero-external-field
configurations have negative total W on all three grids. Such W cannot
support stationary positive kinetic energy for the fixed mass/tracer shape,
but actual satellite environments and nonuniform tides require additional
mapping. [Independent EFE review](EFE_REVIEW.md)

The successful tensor experiment checks 432 deterministic jets and four
sinusoidal second-energy variations. Two failed finite-difference controls
are retained: small mixed contractions were poorly conditioned in ordinary
centered differences. The accepted version uses Richardson differences
without changing the physical law or the tensor-normalized 2e-6 gate.
All four manifests, including both failures, validate; VERIFICATION.json
records their status and the current source hashes.
