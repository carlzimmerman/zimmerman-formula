# X8_soft_side_caustics: do v3s soft-side khronon flows fold at a moving two-body saddle when the khronon's field is solved self-consistently?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (43eedad42a, committed alone before any script). Amendments: A1
PRE-RESULT (c4f6fdaddf, method), A2 PRE-RESULT (fe80bedb81, N-check wording), A3 POST-RESULT (44060708b7, a mechanism
diagnostic with no verdict weight). The open item is the review `reviews/v3s_soft_side_caustics_2026_10_23/` (b362f12477)
and the row "Soft-side caustics in v3s" of V3_FULL_PICTURE §6. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s²,
never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict

**Frozen reading: UNDECIDED (validation N-dt FAILS).** Halving the time step moves the first soft fold of the
N-check case by 0.221 Gyr, against the frozen 0.2 Gyr line. Every other check passes.

**Per case** (§5, h = 10 vs h = 5):
- **CAUSTIC in 6/12:** every O2 case, on both footings.
- **NO-CAUSTIC in 2/12:** O1 t_i 9, both footings.
- **UNDECIDED (not converged) in 4/12:** O1 t_i 3 and 6.

**Bottom line.** In the review's model with the khronon solved self-consistently, soft-side folds are not removed:
- **O2 folds converge and are robust.** On the constant-velocity orbit the soft lobe folds at t₀ + 0.4 to t₀ + 2.7 Gyr,
  converged in resolution, on both footings and in all three numerical variants (t_c 14.34–14.57 Gyr for the N-check
  case).
- **The mechanism is the review's.** Soft elements near the axis are swept up by the approaching MW, fall through its
  inner 10–30 kpc and collapse onto the symmetry axis.
- **Self-consistency only delays the folds:** by −0.03 to +0.39 Gyr (typically 0.1–0.2) against frozen F on the same grid. On the slower timing
  orbit the fold is still in progress when the window closes (r = 300 kpc).
- **The classification cannot certify this.** The folds sit on the axis of an exactly head-on, axisymmetric approach, start
  from the review's unphysical v = 0 khronon (which also folds every positive halo within 0.5–2.1 Gyr), and the earliest
  case's fold time has not converged to the frozen 0.2 Gyr in dt.

So the review's "not established, not excluded" moves to: **established in the review's axisymmetric v = 0 model on the
constant-velocity orbit, but not certified by the frozen checks, and not shown for any non-axisymmetric or co-moving
start.**

## The numbers (`x8_production.out`, `x8_production_results.json` → `cases[<foot>|<orbit>|t_i <t>]`)

**First soft threshold time t_c** (Gyr; J < 0.05 sustained for 0.1 Gyr; keys `rows[h].event_t`):

| case | h 20 | h 10 | h 5 | class | frozen F (MUTATE), h 10 / h 5 | review (frozen F, s = 0) |
|---|---|---|---|---|---|---|
| canonical O2 t_i 3 | 14.680 | 14.565 | 14.261 | CAUSTIC | 14.171 / 14.186 | 14.439 |
| canonical O2 t_i 6 | 15.605 | 15.422 | 15.400 | CAUSTIC | 15.250 / 15.227 | 15.425 |
| canonical O2 t_i 9 | 16.717 | 16.505 | 16.500 | CAUSTIC | 16.347 / 16.303 | 16.436 |
| alt O2 t_i 3 | 14.626 | 14.530 | 14.162 | CAUSTIC | 14.165 / 14.187 | 14.439 |
| alt O2 t_i 6 | 15.470 | 15.323 | 15.362 | CAUSTIC | 15.264 / 15.225 | 15.425 |
| alt O2 t_i 9 | 16.623 | 16.442 | 16.426 | CAUSTIC | 16.331 / 16.289 | 16.436 |

All of these are after t₀ = 13.8 Gyr. **S by t₀** (`rows[h].S_by_t0`) is ≥ 0.59 in every case and resolution, so no
fold lies in the Local Group's past. For O2 t_i 3 the fold lies within a Hubble time of evolution (t_i + 13.8 = 16.8 Gyr).

