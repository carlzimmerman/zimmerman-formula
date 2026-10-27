# CFG777 FROZEN CRITERIA: the frozen relic (H-FR) in groups and clusters

Committed alone, before any script or number, and before CFG776's result is read. 2026-10-14. Block CFG770–779.

## Seen before freezing (disclosed)
- **CFG721.** The condensed-source tethered profile with CFG652's placement fails eRASS1 (MID 1.32 / OUTER 1.27), ACCEPT
  (×2 overshoot) and eFEDS (p 0.003–0.004). A post-hoc BCG placement fits eRASS1 MID 0.94 / OUTER 1.07 but overshoots the
  inner band ×3.
- **CFG687.** eRASS1 core excess ×1.8 at 7σ over the plain law; outer on the law, 1.01 ± 0.09.
- CFG776's criteria and hand estimate.

So the eRASS1 numbers are seen; this lane is a forward test of a fixed rule, not a discovery.

## Rule (H-FR, no new constant)
- The tethered cold-energy profile is the law's profile of the **peak** condensed mass p·M_cond. Present-day baryons set the
  potential.
- Clusters' relaxation clock: t0 = √(r_M/a0) ≈ 0.3–0.6 Gyr for 10¹³–10¹⁵ M☉. That is ≲ 30–40 t0 over 10 Gyr, earlier than
  CFG747/776's onset of expulsion. **The relic is frozen (taken as full, f = 1)**; CFG776's D1 tables are quoted, not
  re-run.
- **p from data (declared):** the member galaxies' gas fraction at their quenching epoch, from the same Tacconi+18
  main-sequence scaling as CFG776 (z_q = 1.5, log M* = 10.8; coefficients PROVISIONAL from memory). p = (1 + μ)/0.9.
  Brackets p ∈ {1.5, 2, 3}.
- Catchment and supply are computed from the peak condensed mass (CFG652 rule: max(p M_c/0.10, (M_c + M_hot)/0.90)).
- The rest of the supply is free, placed by CFG637 Method A (as in CFG721).
- Condensed placement: CFG652's own (half BCG Hernquist R_e = 15 kpc, half members Hernquist R_e = 0.5 R_X). This is
  CFG721's primary, so the only change from CFG721's condensed source is p.

## Targets (CFG721 harness and scoring, unchanged)
1. eRASS1 318: MID and OUTER band A within 2σ of 1 (jackknife).
2. ACCEPT 8: OUTER within 2σ.
3. eFEDS 131: χ² p ≥ 0.01.
4. SPARC guard: discs have p = 1, so there is no change by construction (reported).
Kernels ν_s (primary) and ν_mono. Both footings, never pooled.

## Verdict
- **PASS** if 1, 2 and 3 pass on at least one footing at the Tacconi p.
- **PARTIAL** if exactly two pass.
- **FAIL** otherwise.
- Brackets are reported with no verdict weight.

## MUTATE (CFG777_MUTATE=1)
- **M1:** p = 1 must reproduce CFG721's condensed-source numbers (eRASS1 band A within 0.01).
- **M2:** p shuffled per cluster (p_i drawn from {1.5, 3} at random, seed 777). The mean band A must change.

## Machine
- Run only after the CFG650 T1x 1024³ job has finished (no cfg650_pm.py process).
- 1 process, ≤ 1.5 GB, nice -n 10.
- Expected ~2–3 h (eRASS1 stage).

## Hand estimate (before any script)
- In the deep regime the tethered phantom scales as √p. At p ≈ 1.9 it is ×1.37 over CFG721's condensed source.
- CFG721 cond was already *above* the data in eRASS1 (MID 1.32 means obs/model is 1.32, i.e. the model is low). ×1.37 on the
  phantom part may bring MID toward 1.
- ACCEPT, which CFG721 overshot ×2, would get worse.
- Expected: PARTIAL (eRASS1 helped, ACCEPT worse, eFEDS uncertain).

κ fitted; cold energy mass required; not theory closed.
