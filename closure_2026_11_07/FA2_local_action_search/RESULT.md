# FA2: fresh-eyes search for a new LOCAL action. All three graded candidates FAIL, both footings

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. Footings graded separately, never pooled.

- Ideas: IDEAS.md (8 candidates; first draft reviewed by an independent adversarial read, which caught the C2
  Lagrangian; corrected before any number).
- Criteria: FROZEN_CRITERIA.md, committed and pushed alone (origin 614f4404cb). Amendment A1 (KA-ell only, after the
  first run stopped at KA with nothing graded; f390cd8651 local): the deep known answer was mis-stated (law S gives
  ell/r = 0.99505 at y 1e-4); the check moved to y 1e-8 plus an analytic match at 1e-4. The rerun's analytic match
  then caught a slip in my own known-answer derivative (d sqrt(u)/dg_N); the KA formula was fixed, not the code under
  test. Both stopped runs kept (run_main_KAstop.txt; the second is overwritten by the graded run, disclosed).
- Script: fa2.py (one thread, nice 15, a few minutes). Outputs fa2.json / fa2.out (run_main.txt), fa2_MUTATE.json /
  fa2_MUTATE.out (run_mutate.txt).

**Lane label: no local action found. C1 FAIL, C2 FAIL, C3 FAIL, both footings. C4-C7 die on derivation or the
record; C8 is WL1's switch (FAIL, stage 2).**

## Known answers (all PASS before grading)

GB1 L0 class means |d| 0 and all G1-G8 statuses equal gb1.json; KiDS 59-point base 0.141707 / 0.101597 = QX7 iter_4
(|d| 0); ell: point mass r/2 (Newtonian) 0.5000, deep 0.99995 (y 1e-8), y 1e-4 equals law S's analytic 0.995025;
SV5 r 74.7424 / 89.3630 read and reproduced by C2's own web code at L2 = infinity to 1e-6; WL1 r_pop (z 1)
3.75 / 4.32.

## Derivations (sympy, in fa2.py)

