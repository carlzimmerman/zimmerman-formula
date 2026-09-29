# CFG159 -- independent re-derivation of the CFG119 (door 7, Schroedinger-Poisson soliton + baryons) G1 headline. FROZEN CRITERIA

Written 2026-09-29, phase 1, before any script or number of this lane. Referee lane: it edits nothing in the repo. It re-derives the G1 headline (and the G2 line) of CFG119 (committed 435cb43e9) with its own code. A scoped result, a partial agreement, or a disagreement is a valid outcome. kappa = 1/2 is FITTED; nothing here says the data favour the framework; failed controls and wrong expectations are kept, never repaired.

## What I read before writing this, and what I did not

Read: CFG119_FROZEN_CRITERIA.md; CFG119 README.md (including its appended referee note); the CFG44 README and the docstring of Bcommon.py (definition of the exponential sphere only); closure_map/TEN_DOORS_GATES_2026-09-29.md (gates G1-G5).
NOT opened: any CFG119 script, .out or .json (phase 2 only, after my own main and MUTATE runs are saved). The CFG119 README numbers below are TARGETS I have read, not blind predictions. The hand estimates in the section "Hand estimates" were made AFTER reading the README, so where they agree with it they are consistency checks, not independent predictions; this is stated per row.

## What is re-derived

The G1 headline of CFG119, on rule (ii) (free soliton mass per galaxy; the most generous reading, which bounds rule (i)):
- H-a: for m = 1e-23 eV, M_b = 1e9 Msun, CFG44's exponential sphere (h = 2 kpc), free M_sol, the ground state's C_SP(r) = rho_psi(r) r^3 g_tot(r) misses C_target(r) = (a0/4pi) M_b(<r) over x = r/r_M in [0.1, 30] by J = 4.26 dex (canonical a0) and about 4.0 dex (alt a0); pass line +-0.04 dex.
- H-b: with ONE m at every mass, the best m is 1e-23 eV and its worst galaxy (point mass, 1e12 Msun) misses by 1.18e5 dex (canonical).
- H-c: the failure is in both the core (density flat, log slope -0.0005 to -0.07, against the target's -0.55 to -1) and the envelope (exponential; log slope at 30 r_M from -9 to -3e11, against the target's -2).
- H-d (G2): growth within 5% (T_F >= 0.95) to k = 30 /Mpc needs m >= 1.28e-20 eV (HBG transfer function).
Rule (i) (Schive core-halo) is NOT re-derived: rule (ii) minimises over every M_sol and so cannot be worse; CFG119 itself says rule (i) cannot beat (ii). The C1 pure-soliton check is not re-derived (CFG119_referee_sp_shooting.py already does it); I only reuse the no-baryon soliton as a solver control.

## Definitions pinned before any run

