# CFG376 FROZEN CRITERIA: CFG374 MIX-A with the collapsed phase split into hot halo gas (filtered) and stars + cold gas (unfiltered)
(committed before any script)

**Why.** CFG374 (MIX-A, Shull, Smith & Danforth 2012 census) is TENSION: σ₈ ×1.015 / ×1.019, but P(k = 1) +12% / +16%. Its criteria left the whole collapsed 18% UNFILTERED. Most collapsed-phase baryons in groups and clusters are hot, pressure-supported halo gas (CGM / ICM). Only stars and cold neutral gas are dense enough to trace the collisionless field at k ≲ 1 h/Mpc.

**The filter.** As CFG374, with the collapsed phase split in two:
- W(k) = f_cool / (1 + k²/k_J(1e4 K)²) + f_hot / (1 + k²/k_J(1e6 K)²) + f_halo / (1 + k²/k_J(T_halo)²) + f_sc × 1.
- k_J(T) as in CFG372 (comoving, √(1.5 Ω_m a) × 100 km/s / c_s, c_s = √(5kT/(3 μ m_p)), μ = 0.6).
- Everything else is CFG374's engine exactly (copied, not imported): RES rule, R_c = 3 Mpc/h, A0-FLAT, 256³, seed 359, 150 steps. The T1 switch, tidal tensor and cold share s_c read the unfiltered total field.

**Census (fractions of ALL baryons).**
- f_cool = 0.28, f_hot = 0.54: CFG374 MIX-A unchanged (Lyα forest 28%; WHIM 25% + the missing 29% read as WHIM).
- Collapsed total 0.18: Shull, Smith & Danforth 2012 (ApJ 759, 23; arXiv:1112.2706), 18 ± 4%. VERIFIED from the arXiv abstract, read this session.
- Stars + cold gas f_sc = 0.08, halo gas f_halo = 0.10. **NOT verified from a source I could read this session**: the sub-split is in the papers' tables, not their abstracts, and downloading the PDFs needs an owner go. Recalled values: Shull+2012 galaxies (stars) ~7%, cold neutral gas ~1.7%, CGM ~5%, ICM ~4%; Fukugita & Peebles 2004 (ApJ 616, 643) stars Ω ≈ 0.0027 and cold gas Ω ≈ 0.0007 (the values already used in hunt_2026/g06v_adversarial_external_field_refutation.py), i.e. ~6% + ~1.6% of Ω_b ≈ 0.045. **Declared bracket: f_sc ∈ [0.07, 0.09]**, central 0.08 is the one run. The bracket's effect on W is reported analytically (not run, no scan).
- Caveat declared now: part of Shull's CGM is cool (1e4–1e5 K) photoionised gas, not hot. Treating all 10% as hot is the optimistic direction for this lane.

**Halo-gas temperature. Two declared variants, no scan.**
- **HALO-A (PRIMARY): T_halo = 10^6.5 K.** Most collapsed hot-gas MASS sits in groups and clusters (ICM ~4%, group/massive-halo CGM); group virial temperatures are ~10^6.5–10^7 K. 10^6.5 is the low end of that range.
- **HALO-B (conservative): T_halo = 10^6 K.** The virial temperature of L* galaxy coronae; this equals moving the halo gas into the WHIM phase.

**Runs.** 2 variants × 2 footings (canonical a₀ = 9.3603e-11, alt 1.1312e-10, never pooled) = 4 runs, at most 2 processes × 2 FFT threads, niced. Work data go to ../_external_data/cfg376_work/. S0 = ../_external_data/cfg359_work/cfg359_S0_FLAT_canonical_N256.json, read-only.

**Decision.** CFG361's cuts verbatim, per footing, never pooled. Ratios to S0 at z = 0.
- GROWTH OK: |σ₈ ratio − 1| ≤ 5% AND max over k ≤ 1 h/Mpc of |P ratio − 1| ≤ 10%, on BOTH footings.
- TENSION: σ₈ shift in (5%, 20%], or P shift > 10% with σ₈ within 20%.
- FAIL: σ₈ shift > 20% on either footing.
- The lane verdict is set by HALO-A. HALO-B gets its own verdict.

**Also reported (not scored).** The CMB-lensing proxy as in cfg374_analysis.py (mean P ratio over k = 0.05–0.2 h/Mpc at z = 1, 0.5, 0); P ratio at k = 0.1 / 0.3 / 1; comparison with CFG374 MIX-A and CFG372 1e6 K.

**Controls (field/algebra level, as cfg374_checks.py).**
- C1a: the weights sum to 1 for each variant.
- C1b: W(0) = 1 for each variant.
- C1c: the limit T_halo → 0 (halo weight unfiltered) reproduces CFG374 MIX-A's W(k) exactly (max diff < 1e-12, all a).
- **MUTATE** (CFG376_MUTATE=1, separate outputs): all-unfiltered weights (f_sc = 1) must give W ≡ 1 to 1e-6, and must differ from HALO-A's W at k = 1, z = 0 by > 0.3 (the check sees the filter).

**Scope.** Linear, constant-temperature phase filters with z ≈ 0 fractions applied at all z, on a collisionless run; hydrodynamics, cooling and feedback are not simulated. The reservoir is bookkeeping and the settling force is conditional (CFG373). κ = ½ is fitted. No dark-matter particle: the cold fluid is still required.
