# Self-review of assembly claim and evidence

Primary verdict for the original physical target: **incomplete, with the
smallest missing implication being efficient, persistent T formation under
the proposed assembly interaction**. The tested common-parameter scan fails
its declared joint target. This is a self-review, not an independent audit.

For the narrower conservation statement, the derivation is valid on the
admissible smooth domain Ri>0 and z<1, with constant positive drag coefficients
and the declared collective C. Taking gradients of the common potential,
the two cross-work terms sum to minus the nonnegative Rayleigh dissipation.
The independently integrated receiver supplies its opposite. No force law is
switched according to object name. The primitive physics and geometric
restrictions remain assumptions rather than inferred facts.

Dependency checks:

| Obligation | Disposition |
|---|---|
| Positive same mass in T/F and bounded state fraction | Passed analytically |
| Reciprocal work, positive receiver and energy identity | Passed analytically; tested numerically |
| Gravity and phase forces from declared energy | Finite differences and homogeneity checks passed |
| Initial quadrature accuracy | Tested through 2048 cells; not a global trajectory error bound |
| Supported evolution to requested time | All 60 plus 8 refined runs completed |
| Cold evolution to requested time | 2 of 32 completed; 30 boundary-truncated |
| Targeted inward domain extension | Two five-time runs completed |
| Efficient T assembly and RAR preservation | Failed in completed tested cases |
| Asymptotic free-mass retention and observed sufficiency | Not established |
| Local interaction, separate phase transport, disk geometry | Not addressed by this reduced model |

Five manifests validate with current input hashes. They record 102 attempted
trajectories: 72 reached their own requested stopping times, 30 stopped at
the radial boundary. One boundary-truncated cold run has relative energy
error 1.0815e-4, above the declared 1e-4 gate; exclude it from quantitative
physical conclusions. Raw histories are preserved. Batch execution success
is distinct from trajectory success and scientific success.

The supported refinement changes shell sampling, quadrature and solver
tolerance together. Its precise terminal phase fractions therefore do not
establish a convergence order; the order-of-magnitude failure of formation
does persist. Half-mass dynamical times are estimated from each discretized
initial profile, so the physical stopping times also differ slightly.
The extended cold endpoints differ by 0.64 percentage points: sufficient
to retain the qualitative failure at that time, not a precise phase prediction.

This model carries several important interpretation restrictions. A uniform
phase means T/F share the shell velocity and cannot segregate. Conserved
global angular-momentum coherence replaces a locally measured vorticity.
The barrier now extends across the collective field. These changes are
disclosed model assumptions and do not count as verification of the previous
local-vorticity interaction. The soft-shell Hamiltonian averages gravity,
and does not evolve actual shell thickness or a 3D distribution function.

The receiver is a Newtonian energy variable, without microscopic recoil or
gravitating heat. Its positivity is not a derivation of its particle content.
All initial reservoirs, rotation coherences and damping constants are inputs.
The .05-dex and 90%-retention criteria are illustrative, not observational
confidence intervals. No novelty, lensing or cosmological claim is made.

Self-proofreading scope: new derivation, contracts, report and this audit;
no mathematical-token correction was needed after the final conservation
identity check. An empty bounds field in the first invariant contract was
rejected before execution and filled with the actual finite test range;
no computation or physical threshold was altered by that correction.
