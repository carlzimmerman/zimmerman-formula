# CFG774: sealed prediction for a deep-space probe (10 AU – 0.1 pc)

**Label: SEALED.**
- Table sha256 `f40da2eeb29bf51aa77d1fa411b5912ccc78abb1110898a8f52256c0ecd7039a`.
- **Only the committed stiffened action (F1) is alive.** Both γ = 0 forms (F2 local, F3 with the basin rule) keep the
  simple μ's a₀ tail from the Sun's own field and fail the 1-AU ephemeris bound by 2557× / 3091×.
- F1 predicts a constant sunward pull of 4.22e-15 m s⁻² (L* = 5.75 pc) from 10 AU out to 0.1 pc. It is 1.4e-19 at L* = 1 kpc.
  There is no MOND regime around the Sun at all.
- **Kill line:** a non-thermal anomalous sunward acceleration ≥ 1e-13 m s⁻² measured at r ≥ 1000 AU EXCLUDES the framework
  at every L*.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (c271c88d9). Block CFG770–779.
- **Script:** `python3 cfg774.py`. It imports CFG770's `a_anom`/`background` read-only (K2 reproduces CFG770 T3 to < 1e-4).
  Exit 0. `CFG774_MUTATE=1` (L* = 1e-4 pc) gives 6.3e-6 m s⁻², above the kill line: the tooth bites, exit 1.

| L* (pc) | a(10 AU) | a(1000 AU) | a(7000 AU) | a(2×10⁴ AU) | a(10⁵ AU) |
|---|---|---|---|---|---|
| 5.75 | −4.216e-15 | −4.208e-15 | −4.165e-15 | −4.074e-15 | −3.563e-15 |
| 30 | −1.549e-16 | −1.548e-16 | −1.545e-16 | −1.539e-16 | −1.499e-16 |
| 100 | −1.394e-17 | −1.394e-17 | −1.393e-17 | −1.391e-17 | −1.380e-17 |
| 1000 | −1.394e-19 | −1.394e-19 | −1.394e-19 | −1.394e-19 | −1.393e-19 |

These are canonical values; alt agrees to ≤ 2%. The full table is in `cfg774_results.json`.

## Reading
1. **A probe at 7000 AU, where the unscreened law would put the Sun's field at a₀, sees Newton in this framework.** It would
   also see a uniform pull of at most 4e-15 m s⁻² toward the Sun. Its sign is fixed (sunward) and its size does not depend
   on r out to about 0.1 pc. Both are distinctive.
2. **Standard MOND with an external-field effect** predicts anomalies about a₀ ~ 1e-10 at those distances. Any detection at
   that level kills this framework. A null at 1e-13 does not distinguish the framework from GR.

## Disclosures
- Real probes carry non-gravitational accelerations of about 1e-10 (thermal recoil, as for Pioneer). Reaching the kill line
  needs future drag-free technology at hundreds of AU.
- The 0.1-pc row (−4.07e-15) sits between the 2×10⁴ and 10⁵ AU rows, as it should (0.1 pc ≈ 2.06×10⁴ AU).
- quad prints a roundoff warning in one remainder integral. The table is smooth and K1/K2 pass.
- κ fitted; not theory closed.
