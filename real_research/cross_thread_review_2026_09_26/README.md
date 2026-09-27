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

## Updates after the review (2026-09-26, evening)

**The author's decisions** (recorded in the recipe, `27bc6db4c`):
- Both architectures go ahead as separate branches, never pooled: the C-H/K khronon plus vacuum gate, and the lead track's IC28.
- "All doors" on the switch variable: each reading gets its own labelled cell.
- PAPER34 gets a v2 scope note once L372 has been re-scored at p1_x2.5.

**Ledger items closed:**
- `441d811e2` L391: RAR and RC100 re-scored with ν_mono. No change: carrier shift ≤ 1.24e-4 dex, carrier inside R_e 0.000 of ΛCDM's, f_DM 0.232/0.264.
- `77f79072c` L370 gains explicit-cell entry points; `8850550c4` scoped L372 and fixed L370's docstring.
- `27bc6db4c` XC4 confirms the ν_mono splice in closed form: y* = 2.3374, maximum difference 0.01037 dex. XC3's C_T is corrected, and every verdict holds.
- `9df26672f` L373 is committed, scoped to p2_x2.0: no window. Its only X-COP cell fails Harvey S2 at +0.116 against 0.10.

**The flagship on the matter-only branch is CGM-conditional** (DE4 `ecffd2af3`, DE6 `4132da393`). At z = 2.5:
- An intact carrier gives +0.97 dex, and L380's 6% residue +0.102.
- With the carrier cleared and 30% of L375's maximal CGM, every p ≤ 1 window cell keeps the flagship and every p ≈ 2 cell loses it.
- At 10% CGM only the p = 0.5 cells and (1, 1.5) keep it. **p1_x2.5 loses it.**
- On the matter-only branch the switch reaches 1.5–4.4 less in z than on the upper branch (z_max).
- Candidate to check on that branch: p = 0.5, x_c0 ≈ 2.65–3.39. That range sits inside DE2's cosmic-shear floor (600 km/s, L367's transfers) and its KiDS cap, but the forest is marginal at p = 0.5 (L359/L362). The branch's own T_max (DE5) decides it.

**New axis: the web self-term σ** (V0, `real_research/chk_v0_2026/`: CV1 `cc2b55bbb`, CV2 `db21f7edf`). σ is a physical edge choice: it moves the baryon force inside a region's edge layer by 0.8–1.4 g_N.
- L361's action and V0 use σ = 1.
- Every committed KiDS score (L352, L360, AT3; L361 R3 edgeless) and L370's Harvey use σ = 0.
- Scored since: σ is physical inside the thin edge layer but negligible for both observables. KiDS: σ = 1 passes wherever
  σ = 0 does on the curvature branch, |ΔΔχ²| ≤ 0.40 (DE8 `d522b1767`). Harvey: XR5's H1 already bounds it. With the
  far edge layer excluded, L361's operator at 1/m = 0.2/0.5 (σ = 1) and L370's (σ = 0) give the same substructure
  centroid to |Δβ| ≤ 5e-5 (`XR5_operator_identity.out`, H1). No 3-D σ = 1 Harvey lane is needed.
- **Correction (the orchestrator's misreading, not XR5's):** an earlier version of this section said XR5's σ = 1
  operator moved the centroid 4.1 kpc against 0.52 kpc for σ = 0. XR5 labels that 4.1 kpc as NOISE: the far edge layer
  of the Dirichlet limit on staircase meshes, varying from 0.06 to 6.5 kpc with the outer cell size. It is not a σ
  effect. L373's 3-D check bounds that layer at |Δβ| ≤ 0.0006 for L370's operator.

**Reported by owners, not yet committed when this section was written:**
- L388: 4/4, a pooled window at 575–650 km/s at p1_x2.5 on the matter-only branch.
- AT3 at p1_x2.5: every gate passes on the alternative set except cosmic shear, R = 1.47–1.58 (T(k=1) = 0.85–0.89 against T_max 0.76/0.72). A scan of the window has been requested.

