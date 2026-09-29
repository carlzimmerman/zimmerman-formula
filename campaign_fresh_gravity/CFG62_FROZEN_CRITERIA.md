# CFG62 — can ONE declared variable split the rule's populations into consistent groups? FROZEN CRITERIA

Written 2026-09-29, **before the CFG62 script exists**. This file is committed on its own.

**What was already known when it was written:**
- The four split variables were declared in the proposal to the orchestrating session before CFG59's per-population intervals were read: collapse mass, stellar mass, pressure vs rotation support, satellite vs central.
- CFG59's committed per-population φ intervals were then read (`CFG59_universal_debris_fraction_results.json`, TAB `segs`).
- U6 (X-ray ellipticals) has an EMPTY interval in φ ∈ [0, 1]; it needs φ ≈ 2.15.
- The nine-population question (H2) is therefore declared **after** seeing U6's empty interval. It is disclosed as such.

## Question

B's derived cold-mass rule scaled by one universal debris fraction φ cannot reconcile the ten populations (CFG59: NO). **Is there a split by ONE independent variable into two groups, with a threshold anywhere between consecutive population values, such that the φ intervals intersect within each group?** A YES would be a post-hoc hypothesis for new data, not a rule.

## Inputs (all committed, none refitted)

- **φ intervals:** CFG59's per-population intervals where the lane's own offset is within 1σ of zero (`segs`), for both footings, φ ∈ [0, 1].
- **Variable values** per population:
  - log M_* and log(M_ph,edge / M_coll), from CFG59's `meta` (`logMs`, `logratio`). The latter is the variable that sets f_ex; it stands in for "collapse mass", which is monotone in it at fixed colour.
  - Support, by morphology and tracer: rotation for U7 DT23 S0/S0a and U8 UGC 2487; pressure for the other eight.
  - Environment: satellite for U1 MW ultra-faints, U2 MW classical, U3 M31 Collins, U4 M31 LVD, U9 Boötes I and U10 Tucana II; central for U5 SLUGGS, U6 X-ray, U7 and U8.

## Pre-declared checks

- **C1 CONTROL:** CFG59's committed answer is reproduced from its JSON: no common intersection of all ten on either footing. The binding pair is SLUGGS vs M31 LVD, with a 0.51 gap (canonical).
- **H1 [HEADLINE; MUTATE must fail]:** no split of the TEN populations by any of the four variables, at any threshold, gives non-empty intersections in both groups, on either footing.
- **H2 (declared after seeing U6's empty interval; disclosed):** the same for the NINE populations without U6.
- **Reported:**
  - R1: every split tested, with each group's intersection.
  - R2: the fewest contiguous log M_* groups whose intersections are all non-empty (nine populations), with each group's φ range.
  - R3: the φ_ext values (roots on [0, 6]), so the X-ray case is visible.
- **MUTATE:** every population's interval is replaced by [0, 1]. Every split then succeeds, so H1 must fail and the script must exit 1.

## Reading (declared)

- **H1 PASS and H2 PASS:** the rule's debris fraction is not a one-variable function of mass, support or environment on these lanes. A reconciliation needs at least as many groups as R2 reports, each with its own φ.
- **H2 FAIL:** a one-variable split exists for the nine. It is reported as a hypothesis for independent data.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
