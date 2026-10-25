# X43_collapse_core_floor: one rule nearly closes the cold sector. It fails narrowly, on groups and the heaviest MGAS tercile.

Criteria: `FROZEN_CRITERIA.md` (00bc1a7950, committed alone, with the paper prediction disclosed before any graded
number). There is no amendment. One path fix was needed before the first graded run: the groups loader needed REPO.
κ = ½ FITTED. Footings never pooled. Route E: Newtonian, law emergent, cold dark energy not matter. Not "theory closed".
Nothing here says the data favour the framework.

## The rule (derived, no constant fitted)

    Σ_core(M) = max( a₀/(2πG),  η Σ_coll(M) ),   η = (4/(3B(1))) c_f^{5/4} = 14.83   [c_f = 4 EXTERNAL]

- Cold dark energy collapses like collisionless dust: Bertschinger's self-similar infall, ρ ∝ r^(−9/4).
- Its core is the inner 1/c_f of the half-mass object at the Lacey–Cole formation epoch, on the record's own P(k).
- It can never be cored more thinly than the framework's floor a₀/(2πG).
- The crossover falls at M ≈ 10^12.1 (canonical) / 10^12.4 (alt) M☉. Below it the a₀ floor rules; above it the collapse
  core rules.

## Verdict (frozen): **CC FAILS [c_f EXTERNAL]**, both footings, on two keys only

| | X38 (floor only) | **X43 (floor + collapse core)** |
|---|---|---|
| SPARC rms / median Υ (canonical; alt) | 0.0795 / 0.77 (0.0729 / 0.60) PASS | **0.0782 / 0.77 (0.0729 / 0.60) PASS** |
| groups, 63 (P4 estimator) | +0.097, Z +2.48 | **+0.084, Z +2.05** (line 2.0: FAIL by 0.05) |
| MID T3 | 1.05, Z **+4.26** | **2.06, Z +0.30** ✓ |
| MID T2 | Z +1.80 | Z −0.41 ✓ |
| MID KT slope | −0.04, Z **+3.07** | **+0.98, Z +1.70** ✓ |
| OUTER all-KT / terciles / slope | pass | pass (Z −1.15 to +1.29) |
| OUTER MGAS all | Z +2.36 | **Z +0.49** ✓ |
| **OUTER MGAS T3** | Z **+5.36** | **Z +2.41** (FAIL) |
| INNER (uninformative) | pass | pass (Z −1.0 / −1.2) |

On alt the grades are identical in class. **14 of 15 cluster keys pass**, against 10 of 15 for X38. The failures shrink
from Z up to 5.4 to Z 2.05 and 2.41.

**Reported, not adopted:** c_f = 5 (η = 19.6) puts the groups at CONSISTENT (Z +1.82), with only MGAS T3 OUTER failing.
c_f = 3 (η = 10.4) is worse. This is sensitivity only. c_f = 4 is the frozen value and is not moved.

**Checks 7/7** (K0 EM1 law + X30 bands; K1 Burkert, EPS and η = 14.83 with the exact mass match; K2 EM1 σ₈; K2b X41's
table; K0x38 X38 reproduced; K4 the 63 groups vs P4; K3 0.63 GB). `--mutate` (infall slope 3/2) fails K1 (η = 5.24),
exit 1.

## Reading

- **This is the closest the record has come.** One rule, built from the framework's floor a₀/(2πG) and ordinary
  self-similar collapse on the record's own growth history, takes three things at once:
  - SPARC, at the law's quality of fit (rms 0.073–0.078);
  - the cluster outskirts;
  - the heavy cluster cores, which every earlier model missed by 4–5σ.
  The galaxy groups move toward the data (Z 2.48 → 2.05).
- **What is left:**
  - groups at Z 2.05, just over the line;
  - the heaviest MGAS500 tercile's OUTER band at Z 2.41: predicted 1.12 against measured 1.37, still a little short.
  Both are under-predictions, so they ask for slightly denser cores at group and top-cluster masses. The reported
  c_f = 5 reads the same way.
- **The one external number is c_f = 4** (the formation-epoch concentration from ΛCDM-calibrated collapse studies). A
  first-principles c_f (from the infall solution itself) is the next derivation. If it comes out at 4–5 it would close
  the groups too.
- **What it means:** the cold sector is now one sentence. Cold dark energy collapses like dust, its cores carry the
  ordinary collapse concentration, and they can never be thinner than a₀/(2πG) = c²√(Λ/32π)/(2πG). Galaxies sit on the a₀
  floor, and groups and clusters sit on the collapse core. The galaxy law is then what the a₀ floor looks like. Adopting
  that is the owner's call.

## Files

`FROZEN_CRITERIA.md`, `x43_collapse_core.py`, `.out` / `_results.json`, `_MUTATE`, `x43_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x43_collapse_core.py            # exit 0, 7/7
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x43_collapse_core.py --mutate   # exit 1, K1 fails