### Late evening: the switch variable at action level, and cosmic shear

- **What the switch may read.** MS1–MS3 (`2a5def6d9`, `real_research/mond_sector_gate_2026/`) settle it.
  - MS1: once the gate is an action term, a switch that reads the dark carrier leaks a force onto it. Through curvature
    this is 0.06–6× the carrier's own gravity around an L\* lens; through matter density it is 0.6–60×.
  - The **MOND-sector reading**, baryons plus their phantom (U = C∇²(Φ − v)), leaks nothing.
  - DE7 (`095ab610a`) independently finds that a curvature-reading gate makes lensing differ from dynamics in
    transition layers. DE7 also proves that an unrepaired smooth gate is ill-posed on every transition, and that the
    lead track's Λ-scaled repair fixes the principal part.
  - MS2: with the MOND-sector switch the z = 2.5 flagship holds with no CGM at all. The unbound web needs 6.36× the
    matter reading's overdensity to switch on, which eases XR4's filament concern.
- **KiDS on each branch.**
  - The matter-only branch fails everywhere, at both σ (DE8 `d522b1767`; L392 `1eaac841b`).
  - The curvature branch passes (L392: −41/−34 and −60/−55, with Harvey +0.046..+0.062 on the alternative set).
  - σ is negligible for both KiDS and Harvey.
- **Cosmic shear is not established by any mock-based score** (MS3).
  - L363's region builder cannot grow a region from an isolated seed, and the 100 Mpc mock is cluster-poor. DE3/DE5's
    T_max, L388's shear pass (corrected in `c7de159cc`), AT3's shear numbers and L364's 1.12/1.17 are therefore not
    established.
  - On the resolution-free halo model every uncapped carrier fails (R 2.47–4.32).
  - Capping MOND regions at 1.75 Mpc (v_cap ≈ 325 km/s) with L388's density-trigger retention passes (1.05/1.12). The
    cap has no action yet.
  - AT3's galaxy-only clearing fails even when capped (AT1–AT3 `dd1d6a0d6`).
- **The candidate the threads now converge on (C-H/K branch):** the MOND-sector switch, the linear vacuum gate
  (p = 1, x_c0 = 2.5), a ~1.75 Mpc region cap and a density-triggered carrier that also clears groups and clusters.
  - L395's first cell tests it in the particle-mesh boxes, with shear scored on MS3's halo model.
  - V0's CV3 writes the gate with this reading.
  - Open: an action for the cap and for the trigger; the carrier as a state of the framework's own field; the Local
    Group zero-velocity radius and the EFE samples (XR4); Harvey's perpendicular orientation.

### Night: the converged model's scorecard (XR6, XR7 and the lanes since)

The model: the MOND-sector switch, read from constrained fields only (CV3): C[∇²(u−v) + ∇·((ν−1)∇Sw)]. It uses the
linear vacuum gate at p = 1, x_c0 = 2.5, with transition width w ≲ 0.25 (DE9). MOND regions are capped by MS3's
local rule, threshold × max(1, v_loc²/v_cap²) with v_cap ≈ 325 km/s. The dark carrier is density-triggered and
kicked at 575–650 km/s (L388).

