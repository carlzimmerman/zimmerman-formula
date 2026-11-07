# CE2: the late-heated cold-dark-energy window (QX7 iter_4 / QX10 cells). FAIL, all four cells, both footings, C3 included

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane (DEDUCTION_2026_11_07 section 4, lane "CE1"; the id CE1 is
taken, so this is CE2). Name: cold dark energy, never cold dark matter; no particle. Criteria: FROZEN_CRITERIA.md (8e89ef6740),
pushed alone before any script. Script: ce2.py (main 89 s; MUTATE 12 s). Outputs: ce2.json / ce2.out, ce2_MUTATE.json /
ce2_MUTATE.out, run_main.txt, run_mutate.txt. QX10 iter_2, QX7 iter_4, QX5, QX3 and DB1 are exec'd read-only.

**Label: FAIL.** Every cell fails X-COP's profile (GX), the groups (GG) and the Bullet (GB) on both footings. Every cell passes
CMB lensing (GL), fsigma8 at z < 1 (GF) and the forest at z 2-4 (GFo). The KX1 result cannot rescue a CE2 FAIL.

## Gate x cell x footing (canonical / alt where a0 enters)

| Cell (lambda_0 Mpc, p) | GL CMB lensing chi^2 (dchi^2) | GF fsigma8 Rf, z < 1 | GFo lambda_J(z 2) | GX X-COP mean / rms; bins (0-0.25, 0.25-0.5, 0.5-0.75 R500) | GG groups pass f*0, f*1 /20 | GB Bullet (v 2700) |
|---|---|---|---|---|---|---|
| C1 (2.61, 4.25) | PASS 8.88 (0.31) | PASS 1.000 all bins | PASS 1.7e-4 | **FAIL** -0.045/0.226; +0.18 -0.14 -0.31 \| -0.078/0.232 | **FAIL** 2, 1 \| 2, 1 | **FAIL** (sub's sector stripped) |
| C2 (1.47, 3.5) | PASS 8.70 (0.13) | PASS | PASS 5.2e-4 | **FAIL** -0.281/0.320 \| -0.305/0.340 | **FAIL** 4, 0 \| 3, 0 | **FAIL** (kept, ZM +1.72 / +2.10) |
| **C3 (8.25, 5.625)** | PASS 11.69 (3.12) | PASS | PASS 2.3e-5 | **FAIL** +0.324/0.364; +0.48 +0.30 +0.07 \| +0.287/0.333 | **FAIL** 0, 1 \| 0, 1 | **FAIL** (sub's sector stripped) |
| C4 (2.15, 3.75) | PASS 8.84 (0.27) | PASS | PASS 4.3e-4 | **FAIL** -0.123/0.239 \| -0.153/0.252 | **FAIL** 3, 1 \| 2, 0 | **FAIL** |

The lines are:
- GX: |mean| <= 0.05, rms <= 0.10, every bin <= 0.10 (NA2).
- GG: >= 16/20 at both f*, plus no kT trend.
- GL: chi^2 <= 18.48 and dchi^2 <= 4.
- GF: Rf <= 1.001, and inside 2 err of DESI DR1 on both panels.
- GFo: <= 0.162 Mpc.

## What the numbers say

- **X-COP: the profile is wrong, not the amount.**
  - In C1, C2 and C4 the sector holds its full share (4.2 M_b). The pressure-supported n = 1 profile leaves the centre
    short (inner bin +0.08 to +0.18) and puts too much outside (outer bins -0.23 to -0.41).
  - That is the same miss the record found in iter_4, iter_5 and iter_7: the needed mass is more concentrated than the hot
    gas, and a pressure-supported fluid sector is even less concentrated than the gas.
  - In C3 the sector reaches turnaround in the clusters too, so X-COP keeps too little (+0.29 to +0.32), and most of all in
    the centre (+0.48).
- **Groups: the trend is fine, but the amount and profile are not.**
  - No cell has a significant residual trend with kT: slopes are within 2 SE in every case.
  - The predicted f rises with kT, as the needed f does (Spearman +0.6 to +0.9 against +0.5).
  - But only 0-4 of 20 pass the strict rule. In C1, C2 and C4, f_pred is 4.1-4.2 against a needed 2.6-3.2, at the wrong radii.
    In C3, f_pred is 0.9-1.0 against the same 2.6-3.2.
- **Bullet: the sector is a fluid (p = K rho^2), and the collision is supersonic for it.**
  - Mach is 1.7-1.9 at the subcluster's centre.
  - In C1, C3 and C4 the main cluster's sector ram pressure strips the subcluster's sector. The stripped mass follows the
    gas, and the Bullet FAILS: M300 is off by +2.1 to +2.5 / -2.3 to -2.9 sigma.
  - In C2 the sector is kept on the subcluster, but M300 is still off (+1.7 / +2.1), and DB1's classifier returns FAIL.
  - The record's collisionless reading is not this action's sector.
- **CMB side:**
  - The heating is late enough that linear growth on DESI scales is untouched: Rf = 1.000 at every z < 1 bin.
  - The PR4 lensing shape passes, with C3 the closest at dchi^2 3.12.
  - The forest stays cold by 3 to 4 decades.

## Known answers and MUTATE (all PASS / BITE)

- KA1: iter_4 G2' at C1-C4 reproduced (0.3111, 0.1336, 3.1183, 0.2717), and K1 55.6403 reproduced.
- KA2: QX10 iter_2 static A reproduced exactly (X-COP, groups, G6; |d| = 0).
- KA3: the law alone gives X-COP +0.4675 / +0.4345, equal to QX2 and to GB1 L0 (|d| 4e-5).
- KA4: Rf = 1 at R = 1.
- KA5: the law-alone Bullet reproduced: M300 1.112e14 / 7.337e13, dkappa -0.068 / -0.111.
- M1, no heating (the sector at cosmic density, R = 5.409): captured ratio 4.1110, equal to KD1. G5 fails, and X-COP is -0.703
  (KD1's regime). **BITES.**
- M2, f_cap 0: X-COP +0.4675, so GX fails. **BITES.**
- M3, lambda_* x 10 at C1: CMB-lensing dchi^2 265. **BITES.**

## KX1 narrowing (arrived AFTER CE2's numbers; disclosed, not a re-freeze)

- After this run finished, the requesting session reported KX1 (6e1b777482).
  - The KiDS kill holds on C2 and C4.
  - C1 has no power.
  - Only C3 is untouched.
- It asked that C1, C2 and C4 be excluded and that the CANDIDATE label rest on C3 alone. Those exclusions could not be frozen
  before any number, because the numbers already existed.
- C3 was one of the four cells frozen in 8e89ef6740, and it was graded exactly as frozen. **C3 fails GX (+0.324 / +0.287,
  rms 0.36 / 0.33), GG (0-1 of 20) and GB on both footings.** So the narrowed question has the same answer: the C3 form of the
  window is not a candidate.

## Limits and disclosures

- Background: iter_4's own (QX3 iter2 worst corner), not QX15's footing fit.
- Cell values: the CMB-side gates use the exact iter_4 grid members; X-COP, groups and the Bullet use QX10's rounded values
  (2.6102 etc.). The difference is under 1e-5.
- GF compares DESI's ratio (to its fiducial) with the sector's suppression relative to itself unheated (frozen disclosure).
- Bullet:
  - The separation of the two Bullet-model centres (849 kpc projected) is taken as the 3D distance.
  - The DB1 "gal" field puts the kept sector in galaxy-scale profiles; stripped mass follows all the gas.
  - The Bullet child's peak RSS was 1.48 GB, over the 1 GB line (NA2's child was 1.19 GB). The main process peaked at 145 MB.
- Groups: in C2 every group keeps its whole sector inside R500, so f_pred is constant and its Spearman coefficient is undefined
  (nan, a warning in run_main.txt). The graded trend slope is unaffected.
- The static n = 1 end state follows QX10 iter_2. A multi-stream (post-shell-crossing) remnant is outside the fluid description;
  QX7 iter_7 already graded the gas-tracing remnant reading, and it failed SHAPE.

Kappa = 1/2 FITTED; not theory closed.
