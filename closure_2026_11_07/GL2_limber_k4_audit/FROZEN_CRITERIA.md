# GL2 frozen criteria: independent audit of CK4's post-freeze finding (QX3 iter2 `limber_ratio` omits k^-4)

Frozen and committed alone, before any GL2 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
Audit lane (registered in CLOSURE_REGISTER v1.1, 9760b1acdf). One thread, < 1 GB, no download.

## Claim under audit (CK4, ea06286d99, RESULT section 3)

QX3 iter2's `limber_ratio` weights each z slice by (chi*-chi)^2 (1+z)^2 / (chi^2 chi*^2 H) / chi^2 times P_delta, and
omits the lensing potential's 1/k^4 = (chi/L)^4. Its Limber C_L^pp, normalised to CLASS at L 100, runs
0.045 / 0.239 / 1 / 5.26 / 15.0 / 33.0 at L 20 / 50 / 100 / 200 / 300 / 400. With k^-4 restored it runs 0.98-1.006.

## Known before this freeze (not blind)

CK4's numbers above; the record background (QX3 iter2's worst G1 corner, used by iter_3, iter_4, CE2, CK4):
omega_b 0.0215, omega_d 0.11958060485606123, H0 65.0, n_s 0.95, A_s 2e-9, tau 0.06, N_ur 3.046, T_cmb 2.7255.

## Footings

a0 does not enter the linear background (QX3 iter2 FROZEN_CRITERIA, line 54). So the footing background is the same
record background on canonical (a0 9.3603e-11) and alt (1.1312e-10). Each footing is graded on it and reported
separately, never pooled. Reported, not graded: a second background (QX3's G1 corner omega_b 0.0230, H0 75, n_s 0.98,
at its own omega_d_best from iter2.json).

## Own code (gl2.py; imports nothing from QX3, QX7, CE2 or CK4)

- CLASS (classy) with 'tCl,lCl,mPk', linear (no non-linear correction), lensing potential C_L^pp from raw_cl.
- Limber, written from the definitions: Psi = Weyl potential, Poisson
  k^2 Psi = -(3/2) Omega_m0 H0^2 (1+z) delta_m (c = 1, Mpc units), lensing potential weight 2 (chi*-chi)/(chi chi*):
  C_L^pp = int dchi [2 (chi*-chi)/(chi chi*)]^2 / chi^2 * (9/4) Omega_m0^2 H0^4 (1+z)^2 P_m(k, z) / k^4, at k = (L+1/2)/chi.
  P_m from CLASS pk_lin (total matter). Integrate in chi from the full domain z 1e-3 to 1088 (z_max_pk set to cover it),
  k from CLASS's range, and P = 0 outside.
- Comparison statistic: Q(L) = [C_L^Limber / C_L^CLASS] / [same at L 100], every integer L in 20-400.
  The tolerance line is max |Q - 1| <= 0.02 (2 % shape).

## Steps

1. Kernel K (k^-4 present, full domain): Q per footing. Also reported: Q on QX3's domain (z 0.02-20, k 1e-4-10 /Mpc).
2. MUTATE M1 (separate output): the same code with the 1/k^4 dropped, on QX3's own domain (z 0.02-20, k 1e-4-10 /Mpc,
   the grids iter2.py uses). It must leave the 2 % line, and reproduce CK4's frozen-kernel run: each of Q at
   L 20 / 50 / 200 / 300 / 400 within 10 % of 0.045 / 0.239 / 5.26 / 15.0 / 33.0.
3. Reading: read iter2.py's `limber_ratio` line by line and state whether the per-slice weight contains (chi/L)^4 (or
   1/k^4 in any form). This is graded as PRESENT or ABSENT, with the line quoted.

## Known answers (must pass, else UNDECIDED)

- KA1: the CLASS background gives Om_b0 0.05089 and Om_d0 0.28303 (CK4's print) to 1e-4.
- KA2: the absolute Limber/CLASS ratio at L 100 for kernel K is within 5 % of 1 (constants are right, not just shape).

## Labels (per footing; then the lane)

- CONFIRMED: KA pass, kernel K holds the 2 % line, M1 leaves it and reproduces CK4's run (step 2), and the reading is ABSENT.
- REFUTED: the reading is PRESENT, or M1 holds the 2 % line (dropping k^-4 does not matter).
- UNDECIDED: anything else (for example kernel K fails 2 %, a KA fails, or M1 leaves the line but does not reproduce CK4's run).

The lane label is CONFIRMED or REFUTED only if both footings agree; otherwise UNDECIDED.

## Not done here

No re-read of the lanes that use the kernel (QX3 iter1-3, QX7 iter_3/iter_4 G2', KD1 mu_J, CE2 M3). That is GL1's task.
