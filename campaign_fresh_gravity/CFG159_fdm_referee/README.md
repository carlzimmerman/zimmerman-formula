# CFG159 -- independent re-derivation of CFG119's G1 headline (door 7: Schroedinger-Poisson soliton + baryons vs the CFG44 target)

Referee lane. Criteria frozen and committed before any script (`CFG159_FROZEN_CRITERIA.md`, 94605d68c). Nothing in the repo was edited by this lane. kappa = 1/2 is FITTED. A scoped no-go is a valid result; nothing here says the data favour either model or that the theory is closed.

## Bottom line

**CFG119's G1 headline reproduces, with an independent solver, to 1.4e-7 (canonical) and 1.7e-6 (alt) relative in every rule-(ii) J.** All 64 rule-(ii) cells (32 per footing) fail the +-0.04 dex line; the closest is exp sphere, 1e9 Msun, m = 1e-23 eV at J = 4.261 dex (canonical) and 3.998 dex (alt); the best single m is 1e-23 eV and its worst galaxy (point mass, 1e12 Msun) misses by 1.177e5 dex (canonical), 1.07e5 (alt). The failure is in the core and the envelope. The G2 line (growth within 5% to 30/Mpc needs m >= 1.28e-20 eV) reproduces as a formula check (shared fit, not independent).
Scope: rule (ii) only (rule (i) cannot be better than (ii)); ground state only; spherical, static, Newtonian; the excited-state envelope, granules, self-interactions, m off the grid and feedback are untested here as in CFG119.
Two of my own frozen lines failed on definitions I got wrong (P7a core threshold; P8a "half-amplitude" label) and one on README rounding (P8b); all three are kept as failures and classified below. No physics disagreement was found.

## What was done (files, all in this directory)

| file | role |
|---|---|
| `CFG159_core.py` | own solver: radial equation for u = r psi on a log grid, log-derivative (Riccati) propagation with the potential piecewise constant per step (exact hyperbolic/trigonometric propagator, evaluated in log space so ln u down to about -1e11 is an exponent, never a float), outward from r0 and inward from r_far, matched at the classical turning point; E from a bracketed root of the bounded mismatch (w_out - w_in)/(abs sum), a node (sign change of u) meaning E is above the ground state; self-consistent loop with Anderson mixing. Sweeps in C (compiled at first use with the system `cc`, source embedded in the file). |
| `CFG159_sp_riccati.py` | 32 cells x 2 footings: rule-(ii) scan over log10(M_sol/M_b) in [-16, 4] (0.5 dex, then golden section to 1e-3 dex), the J table, frozen lines P1-P7, controls S1-S4, MUTATE A-E |
| `CFG159_g2_hbg.py` | G2 formula check (P8), MUTATE=1 changes the fit's denominator exponent 8 -> 6 |
| `CFG159_compare.py` | phase 2 only: row-by-row comparison with CFG119's results JSON (read after my own runs were saved) |
| `run_all.sh` | runs everything, writes `exit_codes.txt` |
| `*.out`, `*_results.json`, `run_*.console.txt`, `exit_codes.txt` | outputs (mode-keyed) |

