# XR35: the M\* KiDS chain re-scored with the corrected projection

**Scope.** FP20 (`derivation_chain_2026/FP20_esd_projection_fix.py`, commit 7a8c25321) found that all three KiDS projectors in
the record share one defect: the trapezoid over the Abel integral skips the 1/√ end interval, and the inner-disc term is exact
only for Σ ∝ 1/R. FP20 re-scored the chain's own lanes but left the M\* KiDS chain open (its ledger entry F20n). The chain is:

- DE10, the converged model;
- XR9, the small-region door's KiDS scan;
- XR14, KiDS on M\*'s own carrier. This is the only scorecard row validated ON M\*.

This lane re-scores that chain with only the projector replaced. It then traces which hub lanes lean on the defective
projectors, and re-runs only the evidence where a verdict could flip.

κ = ½ is fitted (Z = 5.7888), and nothing here tests it. Both footings are used throughout. The theory is not closed.

## Files

| file | what it is |
|---|---|
| `XR35_kids_rescore.py` | V (the defect, the drop-ins, the scored carrier templates), K (controls), R (DE10 / XR9 / XR14 before → after), S (halo masses; 2-halo template) |
| `XR35_hub_dependencies.py` | P0 (the corrected slot), D1/D2 (the code-level trace and effect sizes), X1/X2 (XR10's two rule evidences re-scored), X3 (XR10's KiDS rows), XR28 (listed only) |
| `*.out`, `*_results.json` | main runs (`XR35_kids_rescore` rc = 1, see below; `XR35_hub_dependencies` rc = 0) |
| `*_MUTATE.out`, `*_results_MUTATE.json` | MUTATE runs (both rc = 1, as required) |

Run from the repository root in this order. Script 2 reads script 1's results for XR10's rows.

```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR35_kids_rescore.py
         python3 real_research/cross_thread_review_2026_09_26/XR35_kids_rescore.py
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR35_hub_dependencies.py
         python3 real_research/cross_thread_review_2026_09_26/XR35_hub_dependencies.py
```

Each script writes its own `.out` and a final `rc=` line. Runtime is about 1.5 min and 2.7 min, single-threaded. No halo is
regenerated.

## Method

Each lane's committed main block is exec'd twice in this lane's namespace, with file writes refused. The first run uses the
committed projectors (the control). The second run splices FP20's drop-ins in right after DE8 is loaded. The drop-ins are
exec'd from FP20's source at git HEAD. Every exec'd file and cache is asserted identical to HEAD. The drop-ins are:

- `CellFix` for DE8's `esd_from_mlens`;
- `M2Fix` for `project_M2` on the carrier templates' node densities;
- `model_M2_factory(direct=True)` for L352's unswitched baseline. Every baseline χ² is recomputed with it.

DE10's halo generation is answered from XR9's cache, which holds DE10's own eight halos. Check K2 compares every
configuration field of those halos.

## The defect: confirmed independently (V0, V2)

The reference is this lane's own fine-shell projector. It uses 40,000 shells for M_2D and 400,000 for the point values. It
reproduces the closed forms to within 1.2e-6: the truncated SIS, Wright & Brainerd NFW and Plummer spheres. It reproduces
adaptive quadrature to the same precision on a hollowed NFW, a capped NFW and one scored carrier template.

Against that reference, at the 15 KiDS radii:

| profile | committed P2 (`project_M2` / L352 `model_M2` / DE8 `esd_from_mlens`) | committed P1 (FP6 `esd_of_M`) |
|---|---|---|
| SIS, V = 200 km/s | −2.04 … −2.96% at every radius | −58.6% at 35 kpc |
| NFW 1e13, c = 2 | +11.5% at 35 kpc | −35.1% at 35 kpc |
| Plummer, a = 50 / 150 kpc (cored) | +8.5% / +44.6% at 35 kpc | — |
| NFW capped flat inside 50 kpc | +46.0% at 35 kpc | — |
| NFW hollowed inside 100 kpc | up to 8.4% of the peak | — |

On the carrier templates the lanes actually score, the committed `project_M2` is off by +0.3 … +18.5% of the template's peak
at 35 kpc (decayed carriers). That is at most 0.03 σ_KiDS for the decayed carriers and 0.26 σ for the no-decay control halos
(V3). The carriers are small next to the KiDS errors.

## FP20's drop-ins (V1, V3): two pre-declared checks failed; both are kept as run

**On FP20's own profiles (SIS, NFW):** every drop-in path is within 0.012%, and P1 is within 0.006%. FP20's stated 0.04%
holds.

**V1 failed.** On my added Plummer core with a = 150 kpc, the three P2 paths reach 0.073% at 35 kpc, against the 0.04%
threshold.

