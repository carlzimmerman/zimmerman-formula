# CFG639 FROZEN CRITERIA: deficit-gated mobility (settle and relax only where cold energy is missing)

Date: 2026-10-12. Written and committed ALONE, before any CFG639 code exists and before any CFG639 run. Nothing below may be
edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. The footings (9.3603e-11 canonical, 1.1312e-10 alt) are judged separately and never pooled. The cold energy's
mass is still required (an input). No particle species. Not "theory closed". Yardsticks are raw data only (as in CFG623).
Nothing will be phrased as "the data favour the framework". No knob scans: the gate has no free constant.

## 0. What has been seen (stated before any choice below)

- CFG623 (merger stopwatch v5, VALID): allowed set {0} on both footings; α = 0.1, 0.3, ∞ EXCLUDED; α = 0.03, 1, 3, 10
  UNSCORABLE; V-3 INCOMPATIBLE. Its per-node table, mechanism test and disclosures (`CFG623_merger_stopwatch_v5/README.md`).
- CFG544 / CFG550 / CFG554 / CFG558 / CFG620 / CFG626 galaxy-bench results: FIX-2 (two-sided deficit + OU to the instantaneous
  isotropic Jeans dispersion) passes G550 in all 4 cells on IC-B and IC-C; the one-sided "as is" rule fails by overfill
  (+0.05 to +0.23 dex) after a radial collapse; overfill not handled by any knob-free rule.
- CFG638 (this author, 2026-10-12): Kn = √2/(4α), Re = 4α; one α sets both mobility and viscosity; the merger–galaxy tension
  is "collisionless in mergers, fluid in galaxies".
- CFG634 T4a (H-CB settled mass rides with the galaxies at any α) and CFG637's criteria. Not used here.

**Author's expectations, written before any run (not verdict inputs):**
- Mergers: the deficit stays positive near the lagging gas (the phantom is sourced by all baryons, gas included), so the gated
  drift may still pull cold energy toward the gas. The gate may change little at α ≥ 0.1.
- Galaxies: the gate is one-sided in mobility, so an overfilled core (d < 0) is neither pushed out nor heated. The CFG544 IC-C
  collapse overfill may persist; Part A may fail.

## 1. The hypothesis HG (the only physics change)

The mobility of the record's settling law is gated by the sign of the two-sided deficit d = ρ_ph − ρ_c:

  G(x) = 1 if d(x) > 0, else 0.

Both the drift (v_s → G v_s) and the velocity relaxation (OU rate α/τ → G α/τ) are multiplied by G at each cold-energy element's
position. Where cold energy is not missing, it is collisionless (Kn = ∞); where it is missing, it settles and relaxes exactly as
FIX-2. This is CFG542 S2's placement (gate in the mobility only; no leak for any reading). It adds no constant. ψ, ρ_ph, τ, the
OU target and every other rule are unchanged. The sign test uses the code's own gridded d (CIC deposit in the PM, radial bins in
the bench); no threshold.

## 2. Part A: galaxy side (must pass for HG to be compatible with galaxies)

- **Bench:** CFG544's spherical N-body toy (`cfg544.py`), imported read-only, unchanged: N = 30000, seed 544, α = 1, cells
  {MW, cluster} × {can, alt}, the exponential kernel the bench uses (as in CFG544/550/554; disclosed, CFG626), IC-B (infall,
  10 Gyr) and IC-C (settled at rest, 5 Gyr), rule "two" with OU (FIX-2), plus the gate G evaluated per radial bin.
- **Gate G550 (CFG544's, unchanged):** |log X| ≤ 0.1 and |D| ≤ 0.1 at the end, and steady (|Δlog X|, |ΔD| ≤ 0.05 over the last
  2 Gyr).
