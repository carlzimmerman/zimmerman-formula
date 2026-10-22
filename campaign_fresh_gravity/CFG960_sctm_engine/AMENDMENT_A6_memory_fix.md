# CFG960 AMENDMENT A6 (2026-10-22, PRE-RESULT): low-memory body painting, bit-identical; engine re-pin; footprint guard; SC1x resumes at step 89

Committed ALONE, before any further 1024³ CFG960 job. FROZEN_CRITERIA.md, FROZEN_CRITERIA_1024.md, its addenda A1/A2 and amendments
A1–A5 are not edited. Where this amendment and those files differ, this amendment governs. **The frozen reading, the scorer
(`cfg960_score.py`, unchanged, sha256 9a84005f…), the statistic, the data cuts, the classes and the verdict lines (FROZEN_CRITERIA_1024
§5–§6, addendum A1 §1 and A2) are unchanged.** No SC1x or SC2x snapshot beyond zi exists; no P(k) of either job has been seen.

**Approval.** The owner approved this route on 2026-10-22. Their words, in reply to the option "CFG960: a memory-fix amendment, or a
bigger machine", were: "yes to all". No bigger machine is available, so the memory fix is the route.

## 1. What happened (record: `doors_push_2026_10_22/D3_cfg960_status/README.md`)

- SC1x (canonical) started 2026-10-21 17:41 and was killed four times by its own frozen abort rule (swap growth > 4 GB, `run_960.py`),
  rc −9 each time. Try 0 died in step 81; tries 1–3 died in force call 90, a census refresh, after resuming from the step-89 checkpoint
  (a = 0.19). The chain stopped 2026-10-22 01:01 with all 3 resumes used. SC2x never started.
- The process footprint (which counts compressed pages) reached 51–65 GB on the 64 GiB machine; the `ps` RSS read by the 52 GB rule
  showed only 11–19 GB at each kill, because macOS compresses pages. The frozen §3 estimate (43–47 GB) was wrong.
- The partial run is VOID under V3 (only the zi snapshot exists). It carries no verdict on either footing.

## 2. Where the memory went (measured, not estimated)

