# CFG380 -- does the external math collection open a geometric door to 32 pi?

**Verdict: NO. No route is FORCED; none is even NUMEROLOGY (nothing lands within 5%). kappa = 1/2 stays FITTED.**

Criteria: `FROZEN_CRITERIA.md` (committed alone first, 2e52ab1e5). Script: `cfg380_geometric_door.py`
(sympy exact; 11/11 checks pass, exit 0). MUTATE (`CFG380_MUTATE=1`, wrong Nariai mass) fails C2, exit 1;
outputs `*_MUTATE.*`. Target: a = C c^2 sqrt(Lambda) with C = T = 1/sqrt(32 pi) = 0.09974.

Source read (DATA, read-only): `_external_data/openai_math/CONTENTS.md`, items 260 (Penrose inequalities, AF and
asymptotically AdS: the AdS papers' mass bound is m >= (r_A + r_A^3/l^2)/2), 264 (Kerr SCC, Lambda = 0), 348
(Einstein 4-manifolds, Ric > 0, sec >= 0: S^4, CP^2, S^2 x S^2, RP^4), 360/374 (optimal transport).
**The collection contains no positive-Lambda (de Sitter) Penrose or quasi-local-mass theorem.** The Lambda > 0
versions used here are the standard continuations (SdS horizon relation), checked against item 260's AdS form (C1).

## Per route (coefficient C of c^2 sqrt(Lambda); C/T; base-rate p = fraction of 889 simple forms at least as close)
| route | best reading | C | C/T | p_base | verdict |
|---|---|---|---|---|---|
| R1 Penrose relation with Lambda (Nariai extremum, horizon surface gravity) | G m_N/r_N^2 | 1/3 | 3.34 | 0.23 | CHOSEN |
| R2 quasi-local mass on the dS horizon (Hawking = Misner-Sharp; Brown-York) | G m_H/r_c^2 | sqrt3/6 | 2.89 | 0.20 | CHOSEN |
| R2' Lambda-modified Hawking mass | identically 0 in pure dS | -- | -- | -- | no scale |
| R3 area bounds (HGW/Nariai Lambda A <= 4 pi; Boucher-Gibbons-Horowitz A_c <= 12 pi/Lambda) | a = sqrt(pi/A), BGH | sqrt3/6 | 2.89 | 0.20 | CHOSEN |
| R4 Einstein 4-manifolds (radii; Vol^(1/4) -- the only way a pi enters) | S^4, c^2/Vol^(1/4) | 54^(1/4)/(6 sqrt pi) | 2.56 | 0.18 | CHOSEN |
| R5 Lambda > 0 SCC threshold beta = 1/2 read as a0 = kappa_c/2 | -- | sqrt3/6 | 2.89 | 0.20 | CHOSEN (the map beta -> kappa is invented) |
| item 264 itself | Lambda = 0, no scale | -- | -- | -- | NOT APPLICABLE |
| R6 items 360/374 (MTW, Brenier 1/3) | no Lambda, no G, no acceleration | -- | -- | -- | NOT APPLICABLE |

All 22 readings are in `cfg380_geometric_door.out`. The closest miss is a factor 2.56. Base rate: the 1%-window
fraction of the declared family is 0.0022 (record: ~0.003); a 0.1% positive control is flagged (p = 0), so the null can fire.

## Why it fails (structural, not a search gap)
- Q1: every route only *identifies* a0 with some Lambda-geometry acceleration; none derives a0. Q2: which acceleration
  is "a0" is chosen in every case; the geometry then fixes the coefficient, and it is never T.
- Penrose/quasi-local/area-bound coefficients are algebraic (pi-free: 1/3, 1/2, sqrt3/3, sqrt3/6, 1). By the record's
  one-pi obstruction (Lean, 10-05) they can never equal T, which carries pi^(-1/2). The only pi entering pure geometry
  here is via a 4-volume, giving C ~ pi^(-1/2) x (12..24)^(-1/4) ~ 0.25-0.30: the right power of pi, the wrong rational
  by x 6.5-8.5 in C^2. The missing factor is Einstein's coupling (rho_Lambda = Lambda/8 pi G), as in p17/p19.
- Several readings give C = sqrt3/3, i.e. C/T = 5.789 = Z: that is just a0 = cH_Lambda/Z restated (the de Sitter
  horizon scale), not a new number.
- Item 260 with the puzzle's own area A = pi/a0^2 gives m >= 1/(4 a0), saturated by the Schwarzschild hole of surface
  gravity a0: the record's definition, a tautology.
- Item 348 classifies shapes, not sizes: Lambda^2 Vol is scale-free (checked: Lambda^2 Vol = 12 pi^2 chi for S^4, RP^4;
  strictly less for CP^2, S^2 x S^2). Like Gauss-Bonnet (README section 2 of the puzzle), it cannot fix a length ratio.

## Effect on the record's 32-pi lanes
Nothing changes. Lane S (Brown-York/field energy) and p19 (HGW area bound) already cover the quasi-local and area-bound
routes; sections 2 and B1/B3 cover Euclidean dS/Nariai and SdS horizon relations. The one addition is CP^2 (and RP^4) in the
Euclidean Einstein menu, which item 348 shows completes the sec >= 0 list; neither hits. No positive-Lambda Penrose
inequality exists in the collection to test the record's "no real horizon carries a0" scoping (audit H2) further.

## Caveats
- The Lambda > 0 continuations (SdS relation, BGH, HGW, Lambda-Hawking mass) are standard results, not theorems from the
  collection; the collection's own theorems are Lambda <= 0 (or Lambda-free).
- The reading menu was declared in the criteria, but I wrote it knowing the target; it measures what these routes give,
  not every conceivable reading. Products/ratios of readings were not scanned (p60 already showed such grammars hit
  1/2, 1, 1/4 at the base rate).
- Not checked: Lorentzian optimal transport (McCann, Mondino-Suhr) formulations of energy conditions; they carry no
  dimensionful coupling, so no coefficient is expected.
