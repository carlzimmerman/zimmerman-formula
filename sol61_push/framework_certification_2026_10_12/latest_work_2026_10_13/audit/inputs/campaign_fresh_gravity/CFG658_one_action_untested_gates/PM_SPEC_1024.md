# CFG658 — spec for a native 1024³ PM with the one-action law (NOT RUN)

Status: specification only. Nothing here has run. Written 2026-10-13 while CFG650's T12 job (`cfg650_pm.py RES canonical 1024`)
occupies the machine; `cfg650_pm.py` must not be edited or touched while any job uses it. κ = ½ fitted; footings never pooled;
cold energy mass required; not theory closed.

## What changes
Only the law's kernel. The CFG650 engine applies the law where it builds the MOND input:
`Dw.write(slice(j, j + 1), nu_mono(y).astype(np.float32) - 1.0)` (cfg650_pm.py, the `fw` slab loop; y = |g_src|/a₀(a)).
The one-action construction's static law is g_N = g²/(g + a₀), i.e. **ν_s(y) = ½ + √(¼ + 1/y)**.

Implementation (after T12 has finished; never on the running file):
1. Copy `cfg650_pm.py` to `CFG658_one_action_untested_gates/cfg658_pm.py` (record the source sha256).
2. Add one switch `CFG658_NU` ∈ {`mono` (default), `simple`}; `simple` replaces the single `nu_mono(y)` call above by
   `0.5 + sqrt(0.25 + 1/y)` (float64 inside the slab, cast to float32 as now). No other line changes.
3. **V-0 (must pass, 256³ L100 NSEED 512 RMIN 0.78125, lean, ≤ 3 GB):** `CFG658_NU=mono` reproduces CFG650's V-0 / VM12 stored
   quantities bit for bit (same caveat as CFG650 V-2: the multithreaded P(k) of an identical array is not bitwise stable; compare
   positions and fields, not P_grav, at the bit level).
4. **V-K (must bite):** `CFG658_NU=simple` changes the z = 0 field (max |Δρ| > 0) and leaves mass conservation at the CFG650 V-C
   tolerances (|src_sum|/e_sum ≤ 1e-9).

## Jobs (declared now; previews are reported, never used to choose)
| job | modules | kernel | footing | why |
|---|---|---|---|---|
| **K12** (primary) | M1 + M2 (= T12) | ν_s | canonical | isolates the kernel against T12 at fixed modules: a same-seed pair (T12, K12) |
| K0 | none (= CFG596 P0 engine) | ν_s | canonical | the construction as built: law sourced by ALL baryons (C\* has no phase label), against S0 = CFG596 P0 |
| K12a / K0a | as above | ν_s | alt | after the canonical pair, if the owner approves the CPU |

Settings exactly as CFG650 §3: RES, L = 100 Mpc/h, N = 1024, NSEED 1024, seed 359, RMIN 0.78125, lean, spill, 14 threads,
nice 10, CFG596's 150-step grid and snapshots (z = 1, 0.5, 0). Start condition: no engine process running (cfg596/636/640/650/658
`_pm.py`) and free + inactive ≥ 48 GB. Abort: RSS > 52 GB or swap growth > 4 GB. Expected peak ≈ T12's (the kernel swap adds no
state); wall time ≈ T12's.

## Scoring (frozen before any K-run number; criteria to be committed alone as an addendum)
- `cfg650_native.py` executed unchanged with the job tag (MUTATE first), raw KiDS-1000 and DES Y3 ξ± through the record's T-OWN
  harness; report absolute χ²/p for every run (Theory v2 reconciliation item 1), Δχ² vs S0, and the (T12, K12) difference.
- Gravitating-field P(k) ratio vs S0 at k = 0.3, 0.5, 1 h/Mpc (z = 0, 0.5, 1), settled-phantom budget and the census-edge radius
  distribution, as CFG650 reports them.
- No ΛCDM or standard-MOND yardstick; S0 is a same-pipeline benchmark, not an observational exclusion.

## What the CONTEXT estimate (cfg658_d2_sparc.py, CFG556 halo model) says to expect
See README §D2: the sign and size of ΔE between ν_s and the recorded kernel at the halo-model level. A PM is needed because the
halo model's comparator is ΛCDM-built and because CFG556 does not reproduce the PM at k ≈ 1.
