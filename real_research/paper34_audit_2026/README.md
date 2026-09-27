# paper34_audit_2026: the numbers behind PAPER34

PAPER34 is "A Dark Sector the MOND Kernel Cannot See: Reciprocity, Bound-Region Kernels, and the Cosmic-Shear Pincer" (`qwen_claude_field_theory/papers_2026/PAPER34_kernel_blind_dark_sector_2026.tex`). It reports lanes L353–L364, L370–L372 and the generated-phantom lanes GP0–GP4; version 2 adds GP5, DE1, DE8, L373, L392, MS1, V0 and XR5; version 3 adds MS3 and this folder's P34b, P34c and P34d.

| Lane | Script | Checks | Result |
|---|---|---|---|
| P34 | `P34_paper_numbers.py` | 7/7 (MUTATE: the floor read as in the old GP4 summary; X1 and X1b fail, rc = 1) | See below. |
| P34b | `P34b_gp4_window_resolution.py` | 3/4 (H fails, recorded; MUTATE, no free streaming: H fails in both boxes, rc = 1) | GP4's window cells in GP3's 100 Mpc box at twice the resolution: 1.167 and 1.208 on the alternative footing. Superseded by P34c and P34d. |
| P34c | `P34c_gp4_window_fixed_volume.py` | 2/3 (H fails, recorded; MUTATE, no free streaming: H fails, rc = 1) | The window cells in a 200 Mpc box at 512³ with GP4's seed: 1.207 and 1.251 on the alternative footing. The same seed on a finer grid is a different realisation (see P34d). |
| P34d | `P34d_resolution_or_realisation.py` | 7/10 (H1, H2, H3 fail, recorded; MUTATE, no free streaming: H2, H3 fail, rc = 1) | Resolution or realisation? Eight realisations, two paired boxes, the halo tallies. See below. |

**N1: every quoted number.** 298 values (version 3; 281 in version 2, 244 in version 1) the paper quotes are re-derived from the lanes' committed results JSON, or from the committed `.out` where a number is printed but not stored. Each is compared with the paper at the paper's own precision.

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

**Version 2 audit.** The script now also checks the numbers version 2 adds (DE1, GP5, L373, L392, V0, DE8, MS1, XR5). For v2 it was run inside a clean checkout of the committed state, so that uncommitted edits by other sessions (for example to L373's files) cannot enter it. Result: 7/7 checks, 281 values.

**Version 3.**
- The audit adds MS3's numbers and those of this folder's own lane, P34b.
- P34b re-scores GP4's cosmic-shear window at twice the resolution. Its pre-declared hypothesis, that both window cells hold, fails and is recorded: the (0.95, 1200) cell holds at 1.11/1.17, and the (0.90, 1400) cell reaches 1.208 on the alternative footing.
- Checks at that stage: 7/7, 289 values, run in a clean checkout of the committed state.

**Version 3, continued: D's window is withdrawn (P34c, P34d).**
- P34c re-scored the window cells in a 200 Mpc box at 512³ with GP4's seed. Both exceed the gate on the alternative footing (1.207, 1.251) and pass on the canonical (1.146, 1.189). This superseded the "one cell holds" reading of P34b in the unpublished v3 source (f393b3b09).
- But GP3's builder draws its white noise and its halo counts cell by cell, so the same seed on a finer grid is a *different realisation*. P34d separates the two effects.
  - **One realisation at two resolutions.** Each 512³ box is paired with its own 2×2×2 average on GP4's grid, and both are scored with GP4's k bins. The finer grid raises the worst R by 0.0302–0.0315 (alternative footing, two realisations, both cells).
  - **P34c's rise, split.** For GP4's seed, P34c's +0.062 is +0.031/+0.032 realisation, +0.031/+0.032 grid, and −0.0005/−0.0019 binning.
  - **H1 fails narrowly.** Its pre-declared claim was that the grid gives at least half of the rise; the shifts sit against a threshold of 0.0308–0.0309.
  - **Eight realisations at GP4's resolution.** GP4's seed plus 20260932–20260938. The builder draws 20 to 72 halos ≥ 1e14 M☉ (mean 49.5) against the Sheth–Tormen 58.9; GP4's box drew 36.
    - The worst R rises with that count (rank correlation 0.83).
    - On the alternative footing the window cells pass in 3/8 and 2/8 realisations; the means are 1.198 and 1.244.
    - H2, that the window passes in every realisation, fails (2/8).
  - **The ensemble estimate (H3).** The eight-realisation mean plus the paired grid shift gives 1.229/1.275 (alternative) and 1.164/1.208 (canonical). Both cells fail the alternative footing, and the (0.90, 1400) cell fails both. H3 fails.
  - **The census deficit is under-drawing, not shared cells.** GP4's box holds its 36 halos ≥ 1e14 in 36 cells. Only the two richest realisations (72 drawn) put two or more in a cell, in 7 cells each.
- Checks: 7/7, 298 values. As for v2, the audit ran in a clean checkout of the committed state.

