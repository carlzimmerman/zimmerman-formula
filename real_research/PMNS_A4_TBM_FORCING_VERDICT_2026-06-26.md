# FRONT 1 — Does discrete flavor (A4/S4/Δ27/A5) FORCE the MEASURED PMNS angles, and is the framework's triality the A4? — VERDICT

**Date:** 2026-06-26  **Status:** PARTIAL/NEGATIVE, both-ways verified, anti-circular (force the angle, don't input it).
**Scripts:** `real_research/pmns_a4_tbm_forcing_test.py` (mpmath dps=40).
**Data:** NuFIT 6.0 NO (th12=33.68, th23=48.5, th13=8.52, dCP~177) AND the prompt row (33.4/49/8.6/197). Conclusion identical.

## The genuinely-new finding vs the Koide work: the ANGLE is more forceable than the magnitude — but the forcing symmetry is EXCLUDED, and the real angles need TUNING.

### (a) Does A4 force EXACT TBM, and is that excluded by th13≠0? — YES forced, YES excluded.
- Unbroken A4 (Z3 charged-lepton residual × Klein-V4 neutrino residual) GROUP-FIXES the HPS tribimaximal matrix with **ZERO free parameters**: th12 = arcsin(1/√3) = **35.264°** (sin²=1/3), th23 = **45°**, th13 = **0** exactly.
- th13 = 0 is **EXCLUDED at ~65σ** (8.52 ± 0.13°; the 2012 Daya Bay/RENO reactor result). Exact TBM is dead.
- The SURVIVOR is th12: TBM 35.26° vs measured 33.4–33.7° is only **~2.2–2.7σ** — the solar angle is near-TBM. A5 golden-ratio gives th12 = 31.7° (GR1, 2.8σ) or 36.0° (GR2, 3.3σ), and **also** forces th13 = 0 → same exclusion.

### Does a breaking FORCE the measured angles, or is the deviation a TUNED VEV-misalignment? — FORCES one SUM RULE, the rest TUNED.
- The strongest forced content is a **sum rule**, not 4 values. **TM2** (S4→Z2 residual, preserve TBM middle column): sin²th12 = (1/3)/(1−sin²th13) → th12 = **35.72°** given the measured th13, **~2.9σ** off, with NO free th12 parameter. That is a real symmetry-forced relation th12(th13).
- "th13 ~ θ_C/√2" (Cabibbo haze) gives 9.13° — right ORDER, ~4.7σ off in value; the coefficient (1/√2 vs 1) is which-residual-dependent.
- Net count: generic PMNS has 4 physical params; realistic A4/S4/Δ27 + flavon models FORCE **1 sum rule** (a 1–2 param reduction) and leave th13's value, th23's octant, and dCP as **free VEV-alignment parameters — TUNED, by the model-builders' own count.** They do NOT force the 4 measured values.

### (b) THE KEY ASYMMETRY vs Koide — the angle IS genuinely symmetry-forceable where the magnitude wasn't.
- **Koide magnitude:** Q = 1/3 + r²/6 (phase-independent, sympy-exact). For ANY group in the A4/S4/Δ27/A5 chain the amplitude **r stays a FREE real modulus** (the framework's whole closed mass-sector result). The obstruction is a **covariance no-go** — no Gibbs/character measure of any Hamiltonian outputs the non-covariant p=0 weight (KOIDE_CHANNEL_MEASURE).
- **PMNS angle:** TBM fixes ALL 4 mixing params with **0 free reals** — because a mixing angle is a **VACUUM DIRECTION** (the relative misalignment of charged-lepton vs neutrino mass-basis), exactly the kind of object a discrete symmetry CAN pin via residual generators. So Carl's distinction is **CORRECT and confirmed**: the angle is the more forceable object; there is no covariance no-go for it.
- **BUT the obstruction here is EMPIRICAL, not structural:** the symmetry that fully fixes the angle (exact A4/A5) predicts th13 = 0, which is excluded at 65σ. The real angles require *breaking*, and breaking re-introduces free VEV-misalignment parameters. So: forceable-in-principle, but the exact forced pattern is falsified and the measured pattern is tuned. This is a *different and weaker* wall than Koide's — empirical exclusion of the clean case, not a theorem against forcing.

### (c) Does the framework's Spin(8)-triality / J3(O) supply the A4, or is the flavor sector disjoint (Coleman-Mandula)? — DISJOINT.
- The Spin(8) triality group is the **outer-automorphism group = S3 (order 6)** (verified: D4's three-fold Dynkin symmetry → Out = S3). The family symmetries that force TBM are **A4 (order 12), S4 (order 24), Δ27 (order 27), A5 (order 60)** — all LARGER than S3.
- **S3 is not even a subgroup of A4** (the classic "A4 has no order-6 subgroup" counterexample to the converse of Lagrange), so triality-S3 cannot be a residual of an A4 family group. S3 ⊂ S4 and ⊂ A5 abstractly, but the framework only supplies the order-6 triality, not the order-24/60 parent.
- **Coleman-Mandula is decisive regardless of subgroup containment:** the triality S3 is the outer automorphism of the *spacetime/gauge* structure (the dS-horizon character is of the spacetime isometry SO(d+1,1), already used in the channel-measure no-go). Internal-symmetry generators must commute with Poincaré → be a DIRECT PRODUCT with it. The family group acting on flavor space is an *internal* symmetry; the gauge-home triality is a spacetime outer automorphism. They cannot be identified. The flavor sector is **disjoint from the gauge home** — same severance that killed the channel-measure route (the bath is blind to the internal family irrep).

## Both-ways ledger
- **CREDITED (no high-priest):** the mixing ANGLE is genuinely more symmetry-forceable than the Koide magnitude (TBM fixes 4 params with 0 free reals — Carl's instinct right); TM2 is a real symmetry-forced th12(th13) sum rule landing within ~3σ; A4/S4 land the right *neighborhood*; th12 ≈ TBM (~2σ).
- **REFUSED to manufacture:** exact TBM is dead at 65σ (th13≠0); the measured angles need free VEV-misalignment (tuned, not forced); the framework's triality is order-6 S3, too small to be the A4/S4/A5 parent and barred by Coleman-Mandula from acting as the internal family group anyway. NO framework number forces the PMNS angles.

## Bottom line
Discrete flavor FORCES the exact TBM pattern (which th13≠0 EXCLUDES at 65σ) and, after breaking, forces at most ONE sum rule — the measured angles are otherwise TUNED VEV-misalignments. The mixing angle IS more forceable in principle than the Koide magnitude (vacuum direction vs covariance no-go), so Carl's distinction holds — but the framework's Spin(8)-triality is the order-6 S3 outer automorphism, NOT the A4/S4/A5 family group, and Coleman-Mandula keeps the flavor sector disjoint from the gauge home. The framework supplies neither the A4 nor the measured PMNS angles. Quarantine held; no manufactured win, no manufactured deficit.
