# CCT014: dynamic carrier errors separated from physical transport

The adaptive real radial carrier implements the time-dependent phase compensation correctly, and its free3D Gaussian test converges. Relative wave errors decrease .02345,.01131,.006594,.003026 at N16,24,32,48; the finest benchmark's physical energy drift is .240%. Omitting the compensation gives .2956 wave error at N32. The independent Godunov HJ quadratic error halves as the radial grid is refined257→513→1025. The original negative-control dtype failure and first pilot execution-order deviation are preserved in `BENCHMARK_FAILURE.md`; no benchmark pass is invented for that failed execution.

The actual incoming galaxy tests still do not reach a trustworthy remnant. Stopped endpoints:

| case | first sampled stop time | physical energy drift | accumulated absolute gauge defect |
|---|---:|---:|---:|
| Draco N64 |3.7|4.029%|4.029%|
| Draco N96 |4.0|4.484%|4.484%|
| Sextans N64 |3.4|3.163%|3.163%|
| Sextans N96 |3.5|3.203%|3.203%|
| Fornax N64 |2.2|.653%|.653%|
| Leo I N64 |3.2|2.445%|2.445%|

Every listed endpoint violates the5% residual-amplitude phase-occupancy gate. Fornax's smaller energy error does not resolve its phase. D/S and Leo also exceed the1% energy interpretation limit. The5% emergency-energy stop is not the acceptance threshold. The nearly equal physical drift and signed gauge jump show numerical change of representation, not energy transferred into a physical receiver. Diagnostics are sampled every five steps.

At the SAME Draco stage t3.0, accumulated absolute gauge defect is1.755% at N64 and1.448% at N96: refinement helps but remains above1%. Halving dt changes it to1.755%, and doubling reference radial resolution changes it to1.660%; neither closes the error. Matched radial cumulative mass differences are .008923 of inventory for N64/96,3.92e-6 for half dt, and .002641 for doubled reference resolution. Compatible global angular-momentum drift falls .283%→.092% under N64→96 at that stage, without establishing actual outward spin transport. These comparisons are numerical diagnostics, not physical capture predictions.

The short t.5,N64,dt.02 reconstructed physical wave differs from the old static frame by1.386e-4 relative L2 after a global phase alignment (new reference nr2049). This supports early agreement and does not validate late collapse. No stars evolve here; no new stellar-safety, final cold-mass retention or no-overboost verdict is available. The generic early focusing result in CCT012 remains the only resolved four-dwarf concentration comparison in this series.

Two additional controls isolate the accounting problem:

- An EXACT unitary discrete change of carrier, transforming both field and hopping Hamiltonian, changes the reconstructed wave by4.37e-16, tags by2.17e-19, and energy by2.22e-16. A change of reference alone cannot supply physical cooling. Exact covariance is not an improvement in physical resolution.
- Splitting a single coherent wave by a material fraction f adds eta²/8 int rho|grad f|²/[f(1-f)] if the auxiliary core/envelope kinetic energies are summed. This positive interface term is artificial receiver energy unless removed. Gravitational core–envelope cross energy must be counted once. The symbolic Fisher identity has residual0, the sampled gradient identity1.06e-18, and the finite-box cross-energy identity0; deliberately double-counting the cross term fails by .1479 code energy. This identifies a bookkeeping hazard for future receiver calculations, not an assertion that a production receiver used that error.

`ENERGY_AND_SPIN_TRANSPORT.md` gives the conditional CCT action, physical energy/current, gravitational stress, moving-boundary energy/angular-momentum fluxes, and tag-partition corrections. Exact instantaneous self-consistent polynomial Schrödinger/Poisson tests give zero local energy and momentum residuals and a symmetric stress. They validate finite examples/signs, not a galaxy solution or a relativistic/nonparticle completion.

Across both new packets:18 actual-field pilots/controls, maximum measured process RSS628,162,560 bytes, unchanged-source records and a bounded rerun/audit in `audit_001`. All tag subset and bond-continuity gates are checked in the audit. The original first HJ pilot and corrected benchmark briefly overlapped, contrary to the sequential plan; subsequent matrices were sequential. RSS is measured, not an enforced aggregate-memory certificate. Producer runtimes exclude final serialization; actual process caps apply only to the bounded audit. Independent read-only review found no blocker to archiving these as failed/limited numerical experiments.

What remains: a spatial discretization/patch refinement that resolves the total physical generator through collapse without appreciable gauge-energy defects, followed by measured outgoing energy and vector-spin flux, bound core/envelope/escaped mass budgets, and resolved stellar tests under one data-constrained four-dwarf prescription. Neither of the tested dynamic carriers supplies that mechanism. Do not reinterpret numerical gauge work as cooling, total closed-box mass as bound mass, or these CCT results as literal Khronon/AeST evidence.
