# FRZ3R RESULT: blind re-grade of the forest row at flux level

**Blind labels, unchanged (RESULT_BLIND.md, 292fe90b51):**

- **As frozen (graded field M): NO VERDICT / NO VERDICT (canonical / alt).**
  - Known answer (b) fails at z 2.2 on both footings, and (e) fails marginally at z 4.4 on canonical.
  - Field M is also 6.7 / 7.4 % negative (floored).
  - Ungraded numbers: flux Delta chi^2 **790 / 904**; matter level of the same fields **10816 / 9672**; ratio
    **0.073 / 0.093**.
- **Reading T (AMENDMENT_A1 5f39677e97; reported, NOT the frozen label): FOREST ROW FAILS AT FLUX LEVEL / FOREST ROW FAILS
  AT FLUX LEVEL.**
  - Reading T is a positive turnaround-scope field. All its known answers pass and both mutations bite.
  - Flux **363 / 425**; matter, same fields, **5035 / 4377**; ratio **0.072 / 0.097**.
  - No bracket crosses the gate (lowest 35.7 / 36.6, lambda_P = 100 proper kpc).
  - It carries about half of FRZ1's matter-level change. Post hoc, scaled to FRZ1: 715 / 874.

A fail reading on these builds is not a frozen label. It needs a build that passes (b) with a positive field. TEST lane:
adopts nothing, relabels nothing (FRZ3 is not relabelled), registers nothing. Footings never pooled. Cold dark energy is a
gravitating field component. Nothing here says the data favour the framework.

## COMPARISON with FRZ3 (opened only after 292fe90b51)

FRZ3 (criteria e56c67ae91, result bf470aefa1): NO VERDICT / NO VERDICT ((b) fails); ungraded flux **4.71 / 2.58**, matter
of the same painted fields **4720 / 4120**, softening **0.0010 / 0.0006**; conditional readings FAILS FRAGILE / HOLDS
FRAGILE.

| item | FRZ3 | FRZ3R | agree? |
|---|---|---|---|
| frozen label | NO VERDICT / NO VERDICT, (b) fails | NO VERDICT / NO VERDICT, (b) fails at z 2.2 (passes at z 3.0 and 4.4) | **agree on the label** |
| matter level, painted fields with about half FRZ1's change | 4720 / 4120 | reading T 5035 / 4377 | **agree** (within 7 %) |
| painted matter ratio at z 3, k 3 / 5 (canonical) | 0.928 / 0.798 | T 0.913 / 0.785 | **agree** |
| flux-level Delta chi^2 | 4.71 / 2.58 | T 363 / 425; M 790 / 904 | **disagree, by a factor 77 to 165** |
| softening (flux / matter) | 0.0010 / 0.0006 | 0.072 / 0.097 (T), 0.073 / 0.093 (M) | **disagree** |
| sign of the flux response | R_F rises +0.1 to +0.9 % at every DESI k | T: rises +2 to +4 % at k_v <= 0.005 s/km; from z 2.8 up falls 2 to 4 % at 0.03 s/km | **agree on the large-scale sign**, ten times the size; disagree at the small-scale end |
| step that softens | saturation (M1: 1.49 -> 975); pressure smoothing x 9 (gas level 538) | saturation (M1 x 63 to 103); pressure smoothing at my lambda_P softens nothing (gas level T 9390 / 7693, M 19896 / 16527) | **agree on saturation; disagree on pressure smoothing** |
| mean-flux matching | absorbs most of what remains | turns the large-scale response positive; does not remove it | disagree in size |
| brackets | cross the gate (lambda_P x 2 and reading V on canonical, lambda_P x 0.5 on alt) | none cross (lowest 35.7) | disagree |

**Why the flux numbers differ (my diagnosis, post hoc).** The two builds differ in two PROVISIONAL inputs. Each moves the
flux Delta chi^2 by a large factor in my own brackets.

1. **Pressure-smoothing scale.**
   - FRZ3 used 80 proper kpc, from memory: 0.216 Mpc/h comoving at z 3.
   - I used 79 comoving kpc: 0.053 Mpc/h, about 4x smaller. This is Kulkarni et al. 2015's lambda_F = 1/k_ps, read twice
     from the paper, which states the value in comoving kpc.
   - My bracket nearest FRZ3's choice (100 proper kpc) cuts reading T's flux Delta chi^2 from 363 / 425 to 36 / 37,
     a factor of 10.
   - At my scale the gas keeps the halo-scale change: gas 1D ratio 0.70 to 0.85, against FRZ3's 0.84 to 0.96.
