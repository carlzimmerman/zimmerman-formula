# XJ1R BLIND BRIEF (2026-11-14, written 13:43 EST by the clock): a blind grade of one candidate statement about rule 6

Written by the lead and committed alone, before the blind builder is started. It states a question, definitions and
gates. It contains no result of any lane that has computed this statement. The blind builder writes its own
FROZEN_CRITERIA.md from this brief (its own known answers, twins, brackets, compute plan and hand estimate), commits it
alone before any script exists, and builds from there. Where this brief and the builder's criteria differ, the
builder says so in its criteria; the gate numbers below are not to be changed.

TEST lane, BLIND. Adopts nothing, relabels nothing, registers nothing. Footings (canonical a0 = 9.3603e-11 m/s^2, alt
a0 = 1.1312e-10 m/s^2) are graded separately and never pooled. Cold dark energy is a gravitating field component; no
particle is added. kappa = 1/2 and the share 5.41 are FITTED. Rule 6 is a candidate, NOT ADOPTED. A HOLDS label means
"not excluded in this build"; it does not say the data favour the framework over LCDM.

## 1. The statement to be graded

For k = 2 and for k = 3, separately:

> In a system slower than v*(z) the cold component follows the law's own layout, unscaled, inside the k-th caustic of
> the clock's infall, R_set = R_k(z, M_b). Outside R_set the rest of the system's cold component keeps the reference
> layout's shape. A system faster than v*(z) keeps the reference layout at every radius.

## 2. Definitions (all in FRZ1's halo model as FZS1 and FWN1 use it; earlier lanes' files are read-only)

For a halo at redshift z on a footing: M_B(r) is FRZ1's layout mode "B" (the law's layout), M_R(r) its mode "Rb" (the
reference), Bar(r) FZS1's `Bar`; C_B = M_B - Bar, C_R = M_R - Bar, C_tot = C_R(r_ta).

- **Boundary:** a halo with FRZ1's v_vir > v*(z) keeps M_R at every radius. v*(z) = v*(0) / E(z),
  v*(0) = a0 / (10 (1 + 5.41) H0), H0 67.4, Omega_Lambda 0.6847, flat.
- **The exact junction:**
  - r <= R_set: M(r) = M_B(r).
  - r > R_set: M(r) = Bar(r) + C_B(R_set) + t [C_R(r) - C_R(R_set)], with
    t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)], so that M(r_ta) is the halo's turnaround mass.
  - This is NOT the junction earlier lanes used for the settled radius (FZS1's, which multiplies the law's cold
    component inside R_set by a factor so that the enclosed cold mass at R_set equals the reference's). The control
    below uses FZS1's junction; the graded cases use the exact junction.
- **The caustics:** FLD1's construction (`fable52_push/FLD1_fold_reach/`: `fld1_shells.py`, its FROZEN_CRITERIA.md and
  RESULT.md, stored runs in `runs/`): independent radial shells of a clock that starts as cold dust in the Hubble flow
  at z = 10 around a softened point mass of baryons, in the law's static field, with FLD1's device at the centre.
  **R_k(t) is the largest current radius among shells that have passed through the centre at least k times.** R_1 must
  equal FLD1's fold radius R_fold (a known answer for the builder's own passage counter). Use FLD1's primary settings
  (its 12 baryon masses, both footings, N 2400, start z 10, the law on), and for a halo use FZS1's rules for R_fold
  unchanged (its interpolation in z and in log M_b, its `Mb_fold`, its conversion to comoving units), capped at the
  halo's r_ta. No constant multiplies R_k.

## 3. What is graded

