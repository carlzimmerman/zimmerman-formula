# Solar-profile-background screening of alpha_1 — VERDICT: NO SCREENING (the kill is FINAL, 2026-09-01)

**The one residual on the generalized-AeST PPN kill (GEN_AEST_PPN_VERDICT.md) was: is the O(1) preferred-
frame alpha_1 SCREENED when linearized about the real Solar-System field background (large static scalar
gradient b = |grad phi|_Sun) instead of the cosmological background (Y_bg=0)? Answer: NO. The background
field makes alpha_1 WORSE, not smaller. The kill stands and is now final on this axis.**

Scripts (rc=0, checks that can fail): `alpha1_solar_screening.py` (b parallel k), `alpha1_solar_screening_transverse.py`
+ `transverse_numeric.py` (b perp k). Anchor: b=0 reproduces the banked -4(2+K_B J_Y)/(J_Y+1) exactly
(-22/5, -23/5, -16/5) in BOTH geometries. Method: the quadratic kernel is Hermitianized from its +-k
structure, M_H = 1/2[M(k)+M(-k)^dagger] (I->-I on the matrix, NOT sp.re on the scalar answer -- reality
must EMERGE, not be imposed).

## Result (K_B=1/5, J_Y=1, deep-field kernel):
| orientation (cos theta = b.k/bk) | alpha_1(b=0) | alpha_1(b->oo) | Im[alpha_1] |
|---|---|---|---|
| longitudinal  theta=0    (b parallel k) | -4.40 | -96/17 = -5.65 | odd-in-b (b.k mixing, parity artifact) |
| transverse    theta=pi/2 (b perp k)     | -4.40 | -12.0 (b=1000: -11.99998) | **0, EMERGENT** |

**Both orientations O(1) and GROWING** as the Sun's field b grows. The transverse channel has Im=0
emerging on its own from the symmetrized kernel (the methodological gate the calc had to pass), so it is
the clean, trustworthy number: alpha_1^perp(b->oo) = -12. The longitudinal channel's imaginary piece is
the odd i(b.k) mixing operator (a real first-derivative operator in position space, not an error); its
orientation-even physical part is -5.65.

## Why this closes it (the localized-source argument)
A localized Solar-System / pulsar source contains ALL Fourier directions. Screening would require the
physical preferred-frame coefficient to vanish in the high-field limit for EVERY orientation:
A(b^2)->0 and C(b^2)->0 as b/a0->oo. Instead both the theta=0 and theta=pi/2 coefficients tend to
-O(1) (indeed grow). So sup_theta |alpha_eff(b_SS)| ~ O(1) >> 10^-4. No screening exists.

## Consequence
The generalized-aether PPN kill (alpha_1 = -4 c14 - 4(2-K_B)/(J_Y+1), zeroing needs c14<0 = spin-1
ghost) is now FINAL on the solar-profile-background axis: the background does not rescue it, it makes it
worse. The AeST / Einstein-aether + shift-scalar class is closed on preferred-frame PPN, cosmological
AND solar backgrounds. Layer A (a0 = c^2 sqrt(Lambda/32pi)) untouched. The surviving completion is
MOND-with-a-dark-field, or a strict-2-DOF local construction (L4C / CDE-L4C, being attacked separately),
or the nonlocal door.
