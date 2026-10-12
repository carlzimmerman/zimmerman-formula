# CFG596: a lean 1024³ PM and a framework-native shear test with the framework's own boost as the sensitivity tooth. Status: ENGINE VALIDATED (bit-for-bit); PRODUCTION RUNNING; verdict PENDING

- **Dates:** 2026-10-10 (pre-flight, criteria, engine, validation; production started the same evening).
- **Settings:** κ = ½ is FITTED. The footings are never pooled. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing here says the data favour the framework.
- **Numbers:** every number below comes from a committed JSON: `cfg596_preflight.json`, `cfg596_tooth_audit.json`, `cfg596_validate.json`, `cfg596_native_results_test530*.json`, and, when production ends, `cfg596_native_results*.json`.
- **CFG592's verdict is unchanged:** NOT DIAGNOSTIC on every track.

## Commits so far

| step | commit |
|---|---|
| pre-flight (no verdict role) | ac4857dce |
| FROZEN CRITERIA, committed alone, written after the pre-flight (disclosed in it) | f6c27d401 |
| engine + validation | 2258e1ea3 |
| engine v2 (memory) + re-validation | 8459ceedd |
| production code freeze (allocator release) | c8825cf4a |
| production code freeze v2 (uncached spill files, freed views) | 6323b630f |

## Part 0. Pre-flight: no buildable box passes CFG592's frozen tooth (`cfg596_preflight.py`, `cfg596_tooth_audit.py`)

**Method.** CFG592's native machinery was run unchanged. The S0 spectrum is a splice of existing S0 PM spectra: CFG518 S0 L200 N512 below k = 0.5 and CFG530 S0 L100 N512 above. A hypothetical box changes only [k_lo, k_hi = πN/(4L)].

**Proxy check.** At L100 N512 the proxy keeps 20 KiDS / 40 DES points, and the tooth gives χ² 0.89 / 0.13. CFG592's real run gave 20 / 38 points and 0.79 / 0.04.

| box | k range (h/Mpc) | KiDS / DES kept | CFG592 tooth NZ2 χ², KiDS / DES | framework's own boost injected, KiDS (can / alt) | same, DES (can / alt) |
|---|---|---|---|---|---|
| L400 N1024 (first plan) | 0.020–2.01 | **0 / 0** | — | — | — |
| L200 N1024 | 0.040–4.02 | 49 / 57 | 1.32 / 0.36 | | |
| L150 N1024 | 0.053–5.36 | 93 / 70 | 4.13 / 0.79 | 14.43 / 18.75 | 3.40 / 4.21 |
| **L100 N1024** | 0.080–8.04 | **119 / 100** | 6.33 / 0.88 | **14.64 / 19.14** | **8.56 / 9.69** |
| everything resolved (ideal reference) | 0.005–49 | 225 / 227 | **7.95 / 1.95** | 16.98 / 22.10 | 17.91 / 16.64 |

- **CFG592's tooth cannot be passed by any box.** It is a 20% excess at k ≥ 1, and it fails even with every published point resolved. KiDS would need a 21.3% ramp, DES 52%.
- **The framework's own boost is detectable.** B = P_grav/P_part reaches 1.20 at k = 0.3, so injecting it gives χ² of 14–22 on KiDS.

## Part 1. The owner's decision and the frozen rule (`FROZEN_CRITERIA.md`, f6c27d401)

- **New sensitivity tooth T-OWN.** The injected boost is the framework's OWN B(k), from the CFG530 L100 N512 cache, z = 0, both footings. A survey × footing is DIAGNOSTIC only if that injected boost gives χ² ≥ 9 on its surviving points.
  - This rule is post-hoc relative to CFG592. It is disclosed as such in the criteria.
