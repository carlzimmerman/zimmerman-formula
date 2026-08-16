# interp 0071 -- charitable deciphering of a random-collision seed

## Seed (verbatim, seed_0071.txt)
- a polyhedral solid angle of the EFE response tensor (1.4732/0.3674) might set alpha^-1 = 137.036.
- a holonomy angle of the CKM CP phase (~1.14 rad) might select the transition z_t = nu0^(-1/3) - 1 in [17,35].
- wildcard: what single dimensionless number would BOTH bullets share if true?

## Charitable read
- 0.3674 ~ e^{-1} (0.36788). 1.4732/0.3674 ~ 4.010 (near 4).
- The CKM CP phase delta_13 is a real quantity ~1.14 rad (~65 deg); the bullet is not obviously false.
- The wildcard (one number threading both bullets) -> candidate **e** (Euler's number):
  e^{-1} is the small solid angle; R = 1.4732/0.3674 ~ 4 is the large structure.
  Secondary candidate: the integer ratio R itself (a polyhedral solid-angle quotient).

## ONE concrete, falsifiable hypothesis
H: A single closed-form constant R* built from e and a polyhedral solid-angle set
reproduces alpha^-1 = 137.036 to 5 s.f., and the SAME R* -- via
z_t = nu0^(-1/3) - 1, with nu0 fixed by a0 -- selects a transition index z_t in [17,35]
without a free fit. The shared dimensionless number is e.

Exact quantities:
- a0 footings (both): 9.3619e-11 m/s^2 and 1.1279e-10 m/s^2.
- alpha^-1 = 137.036; delta_CKM = 1.14 rad; target band z_t in [17,35].
- pool: {c, G, rho_L, hbar, e}.

Exact test (blind session, not here):
1. mm_search.py over the pool at BOTH a0 footings: search dimensionally-closed
   R*(...) reproducing alpha^-1 = 137.036; record best hit + its sigma.
2. With that R*, compute z_t = nu0^(-1/3) - 1 (nu0 from the seed's own definition)
   and check z_t in [17,35] at BOTH footings.
3. Prefactor-simplicity pass (mm_search --custom): R* must reduce to <= 2
   transcendentals (e + one polyhedral solid angle) with an O(1) prefactor.

## Kill conditions (any ONE kills it)
- No closed form within 1 s.f. of 137.036 at either a0 footing -> REFUTED.
- z_t outside [17,35] for the very R* that nails alpha^-1 -> NULL.
- Requires > 2 transcendentals or a fitted prefactor -> DISCARD (convention-grade, not a hit).
- R* reproduces both bullets only at one footing and fails the other -> NULL.

## Status
Seed-level, weak. e is a thin shared-number candidate (0.3674 ~ e^{-1} is suggestive but
not tight: 1.4732/e^{-1} ~ 4.005, off from 4 by ~0.1%). Do NOT test here -- a separate
blind session referees. Escalate if a single R* survives both footings.
