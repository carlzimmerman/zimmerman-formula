# CFG640 FROZEN CRITERIA: condensed-baryon source (H-CB) plus the deficit gate, in the merger stopwatch

Date: 2026-10-12. Written and committed ALONE, before any CFG640 code exists and before any CFG640 simulation. Nothing below may
be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. The footings (9.3603e-11 canonical, 1.1312e-10 alt) are judged separately and never pooled. The cold energy's
mass is required (an input). No particle species. Not "theory closed". Yardsticks are raw data only (CFG623's D1–D3). Nothing will
be phrased as "the data favour the framework". No knob scans.

## 0. What has been seen (stated before any choice below)

- CFG623 (VALID): allowed set {0} on both footings; α = 0.1, 0.3, ∞ EXCLUDED; V-3 INCOMPATIBLE.
- CFG634 (H-CB, static): NOT DECIDED (reservoir-limited). T3 X-COP: R0 FAILS (η 3.97 / 3.81); RN c = 4 PASSES with the inner
  band; RI PASSES at the headline radius, inner band fails. T4a: H-CB's settled mass is never gas-tied. T4b Bullet aperture
  Δκ: R0 FAIL, RI TENSION, RN TENSION (B1) / PASS (B2, B3).
- CFG639 Part A (galaxy side of the gate): NOT DIAGNOSTIC as frozen; post hoc the gate acts, IC-B passes 4/4, IC-C not steady
  0/4. CFG639 Part B (gate alone, merger grid) is queued and **not yet run**; no Part B number has been seen.
- CFG637's criteria (derived reservoir, in progress in another session; not used here) and the assessment note 6815ab246
  (CFG636 tests a uniform census cap, not a phase-sensitive source).
- One static number computed for this file (no simulation): in CFG599's progenitors the stars-only phantom inside r_t is 0.448 /
  0.442 (main, can / alt) and 0.403 / 0.401 (sub) of the all-baryon phantom. The RN supply is 5.364 M_b (1.196e15 / 1.196e14 M☉).

**Author's expectations, written before any run (not verdict inputs):** without hot gas in the source, the lagging plasma no
longer creates a deficit, so the gated drift should stop pulling cold energy toward the gas. If the merger side is rescued
anywhere it should be here. The risks: (i) the reservoir changes the mass model, so the calibration may fail or land far from
CFG621's; (ii) a large collisionless reservoir may by itself place the lensing peaks; (iii) RN and RI may disagree.

## 1. The model (changes from CFG623's pipeline; everything else is CFG623's code imported read-only)

1. **Source (H-CB, CFG634).** The law's phantom is sourced by condensed baryons only: in this model, the stars. Hot ICM (grid
   gas) and the sub's cool-core cloud are hot phase (CFG634's Bullet split: hot = ICM + cool core, condensed = stars). Applied
   (a) to the progenitors' settled profile (stars-only phantom, truncated at r_t as in CFG599), and (b) to the settle step's
   phantom field during the run (stars-only particles; no gas grid, no cloud). All real mass gravitates (G9), including gas,
   cloud, settled and reservoir cold energy; the OU Jeans target keeps CFG599's all-mass form.
2. **Reservoir (CFG634 brackets).** The cold energy that is not settled is ordinary collisionless cold matter, sampled as cold
   particles with Jeans–Maxwell velocities in the progenitor's new total mass.
   - **RN (primary):** reservoir mass = 5.364 M_b − settled, distributed NFW with c = 4 inside r200 (CFG629 / CFG634).
   - **RI (secondary):** cold(<r) = max(settled(<r), 5.364 M_b(<r)), reservoir = the difference (CFG634).
   - R0 is not run: CFG634 T3 excludes it statically (η 3.97 / 3.81).
   - Progenitor gas pressure is recomputed hydrostatically in the new total mass. Particle numbers are CFG599's.