**Re-run:** `./run_all.sh` (about 10 minutes wall on 16 cores; main 39 s, MUTATE C 166 s, D 354 s, others < 40 s), then
`CFG119_JSON=<path to CFG119_fdm_soliton_results.json> python3 CFG159_compare.py`.
Exit codes recorded in `exit_codes.txt`: main 1 (P7a, and the G2 script's P8a/P8b, failed as frozen), MUTATE A, B, C, D, E all 1 (the control bites), G2 main 1, G2 MUTATE 1.

## Table versus CFG119 (rule (ii), canonical footing; J in dex)

The README column carries the README's rounding (2 significant figures for most entries; up to 2.0% from rounding). The CFG119 JSON column is the committed `R1` rule-(ii) entry.

| cell | m (eV) | CFG159 J | CFG119 JSON J | README J | CFG159/README - 1 |
|---|---|---|---|---|---|
| point 1e9 | 1e-23 | 4.888 | 4.888 | 4.89 | -0.0% |
| point 1e9 | 1e-22 | 369.7 | 369.7 | 370 | -0.1% |
| point 1e9 | 1e-21 | 3.72e4 | 3.72e4 | 3.7e4 | +0.5% |
| point 1e9 | 1e-20 | 3.721e6 | 3.721e6 | 3.7e6 | +0.6% |
| point 1e10 | 1e-23 | 116.3 | 116.3 | 116 | +0.2% |
| point 1e10 | 1e-22 | 1.176e4 | 1.176e4 | 1.2e4 | -2.0% |
| point 1e10 | 1e-21 | 1.177e6 | 1.177e6 | 1.2e6 | -1.9% |
| point 1e10 | 1e-20 | 1.177e8 | 1.177e8 | 1.2e8 | -1.9% |
| point 1e11 | 1e-23 | 3716 | 3716 | 3.7e3 | +0.4% |
| point 1e11 | 1e-22 | 3.721e5 | 3.721e5 | 3.7e5 | +0.6% |
| point 1e11 | 1e-21 | 3.721e7 | 3.721e7 | 3.7e7 | +0.6% |
| point 1e11 | 1e-20 | 3.721e9 | 3.721e9 | 3.7e9 | +0.6% |
| point 1e12 | 1e-23 | 1.177e5 | 1.177e5 | 1.18e5 | -0.3% |
| point 1e12 | 1e-22 | 1.177e7 | 1.177e7 | 1.2e7 | -1.9% |
| point 1e12 | 1e-21 | 1.177e9 | 1.177e9 | 1.2e9 | -1.9% |
| point 1e12 | 1e-20 | 1.177e11 | 1.177e11 | 1.2e11 | -1.9% |
| exp 1e9 (h = 2) | 1e-23 | 4.261 | 4.261 | 4.26 | +0.0% |
| exp 1e9 | 1e-22 | 56.07 | 56.07 | 56.1 | -0.1% |
| exp 1e9 | 1e-21 | 605.2 | 605.2 | 605 | +0.0% |
| exp 1e9 | 1e-20 | 6112 | 6112 | 6.1e3 | +0.2% |
| exp 1e10 (h = 3) | 1e-23 | 43.78 | 43.78 | 43.8 | -0.0% |
| exp 1e10 | 1e-22 | 538.6 | 538.6 | 539 | -0.1% |
| exp 1e10 | 1e-21 | 5529 | 5529 | 5.5e3 | +0.5% |
| exp 1e10 | 1e-20 | 5.545e4 | 5.545e4 | 5.5e4 | +0.8% |
| exp 1e11 (h = 4) | 1e-23 | 474.0 | 474.0 | 474 | +0.0% |
| exp 1e11 | 1e-22 | 5075 | 5075 | 5.1e3 | -0.5% |
| exp 1e11 | 1e-21 | 5.115e4 | 5.115e4 | 5.1e4 | +0.3% |
| exp 1e11 | 1e-20 | 5.119e5 | 5.119e5 | 5.1e5 | +0.4% |
| exp 1e12 (h = 5) | 1e-23 | 4623 | 4623 | 4.6e3 | +0.5% |
| exp 1e12 | 1e-22 | 4.72e4 | 4.72e4 | 4.7e4 | +0.4% |
| exp 1e12 | 1e-21 | 4.731e5 | 4.731e5 | 4.7e5 | +0.7% |
| exp 1e12 | 1e-20 | 4.732e6 | 4.732e6 | 4.7e6 | +0.7% |

All 32 alt-footing J values also agree with CFG119's JSON to 1.7e-6 relative (`CFG159_compare.out`). The alt/canonical ratio is 0.910 in the 28 tail-dominated cells (range [0.893, 0.910]) and 0.94 at the closest cell (README: "6-11% smaller").

Other rows compared with CFG119's JSON (`CFG159_compare.out`):
- log10 ratio at x = 0.1 and x = 30: relative differences <= 3e-4 and <= 1.7e-6. Closest cell, canonical: -3.5721 / -2.5785 / -4.2606 (mine) against -3.5722 / -2.5786 / -4.2606 (CFG119); README -3.57 / -2.58 / -4.26. x = 30 is the argmax in 32/32 cells on each footing, both codes.
- density log-slope at x = 30: [-9.14, -2.71e11] (mine) against [-9.15, -2.71e11] (CFG119), README -9 to -3e11.
- flat cores: cells with density slope at x = 0.1 above -0.075: 8 rule-(ii) cells in mine, the identical 8 in CFG119's R1 (16 over both rules, range -0.0735 to -0.0005, m <= 1e-22, M_b <= 1e10: the README's "16 of 128" claim reproduces from its JSON).
- point-mass cells with a_B inside the Schwarzschild radius: 6 of 16 (a_B/r_s = 0.89 to 9e-5), as README.
- `optimum M_sol/M_b` agrees to <= 0.05 dex in 62 of 64 cells; the two outliers are exp 1e12, m = 1e-20 on each footing (7.6e-10 mine; 1.06e-9 canonical and 1.16e-9 alt in CFG119): the optimum is flat there (J agrees to 1e-7 canonical, 1.7e-6 alt).

## Frozen lines (verdicts)

