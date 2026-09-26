# Cross-thread review — 2026-09-26

An independent review of the dark-sector, vacuum-gate and field-theory work that several sessions (and the lead
track) were running in parallel on 2026-09-26, done while those runs were live. Five read-only lanes, XR1–XR5. Every
number here comes from a script in this folder with a control (and, where it makes sense, a MUTATE run that must
fail). Nothing outside this folder was edited or run by the review. **The closure target is OPEN.** κ = ½ stays a
declared input; no new dark-matter particle species; the dark mass is still required.

## Verdicts

| Lane | Question | Verdict |
|---|---|---|
| [XR1](XR1_README.md) | Does every live verdict use one switch cell, footing, kernel and operator across its stages? | No live verdict mixes switch cells (L381, the only one, is withdrawn). The checker ([XR1_consistency_check.py](XR1_consistency_check.py), ~7 s) finds L381's mismatch from source alone; MUTATE rc = 1. Every p2_x2.0 result (L375, L377, L380, L373) sits on the cell DE1 excludes at canonical. The L388–L390 chain is one cell, **not yet one model**: four phantom operators, four switch-variable conventions, retention at z = 0 used at z = 0.4, canonical-only PM and Harvey, L376's RAR/RC100 on ν_RAR, two trigger branches. L372 scored KiDS switch-free (via L355) and Harvey at p1_x1.5. AT3's on-disk outputs predated its fix. |
| [XR2](XR2_fixed_cell_review.md) | Is DE1's p = 2 flagship failure right, and is L379's fixed-cell correction sound? | DE1 reproduced from scratch to 5.5e-8 (p_max 1.965/2.071). The failure is framework-internal: the flat-a₀ prediction is lost only for y = 0.100–0.110 at 37–39 kpc around 10¹¹ M☉ at z = 2.5, canonical only, beyond today's kinematics (r ≲ 12 kpc). At p = 1, x_c0 = 2.5 MOND stays on to y ≤ 0.1/18 for low-mass lensed discs at z = 1–2.5. **Branch mismatch:** DE1/DE2 read the phantom-inclusive density; the PM switch (L377:18, 119–120) reads matter only, so DE2's flagship pass does not transfer to L388. The fixed-cell correction is sound as a retention measure; the exact clearing estimator is particle-tracked (spec in §5). Lean I28 certifies the idealised mechanism only. |
| [XR3](XR3_obligations.md) | For the author's branch (ν_mono, criterion B), what is established, open, owned and orphaned? | Orphaned: the one covariant action (V0), the Dirac count, the gate varied at the MOND-normalised coupling, the smooth gate's own window, mixed heat-operator vertices (full G8), zero-field evolution, and the dark state at action level. Two cosmological architectures are live (the lead track's IC28 sector vs C-H/K + vacuum gate). Under criterion B the khronon is the global time function, so a dark state made of the clock's own dust would fold the foliation at stream crossing. Wording: ν_mono = ν_RAR only for y ≤ 2.337; the largest difference is 0.0104 dex; the four-form "Z" is not Z = 5.7888. |
| [XR4](XR4_data_gates.md) | Which decisive data tests are orphaned, and does the construction change standing liabilities? | **New tension:** the region kernel screens the external field that rescued the Local Group's zero-velocity radius; at p = 1, x_c0 = 2–2.97 the construction gives R₀ = 1.28–1.62 Mpc vs 0.96 ± 0.03 measured (+0.13 to +0.23 dex, both footings; one system, ~2–4σ, pipeline-dependent). The 09-03 EFE liabilities are **not** rescued (~4.5–6σ combined). Gas in active filaments at z ≲ 1 was never computed (order-one response expected; low-z forest and filament tSZ decide). The "~30 groups" R₀ test cannot be run (6–8 stable groups). |
| [XR5](XR5_README.md) | Does the PM force operator match the one L361's action gives? | Yes, at static-field scope: ≤ 2.2e-3 of the phantom monopole at 0.1–1 Mpc; Harvey \|Δβ\| ≤ 5e-5 between operators (≤ 1.8e-3 with g_e = ±0.01 a₀), against σ_β = 0.07. 13/13; MUTATE (no screening) fails S4 and X-SCREEN. What matters more: region labelling (a split merger pair reverses the phantom pull), the gate definition (absolute vs contrast moves edges 4.8–6.1%), and the far edge layer in projection (Δβ ≈ 0.009 on 2-D meshes; check on the 3-D maps). |

## Acted on by the owning sessions during the review

- `9092fc0fd` recipe and spec: kernel ν_mono, causality criterion B, Z corrected.
- `0b4e319b7` DE1 per-kernel edges (verdict unchanged); DE2's W3 note; DE3's cosmic-shear bound at p1_x2.5.
- `738216fbd` the four-form coupling renamed Z_q.
- `37edac81b` XC5: ν_mono's leaf problem is strictly convex at any positive lapse; the zero-field √ε response stays open.
- `8850550c4` merger lanes: L372 scope, L370 docstring, L373 scoped to p2_x2.0.
- `b3ba1f6fa` L390: KiDS at p1_x2.5.
- Cells aligned: AT3 and L388–L390 at p = 1, x_c0 = 2.5; L373 labelled p2_x2.0 only.

## Open decisions

1. The architecture of the one action: the C-H/K khronon + leaf average + vacuum gate + region kernel (XR3's
   recommendation), or the lead track's IC28 cosmological sector.
2. What the gate reads: the curvature-based, phantom-inclusive density (DE1/DE2, and the leaf curvature an action
   would use), or matter only (the PM runs).
3. Whether PAPER34 needs a v2 scope note on L372.
4. The same-cell re-runs (L373 two-mode, L372 re-score).

## Where to push next, in order

0. Freeze the architecture, the gate variable, the ν_mono splice and the cell.
1. Write the one covariant action and check its reductions.
2. Its Dirac count.
3. The gate varied at the MOND-normalised coupling, and the smooth gate's own window.
4. Full G8 with the filter's variation; a zero-field evolution estimate.
5. A dark state, at action level, that survives stream crossing and keeps the khronon a global time function.
6. One same-model particle-mesh run at the frozen cell carrying every hook: the particle-tracked clearing estimator
   (XR2 §5), z = 0.4 fields for Harvey, the alternative footing in one box, the chosen gate variable.
7. The construction's data-facing gates: active filaments at z ≲ 1; the flagship on the chosen gate branch; the Local
   Group zero-velocity radius and the EFE samples with a 3-D disc solve.
8. External data: Gaia DR4 (2026-12-02), Euclid DR1 (2027), the z ≈ 2.5 zero point (new JWST and ALMA time).

## Files

XR1–XR5 scripts, outputs and results JSON as listed in each lane's README. Re-run any lane from the repository root,
e.g. `python3 real_research/cross_thread_review_2026_09_26/XR1_consistency_check.py` (add `MUTATE=1` for its control).
The registry is a snapshot: re-run XR1's checker after any lane edit.
