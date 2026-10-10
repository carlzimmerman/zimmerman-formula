# CFG555 FROZEN CRITERIA: the CFG361 growth statistic on the GRAVITATING density (audit of PAPER45 and its lanes)

Frozen 2026-10-10, before any gravitating-field number for the CFG424/518 engine runs is computed in this lane.
Trigger: CFG539's post-hoc diagnostic (`cfg539_posthoc_grav_pk.*`): CFG527/530's "GROWTH OK" was measured on the particle
density; on the gravitating density (particles + e − comp) the L200 256³ max|r−1| is 0.336 (canonical) / 0.388 (alt).
Question: does the same hold for the PUBLISHED growth claim (PAPER45 v2.0/v2.1, CFG424 engine, RC = 0) and its confirmations?

## Scope (every run whose z = 0 state is on disk; read-only)

| lane | runs (z = 0 state) | matched S0 (JSON; S0 has no source, so gravitating = particles) |
|---|---|---|
| CFG424 | TA-can, TA-alt, MUTATE (NOCOMP) 256³ seed 359 | cfg359 S0 N256 |
| CFG425 | R1 seed 360, R2 seed 361 (256³ can); R3 512³ can seed 359 | cfg411 S0 N256 seed 360/361; cfg411 S0 N512 |
| CFG426 | D1 DE can, D2 DE alt (seed 359); A1/A2 FLAT alt seed 360/361 | cfg359 S0 N256; cfg411 S0 N256 seed 360/361 |
| CFG427 | E1 eps 0.0385, E2 eps 0.154, G1 MIXB, G2 HOT1 | cfg359 S0 N256 |
| CFG439 | A FLAT alt 512³, B DE can 512³ | cfg411 S0 N512 |
| CFG460 | FLAT can 512³ seed 360 | cfg424 S0 N512 seed 360 |
| CFG518 | DC-can, DC-alt, NOCOMP, K1 (f_ret = 1) 256³; DC-can 512³ | cfg359 S0 N256; cfg411 S0 N512 |
| CFG527 | LR-can, LR-alt L200 256³ (own runs); MUTB (NOCOMP) L200 | cfg359 S0 N256 |
| CFG530 | LR-can/LR-alt L100 and L200 at N128/256/512 | its own S0 per (L, N) (L200 N512 = cfg411 S0 N512), from the CFG530 profile caches |

The engines are each run's OWN engine file (cfg424_pm.py, cfg518_pm.py, cfg527_pm.py), imported unchanged with the run's own
settings (branch, footing, MIX, EPS, f_ret mode, NOCOMP, L, RMIN; RC = 0). No 512³ job is re-run; 512³ states are processed
one at a time (memory check first).

## Task 1: which density each lane's statistic used
Cite file:line for (i) where the run's snapshot P(k) and σ8 are measured, and (ii) which JSON field the lane's analysis reads.

## Task 2: the gravitating density (method, frozen)
1. Load the saved z = 0 positions, deposit δ_p with the engine's own `Mesh.deposit` on the run's mesh, call the engine's own
   `forces(mesh, δ_p, a = 1, switch, branch, foot, dta, diag = True)` (the same call the run made at its z = 0 snapshot).
2. Capture the total potential from the three acceleration transforms (CFG526 method): δ_grav = −k² φ̃_k / (1.5 Ω_m), k = 0 set to 0.
   Then δ_src = δ_grav − δ_p = (e − comp) / (1.5 Ω_m) at a = 1.
