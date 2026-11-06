# EB1b_web_efe: with the web's own external field, the law forms no early seeds

Criteria 0ff17cf4ce (written after EB1's result, labelled post-result, before any EB1b number); script committed
before the run. Kappa = 1/2 FITTED. Not theory closed. Conditional on WG2's R1 rule (fails CMB lensing, WG2-WG6).

## Label: G1 = NO in every cell, both footings, every e(z) reading

The external field e(z) = |g_N| / a0 is read from WG2's own law-on box (R1, TIE, B2, A_s 2.1e-9, 128^3, 1600 h^-1 Mpc),
canonical median: 0.0256 at z 50, 0.0135 at z 30, 0.0095 at z 20, 0.0062 at z 10, 0.0053 at z 7, 0.0020 at z 0.

| reading | earliest collapse of any 1e6-1e13 Msun clump, nu_pk <= 5 | QSO1 gate (all eps, M_BH, seeds) |
|---|---|---|
| p05 (weakest field) | canonical z 0.48 (1e6, 5 sigma); alt z 0.64 | NO everywhere |
| median (primary) | none by z 0 | NO everywhere |
| p95 | none by z 0 | NO everywhere |

Checks: K5 (e = 0 reproduces EB1's R1 table) max rel 0 PASS; K6 (e = 0.03 reproduces EB1's no-collapse cell) PASS;
K7 (median differs from zero field) PASS. MUTATE (e x 0): K7 FAILS, exit 1 (bites).

## Reading
- EB1's EASY rested on an isolated sphere. In the law's own web the large-scale peculiar field is 0.5-2.6 % of a0
  over z 50-7. That caps the boost at nu ~ 7-14 instead of letting it run to sqrt(a0 / g) on a tiny clump, and from
  sigma_b ~ 1e-3 at z 50 a capped boost on baryons alone is not enough to reach collapse for seeds, or for galaxies,
  before z ~ 0.5.
- The field used is a lower bound (12.5 h^-1 Mpc mesh misses smaller-scale field down to the Silk scale), so the
  NO is robust to that limit, as frozen.
- So under the record's one web rule, from the record's baryons-only start, the framework **cannot form
  A2744-QSO1's black hole by z 7.05**, and forms essentially no bound baryon structure early at all. This is the
  growth no-go (QX3, WG2-WG6) seen at seed scales, not a new failure mode.

## Limits
- Scalar EFE ansatz nu((|g_N| + e a0) / a0). A full vector QUMOND treatment of a clump inside an anisotropic web
  field could differ by an order-unity factor in the boost; it would not supply the ~1e3 factor in growth that is
  missing.
- Spherical, pressureless, no fragmentation. The rule R1 is a fixed reading, not the action: growth inside the
  action is separately a no-go (QX3). The one untried route QX3 names (a sector whose Jeans scale is switched by the
  local acceleration) is not tested here.

Run: `python3 eb1b.py` (~30 min, one thread, loaded machine); `EB1b_MUTATE=1 python3 eb1b.py` exits 1.
