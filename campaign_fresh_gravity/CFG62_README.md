# CFG62 — can one declared variable split the rule's populations into consistent groups?

- **Criteria:** frozen before the script, in `CFG62_FROZEN_CRITERIA.md` (dfe4d59ef).
- **Script:** `CFG62_population_split.py`, a pure computation on CFG59's committed per-population intervals; it runs in under 1 s. Its MUTATE control, which sets every interval to [0, 1], exits 1 as required.

## Bottom line

**No split by one variable works.** Four variables were declared before the intervals were read: stellar mass, the phantom-to-collapse ratio log(M_ph,edge/M_coll), pressure vs rotation support, and satellite vs central. Across every threshold, no split gives both groups a common debris fraction φ. That holds for all ten populations (0 of 20 splits succeed, both footings) and for the nine without the X-ray ellipticals (0 of 18; H2 was declared after seeing X-ray's empty interval, disclosed).

## What a reconciliation would need (reported)

The fewest contiguous stellar-mass groups that each admit a common φ number three for the nine populations, and **φ is not monotonic in mass**:

| group | log M_* | φ (canonical) | φ (alt) |
|---|---|---|---|
| Tucana II + MW ultra-faints | 3.7–3.9 | 0.39–0.84 | 0.39–0.83 |
| Boötes I + M31 Collins + M31 LVD + MW classical | 4.6–6.1 | 0.14–0.30 | 0.12–0.22 |
| SLUGGS + DT23 S0/S0a + UGC 2487 | 11.2–11.5 | 0.81–0.96 | 0.68–0.99 |

The X-ray ellipticals need φ ≈ 2.15, more debris than the collapse mass holds. The satellites conflict among themselves: in the satellite-vs-central split the centrals intersect (0.81–0.96) but the satellites do not.

## Reading

**The derived rule's debris fraction is not a one-variable function of mass, the phantom-to-collapse ratio, support or environment on these lanes.** Keeping the rule would take per-population retention (high, low, then high again with mass, plus more than 100% for the X-ray ellipticals). That is a fit, not a law. The control C1 reproduces CFG59's committed answer (the SLUGGS–M31 LVD gap is 0.507 canonical and 0.460 alt).

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
