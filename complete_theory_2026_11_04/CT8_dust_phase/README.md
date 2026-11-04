# CT8_dust_phase: NO RELATION TIES THE DUST PHASE'S AMOUNT TO rho_DE. G5 FAILS for every relation that predicts a number; it can pass only with a fitted omega_x, as AeST does. G6 not reached

Criteria `FROZEN_CRITERIA.md` (written first). Script `ct8_dust_tie.py`; numbers `ct8_dust_tie.out`, `ct8_dust_tie.json`. Vanilla CLASS 3.3.4, CT3's peak finder, about 25 s on one thread, 0.38 GB. No download. Graded under owner decision D1 ("Yes, grade it"): a go to grade, not an adoption. The cold sector retired on 2026-11-01 stays retired. No particle. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## Why a tie to rho_DE is hard, in one line
Dust dilutes as a^-3 and rho_DE does not, so rho_x/rho_DE changes with time. A time-independent tie needs either a chosen epoch (R5, R6: "today", a convention) or a third component (R4: radiation), and then a pure number. The ratio the CMB wants, omega_x/omega_b = 5.36, is a dust-to-dust ratio, constant in time: a baryon-linked tie would be epoch-free; a rho_DE-linked one is not.

## The relations (out:line)
| | Relation | Prediction | G5 |
|---|---|---|---|
| R1 | AeST / mimetic / P(X) shift charge, rho_x a^3 = Q0 I0/(8 pi G) | none: I0 is an initial datum (C2 K2) (out:4) | NO PREDICTION |
| R2 | onset at H = n sqrt(G rho_DE), n = kappa (a0/c) or sqrt(8 pi/3) | H never falls below the de Sitter rate, so onset never; the number needed for z_on 3e4 is n = 3.1e7 (out:5-7) | **FAIL**, H3/H2 0.519-0.535 (out:19) |
| R3 | misalignment at m c^2 = (hbar c)^3/4 (rho_DE c^2)^1/4 = 2.2 meV | onset z ~ 1e16, amount ~ theta_i^2 free; a boson of definite mass, excluded by the no-particle rule (out:8) | NO PREDICTION |
| R4 | epoch-free invariant rho_x^4 = N rho_r^3 rho_DE, N = 1 | ratio 0.017; the data need N = 9.2e9 (out:9) | **FAIL**, 0.521-0.537 (out:20) |
| R5 | rho_x(0) = rho_DE | ratio 13.7 [12.8, 14.8] (out:11) | **FAIL**, 1.35-1.37 (out:21) |
| R6 | a0 = G M_m(<c/H0)/(c/H0)^2, canonical | ratio 4.62 [4.25, 5.08] (out:12) | **FAIL**, 0.933-0.955 (out:22) |
| R6 | same, alt footing (never pooled) | ratio 6.23 [5.75, 6.82] (out:13) | **FAIL**, 1.035-1.057 (out:23) |
| R6 | disclosed second reading, dust-only mass (not graded) | ratio 5.79 (out:14) | outside, 1.008-1.030 (out:24) |

Window: H3/H2 0.979 +- 0.010, ratio 4.9-5.4. H3/H2 ranges are over n_s 0.93 to 1.0. Check: the CT3 row reproduces 0.992 (out:18).

## Reading
- **No natural mechanism.** In the AeST/P(X) class the dust amount is an integration constant (R1). Any rate built from G and rho_DE is at or below the de Sitter rate, so it cannot switch dust on by z 3e4 without a pure number of order 3e7 (R2). The hbar route is a particle with a free amplitude (R3). The only epoch-free tie needs N ~ 1e10 (R4); this is the same size of number as baryons on the same invariant (1.1e7, out:10), so the problem looks like the baryon-asymmetry problem, not like dark energy.
- **R6 is a coincidence relation, not an action.** It brackets the window: canonical low (4.62), dust-only reading high (5.79). That shows how much its O(1) hand choices (R = c/H0, which mass, kappa) move it. Its canonical input range just touches 5.08, and the measured-a0 median sensitivity row gives 5.15 (out:16). These are sensitivity rows, not graded; they rest on kappa = 1/2 FITTED and a 32 % a0 box. Read as: the coincidence gets the order of magnitude, nothing more.
- **Circular trap, recorded.** The two footings encode Planck Omega_L = 0.6847 (out:3). Pooling them returns Planck's omega_c by construction. Not used.

## G6 (not run)
No relation passed G5, so G6 is not reached. If an omega_x were supplied (fitted), G6 would still need what CT3 and MC1 state: a frozen 3D run (AN2 machinery, converged grid, N about 440 per side for 3 %, per AN2) with a baryonic disc, showing the dust phase 66-82 % depleted from discs at 150-250 km/s. AN1/AN2 gave NO VERDICT (folds, no settling).

## Hand-set constants
kappa = 1/2 (R2, R5 via the footings unused, R6). R6 also takes R = c/H0 and M = total matter. R2's n, R4's N and R3's theta_i would each be a new constant. n_s is not natively measured, so it is bracketed. A_s, tau and YHe are inherited from CT3; the ratio barely depends on them.

## Caveats
The native H0 band (C2 K5) uses a sound horizon that depends on omega_m. The SN Omega_L is read in a flat background with matter. The TT fit uses diagonal errors and is not a likelihood (CT3).
