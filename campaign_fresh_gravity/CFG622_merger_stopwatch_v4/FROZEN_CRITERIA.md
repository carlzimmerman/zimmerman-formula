# CFG622 FROZEN CRITERIA: merger stopwatch v4 (CFG621 rerun with a merger-safe lensing estimator)

Date: 2026-10-11. Written and committed ALONE, before any script of this lane exists and before any CFG622 run. Nothing below may
be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. The cold energy's mass is still required (an input). No dark-matter particle is added. The theory is not
closed. Yardsticks are raw data only: no ΛCDM halo or baseline, no MOND force law. Nothing here will be phrased as "the data
favour the framework". α is the declared measured quantity. The only constants set from data are CFG621's two calibration
numbers (v0 = 2666.7 km/s, η = 1.132), held for every α and both footings (9.36e-11 canonical, 1.13e-10 alt; never pooled).

## 0. What has already been seen (stated before any choice below)

CFG621's stage-B results (3fccac215) and its disclosure B-D1 (`cfg621_spread_diag.py`) are known to the author of this file:
- per-node f, Z_B, Z_H and lensing spreads (README table); α = ∞ EXCLUDED (Z_B +7.86 / +8.06, stable); α = 0.3 canonical EXCLUDED;
  α = 0 Bullet cell unstable only because of the (400, 75) variant (other three within 11.7 kpc); α = 1 and 3 unstable with the
  remaining variants disagreeing; the unscored as-run readings rise from Z_B ≈ +1.1 at α = 0 to ≥ +7.6 at α ≥ 0.3;
- at α = 1 CFG621's PRIMARY sub lensing peak lies about 440 kpc from the sub galaxies on the gas side, i.e. beyond the
  perpendicular bisector of the sub–main galaxy segment (about 360 kpc at the 720-kpc epoch). The mask below therefore changes
  the α = 1 primary peak by construction; the edge guard (§2 B-3) exists so that a peak pressed against the mask is never
  scored as a peak.
Every change below is motivated only by B-D1 (lensing estimator circles reaching the other cluster; isolated-halo tolerance
applied to a merger), and is fixed without reference to which α it would favour. No other part of CFG621 is changed.

## 1. Copied from CFG621 unchanged (FROZEN_CRITERIA_B.md 4dfa0833b; code imported read-only)

