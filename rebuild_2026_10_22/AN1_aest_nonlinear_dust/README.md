# AN1_aest_nonlinear_dust: FOLDS OR NEVER COLLAPSES, NO HYDROSTATIC SETTLING. All 68 rows fold first in spherical collapse, centre first; none reaches a well before the single-valued field ends. Reduced system only

**Rerun landed: `README_V3.md`, NO VERDICT, numbers only. It also corrects the side-test table below at 1e15, mu 0.1.**

**CORRECTION, 2026-11-02, post-result. This lane's headline and fold table don't stand.** The title and tables below are kept as first published. A centre-cell error drives the early central folds: enclosed mass was interpolated linearly in r inside the central cell, which overstates the pull on the innermost baryon shell by about 4x. That shell falls early and drags the first field shell with it. The error scales with the grid, so it looks converged in N. K1 has no baryons and couldn't see it. AN2's S0 exposed it: a dust sphere of this amplitude folds at z 1.36, and the floors here read 2.93.

Rerun with mass interpolated in r^3 (`diag_centre/fix.py`, 14 canonical P1 A1 rows, N 300 and 600, strict line, side test with no frozen checks rerun):

| mu /Mpc | 1e12, z at N 300 / 600 | 1e15, z at N 300 / 600 |
|---|---|---|
| 1.24e8 | 1.361 / 1.361 | 1.360 / 1.360 |
| 2.04e4 | 1.360 / 1.360 | 1.360 / 1.360 |
| 56.6 | 1.154 / 1.157 | 1.341 / 1.341, off-centre, r about 19 kpc |
| 10 | 0.429 / 0.434 | 1.213 / 1.213, off-centre, r about 76 kpc |
| 1 | 0.008 / 0.017 | 0.392 / 0.395 |
| 0.1 | no fold by z = 0 / 0.008 | **no fold by z = 0 / no fold by z = 0** |
| 0.0156 | 0.004 / 0.008 | **no fold by z = 0 / no fold by z = 0** |

So "all 68 fold first" is wrong. The floors now match the dust sphere. At low mu, the cluster rows reach z = 0 with a defined solution, and the galaxy rows fold only at z about 0, not settled in N. Whether those rows hold the field, and how much mass is where at z = 0, isn't computed yet: the masses in this README were read at the old fold times. The full rerun goes in a new file; this one's checks and labels aren't reissued until then.

**Plain statement.** In the one-field action's slow-branch equations, a spherical peak at 1e12 or 1e15 Msun loses its single-valued solution at its centre before the disc or the cluster profile exists. It happens at every mu from the record's list, on both footings. No row settles on the hydrostatic branch, and no row reaches z = 0 with a defined solution at the frozen line. So the row "little field mass in discs, 8 x and 5 x gas in clusters" can't be read from this class's own dynamics: the solution stops first. Past that point the class needs a completion, and X14 says that costs a constant. None was run.

This is a result about a reduced system: spherical, Q0 -> infinity, quadratic K, K_B <= 0.078, one Gaussian peak, baryons stopped by hand at measured radii. A radial flow focuses on its centre by symmetry, so the central event is the part most tied to spherical symmetry. It doesn't say the action class fails in 3D. It doesn't say the class works anywhere.

Criteria `FROZEN_CRITERIA.md` (42404910c2), alone first. `AMENDMENT_A1.md` (a246fdc205) before the production rows, `AMENDMENT_A2.md` post-result. Not blind. kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired by the decision of 2026-11-01: **nothing here reinstates it.** No LCDM input in a grade. Not theory closed. Nothing here says the data favour the framework.

## Standing obstacles, not solved here
H1: for MOND-limit F, Y = 0 has a negative-energy mode, and it is the growth mode. C1, M1: planets need a screen outside F(Y, Q). X14: the caustic cure costs a new constant. BOLTZ1: mu floors 56.6, 2.04e4, 1.24e8 /Mpc. C7: K_B runaway at Q0 = 0.1 /Mpc. H2, S4: static term CANNOT for clusters. These all stand.

## What the record had, and what's new
X14 F4 had the shell equation and a crossing argument for v3s at inert K(Q). DR2 N1 had a stream in a fixed well. New here: this reduction written from C1's Lagrangian, times and masses per mu from a cosmological start, the floors, and the held-start test.

