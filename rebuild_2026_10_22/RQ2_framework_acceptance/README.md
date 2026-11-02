# RQ2_framework_acceptance: the list is now 93 rows, 39 of them computable from a candidate's g. The a0 law reads REJECTED on both footings: 17 pass, 20 fail, 2 depend on the vertical form, canonical; 16, 21, 2 alt, the extra fail being Upsilon's line

Criteria `FROZEN_CRITERIA.md` (42241594b2), committed alone first. List `REQUIREMENTS_V2.md`, tolerances `tolerances.json` (c2b0a76630 and one correction, both before any run). Harness `acceptance.py`; results `results/`. **Not blind.** Grades nothing new, adopts no framework. kappa = 1/2 FITTED. Footings never pooled. The cold sector stays retired, and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## What the list says now
A framework has to keep discs tight and flat with surface brightness, meet measured stellar masses and a step no offset fixes, fit dwarfs and IC 1613, clear both weighings with one vertical form, fill the cluster deficit with the right shape (15 keys, X-COP, deficit map), put that mass on the galaxies in the Bullet, leave planets alone, pass PPN and tensor speed, and supply UX2's matter term: omega_x 0.1197, dust by z >= 3e4, without contracting in spirals. And do it from one action that is healthy. New against 11-01's twelve rows: total errors, the Bullet, planets, stellar-mass rows, HSC against KiDS as open data, UX2's numbers, the older frozen list folded in, and LCDM yardsticks from that list dropped by name.

## How many rows run
| | canonical | alt |
|---|---|---|
| Rows | 93 | 93 |
| Computed from g for the law | 39 | 39 |
| NOT COMPUTABLE | 44 | 44 |
| READ, from the record, never a pass | 9 | 9 |
| OPEN DATA, HSC against KiDS | 1 | 1 |

**A11, and form A inside A15 and A16, are reachable only because the candidate is numerically the law:** they read LW1's solves. A new g gets A13, algebraic, in A11's place, and form R only on the Milky Way. Most NOT COMPUTABLE rows need an action or a Boltzmann run, which a static g can't supply. About 12 are older gates simply not wired (A20-A29, B2, B3). Action, health, CMB, PPN, tensor speed: all out of reach of this harness.

## How the law scores
Labels are per row; the full table is `results/law.out`.

| Row | canonical | alt | Old line, on the law |
|---|---|---|---|
| A1 rms | PASS 0.0541 | PASS 0.0537 | same |
| A2 Upsilon | PASS 0.52 | **FAIL** 0.44 | same |
| A3 tilt, A4 surface brightness | PASS Z +0.20, -0.25 | PASS -0.28, -0.36 | same |
| A5 GSWLC, worst bin | **FAIL** +5.55; bins +3.38, +5.55, +1.66, +1.55, +1.90 | **FAIL** +4.63 | same |
| A6 Taylor; A7 step | **FAIL** +7.57; -2.99 | **FAIL** +6.56; -3.06 | same |
| A9 LITTLE THINGS | PASS -0.30 | PASS -0.77 | same |
| A10 IC 1613 | **FAIL** -3.94 | **FAIL** -4.20 | FAIL -7.90, -8.42 |
| A11 dwarfs, E1 | **FAIL** UFD +6.62, others +2.71; bright +1.63 | **FAIL** +6.46, +2.55; +1.51 | FAIL, bright +3.97, +3.66 |
| A12 no field; A13 algebraic | **FAIL** +4.93; +7.78 | **FAIL** +4.61; +7.64 | same |
| A15, A16 Milky Way | FORM-DEPENDENT; R K 70.1, Z +0.92; A K 79.6, Z +3.31 | FORM-DEPENDENT; 69.8, +0.84; 79.2, +3.21 | same, on LW1's labels |
| A18 DiskMass, D | PASS, R -0.13 (r 1.239) | PASS, R -0.38 (r 1.204) | **FAIL** r 0.90-1.10 |
| A30 lensing, absolute | **FAIL** +9.27 | **FAIL** +6.52 | PASS on CL2's rule |
| B1 groups | PASS -0.31 | PASS +0.31 | same |
| B4-B18 keys | **10 of 15**; MID-T3 +4.86, OUT-M3 +4.76 | **10 of 15**; +4.54, +3.99 | same |
| B19 M3 Z_tot; B20 joint | **FAIL** +3.80; p 3.4e-8 | **FAIL** +3.08; p 1.0e-6 | none; same |
| B23, B24 X-COP | **FAIL** +3.86; rms 0.476 | **FAIL** +3.59; 0.444 | FAIL |
| B25 deficit map | **FAIL** -3.04 to -2.17 | **FAIL** -2.86 | none |
| B28 Bullet | **FAIL** M300 -4.55, -4.54 | **FAIL** -4.39 | FAIL (UX6) |
| C1 planets | **FAIL** 1.1e4 to 6.7e4 x | **FAIL** 1.3e4 to 8.1e4 x | same |