| line | verdict | numbers |
|---|---|---|
| P1 closest cell and J | PASS | argmin = exp 1e9 (h = 2), m = 1e-23 on both footings; J = 4.2606 (canonical), 3.9982 (alt) |
| P2 all J >= 3 dex, none in the band | PASS | minimum J 4.261 / 3.998; 0 cells within 0.0458 dex; no undefined cell |
| P3 best single m | PASS | 1e-23 eV on both footings; worst galaxy point 1e12: 1.1766e5 (within 0.3% of 1.18e5), alt 1.0703e5, alt/canonical 0.910 |
| P4 32-cell table | PASS | 32/32 within max(0.3 dex, 2%) (worst deviation 1.97%, a README rounding: 1.176e4 against 1.2e4); P4b alt/canonical in [0.8932, 0.9097] |
| P5 R1 at the closest cell | PASS | -3.572 / -2.578 / -4.261 |
| P6 M_sol/M_b at the closest cell | PASS | 0.6387 canonical, 0.7567 alt |
| P7a core | **FAIL** | 15 "core" cells under my frozen rho(0.1 r_M)/rho(0) >= 0.5; slopes reach -1.19 and some cells have m or M_b outside the frozen limits |
| P7b envelope | PASS | shallowest -9.14, steepest -2.71e11 |
| P7c both ends fail; argmax at x = 30 | PASS | 64/64 and 64/64 |
| P7d target slope (own ODE of the CFG44 target) | PASS | point -1.0099; exp spheres -0.551, -0.621, -0.788, -0.965 (README -0.55 to -1) |
| P8 G2 | **P8a FAIL, P8b FAIL (first entry)**, m_min PASS, T_F(30, 1e-20) PASS | m_min = 1.2767e-20 eV; T_F = 0.8973 (10.3% low) |
| solver controls S1-S4 | PASS | S1 hydrogen: E relative error 5.2e-9, ln psi 2.6e-9; S2 pure soliton E = -0.162769, r_c = 2.67941 a_B(M_sol); S3 virial 3e-8 or better on five point-mass SP states; S4 dt halving: dE/E <= 6.2e-8, dJ/J <= 3.6e-8 |

## Disagreements, classified

There is no solver disagreement and no physics disagreement. The three failed lines are:
1. **P7a (definition):** my frozen "core" threshold (rho(0.1 r_M) >= 0.5 rho(0)) is looser than the README's usage and it also imposed m and M_b limits that a looser core set violates. On the README's own quantity (slope at 0.1 above -0.075) the set reproduces (8 rule-(ii) cells, identical to CFG119's, slopes -0.0286 to -0.0004; 16 over both rules). I report this post hoc row in the script output and do not re-score P7a.
2. **P8a (definition):** my frozen file called the README's k_1/2 a T = 1/2 amplitude scale. It is HBG's closed form 4.5 m22^(4/9) (1.617, 4.500, 12.52, 34.84 /Mpc), which is what CFG119's JSON stores. The T_F^2 = 1/2 crossing of the fit itself is 1.647, 4.584, 12.756, 35.494 (+3.0%, +1.9%, +2.0%, +2.0% against the README numbers); the T_F = 1/2 crossing is 1.825, 5.078, 14.13, 39.32. Neither was my frozen line.
3. **P8b (README rounding):** the first entry, k at which T_F = 0.95 for m = 1e-23, is 1.249 /Mpc; CFG119's JSON has 1.2492; the README prints 1.2. The other three (3.476, 9.672, 26.914) agree with the README to 1%.
4. **M_sol 0.76 against 0.64 in the README (resolved: labelling, not a typo):** both are correct at their footings. The closest cell's optimum is M_sol/M_b = 0.6387 canonical and 0.7567 alt (CFG119's JSON: 0.6386 and 0.7566). The README's bottom line says "(alt footing; 4.3 dex canonical)" and quotes 0.76, i.e. the alt value, while R1 is on the canonical footing and quotes 0.64. The README states the footing for one of the two but not next to the number.
5. **README 2-significant-figure rounding** explains every deviation of a table entry from mine (up to 2.0%, a table rounding of 1.2e4 for 1.176e4).

## Controls, including the ones that do not bite everything

