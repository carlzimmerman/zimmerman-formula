# X51_dwarf_cooling_floor: a cooling-threshold halo mass closes the dwarfs on canonical; on alt the ultra-faints overshoot

Criteria: `FROZEN_CRITERIA.md` (f029a8c37b, committed alone). No amendment. κ = ½ FITTED. Footings never pooled. Route E,
a₀-floor Burkert halos (X49). Cold dark energy is not matter. Not "theory closed". Nothing here says the data favour the
framework.

**Rule.** M200 = max(EM1 extrapolation, M_cool). M_cool is the first-principles atomic-cooling threshold: T_vir = 10⁴ K,
μ = 0.59, z_form = 8, record background A. It gives **M_cool = 1.13×10⁸ M☉** and lifts 65 of 82 dwarfs.

## Verdict (frozen): **UNDECIDED** (canonical: COOLING FLOOR FITS THE DWARFS; alt: FAIL, MW ultra-faint OVER)

| class | X49 | **canonical** E (Z) | **alt** E (Z) |
|---|---|---|---|
| MW ultra-faint (31) | +0.48 (+3.8) | **−0.22 (−1.91) ✓** | **−0.32 (−2.77) ✗** |
| bright M31 (25) | +0.18 | −0.08 (−0.73) ✓ | −0.10 (−0.87) ✓ |
| M31 others (5) | +0.57 | +0.03 (+0.09) ✓ | −0.04 (−0.10) ✓ |
| MW classical (8) | +0.13 | +0.02 (+0.24) ✓ | −0.03 (−0.42) ✓ |
| LG field (13) | −0.03 | −0.05 (−0.88) ✓ | −0.10 (−1.56) ✓ |
| Spearman(E, log M★) | −0.64 | **+0.13** | **+0.18** |

**Variants (reported):**
- H₂ cooling, 3.4×10⁶ M☉ at z = 8: UFD +0.04 / −0.01, bright M31 +0.18 / +0.16, M31 others +0.54 / +0.51.
- Atomic cooling at z = 6 / 10 gives UFD −0.20 / −0.24 (canonical) and −0.28 / −0.33 (alt).

**Checks 9/9** (K0 floor-off reproduces X49 to 1e-9; K1 T_vir(M_cool) = 10⁴ K; K2 the (1+z)^−3/2 scaling; X49's own
K0/K2; K3). `--mutate` (μ/10) fails K1, exit 1.

## Reading

- A first-principles formation threshold removes X49's ultra-faint shortfall and **the whole mass trend** that had followed
  the dwarfs since X19/X20/X24 (ρ −0.64 → +0.13 / +0.18). The trend came from halo masses extrapolated too low.
- **The truth sits between the two cooling limits.** Atomic cooling slightly over-predicts the ultra-faints (−0.22 / −0.32).
  H₂ cooling fits the ultra-faints (≈ 0) but leaves M31's faint dwarfs high (+0.5). The ultra-faints' halos lie between
  3×10⁶ and 10⁸ M☉, as standard reionization-fossil formation would also suggest. No single threshold is picked post hoc.
- **Crater II** is now strongly over-predicted (E −0.97). It is the cold, diffuse, tidally stripped satellite, and halo
  stripping is not modelled. NGC 147 is −0.43.
- **Consequence for the theory:** route E + the a₀ floor + a cooling-limited halo mass accounts for the LG dwarfs with no
  dwarf-specific constant. The verdict is undecided only because alt's ultra-faints overshoot at the atomic limit.
