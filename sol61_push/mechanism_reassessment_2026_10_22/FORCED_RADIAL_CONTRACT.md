# Forced radial radiation, pre-computation

Solve the formal reduced radial operator from RADIAL_WAVE_RESULT.md on a finite-stiffness Plummer background (A=1, epsilon=0.1). B=1, gamma=0.01, eta=0.01/b, b=(2+3 beta)/beta, beta=0.02798. Use a prescribed unit Gaussian breathing density rho=(r²-3) exp(-r²/2)/(2pi)^(3/2), zero total perturbed mass. Harmonic forcing in the u=r sigma equation is -r rho. It is an externally driven source, not a self-consistent matter mode.

At the small inner radius impose u=0,u''=0 as leading regular conditions; at the outer radius retain outgoing and decaying asymptotic branches with their power/log corrections. Frequencies 0.3 and 1; outer radii 100,200,400. Check solver convergence, positive outward flux, source work equals outward flux (relative 1e-4), flux constancy outside the source (relative 1e-4), and outer-radius convergence of power (relative 0.01 from 200 to400). Report actual failures. Compare homogeneous vacuum control to analytic Gaussian form factor power; no halo damping time without a mode-energy calculation.

No full finite-background constraint derivation, live matter, cosmological exterior or novelty claim. Reversing the admitted outgoing branch must produce negative radiated power or fail the outgoing check.

## Diagnostic amendments before the bounded run

The initial complex-valued collocation probe exhausted its mesh in several cases and failed a vacuum energy/control check. Splitting the same equations into eight real components corrected the large control discrepancy; no claim about the library's underlying cause is made. The remaining vacuum error was 1.35e-4 at omega=1 and disappeared when replacing u(rmin)=u''(rmin)=0 by the Taylor-extrapolated regular-origin conditions u-rmin u'=0 and u''-rmin u'''=0. Those are the current boundary conditions at rmin=1e-5. Finally the maximum mesh size was raised from 30000 through 60000 to120000, without loosening tolerance 2e-7, to resolve the longest high-frequency domain. All prior probes are retained as failed diagnostics. They are not successful evidence. Acceptance thresholds and the tested frequencies/radii were unchanged.
