# Redistribution continuation: no complete solution

Density and boundary were allowed to move in all free experiments. Total mass stayed5.364Mb. No target-density or galaxy-law penalty was added. The requested simultaneous exact-law, populated-transition, restoring-boundary and free-exterior equilibrium has not been found.

## What changed

Three new routes were executed rather than repeating old charge, bulk-binding or coherent-activation screens:

1. Release TF-2's exact-law constrained state into the original energy. It returns to the previous populated branch, R58.90kpc, law error.05027dex, with material residual3.9e-8. Thus the target profile does not remain a new free equilibrium simply because its holding constraints are removed.
2. Add positive material-amplitude stiffness only in mixed material. Three strengths equilibrate, but push the boundary outward and worsen the law. A distinct local mixed-material binding energy was also tested: weak binding barely changes the deficit; strong binding favours mixed exterior material or eliminates appreciable exterior mass.
3. Add global material-amplitude stiffness to the older high-pressure branch. This term can penalize a cavity even when its phase remains nearly pure, but it adds a bulk force. Direct-mass minimization was numerically stiff; an amplitude-coordinate continuation solves the same energy more effectively. Independent logarithmic-mass derivative checks validate the density force implementation.

The complete forces, conversion variations, numerical limitations and route distinctions are in [DERIVATION.md](DERIVATION.md).

## Best law match still fails material support

| Global material stiffness L | Boundary kpc | Maximum law error1.5–50kpc | Minimum cell mass between50kpc and boundary |
|---|---:|---:|---:|
|1kpc|134.22|4.11%|1e-12Mb: floor-active gap|
|3kpc|139.97|5.15%|1.08e-7Mb: deep depleted interval|
|10kpc|121.30|21.21%|.02211Mb: materially populated|

Errors include interpolated physical window endpoints. The weak-stiffness improvement from the old10.9% deficit is real for these numerical states, but it comes with a distant boundary and depleted interval. It is not a successful redistribution mechanism. Finite positive tails in the L3 state must not be called a filled gap.

The exterior beyond1.2R remains almost entirely free in these global-stiffness trials. That alone does not satisfy the material-support or law requirements. Material KKT residuals after amplitude continuation are7e-5–2.4e-4, so optimizer success is not an exact-equilibrium certificate either. No new state was advanced as a candidate for a restoration success claim.

## Mass budget checked, not imposed

The exact law at50kpc requires4.801579Mb inside and at most.562421Mb outside. Conservative finite-volume mass reconstructions for L1,L3,L10 give enclosed masses4.67277,4.50536,3.74799Mb. All remain short. The quoted reconstruction and inherited midpoint gravity quadrature differ at finite resolution; actual force-law errors are measured independently above.

The initial134kpc phase crossing is not a viable boundary merely because the inner law error improves. Its interior includes a depleted interval separating the galaxy from a remote transition. The prior mass-budget obstruction at the old59kpc boundary was not imposed as a fixed-radius prohibition: all boundaries moved freely. These experiments show that boundary freedom is necessary but insufficient with the tested constitutive terms.

## Evidence and handoff

Six bounded records RD-1 through RD-6 completed and all six provenance manifests validate. RD-3's three optimization trials nevertheless reached iteration limits; distinguish completed execution from converged physics. RD-4 improves numerical convergence but does not repair the failed combined physical target. Full states, gradients, constraints and diagnostics are retained.

Start a continuation from the unchanged MI-14 populated/restoring branch, not the low-law-error cavity states. New work must supply the measured inward redistribution without rewarding a remote mixed shell, reopening the cavity or overwhelming the cold-interior force law. The local capillary and local mixing-binding coefficients tested here have the wrong response; global capillarity trades material support against bulk-law error. No universal exclusion follows from this finite set.

Files: redistribute.py (release/local stiffness), binding.py (local mixing binding), global_density.py (global stiffness), amplitude.py (same-energy solver continuation), audit.py (density-gradient and mass checks), final_audit.py (endpoint/depletion diagnostics), run_final_audit/results.json (summary), validation.json (provenance). These new files are local; the earlier pushed research branch was not modified by this continuation.
