# Settling energy as a source of outer halo expansion

The new route is to let inward settling transfer energy to a distinct outer cold envelope. This could build the required inner mass while preventing the whole catchment from becoming too concentrated. It changes the current energy-exchange assumption; it is not a consequence already derived from the Zimmerman formula. The first calculation passes a mass and gravitational-energy feasibility test, but does not establish a physical evolution or an observational fit.

The review used scientific base `433d42278ccaab3279d9c54f66ff266c358a3c63` and incorporated Claude's subsequent assessment correction `b5cf2ade2` and kill sheet `d687cd4a9`, on 2026-10-10. The nine toy cases were declared in [contract.json](contract.json) before execution.

Claude's work narrows the problem. [CFG555](../../campaign_fresh_gravity/ASSESSMENT_2026-10-09.md) finds excess growth in the framework's own gravitating PM field at the higher tested resolution; the earlier particle-density pass did not test that field. [CFG557](../../campaign_fresh_gravity/CFG557_settling_catchment_derived/README.md) and [CFG559](../../campaign_fresh_gravity/CFG559_kinetic_settled_profile/README.md) indicate that reducing supply damages galaxy lensing, while the tested velocity support mostly broadens the edge and leaves the concentrated interior. CFG559's halo-model ratios at k = 1 are 1.292 and 1.378, but those sizes depend on imported halo machinery. Claude now correctly labels [CFG590](../../campaign_fresh_gravity/CFG590_framework_pk_vs_cosmic_shear/README.md) as context, not a framework-native survey exclusion. The raw-data comparison in CFG592 remains the decisive pending test. No 5–8 sigma exclusion is adopted here.

The overlooked assumption is explicit: [CFG541 equations, item 8.2](../../campaign_fresh_gravity/CFG541_cold_energy_equations_precise/EQUATIONS.md) permit only dark-energy exchange. Selective energy transfer to an outer cold envelope replaces that restriction. CFG550/558's failed temperature prescriptions and CFG559's constrained drift do not establish that every such transfer is impossible. [CFG593](../../campaign_fresh_gravity/CFG593_required_halo_profile/FROZEN_CRITERIA.md) varies settled fraction, edge and core, with an NFW-shaped residual; it does not derive an independently heated envelope. The proposed transfers can remain entirely inside the turnaround catchment, retaining its mass budget.

For a spherical density, write

\[
U(k)=\int j_0(kr)\,dM=M-\frac{k^2 I_2}{6}+\frac{k^4 I_4}{120}+\cdots,
\qquad I_n=\int r^n\,dM.
\]

Moving mass \(m_i\) from \(r_m\) to \(r_i<r_m\), and mass \(m_o\) from \(r_m\) to \(r_o>r_m\), gives

\[
\Delta I_2=-m_i(r_m^2-r_i^2)+m_o(r_o^2-r_m^2).
\]

Mass conservation alone allows the first inward move to increase low-k amplitude. Cancelling the second moment requires

\[
R_2\equiv\frac{m_o}{m_i}=\frac{r_m^2-r_i^2}{r_o^2-r_m^2}.
\]

This cancellation is not a suppression theorem: for these narrow shells, \(\Delta I_4=m_i(r_m^2-r_i^2)(r_o^2-r_i^2)>0\), leaving a positive leading k-to-the-fourth correction.

Energy supplies a different constraint. For infinitesimal moves in an initial potential \(\Phi\), gravitational-energy neutrality requires

\[
R_E=\frac{\Phi(r_m)-\Phi(r_i)}{\Phi(r_o)-\Phi(r_m)}\ge R_2
\]

whenever the enclosed mean density decreases outward. The inequality follows because \(d\Phi/d(r^2)=GM(r)/(2r^3)\) decreases: the inner secant slope is at least the outer one. Thus equal gravitational energy generally requires more outward movement than moment cancellation, giving a nonnegative second-moment change and a favorable low-k sign.

For finite transfers, self-gravity is included exactly through

\[
\Delta W=-G\int_0^\infty\frac{M_0\delta M}{r^2}\,dr
-\frac G2\int_0^\infty\frac{(\delta M)^2}{r^2}\,dr.
\]

For a fixed inward transfer and fixed radial shapes, this is a quadratic in outward mass. Its smaller physical root determines that mass; there is no separately fitted heating fraction in this test. The radial shapes themselves are prescribed toy inputs.

