# CFG16 — the self-consistent KiDS floor

Script: `CFG16_selfconsistent_floor.py`, about 10 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. The caps are held at 0, the floor returns to 0.47, and H1 fails (rc = 1).
- The main run exits 1, because H1 failed.

## The closure

CFG15's framework lens bias (1.1–1.6) was taken at the law's **untruncated** turnaround masses. With the phantom cut at x r_ta (CFG4's density edge), each system's actual turnaround mass is smaller, and so is its bias.

The zero-parameter closure is taken at every x. For each lens bin:
- take CFG4's truncated profile and find its own turnaround radius (CFG4_switch's `r_bound`, at Δ_ta(0.25));
- take the enclosed mass there;
- compute that mass's peak-background bias, using the larger of the collapse and turnaround values.

That bias is the bin's 2-halo cap. It is an **upper** estimate, because KiDS's isolation cut lowers the true bias.

## Results

**Control.** C1 reproduces CFG15's committed floors (caps 0, 1 and 2, and its untruncated bias) exactly.

**The truncated bias (canonical P2, bins by increasing M_b)**

| profile | bias per bin |
|---|---|
| untruncated (CFG15) | 1.11, 1.35, 1.44, 1.57 |
| truncated at x = 0.30 | 0.89, 1.04, 1.09, 1.17 |
| truncated at x = 0.34 | 0.91, 1.06, 1.12, 1.21 |

**The self-consistent floor against CFG12's budget edge (FG001 grouping plus the share at the budget's own scale)**

| row | floor | edge | gap |
|---|---|---|---|
| canonical P2 | 0.3409 | 0.3406 | **+0.0003** |
| canonical ν_mono | 0.3476 | 0.3380 | **+0.0096** |
| alt P2 | 0.3402 | 0.2932 | +0.047 |
| alt ν_mono | 0.3453 | 0.2910 | +0.054 |

**H1** (the canonical window survives self-consistently): **FAILED**.

## Standing

**CFG4's minimal conflict is not resolved.**
- **Canonical P2:** the window closes to zero width, with the floor 0.0003 above the edge.
- **Canonical ν_mono (the contract kernel):** closed by 0.010 in x, about 3%.
- **Alt footing:** closed by about 15%.

This uses the most generous self-consistent lens bias. KiDS's isolation cut lowers it, which raises the floor further.

Taken together:
- CFG11 and CFG12 moved the budget edge up, from 0.280 to 0.341 canonical;
- CFG15 and CFG16 moved the KiDS floor up, from 0.309 to 0.341–0.348, once the lens bias is physical and self-consistent.

The two meet at the margin. The conflict is now **within about 3% on canonical and about 15% on alt**.

**Where a resolution would have to come from:**
- the budget's own systematics, i.e. the HI-selected gas fractions and the SMF normalisation;
- a lens population with a higher real bias;
- an ingredient not in CFG4's target.

Nothing here says the theory is closed.