**At h = 5 the event elements** (runs/`*_h5.json` → `event`) sit as follows:
- labels at R_q = 10–20 kpc, 225–330 kpc on MW's side of the Newtonian null;
- at t_c, at R = 4–15 kpc, 11–33 kpc from MW's centre;
- 76–263 soft labels are below threshold at once (`n_event_elements_max`).

**O1 (timing orbit), S = min soft J in the window** (`rows[h].S`; no event at any h):

| case | h 20 | h 10 | h 5 | class |
|---|---|---|---|---|
| canonical O1 t_i 3 | 0.748 | 0.624 | 0.539 | UNDECIDED (\|ΔS\| 0.085) |
| canonical O1 t_i 6 | 0.554 | 0.434 | 0.508 | UNDECIDED (\|ΔS\| 0.074) |
| canonical O1 t_i 9 | 0.572 | 0.320 | 0.331 | NO-CAUSTIC |
| alt O1 t_i 3 | 0.745 | 0.626 | 0.541 | UNDECIDED (\|ΔS\| 0.085) |
| alt O1 t_i 6 | 0.455 | 0.530 | 0.378 | UNDECIDED (\|ΔS\| 0.152) |
| alt O1 t_i 9 | 0.593 | 0.314 | 0.270 | NO-CAUSTIC |

Frozen F (MUTATE) reaches the threshold in O1 t_i 3 (16.19 / 16.17) and t_i 9 (16.45 / 16.40), and is unconverged in
t_i 6.

**Footings agree** to ≤ 0.1 Gyr in t_c (h = 5, the t_i 3 case) and to ≤ 0.13 in S. They are never pooled.

**Mechanism (A3, `x8_mechanism_O2.out`, `x8_mechanism_O1.out`, `x8_mechanism_*.json`; canonical, h = 10).**
- **Before the approach.** The O2 t_i 3 event label (20, −400) is undisturbed (J > 0.99) until t ≈ 11 Gyr.
- **The fall.** As MW approaches at 70 km/s, the element accelerates toward it (v_z → −66 km/s) and passes 12 kpc from
  MW's centre at t = 14.2.
- **The fold.** Its ring then collapses onto the axis: at t = 14.70, J = 0.008 = hoop factor 0.022 × in-plane
  determinant 0.35.
- **The extent.** At t_c, the minimum soft J by label radius near that height is 0.03, 0.11, 0.06, 0.14, 0.16, 0.34 and
  0.51 for R_q = 20 to 80 kpc. A ~60 kpc region compresses; this is not one lattice column.
- **Debris.** Folded positive material lies within 30 kpc of the element from t ≈ 11.4 Gyr.
- **O1 t_i 9.** The same sequence happens 2 Gyr later: MW sweeps through the S label at t = 16.25 (15 kpc), and the
  window closes at t_end = 16.48 with J = 0.34 still falling. That is why the O1 cases do not converge.

**This is the review's crossing, now with the self-consistent field.** The approaching galaxy's field drags the
near-axis soft khronon in. The halos' own F does not push it away. It shifts the fold by −0.03 to +0.39 Gyr (h 10 and 5) against frozen F
on the same AQUAL sign map.

## Validation (`x8_validate.out`, `x8_validate_results.json`)

| check | result | key numbers (JSON) |
|---|---|---|
| R0 review reproduced | PASS | its own `integrate` on 4 cases: det_min and t_sc identical (diff 0) to `caustics_results.json` (`R0.rows`) |
| V-a1 static single mass, 10 Gyr | PASS | max \|J − 1\| ≤ 4.1e-10, displacement ≤ 5.8e-9 kpc, both footings, h 20/10/5 (`Va1.rows`) |
| V-a2 Galilean-moving single mass, 6 Gyr | PASS | max \|J − 1\| outside 2ε: 0.060 / 0.022 / 0.0075 at h 20/10/5 (`Va2.rows[].max_absJm1_outside_2eps_le300`) |
| V-b linear dispersion, both sides of D·P = 0 | PASS | rate_meas/rate_pred at h 2: L+ 0.9930, L− 0.9903, T+ 0.9952, T− 0.9948 (0.87–0.92 at h 8, 0.97–0.98 at h 4) (`Vb.rows[].ratio`) |
| V-c convergence | per case | above |
| N-box (B_out 10 Mpc) | PASS | t_c 14.565 → 14.370 (\|Δ\| 0.195) |
| N-tol (tol 1e-8) | PASS | t_c 14.565 → 14.442 (\|Δ\| 0.123) |
| **N-dt (dt/2)** | **FAIL** | t_c 14.565 → 14.344 (\|Δ\| 0.221 > 0.2) |

