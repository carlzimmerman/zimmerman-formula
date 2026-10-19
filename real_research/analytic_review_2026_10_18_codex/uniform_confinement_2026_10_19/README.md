# Conditions for a uniformly finite perturbed halo

19 October 2026. Checkpoint ZAR-2026-10-19-06, continuing [nonlinear radial stability](../nonlinear_radial_2026_10_19/README.md). The positive point baryon mass, two populations, exact warm equilibrium and spherical deep-cubic equations are unchanged.

**One common binding reserve at every outward crossing of a fixed outer sphere is enough to bound the full halo for all time.** The condition tests the particles that can enlarge the boundary, allows continued interior oscillations and gives an explicit enclosing radius. Necessary and sufficient launch-speed thresholds differ by a quantified O(epsilon) allowance from the previously controlled exterior mass. They coincide for the autonomous comparison force.

This is a sharp comparison criterion, not a proof of a globally weakest initial-data condition. Its propagation from initial data alone remains unresolved. Small nonlinear density/energy perturbations and initially negative particle energies do not themselves establish the required all-time reserve.

Let T,U be the actual conserved masses and let the established nonlinear theorem give sup_t X(f(t)-F)<epsilon. Set c=G^2/a_0 and

\[
A_f^w=G[M_b+(T+U-\epsilon)_+],\quad B_f^w=0,
\qquad A_t^w=G[M_b+(U-\epsilon)_+],\quad B_t^w=cT^2.
\]

Choose b containing the original and initial supports and large enough that A_i^w b^2-Lambda b-B_i^w>0. Write

\[
W_i^w(r,L)=L/(2r^2)-A_i^w/r+B_i^w/(3r^3).
\]

If every repeated outward crossing of b has speed u satisfying

\[
\frac{u^2}{2}+W_i^w(b,L)\le-\eta_i<0,
\]

then every particle stays within

\[
\boxed{R_* =\max\{b,A_f^w/\eta_f,A_t^w/\eta_t\}}
\]

for all time. A sharper speed cap certifies any selected radius R>b directly. [EXTERIOR_LAUNCH_CRITERION.md](EXTERIOR_LAUNCH_CRITERION.md) proves the result, the necessary comparison threshold and their explicit difference.

[BINDING_WORK_AND_CURRENTS.md](BINDING_WORK_AND_CURRENTS.md) gives exact energy-transfer identities and independent sufficient certificates. The most useful scalar version requires that total positive potential work, computed from the signed radial currents, remain below the initial binding reserve. A finite-boundary version only uses relative potential work inside the chosen radius. These are additional dynamical estimates; the old nonlinear theorem bounds their instantaneous rate but not their accumulated value over infinite time.

Under any one of the stated confinement certificates, the existing nonlinear stability and uniform cumulative-mass/force-law estimates survive. Radial pressure remains close in integral norm, and there is now an explicit all-time positive dispersion bound at every fixed radial resolution. A pointwise all-time temperature floor still requires more information. [WARMTH_AND_SCOPE.md](WARMTH_AND_SCOPE.md) gives the bounds and the smooth vacuum matching outside the enclosing radius.

[ROUTES_AND_AUDIT.md](ROUTES_AND_AUDIT.md) distinguishes the proved conditional theorems from the open propagation problem. In particular, an explicit prescribed Kepler field can pump an initially bound particle to escape despite arbitrarily small force error. That defeats a force-envelope-only propagation argument; it is not a counterexample to the actual self-consistent initially bound subclass. [CHECKPOINT.json](CHECKPOINT.json) records the inputs, claims and review revisions.

Only this new checkpoint directory was written. No scientific scripts, simulations, numerical integrations or process inspection/control were used. Claude's calculations and all previous artifacts were left untouched. These are internal analytic results for the stated model, without a claim of global mathematical novelty or new observational evidence.
