# LEE1_look_elsewhere: FROZEN CRITERIA (committed alone, before any LEE1 number)

**Question.** CL2 (b57ed8751f) found one setting (native slope S9, L = 4, switch T = 10^12.3, measured cluster budget) that
passes every graded line on the canonical footing. That setting was found after many settings were tried. How much of
the pass is the search itself?

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## Part A: census of settings tried (from committed result JSONs only)

Every configuration graded on X62's full line set is counted:
- CF1;
- CF2;
- CL1;
- CL2;
- CL3, once committed.

For each footing the census reports the number of configurations and the number passing every line. These lanes graded
the same full line set: SPARC on two backgrounds, 63 groups, 15 cluster keys in two h cells, five LG dwarf classes, and
KiDS lensing.

**Reported:**
- the raw pass fraction (passes / configurations) on canonical;
- the number of free knobs explored: T, c_f or L, shape, and the cluster budget on or off.

## Part B: pass fraction in the explored box (random draws, run when cores allow)

- **Setup:** CL2's harness, with shape S9, the measured cluster budget, and the switch at T.
- **Draws:** 24 points drawn uniformly in the explored box, T ∈ [12.0, 12.6] and L ∈ [3.5, 4.5], with numpy
  default_rng(20261027).
- **Graded:** both footings.
- **Primary statistic:** the canonical pass fraction p̂, with a Clopper–Pearson 68 % interval.

## Verdict (frozen; Part B)

| verdict | condition |
|---|---|
| **NARROW (tuned-looking)** | p̂ < 0.10. The passing region is a small part of what was searched, so the pass needs an independent derivation of T and L, or held-out success, before it counts as evidence |
| **MODERATE** | 0.10 ≤ p̂ < 0.40 |
| **BROAD** | p̂ ≥ 0.40. The pass does not hinge on fine settings within the box |

The alt footing is reported separately. Its known T- and L-independent failures (the SPARC line and the MW ultra-faints)
are expected to fail throughout.

## Checks and twin

- **K1.** Part A's counts reproduce each lane's committed configuration count.
- **K2.** Part B's draw list is reproducible from the seed (byte-identical).
- **K3.** Peak RSS < 1 GB.
- **MUTATE (`LEE1_MUTATE=1`, separate outputs).** It draws with seed + 1 and grades only 2 points. It must report a
  different draw list, so K2 fails against the frozen list.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I lee1.py`.
