# Fixed-mass cold limit of finite kinetic equilibria, before computation

Use the finite-stiff identified model already derived, gamma0.01, ra1, Plummer baryon scale1. Hold cold mass/Mb=1 fixed. Vary positive distribution amplitude A=10,100,1000,10000 and shoot central Psi to match the finite-edge mass. Upper trajectories hitting q0.99 may bracket the search but cannot count as solutions: final result must reach Psi0 and match mass within1e-5. Record failure if no valid root. Report edge, central Psi, kinetic pressure scale and native cold algebraic-law diagnostics over a common interior range where all solutions exist. No empirical fit or derived population fraction.

The formal functional argument predicts that large F (hence A) weakens the quadratic occupation penalty and can approach a cold constrained energy minimum, but convergence and its rate are not assumed. At positive gamma the correct limiting condition is R+gamma rho'=gNb, not exactly the zero-stiffness algebraic law. Do not use agreement with the latter alone as a success gate.

## Probe correction and cold reference

The displayed limiting-condition sign above was a transcription error: the native force is -gNb+R-gamma rho', so the cold condition is R-gamma rho'=gNb. The evolution/shooting equations already used that sign. The diagnostic residual is corrected accordingly. The first fixed-mass probe failed the1e-5 gate at A10000 because changing the integrator tolerance after shooting shifted mass by5.62e-5. Tighten shooting to2e-11, independently evaluate final solutions at2e-13 and retain the gate.

Compute an independent cold free-boundary BVP with m'=r²rho and rho'=(R-gNb)/gamma, total mass1, zero edge density, regular centre and unknown edge radius. Compare warm solutions to this finite-stiffness reference, not just the algebraic law. Numerical failure or cap violation invalidates the reference; require converged BVP and positive density inside.
