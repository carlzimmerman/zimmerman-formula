# CFG935 AMENDMENT A0 (pre-result): run lengths and the meaning of "f_min"

Date: 2026-10-20. Committed alone, after FROZEN_CRITERIA.md (38f4b6f18) and BEFORE any CFG935 script exists or any CFG935 number
has been computed. FROZEN_CRITERIA.md is not edited. Both changes come from hand reasoning about the frozen design, not from any
run.

## A0.1 Run lengths scale with each gravity type's own edge period

The frozen t_end (IC-L 200, IC-I / IC-S 400) is too short for the S2 tether. Its cold energy is bound only by the baryons (the
tether cancels its self-gravity), so the oscillation period about the settled edge is T_edge,S2 = 2π√(r_*³/(G M_b)) = 198.7 toy
units: t_end = 400 is two periods at r_*. The N-type period is T_edge,N = 2π√(r_*³/(G(M_b + M_c))) ≈ 61.5. The record's
collisionless tether runs averaged over t = 2000–3000 (CFG747) and 10000 (CFG748) in the same units.

**Replacement:** t_end = 10 T_edge (rounded up to a multiple of 50) for IC-I and IC-S, and 5 T_edge for IC-L:
- N-type repairs (R-a(i), R-b, R-c, R-d): IC-I / IC-S t_end = 650, IC-L t_end = 350;
- S2 (R-a(ii)): IC-I / IC-S t_end = 2000, IC-L t_end = 1000.

The windows stay W1 = [0.50, 0.75] t_end and W2 = [0.75, 1] t_end. K2 (t = 200) and MUTATE (t = 100) are unchanged.

## A0.2 "f_min" is the largest escape fraction compatible with a law remnant

FROZEN_CRITERIA §3 defines f_min = 1 − M_rem/M_c from E_law(M_rem) = E_init ("marginal escape"). With E_law(M) decreasing in M
and E_init = E_law(M_rem) + E_esc, E_esc ≥ 0, a remnant on the law needs E_law(M_rem) ≤ E_init, i.e. M_rem ≥ M_x with
E_law(M_x) = E_init. Zero-energy escapers (M_rem = M_x) give the LARGEST escaped fraction; energy alone sets no lower bound above
0⁺ (a small mass can carry the excess at high speed). The quantity is computed exactly as frozen and reported as
**f_esc,max (zero-energy escapers)**. The robust number is the excess energy ΔE_x = E_init − E_law(M_c), reported as a fraction
of |E_law(M_c)|. A run whose remnant is ON THE LAW with f_esc > f_esc,max would be internally inconsistent (checked).

The §6 estimate f ≈ E_x/(M_cat|Φ(r_*)|) is the same zero-energy-escaper estimate in the law's potential and is reported under the
same name (an indicative upper-type figure, not a minimum).

## A0.3 Implementation layout (no physics change)

Each run is a separate part (`python3 cfg935.py <part>`) writing `parts/<part>.json`; a runner script executes the parts one at a
time (K and MUTATE first) and a summary part aggregates them into `cfg935.out` / `cfg935_results.json` (and the `_MUTATE` pair).