- **Everything else is CFG592's, unchanged:** the support cut (f ≥ 0.9 inside [k_lo, k_hi], N_kept ≥ 10), the nuisances, the statistic Δχ²(F − S0), and the class labels.
- **Framework model:** its MEASURED gravitating P(k, z) at the nodes z = 0, 0.5, 1. "Held" (CFG592's former PRIMARY) replaces "fade" in the robustness set.
- **Box:** L = 100 Mpc/h, N = 1024, chosen by the pre-flight (more kept points, and the strongest own-boost tooth). NSEED 1024 and seed 359 give a new realisation. RMIN = 0.78125.
- **Snapshots:** z = 1, 0.7548, 0.5, 0.2562, 0. The two extras are measurement only.

## Part 2. The lean engine (`cfg596_pm.py`, launcher `run_596.py`)

**Source.** It is a copy of the CFG527 census engine (cfg527_pm.py, sha256 aeabd0ba…), the engine of the CFG530 runs. It runs the RES switch (census edge, shell draw, unfiltered source, cap) and S0. No formula, constant, threshold, switch, mask rule or time step is changed.

**Engineering changes:**
- **FFTs** are in-place and axis by axis on padded buffers. They are bitwise identical to scipy's rfftn / irfftn; this was checked directly and through the V-E gates.
- **Elementwise expressions** are evaluated slab by slab on a thread pool; 1/k² is computed per slab.
- **Kicks** are fused per component, so no particle accelerations are stored.
- **Disk-backed slab fields** (pread / pwrite, not memory-mapped) hold δ, f_sw, w = ν − 1, the f_ret code and the IC field.
- **The census and catchment masks** are stored as packed bits.
- **The resolved-peak search** is shared between the two catchment calls. It is deterministic, so the result is identical.
- **The macOS allocator** keeps freed pages resident; the engine asks it to release them at stage changes. This has no effect on any number.

**Two modes:**
- **exact:** float64 wrapped positions and momenta, unchunked deposit, the original six-field tidal transform, the original IC routine.
- **lean (production):** float32 Lagrangian displacement and float32 momentum, a windowed chunked deposit, factorised tidal transforms, a component-wise in-place IC.

## Part 3. Validation at 256³ (`cfg596_validate.py` → `cfg596_validate.out` / `.json`): ALL GATES PASS

| gate | result |
|---|---|
| V-E(a) exact LRcan L200 N256 vs CFG527 | **bit-for-bit:** P and σ8 at all four snapshots differ by 0; z = 0 positions identical; q_max, n_catch, e_sum, src_sum identical |
| V-E(b) exact S0 L100 N256 (NSEED 512) vs CFG530 | **bit-for-bit;** z = 0 positions identical |
| V-G gravitating P vs CFG555 (527_LRcan_L200) | max \|ΔP_grav/P_grav\| 7.4e-8; \|Δσ8_grav\| 3.2e-9 → PASS |
| V-L lean S0 L100 N256 vs CFG530 | max \|ΔP/P\| 3.9e-8 (k ≤ 2.01); \|Δσ8/σ8\| 3.7e-9 → **STRICT PASS** |
| V-L lean LRcan L100 N256 vs CFG530 | max \|ΔP/P\| 6.3e-8; \|Δσ8/σ8\| 5.4e-9; \|ΔB\| (z = 0) 7.6e-8 → **STRICT PASS** |

- The extra snapshots were confirmed measurement only: exact mode with them on is still bit-for-bit.
- The likelihood pipeline (`cfg596_native.py --test530`) reproduces CFG592 exactly on CFG530 L100 N512, using the held construction. Its outputs are `cfg596_native_test530.out` and `_MUTATE.out`.
  - Δχ² is +23.85 (KiDS) and +4.20 (DES) canonical, +30.04 and +5.56 alt.
  - That box's T-OWN tooth (pipeline check only, no verdict) gives 7.78 / 2.06 canonical and 9.89 / 1.14 alt.

## Part 4. Memory (frozen gate V-M)

| job | peak resident (GB) | note |
|---|---|---|
| 256³ (VEa, VEb, VLs, VLr) | 5.9 / 5.2 / 2.9 / 2.9 | exact mode holds full arrays; the lean 256³ runs are dominated by the NSEED-512 IC |
| 512³ RES, first 12 calls (VMr) | 9.0 (watchdog), 9.9 (ru_maxrss) | measured before the allocator release was added; RSS then included freed-but-resident pages |
| 512³ RES profile with release | 6.6 | live memory about state + 3 fields |
| 512³ S0 full run (VMs) | 8.7 (watchdog), footprint 4.9 | reported comparison with CFG530 S0_L100_N512: max \|ΔP/P\| ≤ 5.6e-8 (k ≤ 4.02), \|Δσ8\| ≤ 6.6e-9 |
| **1024³ RES probe (VMx)**, production settings: IC, zi snapshot, initial force, 3 steps | **39.2 (watchdog), 40.5 (ru_maxrss), footprint ≤ 39.2; swap growth ≤ 2.4 GB** | **V-M PASS (≤ 50 GB)** |

- **An earlier probe was aborted by the frozen swap rule** (+6.6 GB) on code freeze c8825cf4a. The 8.6 GB IC spill was written through the file cache, and the machine's other load left little room. The fix was to open spill files uncached and drop views that kept freed buffers alive (6323b630f). That probe was discarded, and its spill file was removed.
- **Probe step timing at 1024³:** about 370–450 s per step, made up of deposit ~140 s, forces ~100 s and acceleration ~130–200 s.

The analytic model at 1024³:
- particle state: 25.8 GB;
- at most three full mesh fields alive at once: 12.9 GB;
- per-thread temporaries: under 1 GB;
- expected total: about 40–44 GB.

## Part 5. Production (`run_596.py serial VMx P0 P1 P2`, detached, nice 10, 14 threads, watchdog)

- **Order:** the probe VMx, then P0 (S0), P1 (LRcan), P2 (LRalt).
- **Watchdog:** a job is killed if its RSS exceeds 50 GB, if swap grows by more than 4 GB, or if free disk falls below 3 GB. A 1024³ job does not start with less than 18 GB of free disk.
- **Checkpoints:** none. Free disk was 25 GB, below the state + 10 GB that the criteria require. Partial JSON is written after every snapshot.
- **Started:** 2026-10-10 21:40 (P0).
- **Timing estimate** from the 1024³ probe: S0 about 12 h; each RES footing about 16–18 h. Expected finish: P0 about 2026-10-11 10:00, P1 about 2026-10-12 04:00, P2 about 2026-10-12 22:00.
- **Likelihood:** after P0 and P1, run
  ```
  CFG596_MUTATE=1 nice -n 10 python3 cfg596_native.py
  nice -n 10 python3 cfg596_native.py
  ```
  The alt footing stays PENDING until P2 finishes.

## Disclosures (dated 2026-10-10)

- **The new tooth was set after the pre-flight.** It is post-hoc relative to CFG592, whose verdict stands.
- **The production realisation is new.** NSEED = 1024, whereas CFG530 used NSEED = 512. S0 and the framework run share it.
- **Lean-mode numerics differ from exact mode** at the 1e-8 level in P(k) at 256³ (V-L). The 1024³ runs exist only in lean mode.
- **No checkpoints,** because of the disk limit. A crash means a rerun.
- **Flagged ingredients inherited from ΛCDM, as in CFG592:**
  - the EH IC spectrum;
  - the flat w = −1 background;
  - the Δ_ta(z) shell table;
  - the survey nuisance priors;
  - massless neutrinos.

## RESULT (2026-10-12): canonical footing, 1024³ L100 (P0 S0 + P1 RES canonical)

Scored with `cfg596_native.py` exactly as frozen (criteria f6c27d401), after a one-line engineering fix (2026-10-12): the
extra-snapshot merge `dict({...}, **extra)` crashed on float keys and was replaced by `{**{...}, **extra}`; no statistic,
data cut or rule changed. Outputs: `cfg596_native.out/json`, `cfg596_native_MUTATE.out/json`. (numpy matmul RuntimeWarnings
from CFG592's projection appear in the console; every χ² is finite and the pipeline reproduces CFG592 on the CFG530 test.)

- Own boost on the gravitating field, B(z=0) at k 0.3/0.5/1/2/4 h/Mpc: 1.186 / 1.252 / 1.206 / 1.103 / 1.035.
- **KiDS-1000 (N_kept 104 of 225): Δχ²(F − S0) = +68.7** (χ² S0 144.3, p 0.014; F 213.0, p < 0.001); robustness set
  min +43.9 (widen2), noIA +86.0, held-out +61.2, DESI background +56.8; T-OWN tooth PASS (χ²_min 16.4 ≥ 9).
  **Verdict: EXCLUDED** (Δχ² ≥ 9 and every robustness variant ≥ 9).
- **DES Y3 (N_kept 52 of 227): Δχ² = +22.4**, same direction (robust 12.7–44.3), but the T-OWN tooth FAILS (χ²_min 2.4 < 9)
  → **NOT DIAGNOSTIC** as frozen.
- MUTATE: NZ1 bites in every survey (|Δχ²| = 0 when F ≡ S0).
- Alt footing: PENDING (P2 running).

Reading: on raw KiDS-1000 ξ±, with no ΛCDM-calibrated machinery and a same-pipeline comparison, the framework's current
settling rules (candidate B, census supply, phantom sourced by all baryons) put ~19–25% too much power at k 0.3–1 h/Mpc and
are EXCLUDED on the canonical footing. Scope: the L100 box loses 54% (KiDS) / 77% (DES) of points to the support cut; no
baryonic feedback in either arm (same pipeline); S0 itself is marginal on KiDS (p 0.014). The condensed-baryon source
(CFG634 H-CB) is NOT tested by this run. κ = ½ fitted; cold energy mass required; not theory closed.
