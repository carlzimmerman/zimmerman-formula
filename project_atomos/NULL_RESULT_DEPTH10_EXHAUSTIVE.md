# Depth 10, EXHAUSTIVE: clean null (2026-07-28)

**The first exhaustive depth past 9.** Not a sample — every Gate-B-passable dimensionless value
constructible at depth 10 from the framework's forced germs was enumerated and swept.

## Result

```
distinct values enumerated : 42,534,139   (raw candidates 174,890,804)
targets swept              : 19           (holdout excluded -- this is a search)
in-window hits             : 82,613
CERTIFIED (gate-passing)   : 0
RE-LABELED                 : 0
sweep wall                 : 2,144 s
```

**CLEAN NULL.** No expression built from `3` and `sqrt(8pi/3)` at depth <= 10 matches any of the 19
Standard-Model targets with surplus information over chance.

## Why the hit distribution is the diagnostic

Hits track measurement-window width and nothing else:

| target | rel. window | hits |
|---|---|---|
| a_e, 1/alpha, m_p/m_e, m_n/m_p | 1e-11 – 1e-10 | **0** |
| m_mu/m_e, a_mu | 2e-8 – 4e-7 | **0** |
| r_tau_e, 1/alpha(M_Z), sin^2 theta_W | 7e-5 – 2e-4 | 28 / 50 / 72 |
| koide_Q_up, higgs_lambda, ckm_lambda, koide_Q_down | 2e-3 – 5e-3 | 838 / 1130 / 2121 / 2098 |
| r_b_tau, r_t_b, alpha_s(M_Z) | 8e-3 – 1.1e-2 | 4747 / 4443 / 4933 |
| pmns_sin2_13/12/23 | 3.5e-2 – 6e-2 | 15212 / 26142 / 20799 |

The six most precisely measured quantities in the set return **exactly zero** across 42.5 million
values. The loosely measured mixing angles return tens of thousands. That is chance drawn to scale,
and every one of them died in the FDR gate.

## Corrections to my own estimator, recorded

The naive expected-count model N*2w OVERESTIMATES observed hits by ~100x (pmns_sin2_12: predicted
5.1e6, observed 26,142). The value set is not uniformly distributed -- it clusters -- so local density
near a given target is far below the global average. `BITS_RULE.py`'s chance figures inherit that
crudeness; the correct method is the empirical local-density estimate used in
`alpha_12pi_identity_audit_2026.py`. The conclusion is unaffected (zero certified is zero), but the
estimator was wrong and the thresholds in BITS_RULE should be read as conservative rather than exact.

## Two bugs found on the way, both mine, both caught by committed guards

1. **Shard-local record indices.** Each shard wrote `idx = len(vals)-1`, the global index in grind's
   serial build but shard-local in mine. The sweep compares `values[idx]` from the MERGED array against
   the record's stored value; they disagreed and grind's own `REBUILD MISMATCH` RuntimeError fired on
   the first loose target. Worse, `idx INTEGER PRIMARY KEY` meant colliding indices were silently
   REPLACED, so records were lost as well as misaligned. Fixed by remapping on `value_key` at merge
   time; verified 2,000 random records now align exactly. **Without that guard I would have swept
   against misaligned records and reported a null built on garbage.**
2. **Missing `build_meta` keys** (`splits`) that the sweep reads.

## What this does and does not establish

**Does:** no forced-germ expression at depth <= 10 matches any of the 19 SM targets past the gate,
exhaustively. Depths 3-9 were already exhaustive clean nulls; this extends the proven-empty range to 10.

**Does not:** say anything about depth 11+ (13.5 days sharded) or depth 12 (~16 days). It is one
vocabulary, one depth, one gate. And per `GATE_POWER_ANALYSIS.py`, single-target matching is
statistically empty past depth ~10-13 anyway -- so this is close to the last depth where an exhaustive
null carries information.

**Standing:** the SM sector is now walled by seven independent arguments -- number-field obstruction
(transcendental sqrt(pi) vs algebraic flavour data), period-ring weight-1 disjointness, the D3-D9
exhaustive nulls, THIS depth-10 exhaustive null, the RG dictionary gate (acceleration ratio vs energy
scale, ~38 orders), varying constants (atomic clocks bound the coupling to |p| <= 6e-8), and the
12 pi / alpha audit. a0's value, Z, s = -1 and omega_c remain POSTULATED. No theory is closed.
