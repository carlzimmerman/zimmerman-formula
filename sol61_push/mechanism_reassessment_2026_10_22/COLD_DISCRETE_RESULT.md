# Cold branch retains coherent radial oscillations

The warm-medium transient is not a demonstrated settling mechanism for the colder branch that approaches the acceleration law. The A=10000 branch retains large breathing oscillations through t=40, with similar behavior at both tested resolutions. This is a finite-time result, not a no-go theorem for eventual phase mixing, nonlinear stability, formation, or a complete relativistic theory.

## Equilibria and comparison with the target

The CIC mean-field equilibrium solver now accepts occupation A and a previous equilibrium as an initial guess. Continuation at A=10,30,100,300,1000,3000,10000 converges on 256 and 512 radial nodes. All 14 mass/residual errors are below 6e-13. A10000 quadrature refinement from order12 to24 passes the 1e-8 potential comparison; an additional 1024-node static solution converges. These are different equilibria with different phase-space invariants, not a time evolution from warm to cold.

Integrating the interpolated equilibrium density independently gives the following total-acceleration ratios to the continuum A10000 solution:

| radius | 256 nodes | 512 nodes | 1024 nodes |
|---|---:|---:|---:|
| .1 | .89709 | .95642 | .98023 |
| .3 | .94416 | .97254 | .98637 |
| .5 | .96193 | .98094 | .99046 |
| 1 | .97918 | .98955 | .99476 |

This is significant spatial discretization error, especially near the center. The live solutions therefore approximate the cold branch, rather than exactly reproducing its continuum law. Relative to the zero-pressure finite-stiffness reference, the 1024-node acceleration ratios are .93556,.96356,.98018,.99086 at those radii. The finite-stiffness reference is itself distinct from the zero-stiffness algebraic law. A10000 was chosen; it is not derived.

## Live dynamics

Use the previous radial Hamiltonian with A10000 initial sampling. Coarse: N32768,256 nodes,dt=.005. Refined: N131072,512 nodes,dt=.0025. Both have controls and canonical dilations injecting energy .0008. All four runs finish t=40 without a domain or cap failure. Dilation factors are 1.03422844 and 1.03442790.

| response statistic | coarse | refined |
|---|---:|---:|
| control RMS-radius drift | .00041078 | .00037996 |
| early-window standard deviation, t=0–10 | .0181544 | .0180622 |
| late-window standard deviation, t=30–40 | .0170017 | .0169649 |
| late/early fluctuation ratio | .9365 | .9393 |
| late-window mean offset | .00845583 | .00828905 |
| perturbed energy error / injected energy | .0395% | .0139% |

The fluctuation ratio describes these windows; it is not a fitted damping factor. The response curves differ by .00204594 RMS and .00562334 maximum. Both show repeated oscillations with substantial retained amplitude. Maximum q stays below .472, and angular-momentum error below 8e-15. The cold controls drift much less than the warm controls. No independent particle/grid/time-step convergence is claimed.

## Verification limits retained

The first analysis run failed on JSON serialization of a NumPy boolean. The original code/run remain preserved; v2 converts check booleans to Python bools.

The v2 bounded audit has 12 of 13 checks passing and status FAILED. Its one failed gate is the refined control's finite-difference force check: relative error .00011096 versus the specified .0001 threshold. The manifest validates as an intact failed record. A direct finite-difference step probe gives errors for this particle of .00036978 at step1e-6, .00011096 at1e-5, and .00001846 at1e-4, consistent with subtraction cancellation at small steps. The probe does not silently replace the failed gate. A step of .001 is too large for another sampled particle (error .134), reinforcing the need to check interpolation boundaries. The analytic discrete force and energy were not changed.

Direct simulations are separate from the bounded artifact audit. Inputs and outputs are hashed in cold_discrete_analysis_run_v2/manifest.json. cold_force_step_probe.json records the additional direct diagnostic. Plot cold_discrete_response.png was visually inspected. Interpretation is self-reviewed.

## Mechanism implication

The warm branch's suppression of coherent radius motion cannot be assumed to survive the approach to the cold acceleration law. In this finite sample of branches, reducing velocity dispersion accompanies persistent collective oscillations. This is compatible with weaker orbital dephasing, but does not isolate the cause: orbit frequencies, collective modes, amplitude dependence and numerical convergence need separate tests.

A useful next route is a linear spectral calculation around the cold equilibrium, followed by a physically derived coupling to an energy-carrying sector if a long-lived mode survives. Adding phenomenological friction would not explain the mechanism. Existing independent-field radiation results cannot be transplanted into the identified medium without deriving a consistent coupled action. This constraint remains central to the requested theory.
