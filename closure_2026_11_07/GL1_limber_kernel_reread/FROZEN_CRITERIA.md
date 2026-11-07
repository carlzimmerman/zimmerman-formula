# GL1 frozen criteria: re-read of every CMB-lensing shape label that rests on QX3 iter2's `limber_ratio`, with the k^-4 restored

Frozen before any GL1 script or GL1 number (CK4's reported kernel numbers, ea06286d99, are the only ones already seen and
are listed in section 3 as such). Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Fix-forward: a moved label is
REPORTED here, not rewritten in its lane; the owner decides. No other lane's file is edited. The independent audit of the
kernel claim is GL2 (other session, own code); GL1 shares no code with it. Cold dark energy, never dark matter; no particle.
One thread, RSS < 1 GB, no downloads.

## 0. The claim and the kernel switch

- `iter2.limber_ratio(M, H0, kgrid, zgrid, R)` returns S(L) = C_L[P R^2] / C_L[P] with per-z weight
  w_j / chi_j^2 = ((chi*-chi)/(chi chi*))^2 (1+z)^2 / H / chi^2. The lensing-potential power is P_Psi ∝ (1+z)^2 P_delta / k^4
  with k = (L + 1/2)/chi, so the correct weight carries an extra (chi/(L + 1/2))^4 (the WG1-WG6 engine carries it and checks
  it analytically, K3 there).
- GL1 replaces the module attribute `iter2.limber_ratio` (and KD1's own exec'd copy, `Q3["limber_ratio"]`) by one function
  with an exponent n: weight x (chi/(L + 1/2))^n. **n = 0 is the record's kernel; n = 4 is the corrected one; n = 2 is the
  MUTATE.** Everything else (grids, solvers, CLASS models, PR4 likelihood, A_s refit, lines chi^2 <= 18.48 and
  Delta chi^2 <= 4) is the lanes' own code, exec'd or imported read-only.

## 1. Labels re-read and the statistic for each

| # | Label (record) | Statistic re-read | Label MOVES iff (n = 4) |
|---|---|---|---|
| L1 | QX3 iter1: AC2q's clock, FAIL (no-go) | none: iter1's statistic is (k_J/k)^2 on (L, z), no Limber weight (checked in the source) | never; stated, not run |
| L2 | QX3 iter2: FAIL (no window: mu_min 3.98e4 > mu_max 79.4) | Delta chi^2 on iter2's 26-point mu grid at all 8 corners (iter2's growth_ratio, its CLASS runs); mu_min per corner and worst; mu_max (G3, kernel-free) taken from iter2.json | mu_min_worst (n = 4) <= mu_max_best 79.43 |
| L3 | QX3 iter3: FAIL (class no-go; 35 cells pass G3'/G4', best Delta chi^2 92.59) | Delta chi^2 of the same 35 (beta, mu0) cells via iter3's g2 | any of the 35 has Delta chi^2 <= 4 |
| L4 | QX7 iter_3: FAIL (no window; 31 analytic cells, closest 17.87) | Delta chi^2 of the 31 evaluated cells via iter_3's g2gen | any of the 31 has Delta chi^2 <= 4 |
| L5 | QX7 iter_4: FAIL (clusters) [0/270 both footings]; G2' window 270 of 857 | Delta chi^2 of all 857 evaluated cells via iter_4's g2gen; new window; cluster pass of each new member read from qx7_iter4.json `cluster_vs_lambda0_galaxyok` (kernel-free, lambda_0 only) | any new window member has X_pass AND groups_strict on both footings |
| L6 | KD1: FAIL; mu_J 2.51e4 (G9a Jeans line), mu_K* = max(mu_B 8.89e6, mu_J); converse rows at mu 0.1 / 79.43 fail B1a, B1b and G9a | KD1's jeans_rows on its own grid (36 log points 1-1e7 plus 0.1, 79.43), both footings (QX15 backgrounds); mu_J; G9a Delta chi^2 at 0.1 and 79.43 | mu_K* changes (it cannot unless mu_J > mu_B), OR the converse block list loses G9a (reported as a moved sub-label; B1a/B1b are kernel-free and stay) |
| L7 | CE2: GL PASS at C1-C4 (dchi2 0.31 / 0.13 / 3.12 / 0.27); M3 (lambda_* x 10 at C1) bites, dchi2 265 | the four cells and M3 via iter_4's g2gen | M3 no longer bites (dchi2 <= 4 and chi^2 <= 18.48): CE2's GL label becomes NO VERDICT; CE2's overall FAIL (GX, GG, GB) is kernel-free and stays |
| L8 | CK4: GL NO VERDICT (M1 3000 km/s does not bite) | recorded in ck4.json (`GLc`) and ck4_MUTATE.json; not re-run | M1 bites at n = 4 (it did not: chi^2 9.19, +0.62; already reported) |
| L9 | QX10 iter_1: J1 (late lensing bound on TT, Delta chi^2_TT <= 1 from max\|1 - S\| over L 2-2500) per cell C1-C4, with its own copy of the same Limber formula (`Sfull`) | J1 Delta chi^2_TT and max\|1 - S\| per cell, jcheck's own code with the weight x (chi/(L + 1/2))^n; jcheck.json is not overwritten (GL1 writes its own) | any cell's J1 changes PASS/FAIL |
| L10 | SE1 arm (a): FAIL (= KD1 exactly; SE1's KA2 reproduces KD1's G9a rows to 1e-6) | no separate run: arm (a)'s G9a is KD1's (L6); its label follows L6 | as L6 |

