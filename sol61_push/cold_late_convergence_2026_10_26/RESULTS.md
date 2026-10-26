# CCT022: later collapse, independent refinement and the remaining mass excess

The later original-history 8192 runs retain their numerical gates through 371.917 Myr for Draco and 426.927 Myr for Sextans, but neither reaches a registered settling window or inserts stars. The inner mass does not undergo a sustained large decline over these segments. This is a failure to demonstrate settlement within attained coverage, not a universal no-go. Local temporal agreement, spatial agreement on an attained early interval and later full-wave convergence are different claims.

## Later 8192 segments

| Quantity | Draco | Sextans |
|---|---:|---:|
| Original accepted start T | 3.1083134213 | 3.3798744551 |
| Final T | 3.8718877901 | 4.6003964104 |
| Final elapsed collapse time, Myr | 371.917 | 426.927 |
| Start cold mass inside reference sphere, Msun | 1.42227e8 | 1.29256e8 |
| End reference-sphere cold mass, Msun | 1.39545e8 | 1.30067e8 |
| Segment fractional change | -0.0188588 | +0.00627625 |
| Sampled minimum reference mass, Msun | 1.28535e8 | 1.19588e8 |
| Sampled maximum reference mass, Msun | 1.42227e8 | 1.33486e8 |
| Final registered window T | 3.85 | 4.60 |
| CDF range / total; limit 0.01 | 0.191462 | 0.152312 |
| Reference mass relative range; limit 0.05 | 0.123314 | 0.109366 |
| Half-mass radius relative range; limit 0.05 | 0.561948 | 0.338416 |
| Maximum relative mass error | 2.57467e-11 | 8.73814e-11 |
| Maximum energy residual / original scale | 3.24880e-6 | 3.24594e-6 |
| Maximum residual-phase occupancy; limit 0.05 | 0.0371116 | 0.0490353 |
| Peak measured RSS, bytes | 115081216 | 115752960 |

Both stop at their declared 1800-second budgets, not a numerical gate, before absolute T=8. Sextans is close to the phase-occupancy limit; do not extend past a future failure or reset its cumulative maximum. Reference-mass extrema are sampled at the saved history cadence, not bounds on continuous extrema. Whole-field conservation holds while cold material redistributes inside the box; this does not demonstrate escape. Boundary occupation is negligible. Retention inside this box does not establish gravitational or tidal retention by the actual dwarf.

The registered one-unit quiet interval still fails all three conditions in both dwarfs. Lower CDF ranges than in CCT021 are finite progress in the diagnostic, not qualification or a justified extrapolation to settlement. Birth times and stellar-validity flags remain null. No actual stellar-survival test or real first-star deadline is met by postponing insertion.

## Local temporal refinement

All six fixed-grid cases finish delta T=0.02 from the same accepted CCT021 late states. Halving h from 1e-4 to 5e-5 to 2.5e-5 reduces unrotated wave differences by factors 14.587 (Draco) and 15.104 (Sextans), with observed local orders 3.867 and 3.917. The smaller pair's CDF differences are 2.570e-7 and 1.004e-7. Global phase alignment does not remove the discrepancy and never rescales amplitude. Final energies and additional parent/grid/carrier/source checks are independently reconstructed in `diagnostics_001` from immutable raw fields.

These are local same-grid tests over about 1.9 Myr. Local energy changes are nonmonotone and can be affected by finite nonlinear-solve residuals; no monotone energy-error order is claimed. They do not establish full-history temporal error, independent spatial convergence or the later dynamics. The complete reports retain original residuals and attained horizons.

## Failed late transfer, explained without accepting it

Unrenormalized 8192-to-16384 interpolation changes discrete mass by 4.90976e-4 (Draco) and 6.78953e-4 (Sextans), above the unchanged 1e-8 gate. Both candidates remain ineligible. They are not evolved as alternative physical remnants.

Independent 8/16/32-point Gauss integrals agree within 2e-16 for each old cubic interpolant. The leading constant-J Lobatto defect predicts the old-minus-nested norm discrepancy to mapped-J corrections of -8.306e-9 and -1.693e-8. This identifies a discrete mass-quadrature effect, not physical mass loss. `MASS_METRIC.md` derives the coefficient and limitations. It supplies no bound on local force or future wave error and does not justify normalization or a changed criterion.

The independent 16384 runs start from the analytic initial conditions. Their actual intervals, shared-time comparisons and final data diagnostics are documented in `SPATIAL_RESULTS.md`; early agreement must not be promoted into late convergence. `CONSISTENT_METRIC_NEXT.md` gives an unimplemented consistent-quadrature method specification for a separate benchmark, with no change to the present producers.

## Galaxy-data and mechanism scope

The final complete-profile analysis retains every saved state, both prescribed acceleration footings, beta=-.5/0, separate Sextans tracer components, held-out Draco PM and exact source/data hashes. Its final LOS table is in `SPATIAL_RESULTS.md`. These are fixed-tracer support diagnostics, not velocities of evolved stars or formal likelihood significances. The mass/energy history and field-level convergence failures remain visible even where instantaneous moments agree across grids.

The original-history Fornax/Leo I controls remain those reconciled in CCT021: finer old T=1.25 projections 52.842/41.710 km/s versus selected-data 12.136/9.030 km/s. Different finite gauge/time/mesh choices and weak late-wave agreement prevent claiming matched converged late controls. No new F/L trajectories or four-dwarf success are claimed, and the separate vin/V=0.8 branch is not substituted.

This remains the spherical conservative CCT complex-wave proxy with fixed supported baryons and passive later stars, not a literal v3s/Khronon/AeST action, retired SCT-M result or established new substance. Cold gravity enters once. Reciprocal source coupling, a measured cold supply, cosmological collapse-start/first-star chronology, live gas/star formation, nonspherical spin transport and escaping energy at infinity remain unresolved. Finite outer energy inventories are not radiation to infinity; the prior density-fluctuation binding correction still applies.

`related_001` verifies raw hashes and late-window CSV pressure of the different real-scalar study at 15b4863c1f. Its supplied-energy periodic boxes cover only 27–82 days and retain substantial positive pressure in dense cases. No cold supply, dwarf assembly or action bridge is imported from that result. This was an artifact reconciliation, not a rerun of those experiments.

## Evidence and next steps

Read `SPATIAL_RESULTS.md`, `VALIDATION.json`, the canonical `analysis_001` and `audit_001` records, and `REVIEW.md` for final coverage and checks. Producer completion denotes a completed bounded execution, not physical success. `NEXT.md` and `RESUME_PREPARATION_CHECK.json` distinguish accepted wall checkpoints from unsupported restarts. No future job, monitor or other-chat message is scheduled by this packet; no old frozen source, criterion or publication was changed.