- **C2, natural local form:** QUMOND's action plus -(m^2/8 pi G)(Phi - psi)^2 gives, with EL residual 0,
  Phi'' = 4 pi G rho + [(nu - 1) psi']' and psi'' = 4 pi G rho - m^2 (Phi - psi). The mass never screens Phi's
  source; it only reshapes psi. **No local action for a screened phantom is in hand.** The target observable was
  graded as a necessary condition.
- **C3:** the linearised AQUAL flux has eigenvalue h'(x) along g and h/x across it. Any two-branch h has an interval
  with h' < 0 (Rolle), where the static operator is not elliptic (radial only). Witness h = x^2/(1+x) + x e^{-4 ln^2 x}
  falls on x 1.29-1.84.
- **C4:** on a flat curve d(lap psi)/dr = -2 g/r^2, so a polynomial (div A)^2 L2^2 term corrects the balance by
  -2 beta L2^2 / r^2: it acts at small r only (Lstar's class).

## C1: any phantom multiplier F of the local field length ell (absolute-scale key, never graded before)

Field lengths (canonical, kpc): SPARC 0.13-1.1e4, X-COP 386-3.5e4, groups 536-3.0e4, KiDS lenses 12-2.8e3,
Coma UDGs 49-215, ellipticals 4.6-29. X-COP's ell overlaps KiDS's and the groups'; the UDGs read galaxy-like.

Oracle (smallest boost that still passes X-COP's mean; t 0.875 / 0.860): F_gen 2.5-5.0 in X-COP's bins.

| ell bin (canonical) | F_gen | KiDS pts, mean D vs law | groups f*0, mean D |
|---|---|---|---|
| 251-398 kpc | 4.82 | 6, +0.246 | 0 |
| 398-631 kpc | 4.97 | 6, +0.208 | 2, +0.472 |
| 631-1000 kpc | 4.54 | 6, +0.229 | 6, +0.493 |
| 1000-1585 kpc | 4.14 | 3, +0.147 | 7, +0.412 |
| 1585-2512 kpc | 2.94 | 5, +0.137 | 11, +0.315 |

| Row | canonical | alt |
|---|---|---|
| K-G6 KiDS shift (line 0.05) | **+0.283 FAIL** | **+0.260 FAIL** |
| G1 SPARC | PASS (rms 0.1456, line 0.1457) | PASS (0.1423 / 0.1425) |
| G2 X-COP | PASS by construction (+0.050) | PASS (+0.050) |
| G3 groups | **FAIL** 2/20, 0/20 (median -0.12 / -0.28: over-boosted) | **FAIL** 2/20, 0/20 |
| G4 ellipticals, G5 UDGs, G6 dSphs | FAIL (= L0; ell below X-COP's range) | FAIL |
| G7 KiDS split | PASS (R +0.062) | PASS (+0.070) |
| G8 Solar System | PASS | PASS |
| W web | **FAIL**: F = 1 there gives L0's 74.7; any variant keeping F >= 1 inside R_ms gives >= r_pop 3.75 | FAIL (89.4; >= 4.32) |

**Label C1: FAIL (K-G6, G3, G4, G5, G6, W).** It is a class statement for every F(ell): KiDS isolated lenses at the
same field length sit +0.14-0.25 dex above the law, X-COP needs F ~4.5-5, and the groups at the same ell need less
than X-COP. No function of ell serves all three. MUTATE M1 (X-COP need set to 0) gives F = 1 and K-G6 shift 0
(PASS); M2 Newton fails G1 and K-G6 (-1.58 / -1.62): bites.

## C2: phantom screened beyond L2 (necessary-condition grade)

Web ladder r(L2) on SV5's field, canonical / alt: inf 74.7 / 89.4; 30 Mpc 70.1 / 83.8; 10 Mpc 45.9 / 54.5;
3 Mpc 7.18 / 8.17; 1 Mpc 1.51 / 1.57; **0.3 Mpc 1.042 / 1.047**; 0.1 Mpc 1.005; 0.03 and 0: 1. Monotone. L_max =
0.3 Mpc.

At L_max (the most generous range the web allows):
- **K-G6: -0.292 / -0.292 FAIL** (line 0.05). KiDS lenses keep 2-100 % of their phantom (F 0.024-0.997).
- G1 SPARC PASS (rms 0.1360 / 0.1325). Discs sit inside 0.3 Mpc.
- G2-G7 stay at L0's FAIL (screening only lowers the phantom). G8 PASS.

**Label C2: FAIL (K-G6, G2-G7; natural local form does not screen).** The web needs the phantom gone by about
0.3 Mpc; KiDS needs it to about 3 Mpc. MUTATE (L2 = 0: r = 1 and K-G6 -1.58 / -1.62 FAIL; L2 = inf: shift 0): bites.

## C3: two static branches (S-shaped h), branch chosen per point most favourably

Delta_up(y) was fitted per y bin on the hot classes (0.19-0.58 at y 0.01-0.6; 1.11 / 1.14 in the deepest UDG bin).
Every point then took whichever branch fits it better. That is more freedom than any history can give.

| Row | canonical | alt |
|---|---|---|
| G1, G2, G4, G6, G8 | PASS | PASS |
| G3 groups | **FAIL** 8/20, 11/20 (needs >= 16 both) | **FAIL** 8/20, 14/20 |
| G5 Coma UDGs | **FAIL** +0.626 (+2.39 sigma_U) | PASS +0.340 |
| G7 KiDS split | PASS | **FAIL** (R +0.158) |
| K-G6 | PASS (+0.006) | PASS (0.000) |
| WP | **FAIL** (radial coefficient h' < 0 on the falling segment) | FAIL |
| W web | **FAIL** (lower branch = law, 74.7; >= r_pop 3.75) | FAIL (89.4; >= 4.32) |

**Label C3: FAIL (G3, G5 canonical, G7 alt, WP, W).** Even with per-point branch choice and a free upper value per
y bin, the groups do not fit two values at fixed y. MUTATE M1 (groups planted on the two-valued solution) gives G3
20/20 on both footings; M2 Newton fails G1: bites.

## What FA2 says

1. **An absolute length is no key.** At the same field length, KiDS lenses, groups and X-COP need different
   boosts, and the web has the largest length of all.
2. **Screening by range cannot split hosts from the web.** The web allows at most ~0.3 Mpc and KiDS needs ~3 Mpc,
   a factor of 10. The natural local completion does not screen at all.
3. **Two values per y are not enough** for SPARC, groups and X-COP together. The two-branch action is also ill-posed
   on its falling segment.
4. Together with the record (single-valued nu QX2, shape keys FA1/KT, stress keys DX1, the mu-pincer X57, WL1),
   no local static term graded so far carries the residue or opens the web. What is left is nonlocal / history
   (FA3) or a change in the source. That is a reading, not a theorem.

## Disclosed

- K-G6 is graded in the pointwise reading; the projected 4 G DeltaSigma reading was not computed.
- ell for UDGs and dSphs uses the quasi-Newtonian EFE estimate frozen in §2; groups use a two-point slope.
- The C2 shell quadrature reproduces the unscreened force to 0.2 % (F 0.998 at L2 = 1e6 Mpc); SPARC's max F 1.005
  is that quadrature error, not a rise above 1. No label is near it.
- C2's web projection holds B(k) constant beyond the grid's k_max 0.2 /Mpc (SV5's convention). Screening raises B
  there, so r and L_max lean generous. The K-G6 FAIL is therefore conservative.
- C3's per-point branch choice uses the observed offset, so it is an upper bound on any history, not a prediction.
  Its alt G5 PASS and canonical G7 PASS come from that freedom.
- C1's G7 PASS comes from the early lenses' larger ell; it does not offset the K-G6 FAIL.

Kappa = 1/2 FITTED; not theory closed.
