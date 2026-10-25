# CCT-010: moving cold wells and stellar cohorts

The recorded escape-pulse history still fails to make the conditional Draco/Sextans profiles. Following the moving cold structure removes much of the earlier fixed-origin stellar-excitation interpretation, but does not restore the missing central mass. This is a finite diagnostic of the selectively coupled CCT wave candidate, not a result for literal v3/AeST/Khronon or SCT-M, and not proof that nature contains a nonparticle cold field.

## What was actually advanced

Resumed the exact CCT-009 source-free fields at code t120 to t130, with eta1500 pc km/s and the same radial/angular grids and dt. Added local potential-well tracking, radius-one cold-aperture centroids, wave-current momentum, orbital subtraction from angular momentum, and full nonspherical potential histories. Evolved 128 passive stellar probes per galaxy in inertial coordinates, initialized around the cold aperture with its mean current velocity. Compared evolving cold fields with a rigidly advected copy of the initial field. The original static-field control is retained separately for Draco.

| Diagnostic | Draco | Sextans |
|---|---:|---:|
| New physical interval | 12.40 Myr | 52.96 Myr |
| Cold aperture mass, initially | 4.14 million Msun | 6.41 million Msun |
| Cold aperture mass, finally | 2.41 million Msun | 5.40 million Msun |
| Cold mass within Rstar about final **stellar** COM | 1.98 million Msun | 5.42 million Msun |
| Conditional reference mass within Rstar | 11.62 million Msun | 8.62 million Msun |
| Final stellar r50 / advected-control r50 | 1.0333 | 0.9624 |
| Final stellar 1D rms speed / control | 0.9882 | 1.0352 |
| Stellar-to-tracked-cold COM separation | 136.4 pc | 26.8 pc |

The moving aperture is a radius-Rstar Eulerian selection recentered by a smooth local centroid iteration seeded by the nearest potential well. Its decline is loss from that selection, not a measured escape fraction from a tagged material fragment. The last stellar-centered mass uses the analytic finite-harmonic angular-cap integral, not the coarse aperture quadrature. Reference profiles remain conditional: Draco's total-mass reference came from an illustrative global moment fit; Sextans' from the previous actual-position survey fit. Neither is an observed total cold-mass inventory.

Draco's final **spherical equilibrium diagnostic about the evolved stellar centre** gives sigma=7.131 km/s versus the catalogued 9.55 km/s. This is separate from the dynamically evolved probes' rms velocity, which is not an observational velocity-DF fit. Sextans' analogous canonical isotropic actual-position survey diagnostic remains worse than the previous reference by 2 Delta NLL=63.627. No significance calibration or posterior claim follows from that number. Thus centre motion does not rescue this history's central/profile deficit.

## Pattern, material flow and spin

For the field psi, rho=|psi|² and j=eta Im(psi* grad psi). In an aperture B around c, record M_B, P_B=integral_B j, and J_int=integral_B x cross j - C_B cross P_B. Subtracting orbital angular momentum is essential for the off-axis Draco wells. A potential minimum or density pattern need not travel at P_B/M_B.

Draco's aperture centroid moves109pc during the interval. Its median centroid-pattern versus local mean-current speed difference is6.38km/s. It remains inappropriate to identify this moving selection with a single conserved material core. Pi symmetry gives a second Draco well; following one does not assign the whole cloud to one observed galaxy. Exact membership, binding and the changing wave interference must still be resolved. Intrinsic-spin values are saved, but initial Draco aperture-mass quadrature changes4.64% on angular doubling and the small orbital-subtracted spin is more sensitive; no converged intrinsic-spin percentage is claimed.

A separate, repeated cold evolution measures the absorber's Pz change before/after every sink step. It reproduces the tracking evolution's final field exactly for Draco and within4.81e-15 relative norm for Sextans. After accounting for the sink, the finite wave-current Pz residual is +14.87%/-8.02% of the small initial net Pz, equivalent to whole-remnant bulk speeds +0.0487/-0.0202km/s. This is small compared with Draco's6.38km/s pattern/current discrepancy, but **linear-momentum/recoil conservation has not been verified**. The spherical finite basis lacks exact translation symmetry and the diagnostic radial derivative is approximate. Do not reinterpret good M/E/Jz ledgers as a passed recoil test.

## Stellar interpretation and gravity bookkeeping

Stars feel the full saved nonspherical cold potential, not a fixed-origin monopole. Their rigid baryonic background follows their COM and contributes the canonical spherical baryon law once. The cold mass is one Poisson source; no second cold enhancement, separate spin gravity, or radiation-mass source is added. The cold field remains the prior source-free pre-stellar solution: this is a passive response assay, with no stellar backreaction on it. It is not a complete coupled late-time solution.

Both dt=.02 and .01 were run for the evolving and advected controls. Final r50 changes by at most6.9e-7 relative for Draco and2.44e-5 for Sextans. The full multipole force agrees with finite differences to8.32e-10 in code units. The new response is modest over these intervals; the old fixed-origin result cannot be presented as actual heating of stars riding a moving core. These circular cohorts are not the real stellar DF, the baryonic/Xi source is rigid and spherical, there is no host, and there is no demonstration of survival over a galaxy's lifetime. Reversible breathing is not irreversible heating.

## Four-dwarf status and executable next obligation

**No four-dwarf formation/survival pass.** The matched escape-pulse Fornax/Leo I production controls remain unrun; earlier bound-history overboosts do not establish their outcome for this pulse. A postulated envelope or a successful stationary endpoint cannot be substituted for those controls. The tested Draco/Sextans history already misses its conditional mass/profile targets, so the requested conjunction fails for this recorded history without declaring any universal exclusion.

Next discriminate a material remnant from a pattern: use a translating/adaptive domain or Cartesian field solver with a validated linear-momentum and absorber-recoil ledger, track the two Draco fragments without enforcing that their stars share a potential minimum, and include live stellar backreaction from the same action. Require radial/angular/boundary convergence of retained mass, current and binding before extending stellar evolution. Then run one paid assembly prescription on **all four** galaxies: mass supply, total energy and angular spectrum must be specified independently of the desired dwarf outcome. Changing the radial pulse to capture more mass is a new history requiring new Fornax/Leo controls, not a repaired prediction.

Numerical M/E/Jz ledgers remain below1% (energy residual6.30e-5/1.61e-4 relative to the original ledger scale), with prior convergence caveats unchanged. Reported producer RSS at its final diagnostic is820/764MB for tracking and125/160MB for the momentum repeats; the late serialization peak was not separately sampled. The audit reruns verification only, not these dynamics. Raw runs pin their sources and parent fields before/after. The audit preflight first required bit-identical repeats; Sextans differed only at4.81e-15 and the explicit comparison tolerance is now1e-12. That is a numerical reproducibility tolerance, not a relaxed physics gate.

All results, failed implications, sources and commands are local in this new packet. Earlier audited packets, publications and frozen criteria are unchanged. No automation, other chats or remote repository writes were made. A read-only git snapshot reached ab4a3a8e1a; its scientific claims were not re-audited here and provide no bridge to CCT.
