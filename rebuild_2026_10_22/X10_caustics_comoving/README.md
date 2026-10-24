# X10_caustics_comoving: with a co-moving khronon start, do X8's soft-side folds persist, and does a focal line form behind each moving mass?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (8a67b46dd7, committed alone before any script or number). **No
amendments.** Two descriptive slips in the frozen text are disclosed under "Execution history"; neither changes a rule.
This lane is X8's model (`rebuild_2026_10_22/X8_soft_side_caustics`, 72515e7e75) with one change, the start. κ = ½ FITTED.
Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the
data favour the framework.

## Verdicts

**(a) Soft-side folds: UNDECIDED (PARTIAL: 4 of 6 O2 cases CAUSTIC, 0 NO-CAUSTIC).** Every check passes. The two O2 t_i 9
cases fold at h = 5 but not at h = 10, so they are NOT CONVERGED.
- **The folds are not removed.** Where the window is long enough (O2 t_i 3 and 6, both footings), the soft lobe still folds,
  converged in h. The co-moving start delays the folds by 1.1–2.0 Gyr against X8.
- **X8's dt sensitivity is gone.** N-dt moves the canonical O2 t_i 3 fold by 0.006 Gyr (X8: 0.221).

**(b) Focal line: FOCAL LINE PRESENT (2 of 24 cells: canonical and alt O2 t_i 9, MW).** Every check passes, including the
three N-checks on the deciding cell (canonical O2 t_i 9 MW).
- **Behind MW, on every O2 case.** A downstream fold forms at t_i + 3.9–4.4 Gyr, converged in h and the same on both
  footings. It forms the same way behind an isolated MW-mass moving through khronon at rest (D-ISO).
- **Upstream stays clean only for ~11 Gyr.** In the four O2 t_i 3 / 6 MW cells the upstream side then drops below 0.5
  (NOT SINGLED OUT). The cause is MW's own held halo folding just ahead of the galaxy. Only the t_i 9 windows (9.07 Gyr) end
  before that.
- **No line behind M31 within any window.** Its held ball is 506 kpc.

**Bottom line.**
- **The folds are not a start artefact.** X8's O2 soft folds are not produced by its v = 0 start. With each galaxy's held
  halo moving with it, the halos follow their galaxies (D-FOLLOW 0.99–1.02, X8 0.51–0.76). The kick-driven stiff folds at
  t_i + 0.5 Gyr disappear. The soft lobe still folds in every case whose window allows it.
- **The folds move.** They now sit 73–156 kpc from MW, at the front of MW's held halo (X8: 14–61 kpc). Most are in-plane
  folds (hoop factor 0.6–1.1), though two h = 5 events are axis collapses (0.02 and 0.008).
- **O1's focal line, now separated from the start transient.** It forms behind MW about 4 Gyr after the start, while the
  upstream side stays above 0.5 for about 7 Gyr more.
- **But the held halo does not survive the wind indefinitely.** After ~11 Gyr its front folds too, in the pair and for an
  isolated mass alike.

## The numbers (`x10_production.out`, `x10_production_results.json`)

