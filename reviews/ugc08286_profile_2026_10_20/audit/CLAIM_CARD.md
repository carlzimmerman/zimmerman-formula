# Independent finite audit target

Authoritative statement: `../TARGET.md`, frozen source code `../invert.py`,
`../baseline.py`, `../kernel/disk_kernel.py`; observed geometry and calibration
scope in `../data/GEOMETRY.md` and `../stellar/CONSTRAINTS.md`.

The tested objects are 17 target radii, signed Newtonian gas contributions,
fixed inherited simple-law acceleration scales, and finitely many constant
surface-density annuli with a normalized exponential vertical distribution.
Nonnegative annular masses are inverse variables. A positive density may give
an outward contribution at an interior target radius.

For additive extra mass the exact finite model is
`Vlo_i^2 - Vbase_i^2 <= sum_j K_ij m_j <= Vhi_i^2 - Vbase_i^2`, with
`m_j >= 0`. The simple-law baseline has fixed published stellar M/L 0.5.
For stellar-only reconstruction define
`F_R(w)=w^2/(w+a0*R*kpc_m/1e6)`. Monotonicity on nonnegative `w` makes the
exact finite constraints
`F_R(Vlo_i^2)-gas_i <= sum_j B_ij U_j <= F_R(Vhi_i^2)-gas_i`,
`0 <= U_j <= u`, minimizing `u`. Here `B_ij=K_ij L_j` and light is flattened
to its annular average before forward calculation. Distance alternatives use
homology, so target R, h and edges scale by lambda, L by lambda^2, B and gas
V^2 by lambda. This is distinct from reapplying the empirical height rule.

No intrinsic radial M/L bounds or full intrinsic 65-point light profile have
been recovered. The supplied 65-point profile is projected. Calibration boxes
are declared old-star Chabrier sensitivity choices. The implemented ceiling
family [0,Ucap] enlarges either positive-lower-bound calibration box. Its
infeasibility excludes that smaller family only conditionally on the stated
old-star/total-light ordering, geometry, extinction and support bridge.

Audit verdict sought: finite numerical assertions only, conditional on the
adopted interpolation, support, source binning, geometry, errors, solver and
quadrature. No unique density, detection, smooth gradient, universal feasibility,
statistical significance, coupled nonlinear field, or lifetime is certified.
Two quadrature orders supply a discrepancy, not an a priori error bound.

Independent reviewer receives raw code and definitions, with no author verdict.
Small single-thread controls are authorized by TARGET.md and delegated scope.
