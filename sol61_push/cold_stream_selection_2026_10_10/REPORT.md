# Cold streams: an occupancy test and the remaining 32 pi condition

2026-10-10, base `93abcbeb6`. This follows the owner's passing-stream interpretation in [RESEARCH_CONTRACT](../RESEARCH_CONTRACT.md). No particle species, scattering cross-section, new geometry or observational yardstick is introduced. The active CFG598 velocity-target and settling-front calculations are not duplicated.

**Assessment:** a gravitating distribution with nonrelativistic motion is a physically meaningful candidate state. The repository has not identified a distinct substance called cold energy. This calculation determines what a passing population would have to do; it does not establish its existence, formation or stability.

## 1. The density measures traffic, not net inflow

For spherical stationary streams, let E and j denote specific orbital energy and angular-momentum magnitude. Where an orbit crosses radius r,

\[
|v_r|=\sqrt{2[E-\Phi(r)]-j^2/r^2},\qquad
A(r)\equiv4\pi r^2\rho_c(r)
=\int_{\rm crossing}\frac{d\dot M_++d\dot M_-}{|v_r|}.
\]

Both crossing-flux measures are positive. Their difference is net flow. Equal inward and outward flux therefore gives zero net accretion while maintaining a nonzero gravitating density. For a bound orbit of radial period T_r and assigned mass dM, each one-way flux is dM/T_r; its contribution is 2dM/(T_r|v_r|). This is residence-time bookkeeping, not an extra force law. Counterstreaming radial velocity variance supplies radial stress even when the mean radial velocity vanishes; whether that stress supports the specified profile requires the full kinetic equations.

Unlike the previously excluded passive beam, this description admits bound, self-gravitating populations. It does not itself derive capture or self-consistency. The [earlier beam calculation](../RESULTS_2026-09-29.md) remains valid in its narrower scope.

## 2. The exact kernel severely limits deep core-crossing traffic

Use compact baryons, the **exponential** kernel, q=r_M/r, r_M=sqrt(GM_b/a0), V_f^4=GM_b a0, and cold mass M_c=M_b/(exp(q)-1), truncated at R. This is the stipulated target, not an evolved prediction. Outside the baryons,

\[
A(r)=\frac{V_f^2}{G}\frac{q^2e^{-q}}{(1-e^{-q})^2}.
\]

For every **bound** stream, |v_r|≤v_esc. Positivity therefore gives a necessary condition on the total unsigned crossing rate:

\[
\boxed{\dot M_{\rm unsigned}(r)\le A(r)v_{\rm esc}(r).}
\]

Include the cold component's gravity, match to the exterior finite mass, and normalize Phi(infinity)=0. With q_R=r_M/R,

\[
\frac{v_{\rm esc}^2}{V_f^2}
=2\left[\frac{q_R}{1-e^{-q_R}}
+\ln\frac{e^q-1}{e^{q_R}-1}\right].
\]

For the inherited illustrative settled supply M_c(R)/M_b=5.364, the cap on unsigned flux, in units V_f^3/G, is approximately **0.023 at r=0.1r_M** and **5.6e-6 at r=0.05r_M**. The baryons must lie inside the radius where the compact-source formula is applied. These are not measured flux limits.

Thus a stream that repeatedly crosses those radii cannot carry arbitrary mass flux while retaining the exact target's central hollow. Any traffic above this cap must avoid those radii, be absent from that population, or the density law must change. Nonzero angular momentum can provide a pericenter barrier. The bound alone does not fix what fraction of outer-halo traffic crosses the core. Unbound streams require a separately declared energy/speed ceiling; the escape-speed bound cannot be applied to them.

For a finite nonzero radial crossing flux with a bounded orbital-energy spectrum in a Kepler-dominated inner annulus, |v_r|≈sqrt(2GM_b/r), so rho_stream∝r^(-3/2). Such a population cannot reproduce an exponentially depleted inner target arbitrarily far into that regime. This is not a statement about all anisotropic streams or the interior of extended baryons.

## 3. The coefficient becomes a measurable stream-selection requirement

In a deep, cold-dominated flat-curve interval, M_c≈Ar with nearly constant A gives V_f²≈GA and

\[
a_0\approx\frac{GA^2}{M_b},\qquad
\kappa_{\rm stream}\equiv\frac{GA^2}{M_b c\sqrt{G\rho_{DE}}}.
\]

The target requires kappa_stream=1/2, equivalently

\[
\boxed{A^4=\frac{c^2\rho_{DE}M_b^2}{4G}.}
\]

Using Lambda=8 pi G rho_DE/c², this is the same **C=Lambda c^4/a0²=32 pi** puzzle. It is a conditional translation into orbit traffic and residence times, not a derivation. A finite radial interval, baryonic force and any enclosed-mass intercept must be accounted for before estimating a0 from A.

There is a specific missing mechanism: central collisionless gravity preserves each orbit's j, even during spherical time-dependent assembly. Phase mixing alone does not erase the angular-momentum population. Conservation of mass, total energy and total vector angular momentum is also insufficient: two isotropically oriented Kepler tracer ensembles with the same mass and E=-1, but j=0.3 and 0.7 (G M_b=1), have zero total vector angular momentum and the same radial period, yet their A(0.5) differ by sqrt(41)≈6.40; only the first reaches r=0.2. This is a fixed-potential tracer counterexample, not a self-gravitating halo solution.

Radial-only dissipative cooling preserves j and drains the radial motion; without replenishment, energy transfer or an undamped sector it tends toward circularization rather than sustaining passing streams. Internal interactions or nonspherical gravitational torques can redistribute j while conserving total vector angular momentum. That possibility remains open. CFG541's additional position-advection drift is not pure Hamiltonian central-force motion, so its orbital-population changes need their own accounting.

## Executable next decision

Measure A from unsigned crossings and residence times in an independently evolved population; separately record net flux, low-j/core-crossing traffic, stress and energy transfer. Compare distinct incoming populations with matched conserved totals. A genuine selector must converge to the required A–M_b–rho_DE relation without imposing the target density. A CFG598 equilibrium fitted to that density cannot independently establish this selection because A is already constrained by the fit.

This is headway on the *selection test*, not on the numerical coefficient itself. The calculation has not supplied a vacuum coupling, cold abundance or a derived stable attractor. The exact kernel may demand significant orbit filtering; whether the actual dynamics performs it is now a concrete question.

## Evidence

`check.py` independently integrates the target potential, differentiates the enclosed mass, normalizes Kepler residence probabilities and checks the equal-conserved-totals counterexample. All 19 assertions passed and the manifest validates. Dimensionless benchmarks use G=M_b=a0=1. The contract and validated run manifest record inputs and numerical limits. Separate readers checked the residence relation and the distinction between individual and total angular-momentum conservation; a focused review confirmed the escape potential, flux inequality, counterexample and coefficient dictionary. The arithmetic is project-specific; standard orbital bookkeeping and circular-support comparisons are not claimed as new physics. No global novelty search or new observational analysis was performed.
