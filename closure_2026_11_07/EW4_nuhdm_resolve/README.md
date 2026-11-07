# EW4: nuHDM (the a0 law + one 11 eV thermal fermion), HC1 vs Angus resolved, graded on the framework's terms

TEST lane. Adopts nothing. **The no-dark-matter-particle rule is relaxed for this lane only, as for HF1 and HC1.**
Kappa = 1/2 FITTED; not theory closed. Footings graded separately, never pooled. Nothing here says the data favour the
framework or nuHDM. Literature items are from memory, no download: [lit, PROVISIONAL].

- Criteria: FROZEN_CRITERIA.md (origin 8833a24300, local 1e3cca4d5c), committed alone before any script or number.
- Scripts: ew4_static.py (KA1-KA5, readings C, SPARC ceiling, UDG bound, KiDS G6; `--mutate` twin), ew4_cmb.py
  (primary CMB on QX15's grader with CLASS ncdm). Outputs *.json / *.out, parts/, logs/. Compute: 1 thread each, nice 15;
  statics 2 s; CMB fits ~25 min per footing.

## 1. Why HC1 says FAIL and Angus says "fits": answered

**They ask different questions, and on the record's clusters both are right.**

- **Same physics inputs.** Mass 11.14 eV (HC1, from the record's omega_d 0.11958) vs 11 eV (Angus), both thermal at
  T_nu with g = 2. Same Tremaine-Gunn form. Same interpolation family (simple nu). These are not the cause.
- **The test differs (the cause).** Angus infers the fermion profile each cluster needs and asks whether phase space
  allows it (consistency, amount and shape free per cluster). HC1 fixes the amount (cosmic fair share inside turnaround,
  several Mpc) and the shape (isothermal in the model potential), then grades it (prediction).
- **EW4 ran Angus's test on X-COP.** 6 of 7 GB1 clusters are consistent on both footings (plus 5 of 5 gas-only
  clusters, reported). The required fermion is M_req/M_b = 1.8-3.4 inside 0.7 R500. That uses 32-62 % of the fair-share
  supply. Phase space never binds: required density / rho_TG <= 0.008 at sigma 1140-1300 km/s. Any m >= 3.3 eV would do.
  The one miss (A644) needs negative fermion mass in its 625-875 kpc shell.
- **So Angus's PASS is the consistency reading (C), and it reproduces on the record's data.** HC1's FAIL is the
  prediction reading (P): fair share spread out to r_ta puts only M_f/M_b 0.31 at X-COP's radii, and the shape is wrong.
  The literature never claimed a predictive profile; it claimed room in phase space.
- **The secondary differences change little.** These are the sample (Chandra ~30 vs X-COP 7 + Lovisari 20), the
  radii, the lower a0 here (more missing mass), and the background. Angus's own failures (cluster centres
  r <~ 100-150 kpc, groups with T < 2 keV) sit inside X-COP's first point or in the groups.
  - The groups do fail here too, but by a different route: the law already over-predicts some cool groups' R2500-R500
    shell when stars are added (f* = 1). Phase space is not what fails them.

## 2. Labels (canonical / alt; the labels agree on both footings)

Label rule (criteria section 3): C FAIL -> FAIL (robust); C pass and P FAIL -> "FAIL (P); C consistent"; both pass -> PASS.

