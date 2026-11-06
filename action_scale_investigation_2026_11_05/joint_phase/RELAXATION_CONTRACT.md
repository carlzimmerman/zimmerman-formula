# Relaxation and baryon-powered steady state

Base: aa12697db1. Target remains both a dynamically selected material inventory
and pressure yielding v_flat^4=G Mb c sqrt(G rho_DE)/2, with no fitted coefficient.
Scope: this investigation directory only. No adopted-action changes.

Route A: derive free-energy dissipation for a thermal particle reservoir versus
number-conserving transport. Identify what can forget history and what still
requires T, chemical potential or conserved inventory. Include self-gravity's
loss of convexity; do not claim a general unique attractor from entropy increase.

Route B: optically thin baryon-powered halo, central luminosity L, heating
H=n sigma_abs L/(4pi r^2), cooling C=n^2 Lambda(T), Lambda=Lambda_q T^q.
Derive outer constant-T density and circular speed with halo self-gravity,
then impose hydrostatic T=m v^2/(2kB). Let L proportional to Mb^p and derive
the mass exponent. Test q=1,p=1 explicitly without imposing the MOND coefficient.
Differentiate thermal balance at fixed density and fixed pressure. Never
substitute a heat equation for a particle continuity equation. A stationary
halo profile is not an established formation attractor.

Route C: match the outer singular isothermal tail to an independently supplied
positive phase pressure, tracking radius and total mass. Check halo dominance
before treating the resulting inventory as a solution with baryons included.
Preserve the earlier distinction between phase splitting and absolute vacuum.

Validation: exact symbolic identities plus bounded isobaric thermal perturbation
ODEs dtheta/dt=1-theta^(q-1). q=2, theta_initial=0.1 and 10, t in [0,12],
DOP853 rtol1e-10 atol1e-12; compare with exact exponential within1e-8.
q=1 has zero RHS for every positive theta and must not be called attracting.
Negative control incorrectly changes the isobaric stability slope from1-q to
-q; the derivative check must fail. 60 seconds, one thread, no empirical data,
parameter scan, full hydrodynamic stability or microscopic cooling derivation.
