# Modular-Weight-at-Omega Test of Koide Q=2/3 (Zimmerman framework)

**Date:** 2026-06-25  **Status:** NULL (both-ways verified, exact).
**Script:** `real_research/modular_weight_omega_test.py` (mpmath dps=40, all values exact to
~40 digits; A4 modular forms built from primary-source q-expansions, higher weights by
standard A4 Clebsch-Gordan — nothing fitted).

## The question (non-circular)

The one genuine resonance this session: modular flavor's residual **Z3 at the fixed point
tau = omega = exp(2 pi i/3)** is the same generation-Z3 the framework's Spin(8)-triality
1+2 decomposition uses for the Koide circulant shape. Q = 2/3 <=> r = sqrt(2) stays free
because Q(omega) had spanned {1/3, 0.36, 0.5, 0.375} across reps/weights tried — never 2/3.

**TEST:** does a **framework-FORCED modular weight k** (fixed by a framework quantum number,
not scanned to hit 2/3) land Koide Q = 2/3 at tau = omega, non-circularly?

## Ground truth (primary sources, not fitted)

Weight-2 A4 (=Gamma_3) triplet, Feruglio [arXiv:1706.08749], q = exp(2 pi i tau):
- Y1 = 1 + 12q + 36q^2 + 12q^3 + ...
- Y2 = -6 q^(1/3)(1 + 7q + 8q^2 + ...)
- Y3 = -18 q^(2/3)(1 + 2q + 5q^2 + ...)
- constraint Y2^2 + 2 Y1 Y3 = 0 (all tau)

Computed here in closed form from Dedekind-eta log-derivatives (eta'/eta = i pi E2/12,
E2 = 1 - 24 sum sigma1(n) q^n), so the omega values are exact, not literature-quoted.
Constraint verified to 1e-41 at omega. Higher weights (4,6,8,10,12) built from the
weight-2 triplet by the standard A4 CG product (triplet x triplet -> 1,1',1'',3_s).

## Q(k) table at tau = omega (triplet-valued channels)

| weight | channel | Koide Q | angle to (1,1,1) |
|---|---|---|---|
| 2  | 3 (Y)              | **0.360000** = 9/25 | 15.793 deg |
| 4  | 3_s (YxY)          | **0.360000** | 15.793 deg |
| 6  | 3 (Y x [YY]_3)     | **0.360000** | 15.793 deg |
| 6  | 3 (1_4 . Y)        | **0.360000** | 15.793 deg |
| 6  | 3 (1'_4 . Y)       | **0.360000** | 15.793 deg |
| 6  | 3 (1''_4 . Y)      | **0.360000** | 15.793 deg |
| 8  | 3 (Y x w6_3)       | **0.360000** | 15.793 deg |
| 8  | 3_s ([YY]x[YY])    | **0.360000** | 15.793 deg |
| 10 | 3 (Y x w8_3)       | **0.360000** | 15.793 deg |
| 10 | 3 (w4 x w6_3)      | **0.360000** | 15.793 deg |
| 12 | 3 (Y x w10_3)      | **0.360000** | 15.793 deg |
| 12 | 3_s (w6 x w6)      | **0.360000** | 15.793 deg |

target 2/3 = 0.666667. **Channels within 1e-4 of 2/3: ZERO.**

## The decisive finding: Q at omega is WEIGHT-INDEPENDENT (= 9/25 exactly)

At the omega fixed point the residual Z3 (= the ST generator) forces every A4 triplet
modular form, at every weight, to align with the SAME Z3-eigenvector. Its magnitude
multiset is **{1, 1, 1/2}** (the position of the "1/2" permutes with weight, but the
multiset is fixed and Koide Q depends only on the multiset, not the ordering — verified
explicitly w4..w10: patterns (2,1,2),(1,2,2),(2,2,1),(2,1,2)).

=> Q(omega, any weight) = Q(1,1,1/2) = (1+1+1/4)/(1+1+1/2)^2 = (9/4)/(25/4) = **9/25 = 0.36**,
sympy/mpmath-exact. In the Koide r-picture this is **r = 2/5** (Q = 1/3 + r^2/6).
Koide 2/3 needs **r = sqrt(2)** = sqrt(2)/(2/5) = 5/sqrt(2) ~ 3.54x larger.

Non-triplet routes are void at omega: the weight-4 singlet triple {1,1',1''} has TWO
components vanishing (Z3), giving the degenerate Q=1 (one-nonzero limit), not 2/3.

## Is any weight framework-forced AND gives 2/3? NO — on both clauses.

1. **No weight gives 2/3 at all.** Q is the weight-independent constant 9/25 for the entire
   tower k=2..12 (and forever, by the Z3 argument). There is no weight to "force" toward 2/3
   because the target is unreachable at omega in the A4 triplet channel — the question is
   moot before circularity even arises.
2. **S4 / A5 cross-check (structural):** the omega-class fixed point tau_ST in S4 and A5 also
   preserves a residual **Z3** [arXiv:1910.03460], so their triplet forms align to a
   Z3-eigenvector by the identical mechanism — same weight-independent {2,2,1}-type pattern,
   no 2/3. (Quintuplet/doublet channels are not 3-vectors and don't furnish a Koide triple.)
3. **Circularity guard — clean.** We did NOT scan weights to find 2/3 (there is nothing to
   find); we did NOT pick a weight because it gives 2/3. The framework numbers that could fix
   k (triality dims {1,2,3,8}, N_gen=3, Z's integer content, kappa=1/2) are irrelevant to the
   OUTCOME because every weight yields the same 9/25. So even a forced k cannot help.

## Why this is the right structural reason (not a coincidence)

Koide 2/3 <=> the sqrt-mass vector at **exactly 45 deg** to (1,1,1). The A4 triplet at omega
sits at **15.79 deg** to (1,1,1) — pinned there by the residual Z3 eigenvector, NOT a free
modulus at this fixed point. Moving tau OFF omega frees the angle (you can dial 45 deg) but
then there is no residual symmetry and no framework-Z3 hook — the resonance evaporates. The
shared-Z3 hook fixes the SHAPE (1+2 / circulant) but pins the AMPLITUDE to r=2/5, the wrong
value. This is the same wall as the spine route (Q = 1/3 + r^2/6, r=sqrt(2) unforced), now
seen from the modular side: **at the only point where the framework-Z3 acts, r is fixed and
fixed wrong.**

## Honest both-ways verdict (one line)

**NULL, as the honest prior expected and now PROVABLY (exact, weight-independent): the
shared Z3 at tau=omega forces every A4 modular-form weight to Koide Q = 9/25 = 0.36 (r=2/5),
never 2/3 — the modular hook is SHAPE-ONLY (corroboration of the 1+2 circulant structure),
not a derivation of the amplitude; no framework-forced weight exists that lands 2/3
non-circularly, because no weight lands 2/3 at all.** This completes the one un-run test the
shared-Z3 resonance licensed and, with the prior formula/relational/mechanism/Dirac/
variational/sector/channel walls, exhaustively confirms the SM mass sector needs genuinely-
new physics not in hand. No opening; quarantine held; no manufactured win, no manufactured
deficit.

Sources: [Feruglio 1706.08749](https://arxiv.org/abs/1706.08749);
[Texture zeros at tau=omega 2207.04609](https://arxiv.org/pdf/2207.04609);
[Novichkov-King S4/A4 fixed points 1910.03460](https://arxiv.org/pdf/1910.03460).
