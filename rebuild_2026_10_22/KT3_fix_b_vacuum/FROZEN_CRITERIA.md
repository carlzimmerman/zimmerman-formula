# KT3_fix_b_vacuum: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: "actually solve it". Target: fix b in KT2's action, where kappa = 1/(n b), without inserting it. κ = 1/2 FITTED. Footings never pooled, and none is used. Not theory closed. No cold component, no particle. **Not blind:** I worked V1 and part of the V2 table by hand, and expect no b = 1. K247, K252, L226, K610 and K690 are read as listings.

## Mechanism
chi becomes the field whose vacuum sources dark energy. **Added hypothesis H, named:** the vacuum chi = 1, g = 0 carries exactly rho c^2. No other new constant is allowed in the potential.

## Questions
- **V1, self-consistency.** Sympy: energy density at vacuum is (s/b)^2 DU / (8 pi G), with DU = U_n(1) + C. Setting it to rho c^2 gives b^2 = DU/(8 pi), so kappa^2 = 8 pi / (n^2 DU). kappa = 1/2 at n = 2 needs DU = 8 pi. Check the C dependence: d kappa/dC != 0 means the zero mode decides.
- **V2, frozen list of ways to set C, none tuned:** (a) C = 0; (b) U = 0 at the transition chi = 1/2; (c) U = 0 at Y_c = Planck acceleration / s, with hbar stated; (d) U = 0 at Y_c = 1/Z-free cosmic value Y = c^2 / (s R), R = c / sqrt(G rho), which is Y = 1; (e) n = 3 and 4 at C = 0. Each gives a kappa, graded against the rho_DE window [0.227, 0.607] and exactly 1/2.
- **V3, dynamics.** Add kinetic term K (d chi)^2 with K free, on de Sitter. At vacuum V'(1) = V''(1) = 0, so chi = 1 is an inflection. Solve delta = 1 - chi at late time. Question: does any solution, attractor or stability condition fix b or C? If the equation only sets the decay amplitude, the answer is no.

## Labels
- **EXACT CANDIDATE:** a listed route gives kappa = 1/2 with no tuned input, and then all of CFG894 §3 and §6 are still owed.
- **CONSISTENT:** a listed route lands in the window.
- **NO FIX:** none does, or only C tuned. Says the zero mode survives in this action. Not a no-go theorem outside the class.

## Controls
MUTATE: 8 pi G -> 4 pi G in the field term. Expected: kappa^2 halves. Separate `_MUTATE` output, exit 1 by design. I1: no target constants in the script's inputs; 1/2 is printed only as a comparison. I3: kappa scale invariant.

Second prediction, S4: V3 gives one if chi's late-time rolling shifts w away from -1; report it with K left free, and state if it isn't testable. No download. Single thread, seconds.
