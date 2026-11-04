# CC10: quantum collisions, neutral cascades and resonance memory

The original weak-coupling cold-matter goal remains open. This directory contains executed computations, not only a continuation prompt. The specified late passive-resonance branch still fails its charged-relic requirement. The corrected early common-state evolution is a separate unfinished calculation; its abundance must not be spliced onto the old late endpoint.

The target is e=.003, mu=2e6 GeV and initial hidden/visible temperature ratio .02, using the matched **leading trajectory** gravity packet. The distinct finite local gravity packet is not substituted. The charged gate is 10% of rho_DM/s=.44e-9 GeV; at the pole it is Ycharged=5.680375574e-16. The photino pole mass in this packet is about 104.73 keV.

## Results that change the assessment

| Calculation | Executed result | Scope |
|---|---|---|
| Quantum collisions | Actual 25 physical scalar/Weyl groups, inverse processes, Bose/Pauli factors, massive neutral momenta and forces | Tree SSS/FFS network with current-projected light F/C/gaugino channels; finite momentum projection |
| Angular correction | Old global two-angle warm RHS errors are 30–40%; analytic segment integration agrees with independent quadrature/Jacobian controls | Supersedes coarse-angle warm histories as physical evidence |
| Corrected direct/averaged bridge | One full warm orbit: charged endpoint error 1.18e-6, U1 yield error 5.09e-8; action endpoint error 2.00e-5 | Exact-angle conditional restart; finite phase/action error remains |
| Four-state resonance memory | Evolving scalar momentum distribution gives Ycharged=1.72351e-13, versus 6.27471e-13 for the stationary control | Recorded slow orbit, specified late initial distribution and vacuum neutral widths |
| Most favorable future resonance cleanup | Yield floors 142.43 times the charged gate with vacuum widths; 37.97 times even with every fermionic exit blocked | Fixed production matrices, positive passive widths, retained mass envelope, factorized pairs and stated cosmological tail |
| Neutral terminal decays | S8_0 gauge lifetime 7.10557 ms; S3_0 10.9650 microseconds | Complete on-shell gauge-pair one-loop calculation in the specified model |
| Open warm vector decay | Four-singlet P→broken-vector pairs contributes 1.63–1.98% of the included SSS/FFS width trace; closed at the cold pole | Actual tree vertex and polarization/counting checks; full vector flow remains uncomputed |
| Conditional hard photinos | Mean propagation 302.73 / 80.78 Mpc; late-stage photino rest density 9.01e-8 of DM | Soft gaugino vertex is not certified on shell; this is a conditional source |

The former 83.84-times-DM **stable neutral rest-energy** estimate is intermediate storage, not final neutral overclosure: these terminal particles have loop-induced decays. The production calculation separately tracks the direct gauge-pair radiation branches. It is not a complete radiation ledger for the mixed hard nonabelian-gaugino/photino branches and their descendants.

The hard photino component is very hot and tiny under the late-stage normalization. It supplies no successful cold-matter source. The early-warm yield transplantation in `production/` is only a sensitivity normalization, not a completed common cosmological history.

## Corrected common-state work

`integration/initial_packet.py` fixes the declared FD-only initial condition with the common gas/field mass interpolation. `integration/action_exact_fast_v2.py` evolves every included population and the scalar action, using analytic angular integration and independently integrated FRW work. The initial exact run reached N=.0002999746 with positive occupations, the Pauli bound, increasing collision entropy and an independent energy-work residual of 5.45e-5. Its requested N=.01 was not reached within its individual job cap; the record is honestly failed, with a durable usable prefix. A subsequent prefix reached N=.0003492778 and identified nearly empty number-coordinate merit scaling as a numerical bottleneck.

`initial_solver/log_number.py` subsequently reduces the same fresh-state nonlinear solve from 19 to 6 iterations while retaining explicit vacancy coordinates, conservative physical residual checks and positive accepted states. Quarter-to-eighth timestep refinement changes the tested U1 yield by .232%. The full coupled-history continuation uses its separately checked API.

