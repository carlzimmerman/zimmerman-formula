# QX17D RESULT: field equations with the adopted Pi^6-blend stiffness. R1 FAIL, R2 CERTIFIED (both test stiffnesses)

Criteria: FROZEN_CRITERIA.md (78b03d2973), committed and pushed alone before any script or number. Script `qx17d.py`
(QX17's qx17.py with a general F); outputs `qx17d_{G,B,KA}.json/.out`. Adopts nothing. Kappa = 1/2 FITTED; not theory
closed. Footing-independent (an identity of the action).

## Label

**R1 FAIL (K3 only); R2 CERTIFIED, for G and for B.** The field equations of the action with a general stiffness F(Pi)
are QX17's with Pi_+ read as F'(Pi) everywhere (P equation, khronon equation, constitutive factor 1 + gamma_L F',
source J_P, curly D_m = d_m F' - F' d_m l), **and the stress-tensor term 2 F h_mn replaced by Pi F'(Pi) h_mn.** For the
raw F = Pi_+^2/2 the two agree (Pi F' = 2F), which is why QX17 could not see the difference.

| case (stiffness) | reading | K1 P eq | K2 khronon eq | K3 metric eq | K5 n n T |
|---|---|---|---|---|---|
| G: Pi^2/2 + (3/10) Pi^4 - (1/7) Pi^6 | R1 | PASS 3.3e-40 | PASS 1.4e-41 | **FAIL 9.1e-2** | PASS 8.1e-41 |
| G | **R2** | PASS 3.3e-40 | PASS 1.4e-41 | **PASS 3.4e-40** | PASS 6.4e-41 |
| B: A Pi^6, A = 122363904/44610575 | R1 | PASS 2.4e-40 | PASS 1.6e-41 | **FAIL 1.4e-1** | PASS 3.8e-40 |
| B | **R2** | PASS 2.4e-40 | PASS 1.6e-41 | **PASS 7.1e-40** | PASS 4.5e-40 |

Max relative residual over seeds 11, 22, 33 (line 1e-10). K0 (Legendre) PASS in every run.

## Controls
- KA (F = Pi^2/2): R1 = R2 = RAW, K1-K3 and K5 PASS to <= 1.2e-40, reproducing QX17. PASS.
- MUTATE (the raw closed forms, F' -> Pi and F -> Pi^2/2, against stiffness G): K1 1.22, K2 1.30, K3 1.66. **BITES.**
  (K5 does not discriminate: on the Pi > 0 branch n n T reads Pi + gamma F under every reading, so it carries no weight
  in the label; K1-K3 do.)

## Consequence for the record
- PAPER70's stress tensor for the adopted action carries Pi F'(Pi) h_mn in place of 2 F h_mn. Nothing graded changes: every
  static, FRW and linear row in the record either sits where the blend equals the raw form (Pi >= b or Pi < 0, TC1) or was
  checked by QX19 at the level of the action.
- n n T of the P sector is Pi + gamma_L F(Pi) for any F (K5), so the static source and the Poisson limit are unchanged.

## Disclosures
1. The first launch crashed on a missing dictionary entry for R2 before any graded number was printed; it was fixed and
   rerun unchanged otherwise.
2. Peak RSS 1.76-3.29 GB per process (ru_maxrss), above the 1 GB line; no 1024^3 run was live (checked before launch),
   which is the condition that line protects. Each run about 30 min at nice 15.
3. B tests the blend's pure-power branch (q <= 1/2) and G a generic polynomial; the C4 layer polynomial is covered by the
   general-F statement because the derivation and the check use only F and F' at a point. The Pi < 0 branch is F = 0
   identically.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