- **MUTATE** (`X8_MUTATE=1`, frozen F; `x8_validate_MUTATE.out`, `x8_production_MUTATE.out`):
  - V-a2 FAILS and V-b FAILS (measured rates ≤ 5e-5 Gyr⁻¹, ratio 0.0000), as frozen;
  - R0 and V-a1 PASS (2/4);
  - MUT-R: every O2 case reaches J ≤ 0 by t_end at h 10. **YES**: this reproduces the review's frozen-F crossings on
    this lane's grid and the AQUAL sign map.
- **Strong-coupling / breakdown flags F1–F4 never fired** (`rows[h].flags`). The hold law converged at every call, max x
  was 2.4 (flux far below the a₀ bound), no particle left the box, and the step floor was never reached.
- **Initial state.** The v3s static solve reaches relative residual ≤ 8e-12, and the net force at t_i is ≤ 1e-8 of
  |g_b|. The stiffness-to-self-force ratio at t_i is ≤ 9e-4 (max), 6e-8 (median).

## D-WAKE (coordinator request, frozen before any number; no verdict weight)

**A fold on the axis forms behind each moving mass, but also in front of it.**
- In every case and at both h = 10 and h = 5, the axis zones (R ≤ 30 kpc) within 1 Mpc of each galaxy, on the
  downstream and on the upstream side, contain positive (stiff-side) labels with J ≪ 0. The minima run from −0.3 to
  −2×10⁴; the large ones are multi-stream values (`D_WAKE` in each run json).
- The downstream line is therefore not singled out.
- **The v = 0 start dominates it.** Every positive halo is kicked against its already moving galaxy. The first stiff
  J < 0.05 comes at t_i + 0.50–0.61 Gyr for every O2 case and O1 t_i 3, at t_i + 1.0–1.2 Gyr for O1 t_i 6, and at t_i + 2.1 Gyr for O1 t_i 9
  (`series[].stiff_now`).
- The halos lag their galaxies: the D-FOLLOW ratio at t₀ is MW 0.51–0.76 and M31 0.69–1.17 (`D_FOLLOW`; O1 t_i 3 excluded: its galaxies have moved only ~20 kpc by t₀).
- **So this lane cannot separate O1's Danby–Camm focal line from the start transient.** It does show that a
  single-stream positive khronon does not survive on the axis near a moving mass in this model. The γ_L stiffness is
  ≤ 9e-4 of the self-force here and does not regularise it.

## What this does not show

- **Symmetry.**
  - The approach is exactly head-on and axisymmetric. The soft folds are collapses onto the symmetry axis (hoop factor
    → 0) and the stiff folds sit on the axis too.
  - In a non-axisymmetric encounter, with an impact parameter, other Local Group mass or a disc, an axis focus is not
    generic. Whether a fold of finite measure survives is not tested.