- **Scope (Theory completion, final):** the sector side only. The web line (SV5, WL1, NA1, FA3, EW2, OQ1/2, QX27-29, QX31,
  LD1) is GL3 (Field equations session) and is not re-read here. SE1's arm (b) also calls the kernel; it is not in GL1's
  scope and is listed only.
- **WG1-WG6** (the a0 law on the linear web, "FAIL (shape)") use a separate pipeline: WG1's own Limber engine carries the
  (chi/(L + 1/2))^4 factor (wg1.py `limber_core`; WG2-WG4/WG6 graders reuse it) and each checks it analytically against
  4 chi_s / [3 (L + 1/2)^4] (K1 / K3 there, tolerance 1e-3). They are outside the claim; GL1 states this from the source
  and re-runs nothing there.
- **GATE (HOLD_KERNEL_REREAD_2026_11_07.md):** no label moves before GL2 (independent from-scratch rebuild) reads
  CONFIRMED. GL1 computes now and reports each label as "WOULD MOVE / STANDS (held)". The record's labels are unchanged.

## 2. Known answers and MUTATE

- **KA0 (n = 0 reproduces the record to 0):** QX10 iter_1's J1 numbers (jcheck.json) to 1e-9; the patched function at n = 0 equals the original `iter2.limber_ratio` to
  1e-12 relative on a test R; and through it: iter2's Delta chi^2 rows at all 8 corners to 1e-9 absolute (and mu_min equal);
  iter3's 35 Delta chi^2 to 1e-9; qx7_iter3's 31 to 1e-9; qx7_iter4's 857 to 1e-9 (KA0 on L5 may be run on a declared
  subset of 60 cells, evenly spaced in the evaluated list, if the full set exceeds 20 min; the n = 4 re-read is on all 857);
  KD1's mu_J (both footings) equal to kd1.json; CE2's four cells equal to ce2.json. A KA0 failure makes that label NO
  VERDICT in GL1.
- **KA4 (the corrected kernel is right):** with n = 4 the absolute Limber C_L^pp shape on iter2's worst-corner CLASS model,
  divided by CLASS's own raw_cl pp and normalised at L 100, is within 3 % of 1 at L 20, 50, 200, 300, 400. With n = 0 it is
  not (CK4 saw 0.045-33).
- **MUTATE (n = 2):** the same shape check must FAIL (some L off by more than 3 %) AND differ from n = 0 and from n = 4 by
  more than 3 % at some L. Outputs gl1_MUTATE.json / .out.

## 3. Already seen before this freeze (CK4, ea06286d99)

CE2's four cells at n = 4: Delta chi^2 0.00 (chi^2 8.57); CK4 GL rows at n = 4: +0.01 to +0.07; M1 at n = 4: +0.62. These are
recomputed in L7 and quoted from ck4.json for L8.

## 4. Outputs

gl1.py writes gl1.json / gl1.out (and gl1_MUTATE.*). RESULT.md: old vs new per label, MOVES / STANDS, with the size.

Kappa = 1/2 FITTED; not theory closed.
