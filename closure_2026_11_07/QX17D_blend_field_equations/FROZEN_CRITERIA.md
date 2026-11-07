# QX17D: field equations of the action with the adopted Pi^6-blend stiffness. FROZEN CRITERIA (committed alone, before any script)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Lane id checked free (`ls closure_2026_11_0* | grep QX17`,
`git log origin/main | grep QX17D`: empty).

## Why
The owner adopted the Pi^6 blend as the stiffness (OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md, 71e4014cd5):
F(Pi) = b^2 f(Pi/b), b = rho_DE, f = A q^6 for q <= 1/2 (A = 122363904/44610575), C4 convex blend on the layer,
f = q^2/2 for q >= 1. QX17 (CERTIFIED) checked the covariant field equations for the raw F = [max(Pi,0)]^2/2 only, where
F' = Pi_+ and Pi F' = 2F. The PAPER70 v1.1 draft states the blend's equations as QX17's with Pi_+ read as F'(Pi), and
says that reading is not separately certified. This lane certifies it or finds the correct form.

## Readings (both registered now, before any number)
- **R1** (PAPER70 draft): QX17's closed forms (E1)-(E5) and T^P with Pi_+ -> F'(Pi) everywhere (including the
  constitutive factor (1 + gamma_L F'), the source J_P, and curly D_m = d_m F' - F' d_m l), and F -> F.
- **R2** (alternative, graded only for K3): as R1, but the stress-tensor term 2 F h_mn becomes Pi F'(Pi) h_mn (the two
  agree only for the quadratic F).

## Test stiffnesses (on the Pi > 0 branch, b = 1)
- **G** generic: F = Pi^2/2 + c4 Pi^4 + c6 Pi^6, c4 = 3/10, c6 = -1/7 (Pi F' != 2F).
- **B** the blend's pure-power branch: F = A Pi^6, A = 122363904/44610575 (exact, from the PI6 case file / QX19 C6).
Footing-independent (an algebraic identity of the action); no data, no footing numbers.

## Checks (PASS = relative residual <= 1e-10 at every test point; QX17's machinery, seeds 11, 22, 33, same tolerance)
- K1 P equation, K2 khronon equation, K3 metric equation (non-GR stress tensor), K5 n n T of the P sector = Pi + gamma F
  (R1) - each closed form vs. the Euler-Lagrange derivative of the Lagrangian density with the test F, by sympy on jet
  variables, 40-digit mpmath total derivatives, random polynomial fields in 2+1, n.P = 0 by P = h.V.
- KA: F = Pi^2/2 reproduces QX17's K1-K3 and K5 PASS (R1 = R2 = QX17 there).
- MUTATE: the raw closed forms (F' -> Pi, F -> Pi^2/2) against stiffness G must FAIL K1 or K3.

## Labels
- **R1 CERTIFIED**: K1, K2, K3, K5 pass under R1 for both G and B, KA passes, MUTATE fails.
- **R1 FAIL, R2 CERTIFIED**: R1 fails K3 only, and R2 passes every check for G and B. PAPER70 then states R2.
- **NOT CERTIFIED**: anything else; the failing equation is named.
Each label is reported for G and B separately. Commit the script and outputs with the result; push as it lands.
