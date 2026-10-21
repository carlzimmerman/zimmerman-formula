# CFG952: the labelled-domain theory (LDT) as a PM-engine change-set, with 64³ smoke tests

**Lane label: SMOKE PARTIAL. The design needs revision on b1, c1 and c2.**
- **What works in the toy.** Labels assigned from the engine's catchment machinery persist through infall, and the own-domain
  phantom removes the external-field effect (EFE) that the engine's global phantom carries in the PM. A blended merge removes the
  instant jump at the trigger.
- **What fails.** The momentum-conserving ("dipole-slaved") source draw becomes infeasible under positivity in an asymmetric
  domain and in a major merger. A one-dynamical-time blend also exceeds the frozen per-step continuity line.
- **No production or medium run.** Nothing in CFG650 / CFG654 was edited or imported. A 1024³ LDT run is only drafted
  (`PREREG_DRAFT_1024.md`, not frozen).

**Settings and provenance.**
- **Criteria:** `FROZEN_CRITERIA.md`, 844ce293d, committed alone first.
- **A1** (pre-result, committed alone, before any script): 7a3ade021.
- **A2** (post hoc, committed alone, after K / MUTATE / MAIN; no grade change): 4141650f1.
- Block 950–959.
- κ = ½ FITTED. Footings never pooled. Cold energy; no particle species. Not "theory closed". Nothing here says the data favour
  the framework.

## Deliverables

- `DESIGN.md`: the change-set.
  - Switches and data structures.
  - Ingredient-by-ingredient engine changes with pseudo-code and the CFG654 engine's function names: (i) labels, (ii)
    own-domain phantom and its cost, (iii) the dipole-preserving draw and why it fails, (iv) the merge rule, (v) RMIN,
    (vi) the cold, (vii) diagnostics.
  - Memory and runtime at 1024³, the validation ladder, and the formulation (A) mapping.
- `PREREG_DRAFT_1024.md`: a draft of the first 1024³ run (LDT-B0), its statistic, control, readings, run order and the owner
  approvals needed.
- `cfg952_ldt_proto.py`: the separate 64³ toy prototype. Final sha256 6a5825c16ec2fbb1….

## Results (all from `cfg952_ldt_proto.py`; code units G = a₀ = 1, L = 40, 64³)

### K controls: ALL PASS

| id | check | result |
|---|---|---|
| K1 | PM momentum with no source; discrete third law | 2.2e-16; 5.6e-17 |
| K2 | isolated sub-box field vs truncated Plummer | 0.021 (line 0.03) |
| K3 | own phantom vs spherical QUMOND inside r_e | 0.013 (line 0.05) |
| K4 | ν_mono replica | monotone; 3.3e-9 vs the RAR ν for y ≤ 1 |

### Smoke tests

| id | result | grade |
|---|---|---|
| a0 | the catchment machinery gives host and satellite distinct labels (r_ON / r_e 9.56 / 3.42 and 6.07 / 1.62); purity 1.00000 for both at t = 0 and at all 41 refresh snapshots | **PASS** |
| a1 | the satellite's own phantom with every particle present equals the label-only computation exactly (0.0) at d = 12.0 / 7.97 / 5.01 | **PASS** |
| a2 | at the end of the infall (t = 15.6, d = 4.96): purity 1.0, a1 exact | **PASS** |
| b1 | DIPSLAVE: B/I = 80.9; infeasible from t = 2.56 (145 / 500 steps); dipole miss 0.83 | **FAIL** |
| c1 | RAMP: max J_Φ 0.94 (line 0.03); median 0.0096 | **FAIL** |
| c2 | RAMP: zero-sum max 0.49 (line 1e-12); book B/I 71 | **FAIL** |

**Reported for (a).**

| d | E4 global-phantom EFE (dex) | LDT-MASK residual (dex) | sub-box vs global satellite-only phantom (dex) |
|---|---|---|---|
| 12.0 | −0.009 | −0.003 | −0.047 |
| 7.97 | −0.025 | −0.001 | −0.025 |
| 5.01 | −0.114 | −0.014 | −0.030 |

