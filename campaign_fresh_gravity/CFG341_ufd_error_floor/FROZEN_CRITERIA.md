# CFG341 FROZEN CRITERIA: could an unaccounted velocity-error floor explain the UFD excess?

**Lane:** orchestrator. The owner said "run the error floor check".

**Question.** Published UFD dispersions are deconvolved with the quoted per-star errors, which already include each survey's documented systematic floor (≈1–2 km/s for DEIMOS-class spectrographs). Suppose a hidden extra per-star error f went unaccounted. Then the true dispersion is σ_true = sqrt(σ_obs² − f²).

## Computed (same sample and estimator as AUDIT_UFD; 31 resolved UFDs from the LVD MW table, M_V > −7.7; both footings)
1. **Per UFD:** f_need = sqrt(σ_obs² − σ_law²), the hidden floor that would bring σ down to the law. If σ_obs ≤ σ_law, f_need = 0.
   - Report the median and the fraction with f_need ≤ 1.0 km/s and ≤ 2.0 km/s.
2. **Re-score:** subtract a hidden floor f = 1.0 km/s (primary) and 2.0 km/s (extreme) in quadrature from every resolved σ_obs, then recompute the median offset and its z.
   - Use AUDIT_UFD's error budget: bootstrap over the resolved systems plus the Υ floor of 0.077 dex.
   - Upper limits are kept and get the same subtraction.
   - Where σ_obs ≤ f, σ_true is set to 0.1 km/s.

## Decision
- **EXPLAINS:** with f = 1.0 km/s the offset falls below 2σ on both footings.
- **ONLY AT EXTREME:** this happens only with f = 2.0 km/s, which is larger than the documented total floors themselves and so implausible as a *hidden* term.
- **NOT:** neither.

## Controls
- **C1:** with f = 0 the run reproduces AUDIT_UFD's measured-only median offset (+0.354 canonical, from CFG327's printout) to 0.005 dex.
- **MUTATE** (CFG341_MUTATE=1): σ_obs is shuffled across systems; the f_need distribution must change.
