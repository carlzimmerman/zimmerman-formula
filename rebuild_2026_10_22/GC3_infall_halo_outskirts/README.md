# GC3_infall_halo_outskirts: cluster cold dark energy halo outskirts from self-similar infall

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (50c3953710).
- **A1** (0447a621c4): a code fix. The first run's saturation branch set r₀ = 10⁴ R500 and left almost no halo, so its
  "G-OUT-M3 +11.35" result is **withdrawn as an artefact**. X43's compact-root, saturate-at-peak convention replaces it.

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

**The halo.**
- **Shape:** a cored infall profile, ρ ∝ 1/[(1 + x)(1 + x²)^{5/8}], with outer slope −9/4 (X43's own GAM).
- **Core:** Σ = ρ₀ r₀ from X43's rule.
- **Normalisation:** M_cold(< R500) = 5.2715 × M_b(< R500), the native fair share of the baryons where they are measured.
- **Edge:** truncation at splashback, 0.364 r_ta.

## Verdict (frozen rule): **NOT REPAIRED: ROBUST on both footings**

**G-OUT-M3 still fails.** On R4 native infall it is +2.40 / +2.10 (h0672 / h0686), and G-MID-T3 newly fails (UNDER). No
rule passes the X43 line set.

**What the infall shape does fix (reported).** The cluster centres. G-IN-Mall moves from −2.37 (RX48 Burkert, FAIL OVER) to
−0.90 (RX48 infall, passes). The R4 / R5 / RX48 infall values are −0.46 / −0.76 / −0.90, and OUT-all improves to
−0.50 … −0.74. CF1's inner/outer c_f tension is therefore resolved by the derived infall shape on the inner side.

**What remains.** The most massive, gas-rich clusters (M3, MID-T3) need more cold dark energy at 0.5–3 Mpc than the fair
share of the baryons observed inside R500. Together with GC2 (counting gas to r_ta overshoots, M3 −5.0), this brackets the
outer budget between the fair share of the observed R500 baryons and that of the turnaround baryons.

**Structural note.** At X43's Σ, 106 of 1956 cluster-cells (5.4 %) cannot hold the fair share inside R500 even at the
saturation peak. These are flagged and reported.

## Checks: 6/6

- S0a reproduces X43 exactly.
- S0b: the profile matches quadrature to 4.8e-7, with outer slope −2.249 and inner slope 0.
- S0c: saturated cells, 5.4 %, flagged.
- K1: target mass hit to 3e-13.
- K2: construction checks.
- K3: 0.68 GB.
- **Pending:** the twin and the rerun.

## Files

- `gc3_infall.py`
- `gc3_infall.out` and `gc3_infall_results.json`
- `runs/`
