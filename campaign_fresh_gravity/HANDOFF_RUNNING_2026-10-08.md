# Handoff: lanes in flight on 2026-10-08 (for any session that resumes later)

Read this first if you pick up after a break. Compute jobs run detached on the local machine and survive the session ending. Agent-driven theory lanes stop if the session ends; resume them from their committed FROZEN_CRITERIA.md.

## 1. Detached compute (keeps running without a session)
| lane | process | outputs land in | when finished, run |
|---|---|---|---|
| **CFG460**: zero-knob growth at 512³, second realisation (seed 360) | `run_460.py` (detached); S0 done, TA running | `../_external_data/cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json` | `python3 campaign_fresh_gravity/CFG460_zero_knob_512_second_seed/cfg460_analysis.py`, then write the README and commit |
| **CFG487**: settled-fraction switch, 256³ growth runs | `run_487.py 256` (detached) | `campaign_fresh_gravity/CFG487_settled_fraction_switch/` + `../_external_data/` per its `cfg487_pm.py` | `cfg487_growth_analysis.py`, then `cfg487_verdict.py` |
| **CFG468**: kernel family, zero-field grid (120 specs, N ≤ 1023) | `cfg468_zero_field_runs.py`, guarded by `watchdog_468.sh` (detached; relaunches it if it dies; resumable, finished arrays are skipped) | the arrays per the script; log `CFG468_kernel_family/cfg468_run.log` (watchdog notes in `.watchdog`) | the lane's analysis in `cfg468_kernel_family.py` per its FROZEN_CRITERIA.md |

Check what is running: `pgrep -fl "run_460|run_487|cfg468_zero_field|watchdog_468|cfg4[0-9][0-9]_pm"`.
Only one 512³ job fits in memory at a time.

## 2. Agent lanes (stop if the session ends; resume from frozen criteria)
| lane | question | state at handoff |
|---|---|---|
| **CFG489** | NC1 = GR + Λ gravity with the MOND law only in the cold fluid's (dissipative) dynamics: well-posedness, attractor, energy, Sun capture | criteria + scripts started; no verdict yet |
| **CFG490** | the G9-violating arm: one direct baryon–cold coupling delivering supply + edge + temperature; experimental bounds (EP, Cassini, pulsars, Bullet, CMB/BAO, DR3 no-EFE) | started; no verdict yet |
| **CFG487** | settled fraction as the switch, V1 (MS1 exception) and V2 (baryon-only clock) | data + well-posedness + Lean done; growth running (above) |
| **CFG468** | kernel family (SPARC + zero-field) | SPARC part done; grid running (above) |

To resume an agent lane: read its FROZEN_CRITERIA.md and any committed outputs, then continue under the same frozen rule. Never edit the frozen text; add dated disclosures instead.

## 3. Decisions waiting on the owner
- **Chassis:** option A (lenient black-hole reading; CFG469 WORKS-CONDITIONAL) or option C (retire the chassis). Option B (UV constant) FAILS.
- **Foundation charter** (`foundation/PROGRAM.md`, draft v0.1): "not yet" on 10-08. Keep exploring first.
- **JWST NIRSpec IFU inventory:** the owner runs `python3 jwst_ifu_inventory.py` in `../_external_data/cfg435_work/`; then pick programmes and run `jwst_ifu_download.py`. Both scripts are outside git.
- **Downloads flagged by CFG465** (globular raw velocities, Harris 2010): need the owner's go.

## 4. Where the theory stands (10-08)
- **Growth:** the zero-knob rule passes 15/15 (PAPER45 v2.1, DOI 10.5281/zenodo.23240853). Its supply postulate cannot be derived under G9:
  - CFG461: no G9 mechanism sets the temperature;
  - CFG462: the lapse cannot make the edge;
  - CFG488: the per-galaxy supply needs a shared baryon–cold label.
  - CFG490 tests the coupled arm.
- **Tension:** the 5.85 r_M edge fails early-type lensing levels (CFG485 caveat 2; CFG398).
- **Artefacts found by re-checks:** CFG429 (now CFG464, NOT EXCLUDED); the CFG358 scope (chassis only); CFG465 globulars (unsourced Pal 3).
- **Confirmed real:**
  - CFG466: SLUGGS centrals fail with stars only; marginal with ownership and orbit-dependent;
  - CFG467: α_c tension.
- **Not diagnostic:** CFG463 (UFD infall), CFG433 (MW satellites), CFG437/438 (BX442).
- **Ready for the owner:** the Keck one-page figure (`explainers/img/keck_osiris_bx442_summary.png`); a private ALMA/VLA draft (`../_external_data/proposals/`).

## Update 2026-10-09 (late): running and queued
- **Running:** CFG530 (512³ fixed-box convergence; L200 canonical = TENSION 0.113, core R 1.14; L100 512³ pending), CFG539 (cold-energy EoM, Stage 2 two-species PM), CFG541 (precise equations: variational origin, edge, energy sink, causality), CFG468 (kernel grid).
- **QUEUED (owner said yes 10-09):** CFG542, a dissipative variational principle for candidate B. Launch it AFTER CFG541 reports, building on its Onsager result. It needs one principle (Onsager / Schwinger–Keldysh / a partner field absorbing the settling energy) that yields the CFG539 class-A drift, the energy sink, and a covariant local definition of "bound" (the switch, Gap 1). No knobs; frozen criteria first.
- **Theory statement:** THEORY_v1_2026-10-09.md. **Assessment:** ASSESSMENT_2026-10-09.md.

