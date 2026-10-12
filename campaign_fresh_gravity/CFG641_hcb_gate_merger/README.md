# CFG640: H-CB (stars-only source) plus the deficit gate, in the merger stopwatch

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4b928d160), 2026-10-12.
- **Question:** if only condensed baryons (stars) source the law's phantom (CFG634's H-CB), and settling and relaxation act only
  where cold energy is missing (CFG639's gate), does the Bullet + Harvey merger allow an α ≥ 0.1, ideally the galaxy-preferred
  α ≈ 1? CFG623 (all-baryon source, ungated) allowed only α = 0.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed";
  nothing here says the data favour the framework.

## Status: QUEUED (no data run yet)

`run_640.sh` (nohup) waits until CFG639 Part B has finished, no 1024³ run is live and ≥ 16 GB is free, then runs `cfg640.py`:
controls → RN calibration → arm P → arm U → RI calibration → arm S → scoring. Expected cost: about 45 grid runs of about 13 min plus
two calibrations (about 20 short runs each) on 4 processes, about 4–5 h and about 10 GB. Log:
`../../../_external_data/cfg640_work/waiter.log` (outside the repo). Outputs `cfg640.out`, `cfg640_results.json`, `runs*/`.
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
| `cfg640.py` | the lane (CFG623/639 pipeline and CFG621 `calibrate()` imported read-only; progenitor, phantom field and calibration patches in-process) |
| `run_640.sh` | waiter |
