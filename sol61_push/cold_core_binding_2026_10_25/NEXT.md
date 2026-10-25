# Continue with an actual receiver and a derived selector

1. Keep the current self-energy, phase-motion, cross-energy and finite-flux ledgers separate. The12 windows are NOT retained material cores. Find/evolve a genuine bound subset and its moving potential, rather than reporting aperture mass or frozen negative spectral weight as a remnant. Any subset definition must be registered and its cutoff/binding sensitivity retained.
2. Diagnose the full-state timestep limitation before a new long production. The remaining error is concentrated in outgoing-region/higher-azimuth structure. Use controlled kinetic-versus-full-step comparisons or exact finite-mode exponential benchmarks to identify stiffness/aliasing; preserve every one-source operator and avoid deleting modes to manufacture cooling. Joint polar/azimuth and radial surface-current convergence still matter. Do not reuse either failed CCT016 s02 endpoint.
3. The common carrier slowdown already fails the initial-energy selector. Do not repeat it with four independently tuned lambdas and call that a mechanism. Derive loading from actual initial densities/source histories or a same-action transmission law, with abundance/supply and profile uncertainties carried through all four dwarfs. Negative whole-wave energy alone is insufficient. Fornax/Leo I controls must remain in the same fit/test.
4. Test an actual energy/angular receiver. LIVE_RECEIVER.md gives conditional all-space work/torque equations for pre-stellar live-source assembly. Freeze a finite receiver mass/profile/history and coupling first, then account for equal-and-opposite work, recoil, radiation/outflow and later recapture. External confinement or lowered interaction energy is not independent cold self-binding. If gas is removed later, follow whether the cold core survives. A static elastic filter can regulate loading but does not supply absorption in the checked approximation.
5. Derive the current-action bridge before borrowing the Palatini filter or another gravity lane. The source density in that interface is externally supported matter, not cold density counted again. Freeze the same rule for Draco, Sextans, Fornax, Leo I, then evolve stars after the proposed pre-stellar assembly. No instantaneous virial screen is stellar survival.

Useful existing reproducible commands (repository root):

    /usr/bin/python3 sol61_push/cold_core_binding_2026_10_25/controls.py
    /usr/bin/python3 sol61_push/cold_core_binding_2026_10_25/phase_controls.py
    /usr/bin/python3 sol61_push/cold_core_binding_2026_10_25/assembly_controls.py
    /usr/bin/python3 sol61_push/cold_core_binding_2026_10_25/radial_controls.py

Completed production commands are retained in each raw JSON and run_manifests. Producers refuse overwrite of completed outputs. To repeat a case, use a fresh destination/source copy or an explicitly new output tag; preserve the current audited files and their pins. A further short timestep test, if justified by the full-state diagnostic, can use the unchanged driver with a NEW tag:

    /usr/bin/python3 sol61_push/cold_core_binding_2026_10_25/time_refine_v2.py --seed draco48x80_s01 --dt .0025 --T .2 --tag late_dt0025_next

This is a conditional diagnostic, not a queued run or a new full formation history. Keep one thread, unchanged750MB measured headroom and all experiments below1GB. No automation, other-chat message or publication is authorized by this handoff.