**(a) The forest at flux level, in FWN1's build.** A copy, in this folder, of
`closure_2026_11_13/FWN1_forest_flux_split_f_ceiling/` (`fwn1_tables.py`, `fwn1_run.py`, `fwn1_grade.py`,
`fwn1_c0.py`; its FROZEN_CRITERIA.md sections 2 to 8 give the build, seeds, statistic, known answers, twins, brackets
and label rule), with the layout function replaced by the statement of section 1. Cases: **SEc2** (k = 2), **SEc3**
(k = 3) and the control **S5** (FZS1's junction at 5 R_fold, which must reproduce FWN1's stored S5 on the seeds the
builder recomputes, and must still fail). Statistic: FWN1's D, the 12-bin flux-level Delta chi^2 against the reference
on DESI DR1 P1D with the full covariance. **Gate: D <= 4.** Labels per case and footing by FWN1's section 8: FOREST
ROW HOLDS AT FLUX LEVEL / FOREST ROW FAILS AT FLUX LEVEL / NO VERDICT (cause named), FRAGILE with the bracket named.

**(b) Do today's rotation curves lie inside?** For each of SPARC's 175 galaxies (PD1's loader and baryon mass: the
largest enclosed baryon mass at mass-to-light 0.5; brackets 0.3 and 0.8): the last measured radius against R_k(z = 0;
M_b), k = 2 and 3. **Gate: no galaxy beyond R_k.** Inside the settled radius the exact junction is the law itself, so
a galaxy wholly inside keeps PD1's rotation-curve numbers; any galaxy beyond is named with its ratio.

**Lane word, per footing and per k:**
- "CAUSTIC k HOLDS, BLIND" if (a) reads HOLDS and (b) finds no galaxy beyond (FRAGILE carried from (a));
- "CAUSTIC k FAILS THE FOREST, BLIND" if (a) reads FAILS;
- "CAUSTIC k CUTS ROTATION CURVES, BLIND" if (b) finds a galaxy beyond at mass-to-light 0.5 (it may be given beside
  either forest word);
- otherwise "NOT RESOLVED", with the cause.

Reported, never a label: R_k / R_fold by redshift and mass; t per case; per-bin D; the matter-level number by the
record's older route if FWN1's `fwn1_c0.py` gives it.

## 4. Blindness (the builder must keep to this and say in its result what it opened)

Forbidden to open, list, search or diff, in the working tree and in git history:
- `closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface/` (everything in it);
- `closure_2026_11_13/CJ1_candidate_completion/` (it will be updated today);
- any assistant memory directory or session transcript, and any handoff file dated 2026-11-14;
- `git show`, `git log -p` or `git diff` on any commit whose subject begins with "XJ1" (subjects carry no outcome
  word; the commit list itself may be seen).

Allowed: this brief; FLD1, FRZ1, FZS1, FRZ3R, FRZ4, FRZ6, FRZ6R, FWN1, FWN1R, FWN2, JNT2, JNT2R, SRH1, PD1 and QX8
folders and every other lane dated before 2026-11-14 (their numbers are for FZS1's junction or for no settled radius
and say nothing about the exact junction or the caustics).

## 5. Procedure

- Own FROZEN_CRITERIA.md committed alone (explicit path) before any script; scripts committed before they are run; the
  grader committed before any part is read; mutation and twin outputs in separate files; frozen files never edited
  (fix forward with a dated amendment committed alone).
- Commit with explicit paths only (`git add <paths>` then `git commit -m ... -- <paths>`); the index is shared with
  other sessions. Never rewrite history, never push (the lead pushes). Commit subjects carry no outcome word.
- No personal names, no home-directory paths and no personal communications in any file. Say "cold dark energy".
  Every file ends with: `kappa = 1/2 FITTED; not theory closed. Adopts nothing.`
- Heavy compute: `nice -n 19`, `python3 -I -B`, one part per process, a runner that starts a part only when at most
  two other heavy forest processes are alive and free disk is at least 10 GB, and stops below 8 GB free disk or above
  14 GB swap; never wait with `pgrep -f` on a pattern that matches the waiting shell itself. Nothing is downloaded.
  Nothing is written outside this folder. A marker file `run_r.done` is written when the last part is done.
- Read the clock (`date`) before writing any time into a file.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