Main mode: exit 1 (P7a). Each MUTATE mode exits 1 when it bites.
- **A (evaluator on the target's own rho_c, re-derived from the CFG44 definition by my own ODE):** J = 6e-11 dex or less in every cell on both footings, so P1, P2, P3, P4, P4b flip; bites.
- **B (C_target := C_SP):** J = 0 exactly in every cell; bites. Tautological by construction; it only bounds the bookkeeping.
- **C (baryons removed from the Schroedinger potential; the target, r_M and g_tot unchanged; restricted to m in {1e-23, 1e-22} to save time):** the closest cell moves from 4.261 to 3.248 dex (alt 3.188), the optimum M_sol/M_b from 0.64 to 2.4, the best-m worst galaxy from 1.18e5 to 7.97 dex. So the baryon potential is load-bearing for the value 4.26, but without it the state still misses by more than 3 dex. Bites on P1, P3, P5, P6. (My prior: moves by > 0.3 dex, 0.85: right.) Its P4/P4b/P7 failures partly reflect the reduced cell set and are not counted as physical bites.
- **D (baryon potential sign-flipped, repulsive baryons with attractive self-gravity; m in {1e-23, 1e-22}):** the closest cell moves to 3.067 (alt 3.003) and the worst-galaxy J at m = 1e-23 falls from 1.18e5 to 1.8e4; bites on P1, P3, P5, P6. Small-s states with no bound state are recorded as undefined and skipped.
- **E (Poisson source x 1.05; the solver controls and the m = 1e-23 cells):** bites through the solver control S2 only (E = -0.17945, r_c = 2.5518, against -0.16277, 2.6794: the values in CFG119's referee note). The headline is robust to this 5% change: closest cell 4.282 (canonical), 4.019 (alt), so P1, P5, P6 still pass. The P4/P7 failures in this mode are artefacts of the m = 1e-23 subset and are not counted.
- **G2 MUTATE (fit denominator x^6):** m_min moves from 1.28e-20 to 1.55e-20; bites.

## Shared and not independent

Same target definition (CFG44 exponential sphere formula, r_M = sqrt(G M_b/a0), G, a0, the two footings), same cell grid (masses, h pairing, m list), same rule-(ii) definition and search range, and the same HBG fit for G2 (G2 is a formula check only). CFG119's `ratio_curve` computes the same quantity as my `evaluate` (rho_psi r^3 G(M_b + M_psi)/r^2 over (a0/4pi) M_b); I read it in phase 2, after my runs, and made no change. Both codes also evaluate deep tails as exponents from piecewise-constant potential steps, which is a shared idea; the eigenvalue method (matched Riccati log-derivative propagation in my case, finite-difference inverse iteration in theirs), the mixing, the minimiser, the interpolation (cubic Hermite in ln r for ln u against linear interpolation of ln rho) and the slope/argmax bookkeeping are separate code. Same author family and same model family as the campaign. Agreement therefore certifies the numerics of a shared setup, not the setup.

## Departures from the frozen plan

- Rule (i) not run (frozen).
- States for s < 1e-13 M_b reuse the s = 1e-16 state with only the ln s and mass-fraction terms updated (the Poisson feedback is < 1e-13 of the potential); not used in modes C and D.
- The frozen 30001-point recheck of the argmax was not implemented; the 3001-point grid includes both endpoints and the argmax is the x = 30 endpoint in 64/64 cells.
- Production step 1e-3 in ln r (second order, E error about 4e-8 relative); controls S1-S3 at 2.5e-4; S4 compares 1e-3 with 5e-4. The grid extends to at least 31 r_M(canonical) and to tail decay; inner edge at 1e-9 x min(1e-4, h/a_B).
- Modes C, D use m in {1e-23, 1e-22}, mode E m = 1e-23 (time); S4 runs only in the main and E modes; S5 is realised as MUTATE A rather than a separate main-run line.
- Frozen pass lines that failed (P7a, P8a, P8b) were not repaired; extra rows are labelled post hoc.

## Not tested

Rule (i); m off the grid (masses below 1e-23 eV; CFG119's analytic remark that no core width can pass was not re-derived); excited states, granules and the NFW-like halo; self-interactions; non-spherical or time-dependent solutions; baryonic feedback; relativistic corrections for the 6 point-mass cells with a_B inside r_s; the CMB and lensing constraints (G2 is a linear-growth fit only); the alternative reading rho = rho_psi + rho_b; G3-G5 statements. The 1e5-1e11 dex misses are formal exponential tails of the ground state; the verdict rests on the closest cell (4.0-4.3 dex) and on all 64 cells failing at both ends.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

`./run_all.sh` and then `CFG119_JSON=../CFG119_fdm_soliton/CFG119_fdm_soliton_results.json python3 CFG159_compare.py` were run in this directory (`exit_codes.txt`: main 1, MUTATE A-E 1, g2 1, g2 MUTATE 1, compare 0 — the same as the referee's). Every `_results.json` is identical to the referee's except per-cell timing fields, and every `.out` differs only in timing. The `run_*.console.txt` logs are the console captures of this re-run; the C build directory `_cfg159_build/` was removed. The frozen criteria are `../CFG159_FROZEN_CRITERIA.md` (94605d68c).
