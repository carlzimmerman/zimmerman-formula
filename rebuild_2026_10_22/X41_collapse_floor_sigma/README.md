# X41_collapse_floor_sigma: collapse gives the right mass slope for the cold dark energy core, at the wrong amplitude

Criteria: `FROZEN_CRITERIA.md` (0ea05957ee, committed alone). No amendment. Two implementation fixes before the first
graded number: the script used EM1's σ(M) from the closure where EM1 stores it, and the Burkert B was made
mutation-independent (this lane mutates ω̃). κ = ½ FITTED. Footings never pooled. Route E, Newtonian, cold dark energy not
matter. Not "theory closed". Nothing here says the data favour the framework.

**Rule CF.** Σ_core = max(a₀/(2πG), Σ_coll(M)). Σ_coll = 18π² ρ_m(z_f) r_f of the half-mass object at the Lacey–Cole EPS
median formation redshift. The inputs are the record's own CLASS P(k) and D(z) (EM1's backgrounds), with no ΛCDM
concentration relation and no new constant.

## Verdict: **CF INACTIVE** (both footings)

Σ_coll < Σ_a₀ everywhere: in 0 of 175 SPARC galaxies and 0 of 652 cluster cells. The rule reduces exactly to X38, with
X38's grades: SPARC passes; the heavy cores fail (MID T3 Z +4.3 / +3.8, MGAS T3 OUTER Z +5.4 / +4.9).

## The physics content

| M (M☉) | z_f (EPS) | Σ_coll (M☉ pc⁻²) |
|---|---|---|
| 10¹¹ | 1.14 | 3.8 |
| 10¹² | 0.94 | 6.8 |
| 10¹³ | 0.75 | 11.9 |
| 10¹⁴ | 0.56 | 20.5 |
| 10¹⁵ | 0.39 | 34.7 |

- **The slope matches.** Over 10¹³–10¹⁵ M☉, d ln Σ_coll / d ln M = **0.23**. X40b requires M^0.25–0.30 for the cluster
  cores. Collapse timing alone, from the record's own growth history, produces nearly the required climb.
- **The amplitude does not.** At the cluster median, Σ_coll / Σ_a₀ = 0.26 / 0.22, so the floor always wins. Reaching
  X40b's 3–5 × Σ_a₀ needs a multiplier η ≈ **11–19 (canonical) / 14–23 (alt)** on the collapsed object's ρr. That is a
  diagnostic, not adopted.
- **What η means.** The core of a collapsed halo is far denser than its virial mean; in standard language, η is a
  concentration factor. So the requirement sharpens to a concrete statement: **cold dark energy cores sit at the floor
  a₀/(2πG) in galaxies, and at ≈ 10–20 × the collapse ρr in groups and clusters, scaling with collapse time.** The record
  has no first-principles derivation of that factor (no ΛCDM concentration relation is allowed).

**Checks 5/5** (K0 EM1 law + X30 bands; K1 Burkert and EPS z_f equation residual 0; K2 EM1 σ₈ vs F3; K0x38 X38
reproduced; K3 0.66 GB). `--mutate` (ω̃ sign flipped) fails K1 (D(z_f) = 2.54 > 1), exit 1.

## Files

`FROZEN_CRITERIA.md`, `x41_collapse_floor.py`, `.out` / `_results.json`, `_MUTATE`, `x41_x30_machinery*.log`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x41_collapse_floor.py            # exit 0, 5/5
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x41_collapse_floor.py --mutate   # exit 1, K1 fails
