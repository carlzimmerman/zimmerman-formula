# CFG641 (renumbered from CFG640): H-CB (stars-only source) plus the deficit gate, in the merger stopwatch

> **Renumbering (2026-10-12).** This lane's criteria were committed as "CFG640" (4b928d160) in `CFG640_hcb_gate_merger/`. The
> orchestrator independently committed a different lane under the same number six minutes later (71b2cc1c9,
> `CFG640_phase_source_pm/`, the 1024³ phase-source shear test), from its own ID block. History is not rewritten: this lane
> moved to CFG641 by `git mv`. `FROZEN_CRITERIA.md` is unedited and still says "CFG640" in its text; it is this lane's
> criteria. No run had started when the lane was renamed.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4b928d160), 2026-10-12.
- **Question:** if only condensed baryons (stars) source the law's phantom (CFG634's H-CB), and settling and relaxation act only
  where cold energy is missing (CFG639's gate), does the Bullet + Harvey merger allow an α ≥ 0.1, ideally the galaxy-preferred
  α ≈ 1? CFG623 (all-baryon source, ungated) allowed only α = 0.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed";
  nothing here says the data favour the framework.

## Status: DONE (2026-10-12 → 2026-10-13 01:32), VALID — see Result below

### (original status note) QUEUED (no data run yet)

`run_641.sh` (nohup) waits until CFG639 Part B has finished, no 1024³ run is live and ≥ 16 GB is free, then runs `cfg641.py`:
controls → RN calibration → arm P → arm U → RI calibration → arm S → scoring. Expected cost: about 45 grid runs of about 13 min plus
two calibrations (about 20 short runs each) on 4 processes, about 4–5 h and about 10 GB. Log:
`../../../_external_data/cfg641_work/waiter.log` (outside the repo). Outputs `cfg641.out`, `cfg641_results.json`, `runs*/`.
Nothing commits them automatically.

## Pre-run disclosures (2026-10-12, before any data run; not verdict inputs)

- **Smoke test (code check only).** One process, 1.8 GB peak: SimH built for arm P's configuration (stars, RN, gate, α = 0.1,
  CFG623's calibration), two steps taken. Numbers seen:
  - progenitors (canonical): main settled 1.533e14 M☉ + reservoir 1.042e15 M☉; sub 4.23e13 + 7.73e13;
  - stars-only phantom field 1.96e14 M☉ against 4.47e14 M☉ for the all-baryon field;
  - **at t = 0, 299983 of 300000 cold elements (99.99%) are gated off.**
- **What that means for the reading (stated before the run).** Under RN the cluster already holds more cold energy than the
  stars-only phantom asks for, so the gate leaves almost all of it collisionless. Arm P is therefore expected to behave close to
  α = 0 at every node.
  - If VH-1 comes out "RESCUES", the honest reading is that **an unsettled, collisionless reservoir holding about 87% of the
    main cluster's cold energy passes the Bullet**. That is close to the standard collisionless-halo picture. It is a statement
    about CFG634's RN reservoir, not evidence for the settling dynamics, and it must not be presented as a framework success.
  - Arm U (no gate) and the two-sided drift push the overfilled cold energy out at rate α, so P vs U should differ (tooth T-G).
  - The reservoir itself is not derived (CFG634 bracket; CFG637 is deriving it in another session).

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (4b928d160) |
| `cfg641.py` | the lane (CFG623/639 pipeline and CFG621 `calibrate()` imported read-only; progenitor, phantom field and calibration patches in-process) |
| `run_641.sh` | waiter |

## Result (`cfg641.py` → `cfg641.out`, `cfg641_results.json`, `cfg641_calibration_RN/RI.json`, `runs*/`)

**Controls:** C-R0 and C-R1 reproduce CFG623's `a0_can` and `a0.1_can` exactly (0 kpc); T-H 0.448 / 0.442 (pass); **T-G bites**:
99.96% of cold settle steps gated off in the pericentre window, |f_P − f_U| = 0.72, |β̄_P − β̄_U| = 0.63. Calibrations: RN v0 1479 km/s,
η 1.442 (speed 2774 km/s, d_SG 176 kpc); RI v0 1000 km/s, η 1.442 (2723 km/s, 177 kpc). Footings valid in every arm.

| arm | result (both footings) |
|---|---|
| **P** stars, RN, gate | **every node EXCLUDED, including α = 0**: Bullet f +0.142 / +0.113–0.130 (Z_B +0.8 / +0.5–0.7, fine) but Harvey β̄ +0.177 / +0.162 (**Z_H +3.1 / +2.9**). α-independent (gate off) |
| U stars, RN, no gate | α = 0 as P (EXCLUDED); α ≥ 0.03 large offsets (f 0.40–1.53), UNSCORABLE or EXCLUDED |
| S stars, RI, gate | **every node ALLOWED**: f −0.008 (Z_B −0.42), β̄ −0.023 to −0.027 (Z_H +0.18 to +0.25). α-independent (gate off) |

**Frozen verdicts:** VH-1 (arm P) **DOES NOT RESCUE** (α = 0 no longer allowed); VH-2 allowed set []; VH-3 **NO RESCUE EITHER WAY**;
VH-4 **RESERVOIR-DEPENDENT** (arm S rescues).

**Reading (the pre-run disclosure applies).**
- With the stars-only source the reservoir already exceeds the phantom everywhere, so the gate switches settling off and **α plays no
  role**. Neither arm tests settling dynamics; both test the unsettled reservoir's profile.
- **RN (diffuse NFW, c = 4)** fails Harvey: with only stars sourcing the settled mass and the reservoir diffuse, the gas pulls the
  lensing peaks toward the plasma across the sample (β̄ +0.17 vs −0.04 ± 0.07).
- **RI (reservoir tracing 5.364 × the enclosed baryons)** passes both Bullet and Harvey: a collisionless component concentrated like the
  baryons keeps the lensing on the galaxies. This is the collisionless-reservoir statement the disclosure warned about, not evidence
  for settling.
- **Across lanes, no single reservoir rule passes:** CFG634 (static) found RN passes X-COP including the inner band while RI fails the
  inner band (η 1.535); CFG641 (dynamic) finds RI passes the mergers while RN fails Harvey. CFG634's "NO SINGLE RESERVOIR RULE" now holds
  for static and merger tests together. A derived reservoir (CFG637, another session) is what could break this.
