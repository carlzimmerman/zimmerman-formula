# DOOR F3 — Prove or refute: can a linear tau-convolution dressing of a KMS seed break KMS at all?
STATUS: OPEN | RANK: 3 | COST: S | KILLS FAST: YES (and it is a theorem either way)

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
Every corrected computation in the review came out anti-MOND. That is too consistent to be an accident, and it
suggests a theorem: **a linear convolution dressing in proper time cannot break the KMS condition of its seed.**
If true, it explains every negative result at once and tells the programme exactly where to look instead
(nonlinear coupling, composite operators, or two baths).

## Why it works with the framework
It is the cleanest possible statement about the machinery the programme actually built, and a theorem here would
be the most valuable single output of the whole NESS effort — a real result from a failed mechanism.

## Concrete first calculation
1. Let `G_seed` satisfy KMS: `G(tau + i beta) = G(tau)`. Let `G = G_seed + q^2 K * G` with K a function of
   `tau - tau'` only.
2. Ask whether G inherits beta-periodicity. Test the analytic continuation `tau → tau + i beta` through the
   convolution.
3. Prove it in general, or construct an explicit counterexample kernel.

## Settles if / refuted if
SETTLED (theorem): a linear tau-convolution preserves KMS ⇒ the entire NESS-by-resummation strategy is dead by
theorem, not by numerics, and A2/A3/B2 become the only routes. **This is publishable and it is cheap.**
REFUTED: an explicit kernel that breaks KMS ⇒ then ask why every numerical attempt still gave anti-MOND, and
whether the breaking is O((v/c)^2) again.

## Known walls — do not rediscover
Bunch-Davies is exactly beta-periodic (verified to 2.1e-16) — that is the seed property, established. And the
review found the linear vertex supplies **exactly zero** KMS violation, which is strong prior evidence that
this theorem is true.