**Equations in one line.** Eliminating the aether current gives a conserved charge that sources the metric, and the system is BS24's and L1's: div[V(E)] + mu^2 h = 4 pi G rho_d, E = -grad h, field force -grad Psi + E, baryon force -grad Psi. Consequence worth stating: **the law's phantom mass is this same conserved charge.** In this limit the law holds only where the field has flowed in and is held (E = grad Psi). A freely falling field gives V near 0 at x << 1 and baryons feel plain Newton on what's enclosed. So there are two masses to read: M_d, and M_d - M_ph.

## Table: frozen rows (all FOLD FIRST, 68 of 68) and the strict-line rerun
"Frozen line" is compression 1e-2. "Strict line" is 1e-4 (post-hoc, A2). r_fold is in cells 0-2 and scales with N on the P1 rows, so it reads "the centre", not a radius.
**M_tot 1e12.** Masses are in Msun at the strict-line end, canonical: M_d / M_b / M_ph.

| mu /Mpc | pi/mu kpc | z frozen line, can / alt | z strict line, can / alt | A2 z frozen, strict (can) | P2 z (can) | K_B 0.078 z (can) | 2.2Rd | Rlast | Q0_need /Mpc |
|---|---|---|---|---|---|---|---|---|---|
| 0.0156 | 2.01e+05 | 1.47 / 1.47 | 0.46 / 0.46 | 5.03, 4.66 | 7.15 | 1.23 | 1.0e+06 / 2.3e+06 / 3.1e+08 | 9.1e+07 / 1.9e+08 / 1.3e+10 | 0.00141 |
| 0.1 | 3.14e+04 | 1.47 / 1.47 | unresolved, budget at 10.2 Gyr / unresolved, budget at 10.2 Gyr | 5.03, 4.65 | 7.15 | 1.23 | 1.0e+06 / 3.7e+06 / 3.9e+08 | 8.6e+07 / 2.8e+08 / 1.6e+10 | 5.73 |
| 1 | 3.14e+03 | 1.48 / 1.48 | unresolved, budget at 10.8 Gyr / unresolved, budget at 10.9 Gyr | 5.03, 4.31 | 7.15 | 1.23 | 1.2e+06 / 5.5e+06 / 4.7e+08 | 9.7e+07 / 3.9e+08 / 1.8e+10 | 5.69 |
| 10 | 314 | 1.74 / 1.74 | 0.68 / 0.68 | not run | 7.20 | 1.48 | 6.6e+06 / 8.6e+06 / 5.9e+08 | 5.8e+08 / 6.4e+08 / 2.3e+10 | 0.0555 |
| 56.6 | 55.5 | 2.24 / 2.24 | 1.40 / 1.40 | not run | 7.64 | 1.98 | 6.1e+07 / 1.8e+07 / 8.5e+08 | 4.5e+09 / 1.1e+09 / 3.1e+10 | 0.0246 |
| 20400 | 0.154 | 2.88 / 2.88 | 2.88 / 2.88 | not run | 8.68 | 2.64 | 2.1e+07 / 3.9e+06 / 4.0e+08 | 2.0e+09 / 3.7e+08 / 1.8e+10 | 634 |
| 1.24e+08 | 2.53e-05 | 2.93 / 2.93 | 2.93 / 2.93 | not run | 8.84 | 2.69 | 2.1e+07 / 3.9e+06 / 4.0e+08 | 2.0e+09 / 3.7e+08 / 1.8e+10 | 644 |
**M_tot 1e15.** Masses are in Msun at the strict-line end, canonical: M_d / M_b / M_ph.

