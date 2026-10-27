# Transition-force correction: derived, not yet realized

The full requested outcome remains open. This continuation derives the exact force correction, tests an alternative energy that can enforce the bulk identity, and establishes a necessary mass budget. It does not produce a new equilibrium passing the filled-gap, restoring-boundary, original-law and free-reservoir requirements together. The previously demonstrated populated branch is preserved unchanged.

## Exact correction

Use the definitions and complete species variations in [DERIVATION.md](DERIVATION.md). For the original action,

    g = q A − (1−q)h′ − q′(Psi−h),
    D = W′(gd) − q A + (1−q)h′ + q′(Psi−h),
    μ_non-gravity′ = −W′(gd)+D.

Thus a variational correction must supply μ_correction′=−D, with its corresponding conversion derivative. Here gd is the gravity of all dark material; u in A is the T contribution. At the existing stationary profile D=W′(gd)−g. Adding a frozen measured force would not cancel D after the density and phase readjust. This is a force requirement, not a derived new interaction.

## New test, TF-1

A coherent-mixture energy replaces the T-only response by an activated total-density response, quenches pressure in the activated mixture, and uses constant-coefficient interface energy. It gives the original law exactly where activation is saturated. This is an explicit new constitutive hypothesis, including a pressure-quenching assumption; it is not a microscopic deduction from the formula.

Three Fs values (.01,.03,.1), n96, domain12, were screened. All passed the directional energy-gradient checks, but none retained a q=.5 boundary. The phase core shrank away, gravity errors reached .27–.35dex to50kpc, and all optimizers ended with line-search failure. The Fs=.03 case had material residual3.1e-6; the other two had large residuals. These results reject the tested candidates, not the entire class of coherent-response theories. No restoration or continuum success claim follows from this screen. The bounded process completed; its numerical candidates did not satisfy the research target.

## Self-consistent holding-force diagnostic, TF-2

The original energy was minimized with enclosed dark mass constrained to the original galaxy law at grid centres1.5–50kpc, while phase and exterior material remained variational. Constraint error is1.1e-16, mass error4.4e-15, and the transition remains populated, with boundary57.84kpc. Material chemical potential is not constant: substantial holding forces are required. Thus merely supplying the target density reproduces the law without establishing material equilibrium.

[The saved diagnostic](run_required/results.json) includes the full chemical-potential profile and finite-difference unbalanced acceleration. Derivatives near the beginning and end of the constrained interval include constraint-edge effects; the reported maximum is not a converged continuum force estimate. It must not be treated as a physical correction law or a fitted success. The analytic variational expression above is the force definition.

## Necessary mass constraint, TF-3

The galaxy law fixes the enclosed dark mass at any chosen radius:

    Mdark,law(R)/Mb = (R/rM)² [law(gb(R))−gb(R)].

For the existing normalization:

| Requirement | Mass in Mb |
|---|---:|
| Total available |5.364|
| Required inside50kpc |4.801579|
| Maximum permitted outside50kpc |.562421|
| Existing free exterior beyond70.715kpc alone |.775244|
| Minimum mass to move from that exterior into≤50kpc |.212823|
| Required inside existing58.929kpc boundary |5.744122|

Even with no exterior mass, the original law cannot extend beyond55.3288kpc at this fixed total mass. Keeping the existing .77524Mb exterior mass bounds the law radius by47.9827kpc. These are necessary constraints, not an exclusion of a new solution: boundary relocation and reservoir redistribution remain allowed. The user did not require the old radius or old exterior mass to stay fixed.

The practical implication is that the next constitutive solution must jointly change material allocation and boundary location. A force cancellation at the old profile cannot preserve that profile and satisfy the exact law. Do not add total mass, pin a radius, convert the exterior, or impose the target density and then call the mechanism solved.

## Continuation and evidence

Start from the unchanged MI-14 state at material_interface_2026_10_24/run_final_recovery/base_192.json, using Mixed with charge0 and polish.py. Its finite radial restoration is established; its exact-law deficit is not fixed. Use the correction D and the mass budget as simultaneous requirements for a new energy. The coherent activation screen and the constrained-density diagnostic are new evidence to retain, not successful substitutes for that state.

All three bounded manifests validate against current inputs. They certify execution/provenance, not the missing physical mechanism. No source evidence was overwritten and no commit was made by this continuation.
