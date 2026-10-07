# CFG443: in CFG378's boxes the cold component in massive halos is MORE concentrated than the law's target, with or without settling. Ordinary cold matter gives the X-COP sign; settling pushes the other way

Criteria 02d8e1d25 (frozen before any CFG378 256³ output was read). Script `cfg443_halo_shape.py` (~100 s, 2 threads; CFG378's engine imported read-only). κ = ½ fitted; both footings. No DM particle; the cold mass is still required.

20 most massive halos per run; cumulative masses at r = 2, 3, 4, 6 cells (1.6–4.7 Mpc/h). Slope of log(M_c/M_t) against log r, median ± bootstrap.

| footing | run | slope log(M_c/M_t) | slope log(M_c/M_b) | verdict | minus g = 0 |
|---|---|---|---|---|---|
| canonical | g = 1 (settling, primary) | **−0.717 ± 0.017** | +0.059 ± 0.017 | X-COP-LIKE | **+0.075 ± 0.031 (measurable)** |
| canonical | g = 0.1 | −0.773 ± 0.026 | +0.007 ± 0.002 | X-COP-LIKE | +0.019 ± 0.037 (invisible) |
| canonical | **g = 0 (no settling)** | **−0.792 ± 0.027** | 0.000 | (reference) | — |
| alt | g = 1 | −0.740 ± 0.016 | +0.042 ± 0.013 | X-COP-LIKE | +0.051 ± 0.031 (invisible) |
| alt | g = 0.1 | −0.775 ± 0.026 | +0.004 ± 0.001 | X-COP-LIKE | +0.015 ± 0.037 (invisible) |
| alt | g = 0 | −0.790 ± 0.026 | 0.000 | (reference) | — |

**Reading.**
- **The X-COP sign comes free from ordinary collisionless cold matter.** With no settling, the cold component in massive halos is already far more concentrated than the law's phantom target (−0.79). A phantom target is shallower than a collapsed halo.
- **Settling pushes the other way:** toward the target, less concentrated. It does so only slightly, consistent with CFG378's "hollow" verdict (2.6% of the gap closed).
- This supports the CFG440 session05 reading: in clusters the cold fluid behaves as ordinary cold matter, and the settling target plays almost no role there.
- **Declared limit:** these radii (1.6–4.7 Mpc/h) do not overlap X-COP's 0.1–1 Mpc. Only the sign is compared, not the magnitude (X-COP −0.46 at its radii).

**Controls.**
- K1 (cold mass conservation) passes in all 6 runs.
- K2 (Q at z = 0 recomputed here against CFG378's own value) passes in all 6 runs, to < 1e-4.
- MUTATE (cold = baryon positions) gives |slope M_c/M_b| < 0.01: detected, exit 1.
