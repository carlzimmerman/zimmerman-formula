# Cold collisions and the four dwarf outflows — 20 October 2026

**Result: the tested fixed-temperature elastic branch cannot supply Sextans' reference outflow.** This is a necessary upper-bound calculation, not a simulation of the actual cold-field collision kernel. It rejects the declared thermal branch and endpoint, while leaving hotter collapse, nonthermal energy transfer and fragment binding-energy release open. No physical four-dwarf formation mechanism is established.

## Exact target and evidence

The endpoint ledger comes from finalized CFG918 results, commit `bb9b20525`, canonical footing, catalogue B0, initial geometry G1, cored core C, phiK=1 and initial-spin diagnostic lambda_c=1. Draco and Sextans use its saved escape endpoints. Fornax and Leo I instead use the independently constructed receivers at radii >=2R that pass the previous **static whole-Plummer upper-dispersion guard**; the original aperture-edge capacity optima overboost that tracer. This change of reference endpoint is explicit, not a regrade of CFG918.

The prior receiver audit is `../cold_final_mile_2026_10_13/receiver_capacity_audit_2026_10_20/RESULT.txt`. These are particular allowed endpoint configurations, not a global optimization over every receiver or an inferred assembly history. The newer Sextans two-population mass-stock obstruction remains separate: this packet uses the older catalogue endpoint and cannot resolve that observational issue.

`run_001/results.json` contains 44 passed numerical/identity checks; `run_002/results.json` adds 8 bulk-motion checks. Both bounded runner-v2 evidence records validate. Peak measured RSS was 61.2 MB and 11.0 MB respectively. The analytic Maxwell moments were checked against independent numerical quadrature, including far-tail arguments. Validation certifies record structure and artifact consistency; the mathematical scope is stated below. The calculation is exploratory: a Sextans prototype preceded the written contract.

## Bound and its assumptions

Assume equal-mass, nonrelativistic, microscopically reversible elastic collisions in a stationary **zero-mean Maxwellian in the chosen inertial frame**, with one-dimensional dispersion sigma no larger than the reference core's virial value. Bound the total cross section per mass pointwise by S_max. Its actual value and angular/velocity dependence have not been derived from ARGON or the original charged-field action. The caps below are hypothetical scan inputs, not observationally established limits.

Give the mechanism highly favorable allowances: all the material spends all 12 Gyr at the cored profile's maximum central density; maintain the undepleted Maxwellian throughout; permit every selected collision outcome to escape without paying gravitational potential energy; and put escaping angular momentum perfectly aligned at R_max. These allowances overestimate the capacity of this specified thermal source. A selectively depleted tail is not an equilibrium wind.

If f_sigma(v) is the normalized Maxwell speed density, equilibrium detailed balance equates outgoing gain and loss. With mean random speed mu, the triangle inequality bounds the per-initial-mass event measure by

\[
 h(v)\,dv\ \leq T\rho_{\max}S_{\max} f_\sigma(v)(v+\mu)\,dv.
\]

Subject to the endpoint's escaping-mass fraction f_B, take the highest velocities of this upper measure first. Since both v^2/2 and R_max v increase with v, this maximizes the separate energy and aligned angular-momentum allowances. Tail moments A_k(c)=integral_c^infinity v^k f_sigma(v) dv give

\[
 f_{\rm esc}=P(A_1+\mu A_0),\qquad
 E_{\max}/M=\tfrac12P(A_3+\mu A_2),\qquad
 J_{\max}/M=R_{\max}P(A_2+\mu A_1),
\]

where P=T rho_max S_max and the code includes the km/s-to-cm/s conversion. Choose c to saturate f_B when enough events are available. These are separate optimistic upper bounds, not a joint realizable orbit. A failure of either is sufficient to reject this branch at that endpoint; passing both is insufficient to establish a wind.

The stationary distribution is **not** a prediction of the source's lambda_c=1 rotating initial condition. The streaming addendum below treats a bounded common local mean explicitly. Counterstreams and nonequilibrium collapse require another calculation.

## Four-system results

The same S_max and duration are applied to all four systems. At S_max=1 cm^2/g:

| System | Reference sigma, km/s | Allowed escaping fraction | E_max / E_required | J_max / J_required |
|---|---:|---:|---:|---:|
| Draco | 8.470 | 0.48647 | 3.848 | 20.843 |
| Sextans | 7.353 | 0.01146 | **0.07574** | **0.51274** |
| Fornax | 11.751 | 0.39477 | 1.779 | 8.858 |
| Leo I | 8.735 | 0.41838 | 1.814 | 12.192 |

Sextans keeps 25.105 million solar masses in its reference core, leaving only **291,027 solar masses** to carry away 2.399 billion solar-mass (km/s)^2 of kinetic energy. The corresponding RMS reference wind speed is **128.39 km/s**, versus random dispersion 7.35 km/s. The undepleted Maxwell probability above that speed is about 8.76e-66; the integrated upper-bound calculation, rather than that probability alone, provides the rejection.

