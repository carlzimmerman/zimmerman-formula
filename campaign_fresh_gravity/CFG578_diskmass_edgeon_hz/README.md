# CFG578: DiskMass σ_z with measured edge-on disc thicknesses (S4G 3.6 μm). NOT DIAGNOSTIC; the shared σ_z deficit dominates

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (3d8a5806f). (owner chat 10-09, "use measured edge-on disc thicknesses")
- **Script:** `cfg578_edgeon_hz.py` → `cfg578_edgeon_hz.out`, `cfg578_results.json`; MUTATE `CFG578_MUTATE=1` → `_MUTATE`.
- **Pipeline:** CFG577's functions by execution, unedited; only h_z changes.
- **Thickness calibration:** S4G 46 edge-ons at 3.6 μm (arXiv:2410.09762, source TeX): log10(h_z/kpc) = 0.90 log10(h_R/kpc) − 0.81, scatter 0.11 dex, z0 = 2 h_z (same convention as DMS II, verified). Bizyaev et al. 2014 not used (definitions unverified).
- κ = ½ fitted; both footings, never pooled; cold energy's mass still required; not theory closed.

## Result
S4G h_z / DMS h_z over the sample: median 1.146 (range 0.87–1.42): the measured edge-on discs are thicker.

| footing | radius | RM | PD |
|---|---|---|---|
| canonical | 1.5 h_R (primary) | 1.425 [1.349, 1.530] | 1.644 [1.580, 1.805] |
| canonical | 2.2 h_R | 1.416 | 1.679 |
| alt | 1.5 h_R (primary) | 1.397 [1.324, 1.497] | 1.650 [1.588, 1.813] |
| alt | 2.2 h_R | 1.386 | 1.687 |

All cells: 30/30 fitted, median Υ_K 0.41–0.56 (Υ gate passes). Newtonian reference 1.604 at Υ_K 0.92.
S4G scatter: h_z × 10^−0.11 → RM 1.247, PD 1.449; × 10^+0.11 → RM 1.627, PD 1.861.

- **Verdict as frozen: NOT DIAGNOSTIC** (neither model consistent, both footings).
- **Controls pass (2/2):** P1 reproduces CFG577's RM 1.342 and PD 1.551 exactly with DMS h_z.
- **MUTATE DETECTED:** a0 × 10 in RM fails the Υ gate (Υ_K 0.065–0.085, 21–24/30).

## Reading (not a verdict)
- With measured thicknesses, every gravity model over-predicts σ_z by 40–65% at plausible Υ_K; even the
  Newtonian model needs only Υ_K ≈ 0.9 for the rotation curve yet over-predicts by 60%. A deficit shared by all
  models points to the measured σ_z (young, kinematically cold tracers dominating the light-weighted dispersion,
  as argued by Aniyan et al.), not to the gravity law. DiskMass cannot separate RM from PD until that is fixed.
- RM stays the closest model in every cell (by 0.2–0.3 in r), but closeness under a shared systematic is not
  evidence. Do not cite as a round-rule win.
- Closing note for the DiskMass front (CFG576–578): no frozen test passed; the instrument's own systematic is
  larger than the RM–PD difference. Next useful data: old-population σ_z (Aniyan-type thin/thick decomposition).
