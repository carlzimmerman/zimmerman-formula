# CFG647 FROZEN CRITERIA: engineering audit of the settled cold-energy accounting in the CFG596 PM engine (crowded regions)

- **Written:** 2026-10-12, committed ALONE before any CFG647 code or measurement.
- **Settings:** κ = ½ FITTED; footings never pooled (canonical only here: P1 is the only finished RES run); "cold energy"; the cold energy's MASS is required; no particle species; not "theory closed".
- **Read-only:** `CFG596_lean_pm_1024/cfg596_pm.py` (production freeze 6323b630f) and its parent `CFG527_law_respecting_engine/cfg527_pm.py` are NOT edited. Stored CFG596 outputs (P0/P1 JSON + 256³ block-mean meshes) are read only. The running 1024³ CFG636 job, the CFG640 waiter and the CFG625 driver are not touched.

## Question

CFG596 EXCLUDED candidate B on raw KiDS (canonical; own boost 1.19–1.25 at k 0.3–1 h/Mpc). The excess sits at 0.2–0.5 r_ta in massive halos (CFG556), which are crowded with overlapping turnaround catchments. Is there an ACCOUNTING BUG that puts too much settled source in crowded regions? Hypotheses:
- H1 overlapping catchments each draw the full supply (supply counted per ball, not per unique cell);
- H2 the demand (excess e) counted per ball;
- H3 the settled source is added on top of the particles' mass without an equal removal (net source ≠ 0; the PM's dropped k = 0 mode would hide this as a uniform offset);
- H4 settled source delivered beyond the available supply of its catchment, or drawn inside the census edge, or a cell carrying both excess and compensation.

## Disclosures before freezing

- The engine source (cfg596_pm.py, cfg527_pm.py), the CFG518/524/527 frozen criteria and astra's notes (sol61_push material_transport RESULT; commits 8433827bc, 9c5205d10, c186b58e1) were READ before this file. Code reading is not a measurement.
- The P1/P0 JSON scalar diagnostics (src_sum, e_sum, overdraw_mass, q_max, cap_active, n_catch) were PRINTED before this file. The H3 check on the stored JSON is therefore not blind; it is kept because its tolerance is fixed here and it is a pure identity check.
- The x_supply edge radius table (x = r_edge/r_ta per resolved R and z) was computed from the engine's own function before this file (no density field involved).

## The spec the engine must match (the reference for "bug")

CFG518 items 2, 5, 6; CFG524 "per catchment C (CFG424 turnaround-ball components)"; CFG527 "Excess / Draw region / Weight":
- catchment = union of turnaround balls (x = 1) around resolved peaks; components = its periodic 6-connected components; f_ret painted per ball, largest host wins, f_ret = 1 outside;
- census edge = union of balls of radius x_supply·r_ON (capped at r_ON);
- e = f_sw·max(s_ph − s_c, 0) × catch, f_sw carrying the edge mask; draw region D = catch AND NOT edge; per component E_C = Σ_C e, R_C = Σ_{D_C} s_c, q_C = E_C/R_C; if q_C > 1: e → e/q_C and q_C → 1; comp = q_C s_c on D_C; src = e − comp; φ_k = −(1.5Ω_m/a)δ_k/k² − src_k/k².

A behaviour that matches this spec is NOT a bug. It may still be a PHYSICS finding about the rule (reported separately).

## Measurements (script `cfg647_audit.py`, outputs `cfg647_audit.out/json`)

M1 (stored JSON, P1 canonical, all six snapshots): |src_sum|/e_sum; overdraw_mass; q_max; cap_active.

