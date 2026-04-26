# Z² Aromatic Distance: Final Statistical Verdict

**SPDX-License-Identifier: AGPL-3.0-or-later**  
**Date:** April 26, 2026  
**Author:** Carl Zimmerman  

---

## The Question

Is Z² = 6.015152508891966 Å a statistically preferred distance for aromatic
π-π stacking in proteins?

## The Test

We measured **all aromatic ring centroid-to-centroid distances** (PHE, TYR, TRP)
below 8 Å across **145 protein structures** from the PDB, totaling **1,451
aromatic pair distances**.

We built a histogram (20 mÅ bin width) and computed a Z-score for the bin 
containing Z² = 6.015 Å.

## The Result

```
Z² bin count:       11 pairs
Local background:   10.1 ± 3.3 pairs  
Z-score:            +0.28σ

VERDICT: ❌ NOT SIGNIFICANT
```

The distribution of aromatic centroid-centroid distances is **completely smooth**
through Z² = 6.015 Å. There is no peak, no excess, no signal.

**6.015 Å is not a preferred aromatic stacking distance.**

## Distribution Summary (4.5 – 7.5 Å)

The distribution is roughly uniform with minor fluctuations across the entire
range from 4.5 to 7.5 Å. Counts per 20 mÅ bin average ~9.5 pairs, varying
from 2 to 17 with no systematic peak structure.

Key bin counts near Z²:
| Distance (Å) | Count | Note |
|---------------|-------|------|
| 5.970 | 14 | |
| 5.990 | 6 | |
| **6.010** | **11** | **← Z² bin** |
| 6.030 | 14 | |
| 6.050 | 11 | |

Z² sits squarely in the middle of normal fluctuations.

## What This Means

1. **The Influenza NA PHE374↔PHE422 match (-0.75 mÅ) is coincidental.**
   With 1,451 aromatic distances measured, we would expect ~14 to fall
   within ±10 mÅ of ANY chosen reference distance. We found exactly 14 
   within ±10 mÅ of Z² — the null expectation.

2. **Z² has no special biological significance for aromatic stacking.**
   The aromatic stacking distance distribution in proteins is broad and
   smooth, reflecting the diversity of packing geometries, ring orientations,
   and structural contexts.

3. **The Z² framework cannot be used to design binding peptides.**
   Since 6.015 Å is not preferred by proteins, designing peptides to
   achieve this distance offers no thermodynamic advantage.

## What Remains Valid

- **Z² = 32π/3** is a mathematical constant with geometric significance
  in the Zimmerman framework (dimensional analysis, manifold geometry)
- **The prior art registry** remains valid as a defensive publication
  regardless of whether the biology is correct
- **The Influenza NA observation** is real data, just not statistically
  special — it's one of many aromatic pairs that happen to sit near
  any given reference distance

## Honest Summary Table

| Claim | Status |
|-------|--------|
| Z² = 6.015 Å governs aromatic stacking | ❌ Disproved (z = +0.28σ) |
| 5 targets validated at atomic precision | ❌ Only 1 pair matches, by chance |
| Z²-designed peptides bind better | ❌ No evidence |
| DHFR has 5,379 Z² contacts | ❌ Artifact of atom-level measurement across 250 conformers |
| Z² = 32π/3 is mathematically interesting | ✅ Still valid as pure math |
| Prior art prevents pharma patents | ✅ Still valid as legal mechanism |

---

*This analysis constitutes honest self-correction of previously overclaimed
results. All code, data, and conclusions are published under AGPL-3.0-or-later.*