Data D1–D3 (f_obs = 0.045, σ_f = 0.125 PROVISIONAL; Harvey β = −0.04 ± 0.07; D3 sign level only); model M-1 to M-5b (CFG599
via `cfg621_sim.py`: grid, hydro, progenitors, cool-core cloud with drag η, case L, rule 2S drift + FIX-2 OU, no EFE, particle
numbers, seed 599 for the grid); α nodes {0, 0.03, 0.1, 0.3, 1, 3, 10, ∞} × both footings = 16 grid runs; galaxy and gas peaks:
estimator E-1 (shrinking circle R0 300 / R_min 75 kpc; gas started at the 600-kpc mass-weighted centre) UNCHANGED; the 720-kpc
epoch, f (O-4), Harvey β̄ over t − t_peri ∈ [0.1, 0.6] Gyr (O-5: ≥ 10 qualifying epochs and ≥ half the window, each with
d_SG ≥ 50 kpc and a stable lensing peak); S-1 Z_B = (f − 0.045)/0.125, Z_H = (β̄ + 0.04)/0.07, no error inflation; S-2 ALLOWED iff
scorable and |Z_B| < 2 and |Z_H| < 2, EXCLUDED iff scorable and not allowed, else UNSCORABLE; no α_max, no interpolation;
V-1 (α = ∞ EXCLUDED iff scorable and Z_B ≥ 3 on both footings), V-2 (α = 0 ALLOWED iff allowed on both footings; NOT ALLOWED iff
scorable on both footings and not allowed on at least one; else UNDETERMINED, exactly as CFG621's code), V-3 (COMPATIBLE iff α = 1 allowed
on both footings; PARTIAL iff not, but some node in {3, 10, ∞} is; INCOMPATIBLE otherwise), V-4 summary (CFG621's code);
the alt footing is VOID if its α = 0 run misses K1 (2700 ± 200 km/s) or G1 (d_SG 194 ± 50 kpc). C1–C3, C5, C6 (CFG621 controls,
unchanged code), C4(a)/C4(b) (isolated halos: no other cluster, so the mask is inactive and E-1 is identical; CFG621's stage-A
T-4 and N_B = 0.188 re-read from CFG621's JSON).

## 2. The only changes (all from B-D1)

B-1 **Merger-safe lensing estimator E-M (the other cluster's half is masked).** For the sub's lensing peaks (primary and all
    variants) and the sub's cold-energy peak, the total (resp. cold) surface-density map is multiplied by the mask
    M_sub = {pixels closer to the sub's galaxy peak than to the main's galaxy peak} (both galaxy peaks from E-1 at that epoch).
    The main's peaks use the complementary mask. Isolated runs: no mask. Shrinking circles unchanged otherwise: primary
    (300, 75), spread over the CFG621 variants (300, 60), (300, 90), (200, 75), (400, 75), all started at the sub's galaxy peak.
    No circle can therefore land on the other cluster's peak. No fraction or radius is tuned. The unmasked CFG621 primary and
    spread are recorded alongside (reported only).
B-2 **Merger-calibrated stability tolerance T_M (per footing, never pooled).** Control ensemble, disjoint from the α grid:
    α ∈ {0, ∞} × seeds {600, 601, 602} × each footing (12 runs; the grid uses seed 599 only), at CFG621's (v0, η). Sample: every
    diagnostic with t − t_peri ∈ [0.1, 0.6] Gyr and d_SG ≥ 50 kpc of the 6 control runs of that footing (this window contains the
    720-kpc epoch). Statistic: the E-M lensing spread (max distance of a variant from the primary). **T_M[foot] = max(T_L, 3 × P95)**
    with T_L = 24.90 kpc (CFG621 stage A, the isolated floor). The factor 3 × P95 is stage A's rule, unchanged.
B-3 **Stability rule (Bullet bracketing epochs and Harvey epochs).** An epoch is STABLE iff (a) E-M spread ≤ T_M[foot]; and
    (b) edge guard: no E-M lensing peak (primary or variant) lies within R_min = 75 kpc of the mask boundary (the bisector);
    and (c) gas guard: the sub's gas peak lies on the sub's side at ≥ 75 kpc from the bisector.
B-4 **Calibration check (no new fit).** One calibration-mode run (α = 0, canonical, seed 599, CFG621's v0 and η; galaxy and gas
    estimators are unchanged) must give speed 2700 ± 200 km/s and d_SG 194 ± 50 kpc with η ∈ [0.1, 2.5]. If it does not,
    CFG621's calibration procedure (4-way bracketing, ≤ 2 rounds) is re-run and its result used; if that fails, VOID.
B-5 **New controls.** C7 mask null test: at t = 0 of each of the 12 control runs (clusters 2300 kpc apart), the E-M and unmasked
    primary sub lensing peaks agree within 3 kpc. C8 reproduction (reported, not a gate): the unmasked primary lensing peak, the
    galaxy and gas peaks of the grid runs that CFG621 also ran (all 16 grid runs) are compared epoch by epoch with CFG621's
    `runs_B` (max difference reported).
B-6 **Seed scatter (reported only, not used in any score).** σ_seed(f) and σ_seed(β̄) over the 3 control seeds at α = 0 and
    α = ∞ per footing; N_M = σ_seed(f)/σ_f. If N_M > 1 at either endpoint on a footing, that footing's Bullet scores are
    flagged "seed-noise comparable to σ_f" in the README (flag only; S-1 is unchanged).
B-7 **MUTATE.** M1 (α = ∞: f ≥ 0.5), M2 (α = 0: |f| ≤ 0.25 AND β̄ ≤ 0.10), M3 (roles swapped, α = ∞: f ≤ 0.25) as CFG621, scored
    with E-M; M3 roles-swapped α = 0 and M4 (seed 600 vs 599 at α = 0, canonical; seed 600 is a control run) reported. M1 and
    M2 are the grid's α = ∞ and α = 0 canonical runs (as in CFG621, B-D2). Where a MUTATE score needs f or β̄ and the cell is
    unstable, the as-run value is used for the gate (as CFG621's code did).

## 3. Gate order (every gate must pass, else every verdict is VOID with the failing control named)

1. C1–C3, C5, C6 (CFG621 controls re-run, unchanged code); C4(a), C4(b), N_B ≤ 1 (re-read).
2. The 12 control runs; C7; T_M[can], T_M[alt]; B-6 reported.
3. Calibration check B-4.
4. MUTATE M1–M3 (runs M1, M2, M3, M3-α0).
5. The rest of the 16-run grid; per-node Z_B, Z_H, status on both footings; V-1 to V-4.
The α scan counts only if 1–4 pass. If a gate fails, remaining numbers may be reported only as unvalidated, labelled VOID.

## 4. Compute and housekeeping

nice -n 10, ≤ 4 processes of 1 thread, ≤ 2 GB each (a long unrelated job shares the machine). Run cache (small JSON) in
`runs/`; console logs outside the repo. Outputs `cfg622_controls_results.json`, `cfg622_results.json`,
`cfg622_results_MUTATE.json` and `.out` files. README numbers come from the JSON. CFG599/CFG621 are read-only. Commit specific
paths only; no push; never rewrite history.