## Update 2026-10-10 (owner away ~5 h): the plan
- **Running:** CFG557 (derive the settling catchment, the lever for the intrinsic growth excess, CFG556) and CFG558 (velocity part: isotropy forced?, overfill removal, α-robustness).
- **Next, automatically:**
  - If CFG557 derives a catchment that passes growth (halo model) and does not break groups, KiDS, MW and LG, AND CFG558 gives a derived velocity part: launch CFG559, the two-species PM with the derived catchment and velocity relaxation. Test at 256³ then 512³ on the GRAVITATING field (CFG555 statistic), both footings.
  - If CFG557 fixes growth but breaks another test: launch a lane on that conflict (mechanism + data check).
  - If CFG557 is NOT DERIVABLE: write the minimal postulate set honestly into Theory v1.
- **Waiting on the owner:** "publish" for PAPER45 v2.2 (prepared, audit 44/44, commit e19da03d0); DES ΔΣ (not public); 100 GB DES shear (needs a yes).
- **2026-10-10 16:2x: CFG468 kernel grid PAUSED (SIGSTOP; watchdog 57207 also stopped) at owner request, to free CPU for CFG596. Resume with: kill -CONT $(pgrep -f cfg468_zero_field_runs.py) 57207**
- **2026-10-10 late: CFG596 production running** (1024³ L100: S0 → LRcan → LRalt; ETAs about 10-11 14:00 / 10-12 10:00 / 10-13 06:00). No checkpoints (disk was about 20 GB free). After P1 finishes, from campaign_fresh_gravity/CFG596_lean_pm_1024/ run `CFG596_MUTATE=1 nice -n 10 python3 cfg596_native.py` then `nice -n 10 python3 cfg596_native.py`, and commit. Caffeinate extended to 96 h.

- **2026-10-11 10:56: CFG596 P1 (RES canonical 1024³) ABORTED by its frozen swap-growth guard** (+5.1 GB swap) after ~4 h, while CFG623/CFG624 lane jobs competed for RAM. P0 (S0) is complete. A watcher (`_external_data/cfg596_work/relaunch_p1.sh`, log `relaunch_p1.log`) relaunches `run_596.py serial P1 P2` once lane RSS < 3 GB and free+inactive ≥ 42 GB; the aborted folder is kept as P1_aborted_1056. New ETAs: P1 ≈ 27 h after relaunch, P2 ≈ 20 h after that. Lesson: no lane job above a few GB while a 1024³ run is live.
- **2026-10-11 12:42: CFG596 P1 relaunched** (then P2); ETA P1 ≈ 2026-10-12 16:00. **CFG625** driver `_external_data/cfg625_work/drive.sh` runs one ~1.4 GB process at a time (waits if free+inactive < 6 GB); 10–20 h. When `cfg625_summary_results.json` appears: commit the phase outputs in CFG625_merger_baryon_inputs/, write its README (disclose the τ density-floor star-cusp dependence), delete the logs, fold into the assessment.
- **2026-10-11 21:xx overnight plan:** P1 (step ~100/150 at 20:36) → a background waiter runs `CFG596_MUTATE=1 cfg596_native.py` then `cfg596_native.py` automatically when the launcher logs `P1 rc 0` (outputs cfg596_native*.out/json in the lane; MUTATE exit 1 = all controls bite). P2 (alt) starts automatically after P1. NEXT HEAVY JOB after P2: the CFG634 H-CB native PM run (spec in CFG634 README; ~29 GB; must run alone; build cfg634_pm.py with the bit-for-bit reproduction control first). CFG625 driver continues one ~1.5 GB process at a time.
- **2026-10-12 07:56: CFG636 (H-CB native 1024³ shear test) QUEUED.** Criteria 89aeaae12; 256³ validation PASS (V-R bit for bit vs CFG596 VLr; V-H smoke differs; preview NOT a verdict). Waiter `_external_data/cfg636_work/cfg636_waiter.sh` (PID 90955, log `cfg636_waiter.log` there) polls every 2 min and starts `run_636.py serial C1` (H-CB canonical) automatically once CFG596 P2 has ended (no `cfg596_pm.py`/`cfg636_pm.py` process) and free+inactive ≥ 42 GB; it kills nothing. P2 at step 110/150 at 07:56, so C1 should start ≈ 11:30–12:30 and finish ≈ 12 h after start (≈ 10-13 00:00–01:00). Then, from CFG636_hcb_native_1024/: `CFG596_MUTATE=1 nice -n 10 python3 cfg636_native.py`, then `nice -n 10 python3 cfg636_native.py`; alt C2 by hand later (README).
- **2026-10-12 21:23: CFG640 H1 ABORTED by its swap-growth guard** (+4.5 GB swap) at step ~10, with several light lanes plus another session's multi-process CFG641 (~5.6 GB) and a large git worktree checkout running. The CFG650 waiter (job T12) now starts next when free+inactive ≥ 48 GB; T1 is chained after T12. CFG640 to be rerun later (`run_640.py serial H1` after moving H1 aside).