| mu /Mpc | pi/mu kpc | z frozen line, can / alt | z strict line, can / alt | A2 z frozen, strict (can) | P2 z (can) | K_B 0.078 z (can) | R500 | 0.7R500 | Q0_need /Mpc |
|---|---|---|---|---|---|---|---|---|---|
| 0.0156 | 2.01e+05 | 0.71 / 1.31 | 0.25 / 0.25 | 3.55, 3.55 | 3.66 | 1.10 | 3.3e+12 / 6.1e+12 / 8.4e+13 | 1.3e+12 / 3.0e+12 / 4.1e+13 | 0.0241 |
| 0.1 | 3.14e+04 | 0.71 / 1.32 | 0.27 / 0.27 | 3.56, 3.56 | 3.66 | 1.10 | 3.6e+12 / 6.2e+12 / 8.4e+13 | 1.4e+12 / 3.0e+12 / 4.1e+13 | 0.0121 |
| 1 | 3.14e+03 | 0.88 / 0.88 | 0.71 / 0.71 | 3.81, 3.81 | 3.67 | 0.65 | 1.9e+13 / 1.1e+13 / 1.1e+14 | 7.7e+12 / 5.2e+12 / 5.3e+13 | 0.00876 |
| 10 | 314 | 1.53 / 1.53 | 1.53 / 1.53 | not run | 5.72 | 1.22 | 8.4e+13 / 1.6e+13 / 1.3e+14 | 4.3e+13 / 8.4e+12 / 6.7e+13 | 0.0121 |
| 56.6 | 55.5 | 1.63 / 1.63 | 1.63 / 1.63 | not run | 7.47 | 1.34 | 8.6e+13 / 1.6e+13 / 1.3e+14 | 4.3e+13 / 8.1e+12 / 6.6e+13 | 0.0115 |
| 20400 | 0.154 | 2.82 / 2.82 | 2.82 / 2.82 | not run | 8.22 | 2.58 | 7.5e+13 / 1.4e+13 / 1.2e+14 | 3.0e+13 / 5.6e+12 / 5.5e+13 | 609 |
| 1.24e+08 | 2.53e-05 | 2.82 / 2.82 | 2.82 / 2.82 | not run | 8.23 | 2.58 | 7.5e+13 / 1.4e+13 / 1.2e+14 | 3.0e+13 / 5.6e+12 / 5.5e+13 | 609 |


**Reading the two lines.** At mu >= 2.04e4 (and mu >= 10 at 1e15) they agree: true focus at the centre. At lower mu the frozen line fires on a centre shell that is still being held, and the strict line finds the fold later. Canonical and alt split at 1e15 mu <= 0.1 on the frozen line (z 0.71, 1.31) for this reason; on the strict line they agree. **So the frozen line's times are early at low mu; use the strict column for when the solution ends, and the frozen column only as the frozen label.** Strict z converges with N 750 to 3000 on the 7 rows tried (`an1_cf2.jsonl`), largest shift 0.05, with r_fold going to 0 with N. Four strict rows (1e12, mu 0.1 and 1, both footings) ran out of steps at 10.2-10.9 Gyr, no fold yet, stiff centre: UNRESOLVED. They are not defined-to-z = 0 results, and I can't say they would fold.

P2, more peaked: earlier, z 3.7-8.8. At 1e15 mu 0.0156-56.6 its fold sits off-centre, r 23-113 kpc (frozen line; not rerun at strict). Not grid-limited, so these are the only real fold radii in the table.

## The questions
- **(a) Settle to the n = 1 polytrope? No row.** No damping exists; only crossing could remove energy. Polytrope radius pi/mu is reached by no shell in a settled state. At the floors pi/mu is below or near the grid, and the field behaves as dust.
- **(b) Caustic first? Yes in every row that resolves.** At the centre, z 0.25-2.93 for P1 A1 on the strict line; 3.6-4.7 for A2.
- **(c) Field mass when it ends.** Inside 2.2 R_d: M_d 1e6 to 6e7 Msun, against M_ph 3e8 to 8e8. Inside R500: 3e12 to 9e13, against M_ph 8e13 to 1.3e14. Baryons on their final profile: 0 at 1e12, at most 36 % (1e15 A2). M_d stays under M_ph at all those radii at the end in P1 A1, so the law isn't yet in force, and the galaxy and cluster reads give **ENDS AT z_f, BEFORE THE WELL EXISTS**. No row earns a comparison against A8, D4, X22, or LM1's 8 x and 5 x. The numbers are states at z_f and are not a capture measure.

Worth noting: low mu doesn't stop collapse in A1. Baryons pull the field, and the fold comes later but before z = 0.

## Held start: if the field were already there (reported; A2 line on start)
Static branch built from H2's system, kicked with smooth velocity. Start F/g at most 5e-6, under the 1e-3 line.

| Mass, mu | Kick 1 % | Kick 10 % |
|---|---|---|
| 1e12, 0.1 | holds 14 Gyr, both footings; least compression 0.55, 0.53 (N 1200), 0.53 (N 2400) | inner fold at 2.8 Gyr |
| 1e15, 0.1 | holds 14 Gyr, both; 0.88 | outer wall cell closes at 3.2 Gyr, no inner fold |
| 1e12, 1 | outer wall cell closes at 6-8.5 Gyr, changes with N: **wall artefact, UNRESOLVED** | same, 2.6 Gyr |
| 1e15, 1 | outer wall cell closes at 0.13-0.16 Gyr: **wall artefact, UNRESOLVED** | same |