2. **Halo placement.**
   - FRZ3 placed haloes by biased Poisson on its lognormal field. My primary places them uniformly.
   - My clustered-placement bracket (field M) cuts the flux Delta chi^2 by 7.
   - The two factors together (about 70) cover most of the gap. I did not run them combined, so this is an estimate,
     not a measurement.

Neither choice is settled by the record. The pressure-smoothing scale is the dominant uncertainty. FRZ3's value appears
to be Kulkarni's number with proper and comoving units swapped; that is my reading of the source, through WebFetch, and
PROVISIONAL.

**(b): did my matter-level known answer pass where FRZ3's failed, and why.**

- FRZ1's R_cold divides a turnaround-scope spectrum difference by the standard (r200m) spectrum, which is about half as
  large at k 3 to 5. Any positive field of haloes that hold their turnaround mass therefore realises about half of FRZ1's
  R - 1. That field is FRZ3's painting and my reading T, and the two agree with each other at matter level.
- FRZ3 attributed its shortfall to "extra small-scale power in the reference field" and did not test it. That is right in
  effect: the reference holds turnaround-scope one-halo power of about 2 x P_std.
- My frozen field M reproduces FRZ1 at z 3.0 and 4.4. At k 3 the miss is 0.002 at z 3 and 0.011 to 0.017 at z 4.4.
- It does so with a per-halo change of about twice the profile difference, applied to a reference without turnaround
  outskirts. That makes 6 to 7 % of the volume negative.
- It still fails at z 2.2, where a 20 Mpc/h box lacks the rare massive haloes that carry P_std's one-halo power.
- So: (b) passed partly, at two of three anchors, and only with a non-physical field. The next build needs a box of at
  least about 50 Mpc/h at z 2.2. It also needs a reference whose halo outskirts exist as real matter shared with
  neighbours (an N-body or 2LPT field with haloes found in it), so that FRZ1's convention and a positive field can hold
  together.

## What this does to the question

- Two independent flux-level builds (FRZ3, FRZ3R) agree on the matter level of the painted fields. They agree that
  saturation does the softening, and that the large-scale flux response is positive.
- They disagree by about two orders of magnitude on whether the flux-level Delta chi^2 is near the gate (FRZ3, 2.6 to
  4.7) or far above it (FRZ3R, 363 to 904). The difference traces to the pressure-smoothing scale and to halo clustering
  on the IGM.
- The forest row at flux level remains open. Neither build has a frozen label other than NO VERDICT.
- The deciding input is the gas smoothing scale, which a hydrodynamic forest model would set rather than assume.

## Files and commits

- READING.md 4abb5b4a36 (alone).
- AMENDMENT_A1 5f39677e97 (alone).
- Code, parts and grading outputs beea11ac52 (`frz3r_core.py`, `frz3r_run.py`, `frz3r_turn.py`, `frz3r_grade.py`,
  `frz3r_grade_turn.py`, `run_all.sh`, `run_turn_after.sh`, `parts/*.json`, `frz3r_grade_<foot>[_MUTATE].json/.out`,
  `frz3r_turn_<foot>[_MUTATE].json/.out`).
- RESULT_BLIND 292fe90b51.
- This file, with the post hoc gas-level script `frz3r_posthoc_gas_T.py` and its two JSON outputs.
- Halo-model tables (about 600 MB of npz) are regenerated by the code and were deleted. Console logs are git-ignored.
- Not pushed.
- Machine time about 4.5 h: one job, nice 19, 4 threads, peak resident memory about 16 GB.
- Nothing downloaded. Nothing written outside this folder.

**Commit ids and the lead's checks (added 2026-11-12, after landing; no number or label changes).** Local / origin:
READING 4abb5b4a36 / e8b15feea5; amendment A1 5f39677e97 / 2ab95dbe15; code, parts and outputs beea11ac52 / e3a65c3d97; RESULT_BLIND
292fe90b51 / 3346a9df8b; RESULT a6a0186a48 / 8e3bbb60d8. Pushed. The lead session re-ran the four grader jobs
(`frz3r_grade.py` and `frz3r_grade_turn.py`, each footing) from a copy at the same folder depth, on the committed
part files: all sixteen outputs are equal byte for byte. No field part was regenerated (the halo-model tables were
deleted after the run and a part needs about 16 GB), so this checks the grading, not the fields. The lead also checked
the comparison's central point independently: FRZ3's script sets its pressure-smoothing scale as 80 proper kpc (320
comoving kpc at z 3), and the abstract of Kulkarni et al. 2015 (arXiv 1504.00366), read by the lead through a web
summariser and so PROVISIONAL, gives 79 kpc comoving at z 3. That is a reproduction and a look-up, not a further
independent re-grade. The two flux-level builds still differ by about a factor of nine at matched smoothing; the cause
named above (clustered halo placement) is post hoc and was not run together with the smoothing change.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
