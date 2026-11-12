# CK1 RESULT: the kicked "cold dark energy" carrier at today's needs. FAILS (rows) at every v_k; binding gate T

**Label line:** FAILS (rows) at every v_k in {500, 525, 550, 575, 600, 625, 650} km/s on both footings; binding gate
T (SPARC high-mass tail, every v_flat >= 250 km/s galaxy, every RM cell); also FAIL G1, G3, G5, G6 at every kick and
G4 at 500-550 (canonical) / 500-600 (alt); G2 X-COP, MW and G7 NO VERDICT (MIXED over the RM cells); G8 PASS;
G9 PENDING GL1/GL3; Bullet OPEN. Residue label: FAILS RESIDUE at every kick.

Criteria f6f15f9e05 (committed alone), amendments A1 ecde71eaff, A2 17dbf6d9e8 (both before any graded number) and
A3 9f4dfee349 (POST-FREEZE, after the first full run, before this rerun). Script `ck1.py`; outputs `ck1.json` /
`ck1.out` and `ck1_MUTATE.json` / `ck1_MUTATE.out`; the first full run's log `ck1_FIRSTRUN_preA3.out` (unedited).
Adopts nothing. Kappa = 1/2 FITTED; not theory closed. The kick v_k is hand-set (CK2 found no release term), so even
a pass could only have read "CANDIDATE ON G1-G8 WITH A POSTULATED KICK".

**Reference used:** CK1's own resolved release model RM (criteria section 4): the a0 law at today's footings
(9.360e-11 / 1.131e-10 m/s^2, Lstar 21.7 / 22.9 pc), parents = KD1's own-terms capture C_f = 4.1110 / 4.1121 of the
on-disk baryons, one isotropic kick at release, retention by escape to the Hubble-flow radius in the law's field,
retained daughters orbit-averaged. Four bracket cells: release potential (law field of (1 + C_f) M_b) or after-loss
potential (law field of M_b), x z_F in {0, 2}. A row is PASS / FAIL only if all four cells agree. L388's retention is
LCDM-referenced and enters only as a labelled reading (A3).

## Known answers and MUTATE (all PASS / bite)

- KA1, KA2 (code checks only, A3): L388's bin medians recomputed from its per-halo JSON, |d| = 0; top 0.79-0.85, low
  0.17-0.34. KA3: GB1 L0 through CK1's candidate with f = 0, |d| = 0 on G1-G8. KA4 (A2): NA2's baryon-traced X-COP at
  KD1's need, mean 0, rms 0.0818 / 0.0835. KA5: RM at v_k = 0 returns f = C_f exactly. KA6: XR13's X-COP
  M(<1 Mpc/h) 5.03e14-8.69e14 Msun reproduced.
