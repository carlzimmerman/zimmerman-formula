# Charged-interface investigation — 24 October 2026

**Status: no complete galaxy formation or stationary interface solution.**
We tested a new conserved interface charge, its polarization dependence,
and independent surface tension. This goes beyond the previous interface-only
alignment and curvature trials; those failures were used rather than rerun.

The charge supplies a real counterforce to shrinking the interface. For an
isolated unit wall the simplest energy is tau R²+k/R², so
f=-2tau R+2k/R³ and K=8tau at R⁴=k/tau. The field calculations release
contrast, radius and all outer phase cells. Those extra degrees of freedom,
and the actual material force, are decisive.

## Evidence

| Run | Finite test | Result |
|---|---|---|
| CI-1 `run_charge` | 16 plain-charge states | Charge stored in outer ripples; no joint pass |
| CI-2 `run_protection` | 12 stronger-barrier states | One apparent finite-radius candidate |
| CI-3 `run_refine` | 3 candidate refinements | At n512 it fragments; matter-force defect already present at n256 |
| CI-4 `run_response` | 16 polarization-charge states | New mass offset included; no joint pass |
| CI-5 `run_constant` | 12 constant-stiffness states | Suppressing cheap gradients does not recover all gates |
| CI-6 `run_tension` | 18 independent-area-tension states | One promising single-wall cell at n128 |
| CI-7 `run_tension_refine` | 4 polished/refined states | Interior law and free exterior persist, but wall becomes layered and kinetic pressure fails |
| CI-8 `run_stress` | 4 stress evaluations, 2 displacement relaxations | Arbitrary kinetic anisotropy cannot repair candidate; shifted minima do not return |
| CI-9 `run_traction` | 9 targeted charge/tension continuations | k120,tau1 clears pressure and interior-force gates at n256 |
| CI-10 `run_traction_refine` | 3 refinements, 2 displacements | Force error grows to 91% at n1024; displaced states do not restore |

The final targeted cell corrects the pressure defect, so the negative-pressure
argument must not be applied to the entire charged-interface family. It still
fails the joint task: at k120,tau1 the interior force error grows from .906%
at n256 to 22.07% at n512 and 90.86% at n1024. Both populations' isotropic
pressures remain nonnegative. The almost-pure interior fraction is therefore
not an adequate proxy for force preservation. Its displacement trials settle
at different radii and different energies, with force errors 56% and 396%.
No tested cell has demonstrated refinement, restoration, the galaxy law and
the free reservoir together. Formation from initially uncharged matter also
remains unprovided by this conserved-charge action.

For CI-7 beta1000, k100, tau.1: the n512,delta1e-6 state has
q_inner=0.999999919, q_outer=3.52e-17, metric speed 4.81e-12 and minimum
generalized phase eigenvalue .06529. Maximum interior force error is .1385%,
versus .5333% at n256 and 2.255% at n128. These are real finite-grid
improvements, but do **not** establish a working galaxy. Phase crossings are
near 21.34,21.88,27.83 kpc, not one smooth isolated wall.

The necessary radial kinetic-pressure upper bound is negative near
25.67 kpc, where T population is .983. Its minimum changes from -.03381
at n256 to -.03003 at n512, and -.03001 when the regulator is reduced tenfold.
This excludes stationary nonnegative radial/tangential kinetic stress at
the granted density with zero outer T traction. It is stronger than failure
of an isotropic Jeans construction. The positive global virial at n512 does
not repair the local stress violation.

Displacing the n512 wall by ±.2 kpc yields distinct stationary minima,
roughly ±.216 kpc away, instead of recovery. The phase Hessian alone was
therefore misleading as evidence of a physical restoring boundary: discrete
pinning/metastability remains. This is not a proof of continuum instability,
but it fails the required restoration demonstration.

## Reproducibility and limits

Each `run_*/manifest.json` records the exact command, bounds, input and output
hashes, software, resource cap and status. `validation.json` records manifest
validation. Run scripts are fixed snapshots; contracts precede their runs.
CI-1/2/4/5/6 have analytic-gradient, Hessian and independent mass-variation
checks, with observed relative errors below 4e-9. CI-6 checks both species.
Refinement and stress checks are orthogonal checks on physical interpretation.

All results are conditional on floating-point numerics, spherical prescribed
density and baryon kinematics, an effective charge postulate and supplied Q.
They are not new observations, a data fit, a microscopic charge production
mechanism or a global no-go theorem. Beta1000 is a changed phenomenological
barrier, not the original beta20 prediction. No live density/baryon evolution
or full local charge transport was solved. The audits are self-review.

See [DERIVATION.md](DERIVATION.md) for all added variational forces and the
kinetic-stress inequality; [HANDOFF.md](HANDOFF.md) for anti-repeat constraints.