3. P(k), σ8 of δ_grav with the engine's own `measure_pk`; the CFG361 statistic against the matched S0 JSON: σ8 ratio and
   max|P/P_S0 − 1| over bins with k ≤ 1 h/Mpc (S0 P interpolated at the run's k, as every lane did).
4. Category (CFG361 cuts, unchanged): FAIL if |σ8 ratio − 1| > 0.20; GROWTH OK if |σ8 ratio − 1| ≤ 0.05 and max|P−1| ≤ 0.10;
   otherwise TENSION.

### Reproduction gates (a run failing any gate is NOT EVALUABLE, not scored)
- R1: the engine's z = 0 diagnostics recomputed from the saved state reproduce the run JSON's z = 0 values:
  q_max, e_mean / e_sum (where present) to relative ≤ 1e-6; n_catch (where present) exactly; |src_sum_recomputed − src_sum_JSON|
  ≤ 1e-6 × max(|e_sum|, N³ e_mean). (Saved positions are float32; if a value misses 1e-6 but is ≤ 1e-4, it is reported as
  "reproduced at float32-position precision" and the run is still NOT EVALUABLE for this lane's verdict unless the gravitating
  number is ≥ 0.02 away from both cut lines, which is then stated explicitly.)
- R2: the particle P(k) re-measured from the saved state reproduces the run JSON z = 0 P at k ≤ 1 to relative ≤ 1e-4, and σ8 to ≤ 1e-5.
- R3: mean(δ_grav − δ_p) ≤ 1e-6 (mass conservation of the source on the mesh).
- For CFG530 (from caches built by CFG530/526 with the same method): the cache's own K record must pass CFG526's kcheck, and one
  cache (LR-can L200 N256) is rebuilt independently here and must agree on max|P−1| to ≤ 1e-4.

## Task 3: which field the observations need (decided from the physics, written in the README)
Galaxy clustering traces baryons/particles; weak lensing, cosmic-shear S8, CMB lensing and "the matter power spectrum" trace the
total gravitating mass. The PAPER45 sentence "structure growth within 10% of ΛCDM-equivalent growth" and its "excess in the matter
power spectrum" are judged against the field they name.

## Task 4: controls (MUTATE run writes `_MUTATE.out` / `_MUTATE.json` separately)
- C0 (source off): with δ_src := 0 the same code must reproduce each lane's committed particle-based (σ8 ratio, max|P−1|) to
  ≤ 1e-4 absolute (float32 positions) and exactly equal the pipeline's own particle number.
- C1 (synthetic source, known power): a fixed-amplitude random-phase field with a declared spectrum P_syn(k) = 0.05 P_S0(k) is
  measured by the same `measure_pk` and recovered bin by bin to relative ≤ 1e-5; and δ_p + c δ_p (c = 0.05) must give
  max|P−1| = (1 + c)² − 1 to ≤ 1e-5 through the full statistic.
- C2 (capture): S0 states passed through `forces(..., "S0")` must give δ_grav = δ_p (max diff ≤ 1e-4 of the peak), and a S0 state
  with δ_p + c δ_p injected must return (1 + c)² in P to ≤ 1e-5.
- MUTATE: the source-off analysis (C0) is written as the `_MUTATE` output; it must reproduce the original particle verdicts (if the
  gravitating verdicts were mere relabelling of the particle ones, the MUTATE would show no difference from the primary — the primary
  and MUTATE outputs are compared and the difference reported).
- Reported only (not a verdict input): δ_grav measured with the CIC window deconvolved from the particle part only (the source is a
  mesh field, not a deposit); and the P/P_S0 ratio at k = 0.5, 1, 2, 4.

## Verdicts
- Per run: the category above, both footings separately, never pooled.
- Per lane: CLAIM HOLDS ON GRAVITATING FIELD if every run the lane counted as GROWTH OK is GROWTH OK on δ_grav;
  CLAIM FAILS ON GRAVITATING FIELD (numbers listed) if any such run is TENSION or FAIL on δ_grav;
  NOT EVALUABLE if a needed state is missing or a reproduction gate fails. Lanes whose original verdict was not a pass get
  their gravitating numbers reported alongside.
- PAPER45 (v2.0 / v2.1 table, 15 rule runs: CFG424 can/alt, CFG425 R1/R2, CFG426 A1/A2, D1/D2, CFG427 E1/E2/G1/G2, CFG425 R3,
  CFG439 A/B): HOLDS if all 15 are GROWTH OK on δ_grav; FAILS (numbers) if any is not; the MUTATE row (no compensation) is
  reported on δ_grav too. If it fails, the exact correction text is drafted in this lane's README only. The paper files are NOT
  edited and nothing is published; the owner decides.

No knobs: nothing is tuned; the statistic, cuts, S0 controls and engines are imported unchanged. κ = ½ is fitted; cold energy mass
is required; this is not "theory closed".
