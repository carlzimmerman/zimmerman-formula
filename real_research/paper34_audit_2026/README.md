# paper34_audit_2026: the numbers behind PAPER34

PAPER34 is "A Dark Sector the MOND Kernel Cannot See: Reciprocity, Bound-Region Kernels, and the Cosmic-Shear Pincer" (`qwen_claude_field_theory/papers_2026/PAPER34_kernel_blind_dark_sector_2026.tex`). It reports lanes L353–L364, L370–L372 and the generated-phantom lanes GP0–GP4.

| Lane | Script | Checks | Result |
|---|---|---|---|
| P34 | `P34_paper_numbers.py` | 7/7 (MUTATE: the floor read as in the old GP4 summary; X1 and X1b fail, rc = 1) | See below. |

**N1: every quoted number.** 244 values the paper quotes are re-derived from the lanes' committed results JSON, or from the committed `.out` where a number is printed but not stored. Each is compared with the paper at the paper's own precision.

**X1: the KiDS realisable floor.** GP4's two window cells score **+19.1 to +21.5** in KiDS-1000 Δχ² above GP2's realisable floor, given the same freedom in the dark component's halo. The floor is the best isolated QUMOND lens in one uniform external field.
- The GP4 summary had said "about +8". +8.2/+8.3 is the floor's own distance from the Gauss-forbidden comparator.

**X4: the strict S8 floor.** KiDS-Legacy's S8 is 0.815 +0.016/−0.021. The lanes took 0.016 as the error (L319, line 186), giving a floor of 0.767.
- With the lower error the 3σ floor is **0.752**.
- GP4's window cells (0.762, 0.755) pass it, and so does L364's nearest miss.
- The strict set is then blocked by the forest alone. No cell of GP4's scan passes it.

**X5: the forest thresholds as thermal relics.** These use L319's own Viel et al. transfer function, cosmology and k grid, at the grid point k = 4.62 h/Mpc nearest 5 h/Mpc.
- The strict threshold 0.9952 is the 5.3 keV relic.
- The loose 0.9 is 1.5 keV.
- GP4's window cells are 4.3 and 4.7 keV.

Nothing is re-simulated here. The lanes themselves were re-run from a clean checkout for the paper (see its Reproducibility section).

Run it from anywhere:

```
python3 real_research/paper34_audit_2026/P34_paper_numbers.py
```

Set `ROOT=<checkout>` to audit another checkout; this mode writes no JSON. The script holds the paper's quoted values, so an edit to the paper's numbers must be mirrored here.

## After the deposit (DOI 10.5281/zenodo.22977900)

**The re-runs the paper lists as "still running" have finished (2026-09-26, 10:46).** Every lane was re-run from a clean checkout of `8ad1d1e69`. Each output and results file was then compared with the committed one, ignoring timing stamps.
- **Main runs identical:** L353, L354, L355, L356, L357, L359, L360, L361, L363, L364 and GP0–GP4 (15 lanes).
- **Mutation controls identical:** L353, L355, L356, L360, L361, L363, L364 and GP1–GP4 (11 controls). L356's only difference is the wrapper's trailing `rc=` label.
- **Not re-run:** L358, L362 and L370–L372, and the controls of L354, L357 and L359.

The deposit needs no change.

**High redshift for construction D, since computed.** The paper gives D's z ≈ 2.5 price as not computed, estimated at +0.8 to +1.0 dex from L356. `generated_phantom_2026/GP5_window_at_high_z.py` (commit `70d8070c0`, by another session) computes it for GP4's window cells:
- the zero-point shift is +0.82 to +1.05 dex, and the gate (≤ 0.10 dex) fails;
- RC100 gives f_DM 0.48–0.58.

This agrees with the paper's estimate.