| Cell | C (consistency) | P (prediction) | Label | Key numbers |
|---|---|---|---|---|
| SPARC (not in discs) | consistent (law fits) | HC1 G1 PASS | **PASS (not robust)** | Phase-space CEILING fails G1: rms 0.160 / 0.165 vs 0.146 / 0.143 (Z -0.015 / -0.043). M_f,max/M_b at R_last median 0.06, max 25. rho_TG median 6e-5 Msun/pc^3. TG allows filling fast discs; HC1's isothermal fair-share profile is what keeps them empty |
| X-COP clusters | **6/7 consistent** (80 % line; disclosure 2) | HC1 G2 FAIL +0.392 / +0.360 | **FAIL (P); C consistent** | M_req/M_b 1.8-3.4; supply 32-62 %; TG ratio <= 0.008; m_min 2.3-3.3 eV |
| Groups (f* 0, 1) | FAIL: f*0 18/20, f*1 **14/20 / 11/20** (line 16) | HC1 G3 FAIL | **FAIL** | All misses are C-a (law over-predicts the shell, needs negative fermion), mostly kT < 2.2 keV. C-b (phase space) never fails; m_min <= 3.9 eV |
| Ellipticals (2-8 Re) | **FAIL 0/7** (phase space) | HC1 G4 FAIL | **FAIL** | In 6 of 7 the largest regional required density is 2.3-49x rho_TG at sigma = V_c,max/sqrt 2 (NGC 4261 passes C-b, fails C-a); TG m_min 9.9-29.5 / 9.4-29.2 eV (median 15.3 / 14.8). At Kroupa M/L; QX26/ST1's IMF explains these with the plain law, no fermion |
| UDG AGC 114905 | FAIL | n/a | **FAIL** | Law over-predicts 5/5 rings; a fermion only adds field. chi2_min over ANY fermion 843.6 / 995.8 (5 rings), p ~ 1e-180 / 1e-213 |
| UDG Malin 1 | FAIL | n/a | **FAIL** | Over-predicts 4/4 rings; chi2_min 69.0 / 132.5 (4), p 4e-14 / 1e-27 |
| Coma UDGs | FAIL (HC1 max bound) | HC1 G5 FAIL | **FAIL** | At the maximum bound +1.000 / +0.953 dex, 3.8 / 3.6 sigma_U |
| dSph classes | consistent (HC1 max bound, bright M31 Delta_max 1.75) | HC1 G6 FAIL (+0.094 / +0.086) | **FAIL (P); C consistent** | Not robust: a host fermion sea passes G6 at 50 kpc, fails at 100 and 200 kpc (hc1_report) |
| KiDS G6 (QX10/EW2 line) | consistent (M_f = 0 allowed) | **G6 -0.098 / -0.098 dex** (line 0.05) | **FAIL (P)** | HC1's R4 fermion keeps the full fair share (M_f/M_b 5.55) by the outer LE radii; shift -0.096 to -0.104 per bin |
| KiDS colour split | as HC1 | HC1 G7 FAIL (R 2.42 sigma) | **FAIL** | carried |
| Cassini / PPN | | | **PASS with v3s / AC2q as the MOND part; FAIL with Angus's QUMOND** | v3s: Q2 >= 4.8e7 inside Hees (C6P); fermion at the MW cap adds 1.3e-20 m/s^2 at Saturn (HC1 G8). QUMOND: 1.70-3.70x / 1.91-4.03x Hees (AX1) |
| c_T | | | **PASS (v3s / AC2q); N/A (QUMOND, non-relativistic)** | v3s c_T = c to 6e-32 (V3W W4a); AC9 |
| Primary CMB (QX15 grader, CLASS ncdm) | | computed | **FAIL** | chi2_PA 6522.0 / 6404.8, Delta +2716 / +2599 vs line 9 (QX15's cold component: -64.7). h fixed by a0 (0.672 / 0.674); the relic also adds Delta N_eff ~ 1. Fit stopped at maxfev 120 on the omega_b bracket edge 0.0215 (disclosure 7). Angus 2009's PASS used a free H0 and Lambda [lit, PROVISIONAL]; LCDM-like background = COMPARISON-ONLY |
| CMB lensing | | HC1 G9 FAIL | **FAIL** | chi2 166-194 vs 18.48 (linear, no a0 term; free streaming, k_1/2 ~ 0.04 h/Mpc) |

**Overall: nuHDM does NOT pass every column EW1 has.** On the framework's terms it fails groups, ellipticals,
both rotating UDGs, Coma UDGs, KiDS G6 and the colour split, primary CMB and CMB lensing. It fails X-COP and the dSphs as a
prediction, while only being consistent with them. EW1 columns not graded here keep EW1's R22 cells: galaxy lensing
UNGRADED, wide binaries OPEN, Bullet PASS [lit], growth FAIL [lit], BBN TENSION [lit], causality UNGRADED, a0 tie BY_HAND.

## 3. Known answers and MUTATE

| Check | Result |
|---|---|
| KA1 M_f = 0 vs GB1 L0 X-COP mean/rms | +0.467499 / 0.476306 and +0.434523 / 0.444157: \|d\| 0 PASS |
| KA2 rho_TG vs closed form | \|d\| 0 PASS |
| KA3 SPARC L0 Z, rms | \|d\| 0 PASS (after disclosure 1) |
| KA4 UD1/UD2 law chi2 | 843.596 / 68.991 and 995.839 / 132.472, exact PASS |
| KA5 KiDS G6 with no fermion | 0 PASS |
| KA-CMB CLASS cold at QX15 canonical theta | 3741.25 vs 3741.08 (+0.17, line 5) PASS |
| **M1 m x 0.5 (5.57 eV)** | **does NOT bite on X-COP: still 6/7 consistent** (m_min <= 3.3 eV). Frozen expectation wrong: **NO POWER** for the phase-space bound at X-COP's radii (>= 0.1 R500 mean). Groups unchanged (they fail by C-a). Ellipticals fail at both masses |
| M2 no fermion | X-COP C 0/7 (every cluster fails phase space with rho_TG -> 0), groups 1-4/20; the harness gives GB1 L0's +0.468 / +0.435: **BITES** |
| Rerun | ew4_static.out and .json byte-identical |

## 4. Disclosed (post-freeze)

1. **a0 precision.** The first run used the rounded footing a0 (9.3603e-11 / 1.1312e-10). KA3 then FAILED at 4e-7 vs 1e-9,
   and the run stopped before grading. EW4 now uses QX5/GB1's full-precision values (9.360325e-11 / 1.131204e-10); KA
   passes exactly. No graded number existed before the fix.
2. **X-COP is 7 clusters, not 12.** GB1's loader keeps only the 7 X-COP clusters with stellar-mass files (35 points);
   HC1's criteria said "12 clusters" and EW4's criteria copied it. The literal line ">= 10 of 12" cannot be met. The
   criteria named it as "the GB1 groups' 80 % count line". On 80 % of 7, 6/7 PASS. The 5 dropped clusters, run with gas
   only (which over-estimates M_req), are 5/5 consistent; reported only.
3. **M1 did not bite** (section 3). The criteria expected the halved mass to fail clusters; on X-COP it does not. The
   phase-space bound starts to bind on X-COP only below m ~ 3.3 eV. Angus's reported core failures lie inside 0.1 R500,
   which X-COP's graded radii only see as a mean.
4. **KiDS G6 reading:** HC1's solver needs R_sys; EW4 used each bin's largest LE radius (not stated in the criteria).
5. **Ellipticals have no per-point mass error** in QX5's loader (Humphrey mass models), so err = 0, as the criteria
   stated. The C-b excess is 2.3-49x, so the label does not hinge on it.
6. Disk: the first full run's JSON write hit "no space left" (shared disk at 100 %). This lane's temp worktree was
   removed and the run repeated; outputs verified byte-identical on a second rerun.
7. **Primary CMB fit not converged.** Nelder-Mead used its full 120 evaluations per footing (as frozen), and both best
   points sit on QX15's omega_b bracket edge (0.0215), with tau near 0.10. The best chi2 fell from about 6600 to
   6400-6520 over the run. A gap of +2600 against a line of 9 is not one a longer fit plausibly closes, but the number
   is an upper bound on the minimum, not the minimum.

Kappa = 1/2 FITTED; not theory closed.