Scanning caps 0.01, 0.1, 1, 10, 100 and 10,000 cm^2/g never meets Sextans' energy or J requirements. At the deliberately extreme cap 10,000, the upper allowances reach only **13.95% of its required energy and 69.64% of its required J**. No cap in this tested fixed-temperature class supplies all four endpoints. The absurd formal large-cap extrapolation saved in the JSON is not a physical cross-section prediction.

Fornax and Leo I pass these necessary ceilings at cap 1 using the guarded reference snapshots. That does **not** show that actual collisions leave their core masses or stellar dispersions acceptable: capacity is an upper allowance, not an automatically generated mass enhancement. The receiver radii also extend to 65–105 kpc; host tides, return and survival remain untested. No universal collision parameter has been fitted to the four dwarfs.

## Can heating or streaming rescue it?

As a diagnostic, hold density, masses and the reference required wind energy fixed while raising the random dispersion. Passing even the optimistic Sextans energy ceiling requires sigma >=25.31 km/s at cap 1, or >=19.24 km/s at cap 10,000. Heating the entire reference core to these dispersions would require about 9.21 or 4.96 times the reference wind kinetic energy, respectively. These are not new equilibrium solutions. A deeper transient potential or another energy source, its subsequent cooling, and its effect on the stars would have to be supplied and tracked.

For a common local bulk velocity bounded by |U|<=U_max, the random collision kernel remains in its comoving frame. The generous triangle-inequality extension is

\[
 E_{\rm lab,max}/M\le E_{\rm random,max}/M+U_{\max}V_{\max}
             +\tfrac12 U_{\max}^2 f_{\rm esc},
\]

where V_max is the selected tail's first velocity moment. Even perfectly aligned U<=2 sigma supplies at most **15.18%** of Sextans' energy at cap 1, or **23.82%** at cap 10,000. Meeting the energy ceiling would require pre-existing U at least **93.08** or **80.44 km/s**, respectively. These are necessary input-flow thresholds, not flow generated by the collisions. Inserting them assumes a large part of the missing energy supply. They do not exclude independently generated infall or counterstreaming.

Physically, elastic collisions redistribute kinetic energy; escape can remove energy and J from the bound system, but a cold Maxwellian cannot conveniently concentrate the required energy into this very small departing mass. The remaining live possibility is an explicitly powered, nonequilibrium phase: gravitational contraction, nonthermal transfer, or release of internal binding energy. Within the tested cross-section range, a mere increase of the equilibrium collision rate does not solve this endpoint.

## Claude selector check

Final CFG921 results `f4c87a342` and clarification `53a4f27f1` report that all five tested one-constant selector posits fail the main wider constraints on both footings. CFG922's cluster-core excess stands, so the clusters-withheld conditional is not the applicable conclusion. Source hashes and revisions are recorded in `sources.json`.

P2's successful aggregate dwarf shape fit is a calibration of a **static baryonic velocity-density selector**, not a measured cold–cold collision process. It contains no scattering kernel, angular distribution, optical depth, assembly time, escape flux or E/J transport ledger. Its cluster/red-lens failures do not exclude conservative cold-fragment scattering or gravothermal formation generally. Conversely, the dwarf fit cannot supply the missing collision mechanism. ARGON11's pinned fragmentation evidence does not yet measure that kernel.

## Executable next physical test

1. Select the actual action first: ARGON M=100 solitons and the original charged-field daughters are distinct models until a bridge is derived. Establish its physical unit mapping for fragment mass, radius, velocity and differential cross section before comparing with cm^2/g caps or dwarf budgets. Construct stable isolated fragments; do not infer their transport cross section from geometric area.
2. Compare matched isolated-fragment and two-fragment runs. Start around the Sextans thermal relative RMS speed sqrt(6) sigma=18.0 km/s (about 6e-5 c), with independently averaged relative phases and impact parameters. Measure outgoing masses, velocities, charge, radiation and capture rather than choosing favorable phases.
3. Separate center-of-mass orbital energy from internal binding energy. Track total Hamiltonian, charge, vector J, emitted modes and the escaping mass spectrum. A fusion event is not automatically orbital cooling; determine which subsystem receives each energy change.
4. Demonstrate convergence of the **small orbital-energy difference**. For two equal masses at this relative speed, orbital kinetic/rest-energy ratio is approximately v_rel^2/(8c^2)=4.5e-10. ARGON11's reported global Hamiltonian drift around 1.55e-7 alone cannot certify that signal. Matched subtraction plus resolution/time-step convergence is required; global drift is not itself a strict lower bound on possible differential accuracy.
5. Use the measured differential collision/merger kernel in conservative formation/escape evolution. Close M, E, Q and vector J with no imposed sink; for the reference Sextans endpoint respect the 291,027-solar-mass escaping budget. Evolve the same microphysics in Draco, Fornax and Leo I, enforcing the stellar and finite-stock constraints. Reconcile the newer Sextans population likelihood before interpreting a catalogue-target success as observational closure.

This packet launches no PDE job, duplicates no Claude experiment, changes no frozen criteria or publication, and leaves the shared CE-FM-093 checkpoint intact. It supplies a quantitative failed thermal branch and the thresholds the next physical mechanism must beat.