3. **Gate (CFG639 HG).** The settle step's drift and OU act only where d = ρ_ph − ρ_cs > 0 (CFG639's `Sim639.settle`, reused).
4. **Calibration.** The mass model changes, so (v0, η) are re-fit per reservoir rule by CFG621's own procedure (`calibrate()`,
   imported read-only: α = 0, canonical, K1 speed 2700 ± 200 km/s and G1 d_SG 194 ± 50 kpc at the 720-kpc epoch, η ∈ [0.1, 2.5],
   at most two rounds), then held for every α and both footings. If calibration fails for a rule, that rule's arms are VOID.
   CFG623's footing validity at α = 0 (K1/G1 per footing) applies per arm.

## 2. Arms and runs

| arm | source | reservoir | gate | role |
|---|---|---|---|---|
| **P** | stars | RN | on | primary |
| S | stars | RI | on | reservoir bracket |
| U | stars | RN | off (FIX-2 everywhere, CFG623 settle) | attribution: H-CB alone |

Nodes α ∈ {0, 0.03, 0.1, 0.3, 1, 3, 10} × {can, alt} per arm (42 runs; P and U share the α = 0 runs by construction and the RN
calibration). Seed 599. Runs cached in CFG640's own `runs*/` directories.

## 3. Controls and teeth

- **C-R0:** source = all baryons, no reservoir, gate off, α = 0 canonical must reproduce CFG623's `a0_can` exactly (max 0 kpc
  over all epochs; sub gal/gas/lens/variants). Verifies the progenitor patch.
- **C-R1:** the same at α = 0.1 canonical must reproduce CFG623's `a0.1_can` exactly. Verifies the phantom-field override.
  If C-R0 or C-R1 fails, CFG640 is VOID.
- **T-H (static):** stars-only settled mass / all-baryon phantom mass inside r_t < 0.5 for the main cluster on both footings
  (disclosed above: 0.448 / 0.442; a sanity check that the source change is real, not a test).
- **T-G (gate acts):** in arm P at α = 0.1 canonical, the gated-off fraction of cold-element settle steps within
  t_peri − 0.3 to t_peri + 0.6 Gyr is ≥ 0.05, AND |f_P − f_U| > 0.02 or |β̄_P − β̄_U| > 0.02 at that node. If T-G fails, VH-3
  (attribution) is NOT DIAGNOSTIC; VH-1 is still scored.

## 4. Scores and verdicts

Scores, stability and status are CFG623's `score_run` unchanged (S-1, S-2: ALLOWED / EXCLUDED / UNSCORABLE). No α_max, no
interpolation.

- **VH-1 (combo rescues mergers), arm P:** "RESCUES" iff some node α ≥ 0.1 is ALLOWED on both footings; "DOES NOT RESCUE" iff no
  α ≥ 0.1 node is ALLOWED on both footings and at least one α ≥ 0.1 node is scorable on both; else "UNDETERMINED". Also reported:
  whether α = 0 is still ALLOWED on both footings.
- **VH-2 (galaxy-preferred α on the merger side), arm P:** "MERGER SIDE COMPATIBLE AT α = 1" iff α = 1 is ALLOWED on both
  footings; else the allowed set is listed. The full one-α verdict also needs the gate's galaxy side, which CFG639 Part A left
  NOT DIAGNOSTIC, so it is stated as conditional on that.
- **VH-3 (attribution), arm U vs P:** per node, whether the status changes between H-CB alone and H-CB + gate. "GATE NEEDED" iff
  some α ≥ 0.1 node is ALLOWED on both footings in P but not in U; "H-CB SUFFICES" iff every node allowed in P is also allowed
  in U and P allows some α ≥ 0.1; else "NO RESCUE EITHER WAY" or "MIXED", listed.
- **VH-4 (reservoir dependence), arm S vs P:** "RESERVOIR-DEPENDENT" iff VH-1 differs between S and P; else "SAME UNDER RN AND RI".

## 5. Order and machine rules

- Heavy (CFG623 footprint: about 10 GB over 4 processes). A waiter starts CFG640 only when no `cfg636_pm.py`, `cfg596_pm.py`,
  `run_636.py`, `run_596.py` or `cfg639_merger.py` process is running and at least 16 GB is free; at most 4 processes,
  `nice -n 10`, one thread each.
- Order inside the lane: controls C-R0, C-R1 → calibration RN → arm P → arm U → calibration RI → arm S → scoring.