| Gate | Status | Evidence |
|---|---|---|
| Flat-a₀ flagship, z = 2.5 | passes with no CGM | MS2 |
| KiDS-1000, carrier lensing included | passes: −37.0/−34.0 (hard), −32.3/−29.3 (w = 0.25) | DE10 `dabce1b73` |
| Cosmic shear, resolution-free | passes only with the cap: 1.049/1.124 (w 0.25), 1.025/1.096 (w 0.5, x_c0 3.0) | MS3, MS4 `969a15e7f` |
| RAR, RC100 | pass | L391 |
| Harvey | knife-edge, provisional: S2 passes only at 575 km/s; S1 at 575–625 | L389 |
| S₈, forest, clearing, X-COP | running | L395 → L396 (575 km/s) → L397 (Harvey at its own epoch) |
| EFE, cluster-infall BTFR | **worse**: 3.0–3.1σ (scalar), 4.9–5.5σ (subtract); the zero point improves to 0.0–2.2σ | XR6 |
| EFE, Local Volume dwarfs | **stands**: 3.9–4.5σ | XR6 |
| Local Group zero-velocity radius | **worse**: 1.41/1.48 Mpc, +0.17/+0.19 dex | XR6 |
| Coma UDGs | **stands**, weaker: 4.35/4.20σ, from 4.9/4.7σ | XR6 |

- **XR6's pincer.** The Local Group's R₀ needs an external field of about 2e-3 a₀ inside its region. That is about 20×
  what a KiDS-passing kernel transmits.
- **The EFE operator split.** On the EFE beyond the cap, the particle-mesh operator (all baryons) and the action's
  operator (screened) disagree.
- **XR7: the cap and the kick are two scales, not one.** The kick's 50% retention transition is at
  v_c ≈ 700–850 km/s, 2.2–2.6× v_cap. "v_cap ≈ v_k/2" is arithmetic between two hand-set numbers. MS3's
  step-at-the-cap row fails shear (1.64/1.74), so the two scales must stay separate.
- **Still posited, with no action:** the cap, the trigger and the kick. The author's direction (09-26):
  > we need to find out what the "Fluid" is.. which is not particles
  - XR8 runs the inverse specification and the shell-crossing test on non-particle continua.
  - Astra's new-sector conversion (Ψ, χ, s) is parked.
  - V0 bounds the search: CV4 finds the khronon's leaves are CMC inside bound regions, so the fluid cannot be the
    clock's own flow, and a wave-type fluid cannot take its phase from τ.

**Follow-up for the checker:** XR1's registry tracks the cell, footing, kernel and operator. It should also track the switch branch (upper/lower, contrast/absolute) and σ, so that pooling across either is flagged automatically.

### Morning 2026-09-27: the redirect, the six lanes, and the lanes serving the chain

- **The redirect.** At 22:40 the author stopped the triggered-carrier chain, because hand-set switch branches, caps
  and kicks add knobs instead of deriving them. The first-principles derivation chain
  (`real_research/derivation_chain_2026/`) now leads. Its target is no declared constant beyond κ = ½.
- **The six lanes (b667f56bb)**, all run to completion at the author's request:
  - XR11 closes the edge-layer reading of the dark fluid.
  - XR12: the fluid's own trigger fires in filaments; the forest sits at its 10% line; spin changes nothing.
  - XR13 closes the per-object region door (2 flips, 5 broken).
  - XR14: KiDS passes on M*'s carrier, the first validator row ON M* (c64766ca8).
  - XR15: neither repair door removes V0's gate obstruction, and CV3's determinant is gate-dependent as written.
  - XR16: the fluid's own conversion clears r_F at z = 2.5 through early escape; the forest is not established.
  - XR17 makes the flagship row's numbers a committed script.
- **Rows received:** DE11b (converged forest pass for the switch) and L389 (partial, uncontrolled). Stopped with no
  result: L393–L397 and AT5.
- **Now running here, for the chain:**
  - XR18: H_Y's well-posedness.
  - XR19: runaway conversion through the web.
  - XR20: a₀ and Λ from one field.
  - XR21: the chain's model in a particle-mesh box, staged and gated.
  - FP10_FULL.

  The answer page's §7 has the details.

## Files

XR1–XR5 scripts, outputs and results JSON as listed in each lane's README. Re-run any lane from the repository root,
e.g. `python3 real_research/cross_thread_review_2026_09_26/XR1_consistency_check.py` (add `MUTATE=1` for its control).
The registry is a snapshot: re-run XR1's checker after any lane edit.
