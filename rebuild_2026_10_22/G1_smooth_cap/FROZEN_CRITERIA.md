# G1_smooth_cap: FROZEN CRITERIA (written before any script or number)

## 0. The hypothesis under test (outside suggestion, untested)

The 15–19 % excess of the gravitating power over the particle power at 512³ (CFG555/556) is a numerical artefact:
the sharp, non-differentiable cell-wise cap of the settling rule injects high-k aliasing power into the source, that
power grows with resolution (256³ → 512³), and a smooth saturation x/(1+x) over an L★/Jeans-scale kernel removes it.

Scope: this lane diagnoses the **old engine only** (CFG424 lineage). F3 (`rebuild_2026_10_22/F3_growth_audit/`) found the
covariant theory v3 contains neither the settling rule nor an additive QUMOND phantom. Whatever the verdict here, it does
not transfer to v3.

## 1. Where the "cap" is in the engine (`campaign_fresh_gravity/CFG424_turnaround_catchment/cfg424_pm.py`, `forces`, RES, RC = 0)

- `e = fsw * max(s_ph - s_c, 0) * catch` (L409–411). The cell-wise `max(·, 0)` is the non-differentiable step: the
  source is the phantom in excess of the local cold supply, i.e. `s_ph - min(s_ph, s_c)`.
- `fsw = clip(0.5 + (l2 - tau)/(2 EPS), 0, 1)` (L352): already a linear ramp of width EPS = 0.077 (not a step).
- `in_cover` / `catch` masks (L302–338): binary balls. Not the cap; held fixed here (reported, not varied).
- `comp = s_c * q_catchment` (L414–420): per-catchment compensation; `src = e - comp`.
- `x_supply` `min(·, 1)` (L300) is a per-host scalar, not cell-wise; not varied.
- Gravitating density at a = 1: `delta_grav = delta_p + src / (1.5 Om)` (CFG555 method).

## 2. Assumption ledger

| item | class | file |
|---|---|---|
| saved z = 0 particle states (256³ TA-can, 512³ R3, 512³ S0) | engine output (ΛCDM-PROCESSED EH ICs, Newtonian dust) | `../_external_data/cfg424_work/*_z0.npz`, `cfg411_work/*_z0.npz` |
| S0 control spectra | engine output | `cfg359_work/cfg359_S0_FLAT_canonical_N256.json`, `cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json` |
| phantom s_ph from baryon field with ν_mono (additive QUMOND) | STANDARD-MOND-MACHINERY | cfg424_pm.py L376–399 |
| settling cap, catchments, compensation, tidal switch | POSITED RULE | cfg424_pm.py L340–425 |
| Δ_ta table | ΛCDM-PROCESSED | cfg424_pm.py L132–160 |
| phase-weighted Jeans filter W_MIX(k) on the baryon field (k_J at 1e4 K and 1e6 K) | engine's own kernel (POSITED, physical gas Jeans scale) | cfg424_pm.py L380–384 |
| L★ ≥ 21.7 pc | FRAMEWORK-NATIVE (D10) | `doors_push_2026_10_22/D10_native_Lstar/` |
| a₀ canonical footing (TA-can, R3 are canonical runs) | κ = ½ FITTED | engine `A0` |
| growth statistic: max\|P_grav/P_S0 − 1\| for k ≤ 1 h/Mpc, σ8 ratio | CFG361 cuts | cfg555_analysis.py L20 |
| the record's decomposition (86 % source-carried at 512³, k = 0.32) | engine output | cfg555_srccheck.out |

This lane adds no constant. The smooth cap's form is fixed in §3 before any number.

## 3. Variants (fixed now)

- **(a) STEP** (record): `e = fsw * catch * max(s_ph - s_c, 0)`.
- **(b1) SMOOTH, x/(1+x)**: the step is `s_ph - min(s_ph, s_c)`. Replace the hard min by the saturating min
  `s_c * x/(1+x)` with `x = s_ph / s_c` (the harmonic min; no new constant): `e = fsw * catch * s_ph² / (s_ph + s_c)` for
  s_ph > 0, else 0. C¹ at s_ph = 0; → s_ph − s_c for s_ph ≫ s_c.
- **(b1n) SMOOTH, same normalisation**: (b1) rescaled per catchment so Σ_catchment e equals the step's Σ_catchment e
  (fixed by the step, not a knob).
- **(b2) STEP + kernel**: the step's e smoothed with a kernel before the catchment mask and compensation.
  Kernel = the engine's own W_MIX(k) (the grid's Jeans scale, §2). An L★ kernel is the identity on these grids
  (L★ / cell ≈ 3e-5 at 256³), stated and checked numerically (K6).
- **(b3) SMOOTH + kernel**: (b1n) then W_MIX.

## 4. Checks (one line each in `g1_smooth_cap.py`; exit 0 iff all PASS)

