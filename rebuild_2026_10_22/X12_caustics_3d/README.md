# X12_caustics_3d: without axial symmetry, does the khronon wake behind a moving Milky Way-mass galaxy still focus, and do the soft-side folds survive an impact parameter?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (423099070f, committed alone before any script or number).
Amendments: **A1 POST-RESULT** (a0c877fd87) and **A2 POST-RESULT** (ec3d40764b), both diagnostics of the failed check with
no verdict weight. Lane launched from the open items of X8 and X10 ("the axis collapse and the axis focus may be artefacts
of axisymmetry") and the V3_FULL_PICTURE §6 rows "Soft-side caustics in v3s" and "Dynamical state of moving subsystems".
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing
here says the data favour the framework.

## Verdicts

**(a) Wake focus in 3D: UNDECIDED (3D NOT VALIDATED: V-cm FAILED).**
**(b) Soft-side folds at b > 0: UNDECIDED (3D NOT VALIDATED: V-cm FAILED).**

- The 3D solver failed its frozen Galilean check (V-cm). The M31 row is 0.0819 at h 15 and 0.0930 at h 10. Both values are
  below the 0.1 line, but the frozen rule also requires h 10 ≤ h 15, so the row fails. The MW row passes.
- By the frozen stop rule (§4), no 3D wake (W) or encounter (E) run was made at any b. The 3D-against-2D cross-checks
  (X-ISO, X-B0), the N-checks and the production MUTATE runs were not run either.
- **So this lane gives no 3D answer to either question.** It does not say whether X8/X10's axis collapse and wake focus are
  artefacts of axisymmetry. That item stays open.
- **The failure is a property of the 3D solver, not of the test.** A1 and A2 (post-result, no verdict weight) rule out the
  test box, the mirror planes and the time step. All three variants reproduce the h 10 value to 4 decimals (0.0929–0.0930).
  The excess sits at the edge of the Plummer core, 40–50 kpc from the moving mass, on the grid axes through it. At h 10 it
  stays at ≈ 0.02 until 8–9 Gyr, then grows to 0.093 at the end of the 15.17 Gyr window.

## The numbers

Collected in `x12_validate.out` / `x12_validate_results.json` (key `checks[<id>]`) and in `x12_amendments.out` /
`x12_amendments_results.json` (key `rows[<tag>]`).

**R-X10: PASS.** X10's 2D isolated-MW D-ISO runs, reproduced with X10's own driver (copied as `x12_2d.py`; X8's
`x8_core.py` imported read-only), MW at both footings and h 20 / 10 / 5:
- **Bit-identical to X10's committed values.** down_event.t, down_min.J, up_min.J, up_event.t, D_EDGE.J and D_STIFF.J all
  differ by 0.0 (`checks[R-X10].rows[].fields`).
- **The 2D reference over the frozen wake window [0, 9.067 Gyr]** (`rows[].Wa`), canonical and alt:

| h | downstream event (Gyr) | J_up (min) | J_down (min) |
|---|---|---|---|
| 20 | 4.880 / 4.900 | 0.814 / 0.816 | −1.44 / −1.36 |
| 10 | 4.321 / 4.332 | 0.816 / 0.818 | −7.62 / −7.75 |
| 5 | 3.922 / 3.928 | 0.816 / 0.816 | −37.5 / −33.4 |

So in 2D the isolated-mass cell would be PRESENT on this window. No 3D counterpart was run.

**V-a1 (3D static, M31 at rest, 10 Gyr): PASS** (`checks[V-a1].rows`). Max |J − 1| was 6.5e-12 / 1.3e-11 / 3.5e-11 at h 20 /
15 / 10 (canonical) and 6.3e-12 / 1.3e-11 / 3.2e-11 (alt). Displacement was ≤ 3.0e-10 kpc. The discrete v3s switched
equilibrium is force-free to round-off: max |a| at t_i ≤ 1.2e-11 kpc/Gyr².

**V-cm (3D Galilean, canonical, 15.167 Gyr): FAIL** (`checks[V-cm].rows[].max_absJm1_outside`). The statistic is max |J − 1|
over labels at 2ε ≤ |q| ≤ 300 kpc.

| mass, boost | h 20 | h 15 | h 10 | rule (≤ 0.1 at h 15 and 10, h 10 ≤ h 15) |
|---|---|---|---|---|
| MW, 68.75 km/s | 0.1326 | 0.0574 | 0.0552 | pass |
| M31, 41.25 km/s | 0.1329 | 0.0819 | **0.0930** | **fail** (h 10 > h 15) |

Inside 2ε the values were 0.08–0.26 (reported only). Flag F3 fired in the MW runs at 11.9–12.6 Gyr: boosted labels near the
outer z face left the 5 Mpc box. F1, F2 and F4 never fired.

**MUTATE (`X12_MUTATE=1`, wrong-sign boost): V-cm FAILS as required.** Max |J − 1| was 1.7e4 / 6.3e4 for MW and 1.1e4 / 9.4e4
for M31, at h 15 / 10 (`x12_validate_MUTATE.out`).

**A1 / A2 (POST-RESULT diagnostics, declared before they were computed; M31, canonical; `x12_amendments.out`):**

| variant | h 15 | h 10 | reading |
|---|---|---|---|
| frozen box | 0.0819 | 0.0930 | the failure |
| A1-loc (frozen box rerun) | 0.0819 | 0.0930 | identical `vstat` (reproduced: True) |
| A1-box (fine z [−600, 1260]; MW [−660, 1680]) | 0.0818 | 0.0929 | not the box (MW 0.0569 / 0.0529) |
| A2-mir (full domain, no mirror planes, 1.49M nodes) | — | 0.0930 | not the mirror planes |
| A2-dt (dt₀ and 0.15 halved, 2770 steps) | — | 0.0930 | not the time step |

- **Where the maximum sits.** It is on labels 40–51 kpc from the moving mass, on the grid axes through it, at both h. Examples
  at h 10: (40.8, 0, 0), (0, 40.8, 0), (9.6, 0, −49.7); the full-domain run gives the same points mirrored, for example
  (−40.7, 0, 0) and (0, −40.8, 0).
- **When it grows.** At h 10: 0.007 at 2 Gyr, 0.019 at 4, 0.020 at 8, 0.050 at 10, 0.056 at 12, 0.082 at 14 and 0.093 at
  15.17 Gyr (`rows[...].series_1Gyr`). At h 15 it is larger early and levels off near 0.08.
- **Reading (a hypothesis, not tested).** This is a grid-crossing (Galilean) error of the Cartesian discretisation. The
  Plummer core (ε = 20 kpc) is resolved by only 2–4 cells, and the error accumulates after the core has crossed 40–60 cells.
- **The quarter-domain mirror construction is exact.** The full-domain run equals the quarter-domain run to 4 decimals, and
  the deposit and force checks below agree.

## What this does not show

- **Neither question is answered.** No 3D wake or encounter run exists. Nothing here says whether the 2D axis collapse (hoop
  factor 0.008–0.022), the 2D wake focus or the O2 soft folds survive in 3D or with an impact parameter. The rows of
  V3_FULL_PICTURE §6 stay exactly as open as before.
- **The V-cm failure does not make X8/X10 wrong.** Those lanes passed their own 2D checks. Their open item, non-axisymmetric
  encounters, is untouched.
- **It does not show that the 3D solver would mislead in production.**
  - The failing row is a 41 km/s M31-mass equilibrium translated across the grid for 15.17 Gyr. Its error is below 0.1 at
    both resolutions and is concentrated 40–50 kpc from the mass.
  - Whether that would move an MW-side fold or a wake event was never tested. The frozen rule stops the lane before that.
  - Arguing that it would not matter would be a post-hoc rescue, and none is made.
- **The h 5 behaviour is unknown.** Resolutions h ≤ 7.5 kpc do not fit under 1 GB in this design (FROZEN §0), so whether the
  error converges at finer h is not known.
- **Model limits (had it run).** Prescribed straight-line kinematic orbits, Plummer baryons, no Hubble flow, no dust,
  μ_K → 0, no back-reaction, and the X10 co-moving start (a posed bracket).
- **Not a data comparison.**

## Execution history

- **423099070f.** Criteria and ledger, committed alone. Scoping before the freeze was one BLAS timing only (disclosed in
  §0).
- **Development (scratchpad, not committed; operator unit tests on a 27 × 27 × 53 grid, no physics case).**
  - Fast-diagonalisation solve: relative error 1.3e-11.
  - Residual against a finite-difference derivative of the discrete energy: 1.2e-8, 6.1e-8 and 2.9e-7 (c = 1, μ, 1 − μ).
  - Hessian-vector product against a finite difference: 3.1e-8.
  - TSC deposit of the deconvolved masses: reproduces the nodal masses to 5.5e-16.
  - Particle force against a finite-difference gradient of the deposited energy: agrees to ≤ 1.3e-9 relative in the fine
    zone, including particles at negative mirrored coordinates, and to 3.8e-7 for one particle in the graded zone.
  - The first 3D physics run was the scored V-a1 h 20 run. No W or E case was ever run, in development or otherwise.
- **Order of work, as frozen.** R-X10 (6 runs, ≤ 87 s each) → V-a1 (6) → V-cm (6) → stop. Then MUTATE V-cm (4), A1 (6 runs)
  and A2 (2 runs).
- **A1 (a0c877fd87, POST-RESULT).** Committed after V-cm was scored and before the A1 runs. Its candidate mechanism (coarse
  graded-zone labels entering the fine zone) was refuted by its own A1-box test.
- **A2 (ec3d40764b, POST-RESULT).** Committed after A1's runs and before A2's.
- **Code changes after scoring.** The `--a1` / `--a2` options and the series location field add diagnostics only.
  A1-loc reproduces the frozen runs exactly. The not-run checks are labelled NOT RUN instead of FAIL in the collectors.
- **Resources.**
  - All 30 runs (24 3D, 6 2D) exited 0, with no resumes needed. The longest run took 14.1 min (A2-mir).
  - Peak sampled physical footprint 0.28 GB. Peak ru_maxrss 0.93 GB (A2-mir, full domain), 0.34 GB otherwise.
  - One thread, nice 15, at most two processes at once. No downloads. The heavy queue (L1) and other lanes were not
    touched. Free memory was 32.5 GB at the start, and the batch checked for ≥ 6 GB before each start.

## Suggested fixes elsewhere (not edited here)

- **V3_FULL_PICTURE §6, row "Soft-side caustics in v3s" (and "Dynamical state of moving subsystems").** Add: "X12 (3D,
  impact parameter): UNDECIDED, no 3D result. The 3D self-consistent solver (variational FD + TSC, h 10–20 kpc) failed its
  frozen Galilean check (M31-mass V-cm 0.082 / 0.093 at h 15 / 10, non-monotone; a core-edge grid-crossing error, not the box,
  mirrors or dt), so the stop rule held. Whether the axis collapse and wake focus are axisymmetry artefacts remains open."
