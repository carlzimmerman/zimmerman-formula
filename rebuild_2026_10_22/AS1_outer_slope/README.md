# AS1_outer_slope: Argon's slope test favours the law on photometric isolation, and is not powered on spectroscopic isolation, where it leans the other way

Criteria: `FROZEN_CRITERIA.md` (7629303317), committed alone before any script or slope number. Script `as1_slope.py <kids_source_cache> <work_dir>` execs SI2's text. Outputs `as1.out`, `as1_results.json`, `as1_MUTATE.*`. Fit: ΔΣ = A (R/300 kpc)^(−γ), six bins in 150–800 kpc, GLS, full covariance.

## Status as frozen: NOT DECIDED, on a check I specified wrongly
The frozen MUTATE multiplied the data by (R/0.3)^−0.5 and kept the covariance, and demanded every γ rise by 0.5 within 0.002. It fails: max |d| 0.363, on the noisiest stacks. That criterion was wrong: GLS on noisy data with unscaled errors need not shift by exactly 0.5. The check does bite, since B21's top bin moves to 1.488 and flips class. Scaling the covariance by the same factor (`--scaled`, `as1_MUTATE_scaled.out`, post-result) returns +0.5 to 7e-16. So by the frozen rule the combined verdict is NOT DECIDED. The classes below are what the frozen cuts give, and K1, K2, K3 pass.

## Frozen classes
| sample | N | γ | σ_γ | A(300 kpc), M☉/pc² | χ²/4 (p) | S/N | class |
|---|---|---|---|---|---|---|---|
| D1 B21 isolated, lg M★ 8.5–10.3 | | 0.583 | 0.266 | 2.88 | 7.0 (0.138) | 9.2 | NOT POWERED |
| D1 B21, 10.3–10.6 | | **0.955** | 0.120 | 7.39 | 5.2 (0.267) | 15.4 | **FAVOURS LAW** |
| D1 B21, 10.6–10.8 | | **0.860** | 0.117 | 8.26 | 7.3 (0.119) | 16.4 | **FAVOURS LAW** |
| D1 B21, 10.8–11.0 | | **1.014** | 0.092 | 10.75 | 5.8 (0.217) | 20.5 | **FAVOURS LAW** |
| D2 S3, L − I | 2,251 | 2.016 | 0.855 | 8.01 | 1.6 (0.817) | 3.6 | NOT POWERED |
| D2 S1, L − I | 10,620 | 1.398 | 0.331 | 7.55 | 1.4 (0.838) | 7.5 | NOT POWERED |
| D3 S3, raw L − R | 2,251 | 1.769 | 0.563 | 8.78 | 6.6 (0.160) | 4.8 | NOT POWERED |
| D3 S1, raw L − R | 10,620 | 1.570 | 0.268 | 7.73 | 0.4 (0.983) | 7.8 | NOT POWERED |

**On Argon's named data Argon's reading is right:** γ is 0.86–1.01 in the three powered bins, 1.675 excluded far beyond 3σ.

## Model slopes through the same estimator (canonical; reported)
The full models include baryons, neighbours and the hole term. Argon's bare 1.00 and 1.675 turn out close to them.

| sample | law R0 | route E R0 | law R2 | route E R2 | data pull from law R2 | data pull from route E R2 |
|---|---|---|---|---|---|---|
| S1, L − I | 0.953 | 1.588 | 0.961 | 1.568 | **+1.32σ** | **−0.51σ** |
| S1, raw L − R | 0.975 | 1.602 | 0.981 | 1.581 | **+2.20σ** | **−0.04σ** |
| S3, L − I | 0.940 | 1.573 | 0.953 | 1.552 | +1.24σ | +0.54σ |
| S3, raw L − R | 0.945 | 1.580 | 0.956 | 1.560 | +1.45σ | +0.37σ |

Alt: law slopes within 0.003, pulls within 0.02σ.

**Amplitude at 300 kpc, S1 (M☉/pc²):** data 7.55; law R0 6.14, R2 7.51; route E R0 2.97, R2 4.48. So S1 has route E's slope at about the law's R2 amplitude. Route E's model at R2 is short by about ×1.7 at this radius. A matched slope does not close that.

## How far apart are the clean and photometric slopes?
S1 (γ 1.398 ± 0.331, raw 1.570 ± 0.268) minus B21 10.8–11.0 (1.014 ± 0.092): +0.38 ± 0.34 (1.1σ), raw +0.56 ± 0.28 (2.0σ). Against B21 10.6–10.8: +0.54 ± 0.35 (1.5σ), raw +0.71 ± 0.29 (2.4σ). This is suggestive and no more. B21's four bins span the mass range differently from S1, and the difference could be leakage, selection, or noise.

**Power.** Scaling σ_γ with √N, the frozen 0.225 needs N ≈ 23,000 for L − I and N ≈ 15,000 for raw L − R, with this completeness. That is 1.4–2.2× S1. GAMA can't supply it. WAVES or a completed DESI BGS footprint could.

## Checks
K1 (noise-free γ 1.3 returned, 2e-15), K2 (B21 √diag C vs error/bias, 4.4e-5), K3 (S1, S3 stacks equal SI1's committed `d`, 0.0): PASS. MUTATE as frozen: FAIL, see the status note. The file `as1_slope.py` was edited after the frozen runs to add `--scaled`; the two edits are inactive without that flag.

## What this does not show
- A power law is not a model, and this ignores amplitude. SI1 and SI2's χ² stand for fit quality.
- It does not establish leakage in B21. It shows the slope's value on the clean samples is compatible with route E and at 1.3–2.2σ from the law, on small N.
- It does not show route E fits B21. On those data route E's slope of about 1.6 is excluded unless the excess is environmental, and that remains to be shown with a hole-corrected nested sample at large N.
- Nothing here says the data favour the framework.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
