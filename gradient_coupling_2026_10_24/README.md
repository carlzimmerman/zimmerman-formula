# Coupled inward redistribution: tested, full target still unresolved

The new interaction can move material inward, but no tested equilibrium preserves the original galaxy law, fills the full transition, retains a resolved restoring boundary, and leaves a substantial free exterior simultaneously. All mass and boundary variables were free. The total available mass stayed 5.364 Mb; no target-density constraint or law-error penalty was used.

## What was derived and changed

A positive completed-square energy couples material amplitude a=sqrt(rho) to the phase gradient:

    Ec = (κ/2) ∫ r² [a′ − eta a q′]² dr, κ=(L/rM)³.

Its density potential, conversion potential and both species forces are derived in [DERIVATION.md](DERIVATION.md), including every mixed derivative. This differs from the previously tested uncoupled material stiffness and fixed-density phase alignment. It favours a density contrast across the phase transition. It also has a bulk force, which is retained when comparing against the galaxy law.

The mechanism and sign control were tested at six coefficient pairs, followed by four intermediate strengths. Directional checks perturb both logarithmic masses and phase. Material-amplitude coordinates avoid the earlier direct-mass stiffness near almost empty cells.

## Inward transfer occurs, but it does not solve the force balance

At L=10 kpc, increasing eta from 1 to 3 moves the boundary from 70.31 to 57.40 kpc and reduces mass outside 50 kpc from 1.7680 to 1.1862 Mb. That is an inward transfer of about 0.582 Mb in these two equilibria. But the exact-law budget permits only 0.56242 Mb outside 50 kpc, so the latter state still has about 0.624 Mb too much there. The maximum law error remains roughly 28%, including the inner core.

At weak stiffness, law errors are smaller, but the material profile contains a depleted interval. Intermediate strengths do not give a verified overlap of law preservation and material support. The coefficients are explicit constitutive hypotheses, not microscopic deductions or universal fitted constants.

## Law and restoration tested together

The selected intermediate state, L=5 kpc and eta=3, was subjected to joint material/phase displacements of ±1 kpc on two grids:

| Diagnostic | n96 | n144 |
|---|---:|---:|
| Boundary radius |122.00 kpc|175.81 kpc|
| Maximum law error, 1.5–50 kpc |.04420 dex|.04667 dex|
| Relaxed local boundary stiffness |1.8103e-4 Eunit/kpc²|4.7109e-5 Eunit/kpc²|
| Material KKT residual in audited recovered state |3.05e-6|4.45e-6|

On each individual grid, both displacements return to the local minimum. The constrained active-tangent Hessian and material Hessian are positive; no negative endpoint diagonal was detected. Thus the finite-grid local force is restoring, approximately F_R=−K(R−R*) for the tabulated K. This is not a resolved physical boundary: its radius shifts by about 54 kpc on refinement, and material support fails.

**Correction to the initial selection screen:** it evaluated density rebound only up to the q=.5 crossing. That cut excluded part of the cavity on the coarse grid. The expanded support audit includes both sides of the interface and finds a depleted interval already on n96. Therefore this state was never a verified filled-gap solution, even before the refined grid rejected it. The retained raw eligibility fields describe the earlier incomplete screen; use run_support/results.json for support interpretation.

The [refinement figure](run_report/refinement.png) shows the density cavity, displaced phase boundary and remaining law deficit. A local positive Hessian and same-grid return test cannot override these failures.

## Why confinement remains missing

Under a mass-preserving uniform dilation, Ec scales as R^-2. Its generalized dilation force is outward. The scaling was checked independently to about 1e-15. The coupling can move material inward relative to other shells while still supplying expansive total stress. This explains an expansion tendency; it is not a universal exclusion theorem.

A combined screen then added the existing mixed-material response capacity k/I to supply an inward stress. This was tested alongside the new density/phase coupling, rather than rerunning charge alone. All density, phase, response and mixed derivatives were retained. The three supplied-charge values .003, .03 and .3 did not fix the mass budget or material support. At stronger charge an extra inner mixed layer appears, repeating a known physical failure despite the new coupling. That combined mechanism is rejected for the tested states. No charge-production mechanism is supplied.

## Evidence and continuation

Nine bounded records are retained. Seven completed and two failed before optimization: GC-1 had a Python module-name collision, and GC-6 stopped at the largest finite-difference step. GC-2 fixes the import without changing the physical model; GC-7 uses converged derivative step sizes. All nine provenance manifests validate. Execution completion is not a physical success certificate.

No new state supersedes the previously established populated MI-14 branch. The original full objective remains open. Preserve the inward-transfer measurement, the expanded interface-support diagnostic, the virial sign and the failed combination with response capacity. Do not continue tuning this positive-gradient family while counting a distant phase crossing or numerical density tails as a solved interface.

[Full forces](DERIVATION.md) · [Machine-readable results](run_report/results.json) · [Expanded support audit](run_support/results.json) · [Handoff](HANDOFF.md) · [Evidence validation](validation.json)

These files are local. No commit or push was made for this continuation; the earlier research branch and unrelated work were not modified.
