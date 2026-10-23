# Mesh-consistent initialization improves the live conservative test

Solving the equilibrium of the actual discrete mean field reduces unperturbed radius drift by factors of about9 and6 on the two tested meshes. Matching the injected perturbation energy then gives closely aligned early bulk responses and smaller late disturbances at both resolutions. This is a better-controlled finite-time response test, not a converged damping-rate or asymptotic-settling result.

The tested A10 equilibrium is the warmer member of the constructed family, which does not reproduce the cold force-law profile closely. These dynamics must not be transferred to the much colder near-law members without a separate calculation.

## Solve the same mean field that is evolved

Retain the spherical cloud-in-cell Hamiltonian of LIVE_RELAXATION_RESULT.md, fixed Plummer baryons, A10,ra1,gamma0.01 and total mass1. Let w_j(r) be the radial interpolation weights and mu_j(m) the derivative of the discrete field energy with respect to node mass. Set z_j=Ecut-mu_j and

    Psi(r)=sum_j w_j(r) z_j-Phi_b(r),
    rho(r)=10 [Psi(r)]_+^(5/2)/(1+r²),
    m_j=integral r² w_j(r) rho(r) dr.

Solve z_j+mu_j(m)-Ecut=0 together with sum m_j=1. This integrates the interpolated chemical potential between nodes. Replacing it with a continuum nodal-density formula would not solve the same stationary problem.

Gauss quadrature is applied separately in each interpolation interval. The response Jacobian dm/dz is a positive semidefinite tridiagonal matrix; the field Hessian is the cumulative positive remainder curvature plus the positive stiffness diagonal. A damped Newton solve maintains the cap condition during iteration.

Both256- and512-node problems converge in7 iterations. Maximum residuals are1.01e-14 and5.97e-15; mass errors are below1.8e-15. Doubling quadrature order12 to24 changes z by at most2.39e-15. The cutoff energies are-0.145603610 and-0.146716416, respectively; the different meshes still represent slightly different mean fields.

This solves the continuous f(Q) mean-field equilibrium on the chosen interpolation scheme. A finite representative-particle sample is not an exact stationary state, so residual particle noise remains expected.

## Matched-energy evolution

Sample each new distribution with the same deterministic quiet-start method, and run:

| grid | particles | dt | duration |
|---|---:|---:|---:|
| 256 | 32768 | 0.005 | 40 |
| 512 | 131072 | 0.0025 | 40 |

At each resolution, evolve an unperturbed control and a canonical dilation x->lambda x,v->v/lambda. Solve lambda separately so the discrete injected energy is0.0008 at both resolutions. The resulting lambda values are1.044304991 and1.044525810. Actual injected energies agree with0.0008 to better than4e-17; the old42% mismatch is removed.

No friction, sink or imposed relaxation term is added. All accepted runs remain within the radial grid and admissible cap. They preserve particle angular momentum and use the force derived from the reported discrete energy.

## Improvement and remaining uncertainty

| metric | 256 nodes | 512 nodes |
|---|---:|---:|
| old continuum-initialized control radius drift | 0.0198541 | 0.00959101 |
| new control radius drift | 0.00217015 | 0.00160444 |
| early control-subtracted RMS response, t<=10 | 0.0332488 | 0.0330486 |
| late control-subtracted RMS response, t>=30 | 0.0135712 | 0.0110419 |
| late/early ratio | 0.4082 | 0.3341 |
| maximum energy drift / injected energy | 0.306% | 0.120% |

The cross-resolution control-subtracted curves differ by0.00148919 RMS and0.00419168 at maximum. The late response therefore still has appreciable resolution dependence. The early curves agree more closely, but two resolutions varying particles and grid together are not an independent convergence study of either error source.

Maximum total-energy drift over all four runs is6.92e-6; force finite-difference errors are below5.68e-6 and absolute angular-momentum errors below2.9e-14. These numerical conservation checks support the calculation but do not establish a physical damping law.

The bulk disturbance becomes smaller during this window without losing its injected energy. That is compatible with orbital phase mixing/internal redistribution. It does not isolate a microscopic damping mechanism, prove permanent settling, or rule out later revivals. No exponential fit or numerical relaxation time is claimed. The windows remain exploratory choices inherited from the earlier probe.

The larger occupation parameters that approach the cold law have narrower velocity distributions and different response scales. Their evolution and numerical noise sensitivity are untested here. Nor does this near-equilibrium perturbation show that a primordial population can reach the chosen f(Q) or generate the free S4 fraction.

## Current repository context

The concurrently completed D7d_screened_q2/README.md at commit b26f14bb82 reports that stiffness suppresses the Galactic-field Cassini quadrupole strongly enough to pass its tested gate at the record's physical lengths. It reports a passing canonical critical-length upper bound0.069pc and Q2 approximately1.0–2.3e-34 s^-2 at24pc. The report distinguishes a nonconverged intermediate band and treats its critical length as a bracket/upper bound.

This checkpoint inspected that report, not its full28-minute solver run. It is a positive reported result for the screened static action, not a verified covariant parent, selection mechanism or proof that the kinetic identified-medium branch is the same theory. It supersedes treating the screened Cassini gate as simply uncomputed in earlier synthesis entries.

## Next obligation and evidence

Extend the matched-energy evolution long enough to test revivals, independently vary particle count and grid, and test a genuinely near-law cold member. Only then is a quantitative relaxation comparison meaningful. Formation and occupation selection require additional conserved-state information or a derived interaction.

The direct equilibrium solves and live trajectories retain their configurations and diagnostics. discrete_analysis_run/manifest.json validates;6 audit checks pass. The bounded run audits the stored direct-run artifacts; it does not claim those evolutions were performed inside the bounded runner. Input hashes cover all code, initial equilibria and trajectory files. No new mutation was performed. The scientific plot discrete_response.png was visually inspected. Interpretation remains self-reviewed.
