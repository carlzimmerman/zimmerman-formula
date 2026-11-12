# GL1: sector-side CMB-lensing labels re-read with the Limber k^-4 restored. 3 labels MOVE (QX3 iter3, QX7 iter_3, QX10 iter_1), 1 gate (CE2's GL) MOVES, KD1/SE1 wall 1 HOLDS

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (3ed2133753), pushed alone before any
script. Script: gl1.py (main 452 s, peak RSS 616 MB; MUTATE 2 s). Outputs: gl1.json / gl1.out, gl1_MUTATE.*, run_main.txt,
run_mutate.txt. Every lane's code is imported or exec'd read-only, and no other lane's file is written.

**Moved labels are REPORTED here, not rewritten in their lanes. The owner decides.**

- **Gate status.** The hold (HOLD_KERNEL_REREAD_2026_11_07.md) is open: GL2 (EV1 session, d0c3692fc6, own code) read
  CONFIRMED. The script prints "WOULD MOVE / STANDS" because it was written under the hold. This file reads those as
  MOVES / HOLDS.
- **The error.** QX3 iter2's `limber_ratio` omits the lensing potential's k^-4 = (chi/(L + 1/2))^4.
  - With n = 4 (restored), the Limber C_L^pp shape over CLASS's own pp is 1.005 / 1.006 / 1 / 0.991 / 0.984 / 0.980 at L 20 /
    50 / 100 / 200 / 300 / 400.
  - With n = 0 (the record's kernel) it is 0.045 / 0.239 / 1 / 5.26 / 15.0 / 33.0.
- **Footings.** Every GL statistic here is a-priori footing-free, because a0 does not enter. Where a lane ran both footings
  (KD1, QX10 iter_1), both are shown.

## Per label: old vs corrected

| # | Label (record) | Old | Corrected (k^-4) | Verdict |
|---|---|---|---|---|
| L1 | QX3 iter1, AC2q clock FAIL (no-go) | (k_J/k)^2 <= 0.0065 | no Limber weight in the statistic | **HOLDS** (kernel-free) |
| L2 | QX3 iter2, FAIL (no window: mu_min > mu_max) | mu_min 2.51e4 / 3.98e4 per corner, worst 3.98e4; mu_max 79.43 | mu_min **631** at all 8 corners | **HOLDS**: 631 > 79.43. The gap shrinks from x500 to x7.9 |
| L3 | QX3 iter3, FAIL (class no-go; 35 cells, best dchi^2 92.59) | best 92.59, 0/35 pass | best **2.78**, 1/35 passes | **MOVES** to PASS (member found): beta 0.80, mu0 1259 Mpc^-1 (record 199.4) |
| L4 | QX7 iter_3, FAIL (no window; 31 cells, closest 17.87) | closest 17.87, 0/31 | dchi^2 -0.05 to +0.03, **31/31** | **MOVES**: the G2' window holds every analytic cell. iter_3 graded no cluster rows for them |
| L5 | QX7 iter_4, FAIL (clusters) [0/270 both footings] | G2' window 270 / 857 | window **857 / 857** (dchi^2 <= 0.028); 23 lambda_0 values; cluster pass on both footings at none | **HOLDS**: FAIL (clusters) [0/857]. Clusters are kernel-free |
| L6 | KD1 FAIL; G9a mu_J 2.51e4; mu_K* = max(mu_B 8.89e6, mu_J); converse G9a fails at mu 0.1 / 79.43 | mu_J 2.51e4 (both footings); converse dchi^2 312.3 / 857.5 (canonical), 314.7 / 857.6 (alt) | mu_J **631** (both); mu_K* = mu_B 8.89e6 unchanged; converse dchi^2 667.5 / 309.0 (canonical), 667.3 / 309.0 (alt) | **HOLDS**, sub-labels included: the converse G9a still fails |
| L10 | SE1 arm (a) FAIL (= KD1; SE1 KA2 reproduces KD1's G9a rows) | as L6 | as L6 | **HOLDS** |
| L7 | CE2: GL PASS C1-C4 (dchi^2 0.31 / 0.13 / 3.12 / 0.27); M3 (lambda_* x 10 at C1) bites, dchi^2 265.4 | as left | C1-C4 dchi^2 0.000; M3 chi^2 8.57, dchi^2 0.00, and GF passed in the record | **GL gate MOVES** to NO VERDICT: M3 no longer bites, so GL has no power. CE2's overall FAIL (GX, GG, GB) is kernel-free and **HOLDS** |
| L8 | CK4: GL NO VERDICT (M1, 3000 km/s, does not bite) | M1 dchi^2 +2.98 | M1 dchi^2 +0.62 (quoted from ck4_MUTATE.json); primary rows +0.01 | **HOLDS** |
| L9 | QX10 iter_1: NO VERDICT on all four cells ("CDM proxy invalid": J1 FAIL) | J1 dchi^2_TT 4.30 / 1.05 / 77.2 / 3.47 (C1-C4); max \|1-S\| 0.124 / 0.061 / 0.525 / 0.111 | J1 1.1e-8 / 5.5e-9 / 9.3e-8 / 1.5e-8; max \|1-S\| <= 1.8e-5 | **MOVES** to PASS for C1-C4 by the lane's own rule: J0 passed, J1 now passes, and both footings pass L1 / L2 / L3 / C-wd |

## What the re-read says

- **The corrected kernel is stricter, not looser, on slow sectors.** On QX3 iter2's mu grid at the worst corner, compared
  with the record:
  - mu 1: dchi^2 1277 (record 336);
  - mu 63: 449 (779);
  - mu 251: 19.3 (1054);
  - mu 1000: 0.46 (1253).
  - So the Jeans line moves from 2.5e4 down to 631 Mpc^-1, and small mu fails harder.
  - The record's kernel was not uniformly lenient; it measured the wrong scales (z ~ 0.02-0.1, k ~ 1-3 /Mpc).
- **Wall 1 (KD1 / SE1 arm a) holds** because its binding side is BBN (mu_B 8.89e6), not CMB lensing.
  - On the CMB side alone, the galaxy-vs-lensing gap narrows from 2.5e4 / 79 (x316) to 631 / 79 (x7.9).
  - Galaxies still need mu_K <= 0.1 to 79. G9a at 79.43 is still dchi^2 309.
- **The late-switched cold dark energy (QX7 iter_3 / iter_4, CE2)** no longer meets the lensing shape at all at L <= 400.
  - Every analytic cell passes G2'.
  - Their labels still fail on clusters (iter_4, CE2), which is kernel-free.
- **QX3 iter3** gains one barotropic member: beta 0.8, mu0 1259 Mpc^-1, dchi^2 2.78. Its G3' (galaxies) and G4' (forest) were
  analytic passes in the record.
- **QX10 iter_1:** J1 was the only blocking row. The early-sector primary-CMB fit is now a PASS on all four cells by the
  lane's own rule. iter_1's other disclosures stand (not independent evidence; raw PR3 diagonal spectra).
- **WG1-WG6** (the a0 law on the linear web) used a **separate pipeline**. WG1's own Limber engine (`limber_core`) carries
  the (chi/(L + 1/2))^4 factor, and the WG2-WG4 / WG6 graders reuse it. Each checks it analytically against
  4 chi_s / [3 (L + 1/2)^4] to 1e-3. They are outside the error, and their "FAIL (shape)" is untouched.
- **Out of scope.** The web line (SV5, WL1, NA1, FA3, EW2, OQ1/2, QX27-29, QX31, LD1) is GL3 (Field equations session).
  SE1 arm (b) also calls the kernel and is listed only.

## Known answers and MUTATE

- **KA0, error re-inserted (n = 0).**
  - The patched function equals the original `limber_ratio` (max rel 0.0).
  - Through it, every recorded number is reproduced with max |d| 0.0: iter2's 8 x 26 rows and mu_min; iter3's 35;
    QX7 iter_3's 31; QX7 iter_4's 857 (all, not a subset); CE2's four cells and M3 (265.41); KD1's 38-row G9a grids
    (both footings); QX10 iter_1's J1 (all four cells).
  - **PASS.**
- **KA4.** n = 4 matches CLASS within 3 % at every L, and n = 0 does not. **PASS.**
- **MUTATE n = 2** (wrong power): shape 0.299 / 0.494 / 1 / 2.56 / 4.64 / 7.22. It fails the 3 % check and differs from both
  n 0 and n 4. **BITES.**

## Limits

- **Same framework, separate code.** GL1 reuses each lane's own solvers and grids. The kernel itself was checked
  independently by GL2 (from-scratch code, d0c3692fc6), not by GL1.
- **Grid ceiling.** The Limber ratio is still truncated at the lanes' kgrid maximum, 10 /Mpc, exactly as recorded. At
  L <= 400 this cuts only chi < 40 Mpc (z < 0.01).
- **Lensing in TT (J1).** QX10 iter_1's J1 remains the lane's conservative bound, not a Boltzmann-code lensing step.

Kappa = 1/2 FITTED; not theory closed.