Block summary, not a p to quote: chi^2 286.7/12 canonical, 219.3/12 alt. Mocks, canonical: planted REJECTED, 29 fail; label REJECTED, tagged; NaN 0 PASS, 0 FAIL, overall NOT REJECTED ON 0 OF 93, by the frozen wording.

**Reading the two line sets side by side:**
- **Flips on total error, none earned by physics.** DiskMass FAIL to PASS, because c 1.0-1.517 is unsettled and I made the error wide on purpose: PASS there means the data can't decide (OD1). Bright M31 class goes under 2 (+3.97 to about +1.6), which rests on UX4's unmeasured orbit, and the row still fails on ultra-faints.
- **Flip the other way.** Lensing: old rule PASS, against retired halos and zero by construction on its first term. Absolute chi^2 154.1/56 canonical, 125.0/56 alt: FAIL, Z +9.27, +6.52. The covariance holds no inventory term, so that Z is overstated and it isn't a new discovery; the record already said no tested model fits in absolute terms.
- **Stays failed but narrower.** IC 1613 -7.90 to -3.94; X-COP +0.467 at Z +3.86 with the 0.12 dex used two-sided.
- **Milky Way:** form R passes (1 and 6 in-prior cells), form A INFEASIBLE, so FORM-DEPENDENT, as LW1. Form R has no field equation behind it and misses the K_z scale length, a row not wired here (A17).

## Known answers: 39 of 39
Law against LW1, FG1, CRG1, UX6, M1: SPARC, tilt, LITTLE THINGS, HS1, IC 1613, dwarfs plain, E1, E2, DiskMass both forms, Milky Way class and counts, X-COP, groups, lens chi^2 (154.1486, CRG1), planets, all 15 key Z to 1e-6, failing set, joint chi^2, Z_tot, Bullet M300. Mocks: planted fails A9, NaN reads no PASS and no FAIL, label mock tagged [LABEL]. **MUTATE, a0 x 1.5 labelled the law: 6 of 39, exit 1.** Rerun byte-identical, all `results/`, keys from cache on the rerun.

## Failures, departures, things to read as hard as a pass
- **Checks are weaker than they look in places.** Tolerances in `known()` were written by me after the criteria: rms 1e-3, Upsilon 6e-3, tilt 0.01, HS1 2e-3, planets only an order of magnitude (it allows up to 1.2e5, and doesn't compare to M1's number though the printed ratios match). The criteria asked for 1e-3 on S, Tl, LT, G; tilt and groups are looser (0.01, because FG1 rounds). Six of the 39 survive MUTATE, so those don't test a0: the five mock checks, and canonical planets, whose loose tolerance a0 x 1.5 slips under (alt's just misses it).
- **Frozen clause not enforced.** "Pass nothing it shouldn't": the planted mock turns law FAILs into PASS on B6, B19 canonical and B6, B7 alt. It lifts g below a0/10 and those are cluster outskirt keys, so I read that as the g change, but the harness prints this and doesn't fail on it. A candidate can win keys this way while failing elsewhere; the whole-row line is what catches it.
- **FORM-DEPENDENT isn't a label in my criteria.** Added in code, for LW1's case; it isn't a PASS and blocks ACCEPTED. The law's A18 carries forms R and A, and with c that wide both read PASS.
- **First two runs had bugs:** keys path wrong (HERE), DiskMass dictionary copy, then a KeyError in a printed message. Both surfaced as failed known answers and NOT COMPUTABLE, not as passes. Fixed before the committed results.
- **V2 says form A K 83.5, harness prints 79.6.** Different selection: V2 quotes UX5's lowest K with v_c in line, in priors; the harness takes the best cell by D. Same side of the line.
- **B19 at f* 0.0615 omits the gas term** (no +0 run there), so Z_tot there reads slightly above LW1's. **Keys' error is stat-only** except M3, since no budget exists. So the key rows are harsher than total error and I can't fix that from committed files. The Bullet's sigma is PROVISIONAL, which rule 2 says can't set a line alone: row marked, UX6's FAIL rule decides it independently.
- **Sign in B1:** Z = model minus data, opposite to FG1's print.
- **Joint block chi^2 selects upward** (worst row per block) and treats correlated blocks as independent. A summary only. UX3's k fit on X-COP shows those blocks aren't independent.
- **Row count isn't a score.** Rows differ in weight, and 15 are one correlated key table.
- **Not checked on a real non-law g.** Only mocks. BK2 and AS2, and any gas-reading g, will be the first test of the gas path; groups, LITTLE THINGS and the Milky Way give NaN gas and so NOT COMPUTABLE by design, which may annoy a gas-tied candidate. UX3's gas term was not run through here as a check, since this grades nothing new.

## Use
`python3 acceptance.py candidates/x.py`: module with `NAME`, `g(Q)`, optional `VERTICAL`, `COSMO`. Q holds gb, gg, gs, r, a0, sample, and S and r500 where they exist, SI. Keys take about a minute per cell, Bullet several minutes under load. `--known` for known answers, `RQ2_MUTATE=1` for the twin. nice 19, one thread, no writes outside this directory.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
