# LC1_live_contraction: STRONG; BLUMENTHAL HOLDS. A disc grown in a live zoom contracts the cold fluid about as the spherical formula says

Criteria: `FROZEN_CRITERIA.md` (f4c8459748). `lc1_disc.py`, `lc1_read.py`, `lc1.out`, `lc1_results.json`, `lc1_x74.py`, `lc1_sparc_fq*.log`. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework. Newtonian, gravity only, no feedback.

## Frozen grade, 10¹², nine same-seed pairs, z = 0
M_d 6.72e10, R_d 3.565 kpc. **R_live 2.154 [1.65, 2.52], STRONG** (line 1.45). **f_Q 0.872 [0.54, 1.07], BLUMENTHAL HOLDS** (line 0.8). At equal particle mass R_live is 2.240, the same class.

| r/R_d | 1 | 2 | 3 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|
| Q live | 3.39 | 2.29 | 1.94 | 1.69 | 1.47 | 1.44 | 1.35 |
| Q Blumenthal | 3.74 | 2.53 | 1.96 | 1.74 | 1.46 | 1.34 | 1.28 |
| Q Gnedin | 3.50 | 2.16 | 1.80 | 1.58 | 1.40 | 1.30 | 1.26 |

r/R_d 1 is at 3ε (1.11 R_d), so read it with care. R_live rises as the disc grows: 1.47, 1.75, 2.15 at z 0.5, 0.25, 0. c_nfw goes 12.95 to 23.90.

**Argon's lines:** both versions (1.25 and 1.45; 1.22 and 1.40) fail: R_live is above each fail line, "confirming Blumenthal's failure in 3D". Its stop condition for isolated galaxy halos needed this together with SI3 and AM1: SI3's post-result reading and AM1 meet their parts, and SI3's frozen class is NO VERDICT.

## SPARC at this strength (reported, carrying one 10¹² number across SPARC's masses; rule with floor, CE1's ng 64 table)
Contraction scaled by f_Q 0.872: **Υ 0.32 / 0.32, rms 0.0717 / 0.0730, SPARC line FAIL.** Alt 0.30 / 0.30. At f_Q 1: 0.30 / 0.31. Without contraction: 0.50 / 0.49. So the live test gives no relief from CN1's result.

## Limits
A smooth analytic disc grown steadily from z_f, with no baryon clumps, no outflows and no back-reaction on the disc. Feedback isn't in this test: it says what gravity alone does, and that's the wall any mechanism has to overcome. One mass. M_d is from EM1's relation. N-body response below 2 R_d is at the resolution edge.

## Checks
K1 M_d 0 against the engine 0. K2 force 3.7e-7. K3 contract 2.0e-8. Reader self-test: identity pair Q 1; particles moved to Blumenthal's radii give f_Q 1.000. MUTATE M_d × 2: Q(3 R_d) − 1 +64 %, BITES.
