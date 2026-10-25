# X44_self_similar_cf: self-similar infall alone gives c_f = 1.85, too low. X43 needs the standard formation concentration of about 4.

Criteria: `FROZEN_CRITERIA.md` (c8dd02f5aa, committed alone, with the paper estimate disclosed). No amendment. κ = ½
FITTED. Footings never pooled. Route E, Newtonian, cold dark energy not matter. Not "theory closed". Nothing here says the
data favour the framework.

## Derivation (frozen definition)

Bertschinger/Fillmore–Goldreich self-similar infall, ε = 1, so ρ ∝ r^(−9/4) and M ∝ r^{3/4}. Self-similar timing gives
M_ta ∝ t^{2/3}, with collapse at twice the turnaround time. The core is defined as the mass already collapsed when the
formation object's outer shell turned around:

    c_f,SS = 2^{2/(3ε(3−γ))} = 2^{8/9} = 1.852  (exact; numerical check to 1e-12)  →  η = 5.66

The structural ratios of the solution, read as "c", give 1.37–2.75: r_ta/r_vir = 2, and Bertschinger's first caustic
gives 2.75.

## Verdict: **SS FAILS** (both footings)

| | X43 (c_f 4, external) | **X44 (c_f 1.85, derived)** |
|---|---|---|
| SPARC | PASS | PASS (unchanged; galaxies sit on the a₀ floor) |
| groups Z | +2.05 | +2.48 / +2.29 FAIL |
| MID T3 | 2.06 (Z +0.3) | 1.40 (Z +2.9) FAIL |
| MID KT slope Z | +1.70 | +2.49 FAIL |
| MGAS T3 OUTER Z | +2.41 | +4.07 FAIL |

**Checks 3/3** (K0 c_f = 4 reproduces X43 exactly; K1 closed form = numerical = 2^{8/9}; K2 γ = 9/4). `--mutate`
(t_coll = t_ta) gives c_f = 1 and fails K1, exit 1.

## Reading

- **Self-similar infall alone is scale-free.** Its natural timing core sits at r_f/1.85, half as concentrated as needed.
  The concentration X43 uses (c_f ≈ 4) is the standard formation-epoch value, and it does not come out of the pure infall
  solution. It comes from the structure the infall picture leaves out: the halo grows from a peak of finite curvature,
  plus early mergers.
- **The data pin c_f tightly.** Interpolating X43's sensitivity, the groups reach Z = 2.0 at c_f ≈ 4.2 (both footings).
  The clusters' cores need about 4 as well. Two independent calibrations agree: X42's cluster-MID-only H1 implies 9–14 ×
  Σ_coll, which is c_f ≈ 3.3–4.6.
- **The status of the one number:** c_f ≈ 4–4.2 is required. It matches the standard simulated formation concentration,
  but it is not yet derived from first principles in the record. A peak-structure derivation would be the next step: the
  initial peak's curvature, not self-similar infall.

## Files

`FROZEN_CRITERIA.md`, `x44_self_similar_cf.py`, `.out` / `_results.json`, `_MUTATE`, `x44_regrade_cf4*` / `x44_regrade_cfSS*`
(X43 reruns), `x44_x30_machinery*.log`.
