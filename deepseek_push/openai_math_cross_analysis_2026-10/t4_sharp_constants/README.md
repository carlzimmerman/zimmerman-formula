# T4 -- sharp-constant search in the a0 sector (EXTREMAL/ENERGY route)

Targets: T = 1/sqrt(32 pi) = 0.099736 (coefficient in a0 = c^2 sqrt(Lambda/32 pi))
and the rational 4 in G rho_Lambda = 4 a0^2/c^2. kappa = 1/2 stays FITTED.
Script: `t4_sharp_constants.py` (sympy + numpy/scipy; 24/24 checks PASS, exit 0).
MUTATE (`T4_MUTATE=1`): seeded random F-form v* = 0.100658 within T's 1%-window,
tagged derived -> 'special' flips 0 -> 1 and the base rate changes as declared
(outputs `*_MUTATE.*`).

## Verdicts (per candidate; miss vs the closer of {T, 4}; p_base = share of the
889-form family F within that miss)
| candidate | value | best miss | p_base | verdict |
|---|---|---|---|---|
| T, 4, 1/4 (fitted-law restatements) | 0.0997 / 4 / 0.25 | exact | 0 / 0.001 / 0.172 | CHOSEN [calibration] |
| 1/(32 pi), 32 pi (squared spellings) | 0.0099 / 100.5 | 90% / 2400% | 0.13 / 1.0 | CHOSEN |
| 32/3 (Mahler n=3, 087) | 10.67 | 167% | 0.93 | CHOSEN |
| sqrt(32/3) | 3.266 | 18.3% | 0.072 | CHOSEN |
| 9/(8 pi) (propeller, 096, sharp) | 0.358 | 259% | 0.25 | CHOSEN |
| sqrt(9/(8 pi)) | 0.598 | 85% | 0.53 | CHOSEN |
| zeta_A(6) (triangular lattice, 090) | 4.1413 | 3.5% | 0.011 | NUMEROLOGY (coincidence; no physical reading; not special) |
| zeta_A(3), zeta_A(4), NN^2, b^-1/2, theta, C_BHS, W(E_triangle) | 8.88 / 5.78 / 1.155 / 1.075 / 0.160 / -0.056 / -0.201 | 44-3200% | 0.01-0.92 | CHOSEN |
| 1/3, 2/3, (32 pi)^{1/4}, (32 pi)^{-1/4} (emerged from (b)) | 0.333 / 0.667 / 3.167 / 0.316 | 21-92% | 0.07-0.92 | CHOSEN |
| 64/9, 8/3 (general Mahler, POST-HOC); 1/pi (propeller k=2, POST-HOC) | 7.11 / 2.67 / 0.318 | 33-92% | 0.13-0.68 | CHOSEN |

## Screen Q1-Q3
- Q1: NO candidate derives a0. The exact hits (T, 4, 1/4) ARE the fitted law
  restated (a0 = c^2 sqrt(L/32 pi) <-> G rho_L = 4 a0^2/c^2 with
  rho_L = Lambda c^2/(8 pi G)); every other candidate accepts a0 and only then
  misses. (Flagged: the 3 Lambda/(8 pi G) spelling with kappa = 1/2 gives
  a0^2 = 3 c^2 Lambda/(32 pi) -- a sqrt(3) discrepancy in a0 -- not used here.)
- Q2: chosen everywhere. The analogy constants (096/087/090) have no physical
  mapping to the a0 sector; the mapping would itself be a free choice, and they
  miss anyway. The (b)-emerged 1/3 and 2/3 are forced by the y^{3/2} Lagrangian
  but miss both targets by > 90%.
- Q3: p_base >= 0.01 for every derived candidate (the only two sub-1%
  p_bases belong to the exact-hit calibrations, which are NOT derived). 1%-window
  shares recomputed: 0.0022 vs T (record 0.002-0.003), 0.0045 vs 4. Null can fire
  (0.1% positive control p = 0). A derived candidate is special nowhere.

## The extremal problem (b) -- honest bottom line
The deep-MOND point-mass sector is fully computable (all checks pass):
E_field(R) = (1/3) M sqrt(G M a0) ln(R/r_in)  [log-divergent, r_in -> 0];
rho_ph(deep) = sqrt(G M a0)/(4 pi G r^2); full-kernel M_ph(<r) = M(nu(y)-1) =
r sqrt(G M a0)/G within 1.1% at 100 r_t (full kernel; declared 3%).
But at fixed Lambda every dimensionless ratio carries free M, R, r_in (or ln,
or is the tautology a0/(c^2 sqrt L) = T by DEFINITION of the fitted law).
(32 pi)^{+/-1/4} appear only inside M,R-dependent combinations. Nothing in the
extremal problem outputs 4 or 1/(32 pi) or a bare half-power; an extremal that
"outputs" T does so only because a0 was inserted via the fitted kappa = 1/2.

## T4b -- propeller partition (096)
The sharp propeller (three 120-deg sectors) has cells of Gaussian measure
1/3, 1/3, 1/3 (exact, C_v4). The bound constrains sum ||z_i||^2, not cell
masses. A 1/2 settled/unsettled ratio requires postulating a 2-cell partition
(k=2 value 1/pi), which is a free choice. NOTHING FORCES 1/2.

## Controls verified
C_law (kappa=1/2 <-> 4 a0^2 = c^2 G rho_L), C_v1-C_v4 (096: 9/(8 pi) exact +
numeric; masses 1/3), C_el (3-Laplacian flux), C_b1 (E_field sympy + numeric),
C_b2 (full-kernel rho_ph: sympy structural identity + flux identity 1e-4 +
finite-difference cross-check 1e-3), C_b3 (deep phantom 3% at 100 r_t),
C3a-c (F from definition; q=32 not in F; T, 1/(32 pi), 32 pi not in F;
4, 1/4 in F), C7 (null can fire), C6 (verdicts generated; 0 specials in main).
MUTATE: 'special' 0 -> 1 and base rate T:0 -> v*:0.002, as declared.

## Bottom line
No FORCED constant; no NUMEROLOGY except zeta_A(6) (3.5% miss, p_base 0.011,
not derived, no physical reading -- flagged coincidence). The analogy families
supply pi^-1-type constants (9/(8 pi), 1/pi), pi-free algebraics (32/3,
sqrt(32/3), 64/9, 8/3, zeta values, 1/3, 2/3) and log-Gamma constants
(C_BHS, W(E_triangle) = -0.201) -- never pi^-1/2 x (rational/32): exactly the
gap CFG380 found on the geometric side, now confirmed from the
extremal/energy side. kappa = 1/2 stays FITTED; 32 pi remains chosen, not
derived.

Note: 1/3 coincides numerically with CFG380's R1 Nariai reading but arises
here from the y^{3/2} Lagrangian power (different mechanism; CFG380 result
not reproduced by route, only by number -- flagged, not re-tread).