# CFG255 — the KiDS-1000 lensing RAR split by lens redshift: NOT POSSIBLE, and NON-DISCRIMINATING by its own MUTATE

> **κ = ½ FITTED. ΛCDM has no a₀ (CFG67's stack is an effective PROXY with no z dependence in its tables). No verdict words: the pre-flight said NOT POSSIBLE before the measurement, and the MUTATE control confirmed it.**

Hashes:
- proposal 00ee88eec;
- criteria **8c925db21** (before any script);
- stage A pre-flight **2fa69fcd1** (committed before stage B ran);
- stage B and this README: the commit that carries this file.

Data: on disk only (CFG110's per-lens sums of the June KiDS-1000 estimator over 181,477 KiDS-bright lenses); nothing fetched.

## Bottom line
1. **KiDS cannot test a₀ ∝ H(z) by a lens-redshift split.**
   - The available lever is the extreme photo-z thirds, median z 0.21 against 0.39 (late) and 0.23 against 0.38 (early).
   - Over that lever the rival predicts an amplitude change of **+0.018 dex**; the flat law predicts +0.001.
   - The jackknife error on the combined amplitude is **0.038 dex**.
   - The power is **Δχ²_pred = 0.14 (canonical) / 0.17 (alt)**, against the 9 required. Stage A: **POSSIBLE_STAT false; POSSIBLE_SYS false** at every declared stellar-mass drift scenario (0.02, 0.05 dex).
2. **The measurement (descriptive):** D, the high-z third minus the low-z third on the 14 deep-regime bins, gives χ²/14 as follows. Every line is acceptable; nothing is separated.

| line | χ²/14 | p |
|---|---|---|
| zero | 19.8 | 0.14 |
| FLAT (canonical and alt) | 19.8 | 0.14 |
| RIVAL | 19.2 | 0.16 |
| ΛCDM proxy | 15.1 | 0.38 |

3. **The amplitude:** +0.060 ± 0.038 dex combined (late −0.16 ± 0.10, early +0.096 ± 0.041), against FLAT +0.001, RIVAL +0.019 and ΛCDM +0.003. That is 1.5σ from FLAT and 1.1σ from the rival: noise-level, and not read as evidence either way.
4. **MUTATE (load-bearing, FAILS as stage A predicted):** with the rival's predicted high/low ratio injected into the high-z third, FLAT is still not rejected (p = 0.10). Per the frozen file the test is **NON-DISCRIMINATING**.
5. **Even with infinite statistics, the test is walled by the stellar-mass drift.** In the deep regime, a stellar-mass calibration drift δ between the redshift bins moves the amplitude by δ/2, exactly as an a₀ drift does. The rival's 0.018 dex therefore needs the KiDS photometric M* to be stable to better than 0.036 dex between z ≈ 0.2 and 0.4. No source quantifies that stability (phase 1a, 63fea6817).

## What would make this test possible (stated, not pursued)
- A lens sample reaching z ≈ 0.8–1.0, where the rival's shift is 0.06–0.09 dex.
- A per-split amplitude error ≲ 0.02 dex.
- A stellar-mass drift across the lever demonstrated below about 0.05 dex.

Phase 1a found no public isolated-lens sample with stellar masses beyond z = 0.5: DES Y3 MagLim has no M* product, and HSC has Mizuki masses but no isolated-lens analysis.

## Disclosures
- **CFG110's R4** (a lens-z halves "photo-z check", consistent with zero) existed before this lane; it was not read before the criteria.
- **A prior independent two-bin KiDS a₀(z) lensing test exists:** `real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md`, b3be606a0, committed as "verified NULL". This lane's author learned of it from a peer session after stage A and has not read it. CFG255 is consistent with a null and adds the pre-flight power and the MUTATE result.
- The numpy RuntimeWarnings in the output are the known spurious numpy 1.26 / Accelerate matmul artefact: they fire on random finite input, and all results are finite.

## Files
- `cfg255_zsplit.py`
- `cfg255_stageA.out` and `cfg255_stageA_results.json`
- `cfg255_stageB.out` and `cfg255_stageB_results.json`
- `cfg255_stageB_MUTATE1.out` and `cfg255_stageB_MUTATE1_results.json`
- `PROPOSAL.md`, `FROZEN_CRITERIA.md`
- `PHASE1A_DATA_SCOPING_2026-09-30.md` (data chat)
