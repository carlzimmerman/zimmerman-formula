# AX1 / v3s: reading PASS on G1–G4 at galaxy and Solar-System scope, both footings. Clean label UNDECIDED: it inherits C6's failed check C2 (float cancellation)

**Regraded under the owner's 11-04 lift** of the v3s freeze. This test adopts nothing. **The 10-24 verdict stands until the owner says otherwise**: v3s passes as a galaxy-scale law and fails as gravity plus cosmology (clusters, growth/CMB, radiation era, hosted dwarfs, Milky Way disc). Those failures are out of this lane's scope and stay open. The cold sector stays retired; nothing here reinstates it.

Criteria `FROZEN_CRITERIA.md` (alone, before this run) + `../common/FROZEN_CRITERIA.md` (fd417eea04). Engine `../common/ax1_engine.py`. Outputs `ax1_v3s.{json,out}`, byte-identical rerun (SHA-256 039de3bd…), twin `ax1_v3s_MUTATE.*` (K1, K2 fail, exit 1). Seconds. **Not blind**: every input is on record. κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

| gate | canonical | alt | source |
|---|---|---|---|
| G1 SPARC | identity: AQUAL with the law's μ outside L★ (P4 rms 0.054 / 0.054) | same | E2, P4 |
| G2a Cassini Q2 | P: all 24 cells, max Q2 1.9e-34 s⁻², margin ≥ 4.8e7 (Hees), ≥ 2.8e7 (Park) | P | C6 (read) |
| G2b planets | hedgehog GM/L★²: Mars 0.173, Saturn 0.035, Earth 0.028 of bound at 24 pc; 0.012 / 0.002 / 0.002 at 90 pc. **V1 reproduces C6's Mars 0.173 to 9e-4** | same (a0-free) | recomputed |
| G2c PPN | P: α1 = α2 = 0 at β = 0, γ = 1 | P | X15, A22 |
| G3 lensing | P at S4's μ_K bound | P | 10-24 record |
| G4 GW, health | P: c_T = c, Δv/c ≤ 6e-32; conditionally healthy (C5); switched stiffness well-posed (X3). Caustics generic (X14): a structural gap, reported | P | C8, C5, X3, X14 |
| G5 | a0 = c²√(Λ/32π) with κ fitted: by hand | | |

**Label.** The engine's rule gives PASS on both footings. C6's frozen verdict is UNDECIDED, because its check C2 failed on float cancellation (3.8e-11 against 1e-12; the identity is exact in sympy). Under the frozen rule that failure is carried, so the clean label here is **UNDECIDED, reading PASS**. Nothing new is computed for Q2: G2a rests on C6 alone.

## Reading
- v3s is the only class in AX1 that passes G1–G4 with the law's own interpolation on both footings. It does so with a new length, L★ (21.7–90 pc), that screens each mass. Every unscreened class fails G2 (see `../README.md`).
- This reproduces the 10-24 galaxy-scale verdict. It does not touch the 10-24 failures, which sit outside G1–G4.