`integration/protocol_floor.py` addresses that specific bottleneck with an absolute residual floor for nearly empty **number** coordinates; tiny fermion vacancy coordinates retain their relative scheme. On the actual fresh checkpoint, changing that floor across 1e-14/1e-13/1e-12 gives bit-identical accepted populations, physical balance error 8.60e-17, positive bounds, increased entropy and local energy conservation. No accepted population is clipped. The separate `history/` continuation records the corrected common trajectory and its actual endpoint; consult its current status before quoting an early abundance.

The preferred comparison state is now `history/run_refine002/result.json`, at N=.0021690179772784167: Ycharged=3.03394306e-7, charged fraction .81003691 and maximum fermion occupation .52896. Reducing the later step cap changes charged yield by .0113%, U1 yield by 1.14% and action by .631%. However, the cumulative energy-work residual is 23.85% of the remaining orbital excitation and does not improve under that refinement. The retained orbit and action are therefore diagnostics pending a converged field/population integration, not precision cosmological predictions. The direct one-period check starts from the separately stored larger-step state.

The old `integration/run_warm*` and global-angle `run_action001` histories are numerical diagnostics. They do not establish a physical warm abundance or persistent fermion saturation. Exact angular evolution removes the old apparent soft-state saturation in the tested restart. `integration/run_action_exact001` is a corrected short common field/population step, not the whole cooling history.

## Interpretation boundaries

1. The late memory correction and its passive future bound close that specified resonance rescue. They do not exclude a different early history, additional pair losses, entropy dilution, correlated states or an active/nonlocal medium.
2. The common warm solver still uses diagonal representation/mass-group populations. In particular the four degenerate massive neutral singlets are **S1_1**, while S1_0 is the massless two-real-state modulus. `warm_coherence/` checks the matrix-population bridge. At two saved eight-phase frozen baths, its rigorous trace envelope for arbitrary positive semidefinite periodic parent states limits the total FFS/SSS charged-current correction to .5405%/.6396%. This is not a uniform bound along the new history or on omitted vector channels. Group labels must not substitute for actual basis indices and masses.
3. A complete cold history needs the corrected common populations, neutral coherence and memory, all retained hard momenta, occupied inverse reactions and loop decays in one state. The current fixed q<=80 warm grid is not a late hard-decay momentum grid.
4. The soft neutral-to-two-gaugino derivative vertex is not the complete on-shell three-point amplitude. Its triplet component has 15.3% gauge-parameter variation. The gauge-pair widths are a separate completed calculation.
5. Warm broken-vector 1-to-2 decays and inverse reactions, gauge/vector 2-to-2 channels, bound states, dynamically matched charged/dispersive selfenergies and the full on-shell gaugino current remain outside the completed common model.
6. These collision results do not remove the previously documented vacuum-normalization tuning or derive the observed dark-energy density. The local gravity window and a predictive dark-energy relation remain different claims.

## Evidence and continuation

- [Target contract](CONTRACT.md), [thermodynamic/action identities](THERMODYNAMIC_IDENTITY.md)
- [Quantum statistics](statistics/STATUS.md), [solver controls](integration_solver/STATUS.md)
- [Cascade and exact angular derivation](cascades/DERIVATION.md), [API and primary run handoff](cascades/HANDOFF.json)
- [Preferred memory kernel](memory/STATUS_V4.md), [passive future bound](post_memory/STATUS.md)
- [Gauge loop calculation](neutral_loop/DERIVATION.md), [conditional cosmic production](production/DERIVATION.md)
- [Warm neutral coherence](warm_coherence/STATUS.md), [open vector channel probe](vector_probe/STATUS.md)
- [Corrected common history](history/STATUS.md), [history precision review](independent_review/history_final/REVIEW.md)
- [Action/energy diagnostic](independent_review/energy_diagnostic/REVIEW.md)
- [Independent final review](independent_review/final/REVIEW.md)
- [Computation summary figure](figures/run002/summary.png), [PDF](figures/run002/summary.pdf)

Every scientific job has a bounded manifest with actual input/output hashes. Failed, timeout and superseded records remain visible; current primary artifacts and archived historical bytes have separate bindings. `VERIFICATION.json` is the aggregate integrity inventory when generated. Previous TP06/CT09 directories are retained unchanged. No commit or push is part of this continuation.
