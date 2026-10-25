# CD1_a0_cored_dwarf_ceiling — RESULT: CONSISTENT on both footings (a necessary condition only)

Frozen criteria c99930b2af (committed alone). Amendment A1 (`AMENDMENT_A1.md`): K2's check definition, made before any
graded number. κ = ½ FITTED; footings scored separately, never pooled; cold dark energy, not matter; nothing here says the
data favour the framework or ΛCDM; not "theory closed".

**Question.** Can X38's a₀-cored cold dark energy halos (Burkert, ρ₀r₀ = a₀/(2πG)) supply the faint dwarfs' route-E
requirement g_obs − g_N at r₁₂ for **any** core radius? A fixed-Σ Burkert halo is capped at g_h,max = 0.254484 a₀ at
every radius, whatever its r₀ (K1). The lane compares each dwarf's requirement with that cap, using X1's binary-corrected
Δ[Newton], so no halo-mass relation is extrapolated.

## Result (`cd1_dwarf_ceiling.out`)

| | canonical | alt |
|---|---|---|
| dwarfs graded | 89 | 89 |
| fraction above the cap at z ≥ 2 | **0.011** (Draco only, z +5.1) | **0.011** (Draco, z +2.1) |
| required surface density S (units of a₀/2πG), median / 84% / 97.5% | 0.53 / 1.11 / 2.49 | 0.44 / 0.90 / 1.90 |
| Spearman S vs log M★ / vs r_h | −0.02 / −0.28 | −0.02 / −0.28 |
| **class** | **CONSISTENT** | **CONSISTENT** |

By class (canonical median S): MW ultra-faints 0.51, MW classicals 0.88 (Draco 1.4), bright M31 0.39, M31 others 0.91,
M31 dE 1.46, LG field 0.67. Checks 5/5. MUTATE (separate outputs) 7/7: a weak discrepancy stays CONSISTENT, and a planted
3× requirement is EXCLUDED (0.60 above the cap). The MUTATE run exits 1, as frozen.

**Reading.** The dwarfs' extra pull fits **under** the a₀ surface-density cap. Most need about half of it at their
half-light radius. This is a necessary condition only: it says a suitable core radius exists for each dwarf, not that a
rule predicts it. Draco is the one clear exception on the canonical footing.

The faint-dwarf excess in the law picture becomes, in the cored-halo picture, a requirement that sits under Σ_a0. The heavy
cluster cores (X39) need about 2× Σ_a0, so in this picture clusters are the remaining problem, not dwarfs.

## Post-run diagnostic (NOT frozen, not graded: `cd1_postrun_r0_window.py`)

- Allowed core radii per dwarf (within 2σ of the requirement): median window 34–4004 pc (canonical) / 28–4947 pc (alt).
- No single r₀ fits 80% of dwarfs. The best shared r₀ is **164 pc** (fits 67 of 88) / **128 pc** (64 of 88).
- Context, not evidence: CFG870's empirical cored component had r_c ≈ 104 pc. SPARC galaxies in X38 have kpc-scale r₀.
  So in this picture r₀ must scale with the system; X40's fixed core radius would have to be checked against this.

Next test that would decide sufficiency: X38's own r₀ rule (halo mass from baryons), extrapolated to dwarfs and frozen
first, or any r₀ rule derived from the action. The dwarf windows above give the target.