- V1d: this is the P2 lanes' read convention, not the projection. The lanes interpolate M_2D linearly in ln R on a 700-point
  grid.
- The exact M_2D, read that way, carries the same 0.0725%.
- FP20's kernel on a 10× finer grid gives 0.0002%.
- The convention is shared by both projectors and kept as committed. It bites only deep inside a large flat core.

**V3 failed.** 4 of the 112 carrier templates exceed 0.2% of their peak: the no-decay control halos b0, b1 and b3, and
MSPH_canonical_b2_v625.

- V3d: every one of these is `M2Fix`'s power-law estimate of the mass inside the first node (1 kpc), extrapolated from two
  noisy histogram nodes.
- On nodecay_b1 it gives 8.9e9 M☉, while the histogram holds 1.25e9 M☉. On MSPH_canonical_b2_v625 it gives 0, while the
  histogram holds 2.7e7 M☉.
- With the histogram's own inner mass, every template is within 0.13% of its peak.
- V3s: replacing every carrier template by the exact reference moves XR14's H1/H1b cells by at most 0.006 and DE10's cells
  by 0.0002. XR14's C2 no-decay control stays at +127/+131.

**Conclusion.** No scored verdict rests on either residual. `XR35_kids_rescore` still ends rc = 1, because V1 and V3 were
declared load-bearing and they failed. Their thresholds are unchanged.

## Re-score: before → after (Δχ², canonical / alt; bar ≤ +4 on both footings)

**DE10** (fs = 1, A ≤ 20). The headline passes. Worst −29.02 → −24.04.

| cell | before | after | verdict |
|---|---|---|---|
| 600 km/s, w = 0.02 | −37.03 / −34.01 | −31.56 / −28.18 | pass → pass |
| 600 km/s, w = 0.25 | −32.27 / −29.29 | −26.82 / −24.36 | pass → pass |
| 650 km/s, w = 0.02 | −36.82 / −33.74 | −31.28 / −27.85 | pass → pass |
| 650 km/s, w = 0.25 | −32.08 / −29.02 | −26.58 / −24.04 | pass → pass |

DE10's C1 column, L390's curvature branch with the same carrier, goes −13.12/−7.16 → −9.61/−3.65 at 600 km/s and
−12.96/−7.14 → −9.35/−3.52 at 650 km/s. It still passes.

**XR9** (gated fs = 1, A ≤ 2, w = 0.25, the worse kick per footing). No verdict flips. p1_x2.5 and p1.5_x2.5 pass; the other
twelve fail.

| cell | before | after |
|---|---|---|
| p1_x2.5 | −32.09 / −29.02 | −26.59 / −24.05 |
| p1_x3.5 | +9.58 / +14.64 | +9.34 / +14.73 |
| p1_x5 | +57.44 / +60.35 | +56.78 / +59.46 |
| p1_x7 | +104.25 / +107.39 | +110.27 / +118.90 |
| p1_x10 | +136.94 / +140.44 | +141.26 / +146.06 |
| p1_x14 | +154.25 / +160.77 | +164.12 / +168.92 |
| p1_x20 | +209.75 / +210.58 | +218.45 / +220.42 |
| p1.5_x2.5 | −17.72 / −13.03 | −10.14 / −4.55 |
| p1.5_x3.5 | +16.72 / +19.93 | +23.40 / +26.49 |
| p1.5_x5 | +88.86 / +87.25 | +95.76 / +94.47 |
| p1.5_x7 | +108.80 / +113.57 | +113.63 / +115.01 |
| p1.5_x10 | +137.87 / +139.24 | +146.06 / +145.99 |
| p1.5_x14 | +170.32 / +175.32 | +173.54 / +178.14 |
| p1.5_x20 | +233.39 / +232.94 | +234.41 / +234.49 |

The other XR9 results:

- The carrier-inclusive KiDS cap goes x_c,eff(0.25) 4.4209 → 4.4060.
- DE9's switch-only cap, XR9's reference line, goes 4.3473 → 4.3043 (X2).
- The door's KiDS half (H-K) still fails: no cell above the switch-only cap passes.
- The hard-gate p1_x3.5 goes −0.74/+0.00 → +1.80/+3.32 and still passes the hard-gate column.
- The flagship is identical under both projections (K4): 4,139 leaves, |d| = 0.

**XR14, ON M\*** (fs = 1, A ≤ 2). The pass survives on every cell: worst −26.28 → −21.72, with shifts of +4.5 … +5.5.

