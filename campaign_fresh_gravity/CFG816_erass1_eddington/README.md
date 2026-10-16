# CFG816: Eddington bias in eRASS1 gas masses. Selection explains the pattern under the frozen rule, but MUTATE did not bite (weak)

**Data side only.** The mass-function slope α = 2.03 ± 0.11 is measured from the full eRASS1 catalogue (10,448 clusters;
counts above the peak). The per-cluster errors come from the catalogue's own M_gas bounds.

| gas tercile (observed) | light | middle | heavy |
|---|---|---|---|
| median σ(ln M_gas) | **0.79** | 0.29 | 0.16 |
| median Eddington correction M_true/M_obs | **0.29** | 0.84 | 0.95 |
| CFG815 P MID, before → after | 1.21 → **2.58 ± 0.53** | 1.64 → 1.59 | 0.90 → 0.93 |
| plain law MID, before → after | 1.39 → 2.96 | 2.24 → 2.09 | 2.00 → 2.05 |
| CFG809 MID, before → after | 0.64 → 1.35 | 0.93 → 0.88 | 0.69 → 0.71 |

**Frozen reading: SELECTION EXPLAINS PATTERN.** CFG815 P's terciles go from non-monotonic to monotonic: short at low mass,
right at high mass.

**What must go with it.**
- **The light tercile's gas masses are very uncertain** (σ ≈ 0.8 in ln, about a factor 2.2). Its earlier "fits fine" result
  was not meaningful.
- **MUTATE (σ shuffled across clusters) did NOT weaken the trend** (light tercile after correction 3.55). Re-binning by
  corrected mass alone can manufacture a monotonic pattern, so this classification is **weak evidence**.
- The lognormal correction −ασ² is a small-σ approximation. At σ = 0.8 (ασ² ≈ 1.3) it likely overstates the bias.
- Selection acts on X-ray count rate, not on M_gas directly.
- A proper fix forward-models the eRASS1 count-rate selection.
- **What survives:**
  - the light-tercile results cannot be trusted;
  - the corrected trend, if real, is monotonic: lower-mass clusters need MORE extra mass. That is the direction expected if
    lower-mass systems expel more gas.

Model rescaling uses ΔΣ ∝ M^0.47 (declared approximation). K1 PASS.

κ fitted; not theory closed.
