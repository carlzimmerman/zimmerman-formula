# Finite-shell diagnostic for the new static equations

Base ec3a9411ad. Freeze before solver. No physical galaxy or solar fit and no
coefficient search. Four prescribed b,Lstar choices test whether the derived
radial system admits regular charged finite-shell solutions for more than one
normalization. A positive result is not stability or cosmological matching.

Units M^2=1,K=1/2, V=1e-8, q^2=2e-9, inner radius1, outer radius20,
metric mass parameter m=1e-4. b=.1,.3 and Lstar=1,3 (four cases),
gamma=K Lstar^2/2. These are numerical diagnostics with arbitrary length
units, not the inferred galactic scale or the target coefficient. No measured
a0 or kappa enters. b/G would be kappa^2 after identifying the density.

Use STATIC_RESULT.md's ODEs for N,B,p,d=p'+2p/r. Boundaries:
B(1)=(1-2m)^(-1/2), N(20)=1, d(1)=d(20)=0. These are stipulated finite-shell
metric and natural-polarization boundaries. The inner mass is a boundary
datum, not a resolved baryonic interior. Do not call it an isolated galaxy.

Use transformed p=a0(N)*tanh(z), allowing signed trial p but physical final
solutions require p>0 and p<a0 throughout. For signed trial polarization
evaluate W from |p| and W_p=p/[K(1-|p|/a0)]. No clipping of p or negative
kinetic terms. Variables are logN/m,logB/m,z,d/a_ref,
a_ref=sqrt(b*(q^2/2+V)). Include a0'(N) in the transformed z equation.

Two independent solves per case from the same analytic weak-field seed:
100 initial nodes, tol1e-6;200 initial nodes,tol1e-8. max_nodes10000.
Compare the four scaled physical fields (logN/m,logB/m,p/a_ref,d/a_ref)
on201 common points with normalized difference <=1e-5. Both solves must
converge; max RMS residual <=their requested tolerance; transformed boundary
residual <=1e-8. Final N,B positive and 0<p/a0<1 throughout all collocation
nodes and common evaluation points. No inference between sampled points
without further enclosure. Keep failed outputs; do not relax criteria.

Single core, run timeout60s. Source and result recorded with v2 manifest.
The analytic first-order equations have an independent variational check in
the preceding symbolic run; the numerical evidence establishes only solver
convergence and sampled regularity. It is not an independent PDE solver,
stability test, rigorous interval existence proof, or coefficient selection.
