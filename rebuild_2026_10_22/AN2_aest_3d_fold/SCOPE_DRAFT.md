# AN2_aest_3d_fold: SCOPE AND DRAFT CRITERIA. Nothing run, nothing frozen

Scoping only, at the owner's request after AN1. No script exists and no number here comes from this lane. If the owner says go, section 4 is revised and committed alone as `FROZEN_CRITERIA.md` before any script. Authority for the lane class: `OWNER_DECISION_2026-11-02_ONE_ACTION_LANE.md`; a run still needs the owner's go. kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## 1. The question
AN1's caveat: a radial flow focuses on its centre by symmetry. **Does the single-valued field reach the well, meaning M_d >= M_ph inside R_test, before its first fold, once the peak isn't spherical?**

## 2. What 3D can and can't decide
- **It can close AN1's symmetry caveat**, or find that symmetry caused the fold.
- **It can't go past the first fold.** L1's particles cross freely, which isn't the single-valued field: it's a multi-stream completion the action doesn't supply. X14: a real cure costs a constant, with C1's beta the one surviving class. Running that is a separate decision.
- **It can't touch** H1's ghost, C1 and M1's planets, C7's K_B runaway, or H2 and S4's static cluster shape.
- **It can't resolve discs.** A 256^3 grid on a 1e12 peak has cells of about 40 kpc comoving, so 2.2 R_d isn't readable. Cluster R500 is coarse.
- **Phase-pinning is already closed in 3D** (`real_research/aest_3d_nbody/VERDICT.md`) and isn't repeated.

**Expectation, before any run, unverified.** For dust, a triaxial peak's first axis collapses earlier than the spherical case (ellipsoidal collapse, from memory, PROVISIONAL). X14 finds caustics generic analytically. So the likely result is an earlier fold, in a sheet instead of a point. The open part is low mu, where the hold term acts.

## 3. Stages and cost
Timing comes from L1's README, not from a benchmark of this setup. Its 128^3 run takes 4-8 min on one thread; a factor of about 3 is assumed for hold solves in a collapsing peak.

| Stage | What | Size | Thread-hours | Peak memory | Disk |
|---|---|---|---|---|---|
| **S0** | Homogeneous ellipsoid, dust limit, AN1's amplitudes | small | under 1 | under 1 GB | under 1 MB |
| **S1** | L1's engine plus constrained peak and fold tracker, 128^3 | 16 rows: 1e12, 1e15; mu 0.1, 56.6; two shapes; two footings | 3-6 | under 1 GB footprint (L1: 0.27; RSS up to 2.3) | under 100 MB |
| **S2** | Full grid, 256^3. **Only if S1 surprises** | 48 rows: mu 0.1, 1, 10, 56.6; three shapes | 30-65 | about 2-4 GB | under 1 GB |
| **S3** | Win verification at 512^3 on 8 threads. **Only if S2 reaches the well** | 4 rows | 50-130 | 17-35 GB | keep under 5 GB |

- **Disk:** 20 GB free, under the 30 GB gate on record. S0 and S1 fit. S3 needs the disk cleared first, and no competing heavy runs.
- **Engineering:** constrained initial conditions, the fold tracker and K_B = 0 known answers are new. AN1 and AR1 each took about 300-360k agent tokens; expect similar.
- **The floors** mu 2.04e4 and 1.24e8 /Mpc have pi/mu below any cell. They read as dust, so S0 covers them.
- **K_B 0.078** isn't in L1's system. Not run; stated as a limit.

## 4. Draft criteria
**Setup.** AN1's background, masses, baryon treatment and amplitude rule. Peak shapes: ellipticity e from Gaussian peak statistics at the row's height, fixed before running, not tuned. Zero shape must reproduce AN1.

**Fold.** Track the deformation tensor on the Lagrangian particle grid; a fold is det J <= 0 for any particle. Report two times, because a fold ends the solution only in its causal future: first fold anywhere, and first fold within q(M_tot).

**Row result.** First fold z; shape of the fold (sheet, filament, point); M_d, M_b and M_ph inside R_test at that time. R_test: R_last for 1e12, R500 for 1e15.

**Labels.**
- **FOLDS NO LATER THAN SPHERICAL:** every resolved row folds at z >= AN1's strict z, within tolerance.
- **DELAYED, STILL ENDS:** some row folds later, none has M_d >= M_ph inside R_test first.
- **REACHES THE WELL AT [rows]:** M_d >= M_ph inside R_test before the first fold inside q(M_tot), confirmed one resolution up. Only then do capture reads against X22 and LM1 count.
- **NO FOLD BY z = 0 AT [rows]:** reported as such, confirmed one resolution up.
- **NOT RESOLVED:** the fold time moves by more than the tolerance between resolutions, or more than 10 % of rows have no result.

**Checks, known answers, tolerances to be fixed at freezing.** Plane-wave Zel'dovich crossing time, exact. Ellipsoid S0 against a separate integration. e = 0 against AN1. Particle-grid det J against the analytic value. L1's KC solver check. Fold time against resolution. Periodic images: box size doubled on one row. A MUTATE twin. A failed check means no verdict, numbers only.

**Stop rule.** S0, then S1. S2 runs only if S1 reads anything but FOLDS NO LATER THAN SPHERICAL, or leaves low mu NOT RESOLVED. S3 runs only on REACHES THE WELL or NO FOLD. No completion in any stage.

## 5. What each result would mean
| Result | Meaning | What follows |
|---|---|---|
| Folds no later (expected) | Symmetry wasn't the cause. In this reduced class, the action needs a completion before it predicts a well | The owner decides on beta, or stops |
| Delayed, still ends | Symmetry mattered, the conclusion doesn't change | Same |
| Reaches the well | Real news: the class has a route to the law from cosmological starts. Other obstacles still stand | Verify at S3, then grade |
| Not resolved | The question needs a bigger run | The owner decides on S3 |

None of these gives a complete action.