**(a) First soft threshold time t_c** (Gyr; J < 0.05 sustained 0.1 Gyr; key `cases[<foot>|O2|t_i <t>].rows[h].event_t`;
X8's from its committed runs):

| case | h 20 | h 10 | h 5 | class | X8 h 10 / h 5 | event at h 10 / h 5: distance to MW, hoop R/R_q |
|---|---|---|---|---|---|---|
| canonical O2 t_i 3 | 16.350 | 15.948 | 15.800 | CAUSTIC | 14.565 / 14.261 | 149 / 109 kpc; 0.78 / 0.62 |
| canonical O2 t_i 6 | 17.970 | 17.391 | 16.648 | CAUSTIC | 15.422 / 15.400 | 156 / 100 kpc; 1.07 / 0.02 |
| canonical O2 t_i 9 | none (S 0.256) | none (S 0.234) | 17.629 | UNDECIDED (h 5 only) | 16.505 / 16.500 | — / 120 kpc; — / 0.80 |
| alt O2 t_i 3 | 16.840 | 15.908 | 15.325 | CAUSTIC | 14.530 / 14.162 | 145 / 73 kpc; 0.78 / 0.85 |
| alt O2 t_i 6 | 17.998 | 17.282 | 16.782 | CAUSTIC | 15.323 / 15.362 | 149 / 112 kpc; 0.96 / 0.008 |
| alt O2 t_i 9 | none (S 0.256) | none (S 0.230) | 17.623 | UNDECIDED (h 5 only) | 16.442 / 16.426 | — / 120 kpc; — / 0.80 |

- **No fold before today.** S by t₀ is ≥ 0.86 in every case (`rows[h].S_by_t0`); every fold is after t₀ = 13.8 Gyr.
- **The events are wind material.** Every event element is a soft label of the at-rest (wind) class (`event.start_class`
  0). None is a straddle label.
- **Footings agree:** t_c to ≤ 0.5 Gyr, S to ≤ 0.005.
- **Hoop factor.** R/R_q is read off the event record (`event.pos[0] / event.label[0]`).

**(a) O1** (no weight in (a)):
- **canonical / alt t_i 3: CAUSTIC**, t_c 13.27 / 12.62 and 13.31 / 12.64. X8 had these UNDECIDED. The event labels are
  soft labels that the rule put inside M31's held ball (`start_class` 2), one or two label rows from the contact surface.
  So this is a consequence of the start's partition (soft khronon boosted with M31), not X8's mechanism. D-HELD: 19 soft
  labels held, 31 soft straddle labels, at h 10.
- **t_i 6:** canonical NO-CAUSTIC (S 0.526 / 0.494); alt UNDECIDED (0.468 / 0.553).
- **t_i 9: NO-CAUSTIC** on both footings, S 0.320 / 0.331 and 0.314 / 0.270. These are X8's values to ≤ 2e-6: here
  the start is X8's except 64 far graded-zone labels.

**(b) Wake cells** (stiff, non-straddle labels on the axis; key `cells[<foot>|<orbit>|t_i <t>|<gal>].per_h[h]`):

| cell | downstream event t_c, h 10 / h 5 (t_c − t_i) | upstream min J, h 10 / h 5 | class |
|---|---|---|---|
| canonical O2 t_i 3 MW | 7.320 / 6.901 (4.32 / 3.90) | −3.13 / −180.6 (first < 0.05 at t_i + 12.3 / 11.2) | NOT SINGLED OUT |
| canonical O2 t_i 6 MW | 10.324 / 9.924 (4.32 / 3.92) | 0.522 / 0.274 | NOT SINGLED OUT |
| **canonical O2 t_i 9 MW** | **13.428 / 12.944 (4.43 / 3.94)** | **0.834 / 0.614** | **PRESENT** |
| alt O2 t_i 3 MW | 7.331 / 6.906 | 0.184 / −78.8 | NOT SINGLED OUT |
| alt O2 t_i 6 MW | 10.323 / 9.929 | 0.522 / 0.288 | NOT SINGLED OUT |
| **alt O2 t_i 9 MW** | **13.451 / 12.968 (4.45 / 3.97)** | **0.834 / 0.632** | **PRESENT** |
| O2 t_i 6 / 9 M31 (both footings) | none; downstream min J 0.95–0.99 | 0.88–0.91 | ABSENT |
| O2 t_i 3 M31 (both footings) | none; downstream min J 0.58 / 0.94 (canonical), 0.46 / 0.94 (alt) | 0.84–0.86 | NOT CONVERGED |
| all 12 O1 cells | events at both h | ≤ −2 | NOT SINGLED OUT |

- **The downstream fold is the wind focusing.** The fold elements are wind labels (`start_class` 0) that started 20–30 kpc
  off the axis in MW's path. They pass through MW's held halo and fold on the axis 76–91 kpc behind MW: the Danby–Camm line
  at small impact parameter.
- **The upstream folds are MW's own held halo.** In the t_i 3 cells the upstream folds are held labels (`start_class` 1),
  40–60 kpc ahead of MW when they first drop below 0.05: the halo is eroded from the front.
- **O1 cells fold on both sides.** The galaxies reverse at apocentre (8.55 Gyr), so both sides are downstream at some
  time. On t_i 6 and 9, MW holds nothing (FROZEN §2), so its halo is kicked as in X8.
- **The bulk stiff fold is now the wake.** In every O2 case the first stiff J < 0.05 in the bulk (`D_STIFF_first_below`,
  straddle excluded) comes at t_i + 3.9–4.45 Gyr, and it is this downstream line. In X8 it came at t_i + 0.5–0.6 Gyr, from
  the kick.

## Checks (`x10_validate.out`, `x10_validate_results.json`; N-checks in `x10_production.out`)

| check | result | numbers (JSON) |
|---|---|---|
| R-X8a X8's own `x8_run.py` (X8_OUT redirected) | PASS | canonical O2 t_i 3 and O1 t_i 9 at h 10: S, S(t₀), t_c, first fold, D-STIFF, n_event all identical (diff 0.0) to X8's committed runs (`checks[R-X8a].detail`) |
| R-X8b this driver, `--start rest` | PASS | the same two cases, diff 0.0. The at-rest start reproduces X8's folds (`checks[R-X8b]`) |
| V-cm boosted single mass, 15.167 Gyr | PASS | max \|J − 1\| (2ε–300 kpc), h 20 / 10 / 5: MW at 74.8 km/s 0.066 / 0.051 / 0.034 (canonical), 0.065 / 0.051 / 0.034 (alt); M31 at 44.9 km/s 0.088 / 0.070 / 0.044, 0.084 / 0.070 / 0.045. Co-moving drift at h 5 ≤ 0.26 kpc (`checks[V-cm].rows`) |
| N-dt / N-box / N-tol (a), canonical O2 t_i 3 h 10 | PASS ×3 | t_c 15.948 → 15.942 / 15.948 / 15.948 |
| N-dt / N-box / N-tol (b), canonical O2 t_i 9 MW h 10 | PASS ×3 | downstream t_c 13.428 → 13.445 / 13.428 / 13.428; upstream min 0.834 → 0.834 ×3 |
| Inherited from X8 (not rerun) | PASS in X8 | R0, V-a1, V-b. The solver is imported unchanged |

- **MUTATE (`X10_MUTATE=1`, wrong-sign boost)**:
  - **V-cm FAILS**, as required: max \|J − 1\| 1.9e4–1.4e6 (`x10_validate_MUTATE.out`).
  - **Production at h 10** (`x10_production_MUTATE.out`, reported only). Halos kicked at 2V fold in the bulk at
    t_i + 0.44–0.47 Gyr. On O2 both wake sides fold by t_i + 0.7–1.6 Gyr, so the downstream/upstream separation disappears.
    The O2 soft events fall 0.04–0.34 Gyr earlier than X8's.
- **Flags.** F1–F4 never fired. Max x was 0.44–0.52 on O2.
- **Contact surface.** Straddle labels fold at t_i + 0.14–0.31 Gyr, matching the kinematic 2h/V = 0.14 / 0.28 Gyr for MW
  (`D_EDGE.first_fold`). They are excluded, as frozen.

## D-ISO: an isolated mass through khronon at rest (diagnostic, `x10_validate_results.json → D_ISO`)

The held ball (e < 0) is boosted and the rest is at rest, run 15.17 Gyr.
- **MW-mass (6e10 M☉, 68.75 km/s, held ball 107 kpc).**
  - The downstream fold comes at t = 4.32 / 3.92 (h 10 / 5, canonical) and 4.33 / 3.93 (alt). Its elements are wind labels
    72–85 kpc behind the mass.
  - The upstream side stays above 0.5 until t ≈ 11–12 Gyr. Then held labels ahead of the mass fold (first < 0.05 at 12.05 /
    11.27).
  - Class: NOT SINGLED OUT.
- **M31-mass (1e11 M☉, 41.25 km/s, held ball 505 kpc).** No fold on either side in 15.07 Gyr: downstream min 0.98 / 0.91,
  upstream 0.79 / 0.82. Class: NOT CONVERGED.

The pair cases reproduce the isolated MW timing to ≤ 0.11 Gyr. So the line behind MW does not depend on M31 or on the saddle.

## What this does not show

- **Symmetry.** The approach is head-on and axisymmetric. The focal line of a point mass in a uniform cold stream is
  generic, but its axisymmetric form here is the symmetry axis. Some soft folds are axis collapses (hoop factor 0.02, 0.008).
  Non-axisymmetric encounters, an impact parameter, other Local Group mass and discs are not run.
- **The start.**
  - The co-moving start is a posed bracket, as X8's v = 0 start is the other, and neither comes from a formation history.
  - Its held extent is the capture law with a sharp edge. Across region boundaries it is not irrotational: there is a
    contact surface, with its labels excluded.
  - A smooth irrotational start would compress the material ahead of each galaxy on the transition scale (FROZEN §0). It
    was not run, because it needs a new shape choice.
  - On O1 the rule gives MW no held halo at t_i 6 and 9, and on O1 t_i 3 it boosts a soft sliver with M31.
- **The held halo's fate.** Its front is eroded after ~11 Gyr, in the pair and for an isolated mass. Why it erodes is not
  diagnosed here.
- **M31.** No line forms behind M31 within the windows. "Every moving mass focuses the wind" is shown only for a mass whose
  held ball is ~100 kpc, at ~70 km/s.
- **The (b) verdict.** The two PRESENT cells are the ones whose 9.07 Gyr window ends before the upstream erosion.
- **Model.** Prescribed kinematic orbits; no back-reaction on the baryons; Plummer point masses (ε = 20 kpc); no Hubble
  flow, no dust, μ_K → 0.
- **Resolution.** Scales below 5 kpc are not resolved. After a fold the particle method is multi-stream, and J values below
  0 mean only "folded". No completion is offered. Quantum strong coupling is not covered.
- **Not a data comparison.**

## Execution history (no amendments)

- **8a67b46dd7**: criteria and ledger, committed alone. Scoping numbers before the freeze are disclosed in its §0: capture
  radii from the orbit formulas, and soft-lobe extents from X8's committed h = 20 arrays.
- **Disclosed slip in FROZEN §2 "Consequences" (descriptive text only; the rule was applied as frozen).**
  - "O1 t_i 9: every label is common" is not exact. 64 far graded-zone labels (up to 27 Mpc from the barycentre, beyond
    MW's 21.6-Mpc capture radius) are held by M31 alone.
  - The O1 t_i 9 numbers equal X8's to ≤ 2e-6 in S.
- **Order of work.**
  - R-X8a/b first, bit-identical.
  - Then V-cm and D-ISO, then 36 main runs, the (a) N-checks, 12 MUTATE runs and 12 MUTATE V-cm runs.
  - The aggregate's frozen rule then named canonical O2 t_i 9 MW as the (b) deciding cell, and its three N-checks
    were run.
- **Post-result readings of existing outputs (no new computation, no verdict weight).** The hoop factors are read from
  event records. The D-ISO "upstream > 0.5 until" times are read from its 0.5-Gyr series.
- **Resources.**
  - All runs exited 0, with no resumes needed. The longest run took 4.1 min (canonical O2 t_i 3, h 5).
  - Peak physical footprint 0.22 GB; peak ru_maxrss 0.35 GB.
  - One thread, nice 15, at most three processes at once. No downloads. The heavy queue and other lanes were not touched.

## Suggested fixes elsewhere (not edited here)

- **V3_FULL_PICTURE §6, "Soft-side caustics in v3s".** Add:
  "X10 (co-moving start): the O2 soft folds persist, delayed 1.1–2.0 Gyr, at the front of MW's held halo, converged in
  4/6 cases. The t_i 9 pair folds only at h = 5. N-dt sensitivity is gone (0.006 Gyr). Frozen reading UNDECIDED
  (PARTIAL 4/6). The v = 0 start does not drive the folds."
- **V3_FULL_PICTURE §6, "Dynamical state of moving subsystems"; O1 §3(ii).** Add:
  "X10: behind MW (held ball ~107 kpc at 70 km/s) the wind focuses into an axis fold at t_i + 3.9–4.4 Gyr, converged, on
  both footings and for an isolated mass. Frozen FOCAL LINE PRESENT (2/24 cells). The upstream side folds after ~11 Gyr as
  the held halo erodes. No line behind M31 within the windows."
- **X8 README, D-WAKE.** "Cannot separate the focal line from the start transient" can point to X10: separated in time
  (4 Gyr vs 0.5 Gyr) and in side.

## Files

| file | contents |
|---|---|
| `x10_run.py` | one production run → `runs/<tag>.json`. Copied from X8's `x8_run.py` with provenance; X8's `x8_core.py` is imported read-only |
| `x10_validate.py` | V-cm and D-ISO single-mass runs (`work/single_*.json`); `--collect` → `x10_validate[_MUTATE].out` / `_results[_MUTATE].json` (R-X8a, R-X8b, V-cm, D-ISO) |
| `x10_batch.py` | the sets repro / single / single_mutate / main / numtests / mutate, ≤ 3 at a time |
| `x10_aggregate.py` | the verdicts → `x10_production[_MUTATE].out` / `_results[_MUTATE].json` |
| `runs/` | per-run json: S, event, WAKE_5b (+ any-sign, wind-only), D-EDGE, D-HELD, D-STIFF, D-FOLLOW, D-WAKE (X8), series, memory |

`work/` (logs, final arrays, single-mass json, the R-X8a outputs) is not committed.

```
python3 x10_batch.py --set repro ; python3 x10_batch.py --set single ; python3 x10_validate.py --collect        # exit 0
python3 x10_batch.py --set main ; python3 x10_batch.py --set numtests ; python3 x10_batch.py --set numtests --case canonical,O2,9
python3 x10_aggregate.py                                                                                       # exit 0
python3 x10_batch.py --set mutate ; python3 x10_batch.py --set single_mutate
X10_MUTATE=1 python3 x10_validate.py --collect ; X10_MUTATE=1 python3 x10_aggregate.py                         # V-cm FAILS
```
(each run: `OMP_NUM_THREADS=1 nice -n 15`, MallocMediumZone=0, set by the batch)
