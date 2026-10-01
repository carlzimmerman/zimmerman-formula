# CFG255 — independent re-run (calculations chat, 2026-09-30): REPRODUCES BYTE FOR BYTE

> Requested by the orchestrator ("an independent re-run of cfg255_zsplit.py from the committed state: STAGE=A, STAGE=B, STAGE=B MUTATE=1"). This is a REPRODUCTION record; it adds no result and changes none. The lane's verdict (NOT POSSIBLE; NON-DISCRIMINATING by its own MUTATE) is the orchestrator's README. New files only; no existing file of the lane was edited.

## 1. The re-run of the committed script
- Script `cfg255_zsplit.py`, sha256 `a6b9b9040b4abb8eeb3bc06660a7340bcca41bc99d730e48bd6d95f94273a6b3` (last changed in 2fa69fcd1, the stage-A commit, before stage B was run).
- Run in a scratch mirror of the COMMITTED tree (`git archive HEAD campaign_fresh_gravity hunt_2026`, with `real_research/` linked for the on-disk data), so the lane's own outputs were never overwritten. Three runs in parallel under `nice`, about 105 s each.
- Mirror note for anyone repeating this: the lane-prefix chain (CFG61 → CFG36 → CFG35) reads `hunt_2026/h10_h18_xray_hse.py` at the repo root, so a mirror of `campaign_fresh_gravity/` alone fails with a FileNotFoundError (my first attempt did).

| run | exit | results JSON vs the committed one | `.out` vs the committed one |
|---|---|---|---|
| `STAGE=A` | 0 (8/8) | BYTE-IDENTICAL, sha256 `f0e58b4c250c2e69…` | identical except the wall-clock seconds |
| `STAGE=B` | 0 (11/11) | BYTE-IDENTICAL, sha256 `a64b9eab6c129dda…` | identical except the wall-clock seconds |
| `STAGE=B MUTATE=1` | 1 (11/12) | BYTE-IDENTICAL, sha256 `85594a254de35808…` | identical except the wall-clock seconds |

The exit code 1 of the MUTATE run is the lane's own: its MUTATE CONTROL check FAILS (p_FLAT 0.098 canonical / 0.097 alt with the rival's ratio injected), which is a load-bearing failure by design. Stage A: power 0.14 / 0.17, ΔA +0.0179 against σ_A 0.0383, POSSIBLE_STAT and POSSIBLE_SYS false at δ = 0 / 0.02 / 0.05 dex; stage B: A_data +0.0595 ± 0.0383, χ² (14 dof) 19.8 (zero, FLAT) / 19.2 (rival) / 15.1 (ΛCDM proxy), all p > 0.1.

## 2. A fresh re-implementation (`cfg255_rerun_xcheck.py`; shares no code with the lane's script)
A byte-identical re-run proves determinism, not correctness, so the measurement side was re-written from the on-disk arrays (`cfg110_perlens.npz`, `lr_lenses.npz`, the 50 patch labels) and compared with the lane's committed JSONs:
- X1: the class photo-z cuts equal stage A's recorded quantiles (1e-12).
- X2: per-class and combined A_data equal stage B's, to 7e-16.
- X3: the per-class and combined jackknife σ equal the recorded ones, to 8e-15 relative. Re-forming the pair weights inside every leave-one-out moves σ_A by −1.7e-4 relative, so that choice is immaterial.
- X4: the ANALYTIC deep-limit rival (a₀ ∝ E(z): Δlog g_obs = ½ log₁₀[E(z_hi)/E(z_lo)] at fixed g_bar) at the thirds' median / mean z gives +0.0187 / +0.0204 dex against the lane's A_RIVAL +0.0188. This checks the lane's full profile machinery against the one-line law.
- X5: the analytic power (ΔA/σ_A)² × Hartlap = 0.151, against the lane's GLS 0.14 / 0.17.
- X4 and X5 are plausibility bands fixed after the first print of the numbers (0.004 dex; [0.10, 0.25]); they are not a pre-registered test.
- 5/5 pass. MUTATE=1 (high and low thirds swapped) makes X2 fail, and MUTATE=2 (patch labels permuted) makes X3 fail; both bite as designed. The first two MUTATE runs crashed in the final bookkeeping (a KeyError: the check results were keyed by the long names) after printing the failing checks, and are kept as `*_firstrun.out`.

## 3. One transcription nit in the lane's README (no number in any JSON is affected)
The README's bottom line says the lever is "median z 0.21 against 0.39 (late)". The lane's own C2 output (and mine) gives the late-class medians 0.2045 and 0.3996, i.e. 0.20 against 0.40; the early class (0.2318 and 0.3785, "0.23 against 0.38") is right. With the late medians the analytic late-class rival shift is +0.0237 dex (early +0.0178); the combined +0.018 dex quoted in the README is unchanged.

## Limits
Same data, same estimator family: this confirms that the committed numbers are what the committed code computes from the on-disk sums, and that the amplitude, its jackknife error and the rival's deep-limit shift are right by an independent route. It does not touch the lane's stated wall (a stellar-mass calibration drift between z ≈ 0.2 and 0.4 mimics an a₀ drift by δ/2), and it uses the lane's own thirds, so it says nothing about other splits.
