# Smooth interface and observed cluster gas gate

Continue a40c03c62e. Keep r=1,s=.25; do not retune to data. Two tests:
1. Smooth fixed-source Einstein rest-density d(z)=10[1-tanh(z/w)], replacing
the d_in=20 sharp interface. w=.1,1,10,100 in prior wall units; solve the scalar
BVP with q(-L)=0,q(L)=q_vac, L=max(20,16w). Probe p/m=.001,.003,.01.
Conserved wave flux must hold to 1e-6. Repeat slowest wave with tighter ODE
tolerance (difference <1e-5). BVP tolerance1e-6, <=30000 nodes. Hold matter and
Einstein metric fixed; do not infer a full galaxy interface or stability.
2. Read gas alone in the seven established X-COP systems, six radii .1,.2,.3,
.5,.7,1 R500. Shell differences are averages, not pointwise density profiles.
Use raw cumulative MGAS and released marginal errors. For local-source matching,
calibrate bare M to restored-region Newton G and H_J to external references
1,1.8,3 e-18 s^-1. At the specified vacuum f=5/6,u=10/9:
D/c²=[3 H_J²/(8piG)] f/u, not automatically the observed vacuum density.
At restored interior rho_star=rho_J. The ideal constant-Einstein-lapse slow-wave
barrier is rho/D>31.04. Evaluate central densities and one-width endpoint-box
lower values as sensitivities, NOT confidence bounds or a joint posterior.
Stars and scalar self-density are not added; avoid double counting the scalar.
Gas is treated nonrelativistically for its trace. No cluster capture simulation.

A constant-source threshold comparison is a necessary consistency diagnostic,
not proof that every point in a shell is forbidden. Smooth real profiles and
nonlinear gravity can change the transfer. Report that limitation explicitly.
Mutation changes R500 kpc->pc conversion by 1000 and must fail independent
SI vs astronomical-unit shell-density calculation. Timeout120s one thread.
