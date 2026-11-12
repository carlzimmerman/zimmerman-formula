# PD2 RESULT: FAIL / FAIL (criteria 98a5315562), first failing gate Q2 KiDS

Variant P: sheet-captured, single-counted phantom dust. TEST lane, quarantined. Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Footings never pooled.

## The share, as the source defines it (graded)

- L_web = v_stiff / H0 = 3.943 / 4.274 Mpc.
- The sqrt(M_b) cancellation holds. M_share / M_b falls from 779 to 7.8 between 1e8 and 1e12 (canonical) while R_trunc stays
  **0.301 / 0.326 Mpc** at every mass.
- The numeric R_trunc equals the closed form plus r_M / 2 (the -M_b / 2 term in the full phantom) to 0.2 %.
- **The source's claimed 143 M_b and 1.48 Mpc do not follow from its own formulas.** At M_b 1e11 they give 24.6 M_b and 0.31 Mpc.
  The claimed closed form (3/2) Omega_d L_web (1.57 / 1.71 Mpc) needs c_ta H^2 = 0.3 H0^2, not pi/2. It is graded as the bracket
  S-claim.

## Gates (canonical / alt)

| gate | canonical | alt |
|---|---|---|
| Q1 conservation, q (z-independent) | PASS 0.361 | PASS 0.430 |
| **Q2 KiDS** | **FAIL** max 0.959 (23/59), every lens Newtonian beyond 0.30 Mpc | **FAIL** 0.926 (23/59) |
| Q2 SPARC | PASS rms 0.0560 (no galaxy truncated inside R_last) | PASS 0.0558 |
| Q3 groups (0.40 share, prefactor-1 profile; orchestrator stand-in) | FAIL 0/1 | FAIL 0/1 |
| Q3 X-COP | FAIL +0.215 (under-filled); f_miss 0.60 / 0.48 / 0.40 vs TR1 0.71 / 0.66 / 0.58 | FAIL +0.206; 0.62 / 0.50 / 0.40 |
| Q4 cosmology | PASS, carried (cold reference; 1-halo NOT EVALUATED) | PASS |
| **Q5 Bullet** (galaxy-traced, Newtonian) | **FAIL**: class FAIL, M300 Z -3.32 / -4.62 (dark in R200 4.6e14 / 5.9e13). The gas-locked reading also FAILS | FAIL |
| Q6 | Cassini and moving Sun carried; screening (r / L*)^4 at Saturn 2.0e-23 | |

**Bracket S-claim (R_trunc 1.57 / 1.71 Mpc at z 0).**
- KiDS FAIL: 0.254 / 0.219, 3/59 points (the outer points at 1.6-3 Mpc).
- SPARC PASS.
- q at z 0.5 / 1 / 2 is 1.08 / 0.59 / 0.20 (alt 1.28 / 0.70 / 0.24). **Conservation fails at z 0.5** under the claim, as WL1 found
  (1.31 / 1.51).

**MUTATE.**
- MQ1 (f_sheet x 5, R_trunc 1.50 / 1.63): KiDS moves to 0.27 / 0.24 (power) and still fails.
- MQ2 (cluster fraction 1.0, PD1's bracket): X-COP passes, groups fail. The 0.40 fraction under-fills clusters.

**Known answers.**
- KA-Q1: universality holds, to 0.2 % against closed form + r_M/2. The frozen 2 % test against the bare closed form misses at 1e11
  canonical (2.0 %) because of the exact r_M/2 offset, which pd2_ka_check.py shows analytically (disclosed).
- KA-Q2: law-only replay exact (2e-16).
- KA-Q3: the frozen check's naive formula hit floating-point cancellation (6e-9 against 1e-10). The cancellation-free form passes
  at 7e-13 (post-run, disclosed).

## P7: is the J equilibrium action-derived?

**No, as relayed.**
- A J-auxiliary term a0^2 F(|J| / a0) - J . grad Phi_b, varied in J, gives |J| = (nu - 1) g_N,b only if F'(x) = x^2 / (1 - x).
- The source's dF/dy = y / (y + 1) gives |J| / a0 = y / (1 - y). At y 0.01 that is 0.005 against the law's 0.067.
- Even with the right F, the conserved dust's own continuity and Euler equations are not shown to place rho_d = div J / (4 pi G).
- So P is a phenomenological closure. The form choices are f_sheet 0.60, pi/2, L_web = v_stiff / H0, and the 0.40 cluster
  fraction (an orchestrator stand-in).

## Reading

- The sheet-capture rule makes the truncation radius universal, as claimed.
- **At the stated normalisation it is 0.30 Mpc,** so every KiDS lens goes Newtonian far inside the 3 Mpc the data reach: about
  -0.9 dex.
- **At the claimed 1.6 Mpc** KiDS still fails beyond it (-0.2 to -0.25 dex), and conservation fails at z 0.5.
- No universal R_trunc below about 3 Mpc can pass KiDS. One above 3 Mpc needs a share beyond conservation at z 0.5.
- Clusters at 40 % of the share are under-filled (X-COP +0.21), groups fail, and the Bullet's mass is too low.

**What a repair would need:**
1. R_trunc beyond the KiDS range (3 Mpc or more) for every isolated lens, while the population phantom stays below the dust at
   z 0.5. That forces the share to grow more slowly than the phantom at early times: a z-dependent capture law.
2. A cluster rule that fills X-COP (about the full share) and the groups together, which no profile tried so far does.

## Files

- Criteria: `FROZEN_CRITERIA.md`.
- Scripts: `pd2.py`, `pd2_ka_check.py` (post-run, disclosed).
- Outputs: `pd2.json` / `pd2.out`, `pd2_ka_check.json` / `pd2_ka_check.out`, the log `run_pd2.txt`.
- Cluster readings come from PD1's `pd1_a1.py` with PD1_SHARE 2.164, PD1_FCPRE 1.0. Those outputs are in PD1's dir:
  `pd1_a1_share2.164_fcpre1.0.json` / `.out`.
- Compute: one thread, about 2 min, RSS < 0.3 GB.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