- **A successor lane needs a re-frozen design that removes or resolves the moving-core error before any production number.**
  Options, with no claim that any of them passes:
  - run case W in the galaxy's rest frame, with the khronon wind streaming through a static core;
  - nested refinement to h ≤ 5 kpc around the cores;
  - a V-cm line frozen with a resolution ladder that reaches the converging regime.
  The 2D references in `x12_validate_results.json → checks[R-X10].rows[].Wa` and the half/quarter-domain mirror code (A2-mir
  shows it is exact) can be reused.

## Files

| file | contents |
|---|---|
| `x12_kern.c` | compiled kernels: variational residual and Hessian, batched tridiagonal solve, TSC deposit and gradient, J, ω_max (built into `work/`) |
| `x12_core.py` | grid, fast diagonalisation, AQUAL Newton–PCG, v3s switched equilibrium, Anderson hold law, `Sim3` |
| `x12_run.py` | one run (`--kind static / vcm / wake / enc`; N-check variants; `--a1`, `--a2` diagnostics) → `runs/<tag>.json` |
| `x12_batch.py` | sets validate / wake / b0 / bpos / numtests / mutate / a1 / a2 / mutate_vcm, ≤ 2 at once, with resume |
| `x12_2d.py` | R-X10: X10's 2D D-ISO driver copied with provenance, plus the [0, W_a] window statistics |
| `x12_validate.py` | R-X10, V-a1, V-cm, X-ISO, X-B0 → `x12_validate[_MUTATE].out` / `_results[_MUTATE].json` |
| `x12_aggregate.py` | the verdicts → `x12_production.out` / `x12_production_results.json` (stop rule applied) |
| `x12_amend.py` | A1 / A2 diagnostics → `x12_amendments.out` / `x12_amendments_results.json` |
| `runs/` | per-run json: vstat (V-a1 / V-cm statistics), series (with the A1 / A2 location of the maximum), flags, resources |

`work/` (logs, checkpoints, the compiled library, the 2D run json) is not committed.

```
python3 x12_batch.py --set validate ; for f in canonical alt; do for h in 20 10 5; do python3 x12_2d.py --foot $f --h $h; done; done
python3 x12_validate.py            # exit 1: V-cm FAIL, X-ISO / X-B0 NOT RUN (stop rule)
python3 x12_aggregate.py           # both verdicts UNDECIDED (3D NOT VALIDATED)
python3 x12_batch.py --set mutate_vcm ; X12_MUTATE=1 python3 x12_validate.py      # V-cm FAILS (wrong-sign boost)
python3 x12_batch.py --set a1 ; python3 x12_batch.py --set a2 ; python3 x12_amend.py   # POST-RESULT diagnostics
```
(each run: `OMP_NUM_THREADS=1 nice -n 15`, MallocMediumZone=0, set by the batch)
