# X48_native_cf_zoom: native formation concentrations. Frozen class UNRESOLVED: the resolution check fails; ng 38 is not converged

Criteria: `FROZEN_CRITERIA.md` (1932858ae8, committed before any production number). Engine and smoke evidence: df13411b6e,
`SMOKE_EVIDENCE.md`. Physics: collisionless dust + Λ on the record's background A (route E's cold dark energy without the a₀
floor), **not v3s**. κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

The six runs at 10¹³ and 10¹⁴ M☉ were started directly (single-thread, nice 15, owner 10-25 "keep it cranking"), in the
same work folders as their queue twins, which are on hold.

## FINAL (all ten runs, 10-25)

| M | ng 38 seeds (c_f from the −2 crossing) | median | particles inside r₋₂ |
|---|---|---|---|
| 10¹² | 10.60, 12.59, 10.19 | 10.6 | 304–468 |
| 10¹³ | 5.86, 9.02, 5.92 | 5.9 | 447–847 |
| 10¹⁴ | 12.68, 8.03, 11.01 | 11.0 | 296–554 |

**Resolution check (frozen §3):** for 10¹⁴ M☉, seed 1, ng 38 → 48 (N 12k → 24k), the −2-crossing c_f goes **12.68 → 2.59**
(−80 %, line ±20 %), with 4 358 particles now inside r₋₂. **Frozen class: UNRESOLVED.** The ng-38 −2-crossing c_f is not
converged at these particle counts, so the provisional regrade below is not evidence either way.

Reported only (no verdict weight): the NFW-form fit of M(<r) gives 5.90 at ng 38 and **4.00 at ng 48**. The standard
formation value, and the data's pinned 4–4.2, sit right there. One run, and the NFW form is a fitting shape, not a measured
crossing.

**What resolves it:** ng ≥ 48 for every mass and seed (about 6–7 h per run at one thread, so ~7 h wall if all nine run in
parallel), or a faster force solver. Until then X43 stands with c_f = 4 external.

## Provisional c_f at the two masses run first (superseded by the resolution failure above; kept as run)

## Native c_f (frozen measurement, x48_analyze.py; checks K3 pass, drift ≤ 4e-15, constraints ≤ 1e-15)

| M | seed 1 | seed 2 | seed 3 | median | particles inside r₋₂ |
|---|---|---|---|---|---|
| 10¹³ | 5.86 | 9.02 | 5.92 | **5.9** | 447–847 |
| 10¹⁴ | 12.68 | 8.03 | 11.01 | **11.0** | 296–554 |

**Frozen class: UNRESOLVED (pending).** The 10¹² mass and the ng = 48 check are not yet run. On the measured masses, c_f lies
**above** the data window [3.3, 4.6].

## Provisional regrade of X43 (x48_regrade.py; η = 24.2 at ≤10¹³, 52.6 at ≥10¹⁴, interpolated in between)

| key (canonical; alt the same in class) | X43 (c_f 4) | native |
|---|---|---|
| SPARC rms / Υ | 0.078 / 0.77 PASS | **0.068 / 0.68 PASS** |
| groups | Z +2.05 FAIL | **Z +1.62 PASS** |
| MGAS T3 OUTER | Z +2.41 FAIL | **Z +0.79 PASS** |
| MID T1 / T2 / T3 | pass | Z −2.60 / −2.14 / −2.87 (OVER) |
| INNER all | pass | Z −3.52 (OVER) |

**Reading (provisional).** The native concentration clears both keys that every earlier rule failed (groups, MGAS T3 OUTER),
but it over-concentrates the cluster cores. The data sit between c_f ≈ 4 and the native ≈ 11 at cluster mass.

Caveats, to be graded when the batch lands:
- These are isolated spheres: no external tides or late mergers, both of which lower concentration.
- Particle counts inside r₋₂ are modest (300–850); the ng = 48 run tests this.
- c_f rises with mass, the opposite of the usual trend. The likely cause is the constrained mean-curvature peak at high ν.