| M\* carrier (MSPH) | before | after | L388 as written | before | after |
|---|---|---|---|---|---|
| 575, w = 0.02 | −34.25 / −31.36 | −29.16 / −25.94 | 575, w = 0.02 | −36.63 / −33.61 | −31.17 / −27.77 |
| 575, w = 0.25 | −29.70 / −26.70 | −25.04 / −22.16 | 575, w = 0.25 | −31.91 / −28.90 | −26.49 / −23.98 |
| 600, w = 0.02 | −34.17 / −31.28 | −29.08 / −25.90 | 600, w = 0.02 | −36.58 / −33.46 | −31.05 / −27.62 |
| 600, w = 0.25 | −29.61 / −26.62 | −24.96 / −22.12 | 600, w = 0.25 | −31.82 / −28.75 | −26.35 / −23.83 |
| 625, w = 0.02 | −34.12 / −30.94 | −29.00 / −25.49 | 625, w = 0.02 | −36.62 / −33.63 | −31.10 / −27.77 |
| 625, w = 0.25 | −29.57 / −26.28 | −24.91 / −21.72 | 625, w = 0.25 | −31.90 / −28.91 | −26.44 / −23.97 |
| 650, w = 0.02 | −33.96 / −30.94 | −28.85 / −25.52 | 650, w = 0.02 | −36.51 / −33.50 | −31.00 / −27.65 |
| 650, w = 0.25 | −29.40 / −26.29 | −24.77 / −21.75 | 650, w = 0.25 | −31.80 / −28.79 | −26.36 / −23.85 |

Where the shift comes from:

- The switch alone (fs = 0) goes −24.63/−20.71 → −21.54/−17.48, a shift of +3.1/+3.2. This comes from the lens model and the
  baseline. The unswitched baseline χ² drops 174.30/166.92 → 159.92/153.02, which is FP20's R9 value to 1e-6 (K3).
- The carrier's share of the score falls from 4.8–6.0 to 3.2–4.7.

Other XR14 rows after the fix:

- FK1 variant: worst −23.50 → −19.18.
- 'As run' (the canonical carrier on the alt footing): worst −28.73 → −23.77.
- C2, the no-decay carrier: +128.7/+131.5 → +127.8/+132.6. It is still rejected.

**The lanes' own checks that flip under the fix** (R4). Every one is pinned to a committed defective-projection number:

| lane | check | pinned to |
|---|---|---|
| DE10 | C1 | L390's scores |
| XR9 | C1 | DE10's table |
| XR9 | C6 | DE9's cap 4.3473 |
| XR9 | C2 | the committed halo plan (see S1) |
| XR14 | C1 | DE10's table |

## Is re-projecting the cached halos enough? (S1, S2)

**DE10 / XR14: yes.** L390's refit masses, which set DE10's and XR14's halos, do not move under the fix: [10.5, 10.8, 11.0,
11.1] both ways. The M\* chain's mass sensitivity is ≤ 0.02. That figure comes from L390's masses against the MOND-sector
refit, using L375's cached halos on M\*'s gate; XR14's own scope note put it at ≤ 0.03.

**XR9: not strictly.** Its per-cell refit, its "rule 3", moves by one grid step in 7 of 14 cells.

- Six of those cells have cached halos at the new masses. Re-scored with them, they move by ≤ 0.3, and no verdict changes.
- p1_x10 needs a bin-1 halo at log M_b = 10.7, which is not cached and was not regenerated. It is a failing cell, +137 from
  the bar.

**The 2-halo template's own inner disc** (S2, kept as committed): at most 2.8e-4 M☉/pc² per unit bias. Making it exact moves
XR14's worst cells by −0.01.

## Hub lanes (XR35_hub_dependencies)