- The last column is discretisation at an edge of 2.6 cells.
- The DIPSLAVE book closes in this gentle infall (B/I 2.8e-9).
- The baryon-vs-cold mean-acceleration difference of the satellite, |a_b − a_c|/|a_sat|, has median 0.068 and maximum 0.19. It
  includes internal forces that do not cancel between the two subsets, so it is not a hover measure.

**Reported for (b).**
- DIPFREE: B/I 0.79 (its expected residual, ∫F dt).
- The frozen linear draw (LIN) is infeasible from the first step (335 steps), with B/I 0.79.

**Reported for (c).**
- The merger triggers at t = 9.64 (separation 1.22; τ_m 3.51; r_e,C 3.51).
- J_Φ at the trigger is 0.025, against INSTANT's 2.77.
- MR1 (CFG947 M-R) bound fractions are 0.998 / 0.999 at the trigger, so M-R does not fire.
- The max J falls on infeasible steps (t = 28.6). Before the first infeasible step the max J is 0.011.
- The merged pair ends bound (separation 1.30).

### MUTATE: every tooth bites (exit 1 by design)

| tooth | result |
|---|---|
| Mu1 | E4 global phantom gives an EFE of −0.114 dex at d = 5.0 |
| Mu2 | E8 draw gives B/I 0.82 |
| Mu3 | INSTANT gives J_Φ 2.77 at the trigger (≥ 2 × RAMP's 0.94 frozen, and also ≥ 2 × the post-hoc 0.053) |
| Mu5 | without merging, the own phantoms over-count the union by ×1.35 inside r_e,C |

### Post-hoc stage (A2; FB-ZS = zero-sum-exact fallback on Newton failure; reported, no grade change)

| run | result |
|---|---|
| PH-b | B/I 6.47 with zero-sum 8.8e-13: the momentum the capacity-limited positive draw cannot carry |
| PH-c RAMP | max J 0.0534, inside the ramp window (0.023 before the trigger, 0.016 after the ramp); book B/I 2.26 |
| PH-c INSTANT | 2.77 at the trigger |
| PH-c NONE | max J 0.053 from motion alone; this pair separates (end 16.7) while the merged runs stay bound |
| PH-c DIPFREE | max J 0.053 |

**A2's declared reading rule** (RAMP ≤ 0.03 and INSTANT ≥ 0.05): **c1's frozen failure is NOT explained by the fallback
artefact.**
- The blend's peak per-step change is (π/2) × J_instant/N_steps plus motion. It cuts the jump 52× but stays above 0.03.
- The toy's own motion baseline (NONE) is already 0.053, so the 0.03 line was set below the toy's variability. This is hindsight;
  the grade stands.

### EST (engine-side design numbers; estimates)

**RMIN.** The engine's r_ON node grid makes the effective RMIN at 1024³ equal to **1.0471 Mpc/h** (×2.41 in M_ta), so
**M_b,ret ≥ 2.19e11 M⊙**. That is 4.5× CFG947's continuous 4.82e10, which is reproduced as a control. With native_cmb inputs it
is 2.13e11. At 256³ the node is 0.784 (4.79e10).

**Runtime and memory.** Against the NC1x baseline (16.27 h compute, peak RSS 44.33 GB):

| alive labels N_L | scheme | wall per footing | note |
|---|---|---|---|
| ≲ 5000 | exact3d or hybrid | 17–18 h | |
| 2e4 | exact3d | about 27 h | ragged batches |
| 6.3e4 (every peak) | exact3d | about 47 h | |

- Peak RSS is 42.8–47.1 GB with labels on disk.
- With labels in RAM the worst case is 51.4 GB: rejected, against the 52 GB abort line.
- `mask` costs +47 s per step and is not cheaper at small N_L.

## Design findings (details in DESIGN.md)

1. **Own-domain phantoms are cheap and correct in the PM.** Isolated sub-box solves per label replace E4's 11 full-box
   transforms. The engine's E4 carries a real EFE (−0.11 dex) that labels remove.
2. **Formulation (B) cannot conserve momentum with a positive shell draw** in asymmetric domains or mergers. The 𝒮-dipole demand
   exceeds the draw capacity. This supports CFG950's choice of formulation (A) for the engine (DESIGN §8). A 1024³ (B) run can
   test only the EFE fix plus labels (LDT-B0, with the momentum non-closure reported, as for class A).
3. **Merges.**
   - CFG947's M-R does not fire in equal-mass mergers, so CFG951's T_c or CFG950's r_dom is needed.
   - An overlap trigger fired at first passage of a pair that, without merging, separates. The merge itself changes the orbit.
   - A blend over one dynamical time removes the 110× jump but not the per-step change set by its length.
4. **RMIN at 1024³** is 2.4× higher in M_ta than the nominal value, because of the node grid, and differs from 256³.

## Disclosures

1. **A1 (pre-result).** Peak smoothing went from 1 to 2 cells, Jeans internal velocities were added, the merger got an approach
   velocity of 1.0, the DIPSLAVE draw became the positive exponential tilt (the frozen linear form kept as LIN), and two cadences
   were fixed. All of it came from paper estimates before any script.
2. **First MUTATE attempt killed by the 1 GB RSS guard (1.003 GB) during (c).** It is kept as
   `cfg952_MUTATE_firstrun_rssguard.out`.
   - Cause: macOS kept freed MALLOC_MEDIUM pages resident. The physical footprint was 0.05–0.14 GB.
   - Fix: the script re-execs itself with `MallocMediumZone=0` (an allocator setting) and calls malloc pressure relief (the class-A
     engine's own technique).
   - The Newton solve's BLAS matmuls (spurious Accelerate warnings) were replaced by elementwise sums.
   - K was rerun with identical lines. Mu1 and Mu2 equal the killed run's printed values.
3. **First MAIN crashed in the reported LIN variant** (an einsum bug); kept as `cfg952_firstrun_LINcrash.out`. It was fixed, and
   reporting-only diagnostics were added before the complete MAIN run. The (a) and (b) DIPSLAVE / DIPFREE lines are identical to
   the crashed run's.
4. **Post-hoc stage: three attempts.**
   - Run 1: the diverged Newton β was infinite, which gave NaNs (`cfg952_POSTHOC_firstrun_nanbeta.out`).
   - Run 2: the bisection bracket was too narrow for |β| ≈ 4e9, so zero-sum broke in PH-b and NONE
     (`cfg952_POSTHOC_secondrun_bracket.out`).
   - Final: the best finite iterate's direction, with a 41-point geometric magnitude grid and an adaptive bracket. This deviates
     from A2's literal "41-point grid in [0, 1] of β_last"; A2's aims (zero-sum exact, dipole best effort) are kept.
   - RAMP and INSTANT gave the same J in all three attempts.
5. **Final consistency run.** K, MUTATE and MAIN were rerun from the final script; the outputs are identical apart from timings
   and RSS. The post-hoc output was produced by the final script.
6. **Absolute paths** in the kept first-run outputs were replaced by relative ones.
7. **Toy constants** (ρ_ta, R_min = 2 dx, x_h = 0.6, truncations, particle counts, seeds 9521–9524) are declared in the criteria
   or code. x_h < 1 departs from the engine's E7 (q = 1) to give the draw headroom. Even so, b1 fails.

## Files and commands

Every stage runs one process on one core at nice 10, with the in-script 1 GB RSS guard. Peak RSS ≤ 0.25 GB; physical footprint
≤ 0.14 GB. Nothing was downloaded, no process touched, and no other lane edited.
- `CFG952_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg952_ldt_proto.py` → `cfg952_K.out`, `cfg952_results_K.json` (exit 0).
- `CFG952_MUTATE=1 …` → `cfg952_MUTATE.out`, `cfg952_results_MUTATE.json` (exit 1 by design).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg952_ldt_proto.py` → `cfg952.out`, `cfg952_results.json` (exit 0). This is MAIN plus
  the EST stage, which reads CFG654's Δ_ta JSONs, its ICs table and the NC1x run JSON (read only).
- `CFG952_STAGE=POSTHOC …` → `cfg952_POSTHOC.out`, `cfg952_results_POSTHOC.json` (exit 0).

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
