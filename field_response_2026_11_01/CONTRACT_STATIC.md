# Frozen static baryonic-response discriminator

Written before implementing or executing the new response solver. This file
owns the static finite assertion only; the root execution contract pins its
hash and the input snapshots before any scientific execution.

Use the PN28 finite-gradient spherical canonical-waterbag parent at fixed
`B,k,C_s`, hence fixed `rho_star,ell,epsilon`, adding only an externally
prescribed smooth Plummer baryon potential. Import the immutable source
snapshot `inputs/check_gradient.py`; the six native baselines have
`psi_c={0.8,0.95,0.99}` crossed with `epsilon={0.0001,0.01}`. Reconstruct
each baseline with its original solver, then freeze its dark mass M and
matter radius R as the response reference.

In the original dimensionless units, set

    phi_b=-mb/sqrt(r^2+a^2),
    n_b=3mb a^2/(r^2+a^2)^(5/2),
    m_b(r)=mb r^3/(r^2+a^2)^(3/2),
    n=psi_+^(3/2) exp(3s),
    Delta psi=-n-n_b,
    epsilon Delta s=exp(3s)(1-psi_+^(5/2))-1.

Two explicitly diagnostic, uncalibrated forcing families:

| Family | final mb/M | a/R |
|---|---:|---:|
| weak_diffuse (dwarf-like label only) | 0.05 | 0.5 |
| strong_compact (spiral-like label only) | 0.20 | 0.1 |

For each family retain all five continuation fractions `0,.25,.5,.75,1`.
The scale a always uses the unforced R. Fractions multiply mb only. The
unknown central psi is free after forcing; replace its Dirichlet condition
with `-L^2 psi'(L)=M+m_b(L)`. Keep both regular central derivatives zero
and the scalar outer Robin condition. Do not enforce `psi_c<1`, impose a
desired column, alter B, select a different waterbag level, or fit a response.

Main solve: original outer L, `tol=1e-6`, analytic Jacobian, at most 20,000
nodes. Every converged solution is assessed with independent quadrature
mass and scalar-integral checks, finite-difference total anisotropic stress
balance, self-gravity potential/force energy equivalence, full virial with
external Plummer virial (not external potential energy), and matter-edge
checks. Gate levels: mass/energy/scalar/virial `2e-5`, finite-difference
stress `5e-4`, boundary residual `1e-8`, outer scalar amplitude `1e-6`.
The zero-forcing solution must reproduce baseline radius, central density
and quarter-density column to relative `5e-5`.
Analytic Plummer controls independently finite-difference its potential
Laplacian at r/a=.1,1,3 and integrate its source, with relative `2e-6`
gates. At each forced solution compare enclosed gravity minus independently
integrated dark mass to positive enclosed baryon mass; the deliberately
opposite source sign must fail that same balance. The latter is a negative
control on the measured balance, not an additional physical solution.

Record `n_c,R,r_q,C_q=sqrt(5/2)n_c r_q`, their ratios to the fixed-mass
baseline, scalar profile changes, energy components, edge behavior, all
failures, and sampled profiles. A rising or falling C_q is an output, not
a success criterion. Failure to converge is unresolved branch continuation,
not nonexistence or instability. Stop a failed family's continuation and
explicitly record its remaining fractions as not attempted; do not silently
substitute another branch or retune the mesh/forcing.

Predetermined refinements: both families' final states for `psi_c=.99`,
both epsilon values (four cases), with `tol=2e-7` and outer radius enlarged
by `max(6 sqrt(epsilon/3),.25 R_aux)`. Repeat from the converged endpoint
with its physical exterior extension; M, mb and a stay unchanged. Require
radius, central density and column relative changes below `5e-5`.

Command: `python3 field_response_2026_11_01/static_response.py NEW_RUN/result.json`.
Root must launch through its bounded runner after freezing the contract.
The script produces `result.json` and `profiles.npz`, uses no randomness,
one numerical thread, and no production or external simulation. Target
wall time is minutes and peak RSS below 1 GB; actual resources belong in
the runner record. Store 400 profile radii per result to keep total artifacts
modest (target below 2 MB).

Non-claims: no dynamical stability, formation, feedback/torque prescription,
anisotropic kinetic evolution, universal column, microscopic B/V selection,
real dwarf/spiral calibration, empirical refit, or shared physical scaling
across the two epsilon values. Baseline comparisons at fixed epsilon share
the same parent coefficients and dark mass. Constants need not be shared
between distinct epsilon experiments.