| lane | depends on a defective projector? | what consumes it | effect | verdict change |
|---|---|---|---|---|
| XR10 (validator) | no call. FP20's token scan hit a regex string, and `gates` is a local set of a row's gate names | its axis verdicts: none | — | none |
| XR10 rule SIGMA0_FOR_SIGMA1 (check E evidence) | DE8's upper-branch σ shift (P2) | check E, which would go rc = 1 if the evidence exceeded 0.4 | r200 0.39991 → **0.36364**; nfw 0.31318 → **0.27522** | none: the evidence still holds (re-run: X1) |
| XR10 rule HARDW_FOR_SMOOTH (carries XR14.kids) | DE9's MOND-sector switch-only cap (P2) | check E | caps 4.4789 / 4.3473 → **4.3855 / 4.3043**; p = 1 window [1.667, 3.448] / [2.0, 3.346] → **[1.667, 3.376] / [2.0, 3.313]** | none: it still contains x_c0 = 2.5 (re-run: X2) |
| XR10 KiDS rows (recorded verdicts) | all 11 rows score KiDS with P2 (AT3 also with P1) | reported only | DE10, XR9, XR14 and L390 as above; DE8 upper branch passing cells (σ = 1) r200 **22 → 5** of 36, nfw 35 → 31; AT3's window keeps its pass (FP20 R11) | not re-scored: DE2.window, DE9.curv, L392.curvature, L392.matter (comparison rows) |
| XR18_frw_yield_crossing | P1, via FP9's `kids_class` | K1 control only | FP9 H2 −2.40/−5.57 → −2.63/−1.94 (FP20 R2) | K1 would fail on re-run (pinned); E1–E4 do not consume KiDS |
| XR18_state_separator | P1, via FP13's `gates()` | K1 control only | FP13 H1: z = 0.25 −6.25/−7.67 → −8.62/−10.35; z = 0.4 −7.83/−10.67 → −8.82/−9.66; z = 0.7 +542.7/+575.7 → +558.7/+595.3 (FP20 R3) | K1 would fail on re-run (pinned); HS1–HS7 do not consume KiDS (only `H["s8"]` is reused) |
| XR25_lambda_regulator | P1, via FP9's `kids_class` | K1 control only | FP13 H1 at z = 0.25, as above | K1 would fail on re-run (pinned); L1 does not consume KiDS |
| XR29_mw_outer_curve | none. FP20's hit was `fit_cell` inside `refit_cell`; Σ_dyn comes from its axisymmetric solver | — | — | none. It exec's FP11 whole but reads only projection-free names (L(a), y_th, Grid, phantom, …) |
| XR28 (in flight; listed, not run) | none. Its own exact uniform-shell kernel (`shell_esd_kernel`), checked against W&B in its K5; FP6 is exec'd only for `phantom()` | — | — | — |

The DE8 upper-branch drop (r200 22 → 5 passing cells) belongs to DE8's own reported verdict, and DE8 is a comparison row that
sits off M\*. It carries the same carrier-template effect FP20 found in L360, where passing pairs went 70 → 35.

## Controls and MUTATE

**Controls, all at |d| = 0:**

| check | what is reproduced |
|---|---|
| K1 (script 1) | with the committed projectors, every committed number: DE10 40, XR9 7,877, XR14 2,187, and every check verdict |
| K2 (script 1) | DE10's eight halo configurations match the cache |
| K3 (script 1) | the corrected slot gives FP20's R9 base (159.920/153.018) to 1e-6, and DE8's C1 fit to 6e-6 |
| K4 (script 1) | the flagship is projection-free |
| K1 (script 2) | DE8's upper-branch scan, 288 numbers |
| K2 (script 2) | DE9's caps |

**MUTATE** puts the committed projectors in the corrected slot:

- script 1: V1 fails at 44.6% (with V3 and K3, which test the same slot), and every "after" equals its "before" (K-MUT);
- script 2: P0 fails at −2.96% / +8.17%, and the X1/X2 "after" values equal their "before".

## Disclosures

**Development runs of script 1.** All were under MUTATE, where the corrected slot holds the committed projector, so they
revealed no corrected score.

1. V0 failed at 5.8e-4 on the hollow NFW, because a reference shell straddled the density jump. The reference then snapped its
   edges onto the known jumps and switched to exact shell masses where M(r) is closed-form.
2. V0 failed at 1.1e-5, from the uniform-shell O(h^1.5) Σ error next to R. The point values then moved to a 400,000-shell set.
3. V0 passed.
4. A full run showed the harness exact.

Scratch debugging scripts stayed in the session scratchpad and were not committed.

**The first recorded main run.** V1 and V3 failed there as pre-declared. I then added three reported diagnostics, labelled
in the file: V1d, V3d and V3s. The thresholds are unchanged. MUTATE and main were then re-run in that order.

After that I added one print line, for the uncached p1_x10 cell, and re-ran both pairs again. The main-run rows are identical
to the first main run (max |d| = 0).

**Script 2.** Its development runs were under MUTATE, so no corrected DE8 or DE9 number was seen before the recorded main
run. Three things changed during development:

- D1 first counted XR10's local variable `gates`. Its criterion is now calls, as stated in the docstring.
- Generic loop names are no longer followed as containers.
- XR18_state's K1 values are read from its committed `.out`, because its JSON keeps only K1's deviation.

**HX2 was not a blind prediction.** It was written after seeing script 1's XR9 C6 flip. HX1 was blind.

**Scope limits.**

- Halo masses are as committed, apart from S1.
- No halo was regenerated.
- The P2 lanes' annulus read of M_2D on the 700-point R grid, and the 2-halo template, are kept as committed.

**Other sessions.** They modified tracked files during this lane (a paper .tex, XR21_pm_core.py). This lane did not touch
them.
