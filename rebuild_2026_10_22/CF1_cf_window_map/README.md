# CF1_cf_window_map: is there one c_f that sets both the condensation threshold and the group/cluster cores?

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (ef5a07c251), committed alone before any script or number.
- **Harness:** X62's committed one (8c7768d26d), text-generated, with c_f as a scalar set consistently in X43 (`CF`, which
  also moves the switch threshold) and in X53 (`eta_of`). The background is inherited, as in X62.
- **Scope note:** the parenthetical list of c_f = 4 fails in criteria S0a was incomplete. It omitted alt's MW ultra-faint
  dwarfs and alt's SPARC line. The check compares the complete committed X62 list, which is what the criteria's main
  clause specifies.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Why this lane

The owner asked why condensation starts at about 10^12–10^12.5. In X62's environment rule, the threshold is X43's
crossover, η Σ_coll = a₀/(2πG), with η ∝ c_f^{5/4}. The same c_f sets the group and cluster cores. So the question was
whether one c_f does both jobs.

## Verdict (frozen rule): **NO SINGLE c_f** (grid 3.5–6.0, both footings)

**Threshold (crossover) per c_f, canonical / alt:**

| c_f | 3.5 | 4.0 | 4.25 | 4.5 | 4.75 | 5.0 | 5.25 | 5.5 | 6.0 |
|---|---|---|---|---|---|---|---|---|---|
| canonical | 12.39 | 12.09 | 11.96 | 11.83 | 11.72 | 11.60 | 11.50 | 11.40 | 11.21 |
| alt | 12.73 | 12.43 | 12.29 | 12.17 | 12.05 | 11.94 | 11.83 | 11.73 | 11.54 |

Values are log₁₀ M☉.

**Grid c_f values at which each line passes on both footings:**

| line | passing c_f |
|---|---|
| KiDS lensing | 3.5 only, which needs the threshold ≥ 10^12.39 (canonical) |
| groups | ≥ 4.75 |
| G-OUT-M3 (outskirts of the most gas-rich clusters) | ≥ 5.25 |
| G-IN-Mall (cluster centres) | ≤ 5.0 |
| SPARC line | ≥ 5.5 (alt fails it below that) |
| MW ultra-faint dwarfs | never on alt, at Z −2.77 independent of c_f (canonical passes) |

## The two binding tensions

1. **Threshold against concentration (lensing against groups).** Isolated KiDS lenses need the condensation threshold at
   or above about 10^12.4 M☉, so that they carry no halo. Groups need c_f ≳ 4.75. In X43's construction a higher c_f
   lowers the threshold, so one number cannot do both jobs. **The threshold therefore cannot be X43's core-floor
   crossover. It must be set by something independent of halo concentration, at about 10^12.4 M☉ or above.**
2. **Inner against outer cluster shape (M3 against G-IN-Mall).** The outskirts need c_f ≥ 5.25 and the centres need
   c_f ≤ 5.0. One Burkert profile cannot satisfy both. This matches GC1–GC3: the cluster halo's outer budget and its core
   concentration are separate degrees of freedom.

There is also a footing note. The alt footing fails the MW ultra-faint class at every c_f. That is a dwarf-side problem
(X51), not a c_f one.

## Checks: 10/10

- K0a/b/c reproduce X48 A2, X53 and X51.
- K2a/b: the halo branch off reproduces the law on SPARC and on lensing.
- S0a: c_f = 4 reproduces X62's reported_cf4 exactly.
- S0b: the crossover at c_f = 4 is 12.09 / 12.43.
- K1: the crossover is monotone in c_f.
- K2: the switch property holds at every point.
- K3: 0.64 GB.
- **Pending:** the twin and the rerun.

## Files

- `cf1_window.py`
- `cf1_window.out` and `cf1_window_results.json`
- the per-run `x62_*copy_*` outputs
