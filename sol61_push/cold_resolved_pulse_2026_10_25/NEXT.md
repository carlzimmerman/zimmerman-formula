# Next discriminating tests

1. **Keep the energy-sign question first.** Reproduce the short local pulse with dt.01 from the clean48x80 s01 checkpoint. Do not resume either failed s02 state. Current .04/.02 results retain outward MASS and SPIN but negative outward core canonical ENERGY. Check material binding and phase-space support separately; fixed-aperture energy is not the energy of a moving material core.

   From the repository root, using a fresh tag:

       /usr/bin/python3 sol61_push/cold_resolved_pulse_2026_10_25/late_compare.py --seed draco48x80_s01 --dt .01 --T .2 --tag late_dt01_next

   This is another conditional pulse, with reset local reference and provenance. Memory is measured, not hard capped; stop at unchanged750MB gate, keep below1GB. Do not overwrite an existing tag. No future run is scheduled by this handoff.

2. **Resolve both angular directions within the same memory budget.** The48x80 branch fails polar bandwidth nearT19.74;56x64 fails spin conservation nearT17.58. The cross-grid core-mass agreement is useful but does not settle transport. Before another production run, register a joint-bandwidth test (e.g.56x80) and reduce temporary working arrays without changing the Hamiltonian/source. Validate kernels against the current implementation on nonconstant complex phases and rerun the full grid/Poisson/flux/inventory preflight below750MB. Prior48x96 failures remain failed. Never lower a gate merely to continue. Start again from clean s05 or re-evolve the original incoming wave; interpolate complex coefficients without normalizing mass. A conditional refined seed must stay labeled conditional.

3. **Make the local surface budget converge.** Derive/evaluate wave and gravitational currents consistently at the actual reporting radius from the element fields, then compare against independent refined radial calculations. The mapped-SEM inventory fixes a real quadrature error; nodal interpolation and partial-element integration still leave large outer residuals. Include the wave boundary conversion and gravitational surface energy. Preserve signed RK transfers and distinguish matter J from full gravitational torque. Demand signal-relative agreement for BOTH signs, not just a small global defect. Existing finite-matrix exactness is a control, not a physical escape certificate.

4. **Test a bound moving remnant and the actual receiver stock.** Track the material core and its potential, retained mass/profile, energy and spin; separate outgoing positive-energy wave packets from bound redistribution. Include finite-envelope support/stress and delayed recapture. AtT17.30 most of the billion-solar-mass supply is still within1546pc, far above the prior conditional Draco profile. An envelope cannot be called a successful receiver just because it temporarily stores excess mass or spin. Register an escape/retention interval and profile bounds before trying a new assembly history. Do not use artificial damping, mass renormalization, a deleted background or a second cold gravitational source to manufacture success.

5. **Only then freeze a shared history/selector test for all four dwarfs.** Use measured stellar histories, survey coverage and supply constraints; propagate their uncertainty. Derive the history-dependent selection/retention rule rather than setting four arbitrary efficiencies. Test Sextans's conditional large stock and compact aperture, Draco's core, and Fornax/Leo I upper-profile controls with the SAME equations and fixed constants. Reduce initial supply only with a common physical history rule: lowering it can cure Draco/control overstock while making Sextans supply impossible. Run actual stellar orbits in the same one-source gravitational field, including potential fluctuations and moving centers; an instantaneous virial screen is not stellar survival.

6. **Derive the action bridge before transferring any success.** MECHANISM.md's wave action is a conditional effective model. Identify its derivation, validity range, stress-energy/source normalization, wave degrees of freedom and conserved currents from the owner's CURRENT action. No result here rescues retired SCT-M/CFG960 or certifies the current theory. A shear pass, algebraic limit or a finite coherent clump is not four-dwarf closure.

Reproduce the post-processing without evolution:

    /usr/bin/python3 sol61_push/cold_resolved_pulse_2026_10_25/stock_check.py

The exact commands for completed evolution/controls are in raw producer metadata and run_manifests. Preserve current audited outputs; regenerate analysis/summary in a fresh destination or copied packet when changing their source. The original summary metadata record is historical, not a command to overwrite the corrected summary.
