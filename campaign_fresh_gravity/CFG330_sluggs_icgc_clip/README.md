# CFG330: are the four cluster-centre ellipticals' excesses intracluster-GC contamination?

**Verdict: NOT SUPPORTED** (frozen criteria 514b5ec8c).

## Method
- Base: AUDIT_SLUGGS's raw-velocity recompute. Raw Forbes+17 GC velocities; JAM-calibrated law; γ = 3, isotropic; outer bins; ν_mono.
- Added: a per-bin local k-σ clip with a truncated-Gaussian correction.

## Results

| mode | centrals (4), canonical | others (12), canonical | centrals' excess over others |
|---|---|---|---|
| K0 (baseline) | +0.224 ± 0.017 | +0.056 ± 0.020 | 0.168 dex |
| **K25 (primary)** | **+0.229 ± 0.011** | +0.070 ± 0.019 | **0.160 dex (−5%)** |
| K20 (aggressive bound) | +0.095 ± 0.031 | +0.032 ± 0.024 | 0.063 dex |

- The alt footing behaves the same way.
- K25 leaves M87, NGC 4365, NGC 4374 and NGC 5846 essentially where they were: +0.260, +0.210, +0.221 and +0.226 against +0.275, +0.205, +0.201 and +0.213 at baseline.
- So the centrals' velocity distributions show no outlier tail that a 2.5σ clip removes. There is no sign of intracluster-GC contamination.
- The K20 bound lowers everything, the twelve non-centrals included. That makes it a non-specific trimming of real tails, not evidence for contamination.

## Controls
- **C1 passes:** K0 reproduces the audit's all-16 offset, +0.0977.
- **C2 passes:** a pure Gaussian bin is recovered to 0.975.
- **C3 passes:** with 25% contaminants at 2.5× σ injected, K25 removes 66% of the inflation, so the clip *can* remove contamination when it is present.
- **MUTATE passes:** with the clip applied to non-centrals only, the centrals' offsets are unchanged, as required.
- The script's inherited audit checks return rc 1 in the clipped modes. They compare against the unclipped CFG55 baseline by design.

## Run
```
CFG330_K=K0  python3 campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc.py
CFG330_K=K25 python3 campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc.py
CFG330_K=K20 python3 campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc.py
CFG330_K=K25 CFG330_MUTATE=1 python3 campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc.py
python3 campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_controls.py
```