- **K0 reproduction.** The lane's lean 256³ re-implementation of the step (chunked deposit, slab-wise eigenvalues,
  < 1 GB RSS) reproduces CFG555's cached `P_grav` for 424_TAcan to ≤ 1e-4 relative on k ≤ 1 and the record's
  max|P−1| 0.075 and r_grav(0.35) 1.0749 to ≤ 1e-3. If K0 fails, nothing below is scored.
- **K1 where the excess sits (record caches, all 256³ and 512³ RES runs in `../_external_data/cfg555_work`).**
  Report k of the max excess and k/k_Ny (k_Ny = π N / L, L = 200 Mpc/h). Also report the excess at k ≥ k_Ny/2.
  PASS = computed. Outcome line: "low-k" if k_max/k_Ny < 0.25 for every run.
- **K2 resolution scaling (record).** Aliasing power at a fixed physical k falls when N rises (the folded power
  comes from |k + 2k_Ny n|, which moves out as N rises). The record's excess at k ≈ 0.3 rises 256 → 512. Report the
  ratio of source auto+cross at fixed k between 256³ and 512³ (same seed, canonical: TA-can vs R3). PASS = computed.
- **K3 direct aliasing measurement.** On a fixed state, evaluate the step (a) on grid N and on the 2N
  Fourier-upsampled fields (s_ph, s_c, fsw spectrally interpolated, masks replicated), truncate the result back to N
  modes, and compare the source's contribution to r_grav at the record's k_max. The difference is the aliasing
  contribution of the cap. Memory restricts this to N = 128 (2N = 256), using the 256³ TA-can state deposited at 128³.
  PASS = computed. Share = |Δ(r_grav − 1)| / |r_grav − 1| at k_max.
- **K4 smooth cap at 256³ (TA-can state, record grid).** Variants (b1), (b1n), (b2), (b3). Report max|P−1| (k ≤ 1),
  r_grav at the step's k_max, and the excess change (r_grav − r_part) relative to the step. PASS = computed.
- **K5 512³ state on the 256³ operator grid.** Stream-deposit R3 512³ and its S0 512³ onto 256³; run (a) and (b1n),
  (b2). If the 512³ excess appears on the 256³ grid, it is carried by the state (the resolved structure), not by
  the operator's grid resolution. PASS = computed.
- **K6 L★ kernel identity.** Gaussian of width L★ = 21.7 pc changes e at 256³ by < 1e-3 relative (rms). PASS iff so.
- **K7 MUTATE.** `G1_MUTATE=1` replaces the step by `e = fsw*catch*s_ph` (no cap). It must break K0
  (reproduction fails). Outputs `*_MUTATE.*`.

## 5. Verdict lines (fixed now)

Let A = aliasing share (K3), S = max over smooth variants (b1n, b2, b3) of |Δexcess| / excess at k_max (K4).
- **ARTEFACT**: A ≥ 0.5 **or** S ≥ 0.5 with (b1n) or (b2) bringing max|P−1| at 512³-state (K5) below 0.10.
- **PHYSICAL (old engine)**: A < 0.2, S < 0.2 at 256³ **and** the excess sits at k_max/k_Ny < 0.25 (K1).
- otherwise **MIXED** (numbers stated).
- **UNDECIDABLE UNDER THE MEMORY LIMIT** if K0 cannot run within 1 GB; state what is needed.
A smooth variant at "same normalisation" that removes the excess by moving mass out of the catchments is reported
as a change of rule, not as a numerical cure.

Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, no PM simulation, CFG960 untouched.
κ = ½ FITTED; footing canonical only (both records used here are canonical; the alt 512³ run 439_A is read in K1 only).

## AMENDMENT A1 (pre-result: written before the first full run produced any K3 number)

K3's PASS line changes from "computed" to a control gate: the linear round trip N → 2N → N of s_ph alone must return
P(k ≤ 1) to ≤ 1e-5 relative. Shares are reported as frozen. Implementation notes (no effect on any definition):
the macOS allocator is run with `MallocMediumZone=0 MallocLargeCache=0` (the script re-execs itself with them; without
them freed 1–16 MB temporaries stay resident and RSS passes 1 GB), particle deposits run in a child process that
streams the npz, and the tidal components are parked on disk. Arithmetic is the engine's (K0 reproduces to 3.3e-7).

## AMENDMENT A2 (post-result)

The §5 ARTEFACT clause "(b1n) or (b2) bringing max|P−1| at 512³-state (K5) below 0.10" is vacuous: on the 256³ operator
grid the step itself already gives 0.077 for the 512³ state. The frozen line returns ARTEFACT through S = 0.553 (b2) and
that vacuous clause. The README reports the frozen outcome and, separately, what the numbers support. Nothing is re-scored.
