# INTERP 0011 — seed_0011 (random collision, interpreted charitably)

## One falsifiable hypothesis
A SINGLE dimensionless number, the Koide fixed point **f = 1/3** (equivalently the 2:1
ratio 2/3 : 1/3), is the same parameter that governs (i) the PMNS solar mixing and
(ii) the MOND-like lensing/dynamics mass ratio. The two-footing fork is the *geometric
image* of that one fixed point; its holonomy angle is the angle by which the fork's two
branches subtend it.

## Exact quantities
- Footings: a = 9.3619e-11, b = 1.1279e-10 (the two footings of the fork).
- Fork holonomy angle: h = arctan(a/b) = arctan(0.8300) = 0.6931 rad.
- Target (i): sin^2(theta_12) = 0.307 (PMNS solar parameter).
- Target (ii): M_lens / M_dyn = 29 at f = 1/3 (Koide 2/3 interpolated to the fixed point).

## Wildcard answer (single shared number)
The shared number is **f = 1/3**. Both bullets are two projections of it:
h (the fork holonomy) and 29 (the lensing ratio) are predicted by the SAME f = 1/3
through a low-degree analytic map. Discriminator for the referee: if the map needs f=1/3
to hit 0.307 AND needs the same f to hit 29, the number is unified; if it needs two
different numbers, the collision is spurious.

## Exact test (pre-registered)
1. Map for (i): pre-register candidates  pred1 = (2/3)*h/pi,  pred2 = 1 - (b/a)/3,
   pred3 = h*(1/3). PASS if one hits 0.307 within +/- 0.03 (3-sigma on the fit).
2. Map for (ii): Koide 2/3 relation R(x) interpolated to the fixed point f=1/3;
   PASS if R(1/3) = 29 within +/- 3 (about 10%).
3. Unification: the f-value used in (i) must equal that used in (ii), to < 1%.

## What kills it
- REFUTED: no pre-registered map1 hits 0.307 within 0.03, OR R(1/3) != 29 within 10%.
- NULL: maps hit individually but with DIFFERENT f-values (no single shared number).
- DISCARD: h depends on the arbitrary choice arctan(a/b); a branch-agnostic angle
  (e.g. via the ratio's log or a loop integral) changes 0.307 by >0.03.

Note: 0.307 taken as sin^2(theta_12) (well-known ~0.304); h=0.6931 ~ ln2 is a coincidence
flagged for the referee, not claimed as structure.
