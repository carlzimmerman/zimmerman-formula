# X49_dwarfs_route_e_floor: a₀-floor halos fit four of five Local Group dwarf classes; the MW ultra-faints are short

Criteria: `FROZEN_CRITERIA.md` (fa308d2c47, committed alone). No amendment. κ = ½ FITTED. Footings never pooled. Route E,
Newtonian, cold dark energy not matter. Not "theory closed". Nothing here says the data favour the framework.

Every dwarf sits far below the ~10¹² M☉ crossover (Σ_coll ≤ 3.8 ≪ 107 M☉ pc⁻²), so these are pure a₀-floor Burkert halos.
The result is independent of c_f.

## Verdict: **FAIL: MW ultra-faint (UNDER)**, both footings; the other four classes are REPRODUCED

| class | canonical E (Z) | alt E (Z) | median M200 (extrapolated) | median r₀ |
|---|---|---|---|---|
| LG field (13) | −0.034 (−0.49) ✓ | −0.068 (−0.95) ✓ | 2.7e8 | 0.25 kpc |
| MW classical (8) | +0.125 (+0.91) ✓ | +0.081 (+0.56) ✓ | 4.0e7 | 0.09 kpc |
| bright M31 (25) | +0.176 (+1.70) ✓ | +0.161 (+1.55) ✓ | 2.9e7 | 0.08 kpc |
| M31 others (5) | +0.571 (+1.71) ✓ | +0.544 (+1.59) ✓ | 3.1e6 | 0.02 kpc |
| **MW ultra-faint (31)** | **+0.476 (+3.80)** | **+0.459 (+3.66)** | 5.2e5 | 0.01 kpc |

**Checks 7/7** (K0 X24 medians; K1 floor and normalisation at 10¹²; K2 the no-halo limit equals X1's Newton; K3 0.12 GB).
`--mutate` (Σ/10) fails K1 and blows up every class, exit 1.

## Reading

- **No new constant**, and four dwarf classes fit. Under v3s the same dwarfs needed a separate ~4–5 km/s velocity floor
  (X24, X28; not in the action, X25). Route E's a₀-floor halos absorb that requirement, except for the faintest systems.
- **The ultra-faint shortfall** tracks the halo mass, which is the disclosed weak link. EM1's SPARC relation is extrapolated
  three to five decades below its range and gives M200 ≈ 5×10⁵ M☉, about 50× their stars. The fair-share variant (even
  smaller halos) is far worse (Z +8.3), so the data want **more massive** halos for the faintest dwarfs than the
  extrapolation gives, not a different core rule.
- **The mass trend survives:** Spearman(E, log M★) = −0.64, against X24's −0.63. The residual still grows toward low M★.
- **Not modelled:** tidal stripping of hosted halos. It would lower the predictions, i.e. worsen the ultra-faints.
- **Reported individuals:** Crater II −0.24 and Sagittarius −0.25 sit slightly below; Antlia II +0.32 and CVn I +0.37
  above.
- **Next, if pursued:** a framework-native halo-mass relation that extends below 10⁸ M☉ of baryons (the abundance of
  cold-dark-energy halos from the record's own P(k)) in place of the SPARC extrapolation.
