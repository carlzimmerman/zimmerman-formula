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