1. Units and constants (from the CFG44 docstring, shared): G = 4.30091727e-6 kpc (km/s)^2/Msun; a0 canonical = 9.3603e-11 m/s^2, alt = 1.1312e-10 m/s^2; 1 kpc = 3.0856775814913673e19 m; c = 299792.458 km/s; hbar c = 1.973269804e-7 eV m. Boson lengths: hbar^2/(G M m^2) = (hbar/mc)^2 / (G M/c^2). Grid of cells: m in {1e-23, 1e-22, 1e-21, 1e-20} eV; baryons: point mass or exponential sphere (rho_b = M/(8 pi h^3) e^(-r/h), M_b(<r) = M[1 - (1+s+s^2/2) e^-s], s = r/h) with h = 2, 3, 4, 5 kpc for M_b = 1e9, 1e10, 1e11, 1e12 Msun (the pairing is read from the CFG119 README). That is 2 geometries x 4 masses x 4 m x 2 footings = 64 rule-(ii) cells.
2. r_M = sqrt(G M_b / a0) with the TOTAL baryon mass of the cell, both geometries (read from CFG44's point-mass form g = sqrt(g_N^2 + a0 g_N), M_c = M(sqrt(1+x^2) - 1)). x = r/r_M.
3. The ground state: nodeless, l = 0, of -(hbar^2/2m) psi'' + m(Phi_b + Phi_psi) psi = E psi, Phi_psi from Poisson with source m|psi|^2, normalised to M_sol = m int |psi|^2 dV. Boundary: regular at 0, decaying at infinity.
4. C_SP(r) = rho_psi(r) r^3 g_tot(r), with rho_psi = m|psi|^2 (the boson density ONLY, the target's "rho_c" is the cold fluid, not the baryons) and g_tot = G [M_b(<r) + M_psi(<r)] / r^2. For a point mass this gives the ratio C_SP/C_target = (4 pi G/a0) rho_psi r (1 + M_psi(<r)/M_b), matching the analytic remark in the README (a consistency check on the reading, not a proof of it). The alternative reading rho = rho_psi + rho_b is NOT used; it would change the question.
5. THE MISS (pinned): for each cell and footing, ratio(x) = C_SP/C_target; J = max over x in [0.1, 30] of |log10 ratio(x)| on 3001 log-spaced points including both endpoints (plus a 30001-point recheck of the argmax). "The closest single galaxy" = the minimum of J over all rule-(ii) cells of that footing. "Best single m" = the m minimising the maximum of J over all 8 geometry x mass cells. Rule (ii): M_sol minimises J; search log10(M_sol/M_b) in [-16, 4] (the range CFG119 declares), 0.5-dex scan then golden section to 1e-3 dex. Ratio uses base-10 logs; a cell's log ratio can be extremely negative (down to about -1e5 to -1e11): those are held as exact log-space exponents, never as floats of rho.
6. "Core" cell: the ground state has rho(0.1 r_M)/rho(0) >= 0.5. Slopes are d ln rho / d ln r of the boson density (target: point mass -1 - x^2/(1+x^2) = -1.010 at x = 0.1 and -2 - ... towards -2 at large x; extended baryons -0.55 to -1 at 0.1 as read from the README).

## Shared with CFG119 and therefore NOT independent (stated plainly)

- The target definition (CFG44: exponential sphere formula, r_M, G, a0, the two footings) and the declared cell grid (m list, masses, h pairing, the pass line, the rule-(ii) definition and the [-16, 4] search range). If any of these is wrong, both of us are wrong together.
- The HBG (2000) transfer-function fit used for G2: I evaluate the same published fit from my recollection of its form (T_F(x) = cos(x^3)/(1+x^8), x = 1.61 m22^(1/18) k/k_J,eq, k_J,eq = 9 m22^(1/2) /Mpc, m22 = m/1e-22 eV; half-amplitude scale 4.5 m22^(4/9) /Mpc). G2 is therefore a formula check, not an independent physical derivation. (Note in passing: the README calls k_1/2 "half-power"; the numbers it lists are the T = 1/2 amplitude scale.)
- Same author family, same model family as the campaign; a shared blind spot is possible.
- The physics statement itself (spherical, static, Newtonian, ground state only) is shared. Untested by both: excited-state envelope and granules, self-interactions, non-spherical/time-dependent solutions, baryonic feedback, m off the grid, relativity for the point-mass cells whose Bohr radius sits inside the Schwarzschild radius (I will report a_B/r_s, not exclude those cells).
Independent: the solver method and code (below), the tail treatment, the minimiser, and the slope/argmax bookkeeping.

## Solver plan (my own, unlike CFG119's finite-difference inverse iteration in ln r)

Dimensionless units: length a_B = hbar^2/(G M_b m^2), energy G^2 M_b^2 m^3 / hbar^2, soliton mass s = M_sol/M_b. Then each cell has only three numbers: b = r_M/a_B, the geometry (point, or h/a_B) and s. Eigenproblem by Riccati/log-derivative shooting in t = ln r: y = d ln psi/d ln r integrated outward from the centre (series start) and inward from a WKB start at large r (the stable direction), matched at the classical turning region; E found by bracketing on the mismatch (nodeless = monotone bracket). ln psi is the integral of y, so tails are exponents (values of order -1e5 to -1e11 are represented, never floored). Enclosed boson mass by cumulative quadrature of exp(2 ln psi - 2 ln psi_max) with the exact saturation of M_psi(<r) beyond the bulk. Self-consistency: fixed-point iteration on Phi_psi with under-relaxation, tolerance |dE/E| < 1e-9, then verified by an independent residual check of the Schroedinger equation on a refined grid.

## Hand estimates (ESTIMATES, made after reading the README; each row says how much they can be trusted)

| item | my estimate | probability the README number reproduces in my solver |
|---|---|---|
| H-b tail scaling: J ~ 2 (30 r_M/a_B)/ln10 for the point mass, 1e12, m = 1e-23: a_B = (hbar/mc)^2/(GM/c^2) = 2.64e17 m = 8.5 pc; r_M = 38.6 kpc; 30 r_M/a_B = 1.355e5; J ~ 1.177e5 (+- a few tens of dex from prefactors). Alt: x sqrt(9.3603/11.3120) = 0.910, so 1.07e5. This reproduces README's 1.18e5 to 0.3%. It is a consistency check of the exponent, not blind. | 1.18e5 within 1% | 0.85 |
| H-b: best single m = 1e-23 eV for both footings | m = 1e-23 (a_B grows as 1/m^2, tail exponent scales as m) | 0.95 |
| H-a canonical J = 4.26, the closest cell = exp sphere 1e9, m = 1e-23 | not derivable by hand (needs the eigenproblem in the exponential-sphere potential; a crude core-size estimate gave an order-of-magnitude agreement at x = 0.1 only). My honest guess: J in [2, 8] dex. | J within 0.3 dex: 0.70; cell is the global argmin: 0.85 |
| H-a alt J about 4.0 | alt/canonical = 0.94 in the README (same order as the 0.91 tail scaling) | J within 0.3 dex: 0.70 |
| R1 at closest cell canonical: -3.57 (x=0.1), -2.58 (x=1), -4.26 (x=30) | shape: too thin everywhere; worst at x = 30 | each within 0.3 dex: 0.60 (three numbers, correlated) |
| optimum M_sol/M_b at the closest cell: 0.64 canonical / 0.76 alt (the README states 0.76 in the bottom line for the alt-footing cell and 0.64 in R1 for canonical) | flat optimum, "more mass shrinks the core"; expect 0.3-1.5 | within 0.1 dex of the README values: 0.45 |
| the 32 canonical J values in the README table (rule ii) | pure-tail cells (point masses, large J) follow the exponent scaling | >= 28 of 32 within tolerance: 0.65; >= 24 of 32: 0.85 |
| H-c flat core / exponential envelope (numeric slope tests below) | qualitative; slopes reasonable | all slope tests pass: 0.75 |
| H-d G2: T_F(x) = 0.95 at x = 0.622 (by hand) gives m_min = 1.28e-20 eV (checked: 30 x 0.1789 = 5.37, 5.37 m22^(-4/9) = 0.622, m22 = 128); T_F(k = 30, m = 1e-20) = 0.897, i.e. 10.3% low (checked by hand). Reproduces the README to the printed digits. | formula-level, shared | 0.92 |

## Exact pass lines (frozen)

For each footing, cells scored on rule (ii). "Agree" needs the whole set below; a miss on any single line is reported as it is.

- P1 closest cell: the argmin of J over the 64 (per footing) is (exp sphere, 1e9 Msun, h = 2 kpc, m = 1e-23 eV) on both footings; canonical J within 0.3 dex of 4.26 and alt J within 0.3 dex of 4.0.
- P2 verdict: J >= 3.0 dex in every one of the 64 cells (a factor 75 above the +-0.04 dex band; this states H1 = FAIL on both footings). I also report the count of cells with J <= 0.0458 (must be 0).
- P3 single m: best m = 1e-23 eV on both footings; canonical worst-galaxy J within 1% of 1.18e5 dex; alt/canonical worst-galaxy ratio in [0.89, 0.94]; worst galaxy = point mass 1e12.
- P4 table: for each of the 32 canonical cells, J within max(0.3 dex, 2%) of the README table entry. Agreement: >= 29 of 32; partial: 24-28; disagreement: < 24. Additionally, all 32 alt J values lie 6-11% below the canonical ones (README statement), tested for cells with J > 100 dex (tail-dominated) by the pure r_M scaling 0.910 +- 0.02.
- P5 R1 profile at the closest cell (canonical): log10 ratio at x = 0.1, 1, 30 each within 0.3 dex of -3.57, -2.58, -4.26; the argmax x is 30.
- P6 M_sol optimum at the closest cell: within 0.1 dex of 0.64 M_b (canonical) and of 0.76 M_b (alt). If only the README's internal 0.64/0.76 inconsistency causes the miss, that is reported as a README ambiguity, not a physics disagreement.
- P7a core slope (numeric test of "flat vs 1/r"): the set of core cells (definition 6) is non-empty, all of them have m <= 1e-22 eV and M_b <= 1e10 Msun, and in every core cell the boson log slope d ln rho/d ln r at x = 0.1 lies in [-0.15, 0]; the target's slope there is <= -0.5. (README: -0.0005 to -0.07 over the 16 core cells of its 128 cells, of which I score only the rule-(ii) ones.)
- P7b envelope slope (numeric test of "exponential vs r^-2"): in every cell the boson log slope at x = 30 is <= -6 (target: -2), with the shallowest cell in [-18, -4.5] and the steepest <= -1e9 (README: -9 to -3e11).
- P7c "both": in every cell |log10 ratio| > 0.3 at BOTH x = 0.1 and x = 30 (so neither end is rescued), and x = 30 is the argmax in >= 90% of the cells (README: all).
- P8 G2: k_1/2 = 1.6, 4.5, 12.5, 34.8 /Mpc within 2%; the k up to which T_F >= 0.95 = 1.2, 3.5, 9.7, 26.9 /Mpc within 3%; m_min(30/Mpc) = 1.28e-20 eV within 3%; T_F(30/Mpc, m = 1e-20) = 0.897 +- 0.005 (10.3% low).
- Solver controls (must pass or the run is void): S1 self-gravity off, point mass: E and ln psi against hydrogen (E = -1/2 in the units above, psi ~ e^(-r/a_B)) to 1e-8 and 1e-6 relative; S2 no baryons: E = -0.16277 (in G^2 M^2 m^3/hbar^2, the value both CFG119 and the literature soliton give) to 1e-5, r_c = 2.6794 a_B(M_sol) to 1e-4; S3 virial theorem 2K + W_total-type identity to 1e-6 on five cells; S4 halving the grid step changes E and J by < 1e-6 relative on five cells; S5 measured against the target's own rho_c the evaluator gives J < 1e-5 dex (this is also MUTATE A).

## MUTATE controls (each flips a load-bearing cell; the env var MUTATE selects it; exit 1 when the control bites, i.e. when the headline P1/P2/P3 no longer holds)

- MUT-A (evaluator): replace rho_psi by the target's own rho_c = a0 M_b(<r)/(4 pi G r^3 (g_tot)) with g_tot = the target's own. Expected J < 1e-5 dex in every cell; P2 flips to "H1 PASS". Bites: exit 1. This shows the evaluator can pass.
- MUT-B (soliton compared with itself): replace C_target by the soliton's own C_SP. Ratio = 1, J = 0 exactly. Expected exit 1. Bounds the bookkeeping, not the physics.
- MUT-C (remove the baryons from the Schroedinger potential, keep the target and M_b in r_M and the target): the state is the pure soliton, of width fixed by M_sol alone. Expected J changes from the main value by > 0.3 dex in the closest cell (I estimate 85% that it does), which would show the baryon potential is load-bearing for the 4.26. If it does not move by > 0.3 dex, that is recorded as an informative non-bite, not repaired.
- MUT-D (sign-flip of the baryon potential only: repulsive baryons, attractive self-gravity). Expected: no cell passes the P1 argmin/P3 lines unchanged (the closest cell moves or no bound state exists in the small-s branch); reported as it comes. If a cell has no bound state the script records that explicitly and treats J as not defined (bites).
- MUT-E (Poisson source x 1.05, as in CFG119's referee note for C1): S2's E and r_c must move (E ~ -0.1795, r_c ~ 2.55) so the solver controls fail. Exit 1. This shows the S2 control can fail.
Exit convention: main run exits 0 iff every solver control and P1-P8 that is declared load-bearing passes (a partial or failed line is printed and the exit is 1; a disagreement is not repaired). Each MUTATE mode exits 1 when it bites. No script prints an absolute home path; outputs use names keyed by mode.

## What counts as disagreement

- Any of P1-P3 failing (closest cell identity, J within 0.3 dex of 4.26/4.0, best m, worst-galaxy 1.18e5 within 1%) is a disagreement with the CFG119 headline. It goes to the orchestrator with the definitional differences separated from solver differences (in particular the choice rho_psi versus rho_total and the r_M definition for extended baryons).
- P4 below 24/32 is a disagreement with the table; 24-28 partial. P5-P7 failures are disagreements with the qualitative core/envelope statement, reported separately per line. A verdict-level disagreement would require a cell with J < 0.3 dex in my solver; I do not expect it (probability 0.03).
- Agreement on all lines would mean only that an independent Riccati solver, using CFG44's shared target, reproduces the CFG119 numbers. It would say nothing about the excited-state envelope, self-interactions or feedback, and nothing about the framework being closed.

## Script plan (all in the scratch lane; runtime < ~15 min per run on multiple worker processes)

- CFG159_sp_riccati.py: solver (Riccati shooting in ln r, log-space tails, self-consistent iteration), the 64-cell rule-(ii) scan, the single-m aggregation, the slope/argmax/R1 rows, controls S1-S5, JSON and .out output. MUTATE=A..E via environment variable; outputs keyed by mode (CFG159_sp_riccati.out / CFG159_sp_riccati_MUTATE_<x>.out and the matching _results.json).
- CFG159_g2_hbg.py: the G2 formula check (H-d) with its own MUTATE (exponent in x^8 changed to x^6: m_min must move) exiting 1.
- Phase 2, after both are saved: only then may I open CFG119's script, .out and .json and compare row by row; the comparison is written as an ANSWER-ROW file, with every difference classified (definition versus solver versus README typo). Runtime budget: cell scan parallelised over cells (64 cells x ~55 solves each); if it exceeds 15 minutes the s-scan is coarsened to 1 dex before golden section and that departure is disclosed.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model or that the theory is closed.