**Equal W is only a necessary endpoint energy condition.** The inference from W to total energy uses \(E=W/2\) for isolated stationary endpoints without surface terms. The experiment does not provide those kinetic states. Fixed external baryons, boundary pressure, an evolving background or exported energy require their own accounting; the simple virial relation must not be applied to those cases unchanged.

The calculation uses one-component truncated NFW spheres, with G = initial mass = outer radius = 1, concentrations 5, 15 and 40 measured at that radius. Transfers follow the initial density within finite bands [0.05, 0.15], [0.25, 0.35] and [0.70, 0.90]. Inward mass is 2%, 10% or 30% of the middle band's mass. The full sinc transform is evaluated, not extrapolated from its low-k series.

| Result across the nine cases | Measured range |
| --- | --- |
| Moment-cancelling outward mass / inward mass | 0.1441–0.1453 |
| Equal-W outward mass / inward mass | 0.9527–2.1079 |
| Donor mass used by equal-W branch | 3.91%–93.24% |
| Individual halo squared-transform ratio at kR = 1 | 0.98894–0.99963 |
| Same ratio at kR = 3 | 0.91447–0.99662 |
| Same ratio at kR = 10 | 1.00879–1.42875 |

All nine equal-W roots conserve mass and leave nonnegative density. The 117 numerical checks pass; independent forms of the gravitational energy agree within 5.7e-16 in the chosen units. A separate [Gauss–Legendre audit](audit.py) reproduces all 27 branches and 135 Fourier points within 6.7e-16; its [results](audit_results.json) also verify the original artifact hashes. These agreements are floating-point checks, not certified error bounds. Under-removing the donor by 1% makes 63 checks fail, including mass and energy consistency, as intended. Both run manifests validate. [Main results](runs/main/results.json), [negative control](runs/mutate/results.json), and [code](checks.py) retain the complete tested range.

These are individual halo transforms, not a cosmic power spectrum or shear prediction. At kR = 3 the squared amplitude falls by 0.34%–8.55%; at kR = 10 it rises. This scale dependence must survive mass weighting and redshift projection before it can help the actual discrepancy. Outer spherical redistribution leaves the interior Newtonian force unchanged relative to the same inward-only branch when the donor lies outside the radius considered. It can still change projected lensing and the allowed orbital distribution. The toy never matches an RAR target.

The density bands also produce upward jumps. An ordinary isotropic nonnegative f(E) equilibrium cannot realize those jumps, because its density increases with relative potential and therefore decreases outward. Positive density and equal binding energy are insufficient. Smooth realizable profiles, anisotropy where required, angular-momentum transfer and an evolution timescale are outstanding conditions, not details to hide after a fit.

There is a precise dynamical obstacle: spherical mass rearrangement entirely inside a radius leaves its exterior Newtonian potential unchanged. It cannot directly heat collisionless orbits that stay outside that radius. For particles crossing a monotonically deepening potential, the specific-energy equation dE/dt = partial Phi / partial t likewise gives no positive energy gain. The current smooth inward drift therefore does not supply the proposed outward heating. A viable mechanism needs a demonstrated transfer channel, such as non-spherical time-dependent gravitational fluctuations, potential cycles, or an explicit cold-sector interaction. Each requires new derivation. They are alternatives to test, not ingredients silently added to the theory.

The next calculation should start with the actual inner RAR target and finite cold supply, not tune these toy bands:

1. Solve the energy-budget condition for a smooth outer redistribution while holding the measured inner force fixed. Include baryonic work and boundary terms. Reject any solution that requires more donor mass or energy than available.
2. Require a nonnegative phase-space distribution and a specified conservative transfer mechanism. If no supported profile meets step 1, close this route before a large simulation.
3. Evolve the surviving mechanism and compare its own gravitating field and galaxy lensing directly with the data using CFG592's framework-native pipeline. Do not use the contextual halo-model amplitude as a verdict.

Outward redistribution affecting power is established physics; for example, [Schneider and Teyssier](https://arxiv.org/abs/1510.06034) model gas ejection and dark-matter response. The proposed distinction here is using the framework's own settling energy to expand its outer cold component. A bounded search of the reviewed campaign lanes found no equivalent tested closure. That supports a new local work direction, not a global novelty or priority claim. Neither the coefficient 1/2 nor the 32 pi squared puzzle is derived by this calculation.
