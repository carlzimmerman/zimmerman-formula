# INTERP 0090 -- footing-invariant ratio quantizes the CKM CP phase & alpha-structure

## Charitable deciphering of the seed
- Bullet 1: a *footing-invariant* combination of the pinned Q0 band (the two
  footings a0 = 9.3619e-11 and a0' = 1.1279e-10) reproduces the CKM CP phase
  delta_CKM ~ 1.14 rad.
- Bullet 2: the "structure" (averaging/variance) of alpha^-1 = 137.036 is the
  shadow of a 690-Gyr transport time.
- Wildcard: the ONE dimensionless number shared by both bullets.

## The single shared number (the claim)
R = a0'/a0 = 1.1279e-10 / 9.3619e-11 = 1.204777   (footing-invariant: cancels
the footing, so it is the only number both bullets can share without smuggling
in a free parameter).  Hypothesis H: the SAME R, with no extra fitted constant,
governs BOTH (i) delta_CKM and (ii) the alpha/transport relation.  Concretely
the proposed functional links (to be tested, not asserted):
  (i)   delta_CKM = f(R)            target delta = 1.14 rad
  (ii)  690 Gyr / (Hubble-time) ~ g(R)   or   var(137.036 structure) ~ g(R)
Note: 690/137.036 = 5.035, 137.036/1.14 = 120.21 -- neither equals R; this is
why the test must find f,g WITHOUT free constants or H is dead.

## Exact test
1. Build R from the two footings only.
2. Test (i): does any parameter-free mapping of R hit delta_CKM = 1.14 (tol
   ~0.02 rad) AND its two-footing partner delta'?
3. Test (ii): does the same R reproduce the 690-Gyr/alpha structure (tol
   ~1 sigma of the 690 figure) -- use mm_search.py for any dimensional match,
   it pre-registers FDR.
4. BOTH footings (9.3619e-11 / 1.1279e-10) on every dimensional number.

## What kills it
- REFUTED: R cannot hit delta_CKM to tolerance without a free constant.
- NULL: R hits one bullet but not the other (shared-number premise fails).
- DISCARD: any hit is CONVENTION-grade (unit/scale convention, not physics).
- H survives only if ONE parameter-free R explains both bullets at once.

## Status
Interpreted, not tested. Referee it blind.