M2 (256³ recomputation on stored P1 dpart block means at z = 1, 0.5, 0; mesh 256, L = 100, RMIN 0.78125, engine functions imported unchanged, SPILL off, lean mode). An instrumented re-implementation of the RES source block exposes per-cell e, s_c, catch, edge, labels, and the ball multiplicity. Reported:
- **V1 overlap:** fraction of catchment volume covered by ≥ 2 turnaround balls; same for the edge; fraction of post-cap settled e in cells covered by ≥ 2 balls; number of resolved peaks per component (distribution); volume and supply fraction of the largest component.
- **V2 supply accounting:** Σ over components of R_C vs Σ over unique shell cells of s_c; Σ E_C vs Σ unique e; the NAIVE per-ball sums (each ball's own shell and edge summed ball by ball, overlaps counted once per ball) as the size a per-ball bug would have; delivered settled Σ_C min(E_C, R_C) vs total shell cold Σ R_C vs total catchment cold vs (Ω_c/Ω_b)·Σ_catch f_ret·f_b(1+δ) (cold-to-retained-baryon ceiling); per-component zero sum.
- **V3 pooling (theory rule, not a bug test):** counterfactual "own host" accounting: every catchment cell assigned to ONE host (the covering ball with the smallest d/r_ON; ties to the larger host), E_h and R_h summed per host with the same union edge and shell, delivered Σ_h min(E_h, R_h). Pooling gain G = Σ_C min(E_C,R_C) / Σ_h min(E_h,R_h). Split of the gain by host log M_ta (< 13.5, ≥ 13.5).
- **V4 static P(k) effect of pooling:** on the frozen z = 0 particle field, P of δ_p + a·src/(1.5Ω_m) with the engine rule vs the own-host rule, ratio at k = 0.3, 0.5, 1 h/Mpc (no re-evolution; labelled static).
- **V5 resolution control:** the recomputed 256³ s = a·src/(1.5Ω_m) vs the STORED s_stored = dgrav − dpart (block means of the 1024³ run): positive and negative sums and the Pearson correlation. Reported, not gating, except as stated in C2.

## Controls (must pass, or the M2 numbers are not used)

- **C0 instrumentation:** φ_k from the instrumented re-implementation equals φ_k from the unmodified `cfg596_pm.forces(..., diag=True)` on the same 256³ input: max|Δφ_k| ≤ 1e-5 · max|φ_k|, and q_max, n_catch, e_sum, src_sum agree to 1e-5 relative (src_sum to 1e-5 · e_sum absolute).
- **C1 synthetic:** two overlapping balls on a uniform field with hand-set e and s_c: the engine's labels give ONE component, and its R_C equals the hand count of unique shell cells (exact in float64 to 1e-9 relative); the naive per-ball sum exceeds it by the hand-counted overlap.
- **C2 representativeness:** the 256³ recomputation must show cap_active = True at z = 0 and overdraw_mass within a factor 1.5 of the stored 1024³ value; otherwise V3/V4 are reported as "resolution-limited" and not used for the physics finding.

## Verdict rules

**BUG FOUND** if any of:
- B1 (H1): |Σ_C R_C − Σ_unique shell s_c| / Σ_unique > 1e-5, or any catchment cell carries more than one component label;
- B2 (H2): |Σ_C E_C − Σ_unique e| / Σ_unique > 1e-5;
- B3 (H3): stored |src_sum|/e_sum > 1e-5 at any snapshot, or in M2 any component with R_C > 0 has |Σ_C src| > 1e-4 · E_C;
- B4 (H4): any component with delivered settled > R_C·(1 + 1e-5); comp ≠ 0 in any edge cell; e ≠ 0 in any shell cell; e ≠ 0 outside the catchment;
- B5: any engine line found to deviate from the spec text above (cited line + spec sentence). Inherited cfg527 behaviour that the spec does not address is reported as an "inherited inconsistency", not a bug, with its scope.

On BUG FOUND: exact lines, the size of the effect on P(k) estimated (static, V4-style), a corrected spec, a patched COPY (never the production file) and a reproduction plan. No production rerun in this lane.

**NO BUG** otherwise. Then the physics reading of the RULE itself in crowded regions, from V3 (only if C2 passes):
- G − 1 < 0.01: pooling negligible;
- 0.01 ≤ G − 1 < 0.05: minor;
- G − 1 ≥ 0.05: MATERIAL: the per-component rule moves neighbour supply into the dominant host; reported as a theory finding, not an engine bug.

## Run limits

At most one diagnostic process, ≤ 2 GB, nice -n 10, started only if vm_stat free + inactive ≥ 8 GB. No new simulation is planned (M2 reuses the stored production density); a 128³–256³ simulation is run only if C2 fails AND the remaining question needs it, under the same limits. No downloads.