- **The initial condition.**
  - The khronon starts at rest while the galaxies already move (the review's case definition, kept as frozen). This
    kicks every halo and folds it within 0.5–2.1 Gyr. The folded halo material is near the soft events.
  - A co-moving or adiabatically prepared khronon is not run. Only O1 t_i 9 starts near apocentre, and it does not reach
    the threshold in the window.
- **Model limitations.**
  - Prescribed kinematic orbits: the Newtonian timing orbit and a constant-velocity bracket, not v3s's own two-body
    dynamics.
  - No back-reaction on the baryons.
  - Plummer point masses (ε = 20 kpc).
  - No Hubble flow, no dust, μ_K → 0.
- **Resolution.**
  - Scales below 5 kpc are not resolved.
  - The fold times converge to ≤ 0.04 Gyr for t_i 6 and 9. For t_i 3 they drift by 0.30–0.37 Gyr between h = 10 and 5,
    and by 0.22 Gyr under dt/2.
- **After the fold.** The particle method continues multi-stream; it is not the theory's single-stream fluid, and no
  completion is offered. Post-fold J values (S down to −10²) carry no meaning beyond "folded".
- **Not covered.** Quantum strong coupling (the strong-coupling review covers it). The DBI K, and any EFT validity at
  the axis focus itself.
- **Not a data comparison.**

## Execution history and amendments

- **43eedad42a**: criteria and ledger, committed alone.
- **c4f6fdaddf (A1, PRE-RESULT, not blind).**
  - The frozen node-centred FV + momentum-conserving CIC scheme failed its own static test in development:
    |J − 1| 0.19 at h 5, and the kick energy grew ×85 in 3 Gyr.
  - Replaced by Q1 finite elements + quadratic-B-spline energy-conserving particles; the discrete v3s switched static
    equilibrium as the initial state; a fast-diagonalisation Laplacian and Newton–PCG (the sparse factors reached
    0.83 / 2.1 GB); an adaptive dt with flag F4; MallocMediumZone = 0.
  - Axis labels (near-massless tracers in the ring representation) are excluded from J statistics, and the soft set is
    the discrete phantom sign.
  - Development numbers are disclosed in A1, including one development run of the final method on canonical O2 t_i 3 at
    h 10.
- **fe80bedb81 (A2, PRE-RESULT).** N-checks compare t_c when the base case folds, and S otherwise, as §5 does.
- **44060708b7 (A3, POST-RESULT).** The mechanism diagnostic, declared before it was computed. No verdict weight.
- **Production.**
  - 36 main runs, 36 MUTATE runs, 3 N-check runs and 2 mechanism runs, all with exit 0 and no resumes needed.
  - The longest run took 5.9 min (canonical O2 t_i 3, h 5).
  - Peak physical footprint 0.22 GB; peak ru_maxrss 0.34 GB (R0: 0.53 GB).
  - One thread, nice 15, at most three processes at once. No downloads. The heavy queue was not touched.

## Suggested fixes elsewhere (not edited here)

- **V3_FULL_PICTURE §6, row "Soft-side caustics in v3s".** "OPEN: not established, not excluded" can become:
  "self-consistent axisymmetric solve (X8): the O2 soft lobe folds at t₀ + 0.4–2.7 Gyr, converged in h and on both
  footings. Same mechanism as the review's (near-axis soft khronon swept through the approaching galaxy and collapsed onto
  the axis). Frozen reading UNDECIDED (N-dt 0.221 > 0.2 Gyr). Open: non-axisymmetric encounters and a co-moving start."
- **The review's A2 hypothesis** ("the halos' own fast F should push negative elements away") is not borne out in this
  model: self-consistency shifts the folds by −0.03 to +0.39 Gyr only.
- **The positive (stiff-side) halos fold on the axis within 0.5–2.1 Gyr of a v = 0 start.** This bears on O1 §3(ii)'s
  focal-line item and on any lane that starts a khronon at rest around moving masses.

## Files

| file | contents |
|---|---|
| `x8_core.py` | Q1 FEM + B2 particle solver, orbits, static equilibrium |
| `x8_run.py` | one production run → `runs/<tag>.json` |
| `x8_batch.py` | runs a set, ≤ 3 at a time, with resume |
| `x8_aggregate.py` | the verdict → `x8_production[_MUTATE].out` / `_results[_MUTATE].json` |
| `x8_validate.py` | R0, V-a1, V-a2, V-b → `x8_validate[_MUTATE].out` / `_results[_MUTATE].json` |
| `x8_mechanism.py` | the A3 diagnostic → `x8_mechanism_*.json`, `x8_mechanism_O1.out`, `x8_mechanism_O2.out` |
| `runs/` | per-run json: S, event, flags, D-WAKE, D-STIFF, D-FOLLOW, series, memory |

`work/` (checkpoints, logs, final particle arrays) is not committed.

```
OMP_NUM_THREADS=1 nice -n 15 python3 x8_validate.py --part R0|Va1|Va2|Vb ; python3 x8_validate.py --collect
python3 x8_batch.py --set main ; python3 x8_batch.py --set numtests ; python3 x8_aggregate.py          # exit 1 (N-dt FAIL)
X8_MUTATE=1 ... x8_validate.py ... ; python3 x8_batch.py --set mutate ; X8_MUTATE=1 python3 x8_aggregate.py
```