A diagnostic replay of force call 90 ran the **frozen** engine (sha256 e1fe3b3d…74d5) on the intact step-89 checkpoint. Particles were
memory-mapped read-only (so only the step's own allocations count), kicks and drifts were disabled, and the replay stopped after the
step. It is not a run: nothing from it enters any record except the memory figures and the body counts below. The live-allocation
peaks (tracemalloc) per stage, on top of the 25.8 GB of particle arrays the production process holds, were:

| stage | frozen engine (GB) | A6 engine (GB) |
|---|---|---|
| all-particle deposit | 11.4 | 11.4 |
| census cover (`cover_peaks` / `cover_balls`) | 13.4 | 13.4 |
| partition / refresh pass | 4.8 / 3.1 | 4.8 / 3.1 |
| profiles / merges | 2.6 / 10.1 | 2.6 / 10.1 |
| **body painting (S6/S7)** | **18.8** (8.4 GB of point arrays then held through the force call) | **4.9** |
| **body CIC deposit** | **> 37** (the replay's own footprint passed 38.9 GB and it stopped itself) | 10.6 (incl. the 8.6 GB mesh) |
| M3 / Poisson / accel | not reached | 6.0 / 10.2 / 11.1 |
| **replay process footprint, maximum** | > 38.9 (aborted) | **13.4** (external 0.5 s sampler, `memory/replay_call90_A6_engine_footprint_series.json`) |

Call 90 paints 1 117 863 bodies with **176 234 305 inner CIC points** and 7 477 194 outer mesh nodes. The frozen `body_points` builds
every point at once (position, mass and owner: 40 B per point), and `deposit_points` and the accel pass then make full-length CIC
temporaries over all of them (about 150 B per point). That is the 25.8 + ≈ 37 ≈ 65 GB footprint in `watch.log`. Nothing else in the
step comes close.

## 3. The change (engine `cfg960_sctm_pm.py`)

- **`body_shells`** runs `body_points`' S6/S7 + A3/A4 arithmetic statement for statement. Instead of materialising points, it records
  each inner shell as (body, mid radius, n_a, rotation index k, per-point mass ΔM/n_a); the A4 fallback shell is recorded with rotation
  index −1 (unrotated). The point bodies and the outer mesh nodes are kept exactly as before. At call 90 that is 2 631 164 shell
  records instead of 176 M points.
- **`shell_points`** regenerates the points of a contiguous range of items, in `body_points`' order, with the same elementwise
  expressions (`X_q + r̄ (v₀ cos θ_k − v₁ sin θ_k, v₀ sin θ_k + v₁ cos θ_k, v₂)`, `% L`; mass `ΔM/n_a × mut`; θ_k = k × golden angle
  via `math.cos` / `math.sin`, as before).
- **`deposit_shells`** = `deposit_points`: CIC corner-major, and within a corner the points in their original order, in blocks of
  about 2²¹ points (`CFG960_SH_BLOCK`; memory only).
- **The accel pass** interpolates the body points block by block. The blocks never split a body, so each body's force sum `bincount`
  is formed inside one block, in the original order. The other blocks add +0.0 to it.
- **The painted-mass book** sums the same full per-point mass array as before (built transiently, 1.4 GB at call 90).
- **On a resume** the run JSON now records the engine of every segment: `engine_sha256_segments` = [[0, sha of the first segment],
  [n_done, sha now], …], and `engine_sha256` = the current engine.
- `body_points` and `deposit_points` are kept unchanged, because `cfg960_law.py` uses them (V-LAW).
- **`CFG960_SHELLCHECK=1`** also runs `body_points` at every step and asserts that the regenerated points, masses, owners, nodes, r_e
  and diagnostics are byte-identical. It is used in validation only.

**Unchanged:** every rule S1–S13, U1–U13, A3/A4/A5; the CFG654 engine (imported read-only, sha asserted); the checkpoint format
(particles, f_d, labels, domain table, meta). No precision changes: no float32 is introduced anywhere.

### Why the output is bit-identical (the argument; §4 is the test)

1. **Points.** Each regenerated coordinate and mass is the same IEEE operation on the same operands as in `body_points`. Separate
   numpy ufunc calls are not fused, and the elementwise functions used here were checked to be position-independent on this machine
   (shift and chunk tests on log10, exp, cube, sqrt and expm1).
2. **Deposit.** `np.add.at` is unbuffered and sequential in index order. Splitting one corner's point list into consecutive blocks
   therefore keeps every cell's summation sequence, and the corner order is kept.
3. **Force.** A body's points are consecutive items. A block boundary never falls inside a body, so `bincount` forms each body's sum
   from 0.0 in the original order, and x + 0.0 = x exactly.
4. **Book.** The painted sum runs over a byte-identical array of the same length and layout.

## 4. Equivalence evidence (`A6_equivalence/`; same ICs, seed 359, native_cmb, lean, SPILL on, checkpointing on)

| test | result |
|---|---|
| 128³, 1 thread, A6 vs frozen, SHELLCHECK on every one of 151 force calls | **bit-identical**: all 3 922 JSON numbers (P, P_grav, σ, book, events, SCT diagnostics) and all 25 npz arrays (density / gravitating meshes, domain table) |
| 128³, the same with 1 000-point blocks (≈ 69 blocks per step) | **bit-identical** |
| 128³: **resume** — frozen engine to step 89 and its checkpoint, then the A6 engine from that checkpoint to z = 0, vs the frozen engine straight through | **bit-identical** (all 3 922 numbers, 25 arrays); `engine_sha256_segments` = [[0, e1fe3b3d…], [89, d1486fcc…]] |
| 256³, 4 threads, 20 000-point blocks, SHELLCHECK on every force call, A6 vs frozen | every book entry, event, domain table, density and gravitating mesh field, SCT diagnostic and **P_grav at every snapshot bit-identical**. The particle P(k) / σ of one snapshot (x0.2562) differs by ≤ 4.17e-8 relative |
| 256³, 4 threads, **frozen engine vs itself** (two identical runs) | the particle P(k) / σ of z1, x0.2562 and z0 differ by up to 4.17e-8 relative; everything else is identical |
| 1024³ real data (step-89 state, call 90; 9 982 bodies: the 3 000 most massive + 7 000 random; 7.6 M points, 4.8 M outer nodes, 2 943 outer bodies; 150 blocks) | regenerated points, masses, owners, nodes, r_e, diagnostics **and the full add.at index / weight streams of all 8 CIC corners byte-identical** to `body_points` + `deposit_points` |

**Reading.** The A6 engine reproduces the frozen engine bit for bit in every evolved quantity. The one difference at 256³ is a
pre-existing measurement jitter of the frozen engine with more than one thread. It appears between two frozen runs as well, at the
same size (4.17e-8), and it touches only the particle-P(k) measurement of a density mesh that is itself byte-identical. That is the
"measurement-level last-bit effect" that V2 already allows for. It has no feedback on the dynamics: the next snapshots agree bit for
bit. The verdict uses P_grav (framework) and NCS0's stored P(k) (control), and both are untouched. **Tolerance for V2 and the record:
0 in every evolved quantity; ≤ 1e-7 relative in a particle-P(k) measurement, the frozen engine's own run-to-run spread.**

## 5. New memory estimate and its basis

- **Basis.** The A6 replay of call 90 had a process footprint of at most **13.4 GB** above the particles: the census cover, which is
  mesh-bound and present at every refresh since step 0. Adding the 25.8 GB of particle arrays gives **≈ 39–41 GB at call 90**, against
  ≈ 65 GB for the frozen engine. The production `watch.log` showed 40–41 GB in the cover stage in every try, which confirms the
  baseline.
- **Projection to z = 0.** The domain-count stages scale with the number of live domains: merges 10.1 GB, profiles 2.6 GB, painting
  4.9 GB. The other stages are mesh-bound and constant.
  - Births peaked between refreshes 80 and 90 (788 086 and 758 233). At 256³ the live count peaked about 1.4× above its value at the
    birth peak.
  - Allowing 1.6×, merges ≤ 16 GB and painting ≤ 8 GB, so the per-step peak is **≈ 40–44 GB per footing** (SC1x and SC2x alike).
  - The inner-point count no longer matters: points exist only in blocks of about 2 M.
- This is an estimate, not a result. The run's own `watch.log` footprint column is the record.

## 6. Runner and guard (`run_960.py`, re-pinned)

- **Unchanged:** the frozen abort rules (ps RSS > 52 GB; swap growth > 4 GB; disk < 3 GB), the in-engine RSS guard (52 GB), the start
  gate in `chain960.sh` (no heavy job; no other python process > 1 GB; free + inactive ≥ 46 GB; free disk ≥ 45 GB) and
  `chain960.sh` itself (sha256 eb8925d9…, unchanged).
- **Added, a tightening only:** the launcher also kills the job if the process **footprint** exceeds 52 GB. That is the 52 GB rule
  read through the measure that counts compressed pages on macOS. Nothing is loosened.

## 7. Resume from the step-89 checkpoint

SC1x **resumes from its step-89 checkpoint** (`_external_data/cfg960_work/SC1x/…_ckpt`; n_done 89, calls 90).
- **Format.** The checkpoint holds only engine-version-independent state: particle positions and momenta, f_d, labels, the domain table
  and the meta/res record. Body shapes are rebuilt from that state at every force call.
- **Pins.** Its four pinned files still match addendum A1's sha256 values (checked 2026-10-22).
- **Evidence.** The 128³ resume test in §4 shows that a frozen-engine checkpoint continued by the A6 engine is bit-identical to the
  frozen engine straight through.
- **Resumes.** The re-launched chain starts a fresh resume counter: up to 3 checkpoint resumes per job, as frozen. Every resume
  (including this one) is logged in `chain960.log` and in `resumed_after_step` of the run JSON, and is disclosed.
- **SC2x** starts from zi under the A6 engine.

## 8. Re-pins (replacing addendum A1 §3 for these files) and V1

| file | sha256 |
|---|---|
| `cfg960_sctm_pm.py` | d1486fcc56c6f5e8c6ee8457345445cc444ef2889f7d417ff9c14db4024599f0 |
| `run_960.py` | f243fc50ec0168cb00d93df9e97c1811689b20d7dd99d06461314b13246ede9a |
| `chain960.sh` / `cfg960_score.py` | unchanged (eb8925d9… / 9a84005f…) |
| CFG654 engine / CFG654 scorer | unchanged (7058f433… / e5e3da3b…), asserted at import |

**V1 (VOID), amended.** A run is VOID unless all of the following hold:
- its JSON `engine_sha256` = d1486fcc…99f0;
- every segment in `engine_sha256_segments` is d1486fcc…, except a first segment [0, e1fe3b3d…74d5] that ends at step 89 (SC1x only);
- `sct.own_baryons` = "census f_ret (A5 primary)".

V2–V4 are unchanged; V2's measurement-level allowance is as stated in §4.

## 9. Disclosed

- Seen before this amendment:
  - the frozen and the A6 replays of call 90 (memory, timings, and the refresh / merge / body counts quoted above: 758 233 births,
    313 k merges, 1.12 M bodies; mass error 2.2e-16);
  - the 128³ and 256³ equivalence runs.
- The 256³ P(k) values were compared for identity only. They were not examined, plotted or reported as a preview, and they are NOT A
  VERDICT.
- Cost.
  - The A6 painting regenerates the body points 8 times for the deposit and 3 times for the accel in each step.
  - The replay (tracemalloc on, particles read from disk) is not a timing benchmark.
  - Expected: about +1–3 min per step at 1024³, so SC1x's remaining 61 steps take about 8–11 h and SC2x about 20–32 h.

κ = ½ FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed.
