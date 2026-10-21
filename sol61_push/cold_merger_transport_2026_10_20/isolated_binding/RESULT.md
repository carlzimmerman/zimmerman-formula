# Actual-action isolated stationary binding test

20 October 2026. **A positive stationary-state merger energy gap exists in the exact ARGON11 two-field action at the tested charges.** This is new isolated-profile evidence, not an inference from the fragmentation medians. It is not a dynamical merger, a proof of a ground state/stability, or a measured escaping energy/charge/angular-momentum flux.

The source `frag3d.c` matches revision `07546091c`, SHA256 `3e54252e108e01cd2852563c7b932f3ebafa6526ad2e5bb1daf219d43ba91a82`. No source code or live simulation was executed or changed. The exploratory contracts precede the runs; no existing frozen criteria were modified.

## Exact action and normalization

Use the source's m_h=1 units, M=100, Lq=1.99 and a=200:

    V(f,h) = f^2 + Lq f^4 + a h f^2 + U(h),
    U(h) = M^2 h^2/2 - M h^3/8 + h^4/4.

For Psi=f(r) exp(i omega t), chi=h(r), the coupled spherical stationary equations are

    f'' + 2 f'/r = [1-omega^2 + 2 Lq f^2 + a h] f,
    h'' + 2 h'/r = M^2 h - 3 M h^2/8 + h^3 + a f^2.

Both field gradients are retained. This is not adiabatic mediator elimination. The boundary conditions are f'=h'=0 at epsilon=1e-4, f=h=0 at the outer box L. A cumulative-charge state enforces fixed Q and prevents convergence to the trivial zero-field solution:

    Q = 8 pi omega integral r^2 f^2 dr,
    E = 4 pi integral r^2 [omega^2 f^2 + f'^2 + h'^2/2 + V] dr.

The factors agree with the source's Q=2 Im(Psi* Psi_t). The stationary virial identity is

    T_gradient + 3 U_potential - 3 T_rotation = 0.

## Numerical result

SciPy collocation finds nodeless nonzero profiles with E/Q<1. Initial profiles are logistic guesses, not extracted from a periodic ARGON box. At L=60 and tolerance 1e-7:

| Q | omega | E | E/Q |
|---:|---:|---:|---:|
| 80,000 | 0.9218835527 | 76,157.983363 | 0.9519747920 |
| 160,000 | 0.9096140574 | 149,338.139064 | 0.9333633691 |

Hence, on this stationary branch,

    2 E_stat(80000) - E_stat(160000) = 2977.827663,
    gap / [2 E_stat(80000)] = 0.01955033164.

If two such Q=80000 profiles merge into the tested Q=160000 stationary profile, about **1.955% of their initial profile energy** must be deposited elsewhere. It may remain in oscillations, radiation, daughter fragments or spin; the calculation does not determine which channel receives it. A different dynamically accessible remnant could retain part or all of that gap instead.

This establishes substantially more than E/Q<1, but still does not establish a merger fuel rate. The difference is invariant under a common multiplicative energy/charge normalization, while physical carrier mass, weak-coupling mapping, fragment abundance and conversion to galaxy-scale power remain separate.

## Checks and evidence records

- `run_001`: 23 checks passed. L=40 and L=60 results agree in E to better than 6e-10 relative. Charge integration, virial identity, nodeless bound-branch tests and far-boundary tail tests pass.
- `run_002`: 19 checks passed, collocation tightened from 1e-5 to 1e-7. E agrees with the previous L=60 profiles to better than 6e-10 relative; gap changes by about 5.4e-5 in absolute energy units, versus a gap of 2977.8.
- Profiles at Q=79200 and 80800 give finite-difference dE/dQ=0.9218840444 at Q=80000, consistent with omega=0.9218835527 to about 5.3e-7 relative. This checks the fixed-charge normalization independently of the virial identity.
- Tight-profile integrated charges differ from their targets by less than 1e-12 relative. Virial residuals are about 1.2e-11 relative to total E; outer-20%-of-box energy fractions are below 3e-15.
- Both runner-v2 records validate and status is `completed`. Peak measured RSS is 96.1 MB and 126.7 MB; each solver command took seconds, single-threaded. No 3D calculation or live experiment was duplicated.

The numerical collocation residual is not a rigorous continuum error bound. The box/tolerance comparisons and orthogonal identities strongly support the displayed stationary branch, not uniqueness or nonlinear stability. Positive nodeless profiles and a decreasing omega along these sampled charges do not prove global energy minimization or stability against nonradial perturbations.

## What remains necessary

The next physical test must collide matched isolated profiles, vary relative phase/impact parameter, and distinguish the final bound remnant's internal energy/spin from escaping material and radiation. Close total energy, Q, linear momentum and vector J with convergence at the small orbital-energy scale. The 1.955% stationary gap alone neither supplies directional galaxy-scale torque nor predicts how much material escapes. It also does not repair the separate dwarf observational-aperture/profile/finite-stock obligations.
