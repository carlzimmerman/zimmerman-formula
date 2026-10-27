# Settled-halo test: heating confirmed, profile selection absent

12 October 2026. This tests the specific continuation left open by FORWARD_FEEDBACK_RESULT.md: start from settled halos rather than a collapsing cold sphere. The result remains negative for the proposed target selector, while the sign of feedback energy transfer becomes positive.

## Preparation and scope

Two initial spherical cold density distributions use Plummer enclosed mass

    M_c(<r)=M r³/(r²+b²)^(3/2), b=0.15 or 0.30 target radii.

Radial positions are deterministic equal-mass quantiles. Each particle is placed on a circular orbit in the actual discrete shell self-force plus the fixed initial baryon force; randomly oriented orbital planes produce spherical statistical symmetry. Circular velocities satisfy v²=r|a_r|. Thus the initial conditions are stationary shell configurations, not a guessed Jeans dispersion or a collapsing sphere. They are strongly tangential and are not representative isotropic galaxy halos. Their special form makes a clean control possible, but limits extrapolation.

Static controls confirm that the sampled mass profiles remain essentially unchanged: both refined controls have zero change at the scored radii, and energy errors below 4e-10 of initial binding energy. Softening and the shell convention are unchanged from the preceding feedback experiment. No radial target was inserted into forces, velocities, or the feedback driver.

The same prescribed baryonic redistribution expands the gas scale by eight, with gas fraction 0.5, four cycles, start time 1.0, rapid expansion duration 0.02 and slow return duration 0.60. A slower symmetric 0.31/0.31 control is also run. End time is 8 model units, 24.35 Gyr of isolated exploratory evolution. The stellar/gas energy source is still not simulated. Work transferred by the prescribed driver is measured explicitly. No cold self-collisions are included; the test isolates spherical gravitational feedback.

There are ten cases: static, rapid and slow for each initial scale at N=1024 and dt=0.001; static and rapid for each scale at N=2048 and dt=0.0005. One orbital-plane seed, 123, is used. This is limited numerical refinement, not full convergence or a sample of formation histories.

## Refined results

| Initial scale b/r_target | History | Net work / initial binding-energy magnitude | Maximum enclosed-mass error / supplied mass | Mass inside target radius |
|---:|---|---:|---:|---:|
| 0.15 | Static | 0 | 43.513% | 96.729% |
| 0.15 | Rapid cycles | +0.3089% | 43.542% | 96.729% |
| 0.30 | Static | 0 | 13.753% | 87.891% |
| 0.30 | Rapid cycles | +0.3316% | 13.753% | 87.891% |

Rapid feedback changes each scored cumulative profile by at most 1.563% or 1.709% of supplied mass, respectively. The two rapid refined final profiles remain separated by 38.477% of supplied mass at their most different scored radius. One happens to start closer to the target, but neither evolves to it. RMS log10 acceleration errors after rapid cycling are 0.2690 and 0.2461, respectively.

Refined work-balance errors are 4.02e-6 and 2.31e-7 of initial binding-energy magnitude, well below their positive work signals. The energy gain is therefore numerically resolved in this finite model. The slower coarse controls also gain some energy; they are not guaranteed adiabatic for every orbit. No universal rapid-versus-slow efficiency is inferred from them.

## Exact invariant explaining persistent orbital memory

For any time-dependent spherical potential,

    dL/dt = r cross F(r,t) = 0

for each collisionless particle. Changing the potential can change radial energy and eccentricity, but cannot change that particle's angular momentum. The maximum fractional angular-momentum error in these runs is below 5e-14. This is an analytic invariant, not just an observed numerical trend.

This does not prove that every common density profile is inaccessible to populations with different angular-momentum distributions: different distribution functions can share a density. It does show that the driver cannot erase arbitrary phase-space memory, and the finite experiments show substantial surviving density memory in the tested family. Nonspherical gravitational torques, collisions, accretion and mergers are outside this test and can change that conclusion.

The earlier self-collision estimate is relevant to proposed repairs: for S=0.3 cm²/g in the declared 200 km/s singular-isothermal example, the collision time is about 165 Gyr at 50 kpc, growing as r² at fixed speed. It cannot simply be assumed to provide rapid outer-halo orbital redistribution. These estimates are examples, not collision times for every particle in the present Plummer runs.

## Research decision

The feedback transfer channel works for prepared settled states, so the negative work in the collapsing experiment was not a general failure of gravitational heating. However, positive energy transfer is insufficient: the tested driver does not select the target profile from different equilibrium initial states. Repeating the same four spherical gas cycles with slightly different constants would not address the identified absence of profile selection.

A further serious route must supply the missing assembly/transport physics: nonspherical torques, physically specified accretion histories, or a new interaction with a derived collision operator. It must also explain the normalization across baryonic masses and the claimed vacuum dependence. None is derived here. There is currently no justified basis for advertising the candidate as a solved cold-energy mechanism.

## Evidence

settled_feedback.py, settled_feedback_contract.json and settled_feedback_run/ preserve the inputs, work histories, profiles and manifest. All 20 declared work-accounting and angular-momentum checks passed. Static-profile preservation and final profile differences were additionally inspected from saved outputs. These are implementation and bounded dynamical results, not universal attractor proofs or empirical detections.
