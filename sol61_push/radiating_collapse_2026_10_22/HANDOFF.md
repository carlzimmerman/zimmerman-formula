# Handoff: RC-20261022

Base revision08daade3f873ad4fa6dfbf31b9be950a833d9072; predecessor dynamical_arrest_2026_10_22. Own directory only, no commit/push. Shared repository HEAD may change during execution; each manifest pins its observed inputs and revision.

Read RESULT.md and AUDIT.md first. Original target remains open. Do not call these full 3D formation simulations or converged dwarf fits.

New durable results:
- Implemented reciprocal radial-shell/field Hamiltonian evolution. No matter damping/removal, finite chi and P inertia, exterior field absorber, signed control-surface flux, static-source ringing control and spatial/time/box repeats.
- Twelve baseline seeds M/Mstar=.5,1,2,4, spin energy0,.02,.05 retain initial inventory. Four long strong-phase seeds at1.45Gyr give M(<.881kpc)/Mstar=.5,.992,1.922,3.719. Refined heavy run3.750. No declared far-outward unbound candidates.
- Strong heavy phase export is real within numerical precision: absorbed energy~1.0–1.2% of initial binding magnitude; same-radius phase flux differs13.1% under refinement. This is finite-time export, not a cooling rate extrapolation.
- Instantaneous CDF convergence FAILS:256->512 difference.219,512->1024 difference.152. Last-third mean aperture differences improve to.0283. Bulk inner mass repeats well. Do not infer precision profiles from small energy error.
- Energy budget excludes the specified canonical cold-density endpoint for heavier bound seeds if the rest is nonnegative-energy debris/radiation. It is not a global no-go over all endpoint shapes or multiple self-bound fragments.
- Phase radiation carries no separately conserved cold material charge. Actual mass partition/ejection is required for mass selection.
- Unpumped homogeneous cold longitudinal growth has eps*y²+[1+k²-eps*rho0(1-k²)]y-rho0=0; positive growing branch decreases with k. No finite fastest wavelength is selected in this local regime. Nonlinear/nonradial fragmentation remains open.

Observational status: instantaneous snapshot comparisons are saved but NOT physical fits because of nonconvergence, time dependence and missing baryon evolution. Coarse SPARC means change little; dwarf residuals generally worsen. Growth remains the prior conditional background diagnostic; formation population/radiation cosmology uncomputed.

Next distinct work: resolve a continuum/kinetic closure through crossings and nonradial angular-momentum transport/fragmentation; identify an actual fragment-scale mechanism or supply distribution. A more tightly bound target at the same mass must be tested against its own density/lensing/stellar profile, not assumed equivalent to the canonical fit. Repeating spherical cooling alone is not evidence for a universal mass. A full 3D implementation would be a new, much larger conditional numerical study and must keep the same energy/material accounting.

Reproduction: contracts list the exact mathematical bounds and input closure. model.py is preserved for original runs; model_flux.py adds only flux instrumentation. energy_v2.py fixes only JSON bool serialization. The failed endpoint run is retained. postcheck_run records five passing and two failing interpretation gates. Manifests can be validated with computation-audit/scripts/validate_manifest.py --root .; a completed postcheck is not a pass of failed gates.
