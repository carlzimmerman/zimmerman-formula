# Spatial coverage and galaxy-data diagnostics

The independent 16384-element trajectories reproduce early collapse closely, but have not reached the later 8192-element collapse. This packet establishes early agreement and continued late non-settlement, not late spatial convergence.

| Independent original-IC run | Final T | Elapsed Myr | Accepted / rejected steps | Peak RSS, bytes |
|---|---:|---:|---:|---:|
| Draco | 1.0561699483 | 101.451 | 1628 / 459 | 158171136 |
| Sextans | 1.0040214281 | 93.175 | 1282 / 565 | 159137792 |

Both runs finished their declared 600-second wall budgets without a numerical gate failure. Mass errors remain below 1.8e-12 and energy residuals below 1.1e-8 of their own original scales. Neither reaches T=2, the first time eligible for a settling decision. Neither inserts stars. Sources, analytic initial conditions, physical parameters and gates match the declared original-IC route; no late interpolation or amplitude normalization is used.

Only T=0, 0.5 and 1 are shared saved times of the independent 8192/16384 trajectories. At T=1:

| Physical comparison | Draco | Sextans |
|---|---:|---:|
| Relative unaligned wave L2 difference | 1.0862342e-5 | 9.1042420e-6 |
| CDF sup difference / total | 0.0001313205 | 0.0001355758 |
| Canonical beta=0 support, 8192, km/s | 23.7429635 | 18.9047067 / 20.8197829 |
| Canonical beta=0 support, 16384, km/s | 23.7429760 | 18.9047094 / 20.8197893 |
| Selected-data constant dispersion, km/s | 9.7031361 | 8.8006414 |

Sextans entries are separate tracer components, not a fitted mixture. These fixed-tracer projections are support diagnostics, not evolved stellar velocities or a likelihood test. Maximum support changes under this early refinement are 1.245e-5 km/s for Draco and 6.452e-6 km/s for Sextans. Early overconcentration persists under refinement.

At T=0 the common-grid linear-interpolation wave comparison is 6.62e-8, and the nodal cumulative CDF comparison is 0.0001855944. These representation diagnostics are not a physical difference in analytic initial supply. Initial discrete total mass differs by about -1.89e-15, and original energy by about 9.1e-9 of the left original scale. Reference-sphere nodal quadrature also differs slightly. Every pair exposes its original mass/energy references and both grid sizes; no invariant reference is reset.

The later 8192 endpoints remain excessive:

| Endpoint diagnostic | Draco | Sextans |
|---|---:|---:|
| Elapsed Myr | 371.917 | 426.927 |
| Cold mass inside reference sphere, Msun | 139545035 | 130067043 |
| Cold half-mass radius, pc | 4254.927 | 6136.640 |
| Canonical beta=0 support, km/s | 31.578317 | 18.756375 / 19.519155 |
| Selected-data constant dispersion, km/s | 9.703136 | 8.800641 |

The main later segments change reference mass by -1.886% and +0.628%, respectively. Short dips rebound; they do not show sustained shedding of the excess. All three registered quiet-window conditions still fail. The reflecting domain and finite outer energy gains demonstrate redistribution only, not loss to infinity, nonspherical spin transport or tidal retention.

Legacy 4096/8192 comparisons remain distinct. Their last attained overlap has unaligned wave differences 0.9163 at Draco T=2.5 and 1.0166 at Sextans T=3, despite instantaneous canonical support agreement at roughly 2.65% and 0.2%. Such agreement of a smoothed observable does not establish convergence of later dynamics. Neither local time-step convergence nor favorable early snapshots repairs this gap.

The complete analysis covers 13 runs, 228 LOS rows, 104 Draco PM rows, 30 wave/lineage comparisons and 76 observable pair rows. Both prescribed gravity footings, beta=-0.5/0, separate Sextans tracers, source hashes and valid/invalid endpoints remain explicit in analysis_001/result.json. No new matched late Fornax/Leo I trajectories are claimed. Their existing original-history excesses remain failures, not accepted controls. There is no four-dwarf or pre-stellar settlement success in this packet.
