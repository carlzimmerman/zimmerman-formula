# Claude handoff — CCT015: actual collapse and inner transport, no four-dwarf closure

Read cold_fourth_flux_2026_10_25/RESULT.md first, then MECHANISM.md and analysis.json. This supersedes the next-experiment suggestions in the earlier dynamic-phase handoff, not its frozen failures.

**Answer so far:** a conditional collisionless coherent field really concentrates mass and transfers energy to the inner envelope. In Draco, radial/time refinement and a separate angular check give ~203million Msun inside r=Rstar at T8, vs the prior conditional11.6million reference. Sextans has~185million vs8.6million. The shared incoming family already over-supports Fornax/Leo under the instantaneous stellar screen. This is not the selective low-spin remnant mechanism we need.

**Actual transport:** D T0..8 has positive energy transfer through2/4Rstar, but NET SPIN AND MASS FLOW INWARD there. A resolved short T8..8.5 replay shows outward mass at2Rstar with NEGATIVE energy and inward net spin. Weak outer energy flux is below its error. No escaped-energy/remnant/stellar-survival certificate.

**What now works:** origin-safe combined radial+angular kinetic CN, static phase factoring, full square angular point field, one symmetric Poisson source, correct half global self-energy and canonical surface correction. Signed finite radial CN mass transport closes to<1e-10 in actual runs. No projected-material overcount, auxiliary tag energy or duplicate cold/Xi force.

**What failed:** radial/angular kinetic splitting passes norm yet fails analytic/galaxy energy checks. Later ne256 nt32 nf32 runs fail Jz by>5% (D10.2, S8.7); ne128 nt32 nf64 has better spin but insufficient late local-energy budgets. Coarse F/Leo runs stop on angular bandwidth. Preserve those failures; do not call a completed/capped process a physical pass. The independent alias counterexample proves the ell-tail alone misses torque errors.

**Next executable check:** use galaxy_v3.py or late.py with ne256 nt32 nf64 (same physical input, eta and supply), bounded240s segments and measured memory preflight (<1GB). continue.py resumes an identical geometry/dt from a named runs checkpoint; pulse.py does the same with physical flux each timestep and has been exercised on draco_v2_256 -> draco_pulse_T8_85. Inspect RSS headroom before increasing simultaneous radial/angle counts; the stronger combined grid has NOT been run in this packet. Do not use the failed nf32 late state as a clean physical seed. Compare shell budgets to transported signal and repeat the outer box before interpreting escape. Eventually measure stable retained profiles and evolve stellar cohorts in the same moving field.

**Physical selector still missing:** common saved supply=5.364*200*formed stellar mass requires retention D3.15%, S46.74%, F0.141%, Leo0.296% for the old conditional total profiles. The ~330x S/F retention contrast is a requirement, not a derived mechanism. Constrain supply/assembly/stellar timing independently before trying per-galaxy cuts. Sextans survey/anisotropy dependence and the illustrative nature of other total profile masses remain in force.

Scope: CCT Schrödinger-Poisson coherent-field candidate, NOT an action-level derivation of current Khronon/AeST v3. Owner main at87267ee9d9 reports X40b cluster-core scaling unresolved; shared CURRENT and the original Claude handoff are stale different contexts, not new evidence for this candidate. No SCT-M result is transferred, no owner/frozen/publication files changed, no automation created, no other chat messaged.

All new evidence and exact source/input hashes are under cold_fourth_flux_2026_10_25, including preserved negative controls, raw fields/history, audits and review. Full theory completion remains open.