So the hydrostatic branch at mu 0.1 isn't quickly destroyed by a small radial kick, and a 10 % one in a galaxy does fold it. Formation isn't that gentle: A1 rows never get there. This tests radial modes only, and doesn't touch H1's ghost statement.

## Checks: all frozen checks pass after A1
| Id | Result | Line |
|---|---|---|
| K0 static form + kernel, sympy | residual 0 | 0 |
| K1 Oppenheimer-Snyder | 4.7e-4 | 3e-3 |
| K2 r_ta slope | 0.8898 (8/9 = 0.8889) | 0.01 |
| K3 polytrope | F/g 1.0e-5; drift 5.5e-7 | 5e-3; 0.02 |
| K4 static law, E | 2.0e-10 / 1.9e-10 | 2e-3 |
| K5 energy, hold, mass | 1.6e-5; 4e-16; 0 | 3e-3; 1e-8; 1e-13 |
| K6 linear kernel growth | 1.1 % | 5 % |
| K7 convergence, frozen line | largest t shift 0.75 % (1e15, mu 56.6); eta 0; all r_fold grid-limited, so the factor line doesn't apply | 3 %; 1.5 |
| K8 SIGTERM resume | 0 | 1e-10 |
| K9 MUTATE | K3, K5, K6 fail | must fail K3 or K4 |

Newton warnings 0 of 68 rows on the frozen line. Max RSS for the checks 0.11 GB; the whole lane about an hour single thread at nice 15, under 1 MB of output.

## Departures and first-run failures, all of them
- **First checks failed** at frozen eta 0.1: K1 -0.024, K2 slope 1.53, K3, K5, K6 (`an1_checks_RUN1.json`). Fixed by A1 (eta 0.005 and code), before production. Tolerances unchanged.
- **Bugs found before production:** baryon stop true at rf = infinity; shells stopping at once at z 20; baryons on field nodes, giving a false fold at about z 3.7. About 20 development rows were seen on faulty code before A1, disclosed there.
- **Hand expectation missed twice.** I expected NO COLLAPSE at low mu in A1: all fold. I expected held-start phase-mix folding at 1 %: at mu 0.1 it holds 14 Gyr. Also `grid-limited` is true at nearly every P1 row, which I didn't plan for.
- **Frozen line's weakness** (A2): it isn't a crossing test at low mu, found only by the post-hoc rerun. K7's list missed those rows. The label doesn't change, and the times do.
- **Frozen arithmetic slip:** section 2 said Q0 = 0.1 would be outside the limit, from an error of 1000 by hand. Computed Q0_need over the frozen rows is 0.011 to 4 /Mpc, set by where g/V_c peaks at that moment, and up to 640 in the strict rows at the floors, from the smallest cells. For a settled galaxy at a0, V 200, it's about 0.05 /Mpc. So Q0 = 0.1 is marginal, not excluded, and rows above that aren't described at Q0 = 0.1.
- **Held-start first run void** for galaxies (code fault, A2), `an1_held_RUN1.*`. Line on start set post-hoc.
- **R500** frozen at 1.35 Mpc; median of all 12 X-COP systems on disk is 1.24. Kept.
- **mu 0.0156 rows:** h_bar(z_i)/c^2 = 0.76: QUADRATIC K LAPSES AT START on every mu 0.0156 row. Reported, not trusted beyond that. mu 0.1 is 0.019.
- **Generous start:** field growth before z 20 not charged. Background constant Lambda, not the CPL form. Same h on both footings. a0 constant, as in the action. Web: none used; action through C1's transcription, which C1 says wasn't verified on disk.

## Not run
Finite Q0 and the fast modes. Non-quadratic K (Cosh, Exp). Published K_B 0.1, 0.5. 3D, angular momentum, or asphericity. Any completion, or anything past the first fold. Baryon pressure or feedback. Strict line on the P2 and K_B rows. Grading against SPARC or X-COP data: nothing reached a state to grade.

## Files
`an1.py` (`checks`, `rows`, `conv`, `held`, `--mutate`), `an1_rows.jsonl`, `an1_conv.jsonl`, `an1_held.jsonl`, `an1_held2.py/.jsonl`, `an1_cf.py`, `an1_cf1e-4.jsonl`, `an1_cf2.py/.jsonl`, `an1_checks*.json`, `an1_tab.py`.
