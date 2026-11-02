# AN1 AMENDMENT A3: centre-cell bug, its fix, a second fault, new checks. POST-RESULT, NOT BLIND

Committed alone, before `an1_v3.py`'s checks and before any production number. Labels of FROZEN_CRITERIA sections 5 and 6, mu list, rows, frozen check lines: unchanged. First-published files stay as the record; v3 writes only `an1_v3_*`.

**Not blind.** The first publication, its correction and the 14-row side test (`diag_centre/`) were read. The expected reading of the low-mu rows is known. Also seen while writing this file, all canonical P1 A1: 1e12 at mu 0.1, N 300 to 2400; 1e12 at mu 1, 10, 56.6, N 600 and 1200; 1e15 at mu 0.1, 1, 10, N 600, fold times and first-shell traces only. They are rows of that side test, at more N. Scripts in `diag_v3/`.

## 1. The bug
Enclosed baryon mass was interpolated linearly in r (`Run.Mb`), and enclosed field mass at baryon shells likewise (the `gb` term). Inside the central cell this overstates the pull on the innermost baryon shell about 4x: 1/2 of its mass against the true 1/8. It falls early and drags the first field shell. Self-similar, so converged-looking in N. K1 has no baryons.

## 2. Fix, after checking `diag_centre/fix.py`
Mass interpolated in r^3, each baryon shell carrying the mass inside its mid-q surface. On a uniform peak this is exact at every node (hand check: q = dq gives exactly dq^3 of density). Accepted. It was incomplete:
- `Run.Mb` itself stayed linear, so `diag`'s M_b reads did; its field read `np.interp(X, r, m)` is linear too. Both now r^3.
- It broke `Mb_fn` and `Mseed` runs (held start, K2). `Mb` is now one method handling all three.
- It wasn't run with the checks. Now run below.

## 3. Other faults looked for
| What | Found | Action |
|---|---|---|
| **Wall overshoot, new fault.** At low mu E is singular at r_w = sqrt(G m/a0). A drift just past r_w meets a huge E and the kick injects energy. Traced on 1e12, mu 0.1, N 600: first shell at v = +1361 km/s after falling in at about 13 km/s, then striking shell 2 at r 1.27 kpc | The fold at r about 1.27 kpc, z 0.008, and its radius's N-dependence were **this artefact**. With the fix below the same row folds at r 0.20 kpc, z 0.0045, and 0.044 kpc, z 0.0086 (N 1200), 0.040 kpc, z 0.0106 (N 2400). The time is settling and the radius going to the centre: a central focus just before z = 0 | Step rejection: a KDK step whose trapezoid work error 0.5 abs(F_new - F_old) abs(dr) on any field shell exceeds 1e-3 of v^2/2 + g r is undone and retried at half dt. A numeric tolerance, no physics. Tested at 1/4 of it on rows in section 6 |
| Stop radii | r_f was set from the mass at the shell's outer edge, while the shell sits at mid-q. Same kind of error, half a shell; self-similar at the centre | r_f from the mass inside mid-q |
| Stop rule | Code moved a shell that turned around below r_f up to r_f, against A1 item 7's text and its own comment | Stops where it turned, as A1's text. The count and mass are written per row. None occurred on the rows traced, so it changes nothing there |
| Fold reader | Tested only the smallest cell; a closing cell above an opening smaller one was missed | Any closing cell under the line; smallest such |
| Hold geometry at the centre | None. r_1^2 V(E_1) + mu^2 u_0 dV_0 = G dm_0 is exact flux; node spacing enters only through u's differences, and K3 tests it. At low mu E_1 follows from charge alone | No change |
| Field enclosed mass at field nodes | None: nodes are mass surfaces | No change |
| Q0_need | Set by the innermost cell | Frozen read kept; a read outside 1 kpc added |

## 4. The fold line
**The strict line 1e-4 is now primary, for rows, K1, K7 and the held start.** Lesson of the first run (A2): 1e-2 fires on held shells. The frozen line's z is still recorded per row. No completion, as frozen.

## 5. New checks, lines set here before they are run
A miss in any of them, or in a frozen check, means NO VERDICT, numbers only.
- **K10.** Uniform-core peak, d0 = 0.2030, field and baryons on the same q, mu 1.24e8, canonical, compensated by nothing outside (K1's form), both masses, N 300 and 1200, each with production stop radii and with baryons never stopped. Strict-line fold time against an independent dust sphere: quadrature of the energy integral, cross-checked by an ODE to 1e-6 and against S0's z 1.361 (`../AN2_aest_3d_fold/README.md`). **Line: abs(t - t_exact)/t <= 2e-3**, about 0.003 in z.
- **K11.** On K10's peak and on the P1 floor rows, both masses, N 300 and 1200: **abs(r_1 k / r_k - 1) <= 0.02, k = 2, 3, 5**, at every step until the central cell reaches 1e-3 of its comoving size. No single-shell runaway before the true focus. The value is also written per production row at its end.
- **K12 (added for the fault above; not asked for by the brief).** Field only, mu 0.1 /Mpc, first shell comes in at 100 km/s, N 300 and 1200: energy after reflection off r_w against the closed potential, K5's line 3e-3. Its form was developed on a trial before this file: fixed 100.02 km/s out, unfixed 6822 km/s. Disclosed.
- **MUTATE.** `--mutate-linear` restores the linear interpolation and old stop radii: **must fail K10.** `--mutate-step` removes rejection: must fail K12. `--mutate`, frozen K9, stays.

## 6. Verification, frozen before the rows
- Frozen K7's rows at the strict line.
- **Every row that doesn't fold, and every fold row at z < 0.05:** N 3000, eta 0.0025, outer boundary at 3 q_t at unchanged dq, rejection tolerance 2.5e-4. No claim rests on one setting. A row whose status changes in any of these is reported as **not settled numerically**, not as its N 1500 label. SETTLED repeats at N 3000, as frozen.
- END rows carry one of SETTLED, NO COLLAPSE, OSCILLATING by frozen section 5.
- Held start: outer 5 % of cells read apart from the inner fold, R_out doubled on each canonical row, so a wall artefact shows.

## 7. Reads required
At z = 0, for rows that reach it: M_d, M_b, M_ph, M_d - M_ph at 2.2 R_d, R_last, 0.3, 0.7, 1.0 R500. Against the frozen needs of section 6: X22 capture, A8, D4 (`../RQ3_acceptance_v2/REQUIREMENTS_V2.md`), X-COP windows, LM1's 8 x and 5 x gas. Those comparisons count only for a row defined to z = 0, as frozen. **A row with fold after z = 0 at N 1500 and before it at N 3000 is not defined to z = 0.** Rows flagged QUADRATIC K LAPSES (mu 0.0156, h_bar/c^2 0.76) can't carry a positive claim alone. Q0_need per row. Any win is stated beside H1's ghost and growth statement: this start doesn't charge suppressed growth before z_i, frozen as generous.

## 8. Other departures
- Budget 4e5 steps or 20 min per row, counted in CPU seconds, because the machine is shared under load.
- Domain parameter added for section 6 only.
- `R500`, background, start: as frozen.

kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired: nothing here reinstates it. No LCDM input. Not theory closed. Nothing here says the data favour the framework.