- M1 (RM, v_k = 0): every X-COP cluster F = 4.1110 / 4.1121 (KD1's capture); L388's v_k = 0 runs read 4.118 / 4.119.
  HOLDS.
- M2: v_k = 2000 km/s does NOT empty X-COP in the law's field: f_ret = 1.00 in all 7 clusters, v_esc(r_F) 4810-6021 /
  5046-6309 km/s. G2 still fails (+0.167 / 0.208 and +0.132 / 0.181): the daughters are bound but puffed outward.
  Bite at 20000 km/s: f_ret 0.000, G2 +0.467 / +0.435 (the plain law). BITES.
- M3: kick off, f = C_f > SPARC cap: T fails. BITES.

## Gate table (canonical / alt; each cell is the 4-cell rule; numbers are release-z0 / after-loss-z0 cells)

| v_k | G1 SPARC (Z, rms; line ~0.146) | T tail: max f (cap 0.33 / 0.19); n over cap of 10 | G2 X-COP (mean / rms) | G3 groups (pass f*0, f*1 of 20) | G4 ell | G5 UDG | G6 dSph | G7 KiDS | G8 | MW (dKz, dv_c, dlog g inner) |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | FAIL / FAIL: -0.231, 0.346 and -0.083, 0.197 / alt -0.258, 0.358 and -0.115, 0.209 | FAIL / FAIL: 3.86 and 2.68 (10/10) / 3.88 and 2.82 (10/10) | NV / NV: +0.002/0.095 pass, +0.029/0.106 fail / -0.023/0.098 pass, +0.001/0.102 fail | FAIL / FAIL: 4,1 and 1,1 / 5,1 and 2,1 | FAIL / FAIL | FAIL / FAIL (+0.999 / +0.956) | FAIL / FAIL | NV / NV | PASS / PASS | NV / NV: 14.5, 99 km/s, 0.42 fail; 3.4, 16.3, 0.12 (dlog g fails, dKz pass) |
| 525 | FAIL / FAIL | FAIL / FAIL (10/10 every cell) | NV / NV (release pass, after-loss fail) | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL | NV / NV | PASS | NV / NV |
| 550 | FAIL / FAIL: -0.212, 0.329 and -0.059, 0.175 / -0.240, 0.341 and -0.091, 0.186 | FAIL / FAIL: 3.78 and 2.29 / 3.81 and 2.44 (10/10) | NV / NV: +0.005/0.096 pass, +0.036/0.110 fail / -0.020/0.098 pass, +0.008/0.104 fail | FAIL / FAIL: 4,1 and 1,1 / 5,1 and 2,1 | FAIL / FAIL | FAIL / FAIL | FAIL / FAIL | NV / NV | PASS | NV / NV: 12.8, 89, 0.38; 1.8, 8.3, 0.073 |
| 575 | FAIL / FAIL | FAIL / FAIL | NV / NV | FAIL / FAIL | NV / FAIL | FAIL / FAIL | FAIL / FAIL | NV / NV | PASS | NV / NV |
| 600 | FAIL / FAIL | FAIL / FAIL | NV / NV | FAIL / FAIL | NV / FAIL | FAIL / FAIL | FAIL / FAIL | NV / NV | PASS | NV / NV |
| 625 | FAIL / FAIL | FAIL / FAIL | NV / NV | FAIL / FAIL | NV / NV | FAIL / FAIL | FAIL / FAIL | NV / NV | PASS | NV / NV |
| 650 | FAIL / FAIL: -0.178, 0.296 and -0.021, 0.148 / -0.206, 0.308 and -0.052, 0.154 | FAIL / FAIL: 3.56 and 1.55 (9/10 after loss) / 3.61 and 1.71 (10/10) | NV / NV: +0.012/0.098 pass, +0.053/0.119 fail / -0.014/0.099 pass, +0.023/0.109 fail | FAIL / FAIL: 2,1 and 1,1 / 4,1 and 1,1 | NV / NV | FAIL / FAIL | FAIL / FAIL | NV / NV | PASS | NV / NV: 9.9, 68, 0.30; 0.33, 1.6, 0.018 |

z_F = 2 cells match z_F = 0 to within 0.003 dex on every row (`ck1.json`). Lines: T cap 0.3257 / 0.1937 (KD1);
MW dKz/2piG <= 4.4 Msun/pc^2, dv_c(R0) <= 8.63 / 16.02 km/s, dlog g(r <= 30 kpc) <= 0.057.

**Binding gate T.** In every cell, footing and kick, 9-10 of the 10 tail galaxies (ESO563-G021, NGC2841, NGC5005,
NGC5985, UGC02487, UGC02885, UGC02953, UGC06787, UGC11455, UGC11914) keep f = 1.5-3.9 of their baryons, 5-20 times
the SPARC cap. Escape speeds at r_F in the law's field are 740-900 km/s after loss and 1270-1480 km/s in the release
potential, above every kick graded. The Milky Way's v_esc(r_F ~ 6 kpc) is 550-640 (after loss) to 920-1040 km/s
(release), and it keeps f_ret 0.16-0.99.

**Coordinator rule (window closed from both ends), cell by cell.** G2 X-COP passes in exactly the cells where T and
MW fail hardest (release potential: X-COP mean +0.002 to +0.012 canonical with rms 0.095-0.098, while T reaches f 3.6-3.9
and MW dv_c 62-99 km/s). In the after-loss cells, where the galaxies retain least, X-COP fails (rms 0.102-0.120). The
formal flag in the JSON is False only because G2 is MIXED; no RM cell passes both X-COP and the galaxies.

## X-COP per cluster (v_k 550, mean residual dex, release-z0 / after-loss-z0; F = M_c/M_b at Mb_last's radius)

| cluster | canonical | alt | F (canonical, release) |
|---|---|---|---|
| A1795 | -0.007 / +0.028 | -0.031 / +0.000 | 3.82 |
| A2029 | -0.010 / +0.018 | -0.033 / -0.007 | 3.80 |
| A2142 | -0.049 / -0.021 | -0.073 / -0.048 | 3.80 |
| A2319 | +0.018 / +0.048 | -0.008 / +0.021 | 3.69 |
| A644 | +0.094 / +0.126 | +0.069 / +0.097 | 3.82 |
| A85 | -0.026 / +0.008 | -0.052 / -0.021 | 3.74 |
| ZW1215 | +0.014 / +0.046 | -0.013 / +0.015 | 3.83 |

Retention f_ret = 1.00 in every cluster at every kick (cluster escape speeds are thousands of km/s in the law's field).
Per bin (release z0, canonical 550): 0-0.25 R500 +0.085 (n 14), 0.25-0.5 +0.027 (7), 0.5-0.75 -0.086 (14): inside
the NA2 0.10 bin rule; alt 0.5-0.75 is -0.113, outside it.

**Profile against NA2's band.** Concentration M(<0.25 R500)/M(<0.7 R500), release z0, every kick: RM carrier
0.17-0.23, gas 0.16-0.24, HSE 0.21-0.30, stars 0.32-0.51. The kicked carrier traces the gas (within 0.02 in every
cluster), i.e. it sits on the gas edge of NA2's band, not near HSE where NA2 put the needed profile. Fixed-shape readings
at the graded amount (release z0, 550): baryon-traced passes (+0.040 / 0.092; alt +0.015 / 0.085), gas-traced fails
(rms 0.115 / 0.105), HSE fails (-0.057 / 0.109; alt -0.079 / 0.121), stars fail.

## Residue rows (SE2 95 % / UA1)

SPARC: NO VERDICT (FAIL on alt at 500); ellipticals FAIL every kick; bright M31 PASS (SE2's interval contains 0);
X-COP NO VERDICT (median F 3.7-3.8 vs SE2's [2.82, 3.98], MIXED over cells); groups FAIL / NO VERDICT; UA1 groups step
PASS (the carrier's median group offset is inside UA1's 95 % interval); T FAIL; MW NO VERDICT. Residue label: FAILS
RESIDUE at every kick (MW, SPARC, T, X-COP, ellipticals, groups).

## Reported rows (not graded)

- **Trigger mass (A1 c).** RM and L388 have no M_min. With M_min = 1e11 / 1e12 Msun on (1 + C_f) M_b, 88 / 136 of
  145 SPARC galaxies shed nothing and G1 fails harder; the MW sheds only at M_min 1e11.
- **L353 reading (carrier feels Newton only, release, z_F 0, v_k 550):** the tail still keeps f 1.6-3.4 and the MW
  f_ret 0.38. The September clearing (L376) came from Newtonian NFW shells with progenitor release, not from RM's
  baryon-traced parents.
- **L388 reading (LCDM-referenced, not evidence):** its top-bin amount with the RM shape gives X-COP +0.002 to
  +0.047 / rms 0.095-0.108 canonical; unit-consistent placement puts every X-COP cluster in L388's top bin
  (3.39e14-5.85e14 Msun/h; A2029, A2142, A3266 above 1.1 x the heaviest L388 halo, bracketed).
- **Retention curves for CK3:** `ck1.json` keys `single_shell_curve` (P(|v_p + v_k n| < v_esc), v_esc 100-3000 km/s,
  two sigma conventions, every v_k), RM per-system f_ret / v_esc(r_F) / r_F in every cell, and
  `L388_bin_vesc_proxy_kms`.

## Compute

One thread at nice 15. Main 526 s, peak RSS 682 MB; MUTATE peak 451 MB. No PM run (an L388-type box is several GB).

## Disclosures

1. **A3 is post-freeze.** The coordinator's relay of the paper session's sourcing (L388 inadmissible, old footings,
   1 Mpc/h aperture, Bullet, 5.4, kick hand-set) arrived after the first full run. That run graded X-COP and groups
   from L388's amounts. Its label was the same ("FAILS (rows) at every v_k; binding gate T"); its log is committed
   unedited as `ck1_FIRSTRUN_preA3.out`.
2. **Bug in the first run, fixed in the rerun:** the MW evaluation grid was unsorted, so rho_c(R0), Delta K_z,
   Delta v_c(R0), the dSph host densities and the carrier inside 9.58 AU were wrong there (they printed 0). The inner
   Delta log g was unaffected. The first run's MW FAIL at 500-550 rested on that row; after the fix MW is NO VERDICT
   (the after-loss cells pass Delta K_z and Delta v_c at 550-650 but fail Delta log g at 500-550).
3. **A2 (pre-number):** KA4's frozen reference quoted NA2's means at NA2's fitted F; at KD1's need the mean is 0.
   RM's v_k = 0 branch had a 2.5e-3 interpolation error; fixed. The first MUTATE launch stopped at KA, nothing graded.
4. **Model limits.** RM is spherical and static after release; parents trace the baryons (KD1's v_k = 0 state), not a
   hierarchical progenitor history; the escape boundary is the Hubble-flow radius of the law's mean dynamical density.
   These favour retention in deep, extended law potentials; the after-loss cells are the bracket's favourable end for
   clearing, and T fails there too.
5. **Coma (A1656) is not on disk;** the UDG host term uses A2319 as proxy (A1). G5 fails by about 1 dex in every
   cell, and UA1 already reads the UDG row NOT A TEST.
6. **Not graded here:** CK2 (release speed), CK3 (groups f-sigma slope), CK4 and G9 (CMB lensing, fsigma8, forest;
   QX3/SV5 numbers held under HOLD_KERNEL_REREAD), the Bullet (OPEN).
7. Commits went through a temporary index onto origin/main (no checkout, no rebase or force).

Kappa = 1/2 FITTED; not theory closed.
