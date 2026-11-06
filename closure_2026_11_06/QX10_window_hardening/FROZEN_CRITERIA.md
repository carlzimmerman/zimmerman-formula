# QX10 frozen criteria: harden or kill QX7 iter_4's CMB/galaxy window

Frozen before any QX10 number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane under the owner's 11-04
rule (retired cold sectors may be reopened for tests). Name: COLD DARK ENERGY, never cold dark matter; no particle.
Shared rules: ../SWARM_BRIEF.md. Footings: canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2, never pooled.

## The object

QX7 iter_4 (criteria 22af3e7b43, result 9a8f2e4778): a cold dark energy sector with a leaf-uniform Jeans length
lambda_J(a) = lambda_* Omega_DE(a)^p (physical), lambda_* = lambda_0 / Omega_DE(0)^p, captured early and assumed today to
sit in n = 1 cores of radius lambda_J(0)/2 that ignore the host's own potential. 270 cells (lambda_0 1.47-8.25 Mpc,
p 1.125-6) passed PR4 lensing shape (G2'), forest (G4'), SPARC inner mass (G5), KiDS shift (G6) and ellipticals (G7).
Background of that grade: QX3 iter2's worst corner, omega_b 0.0215, H0 65, n_s 0.95, omega_d 0.1196 (R = 5.562).

## Cells chosen now, before any grade (rule, then values)

Rule: from QX7's committed window list (qx7_iter4.json "window"), C1 = median log lambda_0 with the median p of the whole
window, snapped to a member; C2 / C3 = the smallest / largest window lambda_0, each at the lower-middle median p of
its own members; C4 = the lambda_0 nearest 2.15 Mpc (where QX7's X-COP mean crosses zero), at the lower-middle median
p of its members. Values (all are window members):

| Cell | lambda_0 (Mpc) | p |
|---|---|---|
| C1 centre | 2.6102 | 4.25 |
| C2 low edge | 1.4678 | 3.5 |
| C3 high edge | 8.254 | 5.625 |
| C4 cluster crossing | 2.1544 | 3.75 |

Every QX10 label holds only for these four cells. No other cell is graded, and no cell is added after a number exists.

## Iterations (each has its own FROZEN_CRITERIA.md in its directory)

1. iter_1_primary_cmb: primary CMB TT/TE/EE on the framework-native background (the decisive test of the early sector).
2. iter_2_capture_dynamics: the sector's hydrostatic end state in each host's real potential (a0 law on), plus a
   time-dependent spherical collapse-and-heating run; regrade G5/G6/G7 and the cluster predictions on it.
3. iter_3_sparc_refit: the full flagship SPARC grade (QX8's pipeline, imported read-only) with each galaxy's sector
   profile from iter_2 added.

## Overall label, per cell

- HARDENED if iter_1, iter_2 and iter_3 all PASS for that cell on both footings.
- KILLED if any of them FAILS for that cell on either footing (the iteration that kills it is named).
- NO VERDICT for a cell only if a gate is uncalibrated (its known answer fails) or a MUTATE does not bite.
- The window as a whole: HARDENED if at least one cell is HARDENED, KILLED if all four are KILLED.
Clusters stay FAIL whatever happens here (QX7 iter_4, QX2, QX5, QX6); iter_2 reports the cluster predictions on the
dynamical profile, and a pass there would be reported as news, not as a label change for this lane.
