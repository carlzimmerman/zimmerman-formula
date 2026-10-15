# Three-dimensional continuum wall proof and a specified control mechanism

2026-10-14. Base `cabce594b9a2b682026189af188c3a98ab89d0fe`. C3W-001–006. Self-reviewed theoretical work; no independent author review, physical experiment or novelty claim.

**The requested infinite-domain three-dimensional quadratic-energy proof is obtained for a strengthened, explicitly restricted model.** It includes the actual spherical wall with bz nonzero, full gravity, all lapse/shift constraints, every direction and every wavelength on R³. It strengthens the derivative-elastic coefficient from κ=1 to κ=4; it does not retroactively certify the unchanged previous candidate or arbitrary speeds.

For a C∞ spherical transition b(r)=V F(2r/R−1), with flat cabin r≤R/2 and flat exterior r≥R, a sufficient regime is

\[
\boxed{V\le0.1c,\qquad R\ge100\sqrt D,\qquad D=M_p^2/h_{\rm med}.}
\]

D is an assigned theory scale. This is not a measured curvature activation threshold. The engineered medium remains present outside the wall, so the proof is not a physical interface to ordinary vacuum.

## What is proved

The [complete proof](PROOF.md) derives an exact positive-square identity for the joint velocity/lapse/shift form, then bounds the static metric form. Positivity of the elliptic auxiliary Hessian gives the physical Schur-complement inequalities without replacing the infinite domain by a grid. The reduced energy obeys

\[
E_2\ge M_p^2\left[\tfrac12\|\delta\dot\gamma\|_2^2
+\tfrac1{10}\|\nabla\delta\gamma\|_2^2
+\frac1{4D}\|\delta\gamma\|_2^2\right].
\]

This energy is conserved for smooth finite-energy solutions of the stationary linearized equations. It is a quadratic energy-stability theorem, not nonlinear stability, a causal-front or general well-posedness theorem, or an experimental validation of the assigned negative-energy source.

The separate full 3D audit retains every metric and auxiliary component and the nonzero normalized-clock expansion terms. Its 27-mode Galerkin calculation agrees with the positive-square identity to about 3.6×10^−15, reproduces the flat six-mode spectrum to about 2.6×10^−15, and satisfies the analytic operator lower bounds in all three specified curvature controls. These finite checks audit the derivation; the all-R³ theorem rests on the displayed inequalities.

## The theoretical propulsion chain is now specified

Two missing interactions have been made explicit:

1. [A dynamical controller](CONTROL.md) promotes the speed state to a scalar Λ and adds a derivative current that cancels its otherwise nonzero field-equation force. The allowed steady speeds then belong to **one fixed covariant action**. A sufficient mixed-energy stiffness criterion is derived in terms of explicitly defined coefficient norms; those norms have not been numerically expanded or independently audited as a seven-mode matrix.
2. [An optical pump](PUMP.md) adds a postulated gauge-invariant coupling between clock-frame electric energy and Λ. Its Hamiltonian and reciprocal work terms show exactly how light can supply controller energy. The coupling is assumed, not derived from or measured for cold energy.

The action-level mechanism is photons → controller → clock/material stress → geometry → test-payload motion. [The payload analysis](MECHANISM.md) distinguishes geodesic transport in the cavity from an optional direct scalar-gradient force and retains the reciprocal energy/momentum exchange. A finite massive payload changes the geometry and has not been included in the proved background.

## The decisive remaining limits

A uniform controller change over infinite space has infinite kinetic cost. Local activation requires gradient energy. For one explicit strong sufficient controller choice, a localized controller offset Δ=0.01 across a metre-scale region has a quadratic model energy bound of about **3×10^39 J**. This is model-specific and conditional on that branch's coupling criterion; it is neither a universal propulsion bound nor an achieved craft velocity change.

The uniform κ=4 medium also fails the ordinary-vacuum tensor-speed check: its tensor group speed is below about 0.775c, in conflict with the near-light propagation observed in [GW170817](https://arxiv.org/pdf/1710.05834) if the medium filled observed vacuum. A finite engineered phase must therefore be matched to an acceptable exterior; that interface is not supplied by the all-space theorem.

No localized finite-energy launch solution with a backreacting craft has yet been derived. No microscopic cold carrier or source of the exotic stress has been identified. The hypothetical χ/S conversion rate, the new optical coupling and a physical vacuum interface remain unverified. General relativity's geometric ADM surface integrals for this prescribed target vanish, but the full modified-theory canonical charge and fuel/hardware budget have not been computed; zero geometric ADM charge is not free propulsion.

The continuum wall obstruction has a rigorous sufficient repair in the stated model. The mechanism now has explicit controller and light-transfer terms, rather than an unexplained connection. **It is not a working or practically supported cold-energy drive.** The next physical obligation is the coupled localized launch/payload solution and its work budget, with the controller-cost problem addressed.

Evidence: 60 mathematical assertions across seven completed frozen runs, one retained implementation failure, [audit](AUDIT.md), [current state](CURRENT.txt), and [reproduction](REPRODUCE.txt). None of those counts supplies empirical evidence.