- **A-PASS** iff G550 passes in all 8 runs (4 cells × IC-B, IC-C). Otherwise **A-FAIL**, with the failing runs listed.
- Reported (no verdict weight): overfill excess inside r_*, r99, β, sink, the fraction of particle-steps gated off.
- **Control A-C1:** with G ≡ 1 the code must reproduce CFG544's `MW_can|fix2_C` final log X and D exactly (Δ = 0). If A-C1
  fails, Part A is VOID.
- **Tooth A-M1 (MUTATE):** inverted gate (G = 1 where d < 0) must change the MW_can IC-C end state (|ΔD| > 0.02 vs gated). If it
  does not, the gate is not acting and Part A is NOT DIAGNOSTIC.

## 3. Part B: mergers (Bullet + Harvey, CFG623 pipeline)

- **Copied from CFG623 unchanged (code imported read-only):** simulator and estimator (`cfg622_sim.py` via CFG623), data D1–D3,
  calibration (v0 2666.7 km/s, η 1.132, held fixed), seed 599, Harvey window d_SG ≥ 200 kpc, the majority stability rule (≥ 3
  of 4 variants within T_L), edge and gas guards, S-1 Z_B = (f − 0.045)/0.125, Z_H = (β̄ + 0.04)/0.07, no error inflation, S-2
  ALLOWED / EXCLUDED / UNSCORABLE exactly as CFG623's `score_run`, footing validity K1/G1 at α = 0.
- **The only change:** CFG599's settle step with the gate G applied to the displacement and to the OU update (momentum
  correction over gated elements only). Runs are cached in CFG639's own `runs/` (never CFG623's).
- **Nodes:** α ∈ {0, 0.03, 0.1, 0.3, 1, 3, 10} × {can, alt} = 14 runs. α = ∞ is not run: it is CFG599's field form with no
  elements to gate (already EXCLUDED in CFG623).
- **Controls:**
  - B-R: α = 0 never calls the settle step, so both α = 0 runs must reproduce CFG623's α = 0 runs exactly (max 0 kpc over all
    epochs, sub gal/gas/lens/variants). If not, Part B is VOID.
  - B-G1: with G ≡ 1, α = 0.1 canonical must reproduce CFG623's `a0.1_can` run exactly. If not, Part B is VOID.
- **Tooth B-M1:** in the gated α = 0.1 canonical run, the fraction of cold-element settle-steps gated off within
  t_peri − 0.3 to t_peri + 0.6 Gyr must be ≥ 0.05, and the run's f or β̄ must differ from CFG623's ungated value by more than
  0.02. If either fails, Part B is NOT DIAGNOSTIC (the gate does not act in the merger).
- **Verdicts:**
  - **VG-1 (merger rescue):** "RESCUES" iff some node α ≥ 0.1 is ALLOWED on both footings; "DOES NOT RESCUE" iff every
    scorable node α ≥ 0.1 is EXCLUDED on at least one footing and at least one α ≥ 0.1 node is scorable on both; otherwise
    "UNDETERMINED".
  - **VG-2 (one α for galaxies and mergers):** "COMPATIBLE" iff α = 1 is ALLOWED on both footings AND Part A passes;
    "PARTIAL" iff some node in {0.3, 3} is ALLOWED on both footings AND Part A passes; "INCOMPATIBLE" otherwise, with the reason
    (Part A fail, or merger side).
  - No α_max, no interpolation between nodes.

## 4. Order and machine rules

- Part A runs first. It is light (≤ 2 processes, < 1 GB each) and may run while the 1024³ production (CFG636) is live.
- Part B is heavy (CFG623: about 10 GB over 4 processes; it once competed with a 1024³ run). It starts only when no
  `cfg636_pm.py` / `cfg596_pm.py` process is running and at least 16 GB is free; at most 4 processes, `nice -n 10`, one thread
  each. A waiter script polls (every 10 min) and launches Part B when those hold.
- Both parts commit their own outputs; the Part B verdict uses Part A's result for VG-2. If Part A is VOID or NOT DIAGNOSTIC,
  VG-2 is UNDETERMINED.
